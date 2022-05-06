"""
Module natural_gas_extraction
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="abundance total nat gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 3, "pes_nat_gas": 2},
)
def abundance_total_nat_gas():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_nat_gas_ej() < pes_nat_gas(),
        lambda: 1,
        lambda: 1 - zidz(ped_nat_gas_ej() - pes_nat_gas(), ped_nat_gas_ej()),
    )


@component.add(
    name="check gas delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_check_gas_delayed_1yr": 1},
    other_deps={
        "_delayfixed_check_gas_delayed_1yr": {"initial": {}, "step": {"check_gases": 1}}
    },
)
def check_gas_delayed_1yr():
    """
    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return _delayfixed_check_gas_delayed_1yr()


_delayfixed_check_gas_delayed_1yr = DelayFixed(
    lambda: check_gases(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_check_gas_delayed_1yr",
)


@component.add(
    name='"constrain gas exogenous growth? delayed 1yr"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_constrain_gas_exogenous_growth_delayed_1yr": 1},
    other_deps={
        "_delayfixed_constrain_gas_exogenous_growth_delayed_1yr": {
            "initial": {},
            "step": {"constrain_gas_exogenous_growth": 1},
        }
    },
)
def constrain_gas_exogenous_growth_delayed_1yr():
    return _delayfixed_constrain_gas_exogenous_growth_delayed_1yr()


_delayfixed_constrain_gas_exogenous_growth_delayed_1yr = DelayFixed(
    lambda: constrain_gas_exogenous_growth(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_constrain_gas_exogenous_growth_delayed_1yr",
)


@component.add(
    name="conv gas to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_policy_leave_in_ground_conv_gas": 1,
        "share_rurr_conv_gas_to_leave_underground": 1,
        "rurr_conv_gas_until_start_year_plg": 1,
    },
)
def conv_gas_to_leave_underground():
    """
    Conventional natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_conv_gas(),
        lambda: 0,
        lambda: rurr_conv_gas_until_start_year_plg()
        * share_rurr_conv_gas_to_leave_underground(),
    )


@component.add(
    name="cumulated conv gas extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_conv_gas_extraction": 1},
    other_deps={
        "_integ_cumulated_conv_gas_extraction": {
            "initial": {"cumulated_conv_gas_extraction_to_1995": 1},
            "step": {"extraction_conv_gas_ej": 1},
        }
    },
)
def cumulated_conv_gas_extraction():
    """
    Cumulated conventional gas extraction.
    """
    return _integ_cumulated_conv_gas_extraction()


_integ_cumulated_conv_gas_extraction = Integ(
    lambda: extraction_conv_gas_ej(),
    lambda: cumulated_conv_gas_extraction_to_1995(),
    "_integ_cumulated_conv_gas_extraction",
)


@component.add(
    name="cumulated conv gas extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulated_conv_gas_extraction_to_1995"},
)
def cumulated_conv_gas_extraction_to_1995():
    """
    Cumulated conventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_conv_gas_extraction_to_1995()


_ext_constant_cumulated_conv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_conventional_gas_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_conv_gas_extraction_to_1995",
)


@component.add(
    name="cumulated tot agg gas extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_tot_agg_gas_extraction": 1},
    other_deps={
        "_integ_cumulated_tot_agg_gas_extraction": {
            "initial": {"cumulated_tot_agg_gas_extraction_to_1995": 1},
            "step": {"extraction_tot_agg_gas_ej": 1},
        }
    },
)
def cumulated_tot_agg_gas_extraction():
    """
    Cumulated total aggregated gas extraction.
    """
    return _integ_cumulated_tot_agg_gas_extraction()


_integ_cumulated_tot_agg_gas_extraction = Integ(
    lambda: extraction_tot_agg_gas_ej(),
    lambda: cumulated_tot_agg_gas_extraction_to_1995(),
    "_integ_cumulated_tot_agg_gas_extraction",
)


@component.add(
    name="cumulated tot agg gas extraction to 1995",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cumulated_conv_gas_extraction_to_1995": 1,
        "cumulated_unconv_gas_extraction_to_1995": 1,
    },
)
def cumulated_tot_agg_gas_extraction_to_1995():
    """
    Cumulated total agg gas extraction to 1995.
    """
    return (
        cumulated_conv_gas_extraction_to_1995()
        + cumulated_unconv_gas_extraction_to_1995()
    )


