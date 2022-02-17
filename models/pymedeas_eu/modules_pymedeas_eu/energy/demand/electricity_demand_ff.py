"""
Module electricity_demand_ff
Translated using PySD version 2.2.1
"""


def a_lineal_regr_phaseout_oil_for_elec():
    """
    Real Name: "a lineal regr phase-out oil for elec"
    Original Eqn: (share in target year oil for elec-"Hist share oil/FF Elec")/("target year policy phase-out oil for elec"-"start year policy phase-out oil for elec")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the share of oil for electricity over time.
    """
    return (share_in_target_year_oil_for_elec() - hist_share_oilff_elec()) / (
        target_year_policy_phaseout_oil_for_elec()
        - start_year_policy_phaseout_oil_for_elec()
    )


def b_lineal_regr_phaseout_oil_for_elec():
    """
    Real Name: "b lineal regr phase-out oil for elec"
    Original Eqn: share in target year oil for elec-"a lineal regr phase-out oil for elec" *"target year policy phase-out oil for elec"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the share of oil for electricity over time.
    """
    return (
        share_in_target_year_oil_for_elec()
        - a_lineal_regr_phaseout_oil_for_elec()
        * target_year_policy_phaseout_oil_for_elec()
    )


def decrease_share_gas_for_elec():
    """
    Real Name: decrease share gas for Elec
    Original Eqn: max auxiliar Elec*"perception of inter-fuel PS scarcity coal-gas"*("Future share gas/(coal+gas) for Elec")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Decrease in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_coalgas()
        * (future_share_gascoalgas_for_elec())
    )


def decrease_share_oil_for_elec():
    """
    Real Name: decrease share oil for Elec
    Original Eqn: max auxiliar Elec*"perception of inter-fuel PS scarcity FF-oil"*("Future share oil/FF for Elec")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Decrease in future share of oil over (oil+coal+gas) for electricity
        generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_ffoil()
        * (future_share_oilff_for_elec())
    )


