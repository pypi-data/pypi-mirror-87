from binarycpython.utils.functions import (
    get_help_super,
    get_help_all,
    get_help,
)

#############################
# Script that contains unit tests for functions from the binarycpython.utils.functions file


def test_get_help_super():
    """
    Function to test the get_help_super function
    """

    get_help_super_output = get_help_super()
    get_help_super_keys = get_help_super_output.keys()

    assert "stars" in get_help_super_keys, "missing section"
    assert "binary" in get_help_super_keys, "missing section"
    assert "nucsyn" in get_help_super_keys, "missing section"
    assert "output" in get_help_super_keys, "missing section"
    assert "i/o" in get_help_super_keys, "missing section"
    assert "algorithms" in get_help_super_keys, "missing section"
    assert "misc" in get_help_super_keys, "missing section"


def test_get_help_all():
    """
    Function to test the get_help_all function
    """

    get_help_all_output = get_help_all(print_help=False)
    get_help_all_keys = get_help_all_output.keys()

    assert "stars" in get_help_all_keys, "missing section"
    assert "binary" in get_help_all_keys, "missing section"
    assert "nucsyn" in get_help_all_keys, "missing section"
    assert "output" in get_help_all_keys, "missing section"
    assert "i/o" in get_help_all_keys, "missing section"
    assert "algorithms" in get_help_all_keys, "missing section"
    assert "misc" in get_help_all_keys, "missing section"


def test_get_help():
    """
    Function to test the get_help function
    """

    assert (
        get_help("M_1", print_help=False)["parameter_name"] == "M_1"
    ), "get_help('M_1') should return the correct parameter name"


def all():
    test_get_help()
    test_get_help_all()
    test_get_help_super()


if __name__ == "__main__":
    all()
