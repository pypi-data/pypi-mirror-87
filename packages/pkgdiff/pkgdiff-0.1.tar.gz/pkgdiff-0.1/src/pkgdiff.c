/* Copyright 2020 Florian Wagner <florian@wagner-flo.net>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <mba/diff.h>
#include <pkg.h>
#include "pkgdiff.h"

const char* PKGDIFF_QUERY[PKGDIFF_QUERY_LEN] = {
  "name",
  "version",
  "origin",
  "prefix",
  "categories",
  "maintainer",
  "comment",
  "description",
  "licenses",
  "homepage",
  "architecture",
  "messages",
  "options",
  "annotations",
  "users",
  "groups",
  "dependencies",
  "required_libraries",
  "files",
  "directories",
  "provided_libraries"
};

int pkgdiff_errno = 0;

static const char* PKGDIFF_FORMAT[PKGDIFF_QUERY_LEN] = {
  "%n",
  "%v",
  "%o",
  "%p",
  "%C%{%Cn\n%}",
  "%m",
  "%c",
  "%e",
  "%L",
  "%w",
  "%q",
  "%M",
  "%O%{%On: %Ov [default: %Od] <%OD>\n%}",
  "%A%{%An: %Av\n%}",
  "%U%{%Un, %|%}",
  "%G%{%Gn\n%}",
  "%d%{%dn-%dv (%do)\n%}",
  "%B%{%Bn\n%}",
  "%F%{%Fn %Fu:%Fg:%Fp %Fs\n%}",
  "%D%{%Dn %Du:%Dg:%Dp\n%}",
  "%b%{%bn\n%}"
};

static char* get_info(struct pkg* pkg, const char* format) {
  char* ret = NULL;
  pkg_asprintf(&ret, format, pkg);
  if (ret == NULL)
    asprintf(&ret, "");
  return ret;
}

static struct pkg* open_pkg(const char* filename) {
  struct pkg* pkg = NULL;
  struct pkg_manifest_key* keys = NULL;

  pkg_manifest_keys_new(&keys);

  if (pkg_open(&pkg, filename, keys, 0) != EPKG_OK) {
    pkgdiff_errno = errno;
  }

  pkg_manifest_keys_free(keys);

  return pkg;
}

static const unsigned int find_lines(const char* str, struct varray* lines) {
  const char* start = str;
  const char* end = str + strlen(str);
  unsigned int num = 0;
  size_t lb = 0;

  do {
    lb = strcspn(start, "\n");
    struct pkgdiff_lineref* l = varray_get(lines, num++);
    l->start = start;
    l->length = lb;
    start = start + lb + 1;
  } while(start < end);

  return num;
}

static const void* diff_idx(const void* s, int idx, void* context) {
  return varray_get((struct varray*)s, idx);
}

static int diff_cmp(const void* e1, const void* e2, void* context) {
  struct pkgdiff_lineref* a = (struct pkgdiff_lineref*) e1;
  struct pkgdiff_lineref* b = (struct pkgdiff_lineref*) e2;

  if (a->length == b->length)
    return strncmp(a->start, b->start, a->length);

  return 1;
}

static int diff_lines(
    const char* a,
    const char* b,
    const char* name,
    pkgdiff_result_fn result_fn)
{
  struct varray* lines_a = varray_new(sizeof(struct pkgdiff_lineref), NULL);
  struct varray* lines_b = varray_new(sizeof(struct pkgdiff_lineref), NULL);

  unsigned int num_lines_a = find_lines(a, lines_a);
  unsigned int num_lines_b = find_lines(b, lines_b);

  struct varray* ses = varray_new(sizeof(struct diff_edit), NULL);
  int ses_len;
  int d = diff(lines_a, 0, num_lines_a,
               lines_b, 0, num_lines_b,
               &diff_idx, &diff_cmp, NULL,
               0,
               ses, &ses_len,
               NULL);

  if (d > 0 && result_fn != NULL) {
    struct pkgdiff_result* dr = malloc(ses_len + sizeof(struct pkgdiff_result));

    for (int i = 0; i < ses_len; i++) {
      struct diff_edit* e = varray_get(ses, i);

      dr[i].lines_len = e->len;
      dr[i].lines = malloc(e->len * sizeof(struct pkgdiff_lineref*));

      switch (e->op) {
        case DIFF_MATCH:  dr[i].op = PKGDIFF_RESULT_MATCH;  break;
        case DIFF_DELETE: dr[i].op = PKGDIFF_RESULT_DELETE; break;
        case DIFF_INSERT: dr[i].op = PKGDIFF_RESULT_INSERT; break;
      };

      for (int j = e->off; j < e->len + e->off; j++) {
        dr[i].lines[j - e->off] = varray_get(e->op == DIFF_INSERT ? lines_b : lines_a, j);
      }
    }

    result_fn(name, dr, ses_len);

    for (int i = 0; i < ses_len; i++) {
      free(dr[i].lines);
    }

    free(dr);
  }

  varray_deinit(ses);
  varray_deinit(lines_a);
  varray_deinit(lines_b);

  return d;
}

int pkgdiff(
    const char* pkgname1,
    const char* pkgname2,
    const char* query[],
    pkgdiff_result_fn result_fn)
{
  int ret = 0;
  int res = 0;

  struct pkg* pkg1 = open_pkg(pkgname1);
  if (pkg1 == NULL){
    return -1;
  }

  struct pkg* pkg2 = open_pkg(pkgname2);
  if (pkg2 == NULL) {
    pkg_free(pkg1);
    return -1;
  }

  char* info1 = NULL;
  char* info2 = NULL;

  for (unsigned int i = 0; i < PKGDIFF_QUERY_LEN; i++) {
    const char* name = PKGDIFF_QUERY[i];
    const char* format = NULL;

    for (unsigned int j = 0; j < PKGDIFF_QUERY_LEN; j++) {
      if (query[j] == NULL || strcmp(query[j], name) != 0)
        continue;

      format = PKGDIFF_FORMAT[i];
      break;
    }

    if (format == NULL)
      continue;

    info1 = get_info(pkg1, format);
    info2 = get_info(pkg2, format);

    if (result_fn != NULL) {
      res = diff_lines(info1, info2, name, result_fn);

      if (res == -1) {
        pkgdiff_errno = errno;
        ret = -1;
      }
      else if (res > 0) {
        ret = 1;
        res = 0;
      }
    }
    else {
      if (strcmp(info1, info2) != 0)
        ret = res = 1;
    }

    free(info1);
    free(info2);

    if (res != 0)
      break;
  }

  pkg_free(pkg1);
  pkg_free(pkg2);

  return ret;
}