@component.add(
    name="Cumulated unconv gas extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_unconv_gas_extraction": 1},
    other_deps={
        "_integ_cumulated_unconv_gas_extraction": {
            "initial": {"cumulated_unconv_gas_extraction_to_1995": 1},
            "step": {"extraction_unconv_gas_ej": 1},
        }
    },
)
def cumulated_unconv_gas_extraction():
    """
    Cumulated unconventional gas extraction.
    """
    return _integ_cumulated_unconv_gas_extraction()


_integ_cumulated_unconv_gas_extraction = Integ(
    lambda: extraction_unconv_gas_ej(),
    lambda: cumulated_unconv_gas_extraction_to_1995(),
    "_integ_cumulated_unconv_gas_extraction",
)


@component.add(
    name="cumulated unconv gas extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_cumulated_unconv_gas_extraction_to_1995"
    },
)
def cumulated_unconv_gas_extraction_to_1995():
    """
    Cumulated unconventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_unconv_gas_extraction_to_1995()


_ext_constant_cumulated_unconv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_unconventional_gas_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_unconv_gas_extraction_to_1995",
)


@component.add(
    name="Demand conv gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "extraction_unconv_gas_ej": 1},
)
def demand_conv_gas():
    """
    Demand of conventional gas. It is assumed that conventional gas covers the rest of the liquids demand after accounting for the contributions from unconventional gas.
    """
    return np.maximum(ped_nat_gas_ej() - extraction_unconv_gas_ej(), 0)


@component.add(
    name="demand gas for oil refinery gains",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_refinery_gains_ej": 1, "efficiency_gas_for_oil_refinery_gains": 1},
)
def demand_gas_for_oil_refinery_gains():
    """
    Demand of natural gas to be used as input in the refineries to obtain the so-called "oil refinery gains".
    """
    return oil_refinery_gains_ej() * efficiency_gas_for_oil_refinery_gains()


@component.add(
    name="Efficiency gas for oil refinery gains",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_gas_for_oil_refinery_gains"},
)
def efficiency_gas_for_oil_refinery_gains():
    """
    We assume a 100% efficiency as first approximation.
    """
    return _ext_constant_efficiency_gas_for_oil_refinery_gains()


_ext_constant_efficiency_gas_for_oil_refinery_gains = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_gas_for_oil_refinery_gains",
    {},
    _root,
    {},
    "_ext_constant_efficiency_gas_for_oil_refinery_gains",
)


@component.add(
    name="evolution share unconv gas vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_unconv_gas_vs_tot_agg_in_2050": 3, "time": 1},
)
def evolution_share_unconv_gas_vs_tot_agg():
    """
    Linear relation of the evolution of the share of unconventional gas vs total aggregated gas.
    """
    return (share_unconv_gas_vs_tot_agg_in_2050() - 0.1268) / (2050 - 2012) * time() + (
        share_unconv_gas_vs_tot_agg_in_2050()
        - ((share_unconv_gas_vs_tot_agg_in_2050() - 0.1268) / (2050 - 2012)) * 2050
    )


@component.add(
    name="exponent availability conv gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exponent_availability_conv_gas():
    """
    The smaller the exponent, more priority to conventional vs unconventional gas: 1: lineal 1/2: square root 1/3: cube root ...
    """
    return 1 / 4


@component.add(
    name='"extraction conv gas - tot agg"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_gas_ej": 1, "share_conv_gas_vs_tot_agg": 1},
)
def extraction_conv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_conv_gas_vs_tot_agg()


@component.add(
    name="extraction conv gas EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_conv_gas": 1,
        "unlimited_gas": 1,
        "unlimited_nre": 1,
        "demand_conv_gas": 2,
        "max_extraction_conv_gas_ej": 1,
    },
)
def extraction_conv_gas_ej():
    """
    Annual extraction of conventional gas.
    """
    return if_then_else(
        rurr_conv_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: demand_conv_gas(),
            lambda: np.minimum(demand_conv_gas(), max_extraction_conv_gas_ej()),
        ),
    )


@component.add(
    name="extraction tot agg gas EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_tot_agg_gas": 1,
        "unlimited_gas": 1,
        "unlimited_nre": 1,
        "max_extraction_tot_agg_gas_ej": 1,
        "ped_nat_gas_ej": 2,
    },
)
def extraction_tot_agg_gas_ej():
    """
    Annual extraction of total aggregated natural gas.
    """
    return if_then_else(
        rurr_tot_agg_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: ped_nat_gas_ej(),
            lambda: np.minimum(ped_nat_gas_ej(), max_extraction_tot_agg_gas_ej()),
        ),
    )


@component.add(
    name='"extraction unconv gas - tot agg"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_gas_ej": 1, "share_unconv_gas_vs_tot_agg": 1},
)
def extraction_unconv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_unconv_gas_vs_tot_agg()


@component.add(
    name="extraction unconv gas delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_unconv_gas_delayed": 1},
    other_deps={
        "_delayfixed_extraction_unconv_gas_delayed": {
            "initial": {"time_step": 1},
            "step": {"extraction_unconv_gas_ej": 1},
        }
    },
)
def extraction_unconv_gas_delayed():
    return _delayfixed_extraction_unconv_gas_delayed()


_delayfixed_extraction_unconv_gas_delayed = DelayFixed(
    lambda: extraction_unconv_gas_ej(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_extraction_unconv_gas_delayed",
)


@component.add(
    name="extraction unconv gas EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_unconv_gas": 1,
        "max_unconv_gas_growth_extraction_ej": 1,
        "time": 1,
        "separate_conv_and_unconv_gas": 1,
        "historic_unconv_gas": 1,
        "max_extraction_unconv_gas": 1,
    },
)
def extraction_unconv_gas_ej():
    """
    Annual extraction of unconventional gas. IF THEN ELSE("separate conv and unconv gas?"=1, IF THEN ELSE(Time<2011, Historic unconv gas(Time), MIN(max extraction unconv gas,max unconv gas growth extraction EJ )), 0)
    """
    return if_then_else(
        rurr_unconv_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2013,
            lambda: historic_unconv_gas(),
            lambda: if_then_else(
                separate_conv_and_unconv_gas() == 1,
                lambda: np.minimum(
                    max_extraction_unconv_gas(), max_unconv_gas_growth_extraction_ej()
                ),
                lambda: 0,
            ),
        ),
    )


@component.add(
    name="Flow conv gas left in ground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_conv_gas": 2,
        "conv_gas_to_leave_underground": 1,
    },
)
def flow_conv_gas_left_in_ground():
    """
    Flow of conventional natural gas left in the ground. We assume that this amount is removed from the stock of conventional natural gas available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_conv_gas(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_conv_gas() + 1,
            lambda: 0,
            lambda: conv_gas_to_leave_underground(),
        ),
    )


