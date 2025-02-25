"""
Module energy.availability.natural_gas_extraction
Translated using PySD version 3.14.2
"""

@component.add(
    name='"abundance_total_nat._gas_CAT_"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 3, "pes_nat_gas_cat_": 2},
)
def abundance_total_nat_gas_cat_():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_nat_gas_ej() < pes_nat_gas_cat_(),
        lambda: 1,
        lambda: 1 - zidz(ped_nat_gas_ej() - pes_nat_gas_cat_(), ped_nat_gas_ej()),
    )


@component.add(
    name="check_gas_delayed_1yr",
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
    name='"constrain_gas_exogenous_growth?_delayed_1yr"',
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
    name="conv_gas_to_leave_underground",
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
    name="cumulated_conv_gas_extraction",
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
    name="cumulated_conv_gas_extraction_to_1995",
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
    r"../energy.xlsx",
    "Catalonia",
    "cumulative_conventional_gas_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_conv_gas_extraction_to_1995",
)


@component.add(
    name="cumulated_tot_agg_gas_extraction",
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
    name="cumulated_tot_agg_gas_extraction_to_1995",
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
    name="Cumulated_unconv_gas_extraction",
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
    name="cumulated_unconv_gas_extraction_to_1995",
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
    r"../energy.xlsx",
    "Catalonia",
    "cumulative_unconventional_gas_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_unconv_gas_extraction_to_1995",
)


@component.add(
    name="delay_gas_to_leave_underground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_delay_gas_to_leave_underground": 1},
    other_deps={
        "_sampleiftrue_delay_gas_to_leave_underground": {
            "initial": {},
            "step": {
                "time": 1,
                "start_year_policy_leave_in_ground_fossil_gas": 1,
                "total_agg_fossil_gas_to_leave_underground": 1,
            },
        }
    },
)
def delay_gas_to_leave_underground():
    return _sampleiftrue_delay_gas_to_leave_underground()


_sampleiftrue_delay_gas_to_leave_underground = SampleIfTrue(
    lambda: time() == start_year_policy_leave_in_ground_fossil_gas(),
    lambda: total_agg_fossil_gas_to_leave_underground(),
    lambda: 0,
    "_sampleiftrue_delay_gas_to_leave_underground",
)


@component.add(
    name="Demand_conv_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "extraction_unconv_gas_ej": 1},
)
def demand_conv_gas():
    """
    Demand of conventional gas. It is assumed that conventional gas covers the rest of the liquids demand after accounting for the contributions from unconventional gas.
    """
    return float(np.maximum(ped_nat_gas_ej() - extraction_unconv_gas_ej(), 0))


@component.add(
    name="demand_gas_for_oil_refinery_gains",
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
    name="Efficiency_gas_for_oil_refinery_gains",
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
    r"../energy.xlsx",
    "Global",
    "efficiency_gas_for_oil_refinery_gains",
    {},
    _root,
    {},
    "_ext_constant_efficiency_gas_for_oil_refinery_gains",
)