def demand_elec_gas_and_coal_twh():
    """
    Real Name: demand Elec gas and coal TWh
    Original Eqn: IF THEN ELSE("switch scarcity-PS elec substit"=0, demand Elec plants fossil fuels TWh*(1-"Hist share oil/FF Elec" ), IF THEN ELSE(Time<2016, demand Elec plants fossil fuels TWh*(1-"Hist share oil/FF Elec"), demand Elec plants fossil fuels TWh *"Future share gas+coal/FF for elec"))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        switch_scarcityps_elec_substit() == 0,
        lambda: demand_elec_plants_fossil_fuels_twh() * (1 - hist_share_oilff_elec()),
        lambda: if_then_else(
            time() < 2016,
            lambda: demand_elec_plants_fossil_fuels_twh()
            * (1 - hist_share_oilff_elec()),
            lambda: demand_elec_plants_fossil_fuels_twh()
            * future_share_gascoalff_for_elec(),
        ),
    )


def demand_elec_plants_fossil_fuels_twh():
    """
    Real Name: demand Elec plants fossil fuels TWh
    Original Eqn: MAX(Demand Elec NRE TWh-FE nuclear Elec generation TWh-FES Elec fossil fuel CHP plants TWh , 0)
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    The model assigns priority to RES, CHP plants and nuclear generation
        (depending on the selected nuclear scenario) among the electricity
        generation.
    """
    return np.maximum(
        demand_elec_nre_twh()
        - fe_nuclear_elec_generation_twh()
        - fes_elec_fossil_fuel_chp_plants_twh(),
        0,
    )


def efficiency_coal_for_electricity():
    """
    Real Name: efficiency coal for electricity
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_coal_for_electricity')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of coal gas power centrals. Stable trend between 1971 and 2014
        (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_coal_for_electricity()


def efficiency_gas_for_electricity():
    """
    Real Name: efficiency gas for electricity
    Original Eqn: INTEG ( improvement efficiency gas for electricity, initial efficiency gas for electricity*percent to share)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Efficiency of the gas power centrals.
    """
    return _integ_efficiency_gas_for_electricity()


def efficiency_improv_gas_for_electricity():
    """
    Real Name: Efficiency improv gas for electricity
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_improv_gas_for_electricity')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual efficiency improvement in percentage of the gas power centrals for
        electricity production.
    """
    return _ext_constant_efficiency_improv_gas_for_electricity()


def efficiency_liquids_for_electricity():
    """
    Real Name: efficiency liquids for electricity
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'efficiency_liquids_for_electricity')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of oil in electricity power centrals. Stable trend between 1971
        and 2014 (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_liquids_for_electricity()


def fe_demand_coal_elec_plants_twh():
    """
    Real Name: FE demand coal Elec plants TWh
    Original Eqn: share coal for Elec*demand Elec gas and coal TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of coal for electricity consumption (TWh).
    """
    return share_coal_for_elec() * demand_elec_gas_and_coal_twh()


def fe_demand_gas_elec_plants_twh():
    """
    Real Name: FE demand gas Elec plants TWh
    Original Eqn: "share gas/(coal +gas) for Elec"*demand Elec gas and coal TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of natural gas for electricity consumption (TWh).
    """
    return share_gascoal_gas_for_elec() * demand_elec_gas_and_coal_twh()


def fe_demand_oil_elec_plants_twh():
    """
    Real Name: FE demand oil Elec plants TWh
    Original Eqn: share oil for Elec*demand Elec plants fossil fuels TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of oil to produce electricity.
    """
    return share_oil_for_elec() * demand_elec_plants_fossil_fuels_twh()


def fes_elec_fossil_fuel_chp_plants_twh():
    """
    Real Name: FES Elec fossil fuel CHP plants TWh
    Original Eqn: FES Elec fossil fuel CHP plants EJ/EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final Energy of fossil fuels to produce electricity (TWh) in CHP plants.
    """
    return fes_elec_fossil_fuel_chp_plants_ej() / ej_per_twh()


def future_share_gascoalff_for_elec():
    """
    Real Name: "Future share gas+coal/FF for elec"
    Original Eqn: 1-"Future share oil/FF for Elec"
    Units: Dnml
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - future_share_oilff_for_elec()


def future_share_gascoalgas_for_elec():
    """
    Real Name: "Future share gas/(coal+gas) for Elec"
    Original Eqn: INTEG ( increase share gas for Elec-decrease share gas for Elec, "share gas/(coal+gas) for Elec in 2014")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Endogenous future share of gas over coal+gas for electricity generation.
    """
    return _integ_future_share_gascoalgas_for_elec()


def future_share_oilff_for_elec():
    """
    Real Name: "Future share oil/FF for Elec"
    Original Eqn: INTEG ( increase share oil for Elec-decrease share oil for Elec, "share oil/FF for Elec in 2015")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Endogenous future share of oil over (oil+coal+gas) for electricity
        generation.
    """
    return _integ_future_share_oilff_for_elec()


def hist_share_gascoal_gas_elec():
    """
    Real Name: "Hist share gas/(coal +gas) Elec"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Share of natural gas for electricity in relation to the total gas+coal.
    """
    return _ext_data_hist_share_gascoal_gas_elec(time())


def hist_share_oilff_elec():
    """
    Real Name: "Hist share oil/FF Elec"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_share_of_electricity_produced_from_oil_over_total_fossil_electricity')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Historica share of oil for electricity vs total electricity generation
        from fossil fuels.
    """
    return _ext_data_hist_share_oilff_elec(time())


def historic_efficiency_gas_for_electricity(x):
    """
    Real Name: Historic efficiency gas for electricity
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Europe', 'time_efficiencies', 'historic_efficiency_gas_for_electricity'))
    Units: percent
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historical evolution of efficiency of natural gas power centrals 1995-2013
        (IEA Balances).
    """
    return _ext_lookup_historic_efficiency_gas_for_electricity(x)


def improvement_efficiency_gas_for_electricity():
    """
    Real Name: improvement efficiency gas for electricity
    Original Eqn: IF THEN ELSE(Time<2013, (Historic efficiency gas for electricity(INTEGER(Time+1))-Historic efficiency gas for electricity(INTEGER(Time)))*percent to share, efficiency gas for electricity*remaining efficiency improv gas for electricity*Efficiency improv gas for electricity)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual efficiency improvement of the gas power centrals.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_efficiency_gas_for_electricity(integer(time() + 1))
            - historic_efficiency_gas_for_electricity(integer(time()))
        )
        * percent_to_share(),
        lambda: efficiency_gas_for_electricity()
        * remaining_efficiency_improv_gas_for_electricity()
        * efficiency_improv_gas_for_electricity(),
    )


def increase_share_gas_for_elec():
    """
    Real Name: increase share gas for Elec
    Original Eqn: max auxiliar Elec*"perception of inter-fuel PS scarcity gas-coal"*((1-"Future share gas/(coal+gas) for Elec"))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Increase in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_gascoal()
        * ((1 - future_share_gascoalgas_for_elec()))
    )


