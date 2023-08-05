#include <Python.h>
#include "binary_c_python.h"

/*
 * binary_c/PYTHON API interface functions
 *
 * Remember: variables must be passed by references
 * (i.e. as pointers).
 *
 * See apitest.py for an example of how to use these functions.
 *
 * See also
 * http://www-h.eng.cam.ac.uk/help/tpl/languages/mixinglanguages.html
 * https://realpython.com/build-python-c-extension-module/
 * https://docs.python.org/3/extending/extending.html
 * https://docs.python.org/3/c-api/arg.html#c.PyArg_ParseTuple
 * https://realpython.com/python-bindings-overview/
 * http://scipy-lectures.org/advanced/interfacing_with_c/interfacing_with_c.html
 */

// TODO: Put in clear debug statements
/* list of variables used in the Py<>C interface */

/************************************************************/
/*
 * function prototypes : these are the functions
 * called by PYTHON code, without the trailing underscore.
 */
/************************************************************/

/* Preparing all the functions of the module */
// Docstrings
static char module_docstring[] MAYBE_UNUSED =
    "This module is a python3 wrapper around binary_c";

#ifdef __DEPRECATED
static char create_binary_docstring[] =
    "Allocate memory for a binary";
#endif
static char function_prototype_docstring[] =
    "The prototype for a binary_c python function";
static char new_binary_system_docstring[] =
    "Return an object containing a binary, ready for evolution";

// Evolution function docstrings
static char run_system_docstring[] = 
    "Function to run a system. This is a general function that will be able to handle different kinds of situations: single system run with different settings, population run with different settings, etc. To avoid having too many functions doing slightly different things. \n\nArguments:\n\targstring: argument string for binary_c\n\t(opt) custom_logging_func_memaddr: memory address value for custom logging function. Default = -1 (None)\n\t(opt) store_memaddr: memory adress of the store. Default = -1 (None)\n\t(opt) write_logfile: Boolean (in int form) for whether to enable the writing of the log function. Default = 0\n\t(opt) population: Boolean (in int form) for whether this system is part of a population run. Default = 0.";

// Utility function docstrings
static char return_arglines_docstring[] =
    "Return the default args for a binary_c system";
static char return_help_info_docstring[] = 
    "Return the help info for a given parameter";
static char return_help_all_info_docstring[] = 
    "Return an overview of all the parameters, their description, categorized in sections";
static char return_version_info_docstring[] = 
    "Return the version information of the used binary_c build";

// other functionality
static char return_store_memaddr_docstring[] = 
    "Return the store memory adress that will be passed to run_population";
static char return_persistent_data_memaddr_docstring[] = 
    "Return the store memory adress that will be passed to run_population";

static char free_persistent_data_memaddr_and_return_json_output_docstring[] = 
    "Frees the persistent_data memory and returns the json output";
static char free_store_memaddr_docstring[] = 
    "Frees the store memaddr";

static struct libbinary_c_store_t *store = NULL;

/* Initialize pyobjects */
// Old functions. Can be removed I think
#ifdef __DEPRECATED
static PyObject* binary_c_create_binary(PyObject *self, PyObject *args);
#endif
static PyObject* binary_c_function_prototype(PyObject *self, PyObject *args);
static PyObject* binary_c_new_binary_system(PyObject *self, PyObject *args);

// Evolution function headers
static PyObject* binary_c_run_system(PyObject *self, PyObject *args, PyObject *kwargs);

// Utility function headers
static PyObject* binary_c_return_arglines(PyObject *self, PyObject *args);
static PyObject* binary_c_return_help_info(PyObject *self, PyObject *args);
static PyObject* binary_c_return_help_all_info(PyObject *self, PyObject *args);
static PyObject* binary_c_return_version_info(PyObject *self, PyObject *args);

// Other function headers
static PyObject* binary_c_return_store_memaddr(PyObject *self, PyObject *args);
static PyObject* binary_c_return_persistent_data_memaddr(PyObject *self, PyObject *args);

// Free functions
static PyObject* binary_c_free_persistent_data_memaddr_and_return_json_output(PyObject *self, PyObject *args);
static PyObject* binary_c_free_store_memaddr(PyObject *self, PyObject *args);