@component.add(
    name="evol_fossil_gas_extraction_rate_constraint",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_to_end_fossil_gas_extraction": 2,
        "extraction_tot_agg_gas_ej": 1,
    },
)
def evol_fossil_gas_extraction_rate_constraint():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets.
    """
    return if_then_else(
        time() < year_to_end_fossil_gas_extraction(),
        lambda: -extraction_tot_agg_gas_ej()
        / (year_to_end_fossil_gas_extraction() - time()),
        lambda: 0,
    )


@component.add(
    name="evol_fossil_gas_extraction_rate_delayed",
    units="EJ/(year*year)",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_evol_fossil_gas_extraction_rate_delayed": 1},
    other_deps={
        "_delayfixed_evol_fossil_gas_extraction_rate_delayed": {
            "initial": {"time_step": 1},
            "step": {"evol_fossil_gas_extraction_rate_constraint": 1},
        }
    },
)
def evol_fossil_gas_extraction_rate_delayed():
    """
    Slope of linear fit to limit extraction from current extraction to zero,where the are under the curve is the remainig extractable resources to comply with leave in ground targets. Delayed one time step.
    """
    return _delayfixed_evol_fossil_gas_extraction_rate_delayed()


_delayfixed_evol_fossil_gas_extraction_rate_delayed = DelayFixed(
    lambda: evol_fossil_gas_extraction_rate_constraint(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_evol_fossil_gas_extraction_rate_delayed",
)


@component.add(
    name="evolution_share_unconv_gas_vs_tot_agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_unconv_gas_vs_tot_agg_in_2050": 3,
        "year_2012": 2,
        "year_2050": 3,
        "time": 1,
    },
)
def evolution_share_unconv_gas_vs_tot_agg():
    """
    Linear relation of the evolution of the share of unconventional gas vs total aggregated gas.
    """
    return (share_unconv_gas_vs_tot_agg_in_2050() - 0.1232) / (
        year_2050() - year_2012()
    ) * time() + (
        share_unconv_gas_vs_tot_agg_in_2050()
        - (
            (share_unconv_gas_vs_tot_agg_in_2050() - 0.1232)
            / (year_2050() - year_2012())
        )
        * year_2050()
    )


@component.add(
    name="exponent_availability_conv_gas",
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
    name="extraction_conv_gas_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_conv_gas": 1,
        "time": 1,
        "max_extraction_conv_gas_ej": 1,
        "ped_domestic_cat_conv_nat_gas_ej": 2,
    },
)
def extraction_conv_gas_ej():
    """
    Annual extraction of conventional gas. IF THEN ELSE(RURR coal<0,0, IF THEN ELSE(Time<2016, PED domestic EU coal EJ, IF THEN ELSE("unlimited NRE?"=1, PED domestic EU coal EJ, IF THEN ELSE("unlimited coal?"=1, PED domestic EU coal EJ,MIN(PED domestic EU coal EJ, max extraction coal EJ)))))
    """
    return if_then_else(
        rurr_conv_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2016,
            lambda: ped_domestic_cat_conv_nat_gas_ej(),
            lambda: float(
                np.minimum(
                    ped_domestic_cat_conv_nat_gas_ej(), max_extraction_conv_gas_ej()
                )
            ),
        ),
    )


@component.add(
    name='"extraction_conv_gas_-_tot_agg"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_gas_ej": 1, "share_conv_gas_vs_tot_agg": 1},
)
def extraction_conv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_conv_gas_vs_tot_agg()


@component.add(
    name="extraction_fossil_gas_agg_EJ_delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_fossil_gas_agg_ej_delayed": 1},
    other_deps={
        "_delayfixed_extraction_fossil_gas_agg_ej_delayed": {
            "initial": {"time_step": 1},
            "step": {"extraction_tot_agg_gas_ej": 1},
        }
    },
)
def extraction_fossil_gas_agg_ej_delayed():
    """
    Annual extraction of aggregated fossil gas delayed one year. The delay allows to progressively limit extraction (due to leave underground policies) using previous extraction rates.
    """
    return _delayfixed_extraction_fossil_gas_agg_ej_delayed()


_delayfixed_extraction_fossil_gas_agg_ej_delayed = DelayFixed(
    lambda: extraction_tot_agg_gas_ej(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_extraction_fossil_gas_agg_ej_delayed",
)


@component.add(
    name="extraction_tot_agg_gas_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ped_domestic_cat_total_natgas_ej": 3,
        "remaining_extractable_fossil_gas_with_left_underground": 1,
        "activate_force_leaving_underground": 1,
        "nvs_1_year": 1,
        "max_extraction_tot_agg_gas": 2,
    },
)
def extraction_tot_agg_gas_ej():
    """
    Annual extraction of total aggregated fossil gas. IF THEN ELSE(Time<2016 , historic gas extraction(Time), IF THEN ELSE(Activate force leaving underground = 0, MIN("PED domestic CAT total nat.gas EJ", max extraction tot agg gas), MIN(MIN("PED domestic CAT total nat.gas EJ", max extraction tot agg gas), remaining extractable fossil gas with left underground)))
    """
    return if_then_else(
        time() < 2016,
        lambda: ped_domestic_cat_total_natgas_ej(),
        lambda: if_then_else(
            activate_force_leaving_underground() == 0,
            lambda: float(
                np.minimum(
                    ped_domestic_cat_total_natgas_ej(), max_extraction_tot_agg_gas()
                )
            ),
            lambda: float(
                np.minimum(
                    float(
                        np.minimum(
                            ped_domestic_cat_total_natgas_ej(),
                            max_extraction_tot_agg_gas(),
                        )
                    ),
                    remaining_extractable_fossil_gas_with_left_underground()
                    / nvs_1_year(),
                )
            ),
        ),
    )


@component.add(
    name="extraction_unconv_gas_delayed",
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
    name="extraction_unconv_gas_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_unconv_gas": 1,
        "time": 1,
        "max_extraction_unconv_gas": 1,
        "separate_conv_and_unconv_gas": 1,
        "historic_unconv_gas": 1,
        "max_unconv_gas_growth_extraction_ej": 1,
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
                lambda: float(
                    np.minimum(
                        max_extraction_unconv_gas(),
                        max_unconv_gas_growth_extraction_ej(),
                    )
                ),
                lambda: 0,
            ),
        ),
    )


@component.add(
    name='"extraction_unconv_gas_-_tot_agg"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_gas_ej": 1, "share_unconv_gas_vs_tot_agg": 1},
)
def extraction_unconv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_unconv_gas_vs_tot_agg()


@component.add(
    name="Flow_conv_gas_left_in_ground",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_conv_gas": 2,
        "conv_gas_to_leave_underground": 1,
        "nvs_1_year": 1,
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
            lambda: conv_gas_to_leave_underground() / nvs_1_year(),
        ),
    )


@component.add(
    name="Flow_unconv_gas_left_in_ground",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_unconv_gas": 2,
        "unconv_gas_to_leave_underground": 1,
        "nvs_1_year": 1,
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
            lambda: unconv_gas_to_leave_underground() / nvs_1_year(),
        ),
    )


@component.add(
    name="Historic_unconv_gas",
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
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_unconventional_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_gas",
)


@component.add(
    name="increase_scarcity_conv_gas",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_conv_gas": 1,
        "scarcity_conv_gas_delayed_ts": 1,
        "time_step": 1,
    },
)
def increase_scarcity_conv_gas():
    return (scarcity_conv_gas() - scarcity_conv_gas_delayed_ts()) / time_step()


@component.add(
    name="max_extraction_conv_gas_EJ",
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
    name="max_extraction_tot_agg_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_force_leaving_underground": 1,
        "max_extraction_total_agg_gas_technical_ej": 3,
        "start_year_policy_leave_in_ground_fossil_gas": 1,
        "time": 1,
        "max_extraction_total_agg_gas_policy": 1,
    },
)
def max_extraction_tot_agg_gas():
    """
    Maximum extraction of aggregated gas due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return if_then_else(
        activate_force_leaving_underground() == 0,
        lambda: max_extraction_total_agg_gas_technical_ej(),
        lambda: if_then_else(
            time() > start_year_policy_leave_in_ground_fossil_gas(),
            lambda: float(
                np.minimum(
                    max_extraction_total_agg_gas_technical_ej(),
                    max_extraction_total_agg_gas_policy(),
                )
            ),
            lambda: max_extraction_total_agg_gas_technical_ej(),
        ),
    )


