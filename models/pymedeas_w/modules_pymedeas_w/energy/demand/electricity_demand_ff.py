"""
Module electricity_demand_ff
Translated using PySD version 2.2.3
"""


def a_lineal_regr_phaseout_oil_for_elec():
    """
    Real Name: "a lineal regr phase-out oil for elec"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (share_in_target_year_oil_for_elec() - hist_share_oilff_elec()) / (
        target_year_policy_phaseout_oil_for_elec()
        - start_year_policy_phaseout_oil_for_elec()
    )


@subs(["primary sources"], _subscript_dict)
def abundance_primary_sources():
    """
    Real Name: Abundance primary sources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant, Auxiliary
    Subs: ['primary sources']

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    value = xr.DataArray(
        np.nan,
        {"primary sources": _subscript_dict["primary sources"]},
        ["primary sources"],
    )
    value.loc[{"primary sources": ["coal"]}] = abundance_coal()
    value.loc[{"primary sources": ["oil"]}] = abundance_total_oil()
    value.loc[{"primary sources": ["natural gas"]}] = abundance_total_nat_gas()
    value.loc[{"primary sources": ["others"]}] = 1
    return value


def b_lineal_regr_phaseout_oil_for_elec():
    """
    Real Name: "b lineal regr phase-out oil for elec"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (
        share_in_target_year_oil_for_elec()
        - a_lineal_regr_phaseout_oil_for_elec()
        * target_year_policy_phaseout_oil_for_elec()
    )


def decrease_share_gas_for_elec():
    """
    Real Name: decrease share gas for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Decrease in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_coalgas()
        * future_share_gascoalgas_for_elec()
    )


def decrease_share_oil_for_elec():
    """
    Real Name: decrease share oil for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Decrease in future share of oil over (oil+coal+gas) for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_ffoil()
        * future_share_oilff_for_elec()
    )


def demand_elec_gas_and_coal_twh():
    """
    Real Name: demand Elec gas and coal TWh
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The model assigns priority to RES, CHP plants and nuclear generation (depending on the selected nuclear scenario) among the electricity generation.
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of coal gas power centrals. Stable trend between 1971 and 2014 (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_coal_for_electricity()


_ext_constant_efficiency_coal_for_electricity = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_coal_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_coal_for_electricity",
)


def efficiency_gas_for_electricity():
    """
    Real Name: efficiency gas for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Efficiency of the gas power centrals.
    """
    return _integ_efficiency_gas_for_electricity()


_integ_efficiency_gas_for_electricity = Integ(
    lambda: improvement_efficiency_gas_for_electricity(),
    lambda: initial_efficiency_gas_for_electricity() * percent_to_share(),
    "_integ_efficiency_gas_for_electricity",
)


def efficiency_improv_gas_for_electricity():
    """
    Real Name: Efficiency improv gas for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual efficiency improvement in percentage of the gas power centrals for electricity production.
    """
    return _ext_constant_efficiency_improv_gas_for_electricity()


_ext_constant_efficiency_improv_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improv_gas_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_improv_gas_for_electricity",
)


def efficiency_liquids_for_electricity():
    """
    Real Name: efficiency liquids for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of oil in electricity power centrals. Stable trend between 1971 and 2014 (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_liquids_for_electricity()


_ext_constant_efficiency_liquids_for_electricity = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_liquids_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_liquids_for_electricity",
)


def fe_demand_coal_elec_plants_twh():
    """
    Real Name: FE demand coal Elec plants TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy demand of coal for electricity consumption (TWh).
    """
    return share_coal_for_elec() * demand_elec_gas_and_coal_twh()


def fe_demand_gas_elec_plants_twh():
    """
    Real Name: FE demand gas Elec plants TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy demand of natural gas for electricity consumption (TWh).
    """
    return share_gascoal_gas_for_elec() * demand_elec_gas_and_coal_twh()


def fe_demand_oil_elec_plants_twh():
    """
    Real Name: FE demand oil Elec plants TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy demand of oil to produce electricity.
    """
    return share_oil_for_elec() * demand_elec_plants_fossil_fuels_twh()


def fes_elec_fossil_fuel_chp_plants_twh():
    """
    Real Name: FES Elec fossil fuel CHP plants TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final Energy of fossil fuels to produce electricity (TWh) in CHP plants.
    """
    return fes_elec_fossil_fuel_chp_plants_ej() / ej_per_twh()


def future_share_gascoalff_for_elec():
    """
    Real Name: "Future share gas+coal/FF for elec"
    Original Eqn:
    Units: Dnml
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return 1 - future_share_oilff_for_elec()


