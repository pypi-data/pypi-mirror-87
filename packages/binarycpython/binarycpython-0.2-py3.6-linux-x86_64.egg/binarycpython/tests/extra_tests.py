import subprocess
import os

# Script containing extra tests
# TODO: store the version somewhere


def test_binary_c_installed():
    binary_c_dir = os.getenv("BINARY_C", None)

    assert (
        binary_c_dir is not None
    ), "Error: the BINARY_C environment variable is not set."
    assert os.path.isfile(
        os.path.join(binary_c_dir, "binary_c")
    ), "binary_c doesn't exist!"


def test_binary_c_version():
    required_binary_c_versions = ["2.1.7"]

    binary_c_dir = os.getenv("BINARY_C", None)
    binary_c_config = os.path.join(binary_c_dir, "binary_c-config")

    installed_binary_c_version = (
        subprocess.run([binary_c_config, "version"], stdout=subprocess.PIPE, check=True)
        .stdout.decode("utf-8")
        .split()
    )[0]

    message = """
    The binary_c version that is installed ({}) does not match the binary_c versions ({}) 
    that this release of the binary_c python module requires. 
    """.format(
        installed_binary_c_version, required_binary_c_versions
    )
    assert installed_binary_c_version in required_binary_c_versions, message


###

if __name__ == "__main__":
    test_binary_c_version()
    test_binary_c_installed()
