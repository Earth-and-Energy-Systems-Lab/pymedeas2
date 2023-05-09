"""
Module energy.demand.electricity_demand_ff
Translated using PySD version 3.10.0
"""


@component.add(
    name='"a lineal regr phase-out oil for elec"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_ff_for_elec": 1,
        "hist_share_oilff_elec": 1,
        "target_year_policy_phaseout_ff_for_elec": 1,
        "start_year_policy_phaseout_oil_for_elec": 1,
    },
)
def a_lineal_regr_phaseout_oil_for_elec():
    """
    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (share_in_target_year_ff_for_elec() - hist_share_oilff_elec()) / (
        target_year_policy_phaseout_ff_for_elec()
        - start_year_policy_phaseout_oil_for_elec()
    )


@component.add(
    name='"b lineal regr phase-out FF for elec"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_ff_for_elec": 1,
        "a_lineal_regr_phaseout_oil_for_elec": 1,
        "target_year_policy_phaseout_ff_for_elec": 1,
    },
)
def b_lineal_regr_phaseout_ff_for_elec():
    """
    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (
        share_in_target_year_ff_for_elec()
        - a_lineal_regr_phaseout_oil_for_elec()
        * target_year_policy_phaseout_ff_for_elec()
    )


@component.add(
    name="decrease share gas for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_auxiliar_elec": 1,
        "perception_of_interfuel_ps_scarcity_coalgas": 1,
        "future_share_gascoalgas_for_elec": 1,
    },
)
def decrease_share_gas_for_elec():
    """
    Decrease in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_coalgas()
        * future_share_gascoalgas_for_elec()
    )


@component.add(
    name="decrease share oil for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_auxiliar_elec": 1,
        "perception_of_interfuel_ps_scarcity_ffoil": 1,
        "future_share_oilff_for_elec": 1,
    },
)
def decrease_share_oil_for_elec():
    """
    Decrease in future share of oil over (oil+coal+gas) for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_ffoil()
        * future_share_oilff_for_elec()
    )


@component.add(
    name="demand Elec gas and coal TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_scarcityps_elec_substit": 1,
        "share_oil_for_elec": 2,
        "demand_elec_plants_fossil_fuels_twh": 3,
        "time": 1,
        "future_share_gascoalff_for_elec": 1,
    },
)
def demand_elec_gas_and_coal_twh():
    return if_then_else(
        switch_scarcityps_elec_substit() == 0,
        lambda: demand_elec_plants_fossil_fuels_twh() * (1 - share_oil_for_elec()),
        lambda: if_then_else(
            time() < 2016,
            lambda: demand_elec_plants_fossil_fuels_twh() * (1 - share_oil_for_elec()),
            lambda: demand_elec_plants_fossil_fuels_twh()
            * future_share_gascoalff_for_elec(),
        ),
    )


@component.add(
    name="demand Elec plants fossil fuels TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_elec_nre_twh": 1,
        "fe_nuclear_elec_generation_twh": 1,
        "fes_elec_fossil_fuel_chp_plants_twh": 1,
    },
)
def demand_elec_plants_fossil_fuels_twh():
    """
    The model assigns priority to RES, CHP plants and nuclear generation (depending on the selected nuclear scenario) among the electricity generation.
    """
    return np.maximum(
        demand_elec_nre_twh()
        - fe_nuclear_elec_generation_twh()
        - fes_elec_fossil_fuel_chp_plants_twh(),
        0,
    )


