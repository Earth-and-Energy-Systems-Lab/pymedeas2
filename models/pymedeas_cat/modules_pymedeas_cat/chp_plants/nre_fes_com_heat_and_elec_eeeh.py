"""
Module nre_fes_com_heat_and_elec_eeeh
Translated using PySD version 2.2.0
"""


def efficiency_elec_coal_chp_plants():
    """
    Real Name: efficiency Elec coal CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_electricity_coal_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of elec in coal CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_coal_chp_plants(time())


def efficiency_elec_gas_chp_plants():
    """
    Real Name: efficiency Elec gas CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_electricity_gas_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of elec in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_gas_chp_plants(time())


def efficiency_elec_oil_chp_plants():
    """
    Real Name: efficiency Elec oil CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_electricity_liquids_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of liquids in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_oil_chp_plants(time())


def efficiency_heat_coal_chp_plants():
    """
    Real Name: efficiency Heat coal CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_heat_coal_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of heat in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_coal_chp_plants(time())


def efficiency_heat_gas_chp_plants():
    """
    Real Name: efficiency Heat gas CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_heat_gas_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of heat in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_gas_chp_plants(time())


def efficiency_heat_oil_chp_plants():
    """
    Real Name: efficiency Heat oil CHP plants
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_efficiency_heat_liquids_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Efficiency of heat in oil CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_oil_chp_plants(time())


