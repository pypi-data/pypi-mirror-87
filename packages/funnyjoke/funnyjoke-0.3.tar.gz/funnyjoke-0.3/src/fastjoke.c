#include <Python.h>

static PyObject* tell(PyObject* self, PyObject* args)
{
    printf("Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... ");
	printf("Beiherhund das Oder die Flipperwaldt gersput.");
    return Py_None;
}

static PyMethodDef myMethods[] = {
    { "tell", tell, METH_NOARGS, "Tells a fast joke" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef fastjoke = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Test Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_fastjoke(void)
{
    return PyModule_Create(&fastjoke);
}
