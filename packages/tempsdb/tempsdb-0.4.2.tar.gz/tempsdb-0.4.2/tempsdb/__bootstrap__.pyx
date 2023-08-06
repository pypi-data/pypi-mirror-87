import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "chunks.h":
    object PyInit_2b08b29c0643e7c5a767048f5323af2bb07066cbadcb5374b3530f7c61ff87a6()
cdef extern from "database.h":
    object PyInit_75ed4ef179a1f6762374f207f43eb4020b9336df4d3ae6233d67a716d0772a4b()
cdef extern from "exceptions.h":
    object PyInit_2be46c4ad35b201ad53a980bb3ce2c4bc299b2010075e3af5895c0f88f761c67()
cdef extern from "iterators.h":
    object PyInit_4e190efa9be68aefac8d8f5de6ffeab193e012449e9d16ea3eab94402ada0732()
cdef extern from "series.h":
    object PyInit_c400903c75c92d0d2dc851e6771bab10435fe536c2c85ca9bda829144732d97c()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.chunks":
        return PyInit_2b08b29c0643e7c5a767048f5323af2bb07066cbadcb5374b3530f7c61ff87a6()
    elif name == "tempsdb.database":
        return PyInit_75ed4ef179a1f6762374f207f43eb4020b9336df4d3ae6233d67a716d0772a4b()
    elif name == "tempsdb.exceptions":
        return PyInit_2be46c4ad35b201ad53a980bb3ce2c4bc299b2010075e3af5895c0f88f761c67()
    elif name == "tempsdb.iterators":
        return PyInit_4e190efa9be68aefac8d8f5de6ffeab193e012449e9d16ea3eab94402ada0732()
    elif name == "tempsdb.series":
        return PyInit_c400903c75c92d0d2dc851e6771bab10435fe536c2c85ca9bda829144732d97c()


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
    modules_set = {'tempsdb.series', 'tempsdb.exceptions', 'tempsdb.iterators', 'tempsdb.chunks', 'tempsdb.database'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
