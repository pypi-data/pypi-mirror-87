"""
Module containing most of the utility functions for the binarycpython package

Functions here are mostly functions used in other classes/functions, or
useful functions for the user
"""

import json
import os
import tempfile
import copy
import inspect
import ast

from collections import defaultdict

import h5py
import numpy as np

from binarycpython import _binary_c_bindings

########################################################
# utility functions
########################################################


def verbose_print(message, verbosity, minimal_verbosity):
    """
    Function that decides whether to print a message based on the current verbosity
    and its minimum verbosity

    if verbosity is equal or higher than the minimum, then we print
    """

    if verbosity >= minimal_verbosity:
        print(message)


def remove_file(file, verbosity=0):
    """
    Function to remove files but with verbosity
    """

    if os.path.exists(file):
        try:
            verbose_print("Removed {}".format(file), verbosity, 1)
            os.remove(file)

        except FileNotFoundError as inst:
            print("Error while deleting file {}: {}".format(file, inst))


def temp_dir():
    """
    Function to return the path the custom logging library shared object
    and script will be written to.

    Makes use of os.makedirs exist_ok which requires python 3.2+
    """

    tmp_dir = tempfile.gettempdir()
    path = os.path.join(tmp_dir, "binary_c_python")

    #
    os.makedirs(path, exist_ok=True)

    return path


def create_hdf5(data_dir, name):
    """
    Function to create an hdf5 file from the contents of a directory:
     - settings file is selected by checking on files ending on settings
     - data files are selected by checking on files ending with .dat

    TODO: fix missing settingsfiles
    """

    # Make HDF5:
    # Create the file
    hdf5_filename = os.path.join(data_dir, "{}".format(name))
    print("Creating {}".format(hdf5_filename))
    hdf5_file = h5py.File(hdf5_filename, "w")

    # Get content of data_dir
    content_data_dir = os.listdir(data_dir)

    # Settings
    if any([file.endswith("_settings.json") for file in content_data_dir]):
        print("Adding settings to HDF5 file")
        settings_file = os.path.join(
            data_dir,
            [file for file in content_data_dir if file.endswith("_settings.json")][0],
        )

        with open(settings_file, "r") as settings_file:
            settings_json = json.load(settings_file)

        # Create settings group
        settings_grp = hdf5_file.create_group("settings")

        # Write version_string to settings_group
        settings_grp.create_dataset("used_settings", data=json.dumps(settings_json))

    # Get data files
    data_files = [el for el in content_data_dir if el.endswith(".dat")]
    if data_files:
        print("Adding data to HDF5 file")

        # Create the data group
        data_grp = hdf5_file.create_group("data")

        # Write the data to the file:
        # Make sure:
        for data_file in data_files:
            # filename stuff
            filename = data_file
            full_path = os.path.join(data_dir, filename)
            base_name = os.path.splitext(os.path.basename(filename))[0]

            # Get header info
            header_name = "{base_name}_header".format(base_name=base_name)
            data_headers = np.genfromtxt(full_path, dtype="str", max_rows=1)
            data_headers = np.char.encode(data_headers)
            data_grp.create_dataset(header_name, data=data_headers)

            # Add data
            data = np.loadtxt(full_path, skiprows=1)
            data_grp.create_dataset(base_name, data=data)

        hdf5_file.close()


########################################################
# version_info functions
########################################################


def return_binary_c_version_info(parsed=False):
    """
    Function that returns the version information of binary_c
    """

    version_info = _binary_c_bindings.return_version_info().strip()

    if parsed:
        version_info = parse_binary_c_version_info(version_info)

    return version_info