@component.add(
    name="Flow tot agg gas left in ground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_tot_agg_gas": 2,
        "tot_agg_gas_to_leave_underground": 1,
    },
)
def flow_tot_agg_gas_left_in_ground():
    """
    Flow of total aggregated natural gas left in the ground. We assume that this amount is removed from the stock of conventional natural gas available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_tot_agg_gas(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_tot_agg_gas() + 1,
            lambda: 0,
            lambda: tot_agg_gas_to_leave_underground(),
        ),
    )


@component.add(
    name="Flow unconv gas left in ground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_unconv_gas": 2,
        "unconv_gas_to_leave_underground": 1,
    },
)
def flow_unconv_gas_left_in_ground():
    """
    Flow of unconventional natural gas left in the ground. We assume that this amount is removed from the stock of unconventional natural gas available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_unconv_gas(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_unconv_gas() + 1,
            lambda: 0,
            lambda: unconv_gas_to_leave_underground(),
        ),
    )


@component.add(
    name="Historic unconv gas",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_gas",
        "__data__": "_ext_data_historic_unconv_gas",
        "time": 1,
    },
)
def historic_unconv_gas():
    """
    Historic unconventional extraction from Mohr et al (2015).
    """
    return _ext_data_historic_unconv_gas(time())


_ext_data_historic_unconv_gas = ExtData(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_unconventional_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_gas",
)


@component.add(
    name="increase scarcity conv gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_conv_gas_stock": 1,
        "scarcity_conv_gas": 2,
        "scarcity_conv_gas_delayed_1yr": 1,
    },
)
def increase_scarcity_conv_gas():
    return scarcity_conv_gas_stock() * zidz(
        scarcity_conv_gas() - scarcity_conv_gas_delayed_1yr(), scarcity_conv_gas()
    )


@component.add(
    name="max extraction conv gas EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "tot_rurr_conv_gas": 1,
        "table_max_extraction_conv_gas": 1,
    },
)
def max_extraction_conv_gas_ej():
    """
    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: table_max_extraction_conv_gas(tot_rurr_conv_gas()),
        lambda: 0,
    )


@component.add(
    name="max extraction tot agg gas EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "tot_rurr_tot_agg_gas": 1,
        "table_max_extraction_agg_gas": 1,
    },
)
def max_extraction_tot_agg_gas_ej():
    """
    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 0,
        lambda: table_max_extraction_agg_gas(tot_rurr_tot_agg_gas()),
        lambda: 0,
    )