@component.add(
    name="efficiency coal for electricity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_coal_for_electricity"},
)
def efficiency_coal_for_electricity():
    """
    Efficiency of coal gas power centrals. Stable trend between 1971 and 2014 (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_coal_for_electricity()


_ext_constant_efficiency_coal_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "efficiency_coal_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_coal_for_electricity",
)


@component.add(
    name="efficiency gas for electricity",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_efficiency_gas_for_electricity": 1},
    other_deps={
        "_integ_efficiency_gas_for_electricity": {
            "initial": {
                "initial_efficiency_gas_for_electricity": 1,
                "percent_to_share": 1,
            },
            "step": {"improvement_efficiency_gas_for_electricity": 1},
        }
    },
)
def efficiency_gas_for_electricity():
    """
    Efficiency of the gas power centrals.
    """
    return _integ_efficiency_gas_for_electricity()


_integ_efficiency_gas_for_electricity = Integ(
    lambda: improvement_efficiency_gas_for_electricity(),
    lambda: initial_efficiency_gas_for_electricity() * percent_to_share(),
    "_integ_efficiency_gas_for_electricity",
)


@component.add(
    name="Efficiency improv gas for electricity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_improv_gas_for_electricity"},
)
def efficiency_improv_gas_for_electricity():
    """
    Annual efficiency improvement in percentage of the gas power centrals for electricity production.
    """
    return _ext_constant_efficiency_improv_gas_for_electricity()


_ext_constant_efficiency_improv_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improv_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_improv_gas_for_electricity",
)


@component.add(
    name="efficiency liquids for electricity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_liquids_for_electricity"},
)
def efficiency_liquids_for_electricity():
    """
    Efficiency of oil in electricity power centrals. Stable trend between 1971 and 2014 (IEA Balances), average of the period.
    """
    return _ext_constant_efficiency_liquids_for_electricity()


_ext_constant_efficiency_liquids_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "efficiency_liquids_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_liquids_for_electricity",
)


@component.add(
    name="FE demand coal Elec plants TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_coal_for_elec": 1, "demand_elec_gas_and_coal_twh": 1},
)
def fe_demand_coal_elec_plants_twh():
    """
    Final energy demand of coal for electricity consumption (TWh).
    """
    return share_coal_for_elec() * demand_elec_gas_and_coal_twh()


@component.add(
    name="FE demand gas Elec plants TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_gascoal_gas_for_elec": 1, "demand_elec_gas_and_coal_twh": 1},
)
def fe_demand_gas_elec_plants_twh():
    """
    Final energy demand of natural gas for electricity consumption (TWh).
    """
    return share_gascoal_gas_for_elec() * demand_elec_gas_and_coal_twh()


@component.add(
    name="FE demand oil Elec plants TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_oil_for_elec": 1, "demand_elec_plants_fossil_fuels_twh": 1},
)
def fe_demand_oil_elec_plants_twh():
    """
    Final energy demand of oil to produce electricity.
    """
    return share_oil_for_elec() * demand_elec_plants_fossil_fuels_twh()


@component.add(
    name="FES Elec fossil fuel CHP plants TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_elec_fossil_fuel_chp_plants_ej": 1, "ej_per_twh": 1},
)
def fes_elec_fossil_fuel_chp_plants_twh():
    """
    Final Energy of fossil fuels to produce electricity (TWh) in CHP plants.
    """
    return (
        sum(
            fes_elec_fossil_fuel_chp_plants_ej().rename(
                {"fossil fuels": "fossil fuels!"}
            ),
            dim=["fossil fuels!"],
        )
        / ej_per_twh()
    )


@component.add(
    name='"Future share gas+coal/FF for elec"',
    units="Dnml",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_oil_for_elec": 1},
)
def future_share_gascoalff_for_elec():
    return 1 - share_oil_for_elec()


@component.add(
    name='"Future share gas/(coal+gas) for Elec"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_future_share_gascoalgas_for_elec": 1},
    other_deps={
        "_integ_future_share_gascoalgas_for_elec": {
            "initial": {"share_gascoalgas_for_elec_in_2014": 1},
            "step": {
                "increase_share_gas_for_elec": 1,
                "decrease_share_gas_for_elec": 1,
            },
        }
    },
)
def future_share_gascoalgas_for_elec():
    """
    Endogenous future share of gas over coal+gas for electricity generation.
    """
    return _integ_future_share_gascoalgas_for_elec()


_integ_future_share_gascoalgas_for_elec = Integ(
    lambda: increase_share_gas_for_elec() - decrease_share_gas_for_elec(),
    lambda: share_gascoalgas_for_elec_in_2014(),
    "_integ_future_share_gascoalgas_for_elec",
)


@component.add(
    name='"Future share oil/FF for Elec"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_future_share_oilff_for_elec": 1},
    other_deps={
        "_integ_future_share_oilff_for_elec": {
            "initial": {"share_oilff_for_elec_in_2015": 1},
            "step": {
                "increase_share_oil_for_elec": 1,
                "decrease_share_oil_for_elec": 1,
            },
        }
    },
)
def future_share_oilff_for_elec():
    """
    Endogenous future share of oil over (oil+coal+gas) for electricity generation.
    """
    return _integ_future_share_oilff_for_elec()


_integ_future_share_oilff_for_elec = Integ(
    lambda: increase_share_oil_for_elec() - decrease_share_oil_for_elec(),
    lambda: share_oilff_for_elec_in_2015(),
    "_integ_future_share_oilff_for_elec",
)


@component.add(
    name="Gen losses demand for FF Elec plants EJ",
    units="EJ/Year",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gas_elec_plants_ej": 1,
        "efficiency_gas_for_electricity": 1,
        "efficiency_coal_for_electricity": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_oil_elec_plants_ej": 1,
        "efficiency_liquids_for_electricity": 1,
    },
)
def gen_losses_demand_for_ff_elec_plants_ej():
    """
    Total generation losses associated to electricity demand.
    """
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["natural gas"]] = ped_gas_elec_plants_ej() * (
        1 - efficiency_gas_for_electricity()
    )
    value.loc[["coal"]] = ped_coal_elec_plants_ej() * (
        1 - efficiency_coal_for_electricity()
    )
    value.loc[["oil"]] = ped_oil_elec_plants_ej() * (
        1 - efficiency_liquids_for_electricity()
    )
    return value


@component.add(
    name='"Hist share gas/(coal +gas) Elec"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_hist_share_gascoal_gas_elec",
        "__data__": "_ext_data_hist_share_gascoal_gas_elec",
        "time": 1,
    },
)
def hist_share_gascoal_gas_elec():
    """
    Share of natural gas for electricity in relation to the total gas+coal.
    """
    return _ext_data_hist_share_gascoal_gas_elec(time())


_ext_data_hist_share_gascoal_gas_elec = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_hist_share_gascoal_gas_elec",
)


@component.add(
    name='"Hist share oil/FF Elec"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_hist_share_oilff_elec",
        "__data__": "_ext_data_hist_share_oilff_elec",
        "time": 1,
    },
)
def hist_share_oilff_elec():
    """
    Historica share of oil for electricity vs total electricity generation
    """
    return _ext_data_hist_share_oilff_elec(time())


_ext_data_hist_share_oilff_elec = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_oil_over_total_fossil_electricity",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_hist_share_oilff_elec",
)


@component.add(
    name="Historic efficiency gas for electricity",
    units="percent",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_efficiency_gas_for_electricity",
        "__lookup__": "_ext_lookup_historic_efficiency_gas_for_electricity",
    },
)
def historic_efficiency_gas_for_electricity(x, final_subs=None):
    """
    Historical evolution of efficiency of natural gas power centrals 1995-2013 (IEA Balances).
    """
    return _ext_lookup_historic_efficiency_gas_for_electricity(x, final_subs)


_ext_lookup_historic_efficiency_gas_for_electricity = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_lookup_historic_efficiency_gas_for_electricity",
)


@component.add(
    name="improvement efficiency gas for electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_efficiency_gas_for_electricity": 2,
        "percent_to_share": 1,
        "remaining_efficiency_improv_gas_for_electricity": 1,
        "efficiency_improv_gas_for_electricity": 1,
        "efficiency_gas_for_electricity": 1,
    },
)
def improvement_efficiency_gas_for_electricity():
    """
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