def parse_binary_c_version_info(version_info_string):
    """
    Function that parses the binary_c version info. Length function with a lot of branches
    """

    version_info_dict = {}

    # Clean data and put in correct shape
    splitted = version_info_string.strip().splitlines()
    cleaned = set([el.strip() for el in splitted if not el == ""])

    ##########################
    # Isotopes:
    # Split off
    isotopes = set([el for el in cleaned if el.startswith('Isotope ')])
    cleaned = cleaned - isotopes

    isotope_dict = {}
    for el in isotopes:
        split_info = el.split("Isotope ")[-1].strip().split(" is ")

        isotope_info = split_info[-1]
        name = isotope_info.split(' ')[0].strip()

        # Get details
        mass_g = float(isotope_info.split(",")[0].split('(')[1].split("=")[-1][:-2].strip())
        mass_amu = float(isotope_info.split(",")[0].split('(')[-1].split("=")[-1].strip())
        mass_mev = float(isotope_info.split(",")[-3].split("=")[-1].replace(")", "").strip())
        A = int(isotope_info.split(",")[-1].strip().split("=")[-1].replace(")", ""))
        Z = int(isotope_info.split(",")[-2].strip().split("=")[-1])

        #
        isotope_dict[int(split_info[0])] = {'name': name, 'Z': Z, 'A': A, 'mass_mev': mass_mev, 'mass_g': mass_g, 'mass_amu': mass_amu}
    version_info_dict['isotopes'] = isotope_dict

    ##########################
    # Argpairs:
    # Split off
    argpairs = set([el for el in cleaned if el.startswith('ArgPair')])
    cleaned = cleaned - argpairs

    argpair_dict = {}
    for el in sorted(argpairs):
        split_info = el.split("ArgPair ")[-1].split(" ")

        if not argpair_dict.get(split_info[0], None):
            argpair_dict[split_info[0]] = {split_info[1]: split_info[2]}
        else:
            argpair_dict[split_info[0]][split_info[1]] = split_info[2]

    version_info_dict['argpairs'] = argpair_dict

    ##########################
    # ensembles:
    # Split off
    ensembles = set([el for el in cleaned if el.startswith('Ensemble')])
    cleaned = cleaned - ensembles

    ensemble_dict = {}
    for el in ensembles:
        split_info = el.split("Ensemble ")[-1].split(" is ")
        if len(split_info)>1:
            ensemble_dict[int(split_info[0])] = split_info[-1]
    version_info_dict['ensembles'] = ensemble_dict

    ##########################
    # macros:
    # Split off
    macros = set([el for el in cleaned if el.startswith('macroxyz')])
    cleaned = cleaned - macros

    param_type_dict = {
        'STRING': str,
        'FLOAT': float,
        'MACRO': str,
        'INT': int,
        'LONG_INT': int,
    }

    macros_dict = {}
    for el in macros:
        split_info = el.split("macroxyz ")[-1].split(" : ")
        param_type = split_info[0]

        new_split = "".join(split_info[1:]).split(" is ")
        param_name = new_split[0]
        param_value = " is ".join(new_split[1:])
        # Sometimes the macros have extra information behind it. Needs an update in outputting by binary_c
        try:
            macros_dict[param_name] = param_type_dict[param_type](param_value)
        except ValueError:
            macros_dict[param_name] = str(param_value)
    version_info_dict['macros'] = macros_dict

    ##########################
    # Elements:
    # Split off:
    elements = set([el for el in cleaned if el.startswith('Element')])
    cleaned = cleaned - elements

    # Fill dict:
    elements_dict = {}
    for el in elements:
        split_info = el.split("Element ")[-1].split(" : ")
        name_info = split_info[0].split(" is ")

        # get isotope info
        isotopes = {}
        if not split_info[-1][0]=='0':
            isotope_string = split_info[-1].split(" = ")[-1]
            isotopes = {int(split_isotope.split("=")[0]):split_isotope.split("=")[1] for split_isotope in isotope_string.split(" ")}

        elements_dict[int(name_info[0])] = {'name': name_info[-1], 'atomic_number': int(name_info[0]), 'amt_isotopes': len(isotopes), 'isotopes': isotopes}
    version_info_dict['elements'] = version_info_dict

    ##########################
    # dt_limits:
    # split off
    dt_limits = set([el for el in cleaned if el.startswith('DTlimit')])
    cleaned = cleaned - dt_limits

    # Fill dict
    dt_limits_dict = {}
    for el in dt_limits:
        split_info = el.split("DTlimit ")[-1].split(" : ")
        dt_limits_dict[split_info[1].strip()] = {'index': int(split_info[0]), 'value': float(split_info[-1])}

    version_info_dict['dt_limits'] = dt_limits_dict

    ##########################
    # Nucleosynthesis sources:
    # Split off
    nucsyn_sources = set([el for el in cleaned if el.startswith('Nucleosynthesis')])
    cleaned = cleaned - nucsyn_sources

    # Fill dict
    nucsyn_sources_dict = {}
    for el in nucsyn_sources:
        split_info = el.split("Nucleosynthesis source")[-1].strip().split(" is ")
        nucsyn_sources_dict[int(split_info[0])] = split_info[-1]

    version_info_dict['nucleosynthesis_sources'] = nucsyn_sources_dict

    ##########################
    # miscellaneous:
    # All those that I didnt catch with the above filters. Could try to get some more out though.
    # TODO: filter a bit more.

    misc_dict = {}
    git_revision = [el for el in cleaned if el.startswith('git revision')]
    misc_dict['git_revision'] = git_revision[0].split("git revision ")[-1].replace("\"", '')

    git_branch = [el for el in cleaned if el.startswith('git branch')]
    misc_dict['git_branch'] = git_branch[0].split("git branch ")[-1].replace("\"", '')

    build = [el for el in cleaned if el.startswith('Build')]
    misc_dict['build'] = build[0].split("Build: ")[-1].replace("\"", '')

    email = [el for el in cleaned if el.startswith('Email')]
    misc_dict['email'] = email[0].split("Email ")[-1].split(',')

    misc_dict['uncaught'] = cleaned

    version_info_dict['miscellaneous'] = misc_dict
    return version_info_dict


