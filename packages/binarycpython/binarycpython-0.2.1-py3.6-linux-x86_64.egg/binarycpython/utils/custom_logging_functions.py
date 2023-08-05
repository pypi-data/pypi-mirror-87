"""
Module containing functions for the custom logging functionality.
The functions here make it possible for the user to define binaryc output logs on runtime
"""

import os
import textwrap
import subprocess
import socket
import ctypes
import uuid

from binarycpython.utils.functions import temp_dir, remove_file


def autogen_C_logging_code(logging_dict, verbose=0):
    """
    Function that autogenerates PRINTF statements for binaryc.
    Input is a dictionary where the key is the header of that logging line
    and items which are lists of parameters that will be put in that logging line

    Example::
        {'MY_STELLAR_DATA':
            [
                'model.time',
                'star[0].mass',
                'model.probability',
                'model.dt'
            ]
        }
        
    """

    # Check if the input is of the correct form
    if not isinstance(logging_dict, dict):
        print("Error: please use a dictionary as input")
        return None

    code = ""
    # Loop over dict keys
    for key in logging_dict:
        if verbose > 0:
            print(
                "Generating Print statement for custom logging code with {} as a header".format(
                    key
                )
            )
        logging_dict_entry = logging_dict[key]

        # Check if item is of correct type:
        if isinstance(logging_dict_entry, list):

            # Construct print statement
            code += 'Printf("{}'.format(key)
            code += " {}".format("%g " * len(logging_dict_entry))
            code = code.strip()
            code += '\\n"'

            # Add format keys
            for param in logging_dict_entry:
                code += ",((double)stardata->{})".format(param)
            code += ");\n"

        else:
            print(
                "Error: please use a list for the list of parameters that you want to have logged"
            )
    code = code.strip()

    return code


####################################################################################
def binary_c_log_code(code, verbose=0):
    """
    Function to construct the code to construct the custom logging function
    """

    if verbose > 0:
        print("Creating the code for the shared library for the custom logging")

    # Create code
    custom_logging_function_string = """\
#pragma push_macro(\"MAX\")
#pragma push_macro(\"MIN\")
#undef MAX
#undef MIN
#include \"binary_c.h\"
#include \"RLOF/RLOF_prototypes.h\"

// add visibility __attribute__ ((visibility ("default"))) to it 
void binary_c_API_function custom_output_function(struct stardata_t * stardata);
void binary_c_API_function custom_output_function(struct stardata_t * stardata)
{{
    // struct stardata_t * stardata = (struct stardata_t *)x;
    {};
}}

#undef MAX 
#undef MIN
#pragma pop_macro(\"MIN\")
#pragma pop_macro(\"MAX\")\
    """.format(
        code
    )

    # print(repr(textwrap.dedent(custom_logging_function_string)))
    return textwrap.dedent(custom_logging_function_string)


def binary_c_write_log_code(code, filename, verbose=0):
    """
    Function to write the generated logging code to a file
    """

    cwd = os.getcwd()
    filePath = os.path.join(cwd, filename)

    # Remove if it exists
    remove_file(filePath, verbose)

    if verbose > 0:
        print("Writing the custom logging code to {}".format(filePath))

    # Write again
    with open(filePath, "w") as file:
        file.write(code)


def from_binary_c_config(config_file, flag):
    """
    Function to run the binaryc_config command with flags
    """

    res = subprocess.check_output(
        "{config_file} {flag}".format(config_file=config_file, flag=flag),
        shell=True,
        stderr=subprocess.STDOUT,
    )

    # convert and chop off newline
    res = res.decode("utf").rstrip()
    return res