@component.add(
    name="max_extraction_total_agg_gas_policy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_fossil_gas_extraction_rate_delayed": 1,
        "time_step": 1,
        "extraction_fossil_gas_agg_ej_delayed": 1,
    },
)
def max_extraction_total_agg_gas_policy():
    """
    Maximum extraction of aggregated gas allowed by leave underground policy (progressive linear decrease assumed).
    """
    return (
        evol_fossil_gas_extraction_rate_delayed() * time_step()
        + extraction_fossil_gas_agg_ej_delayed()
    )


@component.add(
    name="max_extraction_total_agg_gas_technical_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "rurr_tot_agg_gas": 1,
        "table_max_extraction_agg_gas": 1,
    },
)
def max_extraction_total_agg_gas_technical_ej():
    """
    Maximum extraction of fossil gas due to technical constraints (Hubbert).
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 0,
        lambda: table_max_extraction_agg_gas(rurr_tot_agg_gas()),
        lambda: 0,
    )


@component.add(
    name="max_extraction_unconv_gas",
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
    name="max_unconv_gas_growth_extraction",
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
    Constraint to maximum annual unconventional gas extraction (%). This constraint is affected by the relative scarcity of conventional vs unconventional resource (priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached).
    """
    return float(
        np.maximum(
            0,
            1
            + p_constraint_growth_extraction_unconv_gas()
            * time_step()
            * scarcity_conv_gas_stock(),
        )
    )