########################################################
# binary_c output functions
########################################################


def output_lines(output):
    """
    Function that outputs the lines that were recieved from the binary_c run.
    """
    return output.splitlines()


def parse_output(output, selected_header):
    """
    Function that parses output of binary_c:

    This function works in two cases:
    if the caught line contains output like 'example_header time=12.32 mass=0.94 ..'
    or if the line contains output like 'example_header 12.32 0.94'

    You can give a 'selected_header' to catch any line that starts with that.
    Then the values will be put into a dictionary.

    TODO: Think about exporting to numpy array or pandas instead of a defaultdict

    TODO: rethink whether this function is necessary at all
    """

    value_dicts = []

    # split output on newlines
    for line in output.split("\n"):
        # Skip any blank lines
        if not line == "":
            split_line = line.split()

            # Select parts
            header = split_line[0]
            values_list = split_line[1:]

            # print(values_list)
            # Catch line starting with selected header
            if header == selected_header:
                # Check if the line contains '=' symbols:
                value_dict = {}
                if all("=" in value for value in values_list):
                    for value in values_list:
                        key, val = value.split("=")
                        value_dict[key.strip()] = val.strip()
                    value_dicts.append(value_dict)
                else:
                    if any("=" in value for value in values_list):
                        raise ValueError(
                            "Caught line contains some = symbols but not \
                            all of them do. aborting run"
                        )

                    for j, val in enumerate(values_list):
                        value_dict[j] = val
                    value_dicts.append(value_dict)

    if len(value_dicts) == 0:
        print(
            "Sorry, didnt find any line matching your header {}".format(selected_header)
        )
        return None

    keys = value_dicts[0].keys()

    # Construct final dict.
    final_values_dict = defaultdict(list)
    for value_dict in value_dicts:
        for key in keys:
            final_values_dict[key].append(value_dict[key])

    return final_values_dict


########################################################
# Argument and default value functions
########################################################


def get_defaults(filter_values=False):
    """
    Function that calls the binaryc get args function and cast it into a dictionary.

    All the values are strings

    filter_values: whether to filter out NULL and Function defaults.
    """

    default_output = _binary_c_bindings.return_arglines()
    default_dict = {}

    for default in default_output.split("\n"):
        if not default in ["__ARG_BEGIN", "__ARG_END", ""]:
            key, value = default.split(" = ")
            default_dict[key] = value

    if filter_values:
        default_dict = filter_arg_dict(default_dict)

    return default_dict


def get_arg_keys():
    """
    Function that return the list of possible keys to give in the arg string
    """

    return get_defaults().keys()


def filter_arg_dict(arg_dict):
    """
    Function to filter out keys that contain values included in ['NULL', 'Function', '']
    """

    old_dict = arg_dict.copy()
    new_dict = {}

    for key in old_dict.keys():
        if not old_dict[key] in ["NULL", "Function"]:
            if not old_dict[key] == "":
                new_dict[key] = old_dict[key]

    return new_dict


