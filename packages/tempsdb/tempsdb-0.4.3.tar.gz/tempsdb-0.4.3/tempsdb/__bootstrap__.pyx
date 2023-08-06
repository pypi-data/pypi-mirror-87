import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "chunks.h":
    object PyInit_24c5247d5cd175718ac541d18f17ec09ec3525c9d64f8a11b1f1cee8b5e18948()
cdef extern from "database.h":
    object PyInit_7f500c1b24221567e3ca4d2ea837e7f21878fd356f1a1621cdc202aab0167876()
cdef extern from "exceptions.h":
    object PyInit_65cc43e772beef224eb2255b8111090653f5aa24d96797c3ea2bef2b95d438ae()
cdef extern from "iterators.h":
    object PyInit_0314d11262188913b326227df9c8e56071bd320df0715424bf22ac73d0004cfd()
cdef extern from "series.h":
    object PyInit_19c62a47181e00b58c280db11d96509117b8a0fb643fdb6ef8a0c2f769dfdb88()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.chunks":
        return PyInit_24c5247d5cd175718ac541d18f17ec09ec3525c9d64f8a11b1f1cee8b5e18948()
    elif name == "tempsdb.database":
        return PyInit_7f500c1b24221567e3ca4d2ea837e7f21878fd356f1a1621cdc202aab0167876()
    elif name == "tempsdb.exceptions":
        return PyInit_65cc43e772beef224eb2255b8111090653f5aa24d96797c3ea2bef2b95d438ae()
    elif name == "tempsdb.iterators":
        return PyInit_0314d11262188913b326227df9c8e56071bd320df0715424bf22ac73d0004cfd()
    elif name == "tempsdb.series":
        return PyInit_19c62a47181e00b58c280db11d96509117b8a0fb643fdb6ef8a0c2f769dfdb88()


cdef class CythonPackageLoader:
    cdef PyModuleDef* definition
    cdef object def_o
    cdef str name

    def __init__(self, name):
        self.def_o = get_definition_by_name(name)
        self.definition = <PyModuleDef*>self.def_o
        self.name = name
        Py_INCREF(self.def_o)

    def load_module(self, fullname):
        raise ImportError

    def create_module(self, spec):
        if spec.name != self.name:
            raise ImportError()
        return PyModule_FromDefAndSpec(self.definition, spec)

    def exec_module(self, module):
        PyModule_ExecDef(module, self.definition)


class CythonPackageMetaPathFinder:
    def __init__(self, modules_set):
        self.modules_set = modules_set

    def find_module(self, fullname, path):
        if fullname not in self.modules_set:
            return None
        return CythonPackageLoader(fullname)

    def invalidate_caches(self):
        pass

def bootstrap_cython_submodules():
    modules_set = {'tempsdb.series', 'tempsdb.iterators', 'tempsdb.exceptions', 'tempsdb.chunks', 'tempsdb.database'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
