"""
Module waste
Translated using PySD version 2.2.1
"""


def adapt_growth_waste():
    """
    Real Name: adapt growth waste
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_waste_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_waste_growth()
            + (waste_change() - past_waste_growth()) * (time() - 2015) / 5,
            lambda: waste_change(),
        ),
    )


def efficiency_waste_for_elec_chp_plants():
    """
    Real Name: efficiency waste for elec CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of waste in elec in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_elec_chp_plants()


_ext_constant_efficiency_waste_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_elec_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_elec_chp_plants",
)


def efficiency_waste_for_elec_plants():
    """
    Real Name: efficiency waste for elec plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of waste in elec plants.
    """
    return _ext_constant_efficiency_waste_for_elec_plants()


_ext_constant_efficiency_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_elec_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_elec_plants",
)


def efficiency_waste_for_heat_chp_plants():
    """
    Real Name: efficiency waste for heat CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of waste in heat in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_heat_chp_plants()


_ext_constant_efficiency_waste_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_heat_CHP_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_heat_chp_plants",
)


def efficiency_waste_for_heat_plants():
    """
    Real Name: efficiency waste for heat plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of waste in heat plants.
    """
    return _ext_constant_efficiency_waste_for_heat_plants()


_ext_constant_efficiency_waste_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_heat_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_heat_plants",
)


def fes_elec_from_waste_ej():
    """
    Real Name: FES elec from waste EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES electricity from waste.
    """
    return fes_elec_from_waste_in_chp_plants() + fes_elec_from_waste_in_elec_plants()


def fes_elec_from_waste_in_chp_plants():
    """
    Real Name: FES elec from waste in CHP plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of elec in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_elec_chp_plants()


def fes_elec_from_waste_in_elec_plants():
    """
    Real Name: FES elec from waste in elec plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of electricity in Elec plants from waste.
    """
    return pes_waste_for_elec_plants() * efficiency_waste_for_elec_plants()


def fes_elec_from_waste_twh():
    """
    Real Name: FES elec from waste TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES electricity from waste.
    """
    return fes_elec_from_waste_ej() / ej_per_twh()


def fes_heatcom_from_waste_ej():
    """
    Real Name: "FES heat-com from waste EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES commercial heat from waste.
    """
    return fes_waste_for_heatcom_plants() + fes_heatcom_from_waste_in_chp_plants()


def fes_heatcom_from_waste_in_chp_plants():
    """
    Real Name: "FES heat-com from waste in CHP plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of commercial heat in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_heat_chp_plants()


def fes_waste_for_heatcom_plants():
    """
    Real Name: "FES waste for heat-com plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of heat in commercial Heat plants from waste.
    """
    return pes_waste_for_heatcom_plants() * efficiency_waste_for_heat_plants()


def historic_pes_waste_ej(x):
    """
    Real Name: Historic PES waste EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic primary energy supply of waste (1990-2014).
    """
    return _ext_lookup_historic_pes_waste_ej(x)


_ext_lookup_historic_pes_waste_ej = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_primary_energy_supply_of_waste",
    {},
    _root,
    "_ext_lookup_historic_pes_waste_ej",
)


def initial_pes_waste():
    """
    Real Name: initial PES waste
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Waste primary energy supply in 1995.
    """
    return _ext_constant_initial_pes_waste()


_ext_constant_initial_pes_waste = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "initial_primary_energy_supply_from_waste",
    {},
    _root,
    "_ext_constant_initial_pes_waste",
)


def losses_chp_waste():
    """
    Real Name: Losses CHP waste
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Losses in waste CHP plants.
    """
    return (
        pes_waste_for_chp_plants()
        - fes_elec_from_waste_in_chp_plants()
        - fes_heatcom_from_waste_in_chp_plants()
    )


def max_pe_waste():
    """
    Real Name: max PE waste
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Maximun potencial of waste (primary energy supply).
    """
    return _ext_constant_max_pe_waste()


_ext_constant_max_pe_waste = ExtConstant(
    "../energy.xlsx", "Europe", "max_PE_waste", {}, _root, "_ext_constant_max_pe_waste"
)


def new_waste_supply_ej():
    """
    Real Name: new waste supply EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New annual waste primary energy supply.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_pes_waste_ej(time() + 1) - historic_pes_waste_ej(time()),
        lambda: if_then_else(
            max_pe_waste() == 0,
            lambda: pes_waste_ej() * p_waste_change(),
            lambda: ((max_pe_waste() - pes_waste_ej()) / max_pe_waste())
            * adapt_growth_waste()
            * pes_waste_ej(),
        ),
    )


