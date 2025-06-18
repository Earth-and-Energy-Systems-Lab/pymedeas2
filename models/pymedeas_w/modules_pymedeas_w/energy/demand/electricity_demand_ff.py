"""
Module energy.demand.electricity_demand_ff
Translated using PySD version 3.14.2
"""

@component.add(
    name='"a_lineal_regr_phase-out_oil_for_elec"',
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_oil_for_elec": 1,
        "hist_share_oilff_elec": 1,
        "start_year_policy_phaseout_oil_for_elec": 1,
        "target_year_policy_phaseout_oil_for_elec": 1,
    },
)
def a_lineal_regr_phaseout_oil_for_elec():
    """
    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (share_in_target_year_oil_for_elec() - hist_share_oilff_elec()) / (
        target_year_policy_phaseout_oil_for_elec()
        - start_year_policy_phaseout_oil_for_elec()
    )


@component.add(
    name="Abundance_primary_sources",
    units="Dmnl",
    subscripts=["primary_sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "abundance_coal": 1,
        "abundance_total_oil": 1,
        "abundance_total_nat_gas": 1,
    },
)
def abundance_primary_sources():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    value = xr.DataArray(
        np.nan,
        {"primary_sources": _subscript_dict["primary_sources"]},
        ["primary_sources"],
    )
    value.loc[["coal"]] = abundance_coal()
    value.loc[["oil"]] = abundance_total_oil()
    value.loc[["natural_gas"]] = abundance_total_nat_gas()
    value.loc[["others"]] = 1
    return value


@component.add(
    name='"b_lineal_regr_phase-out_oil_for_elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_oil_for_elec": 1,
        "target_year_policy_phaseout_oil_for_elec": 1,
        "a_lineal_regr_phaseout_oil_for_elec": 1,
    },
)
def b_lineal_regr_phaseout_oil_for_elec():
    """
    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for electricity over time.
    """
    return (
        share_in_target_year_oil_for_elec()
        - a_lineal_regr_phaseout_oil_for_elec()
        * target_year_policy_phaseout_oil_for_elec()
    )


@component.add(
    name="decrease_share_gas_for_Elec",
    units="Dmnl/year",
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
    name="decrease_share_oil_for_Elec",
    units="Dmnl/year",
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
    name="demand_Elec_gas_and_coal_TWh",
    units="TWh/year",
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
    name="demand_Elec_plants_fossil_fuels_TWh",
    units="TWh/year",
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
    return float(
        np.maximum(
            demand_elec_nre_twh()
            - fe_nuclear_elec_generation_twh()
            - fes_elec_fossil_fuel_chp_plants_twh(),
            0,
        )
    )


@component.add(
    name='"Desired_share_gas/(coal+gas)_Elec"',
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "end_hist_data": 3,
        "hist_share_gascoal_gas_elec": 3,
        "policy_share_gascoalgas_elec": 2,
        "target_year_policy_gas_electricity": 2,
    },
)
def desired_share_gascoalgas_elec():
    return if_then_else(
        time() < end_hist_data(),
        lambda: hist_share_gascoal_gas_elec(),
        lambda: if_then_else(
            time() < target_year_policy_gas_electricity(),
            lambda: hist_share_gascoal_gas_elec()
            + (
                (policy_share_gascoalgas_elec() - hist_share_gascoal_gas_elec())
                / (target_year_policy_gas_electricity() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: policy_share_gascoalgas_elec(),
        ),
    )


@component.add(
    name="efficiency_coal_for_electricity",
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
    r"../energy.xlsx",
    "World",
    "efficiency_coal_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_coal_for_electricity",
)


@component.add(
    name="efficiency_gas_for_electricity",
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
    name="Efficiency_improv_gas_for_electricity",
    units="Dmnl/year",
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
    r"../energy.xlsx",
    "Global",
    "efficiency_improv_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_improv_gas_for_electricity",
)


@component.add(
    name="efficiency_liquids_for_electricity",
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
    r"../energy.xlsx",
    "World",
    "efficiency_liquids_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_liquids_for_electricity",
)


@component.add(
    name="FE_demand_coal_Elec_plants_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_gascoal_gas_for_elec": 1, "demand_elec_gas_and_coal_twh": 1},
)
def fe_demand_coal_elec_plants_twh():
    """
    Final energy demand of coal for electricity consumption (TWh).
    """
    return (1 - share_gascoal_gas_for_elec()) * demand_elec_gas_and_coal_twh()


@component.add(
    name="FE_demand_gas_Elec_plants_TWh",
    units="TWh/year",
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
    name="FE_demand_oil_Elec_plants_TWh",
    units="TWh/year",
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
    name="FES_Elec_fossil_fuel_CHP_plants_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_elec_fossil_fuel_chp_plants_ej": 1, "ej_per_twh": 1},
)
def fes_elec_fossil_fuel_chp_plants_twh():
    """
    Final Energy of fossil fuels to produce electricity (TWh) in CHP plants.
    """
    return fes_elec_fossil_fuel_chp_plants_ej() / ej_per_twh()


@component.add(
    name='"Future_share_gas+coal/FF_for_elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_oil_for_elec": 1},
)
def future_share_gascoalff_for_elec():
    return 1 - share_oil_for_elec()


@component.add(
    name='"Future_share_gas/(coal+gas)_for_Elec"',
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
    name='"Future_share_oil/FF_for_Elec"',
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
    name='"Hist_share_gas/(coal_+gas)_Elec"',
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
    r"../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_hist_share_gascoal_gas_elec",
)


@component.add(
    name='"Hist_share_oil/FF_Elec"',
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
    Share of oil for electricity (Data extracted from database World Bank: "Electricity production from oil sources (% of total) " / "Electricity production from oil, gas and coal sources (% of total)").
    """
    return _ext_data_hist_share_oilff_elec(time())


