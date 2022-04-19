"""
Module energy_losses_function
Translated using PySD version 3.0.0
"""


@component.add(
    name="a logistic", units="Dmnl", comp_type="Constant", comp_subtype="External"
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
    name="activate ELF", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def activate_elf():
    """
    Active/deactivate the energy loss function by scenario: 1: activate 0: not active
    """
    return _ext_constant_activate_elf()


_ext_constant_activate_elf = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "ELF",
    {},
    _root,
    {},
    "_ext_constant_activate_elf",
)


@component.add(
    name="b logistic", units="Dmnl", comp_type="Constant", comp_subtype="External"
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


@component.add(name="ELF", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal")
def elf():
    return if_then_else(
        activate_elf(),
        lambda: 1
        - 1 / (1 + np.exp((co2_ppm_concentrations() - a_logistic()) / b_logistic())),
        lambda: 0,
    )


@component.add(name="ELF 2015", comp_type="Stateful", comp_subtype="SampleIfTrue")
def elf_2015():
    return _sampleiftrue_elf_2015()


_sampleiftrue_elf_2015 = SampleIfTrue(
    lambda: time() < 2015, lambda: elf(), lambda: elf(), "_sampleiftrue_elf_2015"
)


@component.add(
    name="share E losses CC", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def share_e_losses_cc():
    """
    Share of energy losses in relation to TFED due to climate change impacts.
    """
    return elf() - elf_2015()