@component.add(
    name="max extraction unconv gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tot_rurr_unconv_gas": 1, "table_max_extraction_unconv_gas": 1},
)
def max_extraction_unconv_gas():
    """
    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_unconv_gas(tot_rurr_unconv_gas())


@component.add(
    name="max unconv gas growth extraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_constraint_growth_extraction_unconv_gas": 1,
        "time_step": 1,
        "scarcity_conv_gas_stock": 1,
    },
)
def max_unconv_gas_growth_extraction():
    """
    Constraint to maximum annual unconventional gas extraction (%).
    """
    return np.maximum(
        0,
        1
        + p_constraint_growth_extraction_unconv_gas()
        * time_step()
        * scarcity_conv_gas_stock(),
    )


@component.add(
    name="max unconv gas growth extraction EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "check_gas_delayed_1yr": 1,
        "constrain_gas_exogenous_growth_delayed_1yr": 1,
        "extraction_unconv_gas_delayed": 2,
        "max_unconv_gas_growth_extraction": 1,
    },
)
def max_unconv_gas_growth_extraction_ej():
    """
    Constrained unconventional gas extraction growth (EJ/year), i.e. maximum annual growth compatible with the constraint selected in the scenario.
    """
    return if_then_else(
        check_gas_delayed_1yr() < -0.01,
        lambda: (1 + constrain_gas_exogenous_growth_delayed_1yr())
        * extraction_unconv_gas_delayed(),
        lambda: extraction_unconv_gas_delayed() * max_unconv_gas_growth_extraction(),
    )


@component.add(
    name="P constraint growth extraction unconv gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_p_constraint_growth_extraction_unconv_gas"
    },
)
def p_constraint_growth_extraction_unconv_gas():
    """
    Constant constraint to annual extraction of unconventional gas.
    """
    return _ext_constant_p_constraint_growth_extraction_unconv_gas()


_ext_constant_p_constraint_growth_extraction_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unconv_gas_growth",
    {},
    _root,
    {},
    "_ext_constant_p_constraint_growth_extraction_unconv_gas",
)


@component.add(
    name='"PED nat. gas without GTL"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "ped_nat_gas_for_gtl_ej": 1},
)
def ped_nat_gas_without_gtl():
    """
    Total demand of natural gas without GTL.
    """
    return np.maximum(0, ped_nat_gas_ej() - ped_nat_gas_for_gtl_ej())


@component.add(
    name="PES nat gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas_ej": 1, "real_extraction_unconv_gas_ej": 1},
)
def pes_nat_gas():
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


@component.add(
    name='"PES nat. gas without GTL"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas": 1, "ped_nat_gas_for_gtl_ej": 1},
)
def pes_nat_gas_without_gtl():
    """
    Total extraction of conventional gas and unconventional (without GTL).
    """
    return pes_nat_gas() - ped_nat_gas_for_gtl_ej()


@component.add(
    name="real extraction conv gas EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "extraction_conv_gas_ej": 1,
        "extraction_conv_gas_tot_agg": 1,
    },
)
def real_extraction_conv_gas_ej():
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_conv_gas_ej(),
        lambda: extraction_conv_gas_tot_agg(),
    )


@component.add(
    name="real extraction conv gas emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_conv_gas_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "ped_nat_gas_for_gtl_ej": 1,
    },
)
def real_extraction_conv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_conv_gas_ej()
        - (
            ped_nat_gas_for_gtl_ej()
            + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        )
        * share_conv_vs_total_gas_extraction(),
    )


@component.add(
    name="real extraction unconv gas EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "extraction_unconv_gas_ej": 1,
        "extraction_unconv_gas_tot_agg": 1,
    },
)
def real_extraction_unconv_gas_ej():
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_unconv_gas_ej(),
        lambda: extraction_unconv_gas_tot_agg(),
    )


@component.add(
    name="real extraction unconv gas emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_unconv_gas_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "ped_nat_gas_for_gtl_ej": 1,
    },
)
def real_extraction_unconv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_unconv_gas_ej()
        - (
            ped_nat_gas_for_gtl_ej()
            + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        )
        * (1 - share_conv_vs_total_gas_extraction()),
    )


@component.add(
    name="RURR conv gas",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_conv_gas": 1},
    other_deps={
        "_integ_rurr_conv_gas": {
            "initial": {
                "urr_conv_gas": 1,
                "cumulated_conv_gas_extraction_to_1995": 1,
                "separate_conv_and_unconv_gas": 1,
            },
            "step": {"extraction_conv_gas_ej": 1, "flow_conv_gas_left_in_ground": 1},
        }
    },
)
def rurr_conv_gas():
    """
    RURR conventional gas.
    """
    return _integ_rurr_conv_gas()


_integ_rurr_conv_gas = Integ(
    lambda: -extraction_conv_gas_ej() - flow_conv_gas_left_in_ground(),
    lambda: urr_conv_gas()
    - cumulated_conv_gas_extraction_to_1995() * separate_conv_and_unconv_gas(),
    "_integ_rurr_conv_gas",
)


@component.add(
    name="RURR conv gas until start year PLG",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_conv_gas_until_start_year_plg": 1},
    other_deps={
        "_sampleiftrue_rurr_conv_gas_until_start_year_plg": {
            "initial": {"rurr_conv_gas": 1},
            "step": {
                "time": 1,
                "start_policy_leave_in_ground_conv_gas": 1,
                "rurr_conv_gas": 1,
            },
        }
    },
)
def rurr_conv_gas_until_start_year_plg():
    """
    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_conv_gas_until_start_year_plg()


