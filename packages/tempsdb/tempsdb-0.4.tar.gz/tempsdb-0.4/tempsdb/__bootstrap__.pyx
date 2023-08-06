import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "chunks.h":
    object PyInit_098453e7fba2624bf5714994461fa40a0c8e9251a5f8a7565a488780d62b3e62()
cdef extern from "database.h":
    object PyInit_5db63b8c729a89de00e66094d36cc1b2628bd576e1c271db1c92e0bb29060672()
cdef extern from "exceptions.h":
    object PyInit_2be46c4ad35b201ad53a980bb3ce2c4bc299b2010075e3af5895c0f88f761c67()
cdef extern from "iterators.h":
    object PyInit_40b3c0a986099b9423ad21003b959a9e014cf9473240bce6a8d15a615d42029e()
cdef extern from "series.h":
    object PyInit_9a8997c77487ce3b0ae10b024e1a7e371c74338da4e4832ca79c67e6db2bca9f()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.chunks":
        return PyInit_098453e7fba2624bf5714994461fa40a0c8e9251a5f8a7565a488780d62b3e62()
    elif name == "tempsdb.database":
        return PyInit_5db63b8c729a89de00e66094d36cc1b2628bd576e1c271db1c92e0bb29060672()
    elif name == "tempsdb.exceptions":
        return PyInit_2be46c4ad35b201ad53a980bb3ce2c4bc299b2010075e3af5895c0f88f761c67()
    elif name == "tempsdb.iterators":
        return PyInit_40b3c0a986099b9423ad21003b959a9e014cf9473240bce6a8d15a615d42029e()
    elif name == "tempsdb.series":
        return PyInit_9a8997c77487ce3b0ae10b024e1a7e371c74338da4e4832ca79c67e6db2bca9f()


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
    modules_set = {'tempsdb.database', 'tempsdb.exceptions', 'tempsdb.iterators', 'tempsdb.chunks', 'tempsdb.series'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
