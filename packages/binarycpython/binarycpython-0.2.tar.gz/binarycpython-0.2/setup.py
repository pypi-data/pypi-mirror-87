"""
Setup script for binarycpython
"""
import os
import subprocess
import re
import sys

import setuptools

from distutils.core import setup, Extension
import distutils.command.build

import md_to_rst

# TODO: replace the tasks that call binary_c-config with a single function that handles the return status a bit better. 

# Functions
def readme():
    """Opens readme file and returns content"""
    with open("README") as file:
        return file.read()


# def readme_rst():
#     """Opens readme file and returns contents converted to rst"""
#     with open("README.md") as file:
#         return md_to_rst.convertMarkdownToRst(file.read())


def license():
    """Opens license file and returns the content"""
    with open("LICENSE.md") as file:
        return file.read()


def check_version(installed_binary_c_version, required_binary_c_versions):
    """Function to check the installed version and compare it to the required version"""
    message = """
    Something went wrong. Make sure that binary_c config exists. 
    Possibly the binary_c version that is installed ({}) does not match the binary_c versions ({})
    that this release of the binary_c python module requires.
    """.format(
        installed_binary_c_version, required_binary_c_versions
    )
    assert installed_binary_c_version in required_binary_c_versions, message

def execute_make():
    """
    Function to execute the makefile. 

    This makefile builds the binary_c_python_api library that python will use to interface wth
    """

    # Custom extra command:
    make_command = ["make"]

    p = subprocess.run(make_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = p.stdout # stdout = normal output
    stderr = p.stderr # stderr = error output

    if p.returncode != 0:
        print("Something went wrong when executing the makefile:")
        print(stderr.decode('utf-8'))
        print("Aborting")
        sys.exit(-1)

    else:
        print(stdout.decode("utf-8"))
        print("Successfully built the libbinary_c_api.so")



###
REQUIRED_BINARY_C_VERSIONS = ["2.1.7"]

####
GSL_DIR = os.getenv("GSL_DIR", None)
if not GSL_DIR:
    print(
        "Warning: GSL_DIR is not set, this might lead to errors along the installation if\
        there is no other version of GSL in the include dirs"
    )
BINARY_C_DIR = os.getenv("BINARY_C", None)
if not BINARY_C_DIR:
    print("Error: the BINARY_C environment variable is not set. Aborting setup")
    quit()

# TODO: write code to know exact parent directory of this file.
CWD = os.getcwd()

############################################################
# Getting information from binary_c
############################################################

# binary_c must be installed.
BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")

BINARY_C_VERSION = (
    subprocess.run([BINARY_C_CONFIG, "version"], stdout=subprocess.PIPE, check=True)
    .stdout.decode("utf-8")
    .split()
)
check_version(BINARY_C_VERSION[0], REQUIRED_BINARY_C_VERSIONS)

BINARY_C_INCDIRS = (
    subprocess.run(
        [BINARY_C_CONFIG, "incdirs_list"], stdout=subprocess.PIPE, check=True
    )
    .stdout.decode("utf-8")
    .split()
)
BINARY_C_LIBDIRS = (
    subprocess.run(
        [BINARY_C_CONFIG, "libdirs_list"], stdout=subprocess.PIPE, check=True
    )
    .stdout.decode("utf-8")
    .split()
)
BINARY_C_CFLAGS = (
    subprocess.run([BINARY_C_CONFIG, "cflags"], stdout=subprocess.PIPE, check=True)
    .stdout.decode("utf-8")
    .split()
)
# BINARY_C_CFLAGS.remove('-fvisibility=hidden')
BINARY_C_LIBS = (
    subprocess.run([BINARY_C_CONFIG, "libs_list"], stdout=subprocess.PIPE, check=True)
    .stdout.decode("utf-8")
    .split()
)

# create list of tuples of defined macros
BINARY_C_DEFINE_MACROS = []
DEFINES = (
    subprocess.run(
        [BINARY_C_CONFIG, "define_macros"], stdout=subprocess.PIPE, check=True
    )
    .stdout.decode("utf-8")
    .split()
)

LONE = re.compile("^-D(.+)$")
PARTNER = re.compile("^-D(.+)=(.+)$")
for x in DEFINES:
    y = PARTNER.match(x)
    if y:
        BINARY_C_DEFINE_MACROS.extend([(y.group(1), y.group(2))])
    else:
        y = LONE.match(x)
        if y:
            BINARY_C_DEFINE_MACROS.extend([(y.group(1), None)])

# add API header file
API_h = os.path.join(BINARY_C_DIR, "src", "API", "binary_c_API.h")

############################################################
# Setting all directories and LIBRARIES to their final values
############################################################
INCLUDE_DIRS = (
    [
        os.path.join(BINARY_C_DIR, "src"),
        os.path.join(BINARY_C_DIR, "src", "API"),
        "include",
    ]
    + BINARY_C_INCDIRS
    + [os.path.join(GSL_DIR, "include")]
    if GSL_DIR
    else []
)

LIBRARIES = ["binary_c"] + BINARY_C_LIBS + ["binary_c_python_api"]

LIBRARY_DIRS = [
    os.path.join(BINARY_C_DIR, "src"),
    "./",
    os.path.join(CWD, "lib/"),
] + BINARY_C_LIBDIRS

RUNTIME_LIBRARY_DIRS = [
    os.path.join(BINARY_C_DIR, "src"),
    "./",
    os.path.join(CWD, "lib/"),
] + BINARY_C_LIBDIRS

# filter out duplicates
INCLUDE_DIRS = list(dict.fromkeys(INCLUDE_DIRS))
BINARY_C_LIBS = list(dict.fromkeys(BINARY_C_LIBS))
LIBRARIES = list(dict.fromkeys(LIBRARIES))
LIBRARY_DIRS = list(dict.fromkeys(LIBRARY_DIRS))
RUNTIME_LIBRARY_DIRS = list(dict.fromkeys(RUNTIME_LIBRARY_DIRS))

# 
# print('\n')
# print("BINARY_C_CONFIG: ", str(BINARY_C_CONFIG) + "\n")
# print("incdirs: ", str(INCLUDE_DIRS) + "\n")
# print("BINARY_C_LIBS: ", str(BINARY_C_LIBS) + "\n")
# print("LIBRARIES: ", str(LIBRARIES) + "\n")
# print("LIBRARY_DIRS: ", str(LIBRARY_DIRS) + "\n")
# print("RUNTIME_LIBRARY_DIRS: ", str(RUNTIME_LIBRARY_DIRS) + "\n")
# print("BINARY_C_CFLAGS: ", str(BINARY_C_CFLAGS) + "\n")
# print("API_h: ", str(API_h) + "\n")
# print("macros: ", str(BINARY_C_DEFINE_MACROS) + "\n")
# print('\n')

############################################################
# Making the extension function
############################################################
# TODO: fix that this one also compiles the code itself

BINARY_C_PYTHON_API_MODULE = Extension(
    # name="binarycpython.core.binary_c",
    name="binarycpython._binary_c_bindings",
    sources=["src/binary_c_python.c"],
    include_dirs=INCLUDE_DIRS,
    libraries=LIBRARIES,
    library_dirs=LIBRARY_DIRS,
    runtime_library_dirs=RUNTIME_LIBRARY_DIRS,
    define_macros=[] + BINARY_C_DEFINE_MACROS,
    extra_objects=[],
    extra_compile_args=[],
    language="C",
)

############################################################
# Making the extension function
############################################################

# Override build command
class CustomBuildCommand(distutils.command.build.build):

    def run(self):
        execute_make()

        # Run the original build command
        # print(super().run())
        distutils.command.build.build.run(self)

setup(
    name="binarycpython",
    version="0.2",
    description="""
    This is a python API for binary_c (versions {}) by David Hendriks, Rob Izzard and collaborators.
    Based on the initial set up by Jeff andrews.
    It is tested and designed to work for versions {}, we can't guarantee proper functioning for other versions

    If you want to use a different version of binary_c, download and install a different version of this package
    """.format(
        str(REQUIRED_BINARY_C_VERSIONS), str(REQUIRED_BINARY_C_VERSIONS)
    ),
    author="David Hendriks",
    author_email="davidhendriks93@gmail.com",
    # long_description=readme(),
    long_description="hello",
    url="https://gitlab.eps.surrey.ac.uk/ri0005/binary_c-python",
    license="gpl",
    keywords = ['binary_c', 'astrophysics', 'stellar evolution', 'population synthesis'],   # Keywords that define your package best
    packages=[
        "binarycpython",
        "binarycpython.utils",
        "binarycpython.core",
        "binarycpython.tests",
        "binarycpython.tests.c_bindings",
    ],
    install_requires=["numpy", "pytest", "h5py"],
    include_package_data=True,
    ext_modules=[BINARY_C_PYTHON_API_MODULE],  # binary_c must be loaded

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    cmdclass={'build': CustomBuildCommand},

)
