"""
Module demand_for_ev_batteries
Translated using PySD version 2.1.0
"""


@subs(["materials"], _subscript_dict)
def cum_materials_requirements_for_ev_batteries():
    """
    Real Name: cum materials requirements for EV batteries
    Original Eqn: INTEG ( Total materials required for EV batteries[materials], initial cumulated material requirements for EV batteries 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total cumulative materials requirements for EV batteries.
    """
    return _integ_cum_materials_requirements_for_ev_batteries()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_ev_batteries():
    """
    Real Name: cum materials to extract for EV batteries
    Original Eqn: INTEG ( Total materials to extract for EV batteries Mt[materials], initial cumulated material requirements for EV batteries 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_ev_batteries_from_2015():
    """
    Real Name: cum materials to extract for EV batteries from 2015
    Original Eqn: INTEG ( Total materials to extract for EV batteries from 2015 Mt[materials], initial cumulated material requirements for EV batteries 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries_from_2015()


def initial_cumulated_material_requirements_for_ev_batteries_1995():
    """
    Real Name: initial cumulated material requirements for EV batteries 1995
    Original Eqn: 0
    Units: Mt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0


@subs(["materials"], _subscript_dict)
def materials_per_new_capacity_installed_ev_batteries():
    """
    Real Name: materials per new capacity installed EV batteries
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'materials_per_new_capacity_installed_ev_batteries*')
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Materials requirements per EV battery.
    """
    return _ext_constant_materials_per_new_capacity_installed_ev_batteries()


@subs(["materials"], _subscript_dict)
def materials_required_for_ev_batteries_mt():
    """
    Real Name: materials required for EV batteries Mt
    Original Eqn: "new+replaced batteries TW"*materials per new capacity installed EV batteries[materials]*M per T/kg per Mt
    Units: Mt
    Limits: (None, None)
    Type: component
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
    Original Eqn: materials required for EV batteries Mt[materials]
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total annual materials requirements for EV batteries.
    """
    return materials_required_for_ev_batteries_mt()


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_ev_batteries_from_2015_mt():
    """
    Real Name: Total materials to extract for EV batteries from 2015 Mt
    Original Eqn: IF THEN ELSE(Time<2015,0,Total materials to extract for EV batteries Mt[materials] )
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual materials to be mined for EV batteries from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: total_materials_to_extract_for_ev_batteries_mt(),
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_ev_batteries_mt():
    """
    Real Name: Total materials to extract for EV batteries Mt
    Original Eqn: Total materials required for EV batteries[materials]*(1-recycling rates minerals alt techn[materials])
    Units: Mt/year
    Limits: (None, None)
    Type: component
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
    Original Eqn: Total materials required for EV batteries[materials]-Total materials to extract for EV batteries Mt[materials]
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total recycled materials for EV batteries.
    """
    return (
        total_materials_required_for_ev_batteries()
        - total_materials_to_extract_for_ev_batteries_mt()
    )


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_requirements_for_ev_batteries():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_requirements_for_ev_batteries
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_requirements_for_ev_batteries function
    """
    return initial_cumulated_material_requirements_for_ev_batteries_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_requirements_for_ev_batteries():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_requirements_for_ev_batteries
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_requirements_for_ev_batteries function
    """
    return total_materials_required_for_ev_batteries()


_integ_cum_materials_requirements_for_ev_batteries = Integ(
    _integ_input_cum_materials_requirements_for_ev_batteries,
    _integ_init_cum_materials_requirements_for_ev_batteries,
    "_integ_cum_materials_requirements_for_ev_batteries",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_for_ev_batteries():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_ev_batteries
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_for_ev_batteries function
    """
    return initial_cumulated_material_requirements_for_ev_batteries_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_for_ev_batteries():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_ev_batteries
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_for_ev_batteries function
    """
    return total_materials_to_extract_for_ev_batteries_mt()


_integ_cum_materials_to_extract_for_ev_batteries = Integ(
    _integ_input_cum_materials_to_extract_for_ev_batteries,
    _integ_init_cum_materials_to_extract_for_ev_batteries,
    "_integ_cum_materials_to_extract_for_ev_batteries",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_for_ev_batteries_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_ev_batteries_from_2015
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_for_ev_batteries_from_2015 function
    """
    return initial_cumulated_material_requirements_for_ev_batteries_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_for_ev_batteries_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_ev_batteries_from_2015
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_for_ev_batteries_from_2015 function
    """
    return total_materials_to_extract_for_ev_batteries_from_2015_mt()


_integ_cum_materials_to_extract_for_ev_batteries_from_2015 = Integ(
    _integ_input_cum_materials_to_extract_for_ev_batteries_from_2015,
    _integ_init_cum_materials_to_extract_for_ev_batteries_from_2015,
    "_integ_cum_materials_to_extract_for_ev_batteries_from_2015",
)


_ext_constant_materials_per_new_capacity_installed_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_ev_batteries*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_materials_per_new_capacity_installed_ev_batteries",
)