def create_arg_string(arg_dict, sort=False, filter_values=False):
    """
    Function that creates the arg string for binary_c.

    Options:
        sort: sort the order of the keys.
        filter_values: filters the input dict on keys that have NULL or `function` as value.
    """

    arg_string = ""

    if filter_values:
        arg_dict = filter_values(arg_dict)

    keys = sorted(arg_dict.keys()) if sort else arg_dict.keys()
    for key in keys:
        arg_string += "{key} {value} ".format(key=key, value=arg_dict[key])
    arg_string = arg_string.strip()
    return arg_string


########################################################
# Help functions
########################################################


def get_help(param_name="", print_help=True, fail_silently=False):
    """
    Function that returns the help info for a given parameter.

    Binary_c will output things in the following order;
    - Did you mean?
    - binary_c help for variable
    - default
    - available macros

    This function reads out that structure and catches the different components of this output

    Will print a dict

    return_dict: wether to return the help info dictionary

    """

    available_arg_keys = get_arg_keys()

    if not param_name:
        print(
            "Please set the param_name to any of the following:\n {}".format(
                sorted(available_arg_keys)
            )
        )
        return None

    if param_name in available_arg_keys:
        help_info = _binary_c_bindings.return_help(param_name)
        cleaned = [el for el in help_info.split("\n") if not el == ""]

        # Get line numbers
        did_you_mean_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Did you mean")
        ]
        parameter_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("binary_c help")
        ]
        default_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Default")
        ]
        macros_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Available")
        ]

        help_info_dict = {}

        # Get alternatives
        if did_you_mean_nr:
            alternatives = cleaned[did_you_mean_nr[0] + 1 : parameter_line_nr[0]]
            alternatives = [el.strip() for el in alternatives]
            help_info_dict["alternatives"] = alternatives

        # Information about the parameter
        parameter_line = cleaned[parameter_line_nr[0]]
        parameter_name = parameter_line.split(":")[1].strip().split(" ")[0]
        parameter_value_input_type = (
            " ".join(parameter_line.split(":")[1].strip().split(" ")[1:])
            .replace("<", "")
            .replace(">", "")
        )

        help_info_dict["parameter_name"] = parameter_name
        help_info_dict["parameter_value_input_type"] = parameter_value_input_type

        description_line = " ".join(
            cleaned[parameter_line_nr[0] + 1 : default_line_nr[0]]
        )
        help_info_dict["description"] = description_line

        # Default:
        default_line = cleaned[default_line_nr[0]]
        default_value = default_line.split(":")[-1].strip()

        help_info_dict["default"] = default_value

        # Get Macros:
        if macros_line_nr:
            macros = cleaned[macros_line_nr[0] + 1 :]
            help_info_dict["macros"] = macros

        if print_help:
            for key in help_info_dict:
                print("{}:\n\t{}".format(key, help_info_dict[key]))

        return help_info_dict

    else:
        if not fail_silently:
            print(
                "{} is not a valid parameter name. Please choose from the \
                following parameters:\n\t{}".format(
                    param_name, list(available_arg_keys)
                )
            )
        return None