def return_compilation_dict(verbose=0):
    """
    Function to build the compile command for the shared library

    inspired by binary_c_inline_config command in perl

    TODO: this function still has some cleaning up to do wrt default values for the compile command
    # https://developers.redhat.com/blog/2018/03/21/compiler-and-linker-flags-gcc/


    returns:
     - string containing the command to build the shared library
    """

    if verbose > 0:
        print(
            "Calling the binary_c config code to get the info to build the shared library"
        )
    # use binary_c-config to get necessary flags
    BINARY_C_DIR = os.getenv("BINARY_C")
    if BINARY_C_DIR:
        BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")
        BINARY_C_SRC_DIR = os.path.join(BINARY_C_DIR, "src")
        # TODO: build in check to see whether the file exists
    else:
        raise NameError("Envvar BINARY_C doesnt exist")

    # TODO: make more options for the compiling
    cc = from_binary_c_config(BINARY_C_CONFIG, "cc")

    # Check for binary_c
    BINARY_C_EXE = os.path.join(BINARY_C_DIR, "binary_c")
    if not os.path.isfile(BINARY_C_EXE):
        print("We require  binary_c executable; have you built binary_c?")
        raise NameError("BINARY_C executable doesnt exist")

    # TODO: debug
    libbinary_c = "-lbinary_c"
    binclibs = from_binary_c_config(BINARY_C_CONFIG, "libs")
    libdirs = "{} -L{}".format(
        from_binary_c_config(BINARY_C_CONFIG, "libdirs"), BINARY_C_SRC_DIR
    )
    bincflags = from_binary_c_config(BINARY_C_CONFIG, "cflags")
    bincincdirs = from_binary_c_config(BINARY_C_CONFIG, "incdirs")

    # combine
    binclibs = " {} {} {}".format(libdirs, libbinary_c, binclibs)

    # setup defaults:
    defaults = {
        "cc": "gcc",  # default compiler
        "ccflags": bincflags,
        "ld": "ld",  # 'ld': $Config{ld}, # default linker
        "debug": 0,
        "inc": "{} -I{}".format(bincincdirs, BINARY_C_SRC_DIR),
        # inc => ' '.($Config{inc}//' ').' '.$bincincdirs." -I$srcdir ",
        #   include the defaults plus # GSL and binary_c
        # 'libname': libname, # libname is usually just binary_c corresponding to libbinary_c.so
        "libs": binclibs,
    }

    # set values with defaults. TODO: make other input possile.
    ld = defaults["ld"]
    # debug = defaults["debug"]
    inc = defaults[
        "inc"
    ]  # = ($ENV{BINARY_GRID2_INC} // $defaults{inc}).' '.($ENV{BINARY_GRID2_EXTRAINC} // '');
    libs = defaults[
        "libs"
    ]  # = ($ENV{BINARY_GRID2_LIBS} // $defaults{libs}).' '.($ENV{BINARY_GRID2_EXTRALIBS}//'');
    ccflags = defaults["ccflags"]  #  = $ENV{BINARY_GRID2_CCFLAGS}
    # // ($defaults{ccflags}) . ($ENV{BINARY_GRID2_EXTRACCFLAGS} // '');

    # you must define _SEARCH_H to prevent it being loaded twice
    ccflags += " -shared -D_SEARCH_H"

    # remove the visibility=hidden for this compilation
    ccflags = ccflags.replace("-fvisibility=hidden", "")

    # ensure library paths to the front of the libs:
    libs_content = libs.split(" ")
    library_paths = [el for el in libs_content if el.startswith("-L")]
    non_library_paths = [
        el for el in libs_content if (not el.startswith("-L") and not el == "")
    ]
    libs = "{} {}".format(" ".join(library_paths), " ".join(non_library_paths))

    if verbose > 0:
        print(
            "Got options to compile:\n\tcc = {cc}\n\tccflags = {ccflags}\n\tld = {ld}\n\tlibs = {libs}\n\tinc = {inc}\n\n".format(
                cc=cc, ccflags=ccflags, ld=ld, libs=libs, inc=inc
            )
        )

    return {"cc": cc, "ld": ld, "ccflags": ccflags, "libs": libs, "inc": inc}


def compile_shared_lib(code, sourcefile_name, outfile_name, verbose=0):
    """
    Function to write the custom logging code to a file and then compile it.
    TODO: nicely put in the -fPIC
    """

    # Write code to file
    binary_c_write_log_code(code, sourcefile_name, verbose)

    # Remove the library if present:
    remove_file(outfile_name, verbose)

    # create compilation command
    compilation_dict = return_compilation_dict(verbose)

    # Construct full command
    command = "{cc} -fPIC {ccflags} {libs} -o {outfile_name} {sourcefile_name} {inc}".format(
        cc=compilation_dict["cc"],
        ccflags=compilation_dict["ccflags"],
        libs=compilation_dict["libs"],
        outfile_name=outfile_name,
        sourcefile_name=sourcefile_name,
        inc=compilation_dict["inc"],
    )

    # remove extra whitespaces:
    command = " ".join(command.split())

    # Execute compilation and create the library
    if verbose > 0:
        # BINARY_C_DIR = os.getenv("BINARY_C")
        # BINARY_C_SRC_DIR = os.path.join(BINARY_C_DIR, "src")
        print(
            "Building shared library for custom logging with (binary_c.h) on {}\n".format(
                socket.gethostname()
            )
        )
        print(
            "Executing following command to compile the shared library:\n{command}".format(
                command=command
            )
        )
    res = subprocess.check_output("{command}".format(command=command), shell=True)

    if verbose > 0:
        if res:
            print("Output of compilation command:\n{}".format(res))


def create_and_load_logging_function(custom_logging_code, verbose=0):
    """
    Function to automatically compile the shared library with the given
    custom logging code and load it with ctypes

    returns:
        memory adress of the custom logging function in a int type.
    """

    #

    library_name = os.path.join(
        temp_dir(), "libcustom_logging_{}.so".format(uuid.uuid4().hex)
    )

    compile_shared_lib(
        custom_logging_code,
        sourcefile_name=os.path.join(temp_dir(), "custom_logging.c"),
        outfile_name=library_name,
        verbose=verbose,
    )

    if verbose > 0:
        print("loading shared library for custom logging")

    # Loading library
    _ = ctypes.CDLL("libgslcblas.so", mode=ctypes.RTLD_GLOBAL)
    _ = ctypes.CDLL("libgsl.so", mode=ctypes.RTLD_GLOBAL)
    _ = ctypes.CDLL("libbinary_c.so", mode=ctypes.RTLD_GLOBAL)

    libcustom_logging = ctypes.CDLL(
        library_name, mode=ctypes.RTLD_GLOBAL,
    )  # loads the shared library

    # Get memory adress of function. mimicking a pointer
    func_memaddr = ctypes.cast(
        libcustom_logging.custom_output_function, ctypes.c_void_p
    ).value

    if verbose > 0:
        print(
            "loaded shared library for custom logging. \
            custom_output_function is loaded in memory at {}".format(
                func_memaddr
            )
        )

    return func_memaddr, library_name
