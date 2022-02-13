
// Easy "flattened" definition
typedef struct {
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
    Py_ssize_t ob_size;
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;




// More realistic hierarchy (macros expanded)

// cpython/Include/object.h
typedef struct _object {
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
} PyObject;

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;
} PyVarObject;

// cpython/Include/cpython/listobject.h
typedef struct {
    PyVarObject ob_base;
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;


// cpython/Objects/listobject.c
static PyObject *
list___sizeof___impl(PyListObject *self)
{
    Py_ssize_t res;

    res = _PyObject_SIZE(Py_TYPE(self)) + self->allocated * sizeof(void*);
    return PyLong_FromSsize_t(res);
}