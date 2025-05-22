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
    Share of electricity generated with the aim of exporting
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
    depends_on={"fe_demand_elec_consum_twh": 1, "share_transmdistr_elec_losses": 1},
)
def electrical_distribution_losses_twh():
    """
    Electrical transmission and distribution losses.
    """
    return fe_demand_elec_consum_twh() * share_transmdistr_elec_losses()


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
    depends_on={"fe_demand_elec_consum_twh": 1, "elec_exports_share": 1},
)
def fe_elec_demand_exports_twh():
    """
    Overdemand generated with the aim of exporting.
    """
    return fe_demand_elec_consum_twh() * elec_exports_share()


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
    """
    Historic exports share vs Elec generation
    """
    return _ext_data_hist_elec_exports_share(time())


_ext_data_hist_elec_exports_share = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_of_electricty_exports_of_total_electricity_production",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_hist_elec_exports_share",
)


@component.add(
    name='"Max_share_transm&distr_elec_losses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_transmdistr_elec_losses_initial": 1},
)
def max_share_transmdistr_elec_losses():
    """
    Assumed maximum share of transmission and distribution electric losses (when RES supply 100% of the total consumption).
    """
    return share_transmdistr_elec_losses_initial() * (
        1 + 0.0115 * float(np.exp(4.2297 * 1)) - 0.00251
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
    """
    Share of electricity generated with the aim of exporting
    """
    return _ext_data_p_export_share(time())


_ext_data_p_export_share = ExtData(
    r"../../scenarios/scen_cat.xlsx",
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
    name='"remaining_share_transm&distr_elec_losses"',
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
    name='"share_transm&distr_elec_losses"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_share_transmdistr_elec_losses": 1},
    other_deps={
        "_integ_share_transmdistr_elec_losses": {
            "initial": {"share_transmdistr_elec_losses_initial": 1},
            "step": {},
        }
    },
)
def share_transmdistr_elec_losses():
    """
    Evolution over time of the share of transmission and distribution losses of electricity. It is assumed that these losses increase over time as the share of RES increase in the electricity mix.
    """
    return _integ_share_transmdistr_elec_losses()


_integ_share_transmdistr_elec_losses = Integ(
    lambda: 0,
    lambda: share_transmdistr_elec_losses_initial(),
    "_integ_share_transmdistr_elec_losses",
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
    name="test",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_electricity_demand_for_synthetic": 1,
        "ej_per_twh": 1,
        "electrical_distribution_losses_twh": 1,
        "fe_demand_elec_consum_twh": 1,
        "fe_elec_demand_exports_twh": 1,
    },
)
def test():
    return (
        total_electricity_demand_for_synthetic() / ej_per_twh()
        + electrical_distribution_losses_twh()
        + fe_demand_elec_consum_twh()
        + fe_elec_demand_exports_twh()
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
        "elec_exports_share": 1,
        "share_transmdistr_elec_losses": 1,
        "ej_per_twh": 1,
        "total_electricity_demand_for_synthetic": 1,
    },
)
def total_fe_elec_demand_twh():
    """
    Total final energy electricity demand (TWh). It includes new electric uses (e.g. EV & HEV) and electrical transmission and distribution losses. (FE_demand_Elec_consum_TWh)*(1+"share_transm&distr_elec_losses")/(1-Elec_exports_shar e )+Total_electricity_demand_for_synthetic/EJ_per_TWh
    """
    return (
        fe_demand_elec_consum_twh()
        * (1 + share_transmdistr_elec_losses() + elec_exports_share())
        + total_electricity_demand_for_synthetic() / ej_per_twh()
    )


@component.add(
    name='"variation_share_transm&distr_elec_losses"',
    units="Dmnl/year",
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
    name='"variation_share_transm&distr_losses_elec"',
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_transmdistr_elec_losses_initial": 1,
        "share_res_electricity_generation": 1,
        "nvs_1_year": 1,
    },
)
def variation_share_transmdistr_losses_elec():
    """
    Relationship between transmission and distribution losses of electricity and the penetration of RES in the electricity mix. Source: NREL (2012).
    """
    return (
        share_transmdistr_elec_losses_initial()
        * (
            0.0115 * float(np.exp(4.2297 * share_res_electricity_generation()))
            - 0.00251
        )
        / nvs_1_year()
    )
