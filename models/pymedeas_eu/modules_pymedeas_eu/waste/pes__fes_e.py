"""
Module pes__fes_e
Translated using PySD version 2.2.0
"""


def adapt_growth_waste():
    """
    Real Name: adapt growth waste
    Original Eqn: IF THEN ELSE(Time<2015, Past waste growth, IF THEN ELSE(Time<2020, Past waste growth+(waste change-Past waste growth)*(Time-2015)/5, waste change))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Modeling of a soft transition from current historic annual growth to reach
        the policy-objective 5 years later.
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
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_waste_for_elec_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of waste in elec in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_elec_chp_plants()


def efficiency_waste_for_elec_plants():
    """
    Real Name: efficiency waste for elec plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_waste_for_elec_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of waste in elec plants.
    """
    return _ext_constant_efficiency_waste_for_elec_plants()


def efficiency_waste_for_heat_chp_plants():
    """
    Real Name: efficiency waste for heat CHP plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_waste_for_heat_CHP_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of waste in heat in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_heat_chp_plants()


def efficiency_waste_for_heat_plants():
    """
    Real Name: efficiency waste for heat plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_waste_for_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of waste in heat plants.
    """
    return _ext_constant_efficiency_waste_for_heat_plants()


def fes_elec_from_waste_ej():
    """
    Real Name: FES elec from waste EJ
    Original Eqn: FES elec from waste in CHP plants+FES elec from waste in elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    TFES electricity from waste.
    """
    return fes_elec_from_waste_in_chp_plants() + fes_elec_from_waste_in_elec_plants()


def fes_elec_from_waste_in_chp_plants():
    """
    Real Name: FES elec from waste in CHP plants
    Original Eqn: PES waste for CHP plants*efficiency waste for elec CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of elec in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_elec_chp_plants()


def fes_elec_from_waste_in_elec_plants():
    """
    Real Name: FES elec from waste in elec plants
    Original Eqn: PES waste for elec plants*efficiency waste for elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of electricity in Elec plants from waste.
    """
    return pes_waste_for_elec_plants() * efficiency_waste_for_elec_plants()


def fes_elec_from_waste_twh():
    """
    Real Name: FES elec from waste TWh
    Original Eqn: FES elec from waste EJ/EJ per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    TFES electricity from waste.
    """
    return fes_elec_from_waste_ej() / ej_per_twh()


def fes_heatcom_from_waste_ej():
    """
    Real Name: "FES heat-com from waste EJ"
    Original Eqn: "FES waste for heat-com plants"+"FES heat-com from waste in CHP plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    TFES commercial heat from waste.
    """
    return fes_waste_for_heatcom_plants() + fes_heatcom_from_waste_in_chp_plants()


def fes_heatcom_from_waste_in_chp_plants():
    """
    Real Name: "FES heat-com from waste in CHP plants"
    Original Eqn: PES waste for CHP plants*efficiency waste for heat CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of commercial heat in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_heat_chp_plants()


def fes_waste_for_heatcom_plants():
    """
    Real Name: "FES waste for heat-com plants"
    Original Eqn: "PES waste for heat-com plants"*efficiency waste for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of heat in commercial Heat plants from waste.
    """
    return pes_waste_for_heatcom_plants() * efficiency_waste_for_heat_plants()


def historic_pes_waste_ej(x):
    """
    Real Name: Historic PES waste EJ
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_primary_energy_supply_of_waste')
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic primary energy supply of waste (1990-2014).
    """
    return _ext_lookup_historic_pes_waste_ej(x)


def initial_pes_waste():
    """
    Real Name: initial PES waste
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'initial_primary_energy_supply_from_waste')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Waste primary energy supply in 1995.
    """
    return _ext_constant_initial_pes_waste()


def losses_chp_waste():
    """
    Real Name: Losses CHP waste
    Original Eqn: PES waste for CHP plants-FES elec from waste in CHP plants-"FES heat-com from waste in CHP plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'F52')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Maximun potencial of waste (primary energy supply).
    """
    return _ext_constant_max_pe_waste()