def get_help_all(print_help=True):
    """
    Function that reads out the output of the help_all api call to binary_c

    print_help: bool, prints all the parameters and their descriptions.

    return_dict:  returns a dictionary
    """

    # Call function
    help_all = _binary_c_bindings.return_help_all()

    # String manipulation
    split = help_all.split(
        "############################################################\n"
    )
    cleaned = [el for el in split if not el == "\n"]

    section_nums = [i for i in range(len(cleaned)) if cleaned[i].startswith("#####")]

    # Create dicts
    help_all_dict = {}

    # Select the section name and the contents of that section. Note, not all sections have content!
    for i in range(len(section_nums)):
        if not i == len(section_nums) - 1:
            params = cleaned[section_nums[i] + 1 : section_nums[i + 1]]
        else:
            params = cleaned[section_nums[i] + 1 : len(cleaned)]
        section_name = (
            cleaned[section_nums[i]]
            .lstrip("#####")
            .strip()
            .replace("Section ", "")
            .lower()
        )

        #
        params_dict = {}

        if params:

            # Clean it, replace in-text newlines with a space and then split on newlines.
            split_params = params[0].strip().replace("\n ", " ").split("\n")

            # Process params and descriptions per section
            for split_param in split_params:
                split_param_info = split_param.split(" : ")
                if not len(split_param_info) == 3:
                    # there are ocassions where the semicolon
                    # is used in the description text itself.
                    if len(split_param_info) == 4:
                        split_param_info = [
                            split_param_info[0],
                            ": ".join([split_param_info[1], split_param_info[2]]),
                            split_param_info[3],
                        ]

                    # other occassions?

                # Put the information in a dict
                param_name = split_param_info[0]
                param_description = split_param_info[1]

                if len(split_param_info) > 2:
                    rest = split_param_info[2:]
                else:
                    rest = None

                params_dict[param_name] = {
                    "param_name": param_name,
                    "description": param_description,
                    "rest": ''.join(rest) if rest else '',
                }

            # make section_dict
            section_dict = {
                "section_name": section_name,
                "parameters": params_dict.copy(),
            }

            # Put in the total dict
            help_all_dict[section_name] = section_dict.copy()

    # Print things
    if print_help:
        for section in sorted(help_all_dict.keys()):
            print(
                "##################\n###### Section {}\n##################".format(
                    section
                )
            )
            section_dict = help_all_dict[section]
            for param_name in sorted(section_dict["parameters"].keys()):
                param = section_dict["parameters"][param_name]
                print(
                    "\n{}:\n\t{}: {}".format(
                        param["param_name"], param["description"], param["rest"]
                    )
                )

    # # Loop over all the parameters an call the help() function on it.
    # # Takes a long time but this is for testing
    # for section in help_all_dict.keys():
    #     section_dict = help_all_dict[section]
    #     for param in section_dict['parameters'].keys():
    #         get_help(param)

    return help_all_dict


def get_help_super(print_help=False, fail_silently=True):
    """
    Function that first runs get_help_all, and then per argument also run
    the help function to get as much information as possible.
    """

    # Get help_all information
    help_all_dict = get_help_all(print_help=False)
    for section_name in help_all_dict:
        section = help_all_dict[section_name]
        print(section_name)
        for parameter_name in section["parameters"].keys():
            print("\t", parameter_name)

    help_all_super_dict = help_all_dict.copy()

    # Loop over all sections and stuff
    for section_name in help_all_dict:
        # Skipping the section i/o because that one shouldn't be available to python anyway
        if not section_name == "i/o":
            section = help_all_dict[section_name]

            for parameter_name in section["parameters"].keys():
                parameter = section["parameters"][parameter_name]

                # Get detailed help info
                detailed_help = get_help(
                    parameter_name, print_help=False, fail_silently=fail_silently,
                )

                if detailed_help:
                    # check whether the descriptions of help_all and detailed help are the same
                    if not fail_silently:
                        if not parameter["description"] == detailed_help["description"]:
                            print(json.dumps(parameter, indent=4))

                    ## put values into help all super dict
                    # input type
                    parameter["parameter_value_input_type"] = detailed_help[
                        "parameter_value_input_type"
                    ]

                    # default
                    parameter["default"] = detailed_help["default"]

                    # macros
                    if "macros" in detailed_help.keys():
                        parameter["macros"] = detailed_help["macros"]

                section["parameters"][parameter_name] = parameter

    if print_help:
        print(json.dumps(help_all_super_dict, indent=4))

    return help_all_super_dict


########################################################
# logfile functions
########################################################


def load_logfile(logfile):
    """
    Experimental function that parses the generated logfile of binary_c.
    """

    with open(logfile, "r") as file:
        logfile_data = file.readlines()

    time_list = []
    m1_list = []
    m2_list = []
    k1_list = []
    k2_list = []
    sep_list = []
    ecc_list = []
    rel_r1_list = []
    rel_r2_list = []
    event_list = []

    # random_seed = logfile_data[0].split()[-2]
    # random_count = logfile_data[0].split()[-1]
    # probability = logfile_data[-1].split()

    for line in logfile_data[1:-1]:
        split_line = line.split()

        time_list.append(split_line[0])
        m1_list.append(split_line[1])
        m2_list.append(split_line[2])
        k1_list.append(split_line[3])
        k2_list.append(split_line[4])
        sep_list.append(split_line[5])
        ecc_list.append(split_line[6])
        rel_r1_list.append(split_line[7])
        rel_r2_list.append(split_line[8])
        event_list.append(" ".join(split_line[9:]))

    print(event_list)


########################################################
# Ensemble dict functions
########################################################


