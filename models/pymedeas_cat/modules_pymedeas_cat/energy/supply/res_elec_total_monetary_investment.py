"""
Module energy.supply.res_elec_total_monetary_investment
Translated using PySD version 3.14.0
"""

@component.add(
    name="Balancing_costs",
    units="Tdollars/TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_variable_res_elec_generation_vs_total": 1,
        "balancing_costs_ref": 1,
        "twh_to_mwh": 1,
        "nvs_to_t": 1,
    },
)
def balancing_costs():
    """
    Balancing costs (1995T$ / TWh produced).
    """
    return (
        balancing_costs_ref(share_variable_res_elec_generation_vs_total())
        * twh_to_mwh()
        / nvs_to_t()
    )


@component.add(
    name="Balancing_costs_ref",
    units="dollars/MWh",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_balancing_costs_ref",
        "__lookup__": "_ext_lookup_balancing_costs_ref",
    },
)
def balancing_costs_ref(x, final_subs=None):
    """
    Balancing costs adapting data from Holttinen et al (2011).
    """
    return _ext_lookup_balancing_costs_ref(x, final_subs)


_ext_lookup_balancing_costs_ref = ExtLookup(
    "../energy.xlsx",
    "Global",
    "share_of_variable_res",
    "balancing_cost",
    {},
    _root,
    {},
    "_ext_lookup_balancing_costs_ref",
)


@component.add(
    name="cumulated_invest_E_grid",
    units="Tdollars",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_invest_e_grid": 1},
    other_deps={
        "_integ_cumulated_invest_e_grid": {
            "initial": {},
            "step": {"extra_monet_invest_to_cope_with_variable_elec_res": 1},
        }
    },
)
def cumulated_invest_e_grid():
    """
    Cumulated monetary investment for developing electricity grids to integrate renewable intermittent sources.
    """
    return _integ_cumulated_invest_e_grid()


_integ_cumulated_invest_e_grid = Integ(
    lambda: extra_monet_invest_to_cope_with_variable_elec_res(),
    lambda: 0,
    "_integ_cumulated_invest_e_grid",
)


@component.add(
    name="Cumulated_total_monet_invest_RES_for_Elec",
    units="Tdollars",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_total_monet_invest_res_for_elec": 1},
    other_deps={
        "_integ_cumulated_total_monet_invest_res_for_elec": {
            "initial": {},
            "step": {"total_monet_invest_res_for_elec_tdolar": 1},
        }
    },
)
def cumulated_total_monet_invest_res_for_elec():
    """
    Cumulated total monetary investment in RES for electricity generation from 1995 (1995 US$).
    """
    return _integ_cumulated_total_monet_invest_res_for_elec()


_integ_cumulated_total_monet_invest_res_for_elec = Integ(
    lambda: total_monet_invest_res_for_elec_tdolar(),
    lambda: 0,
    "_integ_cumulated_total_monet_invest_res_for_elec",
)


