"""
File containing functions for HPC computing, distributed tasks on clusters etc.

Functions that the slurm and condor subroutines of the population object use.

Mainly divided in 2 sections: Slurm and Condor
"""

import os
import sys
import time
import subprocess
import __main__ as main


def get_slurm_version():
    """
    Function that checks whether slurm is installed and returns the version if its installed.

    Only tested this with slurm v17+
    """

    slurm_version = None

    try:
        slurm_version = (
            subprocess.run(["sinfo", "-V"], stdout=subprocess.PIPE, check=True)
            .stdout.decode("utf-8")
            .split()
        )[1]
    except FileNotFoundError as err:
        print(err)
        print(err.args)
        print("Slurm is not installed or not loaded")
    except Exception as err:
        print(err)
        print(err.args)
        print("Unknown error, contact me about this")

    return slurm_version


def get_condor_version():
    """
    Function that checks whether slurm is installed and returns the version if its installed.

    otherwise returns None

    Result has to be condor v8 or higher
    """

    condor_version = None

    try:
        condor_version = (
            subprocess.run(
                ["condor_q", "--version"], stdout=subprocess.PIPE, check=True
            )
            .stdout.decode("utf-8")
            .split()
        )[1]
    except FileNotFoundError as err:
        print("Slurm is not installed or not loaded: ")
        print(err)
        print(err.args)
    except Exception as err:
        print("Unknown error, contact me about this: ")
        print(err)
        print(err.args)

    return condor_version


def create_directories_hpc(working_dir):
    """
    Function to create a set of directories, given a root directory

    These directories will contain stuff for the HPC runs
    """

    # Check if working_dir exists
    if not os.path.isdir(working_dir):
        print("Error. Working directory {} does not exist! Aborting")
        raise ValueError

    directories_list = [
        "scripts",
        "stdout",
        "stderr",
        "results",
        "logs",
        "status",
        "joining",
    ]

    # Make directories.
    for subdir in directories_list:
        full_path = os.path.join(working_dir, subdir)
        os.makedirs(full_path, exist_ok=True)

    # Since the directories are probably made on some mount which has to go over NFS
    # we should explicitly check if they are created
    print("Checking if creating the directories has finished...")
    directories_exist = False
    while directories_exist:
        directories_exist = True

        for subdir in directories_list:
            full_path = os.path.join(working_dir, subdir)

            if not os.path.isdir(full_path):
                time.sleep(1)
                directories_exist = False
    print("..Finished! Directories exist.")


def path_of_calling_script():
    """
    Function to get the name of the script the user executes.
    """

    return main.__file__


def get_python_details():
    """
    Function to get some info about the used python version and virtualenv etc
    """

    python_info_dict = {}

    #
    python_info_dict["virtualenv"] = os.getenv("VIRTUAL_ENV")
    python_info_dict["executable"] = sys.executable
    python_info_dict["version"] = sys.version

    return python_info_dict