def fed_heat_coal_chp_plants_ej():
    """
    Real Name: FED heat coal CHP plants EJ
    Original Eqn: FED heat fossil fuels CHP plants EJ*share CHP plants coal
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of coal to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * share_chp_plants_coal()


def fed_heat_fossil_fuels_chp_plants_ej():
    """
    Real Name: FED heat fossil fuels CHP plants EJ
    Original Eqn: MAX("FED heat-com by NRE CHP plants EJ"-"FES Heat-com nuclear CHP plants EJ",0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of fossil fuels in CHP plants.
    """
    return np.maximum(
        fed_heatcom_by_nre_chp_plants_ej() - fes_heatcom_nuclear_chp_plants_ej(), 0
    )


def fed_heat_gas_chp_plants_ej():
    """
    Real Name: FED heat gas CHP plants EJ
    Original Eqn: FED heat fossil fuels CHP plants EJ*historic share CHP plants gas
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of gas to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * historic_share_chp_plants_gas()


def fed_heat_liquids_chp_plants_ej():
    """
    Real Name: FED heat liquids CHP plants EJ
    Original Eqn: FED heat fossil fuels CHP plants EJ*share CHP plants oil
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of oil to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * share_chp_plants_oil()


def fed_heatcom_by_nre_chp_plants_ej():
    """
    Real Name: "FED heat-com by NRE CHP plants EJ"
    Original Eqn: "Share heat-com CHP plants NRE vs NRE tot heat-com generation"*"FED Heat-com NRE EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of commercial heat in CHP plants without RES.
    """
    return (
        share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation()
        * fed_heatcom_nre_ej()
    )


def fes_elec_fossil_fuel_chp_plants_ej():
    """
    Real Name: FES Elec fossil fuel CHP plants EJ
    Original Eqn: MIN(Potential FE gen Elec fossil fuel CHP plants EJ, Demand Elec NRE TWh *EJ per TWh)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final Energy supply of electricity from fossil fuels in CHP plants. We
        assign priority to it due to its better efficiency.
    """
    return np.minimum(
        potential_fe_gen_elec_fossil_fuel_chp_plants_ej(),
        demand_elec_nre_twh() * ej_per_twh(),
    )


def fes_heatcom_fossil_fuels_chp_plants_ej():
    """
    Real Name: "FES heat-com fossil fuels CHP plants EJ"
    Original Eqn: FED heat fossil fuels CHP plants EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final Energy supply of heat from fossil fuels in CHP plants. We assign
        priority to it due to its better efficiency.
    """
    return fed_heat_fossil_fuels_chp_plants_ej()


def fes_heatcom_nuclear_chp_plants_ej():
    """
    Real Name: "FES Heat-com nuclear CHP plants EJ"
    Original Eqn: MIN("Potential FES Heat-com nuclear CHP plants EJ","FED Heat-com NRE EJ" )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Commercial heat produced in cogeration nuclear plants.
    """
    return np.minimum(
        potential_fes_heatcom_nuclear_chp_plants_ej(), fed_heatcom_nre_ej()
    )


def historic_share_chp_plants_gas():
    """
    Real Name: historic share CHP plants gas
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_chp_plants_gas')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Historic share of natural gas for electricity in relation to the total
        fossil fuels for CHP plants
    """
    return _ext_data_historic_share_chp_plants_gas(time())


def historic_share_chp_plants_oil():
    """
    Real Name: historic share CHP plants oil
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_chp_plants_oil')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    historic share CHP plants oil
    """
    return _ext_data_historic_share_chp_plants_oil(time())


def ped_coal_for_chp_plants_ej():
    """
    Real Name: PED coal for CHP plants EJ
    Original Eqn: FED heat coal CHP plants EJ/efficiency Heat coal CHP plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of coal (EJ) for CHP plants.
    """
    return fed_heat_coal_chp_plants_ej() / efficiency_heat_coal_chp_plants()


def ped_gas_for_chp_plants_ej():
    """
    Real Name: PED gas for CHP plants EJ
    Original Eqn: FED heat gas CHP plants EJ/efficiency Heat gas CHP plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of gas (EJ) for CHP plants.
    """
    return fed_heat_gas_chp_plants_ej() / efficiency_heat_gas_chp_plants()


def ped_oil_for_chp_plants_ej():
    """
    Real Name: PED oil for CHP plants EJ
    Original Eqn: FED heat liquids CHP plants EJ/efficiency Heat oil CHP plants
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of oil (EJ) for CHP plants.
    """
    return fed_heat_liquids_chp_plants_ej() / efficiency_heat_oil_chp_plants()


def potential_fe_gen_elec_coal_chp_plants_ej():
    """
    Real Name: Potential FE gen Elec coal CHP plants EJ
    Original Eqn: PED coal for CHP plants EJ*efficiency Elec coal CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential electricity generation from CHP plants burning coal.
    """
    return ped_coal_for_chp_plants_ej() * efficiency_elec_coal_chp_plants()


def potential_fe_gen_elec_fossil_fuel_chp_plants_ej():
    """
    Real Name: Potential FE gen Elec fossil fuel CHP plants EJ
    Original Eqn: (Potential FE gen Elec coal CHP plants EJ+Potential FE gen Elec gas CHP plants EJ+Potential FE gen Elec liquids CHP plants EJ)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential electricity generation from CHP plants burning fossil fuels.
    """
    return (
        potential_fe_gen_elec_coal_chp_plants_ej()
        + potential_fe_gen_elec_gas_chp_plants_ej()
        + potential_fe_gen_elec_liquids_chp_plants_ej()
    )


def potential_fe_gen_elec_gas_chp_plants_ej():
    """
    Real Name: Potential FE gen Elec gas CHP plants EJ
    Original Eqn: PED gas for CHP plants EJ*efficiency Elec gas CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential electricity generation from CHP plants burning natural gas.
    """
    return ped_gas_for_chp_plants_ej() * efficiency_elec_gas_chp_plants()


def potential_fe_gen_elec_liquids_chp_plants_ej():
    """
    Real Name: Potential FE gen Elec liquids CHP plants EJ
    Original Eqn: PED oil for CHP plants EJ*efficiency Elec oil CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential electricity generation from CHP plants burning oil liquids.
    """
    return ped_oil_for_chp_plants_ej() * efficiency_elec_oil_chp_plants()


def potential_fes_heatcom_nuclear_chp_plants_ej():
    """
    Real Name: "Potential FES Heat-com nuclear CHP plants EJ"
    Original Eqn: FE nuclear Elec generation TWh*share of heat production in CHP plants vs total nucelar elec generation
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential commercial heat to be produced in cogeration nuclear plants.
    """
    return (
        fe_nuclear_elec_generation_twh()
        * share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation()
    )


def share_chp_plants_coal():
    """
    Real Name: share CHP plants coal
    Original Eqn: 1-historic share CHP plants gas-share CHP plants oil
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Coal is assumed to cover the rest of the CHP plants demand after RES,
        nuclear, oil and gas.
    """
    return 1 - historic_share_chp_plants_gas() - share_chp_plants_oil()


def share_chp_plants_oil():
    """
    Real Name: share CHP plants oil
    Original Eqn: MAX(IF THEN ELSE(Time>2014, -0.002985*(Time)+6.04554, historic share CHP plants oil),0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Oil share of heat demand. Since this share has been falling globally since
        the first oil shock, and given the difficulties to substitute oil in other
        sectors (e.g. Transportation) and that there are many more resources that
        can supply heat, we assume an exogenous linear decreasing trend for the
        oil share of heat demand to reach 0% around 2025.
    """
    return np.maximum(
        if_then_else(
            time() > 2014,
            lambda: -0.002985 * (time()) + 6.04554,
            lambda: historic_share_chp_plants_oil(),
        ),
        0,
    )


def share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation():
    """
    Real Name: "Share heat-com CHP plants NRE vs NRE tot heat-com generation"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_commercial_heat_in_chp_on_total_commercial_heat_generation')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Share of commercial heat produced in CHP plants from non-renewable
        energies vs. total commercial heat generation from NRE.
    """
    return _ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation(time())


def share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation():
    """
    Real Name: share of heat production in CHP plants vs total nucelar elec generation
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'share_heat_output_vs_electricity_in_nuclear')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of heat production in CHP plants vs total nucelar elec generation.
    """
    return (
        _ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation()
    )


def total_gen_losses_demand_for_chp_plants_ej():
    """
    Real Name: Total gen losses demand for CHP plants EJ
    Original Eqn: PED gas for CHP plants EJ*(1-efficiency Elec gas CHP plants-efficiency Heat gas CHP plants)+PED oil for CHP plants EJ*(1-efficiency Elec oil CHP plants-efficiency Heat oil CHP plants)+PED coal for CHP plants EJ*(1-efficiency Heat coal CHP plants-efficiency Elec coal CHP plants)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total generation losses associated to CHP plants.
    """
    return (
        ped_gas_for_chp_plants_ej()
        * (1 - efficiency_elec_gas_chp_plants() - efficiency_heat_gas_chp_plants())
        + ped_oil_for_chp_plants_ej()
        * (1 - efficiency_elec_oil_chp_plants() - efficiency_heat_oil_chp_plants())
        + ped_coal_for_chp_plants_ej()
        * (1 - efficiency_heat_coal_chp_plants() - efficiency_elec_coal_chp_plants())
    )


_ext_data_efficiency_elec_coal_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_electricity_coal_chp_plants",
    None,
    {},
    _root,
    "_ext_data_efficiency_elec_coal_chp_plants",
)


_ext_data_efficiency_elec_gas_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_electricity_gas_chp_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_elec_gas_chp_plants",
)


_ext_data_efficiency_elec_oil_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_electricity_liquids_chp_plants",
    None,
    {},
    _root,
    "_ext_data_efficiency_elec_oil_chp_plants",
)


_ext_data_efficiency_heat_coal_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_heat_coal_chp_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_heat_coal_chp_plants",
)


_ext_data_efficiency_heat_gas_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_heat_gas_chp_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_heat_gas_chp_plants",
)


_ext_data_efficiency_heat_oil_chp_plants = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_efficiency_heat_liquids_chp_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_efficiency_heat_oil_chp_plants",
)


_ext_data_historic_share_chp_plants_gas = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_chp_plants_gas",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_share_chp_plants_gas",
)


_ext_data_historic_share_chp_plants_oil = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_chp_plants_oil",
    None,
    {},
    _root,
    "_ext_data_historic_share_chp_plants_oil",
)


_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_commercial_heat_in_chp_on_total_commercial_heat_generation",
    "interpolate",
    {},
    _root,
    "_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation",
)


_ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_heat_output_vs_electricity_in_nuclear",
    {},
    _root,
    "_ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation",
)