@component.add(
    name="extra_monet_invest_to_cope_with_variable_Elec_RES",
    units="Tdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_generation_res_elec_twh": 2,
        "balancing_costs": 1,
        "grid_reinforcement_costs_tdollar": 1,
    },
)
def extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Annual additional monetary investment to cope with the intermittency of RES (taking wind as a proxy) including balancing and grid reinforcement costs (1995 US$).
    """
    return (
        float(real_generation_res_elec_twh().loc["wind_onshore"])
        + float(real_generation_res_elec_twh().loc["wind_offshore"])
    ) * balancing_costs() + grid_reinforcement_costs_tdollar()


@component.add(
    name="Grid_reinforcement_costs",
    units="dollars/kW",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_grid_reinforcement_costs"},
)
def grid_reinforcement_costs():
    """
    Grid reinforcement costs. We take the median from the study of Mills et al (2012) for wind: 300 $/kW (238.33 US1995$).
    """
    return _ext_constant_grid_reinforcement_costs()


_ext_constant_grid_reinforcement_costs = ExtConstant(
    "../energy.xlsx",
    "Global",
    "grid_reinforcement_costs",
    {},
    _root,
    {},
    "_ext_constant_grid_reinforcement_costs",
)


@component.add(
    name="Grid_reinforcement_costs_Tdollar",
    units="Tdollar/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grid_reinforcement_costs": 1,
        "kw_per_tw": 1,
        "new_capacity_installed_onshore_wind_tw": 1,
        "nvs_to_t": 1,
    },
)
def grid_reinforcement_costs_tdollar():
    """
    1995 US$.
    """
    return (
        grid_reinforcement_costs()
        * kw_per_tw()
        * new_capacity_installed_onshore_wind_tw()
        / nvs_to_t()
    )


@component.add(
    name="invest_cost_RES_elec",
    units="T$/TW",
    subscripts=[np.str_("RES_elec")],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_invest_cost_res_elec",
        "__data__": "_ext_data_invest_cost_res_elec",
        "time": 1,
    },
)
def invest_cost_res_elec():
    """
    Input assumption on installation cost of new RES capacity for electricity.
    """
    return _ext_data_invest_cost_res_elec(time())


_ext_data_invest_cost_res_elec = ExtData(
    "../energy.xlsx",
    "Global",
    "Time",
    "invest_cost_res_elec",
    "interpolate",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_data_invest_cost_res_elec",
)


@component.add(
    name="invest_RES_elec",
    units="T$/year",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_capacity_under_construction_tw": 1,
        "invest_cost_res_elec": 1,
    },
)
def invest_res_elec():
    return res_elec_capacity_under_construction_tw() * invest_cost_res_elec()


@component.add(
    name="new_capacity_installed_onshore_wind_TW",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_res_installed_capacity": 1},
)
def new_capacity_installed_onshore_wind_tw():
    return float(new_res_installed_capacity().loc["wind_onshore"])


@component.add(
    name='"$_to_T$"', units="$/T$", comp_type="Constant", comp_subtype="Normal"
)
def nvs_to_t():
    return 1000000000000.0


@component.add(
    name="Percent_tot_monet_invest_RESelec_vs_GDP",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_tot_monet_invest_elec_res_vs_gdp": 1},
)
def percent_tot_monet_invest_reselec_vs_gdp():
    """
    Annual total monetary investment for RES for electricity as a share of the annual GDP ( in percentage ).
    """
    return share_tot_monet_invest_elec_res_vs_gdp() * 100


@component.add(
    name="share_extra_monet_invest_to_cope_with_variable_Elec_RES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extra_monet_invest_to_cope_with_variable_elec_res": 1,
        "total_monet_invest_res_for_elec_tdolar": 1,
    },
)
def share_extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Share of the anual additional monetary investment to cope with the intermittency of RES (taking wind as a proxy) in relation to the total investment for RES.
    """
    return (
        extra_monet_invest_to_cope_with_variable_elec_res()
        / total_monet_invest_res_for_elec_tdolar()
    )


@component.add(
    name="share_tot_monet_invest_Elec_RES_vs_GDP",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_monet_invest_res_for_elec_tdolar": 1,
        "nvs_1_year": 1,
        "gdp_cat": 1,
    },
)
def share_tot_monet_invest_elec_res_vs_gdp():
    """
    Annual total monetary investment for RES for electricity as a share of the annual GDP.
    """
    return zidz(total_monet_invest_res_for_elec_tdolar(), gdp_cat() / nvs_1_year())


@component.add(
    name="Total_monet_invest_RES_for_elec_Tdolar",
    units="Tdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "invest_res_elec": 1,
        "extra_monet_invest_to_cope_with_variable_elec_res": 1,
    },
)
def total_monet_invest_res_for_elec_tdolar():
    """
    Annual total monetary investment for RES for electricity: capacity, balancing costs and grid improvements to cope with variability (1995 US$).
    """
    return (
        sum(
            invest_res_elec().rename({np.str_("RES_elec"): "RES_elec!"}),
            dim=["RES_elec!"],
        )
        + extra_monet_invest_to_cope_with_variable_elec_res()
    )


@component.add(
    name="TWh_to_MWh", units="MWh/TWh", comp_type="Constant", comp_subtype="Normal"
)
def twh_to_mwh():
    return 1000000.0
