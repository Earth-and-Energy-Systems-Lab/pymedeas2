"""
Module res_elec_total_monetary_investment
Translated using PySD version 2.2.1
"""


def balancing_costs():
    """
    Real Name: Balancing costs
    Original Eqn:
    Units: Tdollars/TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Balancing costs (1995T$ / TWh produced).
    """
    return (
        balancing_costs_ref(share_variable_res_elec_generation_vs_total()) / m_per_t()
    )


def balancing_costs_ref(x):
    """
    Real Name: Balancing costs ref
    Original Eqn:
    Units: dollars/MWh
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Balancing costs adapting data from Holttinen et al (2011).
    """
    return _ext_lookup_balancing_costs_ref(x)


_ext_lookup_balancing_costs_ref = ExtLookup(
    "../energy.xlsx",
    "Global",
    "share_of_variable_res",
    "balancing_cost",
    {},
    _root,
    "_ext_lookup_balancing_costs_ref",
)


def cumulated_invest_e_grid():
    """
    Real Name: cumulated invest E grid
    Original Eqn:
    Units: Tdollars
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated monetary investment for developing electricity grids to integrate renewable intermittent sources.
    """
    return _integ_cumulated_invest_e_grid()


_integ_cumulated_invest_e_grid = Integ(
    lambda: extra_monet_invest_to_cope_with_variable_elec_res(),
    lambda: 0,
    "_integ_cumulated_invest_e_grid",
)


def cumulated_total_monet_invest_res_for_elec():
    """
    Real Name: Cumulated total monet invest RES for Elec
    Original Eqn:
    Units: Tdollars
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated total monetary investment in RES for electricity generation from 1995 (1995 US$).
    """
    return _integ_cumulated_total_monet_invest_res_for_elec()


_integ_cumulated_total_monet_invest_res_for_elec = Integ(
    lambda: total_monet_invest_res_for_elec_tdolar(),
    lambda: 0,
    "_integ_cumulated_total_monet_invest_res_for_elec",
)


def extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Real Name: extra monet invest to cope with variable Elec RES
    Original Eqn:
    Units: Tdollars/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual additional monetary investment to cope with the intermittency of RES (taking wind as a proxy) including balancing and grid reinforcement costs (1995 US$).
    """
    return (
        float(real_generation_res_elec_twh().loc["wind onshore"])
        + float(real_generation_res_elec_twh().loc["wind offshore"])
    ) * balancing_costs() + grid_reinforcement_costs_tdollar()


def g_per_t():
    """
    Real Name: G per T
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 1000


def grid_reinforcement_costs():
    """
    Real Name: Grid reinforcement costs
    Original Eqn:
    Units: dollars/kW
    Limits: (None, None)
    Type: Constant
    Subs: []

    Grid reinforcement costs. We take the median from the study of Mills et al (2012) for wind: 300 $/kW (238.33 US1995$).
    """
    return _ext_constant_grid_reinforcement_costs()


_ext_constant_grid_reinforcement_costs = ExtConstant(
    "../energy.xlsx",
    "Global",
    "grid_reinforcement_costs",
    {},
    _root,
    "_ext_constant_grid_reinforcement_costs",
)


def grid_reinforcement_costs_tdollar():
    """
    Real Name: Grid reinforcement costs Tdollar
    Original Eqn:
    Units: Tdollar
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    1995 US$.
    """
    return (
        grid_reinforcement_costs()
        * new_capacity_installed_onshore_wind_tw()
        / g_per_t()
    )


@subs(["RES elec"], _subscript_dict)
def invest_cost_res_elec():
    """
    Real Name: invest cost RES elec
    Original Eqn:
    Units: T$/TW
    Limits: (None, None)
    Type: Data
    Subs: ['RES elec']

    Input assumption on installation cost of new RES capacity for electricity.
    """
    return _ext_data_invest_cost_res_elec(time())


_ext_data_invest_cost_res_elec = ExtData(
    "../energy.xlsx",
    "Global",
    "Time",
    "invest_cost_res_elec",
    "interpolate",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_data_invest_cost_res_elec",
)


@subs(["RES elec"], _subscript_dict)
def invest_res_elec_tdolar():
    """
    Real Name: invest RES elec Tdolar
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']


    """
    return res_elec_capacity_under_construction_tw() * invest_cost_res_elec()


def new_capacity_installed_onshore_wind_tw():
    """
    Real Name: new capacity installed onshore wind TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return float(new_res_elec_capacity_under_planning().loc["wind onshore"])


def percent_tot_monet_invest_reselec_vs_gdp():
    """
    Real Name: Percent tot monet invest RESelec vs GDP
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual total monetary investment for RES for electricity as a share of the annual GDP ( in percentage ).
    """
    return share_tot_monet_invest_elec_res_vs_gdp() * 100


def share_extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Real Name: share extra monet invest to cope with variable Elec RES
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of the anual additional monetary investment to cope with the intermittency of RES (taking wind as a proxy) in relation to the total investment for RES.
    """
    return (
        extra_monet_invest_to_cope_with_variable_elec_res()
        / total_monet_invest_res_for_elec_tdolar()
    )


def share_tot_monet_invest_elec_res_vs_gdp():
    """
    Real Name: share tot monet invest Elec RES vs GDP
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual total monetary investment for RES for electricity as a share of the annual GDP.
    """
    return zidz(total_monet_invest_res_for_elec_tdolar(), gdp_aut())


def total_monet_invest_res_for_elec_tdolar():
    """
    Real Name: Total monet invest RES for elec Tdolar
    Original Eqn:
    Units: Tdollars/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual total monetary investment for RES for electricity: capacity, balancing costs and grid improvements to cope with variability (1995 US$).
    """
    return (
        sum(
            invest_res_elec_tdolar().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + extra_monet_invest_to_cope_with_variable_elec_res()
    )