_ext_data_hist_share_oilff_elec = ExtData(
    r"../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_of_electricity_produced_from_oil_over_total_fossil_electricity",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_hist_share_oilff_elec",
)


@component.add(
    name="Historic_efficiency_gas_for_electricity",
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
    r"../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_efficiency_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_lookup_historic_efficiency_gas_for_electricity",
)


@component.add(
    name="improvement_efficiency_gas_for_electricity",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "time_step": 2,
        "percent_to_share": 1,
        "historic_efficiency_gas_for_electricity": 2,
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
            historic_efficiency_gas_for_electricity(time() + time_step())
            - historic_efficiency_gas_for_electricity(time())
        )
        / time_step()
        * percent_to_share(),
        lambda: efficiency_gas_for_electricity()
        * remaining_efficiency_improv_gas_for_electricity()
        * efficiency_improv_gas_for_electricity(),
    )


@component.add(
    name="increase_in_perception_PS_scarcity",
    units="Dmnl/year",
    subscripts=["primary_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_primary_sources": 1,
        "sensitivity_to_scarcity": 1,
        "perception_in_primary_sources_scarcity": 1,
        "nvs_1_year": 1,
    },
)
def increase_in_perception_ps_scarcity():
    """
    Increase in socieconomic perception of primary sources scarcity of each fuel
    """
    return (
        scarcity_primary_sources()
        * sensitivity_to_scarcity()
        * (1 - perception_in_primary_sources_scarcity())
        / nvs_1_year()
    )


@component.add(
    name="increase_share_gas_for_Elec",
    units="Dmnl/year",
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
    name="increase_share_oil_for_Elec",
    units="Dmnl/year",
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
    name="initial_efficiency_gas_for_electricity",
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
    r"../energy.xlsx",
    "World",
    "initial_efficiency_gas_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_initial_efficiency_gas_for_electricity",
)


