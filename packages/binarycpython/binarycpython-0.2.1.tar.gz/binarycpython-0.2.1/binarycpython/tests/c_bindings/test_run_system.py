from binarycpython import _binary_c_bindings

import textwrap


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

    # print("function: test_run_system")
    # print("Binary_c output:")
    # print(textwrap.indent(output, "\t"))

    assert "SINGLE_STAR_LIFETIME" in output, "Run system not working properly"


####
if __name__ == "__main__":
    test_run_system()