_sampleiftrue_rurr_conv_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_conv_gas(),
    lambda: rurr_conv_gas(),
    lambda: rurr_conv_gas(),
    "_sampleiftrue_rurr_conv_gas_until_start_year_plg",
)


@component.add(
    name="RURR tot agg gas",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_tot_agg_gas": 1},
    other_deps={
        "_integ_rurr_tot_agg_gas": {
            "initial": {
                "separate_conv_and_unconv_gas": 1,
                "urr_tot_agg_gas": 1,
                "cumulated_tot_agg_gas_extraction_to_1995": 1,
            },
            "step": {
                "extraction_tot_agg_gas_ej": 1,
                "flow_tot_agg_gas_left_in_ground": 1,
            },
        }
    },
)
def rurr_tot_agg_gas():
    """
    RURR total aggregated natural gas.
    """
    return _integ_rurr_tot_agg_gas()


_integ_rurr_tot_agg_gas = Integ(
    lambda: -extraction_tot_agg_gas_ej() - flow_tot_agg_gas_left_in_ground(),
    lambda: if_then_else(
        separate_conv_and_unconv_gas() == 0,
        lambda: urr_tot_agg_gas() - cumulated_tot_agg_gas_extraction_to_1995(),
        lambda: 0,
    ),
    "_integ_rurr_tot_agg_gas",
)


@component.add(
    name="RURR tot gas until start year PLG",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_tot_gas_until_start_year_plg": 1},
    other_deps={
        "_sampleiftrue_rurr_tot_gas_until_start_year_plg": {
            "initial": {"rurr_tot_agg_gas": 1},
            "step": {
                "time": 1,
                "start_policy_leave_in_ground_tot_agg_gas": 1,
                "rurr_tot_agg_gas": 1,
            },
        }
    },
)
def rurr_tot_gas_until_start_year_plg():
    """
    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_tot_gas_until_start_year_plg()


_sampleiftrue_rurr_tot_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_tot_agg_gas(),
    lambda: rurr_tot_agg_gas(),
    lambda: rurr_tot_agg_gas(),
    "_sampleiftrue_rurr_tot_gas_until_start_year_plg",
)


@component.add(
    name="RURR unconv gas",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_unconv_gas": 1},
    other_deps={
        "_integ_rurr_unconv_gas": {
            "initial": {
                "urr_unconv_gas": 1,
                "separate_conv_and_unconv_gas": 1,
                "cumulated_unconv_gas_extraction_to_1995": 1,
            },
            "step": {
                "extraction_unconv_gas_ej": 1,
                "flow_unconv_gas_left_in_ground": 1,
            },
        }
    },
)
def rurr_unconv_gas():
    """
    RURR unconventional gas.
    """
    return _integ_rurr_unconv_gas()


_integ_rurr_unconv_gas = Integ(
    lambda: -extraction_unconv_gas_ej() - flow_unconv_gas_left_in_ground(),
    lambda: urr_unconv_gas()
    - cumulated_unconv_gas_extraction_to_1995() * separate_conv_and_unconv_gas(),
    "_integ_rurr_unconv_gas",
)


@component.add(
    name="RURR unconv gas until start year PLG",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_unconv_gas_until_start_year_plg": 1},
    other_deps={
        "_sampleiftrue_rurr_unconv_gas_until_start_year_plg": {
            "initial": {"rurr_unconv_gas": 1},
            "step": {
                "time": 1,
                "start_policy_leave_in_ground_unconv_gas": 1,
                "rurr_unconv_gas": 1,
            },
        }
    },
)
def rurr_unconv_gas_until_start_year_plg():
    """
    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_unconv_gas_until_start_year_plg()