@component.add(
    name="max_auxiliar_Elec",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_auxiliar_elec():
    """
    Auxiliarity variable that limit the interchange between fuels to cover electricity.
    """
    return 0.03


@component.add(
    name="Max_efficiency_gas_power_plants",
    units="Dmnl",
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
    r"../energy.xlsx",
    "Global",
    "maximum_efficiency_gas_power_plant",
    {},
    _root,
    {},
    "_ext_constant_max_efficiency_gas_power_plants",
)


@component.add(
    name="P_share_oil_for_Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a_lineal_regr_phaseout_oil_for_elec": 1,
        "time": 1,
        "b_lineal_regr_phaseout_oil_for_elec": 1,
    },
)
def p_share_oil_for_elec():
    """
    Share oil for electricity generation derived from the phase-out policy.
    """
    return float(
        np.maximum(
            0,
            a_lineal_regr_phaseout_oil_for_elec() * time()
            + b_lineal_regr_phaseout_oil_for_elec(),
        )
    )


@component.add(
    name="PE_demand_coal_Elec_plants_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_coal_elec_plants_twh": 1,
        "efficiency_coal_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def pe_demand_coal_elec_plants_ej():
    """
    Primary energy demand of coal (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_coal_elec_plants_twh() / efficiency_coal_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="PE_demand_gas_Elec_plants_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_gas_elec_plants_twh": 1,
        "efficiency_gas_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def pe_demand_gas_elec_plants_ej():
    """
    Primary energy demand of natural gas (EJ) for electricity consumption (including generation losses).
    """
    return (
        fe_demand_gas_elec_plants_twh() / efficiency_gas_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="PE_demand_oil_Elec_plants_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_oil_elec_plants_twh": 1,
        "efficiency_liquids_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def pe_demand_oil_elec_plants_ej():
    """
    Primary energy demand of oil (EJ) for electric generation (including generation losses).
    """
    return (
        fe_demand_oil_elec_plants_twh() / efficiency_liquids_for_electricity()
    ) * ej_per_twh()


@component.add(
    name="percent_to_share", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def percent_to_share():
    """
    Conversion of percent to share.
    """
    return 0.01


@component.add(
    name="perception_in_primary_sources_scarcity",
    units="Dmnl",
    subscripts=["primary_sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_perception_in_primary_sources_scarcity": 1},
    other_deps={
        "_integ_perception_in_primary_sources_scarcity": {
            "initial": {},
            "step": {
                "increase_in_perception_ps_scarcity": 1,
                "reduction_in_perception_ps_scarcity": 1,
            },
        }
    },
)
def perception_in_primary_sources_scarcity():
    """
    Perception of primary sources scarcity of each fuel by economic sectors. This perception drives the fuel replacement for electriciy and heat.
    """
    return _integ_perception_in_primary_sources_scarcity()


_integ_perception_in_primary_sources_scarcity = Integ(
    lambda: increase_in_perception_ps_scarcity()
    - reduction_in_perception_ps_scarcity(),
    lambda: xr.DataArray(
        0, {"primary_sources": _subscript_dict["primary_sources"]}, ["primary_sources"]
    ),
    "_integ_perception_in_primary_sources_scarcity",
)


@component.add(
    name='"perception_of_inter-fuel_primary_sources_scarcity"',
    units="Dmnl",
    subscripts=["primary_sources1", "primary_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_to_scarcity": 4,
        "perception_in_primary_sources_scarcity": 8,
    },
)
def perception_of_interfuel_primary_sources_scarcity():
    """
    Perception of primary energy scarcity between fuels. This perception drives the fuel replacement in electricity and heat sectors. TODO
    """
    value = xr.DataArray(
        np.nan,
        {
            "primary_sources1": _subscript_dict["primary_sources1"],
            "primary_sources": _subscript_dict["primary_sources"],
        },
        ["primary_sources1", "primary_sources"],
    )
    value.loc[["coal"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary_sources": _subscript_dict["primary_sources"]},
                ["primary_sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["coal"]),
                1,
            ),
        )
        .expand_dims({"primary_sources1": ["coal"]}, 0)
        .values
    )
    value.loc[["oil"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary_sources": _subscript_dict["primary_sources"]},
                ["primary_sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["oil"]),
                1,
            ),
        )
        .expand_dims({"primary_sources1": ["oil"]}, 0)
        .values
    )
    value.loc[["natural_gas"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary_sources": _subscript_dict["primary_sources"]},
                ["primary_sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["natural_gas"]),
                1,
            ),
        )
        .expand_dims({"primary_sources1": ["natural_gas"]}, 0)
        .values
    )
    value.loc[["others"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary_sources": _subscript_dict["primary_sources"]},
                ["primary_sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["others"]),
                1,
            ),
        )
        .expand_dims({"primary_sources1": ["others"]}, 0)
        .values
    )
    return value


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_coal-gas"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_coalgas():
    """
    Socieconomic perception of final energy scarcity between fuels (gas-coal)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc[
                    "coal", "natural_gas"
                ]
            ),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_coal-oil"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_coaloil():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc["coal", "oil"]
            ),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_FF-oil"',
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
    return float(
        np.maximum(
            perception_of_interfuel_ps_scarcity_coaloil(),
            perception_of_interfuel_ps_scarcity_nat_gasoil(),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_gas-coal"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_gascoal():
    """
    Socieconomic perception of final energy scarcity between fuels (gas-coal)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc[
                    "natural_gas", "coal"
                ]
            ),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_nat._gas-oil"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_nat_gasoil():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc[
                    "natural_gas", "oil"
                ]
            ),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_oil-coal"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_oilcoal():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-coal)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc["oil", "coal"]
            ),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_oil-FF"',
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
    return float(
        np.maximum(
            perception_of_interfuel_ps_scarcity_oilcoal(),
            perception_of_interfuel_ps_scarcity_oilnatgas(),
        )
    )


@component.add(
    name='"perception_of_inter-fuel_PS_scarcity_oil-nat.gas"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perception_of_interfuel_primary_sources_scarcity": 1},
)
def perception_of_interfuel_ps_scarcity_oilnatgas():
    """
    Socieconomic perception of final energy scarcity between fuels (oil-natural gas)
    """
    return float(
        np.maximum(
            0,
            float(
                perception_of_interfuel_primary_sources_scarcity().loc[
                    "oil", "natural_gas"
                ]
            ),
        )
    )


@component.add(
    name='"phase-out_oil_for_electricity?"',
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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "phase_out_oil_electr",
    {},
    _root,
    {},
    "_ext_constant_phaseout_oil_for_electricity",
)


@component.add(
    name='"policy_share_gas/(coal+gas)_Elec"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_policy_share_gascoalgas_elec"},
)
def policy_share_gascoalgas_elec():
    return _ext_constant_policy_share_gascoalgas_elec()


_ext_constant_policy_share_gascoalgas_elec = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "p_share_gas_elec",
    {},
    _root,
    {},
    "_ext_constant_policy_share_gascoalgas_elec",
)


@component.add(
    name="reduction_in_perception_PS_scarcity",
    units="Dmnl/year",
    subscripts=["primary_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_in_primary_sources_scarcity": 1,
        "energy_scarcity_forgetting_time": 1,
    },
)
def reduction_in_perception_ps_scarcity():
    """
    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_in_primary_sources_scarcity() / energy_scarcity_forgetting_time()


@component.add(
    name="remaining_efficiency_improv_gas_for_electricity",
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
    name="scarcity_primary_sources",
    units="Dmnl",
    subscripts=["primary_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_primary_sources": 1},
)
def scarcity_primary_sources():
    """
    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_primary_sources()


@component.add(
    name='"share_gas/(coal_+gas)_for_Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_scarcityps_elec_substit": 1,
        "desired_share_gascoalgas_elec": 2,
        "time": 1,
        "future_share_gascoalgas_for_elec": 1,
    },
)
def share_gascoal_gas_for_elec():
    """
    Share of natural gas for electricity in relation to the total fossil fuels for electricity.
    """
    return if_then_else(
        switch_scarcityps_elec_substit() == 0,
        lambda: desired_share_gascoalgas_elec(),
        lambda: if_then_else(
            time() > 2014,
            lambda: future_share_gascoalgas_for_elec(),
            lambda: desired_share_gascoalgas_elec(),
        ),
    )


@component.add(
    name='"share_gas/(coal+gas)_for_Elec_in_2014"',
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
    r"../energy.xlsx",
    "World",
    "share_of_electricity_produced_from_gas_over_electricity_produced_coal_and_gas_2014",
    {},
    _root,
    {},
    "_ext_constant_share_gascoalgas_for_elec_in_2014",
)


@component.add(
    name="share_in_target_year_oil_for_elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_in_target_year_oil_for_elec"},
)
def share_in_target_year_oil_for_elec():
    """
    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_share_in_target_year_oil_for_elec()


_ext_constant_share_in_target_year_oil_for_elec = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "share_target_year_oil_for_elec",
    {},
    _root,
    {},
    "_ext_constant_share_in_target_year_oil_for_elec",
)


@component.add(
    name="share_oil_for_Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_scarcityps_elec_substit": 1,
        "hist_share_oilff_elec": 3,
        "p_share_oil_for_elec": 1,
        "time": 2,
        "future_share_oilff_for_elec": 1,
        "start_year_policy_phaseout_oil_for_elec": 1,
        "phaseout_oil_for_electricity": 1,
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
                    lambda: p_share_oil_for_elec(),
                ),
            ),
        ),
    )