/* Set the module functions */
static PyMethodDef module_methods[] = {
#ifdef __DEPRECATED
    {"create_binary", 
        binary_c_create_binary, 
        METH_VARARGS, 
        create_binary_docstring
    },
#endif
    {"function_prototype", binary_c_function_prototype, METH_VARARGS, function_prototype_docstring},
    {"new_system", binary_c_new_binary_system, METH_VARARGS, new_binary_system_docstring},

    {"run_system", (PyCFunction)binary_c_run_system, METH_VARARGS|METH_KEYWORDS, run_system_docstring}, 
    // Wierdly, this casting to a PyCFunction, which usually takes only 2 args, now works when giving keywords. See https://stackoverflow.com/q/10264080

    {"return_arglines", binary_c_return_arglines, METH_VARARGS, return_arglines_docstring},
    {"return_help", binary_c_return_help_info, METH_VARARGS, return_help_info_docstring},
    {"return_help_all", binary_c_return_help_all_info, METH_VARARGS, return_help_all_info_docstring},
    {"return_version_info", binary_c_return_version_info, METH_VARARGS, return_version_info_docstring},

    {"return_store_memaddr", binary_c_return_store_memaddr, METH_VARARGS, return_store_memaddr_docstring},
    {"return_persistent_data_memaddr", binary_c_return_persistent_data_memaddr, METH_NOARGS, return_persistent_data_memaddr_docstring},

    {"free_persistent_data_memaddr_and_return_json_output", binary_c_free_persistent_data_memaddr_and_return_json_output, METH_VARARGS, free_persistent_data_memaddr_and_return_json_output_docstring},
    {"free_store_memaddr", binary_c_free_store_memaddr, METH_VARARGS, free_store_memaddr_docstring},

    {NULL, NULL, 0, NULL}
};

/* ============================================================================== */
/* Making the module                                                              */
/* ============================================================================== */

/* Initialise the module. Removed the part which supports python 2 here on 17-03-2020 */
/* Python 3+ */
static struct PyModuleDef Py__binary_c_bindings =
{
    PyModuleDef_HEAD_INIT,
    "_binary_c_bindings", /* name of module */
    "TODO",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit__binary_c_bindings(void)
{
    return PyModule_Create(&Py__binary_c_bindings);
}

/* ============================================================================== */
/* Some function that we started out with. Unused now.                            */
/* ============================================================================== */

#ifdef __DEPRECATED
static PyObject* binary_c_create_binary(PyObject *self, PyObject *args)
{

    double var1, var2;
    char * empty_str = "";
    int i;
    const int N = 1;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "dd", &var1, &var2))
        return NULL;


    /* Binary structures */
    struct libbinary_c_stardata_t *stardata[N];
    struct libbinary_c_store_t *store = NULL;

    /* Allocate memory for binaries */
    for(i=0;i<N;i++){
        stardata[i] = NULL;
        binary_c_new_system(&stardata[i], NULL, NULL, &store, NULL, &empty_str, -1);
    }

    /* Return the evolved binary */
    PyObject *ret = Py_BuildValue("");

    return ret;
}
#endif //__DEPRECATED


static PyObject* binary_c_new_binary_system(PyObject *self, PyObject *args)
{
    /* Binary structures */
    struct libbinary_c_stardata_t *stardata;

    /* Allocate memory for binaries */
    char * empty_str = "";
    stardata = NULL;
    binary_c_new_system(&stardata, NULL, NULL, &store, NULL, &empty_str, -1);
    
    /* Return an object containing the stardata */
    PyObject *ret = Py_BuildValue("");
    return ret;
}

static PyObject* binary_c_function_prototype(PyObject *self, PyObject *args)
{

    // This function is an very bare example of how a function would look like.

    double var1, var2;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "dd", &var1, &var2))
    {
        return NULL;
    }
    else
    {
        /* Return the evolved binary */
        PyObject *ret = Py_BuildValue("");
        return ret;
    }
}

/*
    Below are the real functions:
    binary_c_run_population
    binary_c_run_system

    binary_c_return_arglines
    binary_c_return_help_info
    binary_c_return_help_all_info
    binary_c_return_version_info
*/