@component.add(
    name="max_unconv_gas_growth_extraction_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "check_gas_delayed_1yr": 1,
        "extraction_unconv_gas_delayed": 2,
        "constrain_gas_exogenous_growth_delayed_1yr": 1,
        "max_unconv_gas_growth_extraction": 1,
    },
)
def max_unconv_gas_growth_extraction_ej():
    """
    Constrained unconventional gas extraction growth (EJ/Year), i.e. maximum annual growth compatible with the constraint selected in the scenario.
    """
    return if_then_else(
        check_gas_delayed_1yr() < -0.01,
        lambda: (1 + constrain_gas_exogenous_growth_delayed_1yr())
        * extraction_unconv_gas_delayed(),
        lambda: extraction_unconv_gas_delayed() * max_unconv_gas_growth_extraction(),
    )


@component.add(
    name="P_constraint_growth_extraction_unconv_gas",
    units="Dmnl/year",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "p_constraint_growth_extraction_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_p_constraint_growth_extraction_unconv_gas",
)


@component.add(
    name="PEC_conv_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas": 1, "imports_cat_conv_gas_from_row": 1},
)
def pec_conv_gas():
    return real_extraction_conv_gas() + imports_cat_conv_gas_from_row()


@component.add(
    name="PEC_unconv_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_unconv_gas": 1, "imports_cat_unconv_gas_from_row": 1},
)
def pec_unconv_gas():
    return real_extraction_unconv_gas() + imports_cat_unconv_gas_from_row()


@component.add(
    name='"PED_nat._gas_without_GTL"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "ped_nat_gas_for_gtl_ej": 1},
)
def ped_nat_gas_without_gtl():
    """
    Total demand of natural gas without GTL.
    """
    return float(np.maximum(0, ped_nat_gas_ej() - ped_nat_gas_for_gtl_ej()))


@component.add(
    name='"PES_nat._gas_CAT_"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas": 1, "real_extraction_unconv_gas": 1},
)
def pes_nat_gas_cat_():
    return real_extraction_conv_gas() + real_extraction_unconv_gas()


@component.add(
    name='"PES_nat._gas_without_GTL"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_cat_": 1, "ped_nat_gas_for_gtl_ej": 1},
)
def pes_nat_gas_without_gtl():
    """
    Total extraction of conventional gas and unconventional (without GTL).
    """
    return pes_nat_gas_cat_() - ped_nat_gas_for_gtl_ej()


@component.add(
    name="real_consumption_UE_conv_gas_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_conv_gas": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "share_conv_vs_total_gas_extraction_eu": 1,
    },
)
def real_consumption_ue_conv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return float(
        np.maximum(
            0,
            pec_conv_gas()
            - float(nonenergy_use_demand_by_final_fuel().loc["gases"])
            * share_conv_vs_total_gas_extraction_eu(),
        )
    )


@component.add(
    name="real_consumption_unconv_gas_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_unconv_gas": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "share_conv_vs_total_gas_extraction_eu": 1,
    },
)
def real_consumption_unconv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return float(
        np.maximum(
            0,
            pec_unconv_gas()
            - float(nonenergy_use_demand_by_final_fuel().loc["gases"])
            * (1 - share_conv_vs_total_gas_extraction_eu()),
        )
    )


@component.add(
    name="real_extraction_conv_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "extraction_conv_gas_ej": 1,
        "extraction_conv_gas_tot_agg": 1,
    },
)
def real_extraction_conv_gas():
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_conv_gas_ej(),
        lambda: extraction_conv_gas_tot_agg(),
    )


