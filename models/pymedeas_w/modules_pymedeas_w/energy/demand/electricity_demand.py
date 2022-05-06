"""
Module electricity_demand
Translated using PySD version 3.0.0-dev
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
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_twh": 1, "share_transmdistr_elec_losses": 1},
)
def electrical_distribution_losses_twh():
    """
    Electrical transmission and distribution losses.
    """
    return total_fe_elec_demand_twh() * share_transmdistr_elec_losses()


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
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def fe_elec_demand_consum_ej():
    """
    Electricity consumption (EJ)
    """
    return float(required_fed_by_fuel().loc["electricity"])


@component.add(
    name='"Max share transm&distr elec losses"',
    units="Dnml",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_transmdistr_elec_losses_initial": 1},
)
def max_share_transmdistr_elec_losses():
    """
    Assumed maximum share of transmission and distribution electric losses (when RES supply 100% of the total consumption).
    """
    return share_transmdistr_elec_losses_initial() * (
        1 + 0.0115 * np.exp(4.2297 * 1) - 0.00251
    )


@component.add(
    name='"remaining share transm&distr elec losses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_share_transmdistr_elec_losses": 2,
        "share_transmdistr_elec_losses": 1,
    },
)
def remaining_share_transmdistr_elec_losses():
    """
    Remaining share in relation to the assumed maximum transmission and distribution losses.
    """
    return (
        max_share_transmdistr_elec_losses() - share_transmdistr_elec_losses()
    ) / max_share_transmdistr_elec_losses()


@component.add(
    name='"share transm&distr elec losses initial"',
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
    "../energy.xlsx",
    "Global",
    "share_transm_and_distribution_elec_losses_initial",
    {},
    _root,
    {},
    "_ext_constant_share_transmdistr_elec_losses_initial",
)


@component.add(
    name='"share transm&distr elec losses"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_share_transmdistr_elec_losses": 1},
    other_deps={
        "_integ_share_transmdistr_elec_losses": {
            "initial": {"share_transmdistr_elec_losses_initial": 1},
            "step": {"variation_share_transmdistr_elec_losses": 1},
        }
    },
)
def share_transmdistr_elec_losses():
    """
    Evolution over time of the share of transmission and distribution losses of electricity. It is assumed that these losses increase over time as the share of RES increase in the electricity mix.
    """
    return _integ_share_transmdistr_elec_losses()


_integ_share_transmdistr_elec_losses = Integ(
    lambda: variation_share_transmdistr_elec_losses(),
    lambda: share_transmdistr_elec_losses_initial(),
    "_integ_share_transmdistr_elec_losses",
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
    depends_on={"fe_demand_elec_consum_twh": 1, "share_transmdistr_elec_losses": 1},
)
def total_fe_elec_demand_twh():
    """
    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses.
    """
    return fe_demand_elec_consum_twh() * (1 + share_transmdistr_elec_losses())


@component.add(
    name='"variation share transm&distr elec losses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_share_transmdistr_losses_elec": 1,
        "remaining_share_transmdistr_elec_losses": 1,
    },
)
def variation_share_transmdistr_elec_losses():
    """
    Annual variation of the share of transmission and distribution losses of electricity.
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: variation_share_transmdistr_losses_elec()
        * remaining_share_transmdistr_elec_losses(),
    )


@component.add(
    name='"variation share transm&distr losses elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_transmdistr_elec_losses_initial": 1,
        "share_res_electricity_generation": 1,
    },
)
def variation_share_transmdistr_losses_elec():
    """
    Relationship between transmission and distribution losses of electricity and the penetration of RES in the electricity mix. Source: NREL (2012).
    """
    return share_transmdistr_elec_losses_initial() * (
        0.0115 * np.exp(4.2297 * share_res_electricity_generation()) - 0.00251
    )