@component.add(
    name="increase share gas for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_auxiliar_elec": 1,
        "perception_of_interfuel_ps_scarcity_gascoal": 1,
        "future_share_gascoalgas_for_elec": 1,
    },
)
def increase_share_gas_for_elec():
    """
    Increase in future share of gas over coal+gas for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_gascoal()
        * (1 - future_share_gascoalgas_for_elec())
    )


@component.add(
    name="increase share oil for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_auxiliar_elec": 1,
        "perception_of_interfuel_ps_scarcity_oilff": 1,
        "future_share_oilff_for_elec": 1,
    },
)
def increase_share_oil_for_elec():
    """
    Increase in future share of oil over (oil+coal+gas) for electricity generation.
    """
    return (
        max_auxiliar_elec()
        * perception_of_interfuel_ps_scarcity_oilff()
        * (1 - future_share_oilff_for_elec())
    )


@component.add(
    name="initial efficiency gas for electricity",
    units="percent",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_efficiency_gas_for_electricity"},
)
def initial_efficiency_gas_for_electricity():
    """
    Efficiency of gas power centrals in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_efficiency_gas_for_electricity()


_ext_constant_initial_efficiency_gas_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "initial_efficiency_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_initial_efficiency_gas_for_electricity",
)


@component.add(
    name="max auxiliar Elec", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def max_auxiliar_elec():
    """
    Auxiliarity variable that limit the interchange between fuels to cover electricity.
    """
    return 0.03


@component.add(
    name="Max efficiency gas power plants",
    units="Dnml",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_efficiency_gas_power_plants"},
)
def max_efficiency_gas_power_plants():
    """
    Assumed maximum efficiency level for gas power centrals.
    """
    return _ext_constant_max_efficiency_gas_power_plants()


_ext_constant_max_efficiency_gas_power_plants = ExtConstant(
    "../energy.xlsx",
    "Global",
    "maximum_efficiency_gas_power_plant",
    {},
    _root,
    {},
    "_ext_constant_max_efficiency_gas_power_plants",
)


@component.add(
    name="P share oil oil Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a_lineal_regr_phaseout_oil_for_elec": 1,
        "time": 1,
        "b_lineal_regr_phaseout_ff_for_elec": 1,
    },
)
def p_share_oil_oil_elec():
    """
    Share oil for electricity generation derived from the phase-out policy.
    """
    return np.maximum(
        0,
        a_lineal_regr_phaseout_oil_for_elec() * time()
        + b_lineal_regr_phaseout_ff_for_elec(),
    )


