import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "basics.h":
    object PyInit_01b3f3da5b6c26e2b9a2f033216db3537f7c08fc2e864eee931479ef8e0dbb14()
cdef extern from "quadtrees.h":
    object PyInit_979ee60454aaf9f36e79b43f29e75653a65769c014c4135b15786d82885f42fc()

cdef object get_definition_by_name(str name):
    if name == "line_intersect_2d.basics":
        return PyInit_01b3f3da5b6c26e2b9a2f033216db3537f7c08fc2e864eee931479ef8e0dbb14()
    elif name == "line_intersect_2d.quadtrees":
        return PyInit_979ee60454aaf9f36e79b43f29e75653a65769c014c4135b15786d82885f42fc()


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
    modules_set = {'line_intersect_2d.basics', 'line_intersect_2d.quadtrees'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