def increase_share_oil_for_elec():
    """
    Real Name: increase share oil for Elec
    Original Eqn: max auxiliar Elec*"perception of inter-fuel PS scarcity oil-FF"*((1-"Future share oil/FF for Elec"))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Increase in future share of oil over (oil+coal+gas) for electricity
        generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_oilff()
        * ((1 - future_share_oilff_for_elec()))
    )


def initial_efficiency_gas_for_electricity():
    """
    Real Name: initial efficiency gas for electricity
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'initial_efficiency_gas_for_electricity')
    Units: percent
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of gas power centrals in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_efficiency_gas_for_electricity()


def max_auxiliar_elec():
    """
    Real Name: max auxiliar Elec
    Original Eqn: 0.03
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Auxiliarity variable that limit the interchange between fuels to cover
        electricity.
    """
    return 0.03


def max_efficiency_gas_power_plants():
    """
    Real Name: Max efficiency gas power plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'maximum_efficiency_gas_power_plant')
    Units: Dnml
    Limits: (None, None)
    Type: constant
    Subs: None

    Assumed maximum efficiency level for gas power centrals.
    """
    return _ext_constant_max_efficiency_gas_power_plants()


def p_share_oil_for_elec():
    """
    Real Name: P share oil for Elec
    Original Eqn: MAX(0, "a lineal regr phase-out oil for elec"*Time+"b lineal regr phase-out oil for elec")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share oil for electricity generation derived from the phase-out policy.
    """
    return np.maximum(
        0,
        a_lineal_regr_phaseout_oil_for_elec() * time()
        + b_lineal_regr_phaseout_oil_for_elec(),
    )


def pe_demand_coal_elec_plants_ej():
    """
    Real Name: PE demand coal Elec plants EJ
    Original Eqn: (FE demand coal Elec plants TWh/efficiency coal for electricity)*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of coal (EJ) for electricity consumption (including
        generation losses).
    """
    return (
        fe_demand_coal_elec_plants_twh() / efficiency_coal_for_electricity()
    ) * ej_per_twh()


def pe_demand_gas_elec_plants_ej():
    """
    Real Name: PE demand gas Elec plants EJ
    Original Eqn: (FE demand gas Elec plants TWh/efficiency gas for electricity)*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of natural gas (EJ) for electricity consumption
        (including generation losses).
    """
    return (
        fe_demand_gas_elec_plants_twh() / efficiency_gas_for_electricity()
    ) * ej_per_twh()


def pe_demand_oil_elec_plants_ej():
    """
    Real Name: PE demand oil Elec plants EJ
    Original Eqn: (FE demand oil Elec plants TWh/efficiency liquids for electricity )*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of oil (EJ) for electric generation (including
        generation losses).
    """
    return (
        fe_demand_oil_elec_plants_twh() / efficiency_liquids_for_electricity()
    ) * ej_per_twh()


def percent_to_share():
    """
    Real Name: percent to share
    Original Eqn: 0.01
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion of percent to share.
    """
    return 0.01


def perception_of_interfuel_ps_scarcity_coalgas():
    """
    Real Name: "perception of inter-fuel PS scarcity coal-gas"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[coal,natural gas])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (gas-coal)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc[
                "coal", "natural gas"
            ]
        ),
    )


def perception_of_interfuel_ps_scarcity_coaloil():
    """
    Real Name: "perception of inter-fuel PS scarcity coal-oil"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[coal,oil])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["coal", "oil"])
    )


def perception_of_interfuel_ps_scarcity_ffoil():
    """
    Real Name: "perception of inter-fuel PS scarcity FF-oil"
    Original Eqn: MAX("perception of inter-fuel PS scarcity coal-oil","perception of inter-fuel PS scarcity nat. gas-oil")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (oil-fossil
        fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_coaloil(),
        perception_of_interfuel_ps_scarcity_nat_gasoil(),
    )


def perception_of_interfuel_ps_scarcity_gascoal():
    """
    Real Name: "perception of inter-fuel PS scarcity gas-coal"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[natural gas,coal])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (gas-coal)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc[
                "natural gas", "coal"
            ]
        ),
    )


def perception_of_interfuel_ps_scarcity_nat_gasoil():
    """
    Real Name: "perception of inter-fuel PS scarcity nat. gas-oil"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[natural gas,oil])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels
        (oil-natural gas)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc["natural gas", "oil"]
        ),
    )


def perception_of_interfuel_ps_scarcity_oilcoal():
    """
    Real Name: "perception of inter-fuel PS scarcity oil-coal"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[oil,coal])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["oil", "coal"])
    )


