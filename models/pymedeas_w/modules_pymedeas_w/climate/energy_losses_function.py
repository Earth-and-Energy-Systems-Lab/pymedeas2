"""
Module climate.energy_losses_function
Translated using PySD version 3.10.0
"""


@component.add(
    name="a logistic",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_a_logistic"},
)
def a_logistic():
    """
    Value of parameter "a" in the logistic equation.
    """
    return _ext_constant_a_logistic()


_ext_constant_a_logistic = ExtConstant(
    "../parameters.xlsx",
    "World",
    "damage_function_parameter_a",
    {},
    _root,
    {},
    "_ext_constant_a_logistic",
)


@component.add(
    name="activate ELF",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_elf"},
)
def activate_elf():
    """
    Active/deactivate the energy loss function by scenario: 1: activate 0: not active
    """
    return _ext_constant_activate_elf()


_ext_constant_activate_elf = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "ELF",
    {},
    _root,
    {},
    "_ext_constant_activate_elf",
)


@component.add(
    name="b logistic",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_b_logistic"},
)
def b_logistic():
    """
    Value of parameter "b" in the logistic equation.
    """
    return _ext_constant_b_logistic()


_ext_constant_b_logistic = ExtConstant(
    "../parameters.xlsx",
    "World",
    "damage_function_parameter_b",
    {},
    _root,
    {},
    "_ext_constant_b_logistic",
)


@component.add(
    name="ELF",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_elf": 1,
        "co2_ppm_concentrations": 1,
        "a_logistic": 1,
        "b_logistic": 1,
    },
)
def elf():
    return if_then_else(
        activate_elf(),
        lambda: 1
        - 1 / (1 + np.exp((co2_ppm_concentrations() - a_logistic()) / b_logistic())),
        lambda: 0,
    )


@component.add(
    name="ELF 2015",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_elf_2015": 1},
    other_deps={
        "_sampleiftrue_elf_2015": {"initial": {"elf": 1}, "step": {"time": 1, "elf": 1}}
    },
)
def elf_2015():
    return _sampleiftrue_elf_2015()


_sampleiftrue_elf_2015 = SampleIfTrue(
    lambda: time() < 2015, lambda: elf(), lambda: elf(), "_sampleiftrue_elf_2015"
)


@component.add(
    name="share E losses CC",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"elf": 1, "elf_2015": 1},
)
def share_e_losses_cc():
    """
    Share of energy losses in relation to TFED due to climate change impacts.
    """
    return elf() - elf_2015()