def future_share_gascoalgas_for_elec():
    """
    Real Name: "Future share gas/(coal+gas) for Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Endogenous future share of gas over coal+gas for electricity generation.
    """
    return _integ_future_share_gascoalgas_for_elec()


_integ_future_share_gascoalgas_for_elec = Integ(
    lambda: increase_share_gas_for_elec() - decrease_share_gas_for_elec(),
    lambda: share_gascoalgas_for_elec_in_2014(),
    "_integ_future_share_gascoalgas_for_elec",
)


def future_share_oilff_for_elec():
    """
    Real Name: "Future share oil/FF for Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Endogenous future share of oil over (oil+coal+gas) for electricity generation.
    """
    return _integ_future_share_oilff_for_elec()


_integ_future_share_oilff_for_elec = Integ(
    lambda: increase_share_oil_for_elec() - decrease_share_oil_for_elec(),
    lambda: share_oilff_for_elec_in_2015(),
    "_integ_future_share_oilff_for_elec",
)


def hist_share_gascoal_gas_elec():
    """
    Real Name: "Hist share gas/(coal +gas) Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []

    Share of natural gas for electricity in relation to the total gas+coal.
    """
    return _ext_data_hist_share_gascoal_gas_elec(time())


_ext_data_hist_share_gascoal_gas_elec = ExtData(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    "_ext_data_hist_share_gascoal_gas_elec",
)


def hist_share_oilff_elec():
    """
    Real Name: "Hist share oil/FF Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []

    Share of oil for electricity (Data extracted from database World Bank: "Electricity production from oil sources (% of total) " / "Electricity production from oil, gas and coal sources (% of total)").
    """
    return _ext_data_hist_share_oilff_elec(time())


_ext_data_hist_share_oilff_elec = ExtData(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_oil_over_total_fossil_electricity",
    "interpolate",
    {},
    _root,
    "_ext_data_hist_share_oilff_elec",
)


def historic_efficiency_gas_for_electricity(x):
    """
    Real Name: Historic efficiency gas for electricity
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historical evolution of efficiency of natural gas power centrals 1995-2013 (IEA Balances).
    """
    return _ext_lookup_historic_efficiency_gas_for_electricity(x)


_ext_lookup_historic_efficiency_gas_for_electricity = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_efficiency_gas_for_electricity",
    {},
    _root,
    "_ext_lookup_historic_efficiency_gas_for_electricity",
)


def improvement_efficiency_gas_for_electricity():
    """
    Real Name: improvement efficiency gas for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual efficiency improvement of the gas power centrals.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_efficiency_gas_for_electricity(time() + 1)
            - historic_efficiency_gas_for_electricity(time())
        )
        * percent_to_share(),
        lambda: efficiency_gas_for_electricity()
        * remaining_efficiency_improv_gas_for_electricity()
        * efficiency_improv_gas_for_electricity(),
    )


@subs(["primary sources"], _subscript_dict)
def increase_in_perception_ps_scarcity():
    """
    Real Name: increase in perception PS scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    Increase in socieconomic perception of primary sources scarcity of each fuel
    """
    return (
        scarcity_primary_sources()
        * sensitivity_to_scarcity()
        * (1 - perception_in_primary_sources_scarcity())
    )


def increase_share_gas_for_elec():
    """
    Real Name: increase share gas for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Increase in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_gascoal()
        * (1 - future_share_gascoalgas_for_elec())
    )


def increase_share_oil_for_elec():
    """
    Real Name: increase share oil for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Increase in future share of oil over (oil+coal+gas) for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_oilff()
        * (1 - future_share_oilff_for_elec())
    )


def initial_efficiency_gas_for_electricity():
    """
    Real Name: initial efficiency gas for electricity
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of gas power centrals in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_efficiency_gas_for_electricity()


_ext_constant_initial_efficiency_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_efficiency_gas_for_electricity",
    {},
    _root,
    "_ext_constant_initial_efficiency_gas_for_electricity",
)