_sampleiftrue_rurr_unconv_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_unconv_gas(),
    lambda: rurr_unconv_gas(),
    lambda: rurr_unconv_gas(),
    "_sampleiftrue_rurr_unconv_gas_until_start_year_plg",
)


@component.add(
    name="scarcity conv gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_extraction_conv_gas_ej": 4,
        "exponent_availability_conv_gas": 1,
        "extraction_conv_gas_ej": 2,
    },
)
def scarcity_conv_gas():
    """
    Priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached.
    """
    return if_then_else(
        max_extraction_conv_gas_ej() == 0,
        lambda: 0,
        lambda: if_then_else(
            max_extraction_conv_gas_ej() >= extraction_conv_gas_ej(),
            lambda: 1
            - (
                (max_extraction_conv_gas_ej() - extraction_conv_gas_ej())
                / max_extraction_conv_gas_ej()
            )
            ** exponent_availability_conv_gas(),
            lambda: 0,
        ),
    )


@component.add(
    name="scarcity conv gas delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_scarcity_conv_gas_delayed_1yr": 1},
    other_deps={
        "_delayfixed_scarcity_conv_gas_delayed_1yr": {
            "initial": {},
            "step": {"scarcity_conv_gas": 1},
        }
    },
)
def scarcity_conv_gas_delayed_1yr():
    return _delayfixed_scarcity_conv_gas_delayed_1yr()


_delayfixed_scarcity_conv_gas_delayed_1yr = DelayFixed(
    lambda: scarcity_conv_gas(),
    lambda: 1,
    lambda: 0.2502,
    time_step,
    "_delayfixed_scarcity_conv_gas_delayed_1yr",
)


@component.add(
    name="scarcity conv gas stock",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_scarcity_conv_gas_stock": 1},
    other_deps={
        "_integ_scarcity_conv_gas_stock": {
            "initial": {},
            "step": {"increase_scarcity_conv_gas": 1},
        }
    },
)
def scarcity_conv_gas_stock():
    return _integ_scarcity_conv_gas_stock()


_integ_scarcity_conv_gas_stock = Integ(
    lambda: increase_scarcity_conv_gas(),
    lambda: 0.2502,
    "_integ_scarcity_conv_gas_stock",
)


@component.add(
    name='"separate conv and unconv gas?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_separate_conv_and_unconv_gas"},
)
def separate_conv_and_unconv_gas():
    """
    Switch to disaggregate between conventional and unconventional fuel: "1" = disaggregation, "0" = conv+unconv aggregated (all the gas flows then through the right side of this view, i.e. the "conventional gas" modelling side).
    """
    return _ext_constant_separate_conv_and_unconv_gas()


_ext_constant_separate_conv_and_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "separate_conv_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_separate_conv_and_unconv_gas",
)


@component.add(
    name="share conv gas vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_unconv_gas_vs_tot_agg": 1},
)
def share_conv_gas_vs_tot_agg():
    return 1 - share_unconv_gas_vs_tot_agg()


@component.add(
    name="share conv vs total gas extraction",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas_ej": 2, "real_extraction_unconv_gas_ej": 1},
)
def share_conv_vs_total_gas_extraction():
    """
    Share of conventional gas vs total gas extracted.
    """
    return zidz(
        real_extraction_conv_gas_ej(),
        real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej(),
    )


@component.add(
    name="share gas for oil refinery gains",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_without_gtl": 2, "demand_gas_for_oil_refinery_gains": 1},
)
def share_gas_for_oil_refinery_gains():
    """
    Share of gas to cover oil refinery gains. Condition to avoid error when the total demand of gas without GTL falls to zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        ped_nat_gas_without_gtl() > 0,
        lambda: demand_gas_for_oil_refinery_gains() / ped_nat_gas_without_gtl(),
        lambda: 0.5,
    )


@component.add(
    name="share RURR conv gas to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_conv_gas_to_leave_underground"
    },
)
def share_rurr_conv_gas_to_leave_underground():
    """
    RURR's conventional gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_conv_gas_to_leave_underground()


_ext_constant_share_rurr_conv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_conv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_conv_gas_to_leave_underground",
)


@component.add(
    name="share RURR tot agg gas to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_tot_agg_gas_to_leave_underground"
    },
)
def share_rurr_tot_agg_gas_to_leave_underground():
    """
    RURR's total aggregated natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_tot_agg_gas_to_leave_underground()


_ext_constant_share_rurr_tot_agg_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_agg_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_tot_agg_gas_to_leave_underground",
)


@component.add(
    name="share RURR unconv gas to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_unconv_gas_to_leave_underground"
    },
)
def share_rurr_unconv_gas_to_leave_underground():
    """
    RURR's unconventional natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_unconv_gas_to_leave_underground()


