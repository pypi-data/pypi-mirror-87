"""
Module containing the utility function run_system,
which handles a lot of things by analysing the passed kwargs
"""


from binarycpython.utils.functions import (
    create_arg_string,
    get_arg_keys,
    remove_file,
)

from binarycpython.utils.custom_logging_functions import (
    create_and_load_logging_function,
)

from binarycpython import _binary_c_bindings


def run_system(**kwargs):
    """
    Function that runs a system.
    Mostly as a useful utility function that handles all the setup of argument lists etc.

    All~ the arguments known to binary_c can be passed to this function as kwargs.
    Several extra arguments can be passed through the kwargs:
        * custom_logging_code (string):
            Should contain a string containing the c-code for the shared library.
            If this is provided binary_c will use that custom logging code to output its data
        * log_filename (string):
            Should contain name of the binary_c system logfile.
            Passing this will make sure that the filename gets written for a run
            (its default behaviour is NOT to write a logfile for a system)
        * parse_function (function):
            should contain a function that parses the output.
            The parse function should take 1 required parameter: the output of the binaryc run
            Passing this will call the parse_function by passing it the output of the binary_c call
            and returns what the parse_function returns

    examples:
        * run_system(M_1=10): will run a system with ZAMS mass 1 = 10
        * run_system(M_1=10, log_filename="~/example_log.txt"): Will run a system
            and write the logfile too
        * run_system(M_1=10, parse_function=fancy_parsing_function)

    TODO: Expand functionality.
    TODO: Notify user when an unknown keyword is passed.
    """

    # Load available arg keywords
    available_binary_c_arg_keywords = get_arg_keys()

    other_keywords = ["custom_logging_code", "log_filename", "parse_function"]

    # Set default values
    func_memaddr = -1
    write_logfile = 0

    # Create dict to pass as argstring
    binary_c_args = {}

    # Check which binary_c arguments have been passed and put them into a dict
    for key in kwargs:
        if key in available_binary_c_arg_keywords:
            binary_c_args[key] = kwargs[key]

        # Notify user when this key wont be used
        else:
            if not key in other_keywords:
                print(
                    "The following keyword was not recognized and wont be used:\n\t{}".format(
                        key
                    )
                )

    # Check if custom logging is required
    if "custom_logging_code" in kwargs:
        func_memaddr, shared_lib_filename = create_and_load_logging_function(
            kwargs["custom_logging_code"]
        )

    # Check if writing logfile is required:
    if "log_filename" in kwargs:
        write_logfile = 1

    # Construct arguments string and final execution string
    arg_string = create_arg_string(binary_c_args)
    binary_c_command = "binary_c {}".format(arg_string)

    # Call binary_c
    output = _binary_c_bindings.run_system(
        binary_c_command,
        custom_logging_func_memaddr=func_memaddr,
        write_logfile=write_logfile,
    )

    # Remove and unload files. .
    if "custom_logging_code" in kwargs:
        remove_file(shared_lib_filename)

    if "parse_function" in kwargs:
        return kwargs["parse_function"](output)
    return output