@component.add(
    name='"share_oil/FF_for_Elec_in_2015"',
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
    r"../energy.xlsx",
    "World",
    "share_of_electricity_produced_from_oil_over_total_fossil_electricity_2015",
    {},
    _root,
    {},
    "_ext_constant_share_oilff_for_elec_in_2015",
)


@component.add(
    name='"start_year_policy_phase-out_oil_for_elec"',
    units="year",
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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_phaseout_oil_for_elec",
)


@component.add(
    name='"switch_scarcity-PS_elec_substit"',
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
    name="target_year_policy_gas_electricity",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_target_year_policy_gas_electricity"},
)
def target_year_policy_gas_electricity():
    return _ext_constant_target_year_policy_gas_electricity()


_ext_constant_target_year_policy_gas_electricity = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "target_year_policy_gas_electricity",
    {},
    _root,
    {},
    "_ext_constant_target_year_policy_gas_electricity",
)


@component.add(
    name='"target_year_policy_phase-out_oil_for_elec"',
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_target_year_policy_phaseout_oil_for_elec"
    },
)
def target_year_policy_phaseout_oil_for_elec():
    """
    Target year for the policy phase-out oil for electricity.
    """
    return _ext_constant_target_year_policy_phaseout_oil_for_elec()


_ext_constant_target_year_policy_phaseout_oil_for_elec = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "target_year_policy_phase_out_oil_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_target_year_policy_phaseout_oil_for_elec",
)


@component.add(
    name="Total_gen_losses_demand_for_Elec_plants_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_demand_gas_elec_plants_ej": 1,
        "efficiency_gas_for_electricity": 1,
        "efficiency_coal_for_electricity": 1,
        "pe_demand_coal_elec_plants_ej": 1,
        "efficiency_liquids_for_electricity": 1,
        "pe_demand_oil_elec_plants_ej": 1,
        "pe_losses_uranium_for_elec_ej": 1,
        "pe_losses_bioe_for_elec_ej": 1,
    },
)
def total_gen_losses_demand_for_elec_plants_ej():
    """
    Total generation losses associated to electricity demand.
    """
    return (
        pe_demand_gas_elec_plants_ej() * (1 - efficiency_gas_for_electricity())
        + pe_demand_coal_elec_plants_ej() * (1 - efficiency_coal_for_electricity())
        + pe_demand_oil_elec_plants_ej() * (1 - efficiency_liquids_for_electricity())
        + pe_losses_uranium_for_elec_ej()
        + pe_losses_bioe_for_elec_ej()
    )
