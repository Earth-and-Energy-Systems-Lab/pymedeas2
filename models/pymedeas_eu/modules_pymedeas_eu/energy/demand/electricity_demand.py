"""
Module energy.demand.electricity_demand
Translated using PySD version 3.14.2
"""

@component.add(
    name="EJ_per_TWh", units="EJ/TWh", comp_type="Constant", comp_subtype="Normal"
)
def ej_per_twh():
    """
    Unit conversion (3.6 EJ=1000 TWh)
    """
    return 0.0036


@component.add(
    name="Elec_exports_share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "hist_elec_exports_share": 1, "p_export_share": 1},
)
def elec_exports_share():
    """
    Share of electricity exports
    """
    return if_then_else(
        time() < 2015, lambda: hist_elec_exports_share(), lambda: p_export_share()
    )


@component.add(
    name="Electrical_distribution_losses_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electrical_distribution_losses_twh": 1, "ej_per_twh": 1},
)
def electrical_distribution_losses_ej():
    """
    Electical distribution losses (EJ)
    """
    return electrical_distribution_losses_twh() * ej_per_twh()


@component.add(
    name="Electrical_distribution_losses_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_twh": 1, "share_trans_and_dist_losses": 1},
)
def electrical_distribution_losses_twh():
    """
    Electrical transmission and distribution losses.
    """
    return total_fe_elec_demand_twh() * share_trans_and_dist_losses()


@component.add(
    name="FE_demand_Elec_consum_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1, "ej_per_twh": 1},
)
def fe_demand_elec_consum_twh():
    """
    Electricity consumption (TWh)
    """
    return float(required_fed_by_fuel().loc["electricity"]) / ej_per_twh()


@component.add(
    name="FE_Elec_demand_exports_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_twh": 1, "elec_exports_share": 1},
)
def fe_elec_demand_exports_twh():
    return total_fe_elec_demand_twh() * elec_exports_share()


@component.add(
    name="Hist_Elec_exports_share",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_hist_elec_exports_share",
        "__data__": "_ext_data_hist_elec_exports_share",
        "time": 1,
    },
)
def hist_elec_exports_share():
    return _ext_data_hist_elec_exports_share(time())


_ext_data_hist_elec_exports_share = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_electricty_exports_of_total_electricity_production",
    None,
    {},
    _root,
    {},
    "_ext_data_hist_elec_exports_share",
)


@component.add(
    name="P_export_share",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_p_export_share",
        "__data__": "_ext_data_p_export_share",
        "time": 1,
    },
)
def p_export_share():
    return _ext_data_p_export_share(time())


_ext_data_p_export_share = ExtData(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_RES_power",
    "share_exports_electricity",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_p_export_share",
)


@component.add(
    name="policy_share_trans_and_dist_losses",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_share_trans_and_dist_losses",
        "__lookup__": "_ext_lookup_policy_share_trans_and_dist_losses",
    },
)
def policy_share_trans_and_dist_losses(x, final_subs=None):
    return _ext_lookup_policy_share_trans_and_dist_losses(x, final_subs)


_ext_lookup_policy_share_trans_and_dist_losses = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_RES_power",
    "share_trans_loss",
    {},
    _root,
    {},
    "_ext_lookup_policy_share_trans_and_dist_losses",
)


@component.add(
    name="share_trans_and_dist_losses",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "share_transmdistr_elec_losses_initial": 3,
        "policy_share_trans_and_dist_losses": 2,
    },
)
def share_trans_and_dist_losses():
    return if_then_else(
        time() < 2015,
        lambda: share_transmdistr_elec_losses_initial(),
        lambda: if_then_else(
            time() < 2020,
            lambda: share_transmdistr_elec_losses_initial()
            + (
                policy_share_trans_and_dist_losses(time())
                - share_transmdistr_elec_losses_initial()
            )
            / 5
            * (time() - 2015),
            lambda: policy_share_trans_and_dist_losses(time()),
        ),
    )


@component.add(
    name='"share_transm&distr_elec_losses_initial"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_transmdistr_elec_losses_initial"},
)
def share_transmdistr_elec_losses_initial():
    """
    Current share of electrical transmission and distribution losses in relation to electricity consumption. We define these losses at around 9.5% following historical data.
    """
    return _ext_constant_share_transmdistr_elec_losses_initial()


_ext_constant_share_transmdistr_elec_losses_initial = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "share_transm_and_distribution_elec_losses_initial",
    {},
    _root,
    {},
    "_ext_constant_share_transmdistr_elec_losses_initial",
)


@component.add(
    name="Total_FE_Elec_demand_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_twh": 1, "ej_per_twh": 1},
)
def total_fe_elec_demand_ej():
    """
    Electricity demand generation (final energy, includes distribution losses).
    """
    return total_fe_elec_demand_twh() * ej_per_twh()


@component.add(
    name="Total_FE_Elec_demand_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_elec_consum_twh": 1,
        "share_trans_and_dist_losses": 1,
        "elec_exports_share": 1,
        "ej_per_twh": 1,
        "total_electricity_demand_for_synthetic": 1,
    },
)
def total_fe_elec_demand_twh():
    """
    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses.
    """
    return (
        fe_demand_elec_consum_twh()
        * (1 + share_trans_and_dist_losses())
        / (1 - elec_exports_share())
        + total_electricity_demand_for_synthetic() / ej_per_twh()
    )