@component.add(
    name="PED coal Elec plants EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_coal_elec_plants_twh": 1,
        "efficiency_coal_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def ped_coal_elec_plants_ej():
    """
    Primary energy demand of coal (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_coal_elec_plants_twh() / efficiency_coal_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="PED gas Elec plants EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_gas_elec_plants_twh": 1,
        "efficiency_gas_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def ped_gas_elec_plants_ej():
    """
    Primary energy demand of natural gas (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_gas_elec_plants_twh() / efficiency_gas_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="PED oil Elec plants EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_oil_elec_plants_twh": 1,
        "efficiency_liquids_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def ped_oil_elec_plants_ej():
    """
    Primary energy demand of oil (EJ) for electric generation (including generation losses).
    """
    return (
        fe_demand_oil_elec_plants_twh() / efficiency_liquids_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="percent to share", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def percent_to_share():
    """
    Conversion of percent to share.
    """
    return 0.01


@component.add(
    name='"perception of inter-fuel PS scarcity coal-gas"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_coalgas():
    """
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


@component.add(
    name='"perception of inter-fuel PS scarcity coal-oil"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_coaloil():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["coal", "oil"])
    )


@component.add(
    name='"perception of inter-fuel PS scarcity FF-oil"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_of_interfuel_ps_scarcity_coaloil": 1,
        "perception_of_interfuel_ps_scarcity_nat_gasoil": 1,
    },
)
def perception_of_interfuel_ps_scarcity_ffoil():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-fossil fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_coaloil(),
        perception_of_interfuel_ps_scarcity_nat_gasoil(),
    )


@component.add(
    name='"perception of inter-fuel PS scarcity gas-coal"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_gascoal():
    """
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


@component.add(
    name='"perception of inter-fuel PS scarcity nat. gas-oil"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_nat_gasoil():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc["natural gas", "oil"]
        ),
    )


@component.add(
    name='"perception of inter-fuel PS scarcity oil-coal"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_oilcoal():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return np.maximum(
        0, float(perception_of_interfuel_primary_sources_scarcity().loc["oil", "coal"])
    )


@component.add(
    name='"perception of inter-fuel PS scarcity oil-FF"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_of_interfuel_ps_scarcity_oilcoal": 1,
        "perception_of_interfuel_ps_scarcity_oilnatgas": 1,
    },
)
def perception_of_interfuel_ps_scarcity_oilff():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-fossil fuels)
    """
    return np.maximum(
        perception_of_interfuel_ps_scarcity_oilcoal(),
        perception_of_interfuel_ps_scarcity_oilnatgas(),
    )


@component.add(
    name='"perception of inter-fuel PS scarcity oil-nat.gas"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_oilnatgas():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
    """
    return np.maximum(
        0,
        float(
            perception_of_interfuel_primary_sources_scarcity().loc["oil", "natural gas"]
        ),
    )


@component.add(
    name='"phase-out oil for electricity?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_phaseout_oil_for_electricity"},
)
def phaseout_oil_for_electricity():
    """
    Activation of a policies to reduce oil contribution in electricity linearly: If=1: ACTIVATED, If=0: DEACTIVATED.
    """
    return _ext_constant_phaseout_oil_for_electricity()


_ext_constant_phaseout_oil_for_electricity = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "phase_out_oil_electr",
    {},
    _root,
    {},
    "_ext_constant_phaseout_oil_for_electricity",
)


