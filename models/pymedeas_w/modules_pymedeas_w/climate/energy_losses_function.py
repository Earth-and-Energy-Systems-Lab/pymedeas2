"""
Module energy_losses_function
Translated using PySD version 2.2.3
"""


def a_logistic():
    """
    Real Name: a logistic
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Value of parameter "a" in the logistic equation.
    """
    return _ext_constant_a_logistic()


_ext_constant_a_logistic = ExtConstant(
    "../parameters.xlsx",
    "World",
    "damage_function_parameter_a",
    {},
    _root,
    "_ext_constant_a_logistic",
)


def activate_elf():
    """
    Real Name: activate ELF
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Active/deactivate the energy loss function by scenario: 1: activate 0: not active
    """
    return _ext_constant_activate_elf()


_ext_constant_activate_elf = ExtConstant(
    "../../scenarios/scen_w.xlsx", "BAU", "ELF", {}, _root, "_ext_constant_activate_elf"
)


def b_logistic():
    """
    Real Name: b logistic
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Value of parameter "b" in the logistic equation.
    """
    return _ext_constant_b_logistic()


_ext_constant_b_logistic = ExtConstant(
    "../parameters.xlsx",
    "World",
    "damage_function_parameter_b",
    {},
    _root,
    "_ext_constant_b_logistic",
)


def elf():
    """
    Real Name: ELF
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        activate_elf(),
        lambda: 1
        - 1 / (1 + np.exp((co2_ppm_concentrations() - a_logistic()) / b_logistic())),
        lambda: 0,
    )


def elf_2015():
    """
    Real Name: ELF 2015
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_elf_2015()


_sampleiftrue_elf_2015 = SampleIfTrue(
    lambda: time() < 2015, lambda: elf(), lambda: elf(), "_sampleiftrue_elf_2015"
)


def share_e_losses_cc():
    """
    Real Name: share E losses CC
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of energy losses in relation to TFED due to climate change impacts.
    """
    return elf() - elf_2015()
