"""
Module electricity_demand_ee
Translated using PySD version 2.1.0
"""


def ej_per_twh():
    """
    Real Name: EJ per TWh
    Original Eqn: 0.0036
    Units: EJ/TWh
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion (3.6 EJ=1000 TWh)
    """
    return 0.0036


def electrical_distribution_losses_ej():
    """
    Real Name: Electrical distribution losses EJ
    Original Eqn: Electrical distribution losses TWh*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electical distribution losses (EJ)
    """
    return electrical_distribution_losses_twh() * ej_per_twh()


def electrical_distribution_losses_twh():
    """
    Real Name: Electrical distribution losses TWh
    Original Eqn: Total FE Elec demand TWh*"share transm&distr elec losses"
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Electrical transmission and distribution losses.
    """
    return total_fe_elec_demand_twh() * share_transmdistr_elec_losses()


def fe_demand_elec_consum_twh():
    """
    Real Name: FE demand Elec consum TWh
    Original Eqn: Required FED by fuel[electricity]/EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity consumption (TWh)
    """
    return float(required_fed_by_fuel().loc["electricity"]) / ej_per_twh()


def max_share_transmdistr_elec_losses():
    """
    Real Name: "Max share transm&distr elec losses"
    Original Eqn: "share transm&distr elec losses initial"*(1+0.0115*EXP(4.2297*1)-0.00251)
    Units: Dnml
    Limits: (None, None)
    Type: component
    Subs: None

    Assumed maximum share of transmission and distribution electric losses
        (when RES supply 100% of the total consumption).
    """
    return share_transmdistr_elec_losses_initial() * (
        1 + 0.0115 * np.exp(4.2297 * 1) - 0.00251
    )


def remaining_share_transmdistr_elec_losses():
    """
    Real Name: "remaining share transm&distr elec losses"
    Original Eqn: ("Max share transm&distr elec losses"-"share transm&distr elec losses")/"Max share transm&distr elec losses"
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining share in relation to the assumed maximum transmission and
        distribution losses.
    """
    return (
        max_share_transmdistr_elec_losses() - share_transmdistr_elec_losses()
    ) / max_share_transmdistr_elec_losses()


def share_transmdistr_elec_losses_initial():
    """
    Real Name: "share transm&distr elec losses initial"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'share_transm_and_distribution_elec_losses_initial')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Current share of electrical transmission and distribution losses in
        relation to electricity consumption. We define these losses at around 9.5%
        following historical data.
    """
    return _ext_constant_share_transmdistr_elec_losses_initial()


def share_transmdistr_elec_losses():
    """
    Real Name: "share transm&distr elec losses"
    Original Eqn: INTEG ( "variation share transm&distr elec losses", "share transm&distr elec losses initial")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Evolution over time of the share of transmission and distribution losses
        of electricity. It is assumed that these losses increase over time as the
        share of RES increase in the electricity mix.
    """
    return _integ_share_transmdistr_elec_losses()


def total_fe_elec_demand_ej():
    """
    Real Name: Total FE Elec demand EJ
    Original Eqn: Total FE Elec demand TWh*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity demand generation (final energy, includes distribution losses).
    """
    return total_fe_elec_demand_twh() * ej_per_twh()


def total_fe_elec_demand_twh():
    """
    Real Name: Total FE Elec demand TWh
    Original Eqn: (FE demand Elec consum TWh)*(1+"share transm&distr elec losses" )
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy electricity demand (TWh). It includes new electric uses
        (e.g. EV & HEV) and electrical transmission and distribution losses.
    """
    return (fe_demand_elec_consum_twh()) * (1 + share_transmdistr_elec_losses())


def variation_share_transmdistr_elec_losses():
    """
    Real Name: "variation share transm&distr elec losses"
    Original Eqn: IF THEN ELSE(Time<2015, 0, "variation share transm&distr losses elec"*"remaining share transm&distr elec losses")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual variation of the share of transmission and distribution losses of
        electricity.
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: variation_share_transmdistr_losses_elec()
        * remaining_share_transmdistr_elec_losses(),
    )


def variation_share_transmdistr_losses_elec():
    """
    Real Name: "variation share transm&distr losses elec"
    Original Eqn: "share transm&distr elec losses initial"*(0.0115*EXP(4.2297*share RES electricity generation)-0.00251)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Relationship between transmission and distribution losses of electricity
        and the penetration of RES in the electricity mix. Source: NREL (2012).
    """
    return share_transmdistr_elec_losses_initial() * (
        0.0115 * np.exp(4.2297 * share_res_electricity_generation()) - 0.00251
    )


_ext_constant_share_transmdistr_elec_losses_initial = ExtConstant(
    "../energy.xlsx",
    "Global",
    "share_transm_and_distribution_elec_losses_initial",
    {},
    _root,
    "_ext_constant_share_transmdistr_elec_losses_initial",
)


_integ_share_transmdistr_elec_losses = Integ(
    lambda: variation_share_transmdistr_elec_losses(),
    lambda: share_transmdistr_elec_losses_initial(),
    "_integ_share_transmdistr_elec_losses",
)