def perception_of_interfuel_ps_scarcity_oilff():
    """
    Real Name: "perception of inter-fuel PS scarcity oil-FF"
    Original Eqn: MAX("perception of inter-fuel PS scarcity oil-coal","perception of inter-fuel PS scarcity oil-nat.gas")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels (oil-fossil
        fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_oilcoal(),
        perception_of_interfuel_ps_scarcity_oilnatgas(),
    )


def perception_of_interfuel_ps_scarcity_oilnatgas():
    """
    Real Name: "perception of inter-fuel PS scarcity oil-nat.gas"
    Original Eqn: MAX(0,"perception of inter-fuel primary sources scarcity"[oil,natural gas])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Socieconomic perception of final energy scarcity between fuels
        (oil-natural gas)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc["oil", "natural gas"]
        ),
    )


def phaseout_oil_for_electricity():
    """
    Real Name: "phase-out oil for electricity?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'phase_out_oil_electr')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Activation of a policies to reduce oil contribution in electricity linearly:        If=1: ACTIVATED,        If=0: DEACTIVATED.
    """
    return _ext_constant_phaseout_oil_for_electricity()


def remaining_efficiency_improv_gas_for_electricity():
    """
    Real Name: remaining efficiency improv gas for electricity
    Original Eqn: (Max efficiency gas power plants-efficiency gas for electricity)/Max efficiency gas power plants
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining efficiency improvement for gas power centrals.
    """
    return (
        max_efficiency_gas_power_plants() - efficiency_gas_for_electricity()
    ) / max_efficiency_gas_power_plants()


def share_coal_for_elec():
    """
    Real Name: share coal for Elec
    Original Eqn: 1-"share gas/(coal +gas) for Elec"
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Coal is assumed to cover the rest of the electricity demand after RES,
        nuclear, oil and gas.
    """
    return 1 - share_gascoal_gas_for_elec()


def share_gascoal_gas_for_elec():
    """
    Real Name: "share gas/(coal +gas) for Elec"
    Original Eqn: IF THEN ELSE("switch scarcity-PS elec substit"=0, "Hist share gas/(coal +gas) Elec", IF THEN ELSE(Time>2014, "Future share gas/(coal+gas) for Elec","Hist share gas/(coal +gas) Elec"))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas for electricity in relation to the total fossil fuels
        for electricity.
    """
    return if_then_else(
        switch_scarcityps_elec_substit() == 0,
        lambda: hist_share_gascoal_gas_elec(),
        lambda: if_then_else(
            time() > 2014,
            lambda: future_share_gascoalgas_for_elec(),
            lambda: hist_share_gascoal_gas_elec(),
        ),
    )


def share_gascoalgas_for_elec_in_2014():
    """
    Real Name: "share gas/(coal+gas) for Elec in 2014"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas_2014')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Historic data
    """
    return _ext_constant_share_gascoalgas_for_elec_in_2014()


def share_in_target_year_oil_for_elec():
    """
    Real Name: share in target year oil for elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'share_target_year_oil_for_elec')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_share_in_target_year_oil_for_elec()


def share_oil_for_elec():
    """
    Real Name: share oil for Elec
    Original Eqn: IF THEN ELSE("switch scarcity-PS elec substit"=0, "Hist share oil/FF Elec", IF THEN ELSE(Time<2016, "Hist share oil/FF Elec", IF THEN ELSE("phase-out oil for electricity?"=0, "Future share oil/FF for Elec", IF THEN ELSE(Time<"start year policy phase-out oil for elec", "Hist share oil/FF Elec", P share oil for Elec ))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Oil share of electricity demand.
    """
    return if_then_else(
        switch_scarcityps_elec_substit() == 0,
        lambda: hist_share_oilff_elec(),
        lambda: if_then_else(
            time() < 2016,
            lambda: hist_share_oilff_elec(),
            lambda: if_then_else(
                phaseout_oil_for_electricity() == 0,
                lambda: future_share_oilff_for_elec(),
                lambda: if_then_else(
                    time() < start_year_policy_phaseout_oil_for_elec(),
                    lambda: hist_share_oilff_elec(),
                    lambda: p_share_oil_for_elec(),
                ),
            ),
        ),
    )


def share_oilff_for_elec_in_2015():
    """
    Real Name: "share oil/FF for Elec in 2015"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_of_electricity_produced_from_oil_over_total_fossil_electricity_2015')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Historic data
    """
    return _ext_constant_share_oilff_for_elec_in_2015()


def start_year_policy_phaseout_oil_for_elec():
    """
    Real Name: "start year policy phase-out oil for elec"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_policy_phase_out_oil_for_electricity')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, start policy phase-out oil for electricity.
    """
    return _ext_constant_start_year_policy_phaseout_oil_for_elec()


def switch_scarcityps_elec_substit():
    """
    Real Name: "switch scarcity-PS elec substit"
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    This swith allows the endogenous replacement of primary and final fuels depending on
        their relative abundance:        =1: activated.        =0: not activated
    """
    return 1


def target_year_policy_phaseout_oil_for_elec():
    """
    Real Name: "target year policy phase-out oil for elec"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'target_year_policy_phase_out_oil_electricity')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_target_year_policy_phaseout_oil_for_elec()


def total_gen_losses_demand_for_elec_plants_ej():
    """
    Real Name: Total gen losses demand for Elec plants EJ
    Original Eqn: PE demand gas Elec plants EJ*(1-efficiency gas for electricity)+PE demand coal Elec plants EJ*(1-efficiency coal for electricity)+PE demand oil Elec plants EJ *(1-efficiency liquids for electricity)+PE losses uranium for Elec EJ+PE losses BioE for Elec EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total generation losses associated to electricity demand.
    """
    return (
        pe_demand_gas_elec_plants_ej() * (1 - efficiency_gas_for_electricity())
        + pe_demand_coal_elec_plants_ej() * (1 - efficiency_coal_for_electricity())
        + pe_demand_oil_elec_plants_ej() * (1 - efficiency_liquids_for_electricity())
        + pe_losses_uranium_for_elec_ej()
        + pe_losses_bioe_for_elec_ej()
    )


_ext_constant_efficiency_coal_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_coal_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_coal_for_electricity",
)


