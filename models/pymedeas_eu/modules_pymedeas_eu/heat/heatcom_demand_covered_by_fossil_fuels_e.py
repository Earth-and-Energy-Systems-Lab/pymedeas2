"""
Module heatcom_demand_covered_by_fossil_fuels_e
Translated using PySD version 2.2.0
"""


def a_lineal_regr_phaseout_oil_for_heat():
    """
    Real Name: "a lineal regr phase-out oil for heat"
    Original Eqn: (share in target year oil for heat-Historic share liquids for heat plants)/("target year policy phase-out oil for heat" -"start year policy phase-out oil for heat")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the share of oil for heat over time.
    """
    return (
        share_in_target_year_oil_for_heat() - historic_share_liquids_for_heat_plants()
    ) / (
        target_year_policy_phaseout_oil_for_heat()
        - start_year_policy_phaseout_oil_for_heat()
    )


def b_lineal_regr_phaseout_oil_for_heat():
    """
    Real Name: "b lineal regr phase-out oil for heat"
    Original Eqn: share in target year oil for heat-"a lineal regr phase-out oil for heat" *"target year policy phase-out oil for heat"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the share of oil for heat over time.
    """
    return (
        share_in_target_year_oil_for_heat()
        - a_lineal_regr_phaseout_oil_for_heat()
        * target_year_policy_phaseout_oil_for_heat()
    )


def efficiency_coal_for_heat_plants():
    """
    Real Name: efficiency coal for heat plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_efficiencies', 'historic_efficiency_coal_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of coal heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_coal_for_heat_plants(time())


def efficiency_gases_for_heat_plants():
    """
    Real Name: efficiency gases for heat plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_efficiencies', 'historic_efficiency_gases_for_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of gas heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_gases_for_heat_plants(time())


def efficiency_liquids_for_heat_plants():
    """
    Real Name: efficiency liquids for heat plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_efficiencies', 'historic_efficiency_liquids_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of liquids heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_liquids_for_heat_plants(time())


def fed_heat_coal_plants_ej():
    """
    Real Name: FED Heat coal plants EJ
    Original Eqn: "FED Heat gas+coal EJ"*"share coal(coal+gas) for heat plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of coal to produce heat.
    """
    return fed_heat_gascoal_ej() * share_coalcoalgas_for_heat_plants()


def fed_heat_gas_plants_ej():
    """
    Real Name: FED Heat gas plants EJ
    Original Eqn: "FED Heat gas+coal EJ"*"share gas/(coal+gas) for heat plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of gas to produce heat.
    """
    return fed_heat_gascoal_ej() * share_gascoalgas_for_heat_plants()


def fed_heat_gascoal_ej():
    """
    Real Name: "FED Heat gas+coal EJ"
    Original Eqn: "FED Heat-com plants fossil fuels EJ"-FED Heat liquids plants EJ
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fed_heatcom_plants_fossil_fuels_ej() - fed_heat_liquids_plants_ej()


def fed_heat_liquids_plants_ej():
    """
    Real Name: FED Heat liquids plants EJ
    Original Eqn: "FED Heat-com plants fossil fuels EJ"*share liquids for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of liquids to produce heat.
    """
    return fed_heatcom_plants_fossil_fuels_ej() * share_liquids_for_heat_plants()


def historic_share_liquids_for_heat_plants():
    """
    Real Name: Historic share liquids for heat plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_share_of_liquids_in_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Historic share liquids for heat plants vs heat production from fossil
        fuels.
    """
    return _ext_data_historic_share_liquids_for_heat_plants(time())


def p_share_oil_for_heat():
    """
    Real Name: P share oil for Heat
    Original Eqn: MAX(0, "a lineal regr phase-out oil for heat"*Time+"b lineal regr phase-out oil for heat")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share oil for heat generation derived from the phase-out policy.
    """
    return np.maximum(
        0,
        a_lineal_regr_phaseout_oil_for_heat() * time()
        + b_lineal_regr_phaseout_oil_for_heat(),
    )


def ped_coal_for_heat_plants_ej():
    """
    Real Name: PED coal for Heat plants EJ
    Original Eqn: FED Heat coal plants EJ/efficiency coal for heat plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of coal (EJ) for heat consumption (including
        generation losses).
    """
    return fed_heat_coal_plants_ej() / efficiency_coal_for_heat_plants()


def ped_gases_for_heat_plants_ej():
    """
    Real Name: PED gases for Heat plants EJ
    Original Eqn: FED Heat gas plants EJ/efficiency gases for heat plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of gas (EJ) for heat consumption (including
        generation losses).
    """
    return fed_heat_gas_plants_ej() / efficiency_gases_for_heat_plants()


