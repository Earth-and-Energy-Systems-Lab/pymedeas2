"""
Module demand_for_ev_batteries
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def cum_materials_requirements_for_ev_batteries():
    """
    Real Name: cum materials requirements for EV batteries
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Total cumulative materials requirements for EV batteries.
    """
    return _integ_cum_materials_requirements_for_ev_batteries()


_integ_cum_materials_requirements_for_ev_batteries = Integ(
    lambda: total_materials_required_for_ev_batteries(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_requirements_for_ev_batteries",
)


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_ev_batteries():
    """
    Real Name: cum materials to extract for EV batteries
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries()


_integ_cum_materials_to_extract_for_ev_batteries = Integ(
    lambda: total_materials_to_extract_for_ev_batteries_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_ev_batteries",
)


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_ev_batteries_from_2015():
    """
    Real Name: cum materials to extract for EV batteries from 2015
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries_from_2015()


_integ_cum_materials_to_extract_for_ev_batteries_from_2015 = Integ(
    lambda: total_materials_to_extract_for_ev_batteries_from_2015_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_ev_batteries_from_2015",
)


def initial_cumulated_material_requirements_for_ev_batteries_1995():
    """
    Real Name: initial cumulated material requirements for EV batteries 1995
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 0


@subs(["materials"], _subscript_dict)
def materials_per_new_capacity_installed_ev_batteries():
    """
    Real Name: materials per new capacity installed EV batteries
    Original Eqn:
    Units: kg/MW
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Materials requirements per EV battery.
    """
    return _ext_constant_materials_per_new_capacity_installed_ev_batteries()


_ext_constant_materials_per_new_capacity_installed_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_ev_batteries*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_materials_per_new_capacity_installed_ev_batteries",
)


@subs(["materials"], _subscript_dict)
def materials_required_for_ev_batteries_mt():
    """
    Real Name: materials required for EV batteries Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual materials required for the fabrication of EV batteries.
    """
    return (
        newreplaced_batteries_tw()
        * materials_per_new_capacity_installed_ev_batteries()
        * m_per_t()
        / kg_per_mt()
    )


@subs(["materials"], _subscript_dict)
def total_materials_required_for_ev_batteries():
    """
    Real Name: Total materials required for EV batteries
    Original Eqn:
    Units: Mt/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Total annual materials requirements for EV batteries.
    """
    return materials_required_for_ev_batteries_mt()


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_ev_batteries_from_2015_mt():
    """
    Real Name: Total materials to extract for EV batteries from 2015 Mt
    Original Eqn:
    Units: Mt/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual materials to be mined for EV batteries from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_materials_to_extract_for_ev_batteries_mt(),
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_ev_batteries_mt():
    """
    Real Name: Total materials to extract for EV batteries Mt
    Original Eqn:
    Units: Mt/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual materials to be mined for the construction of EV batteries.
    """
    return total_materials_required_for_ev_batteries() * (
        1 - recycling_rates_minerals_alt_techn()
    )


@subs(["materials"], _subscript_dict)
def total_recycled_materials_for_ev_batteries_mt():
    """
    Real Name: Total recycled materials for EV batteries Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Total recycled materials for EV batteries.
    """
    return (
        total_materials_required_for_ev_batteries()
        - total_materials_to_extract_for_ev_batteries_mt()
    )