def max_auxiliar_elec():
    """
    Real Name: max auxiliar Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Auxiliarity variable that limit the interchange between fuels to cover electricity.
    """
    return 0.03


def max_efficiency_gas_power_plants():
    """
    Real Name: Max efficiency gas power plants
    Original Eqn:
    Units: Dnml
    Limits: (None, None)
    Type: Constant
    Subs: []

    Assumed maximum efficiency level for gas power centrals.
    """
    return _ext_constant_max_efficiency_gas_power_plants()


_ext_constant_max_efficiency_gas_power_plants = ExtConstant(
    "../energy.xlsx",
    "Global",
    "maximum_efficiency_gas_power_plant",
    {},
    _root,
    "_ext_constant_max_efficiency_gas_power_plants",
)


def p_share_oil_for_elec():
    """
    Real Name: P share oil for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of coal (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_coal_elec_plants_twh() / efficiency_coal_for_electricity()
    ) * ej_per_twh()


def pe_demand_gas_elec_plants_ej():
    """
    Real Name: PE demand gas Elec plants EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of natural gas (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_gas_elec_plants_twh() / efficiency_gas_for_electricity()
    ) * ej_per_twh()


def pe_demand_oil_elec_plants_ej():
    """
    Real Name: PE demand oil Elec plants EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of oil (EJ) for electric generation (including generation losses).
    """
    return (
        fe_demand_oil_elec_plants_twh() / efficiency_liquids_for_electricity()
    ) * ej_per_twh()


def percent_to_share():
    """
    Real Name: percent to share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion of percent to share.
    """
    return 0.01


@subs(["primary sources"], _subscript_dict)
def perception_in_primary_sources_scarcity():
    """
    Real Name: perception in primary sources scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: ['primary sources']

    Perception of primary sources scarcity of each fuel by economic sectors. This perception drives the fuel replacement for electriciy and heat.
    """
    return _integ_perception_in_primary_sources_scarcity()


_integ_perception_in_primary_sources_scarcity = Integ(
    lambda: increase_in_perception_ps_scarcity()
    - reduction_in_perception_ps_scarcity(),
    lambda: xr.DataArray(
        0, {"primary sources": _subscript_dict["primary sources"]}, ["primary sources"]
    ),
    "_integ_perception_in_primary_sources_scarcity",
)


@subs(["primary sources1", "primary sources"], _subscript_dict)
def perception_of_interfuel_primary_sources_scarcity():
    """
    Real Name: "perception of inter-fuel primary sources scarcity"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources1', 'primary sources']

    Perception of primary energy scarcity between fuels. This perception drives the fuel replacement in electricity and heat sectors. TODO
    """
    value = xr.DataArray(
        np.nan,
        {
            "primary sources1": _subscript_dict["primary sources1"],
            "primary sources": _subscript_dict["primary sources"],
        },
        ["primary sources1", "primary sources"],
    )
    value.loc[
        {
            "primary sources1": ["coal"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["coal"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["coal"]),
                1,
            ),
        )
    ).values
    value.loc[
        {
            "primary sources1": ["oil"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["oil"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["oil"]),
                1,
            ),
        )
    ).values
    value.loc[
        {
            "primary sources1": ["natural gas"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["natural gas"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["natural gas"]),
                1,
            ),
        )
    ).values
    value.loc[
        {
            "primary sources1": ["others"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["others"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["others"]),
                1,
            ),
        )
    ).values
    return value


def perception_of_interfuel_ps_scarcity_coalgas():
    """
    Real Name: "perception of inter-fuel PS scarcity coal-gas"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["coal", "oil"])
    )


def perception_of_interfuel_ps_scarcity_ffoil():
    """
    Real Name: "perception of inter-fuel PS scarcity FF-oil"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-fossil fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_coaloil(),
        perception_of_interfuel_ps_scarcity_nat_gasoil(),
    )


def perception_of_interfuel_ps_scarcity_gascoal():
    """
    Real Name: "perception of inter-fuel PS scarcity gas-coal"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["oil", "coal"])
    )


def perception_of_interfuel_ps_scarcity_oilff():
    """
    Real Name: "perception of inter-fuel PS scarcity oil-FF"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-fossil fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_oilcoal(),
        perception_of_interfuel_ps_scarcity_oilnatgas(),
    )