def new_waste_supply_ej():
    """
    Real Name: new waste supply EJ
    Original Eqn: IF THEN ELSE(Time<2014, (Historic PES waste EJ(Time+1)-Historic PES waste EJ(Time)), IF THEN ELSE(max PE waste=0,PES waste EJ*P waste change , ((max PE waste-PES waste EJ)/max PE waste)*adapt growth waste*PES waste EJ))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual waste primary energy supply.
    """
    return if_then_else(
        time() < 2014,
        lambda: (historic_pes_waste_ej(time() + 1) - historic_pes_waste_ej(time())),
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
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'F53')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual PES growth depending on the policy of the scenario.
    """
    return _ext_constant_p_waste_change()


def past_waste_growth():
    """
    Real Name: Past waste growth
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'historic_average_pes_from_waste_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Past growth in PES of waste supply.
    """
    return _ext_constant_past_waste_growth()


def pes_tot_waste_for_elec():
    """
    Real Name: PES tot waste for elec
    Original Eqn: PES waste for elec plants+FES elec from waste in CHP plants+Losses CHP waste*share efficiency waste for elec in CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply for generating electricity from biogas
        (including CHP plants).
    """
    return (
        pes_waste_for_elec_plants()
        + fes_elec_from_waste_in_chp_plants()
        + losses_chp_waste() * share_efficiency_waste_for_elec_in_chp_plants()
    )


def pes_tot_waste_for_heatcom():
    """
    Real Name: "PES tot waste for heat-com"
    Original Eqn: "PES waste for heat-com plants"+"FES heat-com from waste in CHP plants" +Losses CHP waste*(1-share efficiency waste for elec in CHP plants )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply for generating commercial heat from waste
        (including CHP plants).
    """
    return (
        pes_waste_for_heatcom_plants()
        + fes_heatcom_from_waste_in_chp_plants()
        + losses_chp_waste() * (1 - share_efficiency_waste_for_elec_in_chp_plants())
    )


def pes_waste_ej():
    """
    Real Name: PES waste EJ
    Original Eqn: INTEG ( new waste supply EJ, initial PES waste)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Waste primary energy supply (includes industrial and municipal (renew and
        non-renew).
    """
    return _integ_pes_waste_ej()


def pes_waste_for_chp_plants():
    """
    Real Name: PES waste for CHP plants
    Original Eqn: PES waste EJ*share PES waste for CHP
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply waste for CHP plants.
    """
    return pes_waste_ej() * share_pes_waste_for_chp()


def pes_waste_for_elec_plants():
    """
    Real Name: PES waste for elec plants
    Original Eqn: PES waste EJ*share PES waste for elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_elec_plants()


def pes_waste_for_heatcom_plants():
    """
    Real Name: "PES waste for heat-com plants"
    Original Eqn: PES waste EJ*"share PES waste for heat-com plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of commercial heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_heatcom_plants()


def pes_waste_for_tfc():
    """
    Real Name: PES waste for TFC
    Original Eqn: PES waste EJ*share PES waste TFC
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply waste for total final consumption.
    """
    return pes_waste_ej() * share_pes_waste_tfc()


def share_efficiency_waste_for_elec_in_chp_plants():
    """
    Real Name: share efficiency waste for elec in CHP plants
    Original Eqn: efficiency waste for elec CHP plants/(efficiency waste for elec CHP plants+efficiency waste for heat CHP plants)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return efficiency_waste_for_elec_chp_plants() / (
        efficiency_waste_for_elec_chp_plants() + efficiency_waste_for_heat_chp_plants()
    )


def share_pes_waste_for_chp():
    """
    Real Name: share PES waste for CHP
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_pes_waste_for_chp')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES waste for CHP plants.
    """
    return _ext_constant_share_pes_waste_for_chp()


def share_pes_waste_for_elec_plants():
    """
    Real Name: share PES waste for elec plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_pes_waste_for_elec_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES waste for elec plants.
    """
    return _ext_constant_share_pes_waste_for_elec_plants()


def share_pes_waste_for_heatcom_plants():
    """
    Real Name: "share PES waste for heat-com plants"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_pes_waste_for_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES waste for commercial heat plants.
    """
    return _ext_constant_share_pes_waste_for_heatcom_plants()


def share_pes_waste_tfc():
    """
    Real Name: share PES waste TFC
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_pes_waste_tfc')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES waste for total final consumption.
    """
    return _ext_constant_share_pes_waste_tfc()


def waste_change():
    """
    Real Name: waste change
    Original Eqn: IF THEN ELSE(Annual GDP growth rate EU<0, Annual GDP growth rate EU , P waste change)
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    If GDP becomes negative, annual PES change follows it decreasing trends.
    """
    return if_then_else(
        annual_gdp_growth_rate_eu() < 0,
        lambda: annual_gdp_growth_rate_eu(),
        lambda: p_waste_change(),
    )


_ext_constant_efficiency_waste_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_elec_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_elec_chp_plants",
)


_ext_constant_efficiency_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_elec_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_elec_plants",
)


_ext_constant_efficiency_waste_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_heat_CHP_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_heat_chp_plants",
)


_ext_constant_efficiency_waste_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_waste_for_heat_plants",
    {},
    _root,
    "_ext_constant_efficiency_waste_for_heat_plants",
)


_ext_lookup_historic_pes_waste_ej = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_primary_energy_supply_of_waste",
    {},
    _root,
    "_ext_lookup_historic_pes_waste_ej",
)


_ext_constant_initial_pes_waste = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "initial_primary_energy_supply_from_waste",
    {},
    _root,
    "_ext_constant_initial_pes_waste",
)


_ext_constant_max_pe_waste = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "F52",
    {},
    _root,
    "_ext_constant_max_pe_waste",
)


_ext_constant_p_waste_change = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "F53",
    {},
    _root,
    "_ext_constant_p_waste_change",
)


_ext_constant_past_waste_growth = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "historic_average_pes_from_waste_growth",
    {},
    _root,
    "_ext_constant_past_waste_growth",
)


_integ_pes_waste_ej = Integ(
    lambda: new_waste_supply_ej(), lambda: initial_pes_waste(), "_integ_pes_waste_ej"
)


_ext_constant_share_pes_waste_for_chp = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_chp",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_chp",
)


_ext_constant_share_pes_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_elec_plants",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_elec_plants",
)


_ext_constant_share_pes_waste_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_for_heat_plants",
    {},
    _root,
    "_ext_constant_share_pes_waste_for_heatcom_plants",
)


_ext_constant_share_pes_waste_tfc = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_pes_waste_tfc",
    {},
    _root,
    "_ext_constant_share_pes_waste_tfc",
)