def ped_oil_for_heat_plants_ej():
    """
    Real Name: PED oil for Heat plants EJ
    Original Eqn: FED Heat liquids plants EJ/efficiency liquids for heat plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of oil (EJ) for heat consumption (including
        generation losses).
    """
    return fed_heat_liquids_plants_ej() / efficiency_liquids_for_heat_plants()


def phaseout_oil_for_heat():
    """
    Real Name: "phase-out oil for heat?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C168')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Activation of a policies to reduce oil contribution in heat commercial linearly:        If=1: ACTIVATED,        If=0: DEACTIVATED.
    """
    return _ext_constant_phaseout_oil_for_heat()


def share_coalcoalgas_for_heat_plants():
    """
    Real Name: "share coal(coal+gas) for heat plants"
    Original Eqn: 1-"share gas/(coal+gas) for heat plants"
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Coal is assumed to cover the rest of the heat demand after RES, nuclear,
        oil and gas.
    """
    return 1 - share_gascoalgas_for_heat_plants()


def share_gascoalgas_for_heat_plants():
    """
    Real Name: "share gas/(coal+gas) for heat plants"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_share_of_heat_produced_from_gas_over_electricity_produced_coal_and_gas')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Share of natural gas for electricity in relation to the total fossil fuels
        for heat
    """
    return _ext_data_share_gascoalgas_for_heat_plants(time())


def share_in_target_year_oil_for_heat():
    """
    Real Name: share in target year oil for heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'I168')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year for the policy phase-out oil for heat.
    """
    return _ext_constant_share_in_target_year_oil_for_heat()


def share_liquids_for_heat_plants():
    """
    Real Name: share liquids for heat plants
    Original Eqn: IF THEN ELSE(Time<2014, Historic share liquids for heat plants, IF THEN ELSE("phase-out oil for heat?"=0, Historic share liquids for heat plants, IF THEN ELSE(Time<"start year policy phase-out oil for heat", Historic share liquids for heat plants, P share oil for Heat)))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Oil share of heat demand.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_share_liquids_for_heat_plants(),
        lambda: if_then_else(
            phaseout_oil_for_heat() == 0,
            lambda: historic_share_liquids_for_heat_plants(),
            lambda: if_then_else(
                time() < start_year_policy_phaseout_oil_for_heat(),
                lambda: historic_share_liquids_for_heat_plants(),
                lambda: p_share_oil_for_heat(),
            ),
        ),
    )


def start_year_policy_phaseout_oil_for_heat():
    """
    Real Name: "start year policy phase-out oil for heat"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'E168')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, start policy phase-out oil for heat.
    """
    return _ext_constant_start_year_policy_phaseout_oil_for_heat()


def target_year_policy_phaseout_oil_for_heat():
    """
    Real Name: "target year policy phase-out oil for heat"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G168')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year for the policy phase-out oil for heat.
    """
    return _ext_constant_target_year_policy_phaseout_oil_for_heat()


def total_gen_losses_demand_for_heat_plants_ej():
    """
    Real Name: Total gen losses demand for Heat plants EJ
    Original Eqn: PED gases for Heat plants EJ*(1-efficiency gases for heat plants)+PED oil for Heat plants EJ*(1-efficiency liquids for heat plants)+PED coal for Heat plants EJ *(1-efficiency coal for heat plants)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total generation losses associated to heat plants.
    """
    return (
        ped_gases_for_heat_plants_ej() * (1 - efficiency_gases_for_heat_plants())
        + ped_oil_for_heat_plants_ej() * (1 - efficiency_liquids_for_heat_plants())
        + ped_coal_for_heat_plants_ej() * (1 - efficiency_coal_for_heat_plants())
    )


_ext_data_efficiency_coal_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_efficiency_coal_heat_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_coal_for_heat_plants",
)


_ext_data_efficiency_gases_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_efficiency_gases_for_heat_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_gases_for_heat_plants",
)


_ext_data_efficiency_liquids_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_efficiency_liquids_heat_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_liquids_for_heat_plants",
)


_ext_data_historic_share_liquids_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_liquids_in_heat_plants",
    None,
    {},
    _root,
    "_ext_data_historic_share_liquids_for_heat_plants",
)


_ext_constant_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C168",
    {},
    _root,
    "_ext_constant_phaseout_oil_for_heat",
)


_ext_data_share_gascoalgas_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_heat_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    "_ext_data_share_gascoalgas_for_heat_plants",
)


_ext_constant_share_in_target_year_oil_for_heat = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "I168",
    {},
    _root,
    "_ext_constant_share_in_target_year_oil_for_heat",
)


_ext_constant_start_year_policy_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "E168",
    {},
    _root,
    "_ext_constant_start_year_policy_phaseout_oil_for_heat",
)


_ext_constant_target_year_policy_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G168",
    {},
    _root,
    "_ext_constant_target_year_policy_phaseout_oil_for_heat",
)
