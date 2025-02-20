"""
Module energy.demand.commercial_heat_demand_covered
Translated using PySD version 3.14.0
"""

@component.add(
    name='"a lineal regr phase-out oil for heat"',
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_oil_for_heat": 1,
        "historic_share_liquids_for_heat_plants": 1,
        "target_year_policy_phaseout_oil_for_heat": 1,
        "start_year_policy_phaseout_oil_for_heat": 1,
    },
)
def a_lineal_regr_phaseout_oil_for_heat():
    """
    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for heat over time.
    """
    return (
        share_in_target_year_oil_for_heat() - historic_share_liquids_for_heat_plants()
    ) / (
        target_year_policy_phaseout_oil_for_heat()
        - start_year_policy_phaseout_oil_for_heat()
    )


@component.add(
    name='"b lineal regr phase-out oil for heat"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_in_target_year_oil_for_heat": 1,
        "target_year_policy_phaseout_oil_for_heat": 1,
        "a_lineal_regr_phaseout_oil_for_heat": 1,
    },
)
def b_lineal_regr_phaseout_oil_for_heat():
    """
    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the share of oil for heat over time.
    """
    return (
        share_in_target_year_oil_for_heat()
        - a_lineal_regr_phaseout_oil_for_heat()
        * target_year_policy_phaseout_oil_for_heat()
    )


@component.add(
    name="efficiency coal for heat plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_coal_for_heat_plants",
        "__data__": "_ext_data_efficiency_coal_for_heat_plants",
        "time": 1,
    },
)
def efficiency_coal_for_heat_plants():
    """
    Efficiency of coal heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_coal_for_heat_plants(time())


_ext_data_efficiency_coal_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_coal_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_coal_for_heat_plants",
)


@component.add(
    name="efficiency gases for heat plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_gases_for_heat_plants",
        "__data__": "_ext_data_efficiency_gases_for_heat_plants",
        "time": 1,
    },
)
def efficiency_gases_for_heat_plants():
    """
    Efficiency of gas heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_gases_for_heat_plants(time())


_ext_data_efficiency_gases_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_gases_for_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_gases_for_heat_plants",
)