@component.add(
    name="real_extraction_conv_gas_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_conv_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "share_conv_vs_total_gas_extraction_eu": 1,
    },
)
def real_extraction_conv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return float(
        np.maximum(
            0,
            real_extraction_conv_gas()
            - (
                ped_nat_gas_for_gtl_ej()
                + float(nonenergy_use_demand_by_final_fuel().loc["gases"])
            )
            * share_conv_vs_total_gas_extraction_eu(),
        )
    )


@component.add(
    name="real_extraction_unconv_gas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_gas": 1,
        "extraction_unconv_gas_ej": 1,
        "extraction_unconv_gas_tot_agg": 1,
    },
)
def real_extraction_unconv_gas():
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_unconv_gas_ej(),
        lambda: extraction_unconv_gas_tot_agg(),
    )


@component.add(
    name="real_extraction_unconv_gas_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_unconv_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "share_conv_vs_total_gas_extraction_eu": 1,
    },
)
def real_extraction_unconv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return float(
        np.maximum(
            0,
            real_extraction_unconv_gas()
            - (
                ped_nat_gas_for_gtl_ej()
                + float(nonenergy_use_demand_by_final_fuel().loc["gases"])
            )
            * (1 - share_conv_vs_total_gas_extraction_eu()),
        )
    )


@component.add(
    name="remaining_extractable_fossil_gas_with_left_underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_tot_agg_gas": 1, "delay_gas_to_leave_underground": 1},
)
def remaining_extractable_fossil_gas_with_left_underground():
    """
    Remaining extractable fossil gas: corresponds to the difference between the Remaining Ultimate Recoverable Resources and the fossil gas that must be blocked underground (if such policy is enforced).
    """
    return float(np.maximum(0, rurr_tot_agg_gas() - delay_gas_to_leave_underground()))


@component.add(
    name="RURR_conv_gas",
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
    name="RURR_conv_gas_until_start_year_PLG",
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
    name="RURR_tot_agg_gas",
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
            "step": {"extraction_tot_agg_gas_ej": 1},
        }
    },
)
def rurr_tot_agg_gas():
    """
    RURR total aggregated natural gas.
    """
    return _integ_rurr_tot_agg_gas()


_integ_rurr_tot_agg_gas = Integ(
    lambda: -extraction_tot_agg_gas_ej(),
    lambda: if_then_else(
        separate_conv_and_unconv_gas() == 0,
        lambda: urr_tot_agg_gas() - cumulated_tot_agg_gas_extraction_to_1995(),
        lambda: 0,
    ),
    "_integ_rurr_tot_agg_gas",
)


@component.add(
    name="RURR_total_agg_fossil_gas_in_reference_year",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_total_agg_fossil_gas_in_reference_year": 1},
    other_deps={
        "_sampleiftrue_rurr_total_agg_fossil_gas_in_reference_year": {
            "initial": {},
            "step": {"time": 1, "year_reference_rurr": 1, "rurr_tot_agg_gas": 1},
        }
    },
)
def rurr_total_agg_fossil_gas_in_reference_year():
    """
    RURR in the year used to calculate the share to leave underground under the policy to leave in the ground the resource.
    """
    return _sampleiftrue_rurr_total_agg_fossil_gas_in_reference_year()


_sampleiftrue_rurr_total_agg_fossil_gas_in_reference_year = SampleIfTrue(
    lambda: time() == year_reference_rurr(),
    lambda: rurr_tot_agg_gas(),
    lambda: 0,
    "_sampleiftrue_rurr_total_agg_fossil_gas_in_reference_year",
)


