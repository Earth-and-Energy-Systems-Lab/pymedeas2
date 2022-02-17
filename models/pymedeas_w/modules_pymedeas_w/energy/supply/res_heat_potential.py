"""
Module res_heat_potential
Translated using PySD version 2.2.1
"""


def fe_solar_potential_for_heat():
    """
    Real Name: FE solar potential for heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'solar_thermal_pot_FE')
    Units: EJ/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Global solar thermal potential. We assume that the primary energy
        coincides with the final energy. See Technical Report Appendix D.
    """
    return _ext_constant_fe_solar_potential_for_heat()


def geot_pe_potential_for_heat_ej():
    """
    Real Name: Geot PE potential for heat EJ
    Original Eqn: Geot PE potential for heat TWth*EJ per TWh/TWe per TWh
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Geothermal potential (primary energy) for producing heat.
    """
    return geot_pe_potential_for_heat_twth() * ej_per_twh() / twe_per_twh()


def geot_pe_potential_for_heat_twth():
    """
    Real Name: Geot PE potential for heat TWth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'geothermal_PE_pot_heat')
    Units: TWth
    Limits: (None, None)
    Type: constant
    Subs: None

    Geothermal primary energy potential for heat.
    """
    return _ext_constant_geot_pe_potential_for_heat_twth()


@subs(["RES heat"], _subscript_dict)
def max_fe_potential_res_for_heat():
    """
    Real Name: Max FE potential RES for heat
    Original Eqn:
      Max PE potential RES for heat[solar heat]+Efficiency RES heat[solar heat]*0
      Max PE potential RES for heat[geot heat]*Efficiency RES heat[geot heat]
      Max PE potential RES for heat[solid bioE heat]*Efficiency RES heat[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Potential (final energy) for producing heat from renewables.
    """
    return xrmerge(
        rearrange(
            float(max_pe_potential_res_for_heat().loc["solar heat"])
            + float(efficiency_res_heat().loc["solar heat"]) * 0,
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            float(max_pe_potential_res_for_heat().loc["geot heat"])
            * float(efficiency_res_heat().loc["geot heat"]),
            ["RES heat"],
            {"RES heat": ["geot heat"]},
        ),
        rearrange(
            float(max_pe_potential_res_for_heat().loc["solid bioE heat"])
            * float(efficiency_res_heat().loc["solid bioE heat"]),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


def max_pe_potential_biogas_for_heat():
    """
    Real Name: max PE potential biogas for heat
    Original Eqn: max biogas EJ*share PES biogas for heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy potential of biogas for heat taking into account the
        current share.
    """
    return max_biogas_ej() * share_pes_biogas_for_heat()


@subs(["RES heat"], _subscript_dict)
def max_pe_potential_res_for_heat():
    """
    Real Name: Max PE potential RES for heat
    Original Eqn:
      FE solar potential for heat
      Geot PE potential for heat EJ
      available PE potential solid bioE for heat EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Potential (primary energy) for producing heat from renewables.
    """
    return xrmerge(
        rearrange(
            fe_solar_potential_for_heat(), ["RES heat"], {"RES heat": ["solar heat"]}
        ),
        rearrange(
            geot_pe_potential_for_heat_ej(), ["RES heat"], {"RES heat": ["geot heat"]}
        ),
        rearrange(
            available_pe_potential_solid_bioe_for_heat_ej(),
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


def pes_tot_res_for_heat():
    """
    Real Name: PES tot RES for heat
    Original Eqn: SUM("PES RES for heat-com by techn"[RES heat!])+SUM("PES RES for heat-nc by techn"[RES heat!])+"PES tot biogas for heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply for generating commercial and non-commercial
        heat from renewables.
    """
    return (
        sum(pes_res_for_heatcom_by_techn(), dim=("RES heat",))
        + sum(pes_res_for_heatnc_by_techn(), dim=("RES heat",))
        + pes_tot_biogas_for_heatcom()
    )


def remaining_potential_tot_res_heat():
    """
    Real Name: remaining potential tot RES heat
    Original Eqn: IF THEN ELSE(max PE potential tot RES heat EJ > PES tot RES for heat , ZIDZ( max PE potential tot RES heat EJ-PES tot RES for heat , max PE potential tot RES heat EJ ), 0)
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


_ext_constant_fe_solar_potential_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "solar_thermal_pot_FE",
    {},
    _root,
    "_ext_constant_fe_solar_potential_for_heat",
)


_ext_constant_geot_pe_potential_for_heat_twth = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "geothermal_PE_pot_heat",
    {},
    _root,
    "_ext_constant_geot_pe_potential_for_heat_twth",
)
