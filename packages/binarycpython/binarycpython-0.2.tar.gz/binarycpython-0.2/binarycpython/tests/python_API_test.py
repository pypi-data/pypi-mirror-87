#!/usr/bin/python3

from binarycpython import _binary_c_bindings

from binarycpython.utils.custom_logging_functions import (
    autogen_C_logging_code,
    binary_c_log_code,
    create_and_load_logging_function,
)
from binarycpython.utils.functions import temp_dir

import tempfile
import textwrap

############################################################
# Test script for the api functions
# unittests
############################################################


# Evolution functions
def test_run_system():
    m1 = 15.0  # Msun
    m2 = 14.0  # Msun
    separation = 0  # 0 = ignored, use period
    orbital_period = 4530.0  # days
    eccentricity = 0.0
    metallicity = 0.02
    max_evolution_time = 15000
    argstring = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g}  ".format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
    )

    output = _binary_c_bindings.run_system(argstring=argstring)

    print("function: test_run_system")
    print("Binary_c output:")
    print(textwrap.indent(output, "\t"))


def test_run_system_with_log():
    m1 = 15.0  # Msun
    m2 = 14.0  # Msun
    separation = 0  # 0 = ignored, use period
    orbital_period = 4530.0  # days
    eccentricity = 0.0
    metallicity = 0.02
    max_evolution_time = 15000

    log_filename = temp_dir() + "/test_log.txt"
    api_log_filename_prefix = temp_dir() + "/test_log"

    argstring = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g} log_filename {7:s} api_log_filename_prefix {8:s}".format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
        log_filename,
        api_log_filename_prefix,
    )

    output = _binary_c_bindings.run_system(argstring=argstring, write_logfile=1)

    print("function: test_run_system_with_log")
    print("Binary_c output:")
    print(textwrap.indent(output, "\t"))


def test_run_system_with_custom_logging():
    # generate logging lines. Here you can choose whatever you want to have logged, and with what header
    # this generates working print statements
    logging_line = autogen_C_logging_code(
        {"MY_STELLAR_DATA": ["model.time", "star[0].mass"],}
    )

    # Generate entire shared lib code around logging lines
    custom_logging_code = binary_c_log_code(logging_line)

    # Load memory adress
    func_memaddr, shared_lib_filename = create_and_load_logging_function(
        custom_logging_code
    )

    # Some values
    m1 = 15.0  # Msun
    m2 = 14.0  # Msun
    separation = 0  # 0 = ignored, use period
    orbital_period = 4530.0  # days
    eccentricity = 0.0
    metallicity = 0.02
    max_evolution_time = 15000

    argstring = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g}".format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
    )

    output = _binary_c_bindings.run_system(
        argstring, custom_logging_func_memaddr=func_memaddr
    )

    print("function: test_run_system_with_custom_logging")
    print("memory adress of custom logging functions:")
    print(textwrap.indent(str(func_memaddr), "\t"))

    print("binary_c output:")
    print(textwrap.indent(output, "\t"))


# Testing other utility functions
def test_return_help():
    output = _binary_c_bindings.return_help("M_1")

    print("function: test_return_help")
    print("help output:")
    print(textwrap.indent(output, "\t"))


def test_return_arglines():
    output = _binary_c_bindings.return_arglines()

    print("function: test_return_arglines")
    print("arglines output:")
    print(textwrap.indent(output, "\t"))


def test_return_help_all():
    output = _binary_c_bindings.return_help_all("M_1")

    print("function: test_return_help_all")
    print("help all output:")
    print(textwrap.indent(output, "\t"))


def test_return_version_info():
    output = _binary_c_bindings.return_version_info()

    print("function: test_return_version_info")
    print("version info output:")
    print(textwrap.indent(output, "\t"))


# Testing other functions
def test_return_store():
    output = _binary_c_bindings.return_store_memaddr("")

    print("function: test_return_store")
    print("store memory adress:")
    print(textwrap.indent(str(output), "\t"))


####
if __name__ == "__main__":
    test_run_system()

    test_run_system_with_log()

    test_run_system_with_custom_logging()

    test_return_help()

    test_return_arglines()

    test_return_help_all()

    test_return_version_info()

    test_return_store()