@component.add(
    name="RURR_unconv_gas",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_unconv_gas": 1},
    other_deps={
        "_integ_rurr_unconv_gas": {
            "initial": {
                "urr_unconv_gas": 1,
                "cumulated_unconv_gas_extraction_to_1995": 1,
                "separate_conv_and_unconv_gas": 1,
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
    name="RURR_unconv_gas_until_start_year_PLG",
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
    name="scarcity_conv_gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_extraction_conv_gas_ej": 4,
        "extraction_conv_gas_ej": 2,
        "exponent_availability_conv_gas": 1,
    },
)
def scarcity_conv_gas():
    """
    Priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached. If "scarcity conv gas"=1 there is no more available flow to be extracted from the conventional resource.
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
    name="scarcity_conv_gas_delayed_TS",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_scarcity_conv_gas_delayed_ts": 1},
    other_deps={
        "_delayfixed_scarcity_conv_gas_delayed_ts": {
            "initial": {"time_step": 1},
            "step": {"scarcity_conv_gas": 1},
        }
    },
)
def scarcity_conv_gas_delayed_ts():
    """
    "Scarcity conv gas" variable delayed 1 year. For the initial year we arbitrary chose the value "0" given that it will be endogenously calculated by the model for the following periods.
    """
    return _delayfixed_scarcity_conv_gas_delayed_ts()


_delayfixed_scarcity_conv_gas_delayed_ts = DelayFixed(
    lambda: scarcity_conv_gas(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_scarcity_conv_gas_delayed_ts",
)


@component.add(
    name="scarcity_conv_gas_stock",
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
    """
    Stock which accounts for the relative scarcity of conventional vs unconventional resource. For the initial year we arbitrary chose the value "0".
    """
    return _integ_scarcity_conv_gas_stock()


_integ_scarcity_conv_gas_stock = Integ(
    lambda: increase_scarcity_conv_gas(), lambda: 0, "_integ_scarcity_conv_gas_stock"
)


@component.add(
    name='"separate_conv_and_unconv_gas?"',
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "separate_conv_and_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_separate_conv_and_unconv_gas",
)


@component.add(
    name="share_conv_gas_vs_tot_agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_unconv_gas_vs_tot_agg": 1},
)
def share_conv_gas_vs_tot_agg():
    return 1 - share_unconv_gas_vs_tot_agg()


@component.add(
    name="share_conv_vs_total_gas_extraction_EU",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas": 2, "real_extraction_unconv_gas": 1},
)
def share_conv_vs_total_gas_extraction_eu():
    """
    Share of conventional gas vs total gas extracted.
    """
    return zidz(
        real_extraction_conv_gas(),
        real_extraction_conv_gas() + real_extraction_unconv_gas(),
    )


@component.add(
    name="share_gas_for_oil_refinery_gains",
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
    name="share_RURR_conv_gas_to_leave_underground",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_RURR_conv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_conv_gas_to_leave_underground",
)


@component.add(
    name="share_RURR_tot_agg_fossil_gas_to_leave_underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_tot_agg_fossil_gas_to_leave_underground"
    },
)
def share_rurr_tot_agg_fossil_gas_to_leave_underground():
    """
    RURR's total aggregated fossil gas to be left in the ground as a share of the RURR in the reference year.
    """
    return _ext_constant_share_rurr_tot_agg_fossil_gas_to_leave_underground()


_ext_constant_share_rurr_tot_agg_fossil_gas_to_leave_underground = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_RURR_agg_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_tot_agg_fossil_gas_to_leave_underground",
)


@component.add(
    name="share_RURR_unconv_gas_to_leave_underground",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_RURR_unconv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_unconv_gas_to_leave_underground",
)


@component.add(
    name="share_unconv_gas_vs_tot_agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "evolution_share_unconv_gas_vs_tot_agg": 1,
        "ped_nat_gas_ej": 1,
        "historic_unconv_gas": 1,
    },
)
def share_unconv_gas_vs_tot_agg():
    """
    Evolution of the share of unconventional gas vs total aggregated gas.
    """
    return if_then_else(
        time() > 2012,
        lambda: float(np.minimum(evolution_share_unconv_gas_vs_tot_agg(), 1)),
        lambda: zidz(historic_unconv_gas(), ped_nat_gas_ej()),
    )


@component.add(
    name="share_unconv_gas_vs_tot_agg_in_2050",
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
    r"../energy.xlsx",
    "Catalonia",
    "share_unconv_vs_agg_gas_in_2050",
    {},
    _root,
    {},
    "_ext_constant_share_unconv_gas_vs_tot_agg_in_2050",
)


@component.add(
    name="Start_policy_leave_in_ground_conv_gas",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_policy_year_conv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_conv_gas",
)


@component.add(
    name="Start_policy_leave_in_ground_unconv_gas",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_policy_year_unconv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_unconv_gas",
)


@component.add(
    name="Start_year_policy_leave_in_ground_fossil_gas",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_leave_in_ground_fossil_gas"
    },
)
def start_year_policy_leave_in_ground_fossil_gas():
    """
    Year when the policy to progressively leave fossil gas in the ground enters into force.
    """
    return _ext_constant_start_year_policy_leave_in_ground_fossil_gas()


_ext_constant_start_year_policy_leave_in_ground_fossil_gas = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_policy_year_agg_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_leave_in_ground_fossil_gas",
)


@component.add(
    name="table_max_extraction_agg_gas",
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
    r"../energy.xlsx",
    "Catalonia",
    "RURR_agg_gas",
    "max_extraction_agg_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_agg_gas",
)


@component.add(
    name="table_max_extraction_conv_gas",
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
    r"../energy.xlsx",
    "Catalonia",
    "RURR_conv_gas",
    "max_extraction_conv_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_conv_gas",
)


@component.add(
    name="table_max_extraction_unconv_gas",
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
    r"../energy.xlsx",
    "Catalonia",
    "RURR_unconv_gas",
    "max_extraction_unconv_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_unconv_gas",
)


@component.add(
    name="Tot_RURR_conv_gas",
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
    name="Tot_RURR_unconv_gas",
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
    name="total_agg_fossil_gas_to_leave_underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_rurr_tot_agg_fossil_gas_to_leave_underground": 1,
        "rurr_total_agg_fossil_gas_in_reference_year": 1,
    },
)
def total_agg_fossil_gas_to_leave_underground():
    """
    Total aggregated natural gas to be left underground due to the application of a policy.
    """
    return (
        share_rurr_tot_agg_fossil_gas_to_leave_underground()
        * rurr_total_agg_fossil_gas_in_reference_year()
    )


@component.add(
    name="Total_conv_gas_left_in_ground",
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
    name="Total_unconv_gas_left_in_ground",
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
    name="unconv_gas_to_leave_underground",
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
    name="URR_conv_gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_gas": 1, "urr_conv_gas_input": 1},
)
def urr_conv_gas():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1, lambda: urr_conv_gas_input(), lambda: 0
    )


@component.add(
    name="URR_conv_gas_input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_conv_gas_input"},
)
def urr_conv_gas_input():
    return _ext_constant_urr_conv_gas_input()


_ext_constant_urr_conv_gas_input = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "URR_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_conv_gas_input",
)


@component.add(
    name="URR_tot_agg_gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_gas": 1, "urr_total_gas_input": 1},
)
def urr_tot_agg_gas():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1, lambda: 0, lambda: urr_total_gas_input()
    )


@component.add(
    name="URR_total_gas_input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_total_gas_input"},
)
def urr_total_gas_input():
    """
    Input of total aggregated fossil gas URR (Ultimate Recoverable Resources).
    """
    return _ext_constant_urr_total_gas_input()


_ext_constant_urr_total_gas_input = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "URR_agg_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_total_gas_input",
)


@component.add(
    name="URR_unconv_gas",
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
    name="URR_unconv_gas_input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_unconv_gas_input"},
)
def urr_unconv_gas_input():
    return _ext_constant_urr_unconv_gas_input()


_ext_constant_urr_unconv_gas_input = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "URR_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_unconv_gas_input",
)


@component.add(
    name='"Year_scarcity_total_nat._gas"',
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_nat_gas_cat_": 1, "time": 1},
)
def year_scarcity_total_nat_gas():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(
        abundance_total_nat_gas_cat_() > 0.95, lambda: 0, lambda: time()
    )


@component.add(
    name="year_to_end_fossil_gas_extraction",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_tot_agg_gas_ej": 2,
        "remaining_extractable_fossil_gas_with_left_underground": 2,
        "time": 1,
    },
)
def year_to_end_fossil_gas_extraction():
    """
    Year when fossil gas extraction has to end in order to comply with leave in ground policy. This year is dinamically determined, accordig to the actual extraction rate.
    """
    return if_then_else(
        np.logical_or(
            extraction_tot_agg_gas_ej() <= 0,
            remaining_extractable_fossil_gas_with_left_underground() <= 0,
        ),
        lambda: 0,
        lambda: 2
        * remaining_extractable_fossil_gas_with_left_underground()
        / extraction_tot_agg_gas_ej()
        + time(),
    )