_ext_constant_share_rurr_unconv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_unconv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_unconv_gas_to_leave_underground",
)


@component.add(
    name="share unconv gas vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "evolution_share_unconv_gas_vs_tot_agg": 1,
        "historic_unconv_gas": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_unconv_gas_vs_tot_agg():
    """
    Evolution of the share of unconventional gas vs total aggregated gas.
    """
    return if_then_else(
        time() > 2012,
        lambda: np.minimum(evolution_share_unconv_gas_vs_tot_agg(), 1),
        lambda: historic_unconv_gas() / ped_nat_gas_ej(),
    )


@component.add(
    name="share unconv gas vs tot agg in 2050",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_unconv_gas_vs_tot_agg_in_2050"},
)
def share_unconv_gas_vs_tot_agg_in_2050():
    """
    Share of unconventional gas vs total aggregated gas in 2050 depending on the maximum extraction curve selected for total aggregated gas.
    """
    return _ext_constant_share_unconv_gas_vs_tot_agg_in_2050()


_ext_constant_share_unconv_gas_vs_tot_agg_in_2050 = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_unconv_vs_agg_gas_in_2050",
    {},
    _root,
    {},
    "_ext_constant_share_unconv_gas_vs_tot_agg_in_2050",
)


@component.add(
    name="Start policy leave in ground conv gas",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_policy_leave_in_ground_conv_gas"},
)
def start_policy_leave_in_ground_conv_gas():
    """
    Year when the policy to leave in the ground an amount of conventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_conv_gas()


_ext_constant_start_policy_leave_in_ground_conv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_conv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_conv_gas",
)


@component.add(
    name="Start policy leave in ground tot agg gas",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_policy_leave_in_ground_tot_agg_gas"
    },
)
def start_policy_leave_in_ground_tot_agg_gas():
    """
    Year when the policy to leave in the ground an amount of total aggregated gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_gas()


_ext_constant_start_policy_leave_in_ground_tot_agg_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_agg_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_tot_agg_gas",
)


@component.add(
    name="Start policy leave in ground unconv gas",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_policy_leave_in_ground_unconv_gas"
    },
)
def start_policy_leave_in_ground_unconv_gas():
    """
    Year when the policy to leave in the ground an amount of unconventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_unconv_gas()


_ext_constant_start_policy_leave_in_ground_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_unconv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_unconv_gas",
)


@component.add(
    name="table max extraction agg gas",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_agg_gas",
        "__lookup__": "_ext_lookup_table_max_extraction_agg_gas",
    },
)
def table_max_extraction_agg_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_agg_gas(x, final_subs)


_ext_lookup_table_max_extraction_agg_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_agg_gas",
    "max_extraction_agg_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_agg_gas",
)


@component.add(
    name="table max extraction conv gas",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_conv_gas",
        "__lookup__": "_ext_lookup_table_max_extraction_conv_gas",
    },
)
def table_max_extraction_conv_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_conv_gas(x, final_subs)


_ext_lookup_table_max_extraction_conv_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_conv_gas",
    "max_extraction_conv_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_conv_gas",
)


@component.add(
    name="table max extraction unconv gas",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_unconv_gas",
        "__lookup__": "_ext_lookup_table_max_extraction_unconv_gas",
    },
)
def table_max_extraction_unconv_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_unconv_gas(x, final_subs)


_ext_lookup_table_max_extraction_unconv_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_unconv_gas",
    "max_extraction_unconv_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_unconv_gas",
)


@component.add(
    name="tot agg gas to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_policy_leave_in_ground_tot_agg_gas": 1,
        "share_rurr_tot_agg_gas_to_leave_underground": 1,
        "rurr_tot_gas_until_start_year_plg": 1,
    },
)
def tot_agg_gas_to_leave_underground():
    """
    Total aggregated natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_tot_agg_gas(),
        lambda: 0,
        lambda: rurr_tot_gas_until_start_year_plg()
        * share_rurr_tot_agg_gas_to_leave_underground(),
    )


@component.add(
    name="Tot RURR conv gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_conv_gas": 1, "total_conv_gas_left_in_ground": 1},
)
def tot_rurr_conv_gas():
    """
    Total RURR of conventional natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_conv_gas() + total_conv_gas_left_in_ground()


@component.add(
    name="Tot RURR tot agg gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_tot_agg_gas": 1, "total_agg_gas_left_in_ground": 1},
)
def tot_rurr_tot_agg_gas():
    """
    Total RURR of total aggregated natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_tot_agg_gas() + total_agg_gas_left_in_ground()