@component.add(
    name="efficiency liquids for heat plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_liquids_for_heat_plants",
        "__data__": "_ext_data_efficiency_liquids_for_heat_plants",
        "time": 1,
    },
)
def efficiency_liquids_for_heat_plants():
    """
    Efficiency of liquids heat plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_liquids_for_heat_plants(time())


_ext_data_efficiency_liquids_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_liquids_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_liquids_for_heat_plants",
)


@component.add(
    name="FED Heat coal plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_gascoal_ej": 1, "share_coalcoalgas_for_heat_plants": 1},
)
def fed_heat_coal_plants():
    """
    Final energy demand of coal to produce heat.
    """
    return fed_heat_gascoal_ej() * share_coalcoalgas_for_heat_plants()


@component.add(
    name="FED Heat gas plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_gascoal_ej": 1, "share_gascoalgas_for_heat_plants": 1},
)
def fed_heat_gas_plants():
    """
    Final energy demand of gas to produce heat.
    """
    return fed_heat_gascoal_ej() * share_gascoalgas_for_heat_plants()


@component.add(
    name='"FED Heat gas+coal EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_plants_fossil_fuels_ej": 1,
        "fed_heat_liquids_plants_ej": 1,
    },
)
def fed_heat_gascoal_ej():
    return fed_heatcom_plants_fossil_fuels_ej() - fed_heat_liquids_plants_ej()


@component.add(
    name="FED Heat liquids plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_plants_fossil_fuels_ej": 1,
        "share_liquids_for_heat_plants": 1,
    },
)
def fed_heat_liquids_plants_ej():
    """
    Final energy demand of liquids to produce heat.
    """
    return fed_heatcom_plants_fossil_fuels_ej() * share_liquids_for_heat_plants()


@component.add(
    name="Gen losses demand for FF Heat plants",
    units="EJ/year",
    subscripts=[np.str_("fossil fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gases_for_heat_plants_ej": 1,
        "efficiency_gases_for_heat_plants": 1,
        "ped_oil_for_heat_plants": 1,
        "efficiency_liquids_for_heat_plants": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "efficiency_coal_for_heat_plants": 1,
    },
)
def gen_losses_demand_for_ff_heat_plants():
    """
    Total generation losses associated to heat plants.
    """
    value = xr.DataArray(
        np.nan,
        {"fossil fuels": _subscript_dict["fossil fuels"]},
        [np.str_("fossil fuels")],
    )
    value.loc[["natural gas"]] = ped_gases_for_heat_plants_ej() * (
        1 - efficiency_gases_for_heat_plants()
    )
    value.loc[["oil"]] = ped_oil_for_heat_plants() * (
        1 - efficiency_liquids_for_heat_plants()
    )
    value.loc[["coal"]] = ped_coal_for_heat_plants_ej() * (
        1 - efficiency_coal_for_heat_plants()
    )
    return value


@component.add(
    name="Historic share liquids for heat plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_liquids_for_heat_plants",
        "__data__": "_ext_data_historic_share_liquids_for_heat_plants",
        "time": 1,
    },
)
def historic_share_liquids_for_heat_plants():
    """
    Historic share liquids for heat plants vs heat production from fossil fuels.
    """
    return _ext_data_historic_share_liquids_for_heat_plants(time())


_ext_data_historic_share_liquids_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_of_liquids_in_heat_plants",
    None,
    {},
    _root,
    {},
    "_ext_data_historic_share_liquids_for_heat_plants",
)


@component.add(
    name="P share oil for Heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a_lineal_regr_phaseout_oil_for_heat": 1,
        "time": 1,
        "b_lineal_regr_phaseout_oil_for_heat": 1,
    },
)
def p_share_oil_for_heat():
    """
    Share oil for heat generation derived from the phase-out policy.
    """
    return np.maximum(
        0,
        a_lineal_regr_phaseout_oil_for_heat() * time()
        + b_lineal_regr_phaseout_oil_for_heat(),
    )


@component.add(
    name="PED coal for Heat plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_coal_plants": 1, "efficiency_coal_for_heat_plants": 1},
)
def ped_coal_for_heat_plants_ej():
    """
    Primary energy demand of coal (EJ) for heat consumption (including generation losses).
    """
    return zidz(fed_heat_coal_plants(), efficiency_coal_for_heat_plants())


@component.add(
    name="PED FF for Heat plants",
    units="EJ/year",
    subscripts=["matter final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heat_liquids_plants_ej": 1,
        "efficiency_liquids_for_heat_plants": 1,
        "fed_heat_gas_plants": 1,
        "efficiency_gases_for_heat_plants": 1,
        "fed_heat_coal_plants": 1,
        "efficiency_coal_for_heat_plants": 1,
    },
)
def ped_ff_for_heat_plants():
    value = xr.DataArray(
        np.nan,
        {"matter final sources": _subscript_dict["matter final sources"]},
        ["matter final sources"],
    )
    value.loc[["liquids"]] = zidz(
        fed_heat_liquids_plants_ej(), efficiency_liquids_for_heat_plants()
    )
    value.loc[["gases"]] = zidz(
        fed_heat_gas_plants(), efficiency_gases_for_heat_plants()
    )
    value.loc[["solids"]] = zidz(
        fed_heat_coal_plants(), efficiency_coal_for_heat_plants()
    )
    return value


@component.add(
    name="PED gases for Heat plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_gas_plants": 1, "efficiency_gases_for_heat_plants": 1},
)
def ped_gases_for_heat_plants_ej():
    """
    Primary energy demand of gas (EJ) for heat consumption (including generation losses).
    """
    return zidz(fed_heat_gas_plants(), efficiency_gases_for_heat_plants())


@component.add(
    name="PED oil for Heat plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heat_liquids_plants_ej": 1,
        "efficiency_liquids_for_heat_plants": 1,
    },
)
def ped_oil_for_heat_plants():
    """
    Primary energy demand of oil (EJ) for heat consumption (including generation losses).
    """
    return zidz(fed_heat_liquids_plants_ej(), efficiency_liquids_for_heat_plants())


@component.add(
    name='"phase-out oil for heat?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_phaseout_oil_for_heat"},
)
def phaseout_oil_for_heat():
    """
    Activation of a policies to reduce oil contribution in heat commercial linearly: If=1: ACTIVATED, If=0: DEACTIVATED.
    """
    return _ext_constant_phaseout_oil_for_heat()


_ext_constant_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "phase_out_oil_heat",
    {},
    _root,
    {},
    "_ext_constant_phaseout_oil_for_heat",
)


@component.add(
    name='"share coal(coal+gas) for heat plants"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_gascoalgas_for_heat_plants": 1},
)
def share_coalcoalgas_for_heat_plants():
    """
    Coal is assumed to cover the rest of the heat demand after RES, nuclear, oil and gas.
    """
    return 1 - share_gascoalgas_for_heat_plants()


@component.add(
    name='"share gas/(coal+gas) for heat plants"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_gascoalgas_for_heat_plants",
        "__data__": "_ext_data_share_gascoalgas_for_heat_plants",
        "time": 1,
    },
)
def share_gascoalgas_for_heat_plants():
    """
    Share of natural gas for electricity in relation to the total fossil fuels for heat
    """
    return _ext_data_share_gascoalgas_for_heat_plants(time())


_ext_data_share_gascoalgas_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_of_heat_produced_from_gas_over_electricity_produced_coal_and_gas",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_gascoalgas_for_heat_plants",
)


@component.add(
    name="share in target year oil for heat",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_in_target_year_oil_for_heat"},
)
def share_in_target_year_oil_for_heat():
    """
    Target year for the policy phase-out oil for heat.
    """
    return _ext_constant_share_in_target_year_oil_for_heat()


_ext_constant_share_in_target_year_oil_for_heat = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_target_year_oil_for_heat",
    {},
    _root,
    {},
    "_ext_constant_share_in_target_year_oil_for_heat",
)


@component.add(
    name="share liquids for heat plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_share_liquids_for_heat_plants": 3,
        "p_share_oil_for_heat": 1,
        "phaseout_oil_for_heat": 1,
        "start_year_policy_phaseout_oil_for_heat": 1,
    },
)
def share_liquids_for_heat_plants():
    """
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


@component.add(
    name='"start year policy phase-out oil for heat"',
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_phaseout_oil_for_heat"
    },
)
def start_year_policy_phaseout_oil_for_heat():
    """
    From customized year, start policy phase-out oil for heat.
    """
    return _ext_constant_start_year_policy_phaseout_oil_for_heat()


_ext_constant_start_year_policy_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_policy_phase_out_oil_for_heat",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_phaseout_oil_for_heat",
)


@component.add(
    name='"target year policy phase-out oil for heat"',
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_target_year_policy_phaseout_oil_for_heat"
    },
)
def target_year_policy_phaseout_oil_for_heat():
    """
    Target year for the policy phase-out oil for heat.
    """
    return _ext_constant_target_year_policy_phaseout_oil_for_heat()


_ext_constant_target_year_policy_phaseout_oil_for_heat = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "target_year_policy_phase_out_oil_heat",
    {},
    _root,
    {},
    "_ext_constant_target_year_policy_phaseout_oil_for_heat",
)
