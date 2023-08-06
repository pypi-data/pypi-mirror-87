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

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "pkgdiff.h"

PyDoc_STRVAR(pkgdiff_compare_doc,
    "compare(path1, path2, exclude=None)\n"
    "--\n\n"
    "Compares by FreeBSD pkg metadata the files found at path1 and path2\n"
    "while ignoring all fields set in the iterable exclude.\n"
    "\n"
    "Returns False if pkg metadata differs otherwise True.\n"
);

static PyObject* pkgdiff_compare(PyObject *self, PyObject *args, PyObject* kws) {
  int ret = 0;
  PyObject* py_pkgname1 = NULL;
  PyObject* py_pkgname2 = NULL;
  PyObject* py_exclude = NULL;

  static char* keywords[] = {
    "pkgname1", "pkgname2", "exclude",
    NULL
  };

  if (!PyArg_ParseTupleAndKeywords(
          args, kws, "O&O&|O", keywords,
          PyUnicode_FSConverter, &py_pkgname1,
          PyUnicode_FSConverter, &py_pkgname2,
          &py_exclude))
    return NULL;

  const char** query = malloc(PKGDIFF_QUERY_LEN * sizeof(const char*));
  memcpy(query, PKGDIFF_QUERY, PKGDIFF_QUERY_LEN * sizeof(const char*));

  if (py_exclude != NULL) {
    PyObject* iterator = PyObject_GetIter(py_exclude);
    PyObject* item;

    if (iterator == NULL)
      return NULL;

    while ((item = PyIter_Next(iterator))) {
      if (!PyUnicode_CheckExact(item)) {
        PyErr_Format(PyExc_TypeError, "'%s' object is not a str",
                     Py_TYPE(item)->tp_name);
        Py_DECREF(item);
        break;
      }

      PyObject* ascii = PyUnicode_AsASCIIString(item);
      if (ascii == NULL) {
        Py_DECREF(item);
        break;
      }

      char* exclude = PyBytes_AsString(ascii);

      for (unsigned int i = 0; i < PKGDIFF_QUERY_LEN; i++) {
        if (query[i] != NULL && strcmp(query[i], exclude) == 0)
          query[i] = NULL;
      }

      Py_DECREF(ascii);
      Py_DECREF(item);
    }

    Py_DECREF(iterator);
  }

  if (!PyErr_Occurred()) {
    ret = pkgdiff(
        PyBytes_AS_STRING(py_pkgname1),
        PyBytes_AS_STRING(py_pkgname2),
        query,
        NULL
    );

    if (ret == -1)
      PyErr_SetFromErrno(PyExc_OSError);
  }

  free(query);
  Py_DECREF(py_pkgname1);
  Py_DECREF(py_pkgname2);

  if (PyErr_Occurred())
    return NULL;

  return PyBool_FromLong(!ret);
}

static PyMethodDef pkgdiff_methods[] = {
  { "compare", (PyCFunction) pkgdiff_compare,
    METH_VARARGS | METH_KEYWORDS,
    pkgdiff_compare_doc },
  { NULL, NULL, 0, NULL }
};

static struct PyModuleDef pkgdiff_module = {
  PyModuleDef_HEAD_INIT,
  "pkgdiff",
  NULL,
  -1,
  pkgdiff_methods
};

PyMODINIT_FUNC PyInit_pkgdiff(void) {
  return PyModule_Create(&pkgdiff_module);
}
