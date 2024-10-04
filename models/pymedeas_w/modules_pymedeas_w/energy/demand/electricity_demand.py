"""
Module energy.demand.electricity_demand
Translated using PySD version 3.14.0
"""

@component.add(
    name="EJ per TWh", units="EJ/TWh", comp_type="Constant", comp_subtype="Normal"
)
def ej_per_twh():
    """
    Unit conversion (3.6 EJ=1000 TWh)
    """
    return 0.0036


@component.add(
    name="Electrical distribution losses EJ",
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
    name="Electrical distribution losses TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_twh": 1,
        "time": 1,
        "share_trans_and_dist_losses": 1,
    },
)
def electrical_distribution_losses_twh():
    """
    Electrical transmission and distribution losses.
    """
    return total_fe_elec_demand_twh() * share_trans_and_dist_losses(time())


@component.add(
    name="FE demand Elec consum TWh",
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
    name="FE Elec demand consum EJ",
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
    name="share trans and dist losses",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_share_trans_and_dist_losses",
        "__lookup__": "_ext_lookup_share_trans_and_dist_losses",
    },
)
def share_trans_and_dist_losses(x, final_subs=None):
    return _ext_lookup_share_trans_and_dist_losses(x, final_subs)


_ext_lookup_share_trans_and_dist_losses = ExtLookup(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_trans_loss",
    {},
    _root,
    {},
    "_ext_lookup_share_trans_and_dist_losses",
)


@component.add(
    name="Total FE Elec demand EJ",
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
    name="Total FE Elec demand TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_elec_consum_twh": 1,
        "time": 1,
        "share_trans_and_dist_losses": 1,
    },
)
def total_fe_elec_demand_twh():
    """
    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses. (FE demand Elec consum TWh)*(1+"share transm&distr elec losses")
    """
    return fe_demand_elec_consum_twh() * (1 + share_trans_and_dist_losses(time()))
