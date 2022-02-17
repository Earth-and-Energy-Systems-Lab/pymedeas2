"""
Module res_elec_total_monetary_investment
Translated using PySD version 2.2.1
"""


def balancing_costs():
    """
    Real Name: Balancing costs
    Original Eqn: (Balancing costs ref(Share variable RES elec generation vs total))/M per T
    Units: Tdollars/TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Balancing costs (1995T$ / TWh produced).
    """
    return (
        balancing_costs_ref(share_variable_res_elec_generation_vs_total())
    ) / m_per_t()


def balancing_costs_ref(x):
    """
    Real Name: Balancing costs ref
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Global', 'share_of_variable_res', 'balancing_cost'))
    Units: dollars/MWh
    Limits: (None, None)
    Type: lookup
    Subs: None

    Balancing costs adapting data from Holttinen et al (2011).
    """
    return _ext_lookup_balancing_costs_ref(x)


def cumulated_invest_e_grid():
    """
    Real Name: cumulated invest E grid
    Original Eqn: INTEG ( extra monet invest to cope with variable Elec RES, 0)
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated monetary investment for developing electricity grids to
        integrate renewable intermittent sources.
    """
    return _integ_cumulated_invest_e_grid()


def cumulated_total_monet_invest_res_for_elec():
    """
    Real Name: Cumulated total monet invest RES for Elec
    Original Eqn: INTEG ( Total monet invest RES for elec Tdolar, 0)
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated total monetary investment in RES for electricity generation from
        1995 (1995 US$).
    """
    return _integ_cumulated_total_monet_invest_res_for_elec()


def extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Real Name: extra monet invest to cope with variable Elec RES
    Original Eqn: (real generation RES elec TWh[wind onshore]+real generation RES elec TWh[wind offshore])*Balancing costs +Grid reinforcement costs Tdollar
    Units: Tdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual additional monetary investment to cope with the intermittency of
        RES (taking wind as a proxy) including balancing and grid reinforcement
        costs (1995 US$).
    """
    return (
        float(real_generation_res_elec_twh().loc["wind onshore"])
        + float(real_generation_res_elec_twh().loc["wind offshore"])
    ) * balancing_costs() + grid_reinforcement_costs_tdollar()


def gdollar_per_tdollar():
    """
    Real Name: Gdollar per Tdollar
    Original Eqn: 1000
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1000


def grid_reinforcement_costs():
    """
    Real Name: Grid reinforcement costs
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'grid_reinforcement_costs')
    Units: dollars/kW
    Limits: (None, None)
    Type: constant
    Subs: None

    Grid reinforcement costs. We take the median from the study of Mills et al
        (2012) for wind: 300 $/kW (238.33 US1995$).
    """
    return _ext_constant_grid_reinforcement_costs()


def grid_reinforcement_costs_tdollar():
    """
    Real Name: Grid reinforcement costs Tdollar
    Original Eqn: Grid reinforcement costs*new capacity installed onshore wind TW/Gdollar per Tdollar
    Units: Tdollar
    Limits: (None, None)
    Type: component
    Subs: None

    1995 US$.
    """
    return (
        grid_reinforcement_costs()
        * new_capacity_installed_onshore_wind_tw()
        / gdollar_per_tdollar()
    )


@subs(["RES elec"], _subscript_dict)
def invest_cost_res_elec():
    """
    Real Name: invest cost RES elec
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Global', 'Time', 'invest_cost_res_elec')
    Units: T$/TW
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RES elec']

    Input assumption on installation cost of new RES capacity for electricity.
    """
    return _ext_data_invest_cost_res_elec(time())


@subs(["RES elec"], _subscript_dict)
def invest_res_elec_tdolar():
    """
    Real Name: invest RES elec Tdolar
    Original Eqn: RES elec capacity under construction TW[RES elec]*invest cost RES elec[RES elec]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return res_elec_capacity_under_construction_tw() * invest_cost_res_elec()


def new_capacity_installed_onshore_wind_tw():
    """
    Real Name: new capacity installed onshore wind TW
    Original Eqn: new RES elec capacity under planning[wind onshore]
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(new_res_elec_capacity_under_planning().loc["wind onshore"])


def percent_tot_monet_invest_reselec_vs_gdp():
    """
    Real Name: Percent tot monet invest RESelec vs GDP
    Original Eqn: share tot monet invest Elec RES vs GDP*100
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Annual total monetary investment for RES for electricity as a share of the
        annual GDP ( in percentage ).
    """
    return share_tot_monet_invest_elec_res_vs_gdp() * 100


def share_extra_monet_invest_to_cope_with_variable_elec_res():
    """
    Real Name: share extra monet invest to cope with variable Elec RES
    Original Eqn: extra monet invest to cope with variable Elec RES/Total monet invest RES for elec Tdolar
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Share of the anual additional monetary investment to cope with the
        intermittency of RES (taking wind as a proxy) in relation to the total
        investment for RES.
    """
    return (
        extra_monet_invest_to_cope_with_variable_elec_res()
        / total_monet_invest_res_for_elec_tdolar()
    )


def share_tot_monet_invest_elec_res_vs_gdp():
    """
    Real Name: share tot monet invest Elec RES vs GDP
    Original Eqn: ZIDZ( Total monet invest RES for elec Tdolar, GDP )
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual total monetary investment for RES for electricity as a share of the
        annual GDP.
    """
    return zidz(total_monet_invest_res_for_elec_tdolar(), gdp())


def total_monet_invest_res_for_elec_tdolar():
    """
    Real Name: Total monet invest RES for elec Tdolar
    Original Eqn: SUM(invest RES elec Tdolar[RES elec!])+extra monet invest to cope with variable Elec RES
    Units: Tdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual total monetary investment for RES for electricity: capacity,
        balancing costs and grid improvements to cope with variability (1995 US$).
    """
    return (
        sum(invest_res_elec_tdolar(), dim=("RES elec",))
        + extra_monet_invest_to_cope_with_variable_elec_res()
    )


_ext_lookup_balancing_costs_ref = ExtLookup(
    "../energy.xlsx",
    "Global",
    "share_of_variable_res",
    "balancing_cost",
    {},
    _root,
    "_ext_lookup_balancing_costs_ref",
)


_integ_cumulated_invest_e_grid = Integ(
    lambda: extra_monet_invest_to_cope_with_variable_elec_res(),
    lambda: 0,
    "_integ_cumulated_invest_e_grid",
)


_integ_cumulated_total_monet_invest_res_for_elec = Integ(
    lambda: total_monet_invest_res_for_elec_tdolar(),
    lambda: 0,
    "_integ_cumulated_total_monet_invest_res_for_elec",
)


_ext_constant_grid_reinforcement_costs = ExtConstant(
    "../energy.xlsx",
    "Global",
    "grid_reinforcement_costs",
    {},
    _root,
    "_ext_constant_grid_reinforcement_costs",
)


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
