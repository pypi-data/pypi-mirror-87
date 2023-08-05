"""
Module containing tests regarding the persistent_data memory and the ensemble output
"""

import os
import sys
import time
import json
import textwrap

from binarycpython import _binary_c_bindings

from binarycpython.utils.functions import (
    binarycDecoder,
    temp_dir,
    inspect_dict,
    merge_dicts,
    handle_ensemble_string_to_json,
)

TMP_DIR = temp_dir()
os.makedirs(os.path.join(TMP_DIR, "test"), exist_ok=True)


####
def return_argstring(
    m1=15.0,
    m2=14.0,
    separation=0,
    orbital_period=453000000000,
    eccentricity=0.0,
    metallicity=0.02,
    max_evolution_time=15000,
    defer_ensemble=0,
    ensemble_filters_off=1,
    ensemble_filter="SUPERNOVAE",
):
    """
    Function to make a argstring that we can use in these tests
    """

    # Make the argstrings
    argstring_template = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} \
eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g} ensemble 1 ensemble_defer {7} \
ensemble_filters_off {8} ensemble_filter_{9} 1 probability 0.1"

    argstring = argstring_template.format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
        defer_ensemble,
        ensemble_filters_off,
        ensemble_filter,
    )

    return argstring

def test_return_persistent_data_memaddr():
    """
    Test case to check if the memory adress has been created succesfully
    """

    output = _binary_c_bindings.return_persistent_data_memaddr()

    print("function: test_run_system")
    print("Binary_c output:")
    print(textwrap.indent(str(output), "\t"))

    assert isinstance(output, int), "memory adress has to be an integer"
    assert output != 0, "memory adress seems not to have a correct value"


def test_passing_persistent_data_to_run_system():
    # Function to test the passing of the persistent data memoery adress, and having ensemble_defer = True
    # We should see that the results of multiple systems have been added to the one output json

    # Make argstrings
    argstring_1 = return_argstring(defer_ensemble=0)
    argstring_1_deferred = return_argstring(defer_ensemble=1)
    argstring_2 = return_argstring(defer_ensemble=0)

    #
    persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

    output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
    ensemble_jsons_1 = [
        line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    json_1 = handle_ensemble_string_to_json(ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :])

    # Doing 2 systems in a row.
    output_1_deferred = _binary_c_bindings.run_system(
        argstring=argstring_1_deferred, persistent_data_memaddr=persistent_data_memaddr
    )
    output_2 = _binary_c_bindings.run_system(
        argstring=argstring_2, persistent_data_memaddr=persistent_data_memaddr
    )
    ensemble_jsons_2 = [
        line for line in output_2.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    json_2 = handle_ensemble_string_to_json(ensemble_jsons_2[0][len("ENSEMBLE_JSON ") :])

    # Doing system one again.
    output_1_again = _binary_c_bindings.run_system(argstring=argstring_1)
    ensemble_jsons_1 = [
        line for line in output_1_again.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    json_1_again = handle_ensemble_string_to_json(ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :])

    assert (
        json_1 == json_1_again
    ), "The system with the same initial settings did not give the same output"
    assert (
        json_1 != json_2
    ), "The output of the deferred two systems should not be the same as the first undeferred output"
import pickle
def pickle_n_checksize(obj):

    name = os.path.join(TMP_DIR, "test", "pickle")

    with open(name, 'wb') as file:
        pickle.dump(obj, file)

    file_stats = os.stat(name)
    print("size: {}mb".format(file_stats.st_size/(1024*1024)))
    os.remove(name)

def test_full_ensemble_output():
    """
    Function to just output the whole ensemble
    """

    argstring_1 = return_argstring(defer_ensemble=0, ensemble_filters_off=1)

    # print(argstring_1)
    # quit()
    argstring_1 += " ensemble_filter_MERGED 1 "
    argstring_1 += " ensemble_filter_ORBIT 1 "
    argstring_1 += " ensemble_filter_SCALARS 1 "
    argstring_1 += " ensemble_filter_CHEMICALLY_PECULIAR 1 "
    argstring_1 += " ensemble_filter_SPECTRAL_TYPES 1 "
    argstring_1 += " ensemble_filter_HRD 1 "



    output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
    pickle_n_checksize(output_1)
    ensemble_jsons_1 = [
        line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]

    pickle_n_checksize(ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :])

    print('start')
    start = time.time()
    json_1 = handle_ensemble_string_to_json(
        ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
    )
    stop = time.time()
    print('stop')

    pickle_n_checksize(json_1)

    print("took {}s to decode".format(stop - start))
    # print("Size of the json in memory: {}".format(sys.getsizeof(json_1)))

    # print(json_1)
    # assert statements:
    assert "number_counts" in json_1.keys()
    assert "HRD" in json_1.keys()
    assert "HRD(t)" in json_1.keys()
    assert "Xyield" in json_1.keys()
    assert "distributions" in json_1.keys()
    assert "scalars" in json_1.keys()


