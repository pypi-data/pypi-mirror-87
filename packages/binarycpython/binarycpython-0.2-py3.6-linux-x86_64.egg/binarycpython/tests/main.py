# Main file for the tests. This file imports all the combined_test functions from all files.
from population.grid_tests import test_all as test_all_grid_tests
from function_tests import test_all as test_all_function_tests

test_all_grid_tests()
test_all_function_tests()
