"""
Module res_elec_total_monetary_investment
Translated using PySD version 2.2.0
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
    Original Eqn: (FE Elec generation from onshore wind TWh+FE Elec generation from offshore wind TWh)*Balancing costs +Grid reinforcement costs Tdollar
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual additional monetary investment to cope with the intermittency of
        RES (taking wind as a proxy) including balancing and grid reinforcement
        costs (1995 US$).
    """
    return (
        fe_elec_generation_from_onshore_wind_twh()
        + fe_elec_generation_from_offshore_wind_twh()
    ) * balancing_costs() + grid_reinforcement_costs_tdollar()


def g_per_t():
    """
    Real Name: G per T
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
    Original Eqn: Grid reinforcement costs*new capacity installed onshore wind TW/G per T
    Units: Tdollar
    Limits: (None, None)
    Type: component
    Subs: None

    1995 US$.
    """
    return (
        grid_reinforcement_costs()
        * new_capacity_installed_onshore_wind_tw()
        / g_per_t()
    )


def invest_biow_tdolar():
    """
    Real Name: invest bioW Tdolar
    Original Eqn: invest RES elec Tdolar[solid bioE elec]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["solid bioE elec"])


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


def invest_csp_tdolar():
    """
    Real Name: invest CSP Tdolar
    Original Eqn: invest RES elec Tdolar[CSP]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["CSP"])


def invest_geotelec_tdolar():
    """
    Real Name: "invest geot-elec Tdolar"
    Original Eqn: invest RES elec Tdolar[geot elec]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["geot elec"])


def invest_hydro_tdolar():
    """
    Real Name: invest hydro Tdolar
    Original Eqn: invest RES elec Tdolar[hydro]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["hydro"])


def invest_oceanic_tdolar():
    """
    Real Name: invest oceanic Tdolar
    Original Eqn: invest RES elec Tdolar[oceanic]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["oceanic"])


def invest_offshore_wind_tdolar():
    """
    Real Name: invest offshore wind Tdolar
    Original Eqn: invest RES elec Tdolar[wind offshore]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["wind offshore"])


def invest_onshore_wind_tdolar():
    """
    Real Name: invest onshore wind Tdolar
    Original Eqn: invest RES elec Tdolar[wind onshore]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["wind onshore"])


@subs(["RES elec"], _subscript_dict)
def invest_res_elec_tdolar():
    """
    Real Name: invest RES elec Tdolar
    Original Eqn: MAX(0, RES elec capacity under construction TW[RES elec]*invest cost RES elec[RES elec])
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return np.maximum(
        0, res_elec_capacity_under_construction_tw() * invest_cost_res_elec()
    )


def invest_res_for_elec():
    """
    Real Name: Invest RES for Elec
    Original Eqn: MAX(invest bioW Tdolar+"invest geot-elec Tdolar"+invest hydro Tdolar+invest oceanic Tdolar+invest solar Tdolar+invest onshore wind Tdolar+invest offshore wind Tdolar+invest CSP Tdolar, 0)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual investment for the installation of RES capacity for electricity .
    """
    return np.maximum(
        invest_biow_tdolar()
        + invest_geotelec_tdolar()
        + invest_hydro_tdolar()
        + invest_oceanic_tdolar()
        + invest_solar_tdolar()
        + invest_onshore_wind_tdolar()
        + invest_offshore_wind_tdolar()
        + invest_csp_tdolar(),
        0,
    )


def invest_solar_tdolar():
    """
    Real Name: invest solar Tdolar
    Original Eqn: invest RES elec Tdolar[solar PV]
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Investment costs.
    """
    return float(invest_res_elec_tdolar().loc["solar PV"])


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
    Original Eqn: ZIDZ( Total monet invest RES for elec Tdolar, GDP EU )
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual total monetary investment for RES for electricity as a share of the
        annual GDP.
    """
    return zidz(total_monet_invest_res_for_elec_tdolar(), gdp_eu())


def total_monet_invest_res_for_elec_tdolar():
    """
    Real Name: Total monet invest RES for elec Tdolar
    Original Eqn: Invest RES for Elec+extra monet invest to cope with variable Elec RES
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual total monetary investment for RES for electricity: capacity,
        balancing costs and grid improvements to cope with variability (1995 US$).
    """
    return invest_res_for_elec() + extra_monet_invest_to_cope_with_variable_elec_res()


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