_integ_efficiency_gas_for_electricity = Integ(
    lambda: improvement_efficiency_gas_for_electricity(),
    lambda: initial_efficiency_gas_for_electricity() * percent_to_share(),
    "_integ_efficiency_gas_for_electricity",
)


_ext_constant_efficiency_improv_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improv_gas_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_improv_gas_for_electricity",
)


_ext_constant_efficiency_liquids_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "efficiency_liquids_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_liquids_for_electricity",
)


_integ_future_share_gascoalgas_for_elec = Integ(
    lambda: increase_share_gas_for_elec() - decrease_share_gas_for_elec(),
    lambda: share_gascoalgas_for_elec_in_2014(),
    "_integ_future_share_gascoalgas_for_elec",
)


_integ_future_share_oilff_for_elec = Integ(
    lambda: increase_share_oil_for_elec() - decrease_share_oil_for_elec(),
    lambda: share_oilff_for_elec_in_2015(),
    "_integ_future_share_oilff_for_elec",
)


_ext_data_hist_share_gascoal_gas_elec = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    "_ext_data_hist_share_gascoal_gas_elec",
)


_ext_data_hist_share_oilff_elec = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_oil_over_total_fossil_electricity",
    "interpolate",
    {},
    _root,
    "_ext_data_hist_share_oilff_elec",
)


_ext_lookup_historic_efficiency_gas_for_electricity = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_efficiency_gas_for_electricity",
    {},
    _root,
    "_ext_lookup_historic_efficiency_gas_for_electricity",
)


_ext_constant_initial_efficiency_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "initial_efficiency_gas_for_electricity",
    {},
    _root,
    "_ext_constant_initial_efficiency_gas_for_electricity",
)


_ext_constant_max_efficiency_gas_power_plants = ExtConstant(
    "../energy.xlsx",
    "Global",
    "maximum_efficiency_gas_power_plant",
    {},
    _root,
    "_ext_constant_max_efficiency_gas_power_plants",
)


_ext_constant_phaseout_oil_for_electricity = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "phase_out_oil_electr",
    {},
    _root,
    "_ext_constant_phaseout_oil_for_electricity",
)


_ext_constant_share_gascoalgas_for_elec_in_2014 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas_2014",
    {},
    _root,
    "_ext_constant_share_gascoalgas_for_elec_in_2014",
)


_ext_constant_share_in_target_year_oil_for_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_target_year_oil_for_elec",
    {},
    _root,
    "_ext_constant_share_in_target_year_oil_for_elec",
)


_ext_constant_share_oilff_for_elec_in_2015 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_of_electricity_produced_from_oil_over_total_fossil_electricity_2015",
    {},
    _root,
    "_ext_constant_share_oilff_for_elec_in_2015",
)


_ext_constant_start_year_policy_phaseout_oil_for_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    "_ext_constant_start_year_policy_phaseout_oil_for_elec",
)


_ext_constant_target_year_policy_phaseout_oil_for_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_policy_phase_out_oil_electricity",
    {},
    _root,
    "_ext_constant_target_year_policy_phaseout_oil_for_elec",
)
