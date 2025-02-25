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
    depends_on={"fe_elec_demand_consum_ej": 1, "ej_per_twh": 1},
)
def fe_demand_elec_consum_twh():
    """
    Electricity consumption (TWh)
    """
    return fe_elec_demand_consum_ej() / ej_per_twh()


@component.add(
    name="FE_Elec_demand_consum_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1, "total_electricity_demand_for_synthetic": 1},
)
def fe_elec_demand_consum_ej():
    """
    Electricity consumption (EJ) including the electricity for synthetic fuels and hydrogen
    """
    return (
        float(required_fed_by_fuel().loc["electricity"])
        + total_electricity_demand_for_synthetic()
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
    r"../../scenarios/scen_w.xlsx",
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
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_transmdistr_elec_losses_initial"},
)
def share_transmdistr_elec_losses_initial():
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
    depends_on={"fe_demand_elec_consum_twh": 1, "share_trans_and_dist_losses": 1},
)
def total_fe_elec_demand_twh():
    """
    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses. (FE demand Elec consum TWh)*(1+"share transm&distr elec losses")
    """
    return fe_demand_elec_consum_twh() * (1 + share_trans_and_dist_losses())
