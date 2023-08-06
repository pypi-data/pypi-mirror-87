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

#ifndef PKGDIFF_PKGDIFF_H
#define PKGDIFF_PKGDIFF_H

#define PKGDIFF_RESULT_MATCH  ' '
#define PKGDIFF_RESULT_DELETE '-'
#define PKGDIFF_RESULT_INSERT '+'

#define PKGDIFF_QUERY_LEN 21
extern const char* PKGDIFF_QUERY[PKGDIFF_QUERY_LEN];

extern int pkgdiff_errno;

struct pkgdiff_lineref {
    const char* start;
    size_t length;
};

struct pkgdiff_result {
    char op;
    struct pkgdiff_lineref** lines;
    unsigned int lines_len;
};

typedef void (*pkgdiff_result_fn)(
    const char* info,
    struct pkgdiff_result* diff,
    unsigned int diff_len
);

int pkgdiff(
    const char* pkgname1,
    const char* pkgname2,
    const char* query[],
    pkgdiff_result_fn result
);

#endif /* PKGDIFF_PKGDIFF_H */