@component.add(
    name="Tot RURR unconv gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_unconv_gas": 1, "total_unconv_gas_left_in_ground": 1},
)
def tot_rurr_unconv_gas():
    """
    Total RURR of unconventional natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_unconv_gas() + total_unconv_gas_left_in_ground()


@component.add(
    name="Total agg gas left in ground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_agg_gas_left_in_ground": 1},
    other_deps={
        "_integ_total_agg_gas_left_in_ground": {
            "initial": {},
            "step": {"flow_tot_agg_gas_left_in_ground": 1},
        }
    },
)
def total_agg_gas_left_in_ground():
    """
    Total amount of aggregated natural gas left in the ground due to policies.
    """
    return _integ_total_agg_gas_left_in_ground()


_integ_total_agg_gas_left_in_ground = Integ(
    lambda: flow_tot_agg_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_agg_gas_left_in_ground",
)


@component.add(
    name="Total conv gas left in ground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_conv_gas_left_in_ground": 1},
    other_deps={
        "_integ_total_conv_gas_left_in_ground": {
            "initial": {},
            "step": {"flow_conv_gas_left_in_ground": 1},
        }
    },
)
def total_conv_gas_left_in_ground():
    """
    Total amount of conventional natural gas left in the ground due to policies.
    """
    return _integ_total_conv_gas_left_in_ground()


_integ_total_conv_gas_left_in_ground = Integ(
    lambda: flow_conv_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_conv_gas_left_in_ground",
)


@component.add(
    name="Total unconv gas left in ground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_unconv_gas_left_in_ground": 1},
    other_deps={
        "_integ_total_unconv_gas_left_in_ground": {
            "initial": {},
            "step": {"flow_unconv_gas_left_in_ground": 1},
        }
    },
)
def total_unconv_gas_left_in_ground():
    """
    Total amount of unconventional natural gas left in the ground due to policies.
    """
    return _integ_total_unconv_gas_left_in_ground()


_integ_total_unconv_gas_left_in_ground = Integ(
    lambda: flow_unconv_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_unconv_gas_left_in_ground",
)


@component.add(
    name="unconv gas to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_policy_leave_in_ground_unconv_gas": 1,
        "share_rurr_unconv_gas_to_leave_underground": 1,
        "rurr_unconv_gas_until_start_year_plg": 1,
    },
)
def unconv_gas_to_leave_underground():
    """
    Unconventional natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_unconv_gas(),
        lambda: 0,
        lambda: rurr_unconv_gas_until_start_year_plg()
        * share_rurr_unconv_gas_to_leave_underground(),
    )


@component.add(
    name='"unlimited gas?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_unlimited_gas"},
)
def unlimited_gas():
    """
    Switch to consider if gas is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_gas()


_ext_constant_unlimited_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_gas",
    {},
    _root,
    {},
    "_ext_constant_unlimited_gas",
)


@component.add(
    name="URR conv gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "unlimited_gas": 1,
        "unlimited_nre": 1,
        "urr_conv_gas_input": 1,
    },
)
def urr_conv_gas():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: np.nan,
            lambda: urr_conv_gas_input(),
        ),
        lambda: 0,
    )


@component.add(
    name="URR conv gas input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_conv_gas_input"},
)
def urr_conv_gas_input():
    return _ext_constant_urr_conv_gas_input()


_ext_constant_urr_conv_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_conv_gas_input",
)


@component.add(
    name="URR tot agg gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "unlimited_gas": 1,
        "unlimited_nre": 1,
        "urr_total_gas_input": 1,
    },
)
def urr_tot_agg_gas():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: np.nan,
            lambda: urr_total_gas_input(),
        ),
    )


@component.add(
    name="URR total gas input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_total_gas_input"},
)
def urr_total_gas_input():
    return _ext_constant_urr_total_gas_input()


_ext_constant_urr_total_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_agg_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_total_gas_input",
)


@component.add(
    name="URR unconv gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_gas": 1, "urr_unconv_gas_input": 1},
)
def urr_unconv_gas():
    """
    RURR unconventional gas.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1, lambda: urr_unconv_gas_input(), lambda: 0
    )


@component.add(
    name="URR unconv gas input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_unconv_gas_input"},
)
def urr_unconv_gas_input():
    return _ext_constant_urr_unconv_gas_input()


_ext_constant_urr_unconv_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_unconv_gas_input",
)


@component.add(
    name='"Year scarcity total nat. gas"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_nat_gas": 1, "time": 1},
)
def year_scarcity_total_nat_gas():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_total_nat_gas() > 0.95, lambda: 0, lambda: time())