def test_adding_ensemble_output():
    """
    Function that adds the output of 2 ensembles and compares it to the output that we get by deferring the first output
    """

    m1 = 2  # Msun
    m2 = 0.1  # Msun
    extra_mass = 10

    #############################################################################################
    # The 2 runs below use the ensemble but do not defer the output to anything else, so that the
    # results are returned directly after the run

    # Direct output commands
    argstring_1 = return_argstring(
        m1=m1, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=0
    )
    argstring_2 = return_argstring(
        m1=m1 + extra_mass,
        m2=m2,
        ensemble_filter="STELLAR_TYPE_COUNTS",
        defer_ensemble=0,
    )

    # Get outputs
    output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
    output_2 = _binary_c_bindings.run_system(argstring=argstring_2)

    test_1_ensemble_jsons_1 = [
        line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    test_1_ensemble_jsons_2 = [
        line for line in output_2.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]

    test_1_json_1 = handle_ensemble_string_to_json(
        test_1_ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
    )
    test_1_json_2 = handle_ensemble_string_to_json(
        test_1_ensemble_jsons_2[0][len("ENSEMBLE_JSON ") :]
    )

    test_1_merged_dict = merge_dicts(test_1_json_1, test_1_json_2)

    with open(os.path.join(TMP_DIR, "test", "adding_json_1.json"), "w") as file:
        file.write(json.dumps(test_1_json_1, indent=4))
    with open(os.path.join(TMP_DIR, "test", "adding_json_2.json"), "w") as file:
        file.write(json.dumps(test_1_json_2, indent=4))
    with open(os.path.join(TMP_DIR, "test", "adding_json_merged.json"), "w") as file:
        file.write(json.dumps(test_1_json_2, indent=4))

    print("Single runs done\n")

    #############################################################################################
    # The 2 runs below use the ensemble and both defer the output so that after they are finished
    # nothing is printed. After that we explicitly free the memory of the persistent_data and
    # have the output returned in that way

    # Deferred commands
    argstring_1_deferred = return_argstring(
        m1=m1, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=1
    )
    argstring_2_deferred = return_argstring(
        m1=m1 + extra_mass,
        m2=m2,
        ensemble_filter="STELLAR_TYPE_COUNTS",
        defer_ensemble=1,
    )

    # Get a memory location
    test_2_persistent_data_memaddr = (
        _binary_c_bindings.return_persistent_data_memaddr()
    )

    # Run the systems and defer the output each time
    _ = _binary_c_bindings.run_system(
        argstring=argstring_1_deferred,
        persistent_data_memaddr=test_2_persistent_data_memaddr,
    )
    _ = _binary_c_bindings.run_system(
        argstring=argstring_2_deferred,
        persistent_data_memaddr=test_2_persistent_data_memaddr,
    )

    # Have the persistent_memory adress be released and have the json outputted
    test_2_output = _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
        test_2_persistent_data_memaddr
    )
    test_2_ensemble_json = [
        line for line in test_2_output.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    test_2_json = handle_ensemble_string_to_json(
        test_2_ensemble_json[0][len("ENSEMBLE_JSON ") :]
    )

    with open(os.path.join(TMP_DIR, "test", "adding_json_deferred.json"), "w") as file:
        file.write(json.dumps(test_2_json, indent=4))

    print("Double deferred done\n")

    #############################################################################################
    # The 2 runs below use the ensemble and the first one defers the output to the memory,
    # Then the second one uses that memory to combine its results with, but doesn't defer the
    # data after that, so it will print it after the second run is done

    test_3_persistent_data_memaddr = (
        _binary_c_bindings.return_persistent_data_memaddr()
    )

    # Run the systems and defer the output once and the second time not, so that the second run
    # automatically prints out the results
    _ = _binary_c_bindings.run_system(
        argstring=argstring_1_deferred,
        persistent_data_memaddr=test_3_persistent_data_memaddr,
    )
    test_3_output_2 = _binary_c_bindings.run_system(
        argstring=argstring_2, persistent_data_memaddr=test_3_persistent_data_memaddr
    )
    test_3_ensemble_jsons = [
        line
        for line in test_3_output_2.splitlines()
        if line.startswith("ENSEMBLE_JSON")
    ]
    test_3_json = handle_ensemble_string_to_json(
        test_3_ensemble_jsons[0][len("ENSEMBLE_JSON ") :]
    )

    with open(
        os.path.join(TMP_DIR, "test", "adding_json_deferred_and_output.json"), "w"
    ) as f:
        f.write(json.dumps(test_3_json, indent=4))

    print("Single deferred done\n")

    #
    assert_message_1 = """
    The structure of the manually merged is not the same as the merged by double deferring
    """
    assert_message_2 = """
    The structure of the manually merged is not the same as the merged by deferring once
    and output on the second run
    """

    #
    # print(json.dumps(test_1_merged_dict, indent=4))
    # print(json.dumps(test_2_json, indent=4))

    # TODO: add more asserts.
    #
    assert inspect_dict(test_1_merged_dict, print_structure=False) == inspect_dict(
        test_2_json, print_structure=False
    ), assert_message_1
    # assert inspect_dict(test_1_merged_dict, print_structure=False) == inspect_dict(test_3_json, print_structure=False), assert_message_2


def test_combine_with_empty_json():
    """
    Test for merging with an empty dict
    """
    
    argstring_1 = return_argstring(defer_ensemble=0)
    output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
    ensemble_jsons_1 = [
        line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
    ]
    json_1 = handle_ensemble_string_to_json(
        ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
    )

    assert_message = (
        "combining output json with empty dict should give same result as initial json"
    )
    assert merge_dicts(json_1, {}) == json_1, assert_message


def test_free_and_json_output():
    """
    Function that tests the freeing of the memory adress and the output of the json
    """

    m1 = 2  # Msun
    m2 = 0.1  # Msun

    # Get argstring:
    argstring_1 = return_argstring(
        m1=m2, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=1
    )

    # Get a memory adress:
    persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

    # Evolve and defer output
    print("evolving")
    output_1_deferred = _binary_c_bindings.run_system(
        argstring=argstring_1, persistent_data_memaddr=persistent_data_memaddr
    )
    print("Evolved")
    print("Output:")
    print(textwrap.indent(str(output_1_deferred), "\t"))

    # Free memory adress
    print("freeing")
    json_output_by_freeing = _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
        persistent_data_memaddr
    )
    print("Freed")
    print("Output:")
    print(textwrap.indent(str(json_output_by_freeing), "\t"))

    parsed_json = handle_ensemble_string_to_json(
        json_output_by_freeing.splitlines()[0][len("ENSEMBLE_JSON ") :],
    )
    print(parsed_json)

    # ensemble_jsons_1 = [line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")]
    # json_1 = json.loads(ensemble_jsons_1[0][len("ENSEMBLE_JSON "):], cls=binarycDecoder)


def all():
    # test_return_persistent_data_memaddr()
    # test_passing_persistent_data_to_run_system()
    # test_full_ensemble_output()
    test_adding_ensemble_output()
    test_free_and_json_output()
    test_combine_with_empty_json()


####
if __name__ == "__main__":
    # test_return_persistent_data_memaddr()
    # test_passing_persistent_data_to_run_system()
    # test_full_ensemble_output()
    # test_adding_ensemble_output()
    # test_free_and_json_output()
    # test_combine_with_empty_json()
    all()
    print("Done")
