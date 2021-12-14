"""
Module potential_ehr_ear
Translated using PySD version 2.1.0
"""


def geot_pe_potential_for_heat_ej():
    """
    Real Name: Geot PE potential for heat EJ
    Original Eqn: Geot PE potential for heat TWth*EJ per TWh/TWe per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Geothermal potential (primary energy) for producing heat.
    """
    return geot_pe_potential_for_heat_twth() * ej_per_twh() / twe_per_twh()


def geot_pe_potential_for_heat_twth():
    """
    Real Name: Geot PE potential for heat TWth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C56')
    Units: TWth
    Limits: (None, None)
    Type: constant
    Subs: None

    Geothermal primary energy potential for heat.
    """
    return _ext_constant_geot_pe_potential_for_heat_twth()


def max_fe_potential_biogas_for_heat():
    """
    Real Name: max FE potential biogas for heat
    Original Eqn: max PE biogas EJ*share PES biogas for heat*efficiency biogas for heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential (final energy) of biogas for heat.
    """
    return (
        max_pe_biogas_ej() * share_pes_biogas_for_heat() * efficiency_biogas_for_heat()
    )


@subs(["RES heat"], _subscript_dict)
def max_fe_potential_res_for_heat():
    """
    Real Name: Max FE potential RES for heat
    Original Eqn:
      Max FE RES for heat[solar heat]
      Max FE RES for heat[geot heat]
      max PE potential solid bioE for heat EJ*Efficiency RES heat[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']


    """
    return xrmerge(
        rearrange(
            float(max_fe_res_for_heat().loc["solar heat"]),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            float(max_fe_res_for_heat().loc["geot heat"]),
            ["RES heat"],
            {"RES heat": ["geot heat"]},
        ),
        rearrange(
            max_pe_potential_solid_bioe_for_heat_ej()
            * float(efficiency_res_heat().loc["solid bioE heat"]),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


@subs(["RES heat"], _subscript_dict)
def max_fe_res_for_heat():
    """
    Real Name: Max FE RES for heat
    Original Eqn:
      max FE solar thermal urban TWth*EJ per TWh/TWe per TWh
      Max PE RES for heat[geot heat]*Efficiency RES heat[geot heat]
      Max PE RES for heat[solid bioE heat]*Efficiency RES heat[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Maximum level of final energy for producing heat from renewables by
        technology. For technologies solar heat and geot heat this variable
        corresponds with the maximum potential, but not for solids bioenergy due
        to the competing use for heat and electricity.
    """
    return xrmerge(
        rearrange(
            max_fe_solar_thermal_urban_twth() * ej_per_twh() / twe_per_twh(),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            float(max_pe_res_for_heat().loc["geot heat"])
            * float(efficiency_res_heat().loc["geot heat"]),
            ["RES heat"],
            {"RES heat": ["geot heat"]},
        ),
        rearrange(
            float(max_pe_res_for_heat().loc["solid bioE heat"])
            * float(efficiency_res_heat().loc["solid bioE heat"]),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


def max_pe_potential_biogas_for_heat():
    """
    Real Name: max PE potential biogas for heat
    Original Eqn: max PE biogas EJ*share PES biogas for heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy potential of biogas for heat taking into account the
        current share.
    """
    return max_pe_biogas_ej() * share_pes_biogas_for_heat()


@subs(["RES heat"], _subscript_dict)
def max_pe_potential_res_for_heat():
    """
    Real Name: Max PE potential RES for heat
    Original Eqn:
      Max PE RES for heat[solar heat]
      Max PE RES for heat[geot heat]
      max PE potential solid bioE for heat EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']


    """
    return xrmerge(
        rearrange(
            float(max_pe_res_for_heat().loc["solar heat"]),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            float(max_pe_res_for_heat().loc["geot heat"]),
            ["RES heat"],
            {"RES heat": ["geot heat"]},
        ),
        rearrange(
            max_pe_potential_solid_bioe_for_heat_ej(),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


def max_pe_potential_tot_res_heat_ej():
    """
    Real Name: max PE potential tot RES heat EJ
    Original Eqn: max PE potential biogas for heat+SUM(Max PE potential RES for heat[RES heat!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum total primary energy potential of RES for heat.
    """
    return max_pe_potential_biogas_for_heat() + sum(
        max_pe_potential_res_for_heat(), dim=("RES heat",)
    )


@subs(["RES heat"], _subscript_dict)
def max_pe_res_for_heat():
    """
    Real Name: Max PE RES for heat
    Original Eqn:
      max FE solar thermal urban TWth/Efficiency RES heat[solar heat]
      Geot PE potential for heat EJ
      available max PE solid bioE for heat EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Maximum level of primary energy for producing heat from renewables by
        technology.
    """
    return xrmerge(
        rearrange(
            max_fe_solar_thermal_urban_twth()
            / float(efficiency_res_heat().loc["solar heat"]),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            geot_pe_potential_for_heat_ej(), ["RES heat"], {"RES heat": ["geot heat"]}
        ),
        rearrange(
            available_max_pe_solid_bioe_for_heat_ej(),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


def max_tot_fe_potential_res_for_heat():
    """
    Real Name: Max tot FE potential RES for heat
    Original Eqn: SUM(Max FE potential RES for heat[RES heat!])+max FE potential biogas for heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential (final energy) for producing heat from renewables.
    """
    return (
        sum(max_fe_potential_res_for_heat(), dim=("RES heat",))
        + max_fe_potential_biogas_for_heat()
    )


def percent_remaining_potential_tot_res_heat():
    """
    Real Name: Percent remaining potential tot RES heat
    Original Eqn: remaining potential tot RES heat*100
    Units: percent
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_heat() * 100


def remaining_potential_tot_res_heat():
    """
    Real Name: remaining potential tot RES heat
    Original Eqn: IF THEN ELSE(max PE potential tot RES heat EJ > PES tot RES for heat , ZIDZ( max PE potential tot RES heat EJ -PES tot RES for heat, max PE potential tot RES heat EJ ), 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_pe_potential_tot_res_heat_ej() > pes_tot_res_for_heat(),
        lambda: zidz(
            max_pe_potential_tot_res_heat_ej() - pes_tot_res_for_heat(),
            max_pe_potential_tot_res_heat_ej(),
        ),
        lambda: 0,
    )


_ext_constant_geot_pe_potential_for_heat_twth = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C56",
    {},
    _root,
    "_ext_constant_geot_pe_potential_for_heat_twth",
)