def inspect_dict(dict_1, indent=0, print_structure=True):
    """
    Function to inspect a dict.

    Works recursively if there is a nested dict.

    Prints out keys and their value types
    """

    structure_dict = {}

    for key, value in dict_1.items():
        structure_dict[key] = type(value)
        if print_structure:
            print("\t" * indent, key, type(value))
        if isinstance(value, dict):
            structure_dict[key] = inspect_dict(
                value, indent=indent + 1, print_structure=print_structure
            )
    return structure_dict


def merge_dicts(dict_1, dict_2):
    """
    Function to merge two dictionaries.

    Behaviour:

    When dict keys are present in both, we decide based on the value types how to combine them:
    - dictionaries will be merged by calling recursively calling this function again
    - numbers will be added
    - (opt) lists will be appended

    - In the case that the instances do now match: for now I will raise an error

    When dict keys are only present in one of either, we just add the content to the new dict
    """

    # Set up new dict
    new_dict = {}

    #
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        if isinstance(dict_1[key], (float, int)):
            new_dict[key] = dict_1[key]
        else:
            copy_dict = copy.deepcopy(dict_1[key])
            new_dict[key] = copy_dict

    for key in unique_to_dict_2:
        if isinstance(dict_2[key], (float, int)):
            new_dict[key] = dict_2[key]
        else:
            copy_dict = copy.deepcopy(dict_2[key])
            new_dict[key] = copy_dict

    # Go over the common keys:
    for key in overlapping_keys:
        # See whether the types are actually the same
        if not type(dict_1[key]) is type(dict_2[key]):
            print(
                "Error {} and {} are not of the same type and cannot be merged".format(
                    dict_1[key], dict_2[key]
                )
            )
            raise ValueError

        # Here we check for the cases that we want to explicitly catch. Ints will be added,
        # floats will be added, lists will be appended (though that might change) and dicts will be
        # dealt with by calling this function again.
        else:
            # ints
            if isinstance(dict_1[key], int) and isinstance(dict_2[key], int):
                new_dict[key] = dict_1[key] + dict_2[key]

            # floats
            elif isinstance(dict_1[key], float) and isinstance(dict_2[key], float):
                new_dict[key] = dict_1[key] + dict_2[key]

            # lists
            elif isinstance(dict_1[key], list) and isinstance(dict_2[key], list):
                new_dict[key] = dict_1[key] + dict_2[key]

            # dicts
            elif isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                new_dict[key] = merge_dicts(dict_1[key], dict_2[key])

            else:
                print(
                    "Object types {},{} not supported".format(
                        type(dict_1[key]), type(dict_2[key])
                    )
                )
    #
    return new_dict


class binarycDecoder(json.JSONDecoder):
    """
    Custom decoder to transform the numbers that are strings to actual floats
    """

    def decode(self, s):
        result = super().decode(
            s
        )  # result = super(Decoder, self).decode(s) for Python 2.x
        return self._decode(result)

    def _decode(self, o):
        """
        Depending on the type of object is will determine whether to loop over the elements,
        or try to change the type of the object from string to float

        The try except might be a somewhat rough solution but it catches all cases.
        """

        # Check if we can turn it into a float
        # if isinstance(o, str) or isinstance(o, unicode):
        if isinstance(o, str):
            try:
                return float(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def binaryc_json_serializer(obj):
    """
    Custom serializer for binary_c to use when functions are present in the dictionary
    that we want to export.

    Function objects will be turned into str representations of themselves
    """

    if inspect.isfunction(obj):
        return str(obj)
    return obj

def handle_ensemble_string_to_json(raw_output):
    """
    Function that deals with the raw output of the ensemble and 
    creates a working JSON dictionary out of it. 

    It seems that JSON does not like strings that contain dictionaries which have a number as a key, but more specifically it is the fact that binary-c outputs as 5e2 instead of 
    
    e.g. with python 3.6.4: json.loads("{5e2: 10}") leads to a JSONDecodeError. To fix this, I do the following:

    with ensemble_output being the literal string of output, and json_output the correct jsonified version of that.

    eval_dict = ast.literal_eval(ensemble_output)
    json_output =    json.loads(json.dumps(eval_dict), cls=binarycDecoder)

    Note: this does pose somewhat of a risk, since eval'ing something might lead to unexpected behaviour.
    """

    return json.loads(json.dumps(ast.literal_eval(raw_output)), cls=binarycDecoder)
