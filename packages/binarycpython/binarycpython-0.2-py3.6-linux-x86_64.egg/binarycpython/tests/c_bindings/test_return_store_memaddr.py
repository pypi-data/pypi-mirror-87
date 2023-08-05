import textwrap
from binarycpython import _binary_c_bindings


def test_return_store_memaddr():
    output = _binary_c_bindings.return_store_memaddr()

    print("function: test_return_store")
    print("store memory adress:")
    print(textwrap.indent(str(output), "\t"))


def test_unload_store_memaddr():
    output = _binary_c_bindings.return_store_memaddr()

    print("function: test_return_store")
    print("store memory adress:")
    print(textwrap.indent(str(output), "\t"))
    print(type(output))
    _ = _binary_c_bindings.free_store_memaddr(output)
    print("freed store memaddr")


####
if __name__ == "__main__":
    test_return_store_memaddr()
    test_unload_store_memaddr()