def perception_of_interfuel_ps_scarcity_oilnatgas():
    """
    Real Name: "perception of inter-fuel PS scarcity oil-nat.gas"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Activation of a policies to reduce oil contribution in electricity linearly: If=1: ACTIVATED, If=0: DEACTIVATED.
    """
    return _ext_constant_phaseout_oil_for_electricity()


_ext_constant_phaseout_oil_for_electricity = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "phase_out_oil_electr",
    {},
    _root,
    "_ext_constant_phaseout_oil_for_electricity",
)


@subs(["primary sources"], _subscript_dict)
def reduction_in_perception_ps_scarcity():
    """
    Real Name: reduction in perception PS scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_in_primary_sources_scarcity() / energy_scarcity_forgetting_time()


def remaining_efficiency_improv_gas_for_electricity():
    """
    Real Name: remaining efficiency improv gas for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining efficiency improvement for gas power centrals.
    """
    return (
        max_efficiency_gas_power_plants() - efficiency_gas_for_electricity()
    ) / max_efficiency_gas_power_plants()


@subs(["primary sources"], _subscript_dict)
def scarcity_primary_sources():
    """
    Real Name: scarcity primary sources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_primary_sources()


def share_coal_for_elec():
    """
    Real Name: share coal for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Coal is assumed to cover the rest of the electricity demand after RES, nuclear, oil and gas.
    """
    return 1 - share_gascoal_gas_for_elec()


def share_gascoal_gas_for_elec():
    """
    Real Name: "share gas/(coal +gas) for Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of natural gas for electricity in relation to the total fossil fuels for electricity.
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic data
    """
    return _ext_constant_share_gascoalgas_for_elec_in_2014()


_ext_constant_share_gascoalgas_for_elec_in_2014 = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas_2014",
    {},
    _root,
    "_ext_constant_share_gascoalgas_for_elec_in_2014",
)


def share_in_target_year_oil_for_elec():
    """
    Real Name: share in target year oil for elec
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_share_in_target_year_oil_for_elec()


_ext_constant_share_in_target_year_oil_for_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_target_year_oil_for_elec",
    {},
    _root,
    "_ext_constant_share_in_target_year_oil_for_elec",
)


def share_oil_for_elec():
    """
    Real Name: share oil for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic data
    """
    return _ext_constant_share_oilff_for_elec_in_2015()


_ext_constant_share_oilff_for_elec_in_2015 = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_of_electricity_produced_from_oil_over_total_fossil_electricity_2015",
    {},
    _root,
    "_ext_constant_share_oilff_for_elec_in_2015",
)


def start_year_policy_phaseout_oil_for_elec():
    """
    Real Name: "start year policy phase-out oil for elec"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, start policy phase-out oil for electricity.
    """
    return _ext_constant_start_year_policy_phaseout_oil_for_elec()


_ext_constant_start_year_policy_phaseout_oil_for_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    "_ext_constant_start_year_policy_phaseout_oil_for_elec",
)


def switch_scarcityps_elec_substit():
    """
    Real Name: "switch scarcity-PS elec substit"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    This swith allows the endogenous replacement of primary and final fuels depending on their relative abundance: =1: activated. =0: not activated
    """
    return 1


def target_year_policy_phaseout_oil_for_elec():
    """
    Real Name: "target year policy phase-out oil for elec"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_target_year_policy_phaseout_oil_for_elec()


_ext_constant_target_year_policy_phaseout_oil_for_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "target_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    "_ext_constant_target_year_policy_phaseout_oil_for_elec",
)


def total_gen_losses_demand_for_elec_plants_ej():
    """
    Real Name: Total gen losses demand for Elec plants EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total generation losses associated to electricity demand.
    """
    return (
        pe_demand_gas_elec_plants_ej() * (1 - efficiency_gas_for_electricity())
        + pe_demand_coal_elec_plants_ej() * (1 - efficiency_coal_for_electricity())
        + pe_demand_oil_elec_plants_ej() * (1 - efficiency_liquids_for_electricity())
        + pe_losses_uranium_for_elec_ej()
        + pe_losses_bioe_for_elec_ej()
    )
