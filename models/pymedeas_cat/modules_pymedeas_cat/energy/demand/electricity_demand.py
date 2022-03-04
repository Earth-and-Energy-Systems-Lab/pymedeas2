"""
Module electricity_demand
Translated using PySD version 2.2.1
"""


def ej_per_twh():
    """
    Real Name: EJ per TWh
    Original Eqn:
    Units: EJ/TWh
    Limits: (None, None)
    Type: Constant
    Subs: []

    Unit conversion (3.6 EJ=1000 TWh)
    """
    return 0.0036


def elec_exports_share():
    """
    Real Name: Elec exports share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of electricity generated with the aim of exporting
    """
    return if_then_else(
        time() < 2015, lambda: hist_elec_exports_share(), lambda: p_export_share()
    )


def electrical_distribution_losses_ej():
    """
    Real Name: Electrical distribution losses EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electical distribution losses (EJ)
    """
    return electrical_distribution_losses_twh() * ej_per_twh()


def electrical_distribution_losses_twh():
    """
    Real Name: Electrical distribution losses TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electrical transmission and distribution losses.
    """
    return total_fe_elec_demand_twh() * share_transmdistr_elec_losses()


def fe_demand_elec_consum_twh():
    """
    Real Name: FE demand Elec consum TWh
    Original Eqn:
    Units: TWh/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity consumption (TWh)
    """
    return float(required_fed_by_fuel().loc["electricity"]) / ej_per_twh()


def fe_elec_demand_exports_twh():
    """
    Real Name: FE Elec demand exports TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Overdemand generated with the aim of exporting.
    """
    return total_fe_elec_demand_twh() * elec_exports_share()


def hist_elec_exports_share():
    """
    Real Name: Hist Elec exports share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []

    Historic exports share vs Elec generation
    """
    return _ext_data_hist_elec_exports_share(time())


_ext_data_hist_elec_exports_share = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_of_electricty_exports_of_total_electricity_production",
    "interpolate",
    {},
    _root,
    "_ext_data_hist_elec_exports_share",
)


def max_share_transmdistr_elec_losses():
    """
    Real Name: "Max share transm&distr elec losses"
    Original Eqn:
    Units: Dnml
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Assumed maximum share of transmission and distribution electric losses (when RES supply 100% of the total consumption).
    """
    return share_transmdistr_elec_losses_initial() * (
        1 + 0.0115 * np.exp(4.2297 * 1) - 0.00251
    )


def p_export_share():
    """
    Real Name: P export share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of electricity generated with the aim of exporting
    """
    return -0.1


def remaining_share_transmdistr_elec_losses():
    """
    Real Name: "remaining share transm&distr elec losses"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining share in relation to the assumed maximum transmission and distribution losses.
    """
    return (
        max_share_transmdistr_elec_losses() - share_transmdistr_elec_losses()
    ) / max_share_transmdistr_elec_losses()


def share_transmdistr_elec_losses_initial():
    """
    Real Name: "share transm&distr elec losses initial"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current share of electrical transmission and distribution losses in relation to electricity consumption. We define these losses at around 9.5% following historical data.
    """
    return _ext_constant_share_transmdistr_elec_losses_initial()


_ext_constant_share_transmdistr_elec_losses_initial = ExtConstant(
    "../energy.xlsx",
    "Global",
    "share_transm_and_distribution_elec_losses_initial",
    {},
    _root,
    "_ext_constant_share_transmdistr_elec_losses_initial",
)


def share_transmdistr_elec_losses():
    """
    Real Name: "share transm&distr elec losses"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Evolution over time of the share of transmission and distribution losses of electricity. It is assumed that these losses increase over time as the share of RES increase in the electricity mix.
    """
    return _integ_share_transmdistr_elec_losses()


_integ_share_transmdistr_elec_losses = Integ(
    lambda: variation_share_transmdistr_elec_losses(),
    lambda: share_transmdistr_elec_losses_initial(),
    "_integ_share_transmdistr_elec_losses",
)


def total_fe_elec_demand_ej():
    """
    Real Name: Total FE Elec demand EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity demand generation (final energy, includes distribution losses).
    """
    return total_fe_elec_demand_twh() * ej_per_twh()


def total_fe_elec_demand_twh():
    """
    Real Name: Total FE Elec demand TWh
    Original Eqn:
    Units: TWh/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses.
    """
    return (
        fe_demand_elec_consum_twh()
        * (1 + share_transmdistr_elec_losses())
        / (1 - elec_exports_share())
    )


def variation_share_transmdistr_elec_losses():
    """
    Real Name: "variation share transm&distr elec losses"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual variation of the share of transmission and distribution losses of electricity.
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Relationship between transmission and distribution losses of electricity and the penetration of RES in the electricity mix. Source: NREL (2012).
    """
    return share_transmdistr_elec_losses_initial() * (
        0.0115 * np.exp(4.2297 * share_res_electricity_generation()) - 0.00251
    )