def p_waste_change():
    """
    Real Name: P waste change
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual PES growth depending on the policy of the scenario.
    """
    return _ext_constant_p_waste_change()


_ext_constant_p_waste_change = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_waste_growth",
    {},
    _root,
    "_ext_constant_p_waste_change",
)


def past_waste_growth():
    """
    Real Name: Past waste growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Past growth in PES of waste supply.
    """
    return _ext_constant_past_waste_growth()


_ext_constant_past_waste_growth = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "historic_average_pes_from_waste_growth",
    {},
    _root,
    "_ext_constant_past_waste_growth",
)


def pes_tot_waste_for_elec():
    """
    Real Name: PES tot waste for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply for generating electricity from biogas (including CHP plants).
    """
    return (
        pes_waste_for_elec_plants()
        + fes_elec_from_waste_in_chp_plants()
        + losses_chp_waste() * share_efficiency_waste_for_elec_in_chp_plants()
    )


def pes_tot_waste_for_heatcom():
    """
    Real Name: "PES tot waste for heat-com"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply for generating commercial heat from waste (including CHP plants).
    """
    return (
        pes_waste_for_heatcom_plants()
        + fes_heatcom_from_waste_in_chp_plants()
        + losses_chp_waste() * (1 - share_efficiency_waste_for_elec_in_chp_plants())
    )


def pes_waste_ej():
    """
    Real Name: PES waste EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Waste primary energy supply (includes industrial and municipal (renew and non-renew).
    """
    return _integ_pes_waste_ej()


_integ_pes_waste_ej = Integ(
    lambda: new_waste_supply_ej(), lambda: initial_pes_waste(), "_integ_pes_waste_ej"
)


def pes_waste_for_chp_plants():
    """
    Real Name: PES waste for CHP plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply waste for CHP plants.
    """
    return pes_waste_ej() * share_pes_waste_for_chp()


def pes_waste_for_elec_plants():
    """
    Real Name: PES waste for elec plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply of heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_elec_plants()


def pes_waste_for_heatcom_plants():
    """
    Real Name: "PES waste for heat-com plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply of commercial heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_heatcom_plants()


def pes_waste_for_tfc():
    """
    Real Name: PES waste for TFC
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply waste for total final consumption.
    """
    return pes_waste_ej() * share_pes_waste_tfc()


def share_efficiency_waste_for_elec_in_chp_plants():
    """
    Real Name: share efficiency waste for elec in CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return efficiency_waste_for_elec_chp_plants() / (
        efficiency_waste_for_elec_chp_plants() + efficiency_waste_for_heat_chp_plants()
    )


def share_pes_waste_for_chp():
    """
    Real Name: share PES waste for CHP
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES waste for CHP plants.
    """
    return _ext_constant_share_pes_waste_for_chp()


_ext_constant_share_pes_waste_for_chp = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_chp",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_chp",
)


def share_pes_waste_for_elec_plants():
    """
    Real Name: share PES waste for elec plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES waste for elec plants.
    """
    return _ext_constant_share_pes_waste_for_elec_plants()


_ext_constant_share_pes_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_elec_plants",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_elec_plants",
)


def share_pes_waste_for_heatcom_plants():
    """
    Real Name: "share PES waste for heat-com plants"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES waste for commercial heat plants.
    """
    return _ext_constant_share_pes_waste_for_heatcom_plants()


_ext_constant_share_pes_waste_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_heat_plants",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_heatcom_plants",
)


def share_pes_waste_tfc():
    """
    Real Name: share PES waste TFC
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES waste for total final consumption.
    """
    return _ext_constant_share_pes_waste_tfc()


_ext_constant_share_pes_waste_tfc = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_tfc",
    {},
    _root,
    "_ext_constant_share_pes_waste_tfc",
)


def waste_change():
    """
    Real Name: waste change
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If GDP becomes negative, annual PES change follows it decreasing trends.
    """
    return if_then_else(
        annual_gdp_growth_rate_eu() < 0,
        lambda: annual_gdp_growth_rate_eu(),
        lambda: p_waste_change(),
    )