/* ============================================================================== */
/* Wrappers to functions that evolve binary systems.                              */
/* ============================================================================== */

static PyObject* binary_c_run_system(PyObject *self, PyObject *args, PyObject *kwargs)
{

    static char* keywords[] = {"argstring", "custom_logging_func_memaddr", "store_memaddr", "persistent_data_memaddr", "write_logfile", "population", NULL};

    /* set vars and default values for some*/
    char *argstring;
    long int custom_logging_func_memaddr = -1;
    long int store_memaddr = -1;
    long int persistent_data_memaddr = -1;
    int write_logfile = 0;
    int population = 0;

    // By using the keywords argument it scans over the given set of kwargs, but if they are not given then the default value is used
    /* Parse the input tuple */
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "s|lllii", keywords, &argstring, &custom_logging_func_memaddr, &store_memaddr, &persistent_data_memaddr, &write_logfile, &population))
    {
        return NULL;
    }

    // printf("Input persistent_Data_memaddr: %lu\n", persistent_data_memaddr);

    /* Call c-function */
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = run_system(argstring,                    // the argstring
                                      custom_logging_func_memaddr,  // memory adress for the function for custom logging
                                      store_memaddr,                // memory adress for the store object
                                      persistent_data_memaddr,      // memory adress for the persistent data
                                      write_logfile,                // boolean for whether to write the logfile
                                      population,                   // boolean for whether this is part of a population.
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    /* Display error */
    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_run_system): %s\n",
                error_buffer);
    }

    Safe_free(buffer);
    Safe_free(error_buffer);

    // TODO: fix that the return_error_string is returned.
    return return_string;
}

/* ============================================================================== */
/* Wrappers to functions that call other API functionality like help and arglines */
/* ============================================================================== */

static PyObject* binary_c_return_arglines(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_arglines(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_arglines): %s\n",
                error_buffer);
    }

    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_help_info(PyObject *self, PyObject *args)
{
    /* Parse the input tuple */
    char *argstring;
    
    if(!PyArg_ParseTuple(args, "s", &argstring))
    {
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_help_info(argstring,
                                          &buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_help_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_help_all_info(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_help_all_info(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_help_all_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_version_info(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_version_info(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_version_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

/* ============================================================================== */
/* Wrappers to functions that call other functionality */
/* ============================================================================== */

static PyObject* binary_c_return_store_memaddr(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    long int out MAYBE_UNUSED = return_store_memaddr(&buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    PyObject * store_memaddr = Py_BuildValue("l", out);
    // printf("store_memaddr: %ld\n", out);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_store_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return store_memaddr;
}

static PyObject* binary_c_return_persistent_data_memaddr(PyObject *self, PyObject *args)
{
    /* Python binding that wraps the c function which calls the binary_c api endpoint. */
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    long int out MAYBE_UNUSED = return_persistent_data_memaddr(&buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    PyObject * persistent_data_memaddr = Py_BuildValue("l", out);
    // printf("persistent_data_memaddr: %ld\n", out);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_persistent_data_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return persistent_data_memaddr;
}

/* Memory freeing functions */
static PyObject* binary_c_free_persistent_data_memaddr_and_return_json_output(PyObject *self, PyObject *args)
{
    /* Python binding that calls the c function that free's the persistent data memory and prints out the json */

    long int persistent_data_memaddr = -1;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "l", &persistent_data_memaddr))
    {
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;

    long int out MAYBE_UNUSED = free_persistent_data_memaddr_and_return_json_output(persistent_data_memaddr,
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_free_persistent_data_memaddr_and_return_json_output): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_free_store_memaddr(PyObject *self, PyObject *args)
{
    /* Python binding that calls the c function that free's the store memory */
    long int store_memaddr = -1;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "l", &store_memaddr))
    {
        // printf("Error: got a bad input\n");
        fprintf(stderr,
                "Error (in function: binary_c_free_store_memaddr): Got a bad input\n");
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;

    long int out MAYBE_UNUSED = free_store_memaddr(store_memaddr,
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        // printf("Error (in function: binary_c_free_store_memaddr): %s", error_buffer);
        fprintf(stderr,
                "Error (in function: binary_c_free_store_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return Py_BuildValue("");
}