@component.add(
    name="remaining efficiency improv gas for electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_efficiency_gas_power_plants": 2,
        "efficiency_gas_for_electricity": 1,
    },
)
def remaining_efficiency_improv_gas_for_electricity():
    """
    Remaining efficiency improvement for gas power centrals.
    """
    return (
        max_efficiency_gas_power_plants() - efficiency_gas_for_electricity()
    ) / max_efficiency_gas_power_plants()


@component.add(
    name="share coal for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_gascoal_gas_for_elec": 1},
)
def share_coal_for_elec():
    """
    Coal is assumed to cover the rest of the electricity demand after RES, nuclear, oil and gas.
    """
    return 1 - share_gascoal_gas_for_elec()


@component.add(
    name='"share gas/(coal +gas) for Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_scarcityps_elec_substit": 1,
        "hist_share_gascoal_gas_elec": 2,
        "future_share_gascoalgas_for_elec": 1,
        "time": 1,
    },
)
def share_gascoal_gas_for_elec():
    """
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


@component.add(
    name='"share gas/(coal+gas) for Elec in 2014"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_gascoalgas_for_elec_in_2014"},
)
def share_gascoalgas_for_elec_in_2014():
    """
    Historic data
    """
    return _ext_constant_share_gascoalgas_for_elec_in_2014()


_ext_constant_share_gascoalgas_for_elec_in_2014 = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas_2014",
    {},
    _root,
    {},
    "_ext_constant_share_gascoalgas_for_elec_in_2014",
)


@component.add(
    name="share in target year FF for elec",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_in_target_year_ff_for_elec"},
)
def share_in_target_year_ff_for_elec():
    """
    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_share_in_target_year_ff_for_elec()


_ext_constant_share_in_target_year_ff_for_elec = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_target_year_oil_for_elec",
    {},
    _root,
    {},
    "_ext_constant_share_in_target_year_ff_for_elec",
)


@component.add(
    name="share oil for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_scarcityps_elec_substit": 1,
        "hist_share_oilff_elec": 3,
        "p_share_oil_oil_elec": 1,
        "phaseout_oil_for_electricity": 1,
        "time": 2,
        "start_year_policy_phaseout_oil_for_elec": 1,
        "future_share_oilff_for_elec": 1,
    },
)
def share_oil_for_elec():
    """
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
                    lambda: p_share_oil_oil_elec(),
                ),
            ),
        ),
    )


@component.add(
    name='"share oil/FF for Elec in 2015"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_oilff_for_elec_in_2015"},
)
def share_oilff_for_elec_in_2015():
    """
    Historic data
    """
    return _ext_constant_share_oilff_for_elec_in_2015()


_ext_constant_share_oilff_for_elec_in_2015 = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "share_of_electricity_produced_from_oil_over_total_fossil_electricity_2015",
    {},
    _root,
    {},
    "_ext_constant_share_oilff_for_elec_in_2015",
)


@component.add(
    name='"start year policy phase-out oil for elec"',
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_phaseout_oil_for_elec"
    },
)
def start_year_policy_phaseout_oil_for_elec():
    """
    From customized year, start policy phase-out oil for electricity.
    """
    return _ext_constant_start_year_policy_phaseout_oil_for_elec()


_ext_constant_start_year_policy_phaseout_oil_for_elec = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_phaseout_oil_for_elec",
)


@component.add(
    name='"switch scarcity-PS elec substit"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def switch_scarcityps_elec_substit():
    """
    This swith allows the endogenous replacement of primary and final fuels depending on their relative abundance: =1: activated. =0: not activated
    """
    return 1


@component.add(
    name='"target year policy phase-out FF for elec"',
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_target_year_policy_phaseout_ff_for_elec"
    },
)
def target_year_policy_phaseout_ff_for_elec():
    """
    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_target_year_policy_phaseout_ff_for_elec()


_ext_constant_target_year_policy_phaseout_ff_for_elec = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "target_year_policy_phase_out_oil_electricity",
    {},
    _root,
    {},
    "_ext_constant_target_year_policy_phaseout_ff_for_elec",
)
