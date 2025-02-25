"""
Module energy.availability.oil_extraction
Translated using PySD version 3.14.0
"""

@component.add(
    name="abundance total oil EU",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 3, "pes_total_oil_ej_eu": 2},
)
def abundance_total_oil_eu():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_total_oil_ej() < pes_total_oil_ej_eu(),
        lambda: 1,
        lambda: 1
        - zidz(ped_total_oil_ej() - pes_total_oil_ej_eu(), ped_total_oil_ej()),
    )


@component.add(
    name="abundance unconv oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 4, "real_extraction_unconv_oil_ej": 2},
)
def abundance_unconv_oil():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that unconventional oil extractione is far to cover to whole oil demand, if "abundance unconv oil"=0 it means that unconventional oil extraction covers the whole demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() == 0,
        lambda: 0,
        lambda: if_then_else(
            ped_total_oil_ej() > real_extraction_unconv_oil_ej(),
            lambda: (ped_total_oil_ej() - real_extraction_unconv_oil_ej())
            / ped_total_oil_ej(),
            lambda: 0,
        ),
    )


@component.add(
    name="abundance unconv oil2",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_unconv_oil_stock": 1},
)
def abundance_unconv_oil2():
    """
    Adaptation of the parameter abundance for better behaviour of the model. This variable limits the growth of a technology supplying a particular final energy type when its supply increases its share in relation to the total supply of this energy type (to avoid overshootings).
    """
    return abundance_unconv_oil_stock()


@component.add(
    name="abundance unconv oil delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_abundance_unconv_oil_delayed_1yr": 1},
    other_deps={
        "_delayfixed_abundance_unconv_oil_delayed_1yr": {
            "initial": {},
            "step": {"abundance_unconv_oil": 1},
        }
    },
)
def abundance_unconv_oil_delayed_1yr():
    return _delayfixed_abundance_unconv_oil_delayed_1yr()


_delayfixed_abundance_unconv_oil_delayed_1yr = DelayFixed(
    lambda: abundance_unconv_oil(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_abundance_unconv_oil_delayed_1yr",
)


@component.add(
    name="abundance unconv oil stock",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_abundance_unconv_oil_stock": 1},
    other_deps={
        "_integ_abundance_unconv_oil_stock": {
            "initial": {},
            "step": {"increase_abundance_unconv_oil": 1},
        }
    },
)
def abundance_unconv_oil_stock():
    return _integ_abundance_unconv_oil_stock()


_integ_abundance_unconv_oil_stock = Integ(
    lambda: increase_abundance_unconv_oil(),
    lambda: 1,
    "_integ_abundance_unconv_oil_stock",
)


@component.add(
    name="check liquids delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_check_liquids_delayed_1yr": 1},
    other_deps={
        "_delayfixed_check_liquids_delayed_1yr": {
            "initial": {},
            "step": {"check_liquids": 1},
        }
    },
)
def check_liquids_delayed_1yr():
    """
    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return _delayfixed_check_liquids_delayed_1yr()


_delayfixed_check_liquids_delayed_1yr = DelayFixed(
    lambda: check_liquids(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_check_liquids_delayed_1yr",
)


@component.add(
    name='"constrain liquids exogenous growth? delayed 1yr"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr": 1},
    other_deps={
        "_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr": {
            "initial": {},
            "step": {"constrain_liquids_exogenous_growth": 1},
        }
    },
)
def constrain_liquids_exogenous_growth_delayed_1yr():
    return _delayfixed_constrain_liquids_exogenous_growth_delayed_1yr()


_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr = DelayFixed(
    lambda: constrain_liquids_exogenous_growth(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr",
)


@component.add(
    name="conv oil to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_conv_oil_in_reference_year": 1,
        "share_rurr_conv_oil_to_leave_underground": 1,
    },
)
def conv_oil_to_leave_underground():
    """
    Conventional fossil oil to be left underground due to the application of policies that leave oil underground.
    """
    return (
        rurr_conv_oil_in_reference_year() * share_rurr_conv_oil_to_leave_underground()
    )


@component.add(
    name="cumulated conv oil extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_conv_oil_extraction": 1},
    other_deps={
        "_integ_cumulated_conv_oil_extraction": {
            "initial": {"cumulated_conv_oil_extraction_to_1995": 1},
            "step": {"extraction_conv_oil": 1},
        }
    },
)
def cumulated_conv_oil_extraction():
    """
    Cumulated conventional oil extraction.
    """
    return _integ_cumulated_conv_oil_extraction()


_integ_cumulated_conv_oil_extraction = Integ(
    lambda: extraction_conv_oil(),
    lambda: cumulated_conv_oil_extraction_to_1995(),
    "_integ_cumulated_conv_oil_extraction",
)


@component.add(
    name="cumulated conv oil extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulated_conv_oil_extraction_to_1995"},
)
def cumulated_conv_oil_extraction_to_1995():
    """
    Cumulated conventional oil extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_conv_oil_extraction_to_1995()


_ext_constant_cumulated_conv_oil_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cumulative_conventional_oil_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_conv_oil_extraction_to_1995",
)


@component.add(
    name="cumulated tot agg extraction to 1995",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cumulated_conv_oil_extraction_to_1995": 1,
        "cumulated_unconv_oil_extraction_to_1995": 1,
    },
)
def cumulated_tot_agg_extraction_to_1995():
    """
    Cumulated total aggregated oil extraction to 1995.
    """
    return (
        cumulated_conv_oil_extraction_to_1995()
        + cumulated_unconv_oil_extraction_to_1995()
    )


@component.add(
    name="cumulated tot agg oil extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_tot_agg_oil_extraction": 1},
    other_deps={
        "_integ_cumulated_tot_agg_oil_extraction": {
            "initial": {"cumulated_tot_agg_extraction_to_1995": 1},
            "step": {"extraction_tot_agg_oil": 1},
        }
    },
)
def cumulated_tot_agg_oil_extraction():
    """
    Cumulated total aggregated oil extraction.
    """
    return _integ_cumulated_tot_agg_oil_extraction()


_integ_cumulated_tot_agg_oil_extraction = Integ(
    lambda: extraction_tot_agg_oil(),
    lambda: cumulated_tot_agg_extraction_to_1995(),
    "_integ_cumulated_tot_agg_oil_extraction",
)


@component.add(
    name="cumulated unconv oil extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_unconv_oil_extraction": 1},
    other_deps={
        "_integ_cumulated_unconv_oil_extraction": {
            "initial": {"cumulated_unconv_oil_extraction_to_1995": 1},
            "step": {"extraction_unconv_oil": 1},
        }
    },
)
def cumulated_unconv_oil_extraction():
    """
    Cumulated unconventional oil extracted.
    """
    return _integ_cumulated_unconv_oil_extraction()


_integ_cumulated_unconv_oil_extraction = Integ(
    lambda: extraction_unconv_oil(),
    lambda: cumulated_unconv_oil_extraction_to_1995(),
    "_integ_cumulated_unconv_oil_extraction",
)


@component.add(
    name="cumulated unconv oil extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_cumulated_unconv_oil_extraction_to_1995"
    },
)
def cumulated_unconv_oil_extraction_to_1995():
    """
    Cumulated unconventional oil extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_unconv_oil_extraction_to_1995()


_ext_constant_cumulated_unconv_oil_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cumulative_unconventional_oil_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_unconv_oil_extraction_to_1995",
)


@component.add(
    name="delay conv oil to leave underground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_delay_conv_oil_to_leave_underground": 1},
    other_deps={
        "_sampleiftrue_delay_conv_oil_to_leave_underground": {
            "initial": {},
            "step": {
                "time": 1,
                "start_year_policy_leave_in_ground_conv_oil": 1,
                "conv_oil_to_leave_underground": 1,
            },
        }
    },
)
def delay_conv_oil_to_leave_underground():
    """
    This function is used so that the amount of oil to be left underground is substracted from the (technological) RURR from the Start year to leave oil undeground onwards.
    """
    return _sampleiftrue_delay_conv_oil_to_leave_underground()


_sampleiftrue_delay_conv_oil_to_leave_underground = SampleIfTrue(
    lambda: time() == start_year_policy_leave_in_ground_conv_oil(),
    lambda: conv_oil_to_leave_underground(),
    lambda: 0,
    "_sampleiftrue_delay_conv_oil_to_leave_underground",
)


@component.add(
    name="delay oil to leave underground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_delay_oil_to_leave_underground": 1},
    other_deps={
        "_sampleiftrue_delay_oil_to_leave_underground": {
            "initial": {},
            "step": {
                "time": 1,
                "start_year_policy_leave_in_ground_fossil_oil": 1,
                "total_agg_fossil_oil_to_leave_underground": 1,
            },
        }
    },
)
def delay_oil_to_leave_underground():
    """
    This function is used so that the amount of oil to be left underground is substracted from the (technological) RURR from the Start year to leave oil undeground onwards.
    """
    return _sampleiftrue_delay_oil_to_leave_underground()


_sampleiftrue_delay_oil_to_leave_underground = SampleIfTrue(
    lambda: time() == start_year_policy_leave_in_ground_fossil_oil(),
    lambda: total_agg_fossil_oil_to_leave_underground(),
    lambda: 0,
    "_sampleiftrue_delay_oil_to_leave_underground",
)


@component.add(
    name="delay unconv oil to leave underground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_delay_unconv_oil_to_leave_underground": 1},
    other_deps={
        "_sampleiftrue_delay_unconv_oil_to_leave_underground": {
            "initial": {},
            "step": {
                "time": 1,
                "start_year_policy_leave_in_ground_unconv_oil": 1,
                "unconv_oil_to_leave_underground": 1,
            },
        }
    },
)
def delay_unconv_oil_to_leave_underground():
    """
    This function is used so that the amount of oil to be left underground is substracted from the (technological) RURR from the Start year to leave oil undeground onwards.
    """
    return _sampleiftrue_delay_unconv_oil_to_leave_underground()


_sampleiftrue_delay_unconv_oil_to_leave_underground = SampleIfTrue(
    lambda: time() == start_year_policy_leave_in_ground_unconv_oil(),
    lambda: unconv_oil_to_leave_underground(),
    lambda: 0,
    "_sampleiftrue_delay_unconv_oil_to_leave_underground",
)


@component.add(
    name="Demand conv oil EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "extraction_unconv_oil": 1},
)
def demand_conv_oil_ej():
    """
    Demand of conventional oil. It is assumed that conventional oil covers the rest of the liquids demand after accounting for the contributions from other liquids and unconventional oil.
    """
    return np.maximum(ped_total_oil_ej() - extraction_unconv_oil(), 0)


@component.add(
    name="evol conv oil extraction rate constraint",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_to_end_conv_oil_extraction": 2,
        "extraction_conv_oil": 1,
    },
)
def evol_conv_oil_extraction_rate_constraint():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets.
    """
    return if_then_else(
        time() < year_to_end_conv_oil_extraction(),
        lambda: -extraction_conv_oil() / (year_to_end_conv_oil_extraction() - time()),
        lambda: 0,
    )


@component.add(
    name="evol conv oil extraction rate delayed",
    units="EJ/(year*year)",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_evol_conv_oil_extraction_rate_delayed": 1},
    other_deps={
        "_delayfixed_evol_conv_oil_extraction_rate_delayed": {
            "initial": {"time_step": 1},
            "step": {"evol_conv_oil_extraction_rate_constraint": 1},
        }
    },
)
def evol_conv_oil_extraction_rate_delayed():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets. Delayed one time step.
    """
    return _delayfixed_evol_conv_oil_extraction_rate_delayed()


_delayfixed_evol_conv_oil_extraction_rate_delayed = DelayFixed(
    lambda: evol_conv_oil_extraction_rate_constraint(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_evol_conv_oil_extraction_rate_delayed",
)


@component.add(
    name="evol fossil oil extraction rate constraint",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_to_end_fossil_oil_extraction": 2,
        "extraction_tot_agg_oil": 1,
    },
)
def evol_fossil_oil_extraction_rate_constraint():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets.
    """
    return if_then_else(
        time() < year_to_end_fossil_oil_extraction(),
        lambda: -extraction_tot_agg_oil()
        / (year_to_end_fossil_oil_extraction() - time()),
        lambda: 0,
    )


@component.add(
    name="evol fossil oil extraction rate delayed",
    units="EJ/(year*year)",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_evol_fossil_oil_extraction_rate_delayed": 1},
    other_deps={
        "_delayfixed_evol_fossil_oil_extraction_rate_delayed": {
            "initial": {"time_step": 1},
            "step": {"evol_fossil_oil_extraction_rate_constraint": 1},
        }
    },
)
def evol_fossil_oil_extraction_rate_delayed():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets. Delayed one time step.
    """
    return _delayfixed_evol_fossil_oil_extraction_rate_delayed()


_delayfixed_evol_fossil_oil_extraction_rate_delayed = DelayFixed(
    lambda: evol_fossil_oil_extraction_rate_constraint(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_evol_fossil_oil_extraction_rate_delayed",
)


@component.add(
    name="evol unconv oil extraction rate constraint",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_to_end_unconv_oil_extraction": 2,
        "extraction_unconv_oil": 1,
    },
)
def evol_unconv_oil_extraction_rate_constraint():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets.
    """
    return if_then_else(
        time() < year_to_end_unconv_oil_extraction(),
        lambda: -extraction_unconv_oil()
        / (year_to_end_unconv_oil_extraction() - time()),
        lambda: 0,
    )


@component.add(
    name="evol unconv oil extraction rate delayed",
    units="EJ/(year*year)",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_evol_unconv_oil_extraction_rate_delayed": 1},
    other_deps={
        "_delayfixed_evol_unconv_oil_extraction_rate_delayed": {
            "initial": {"time_step": 1},
            "step": {"evol_unconv_oil_extraction_rate_constraint": 1},
        }
    },
)
def evol_unconv_oil_extraction_rate_delayed():
    """
    Slope of linear fit to limit extraction from current extraction to zero, where the area under the curve is the remainig extractable resource to comply with leave in ground targets. Delayed one time step.
    """
    return _delayfixed_evol_unconv_oil_extraction_rate_delayed()


_delayfixed_evol_unconv_oil_extraction_rate_delayed = DelayFixed(
    lambda: evol_unconv_oil_extraction_rate_constraint(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_evol_unconv_oil_extraction_rate_delayed",
)


@component.add(
    name="evolution share unconv oil vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_unconv_oil_vs_tot_agg_in_2050": 3,
        "year_2050": 3,
        "year_2012": 2,
        "time": 1,
    },
)
def evolution_share_unconv_oil_vs_tot_agg():
    """
    Linear relation of the evolution of the share of unconventional oil vs total aggregated oil.
    """
    return (share_unconv_oil_vs_tot_agg_in_2050() - 0.059) / (
        year_2050() - year_2012()
    ) * time() + (
        share_unconv_oil_vs_tot_agg_in_2050()
        - (
            (share_unconv_oil_vs_tot_agg_in_2050() - 0.059)
            / (year_2050() - year_2012())
        )
        * year_2050()
    )


@component.add(
    name="exponent availability conv oil",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exponent_availability_conv_oil():
    """
    The smaller the exponent, more priority to conventional vs unconventional oil: 1: lineal 1/2: square root 1/3: cube root ...
    """
    return 1 / 4


@component.add(
    name="extraction conv oil",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def extraction_conv_oil():
    """
    Annual extraction of conventional oil. IF THEN ELSE(Time<2012, PED domestic EU total oil EJ, IF THEN ELSE(Activate force leaving underground = 0, MIN(PED domestic EU total oil EJ, max extraction conv oil), MIN(MIN(PED domestic EU total oil EJ, max extraction conv oil), remaining extractable conv oil with left underground))) #"PED domestic EU conv. oil EJ" #IF THEN ELSE(Time<2016, PED domestic EU total oil EJ, IF THEN ELSE(Activate force leaving underground = 0, MIN(PED domestic EU total oil EJ, max extraction total agg oil), MIN(MIN(PED domestic EU total oil EJ, max extraction total agg oil), remaining extractable fossil oil with left underground))) # IF THEN ELSE(Time<2016, "PED domestic EU conv. oil EJ", IF THEN ELSE(Activate force leaving underground = 0, MIN("PED domestic EU conv. oil EJ", max extraction conv oil), MIN(MIN("PED domestic EU conv. oil EJ", max extraction conv oil), remaining extractable conv oil with left underground)))
    """
    return 1


@component.add(
    name="extraction conv oil delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_conv_oil_delayed": 1},
    other_deps={
        "_delayfixed_extraction_conv_oil_delayed": {
            "initial": {"time_step": 1},
            "step": {"extraction_conv_oil": 1},
        }
    },
)
def extraction_conv_oil_delayed():
    return _delayfixed_extraction_conv_oil_delayed()


_delayfixed_extraction_conv_oil_delayed = DelayFixed(
    lambda: extraction_conv_oil(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_extraction_conv_oil_delayed",
)


@component.add(
    name='"extraction conv oil - tot agg"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_oil": 1, "share_conv_oil_vs_tot_agg": 1},
)
def extraction_conv_oil_tot_agg():
    return extraction_tot_agg_oil() * share_conv_oil_vs_tot_agg()


@component.add(
    name="extraction fossil oil agg delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_fossil_oil_agg_delayed": 1},
    other_deps={
        "_delayfixed_extraction_fossil_oil_agg_delayed": {
            "initial": {"time_step": 1},
            "step": {"extraction_tot_agg_oil": 1},
        }
    },
)
def extraction_fossil_oil_agg_delayed():
    """
    Annual extraction of aggregated fossil oil delayed one year. The delay allows to progressively limit extraction (due to leave underground policies) using previous extraction rates.
    """
    return _delayfixed_extraction_fossil_oil_agg_delayed()


_delayfixed_extraction_fossil_oil_agg_delayed = DelayFixed(
    lambda: extraction_tot_agg_oil(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_extraction_fossil_oil_agg_delayed",
)


@component.add(
    name="extraction tot agg oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ped_domestic_ff": 3,
        "activate_force_leaving_underground": 1,
        "remaining_extractable_fossil_oil_with_left_underground": 1,
        "nvs_1_year": 1,
        "max_extraction_total_agg_oil": 2,
    },
)
def extraction_tot_agg_oil():
    """
    Annual extraction of total aggregated oil.
    """
    return if_then_else(
        time() < 2016,
        lambda: float(ped_domestic_ff().loc["liquids"]),
        lambda: if_then_else(
            activate_force_leaving_underground() == 0,
            lambda: np.minimum(
                float(ped_domestic_ff().loc["liquids"]), max_extraction_total_agg_oil()
            ),
            lambda: np.minimum(
                np.minimum(
                    float(ped_domestic_ff().loc["liquids"]),
                    max_extraction_total_agg_oil(),
                ),
                remaining_extractable_fossil_oil_with_left_underground() / nvs_1_year(),
            ),
        ),
    )


@component.add(
    name="extraction unconv oil",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def extraction_unconv_oil():
    """
    Time > 2012? IF THEN ELSE(Time<2016, Historic unconv oil domestic EU extracted, IF THEN ELSE(Activate force leaving underground = 0, MIN("PED domestic EU unconv. oil EJ", max extraction unconv oil), MIN(MIN("PED domestic EU unconv. oil EJ", max extraction unconv oil), remaining extractable unconv oil with left underground))) #MIN(IF THEN ELSE(RURR unconv oil<0,0, IF THEN ELSE(Time>2012, IF THEN ELSE("separate conv and unconv oil?"=1, MIN(max extraction unconv oil technical, max unconv oil growth extraction EJ ),0), Historic unconv oil domestic EU extracted)),PED total oil EJ)
    """
    return 1


@component.add(
    name="extraction unconv oil delayed",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def extraction_unconv_oil_delayed():
    """
    Extraction of unconventional oil delayed 1 year. Data from Mohr et al (2015) for 1989. # DELAY FIXED(extraction unconv oil, TIME STEP, 1.09)
    """
    return 1


@component.add(
    name="extraction unconv oil delayed 2",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_unconv_oil_delayed_2": 1},
    other_deps={
        "_delayfixed_extraction_unconv_oil_delayed_2": {
            "initial": {"time_step": 1},
            "step": {"extraction_unconv_oil": 1},
        }
    },
)
def extraction_unconv_oil_delayed_2():
    """
    # THIS NAME NEEDS TO BE CHANGED AND THE REASONS BEHIND THE DUPLICTY OF THIS VARIABLE MUST BE EXPLORED. THIS MAY POTENTIALLY RESULT IN THE VIEW BEING CHANGED.
    """
    return _delayfixed_extraction_unconv_oil_delayed_2()


_delayfixed_extraction_unconv_oil_delayed_2 = DelayFixed(
    lambda: extraction_unconv_oil(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_extraction_unconv_oil_delayed_2",
)


@component.add(
    name='"extraction unconv oil - tot agg"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_tot_agg_oil": 1, "share_unconv_oil_vs_tot_agg": 1},
)
def extraction_unconv_oil_tot_agg():
    return extraction_tot_agg_oil() * share_unconv_oil_vs_tot_agg()


@component.add(
    name="increase abundance unconv oil",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "abundance_unconv_oil": 1,
        "abundance_unconv_oil_delayed_1yr": 1,
        "nvs_1_year": 1,
    },
)
def increase_abundance_unconv_oil():
    return (abundance_unconv_oil() - abundance_unconv_oil_delayed_1yr()) / nvs_1_year()


@component.add(
    name="increase scarcity conv oil",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_conv_oil": 1,
        "scarcity_conv_oil_delayed_1yr": 1,
        "nvs_1_year": 1,
    },
)
def increase_scarcity_conv_oil():
    return (scarcity_conv_oil() - scarcity_conv_oil_delayed_1yr()) / nvs_1_year()


@component.add(
    name="max extraction conv oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_force_leaving_underground": 1,
        "max_extraction_conv_oil_technical": 3,
        "time": 1,
        "start_year_policy_leave_in_ground_conv_oil": 1,
        "max_extraction_conv_oil_policy": 1,
    },
)
def max_extraction_conv_oil():
    """
    Maximum extraction of convetnional oil due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return if_then_else(
        activate_force_leaving_underground() == 0,
        lambda: max_extraction_conv_oil_technical(),
        lambda: if_then_else(
            time() > start_year_policy_leave_in_ground_conv_oil(),
            lambda: np.minimum(
                max_extraction_conv_oil_technical(), max_extraction_conv_oil_policy()
            ),
            lambda: max_extraction_conv_oil_technical(),
        ),
    )


@component.add(
    name="max extraction conv oil policy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_conv_oil_extraction_rate_delayed": 1,
        "time_step": 1,
        "extraction_conv_oil": 1,
    },
)
def max_extraction_conv_oil_policy():
    """
    Maximum extraction of conventional oil due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return evol_conv_oil_extraction_rate_delayed() * time_step() + extraction_conv_oil()


@component.add(
    name="max extraction conv oil technical",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_oil": 1,
        "rurr_conv_oil": 1,
        "table_max_extraction_conv_oil": 1,
    },
)
def max_extraction_conv_oil_technical():
    """
    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: table_max_extraction_conv_oil(rurr_conv_oil()),
        lambda: 0,
    )


@component.add(
    name="max extraction total agg oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_force_leaving_underground": 1,
        "max_extraction_total_agg_oil_technical": 3,
        "time": 1,
        "max_extraction_total_agg_oil_policy": 1,
        "start_year_policy_leave_in_ground_fossil_oil": 1,
    },
)
def max_extraction_total_agg_oil():
    """
    Maximum extraction of aggregated oil due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return if_then_else(
        activate_force_leaving_underground() == 0,
        lambda: max_extraction_total_agg_oil_technical(),
        lambda: if_then_else(
            time() > start_year_policy_leave_in_ground_fossil_oil(),
            lambda: np.minimum(
                max_extraction_total_agg_oil_technical(),
                max_extraction_total_agg_oil_policy(),
            ),
            lambda: max_extraction_total_agg_oil_technical(),
        ),
    )


@component.add(
    name="max extraction total agg oil policy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_fossil_oil_extraction_rate_delayed": 1,
        "time_step": 1,
        "extraction_fossil_oil_agg_delayed": 1,
    },
)
def max_extraction_total_agg_oil_policy():
    """
    Maximum extraction of aggregated oil due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return (
        evol_fossil_oil_extraction_rate_delayed() * time_step()
        + extraction_fossil_oil_agg_delayed()
    )


@component.add(
    name="max extraction total agg oil technical",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_oil": 1,
        "rurr_tot_agg_oil": 1,
        "table_max_extraction_agg_oil": 1,
    },
)
def max_extraction_total_agg_oil_technical():
    """
    Maximum extraction of aggregated fossil oil due to technical constraints (Hubbert).
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 0,
        lambda: table_max_extraction_agg_oil(rurr_tot_agg_oil()),
        lambda: 0,
    )


@component.add(
    name="max extraction unconv oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_force_leaving_underground": 1,
        "max_extraction_unconv_oil_technical": 3,
        "time": 1,
        "max_extraction_unconv_oil_policy": 1,
        "start_year_policy_leave_in_ground_unconv_oil": 1,
    },
)
def max_extraction_unconv_oil():
    return if_then_else(
        activate_force_leaving_underground() == 0,
        lambda: max_extraction_unconv_oil_technical(),
        lambda: if_then_else(
            time() > start_year_policy_leave_in_ground_unconv_oil(),
            lambda: np.minimum(
                max_extraction_unconv_oil_technical(),
                max_extraction_unconv_oil_policy(),
            ),
            lambda: max_extraction_unconv_oil_technical(),
        ),
    )


@component.add(
    name="max extraction unconv oil policy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_unconv_oil_extraction_rate_delayed": 1,
        "time_step": 1,
        "extraction_unconv_oil": 1,
    },
)
def max_extraction_unconv_oil_policy():
    """
    Maximum extraction of unconventional oil due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return (
        evol_unconv_oil_extraction_rate_delayed() * time_step()
        + extraction_unconv_oil()
    )


@component.add(
    name="max extraction unconv oil technical",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_unconv_oil": 1, "table_max_extraction_unconv_oil": 1},
)
def max_extraction_unconv_oil_technical():
    """
    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_unconv_oil(rurr_unconv_oil())


@component.add(
    name="max unconv oil growth extraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_constraint_growth_extraction_unconv_oil": 1,
        "time_step": 1,
        "scarcity_conv_oil_stock": 1,
        "abundance_unconv_oil2": 1,
    },
)
def max_unconv_oil_growth_extraction():
    """
    Constraint to maximum annual unconventional gas extraction (%). This constraint is affected by the relative scarcity of conventional vs unconventional resource (priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached).
    """
    return np.maximum(
        0,
        1
        + p_constraint_growth_extraction_unconv_oil()
        * time_step()
        * scarcity_conv_oil_stock()
        * abundance_unconv_oil2(),
    )


@component.add(
    name="max unconv oil growth extraction EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "check_liquids_delayed_1yr": 1,
        "extraction_unconv_oil_delayed": 2,
        "constrain_liquids_exogenous_growth_delayed_1yr": 1,
        "max_unconv_oil_growth_extraction": 1,
    },
)
def max_unconv_oil_growth_extraction_ej():
    """
    Constrained unconventional oil extraction growth (EJ/Year), i.e. maximum annual growth compatible with the constraint selected in the scenario.
    """
    return if_then_else(
        check_liquids_delayed_1yr() < 0,
        lambda: (1 + constrain_liquids_exogenous_growth_delayed_1yr())
        * extraction_unconv_oil_delayed(),
        lambda: extraction_unconv_oil_delayed() * max_unconv_oil_growth_extraction(),
    )


@component.add(
    name='"Mb/d per EJ/year"',
    units="Mb*year/(EJ*d)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mbd_per_ejyear():
    """
    Conversion between Mb/d to EJ/year.
    """
    return 0.479726


@component.add(
    name='"1 year"', units="year", comp_type="Constant", comp_subtype="Normal"
)
def nvs_1_year():
    return 1


@component.add(
    name="Oil refinery gains EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_refinery_gains_share": 1, "pes_oil_ej_delayed": 1},
)
def oil_refinery_gains_ej():
    """
    Oil refinery gains.
    """
    return oil_refinery_gains_share() * pes_oil_ej_delayed()


@component.add(
    name="Oil refinery gains share",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_oil_refinery_gains_share"},
)
def oil_refinery_gains_share():
    """
    We assume these energy gains are reached by applying natural gas as energy input. Historically, their share has been growing in the last decades (1.9% in 1980). WEO (2010) gives a 2.8% for the year 2009 and BP (2007) 2.6%. The value 2.7% is taken.
    """
    return _ext_constant_oil_refinery_gains_share()


_ext_constant_oil_refinery_gains_share = ExtConstant(
    "../energy.xlsx",
    "Global",
    "oil_refinery_gains_share",
    {},
    _root,
    {},
    "_ext_constant_oil_refinery_gains_share",
)


@component.add(
    name="P constraint growth extraction unconv oil",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_p_constraint_growth_extraction_unconv_oil"
    },
)
def p_constraint_growth_extraction_unconv_oil():
    """
    Constant constraint to annual extraction of unconventional oil.
    """
    return _ext_constant_p_constraint_growth_extraction_unconv_oil()


_ext_constant_p_constraint_growth_extraction_unconv_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_constraint_growth_unconv_oil",
    {},
    _root,
    {},
    "_ext_constant_p_constraint_growth_extraction_unconv_oil",
)


@component.add(
    name="PEC conv oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_oil_ej": 1, "imports_eu_conv_oil_from_row_ej": 1},
)
def pec_conv_oil():
    return real_extraction_conv_oil_ej() + imports_eu_conv_oil_from_row_ej()


@component.add(
    name="PEC unconv oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_unconv_oil_ej": 1,
        "imports_eu_unconv_oil_from_row_ej": 1,
    },
)
def pec_unconv_oil():
    return real_extraction_unconv_oil_ej() + imports_eu_unconv_oil_from_row_ej()


@component.add(
    name="PES oil EJ delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_pes_oil_ej_delayed": 1},
    other_deps={
        "_delayfixed_pes_oil_ej_delayed": {
            "initial": {"time_step": 1},
            "step": {"pes_total_oil_ej_eu": 1},
        }
    },
)
def pes_oil_ej_delayed():
    """
    PES total oil extraction delayed.
    """
    return _delayfixed_pes_oil_ej_delayed()


_delayfixed_pes_oil_ej_delayed = DelayFixed(
    lambda: pes_total_oil_ej_eu(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_pes_oil_ej_delayed",
)


@component.add(
    name='"PES oil Mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_total_oil_ej_eu": 1, "mbd_per_ejyear": 1},
)
def pes_oil_mbd():
    """
    Total oil (conventional + unconventional) extraction.
    """
    return pes_total_oil_ej_eu() * mbd_per_ejyear()


@component.add(
    name="PES total oil EJ EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_oil_ej": 1, "real_extraction_unconv_oil_ej": 1},
)
def pes_total_oil_ej_eu():
    """
    Total oil (conventional + unconventional) extraction.
    """
    return real_extraction_conv_oil_ej() + real_extraction_unconv_oil_ej()


@component.add(
    name="real consumption UE conv oil emissions relevant EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_conv_oil": 1,
        "share_conv_vs_total_oil_extraction_eu": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def real_consumption_ue_conv_oil_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional oil. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        pec_conv_oil()
        - float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
        * share_conv_vs_total_oil_extraction_eu(),
    )


@component.add(
    name="real consumption unconv oil emissions relevant EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_unconv_oil": 1,
        "share_conv_vs_total_oil_extraction_eu": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def real_consumption_unconv_oil_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        pec_unconv_oil()
        - float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
        * (1 - share_conv_vs_total_oil_extraction_eu()),
    )


@component.add(
    name="real extraction conv oil EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_oil": 1,
        "extraction_conv_oil": 1,
        "extraction_conv_oil_tot_agg": 1,
    },
)
def real_extraction_conv_oil_ej():
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: extraction_conv_oil(),
        lambda: extraction_conv_oil_tot_agg(),
    )


@component.add(
    name="real extraction conv oil emissions relevant EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_conv_oil_ej": 1,
        "share_conv_vs_total_oil_extraction_eu": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def real_extraction_conv_oil_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional oil, i.e. excepting the resource used for non-energy uses. We assume conventional and unconventional resource are used for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_conv_oil_ej()
        - float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
        * share_conv_vs_total_oil_extraction_eu(),
    )


@component.add(
    name='"real extraction conv oil Mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_oil_ej": 1, "mbd_per_ejyear": 1},
)
def real_extraction_conv_oil_mbd():
    return real_extraction_conv_oil_ej() * mbd_per_ejyear()


@component.add(
    name="real extraction unconv oil EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "separate_conv_and_unconv_oil": 1,
        "extraction_unconv_oil": 1,
        "extraction_unconv_oil_tot_agg": 1,
    },
)
def real_extraction_unconv_oil_ej():
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: extraction_unconv_oil(),
        lambda: extraction_unconv_oil_tot_agg(),
    )


@component.add(
    name="real extraction unconv oil emissions relevant EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_unconv_oil_ej": 1,
        "share_conv_vs_total_oil_extraction_eu": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def real_extraction_unconv_oil_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional oil, i.e. excepting the resource used for non-energy uses. We assume conventional and unconventional resource are used for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_unconv_oil_ej()
        - float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
        * (1 - share_conv_vs_total_oil_extraction_eu()),
    )


@component.add(
    name="remaining extractable conv oil with left underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_conv_oil": 1, "delay_conv_oil_to_leave_underground": 1},
)
def remaining_extractable_conv_oil_with_left_underground():
    """
    Remaining extractable resources, after substracting the amount that must be left underground to comply with policy targets.
    """
    return np.maximum(0, rurr_conv_oil() - delay_conv_oil_to_leave_underground())


@component.add(
    name="remaining extractable fossil oil with left underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_tot_agg_oil": 1, "delay_oil_to_leave_underground": 1},
)
def remaining_extractable_fossil_oil_with_left_underground():
    """
    Remaining extractable resources, after substracting the amount that must be left underground to comply with policy targets.
    """
    return np.maximum(0, rurr_tot_agg_oil() - delay_oil_to_leave_underground())


@component.add(
    name="remaining extractable unconv oil with left underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_unconv_oil": 1, "delay_unconv_oil_to_leave_underground": 1},
)
def remaining_extractable_unconv_oil_with_left_underground():
    return np.maximum(0, rurr_unconv_oil() - delay_unconv_oil_to_leave_underground())


@component.add(
    name="RURR conv oil",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_conv_oil": 1},
    other_deps={
        "_integ_rurr_conv_oil": {
            "initial": {
                "separate_conv_and_unconv_oil": 1,
                "urr_conv_oil": 1,
                "cumulated_conv_oil_extraction_to_1995": 1,
            },
            "step": {"extraction_conv_oil": 1},
        }
    },
)
def rurr_conv_oil():
    """
    RURR conventional oil.
    """
    return _integ_rurr_conv_oil()


_integ_rurr_conv_oil = Integ(
    lambda: -extraction_conv_oil(),
    lambda: if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: urr_conv_oil() - cumulated_conv_oil_extraction_to_1995(),
        lambda: 0,
    ),
    "_integ_rurr_conv_oil",
)


@component.add(
    name="RURR conv oil in reference year",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_conv_oil_in_reference_year": 1},
    other_deps={
        "_sampleiftrue_rurr_conv_oil_in_reference_year": {
            "initial": {},
            "step": {"time": 1, "year_reference_rurr": 1, "rurr_conv_oil": 1},
        }
    },
)
def rurr_conv_oil_in_reference_year():
    """
    RURR in the year used to calculate the share to leave underground under the policy to leave in the ground the resource.
    """
    return _sampleiftrue_rurr_conv_oil_in_reference_year()


_sampleiftrue_rurr_conv_oil_in_reference_year = SampleIfTrue(
    lambda: time() == year_reference_rurr(),
    lambda: rurr_conv_oil(),
    lambda: 0,
    "_sampleiftrue_rurr_conv_oil_in_reference_year",
)


@component.add(
    name="RURR tot agg oil",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_tot_agg_oil": 1},
    other_deps={
        "_integ_rurr_tot_agg_oil": {
            "initial": {
                "separate_conv_and_unconv_oil": 1,
                "cumulated_tot_agg_extraction_to_1995": 1,
                "urr_tot_agg_oil": 1,
            },
            "step": {"extraction_tot_agg_oil": 1},
        }
    },
)
def rurr_tot_agg_oil():
    """
    RURR total aggregated oil.
    """
    return _integ_rurr_tot_agg_oil()


_integ_rurr_tot_agg_oil = Integ(
    lambda: -extraction_tot_agg_oil(),
    lambda: if_then_else(
        separate_conv_and_unconv_oil() == 0,
        lambda: urr_tot_agg_oil() - cumulated_tot_agg_extraction_to_1995(),
        lambda: 0,
    ),
    "_integ_rurr_tot_agg_oil",
)


@component.add(
    name="RURR total agg fossil oil in reference year",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_total_agg_fossil_oil_in_reference_year": 1},
    other_deps={
        "_sampleiftrue_rurr_total_agg_fossil_oil_in_reference_year": {
            "initial": {},
            "step": {"time": 1, "year_reference_rurr": 1, "rurr_tot_agg_oil": 1},
        }
    },
)
def rurr_total_agg_fossil_oil_in_reference_year():
    """
    RURR in the year used to calculate the share to leave underground under the policy to leave in the ground the resource.
    """
    return _sampleiftrue_rurr_total_agg_fossil_oil_in_reference_year()


_sampleiftrue_rurr_total_agg_fossil_oil_in_reference_year = SampleIfTrue(
    lambda: time() == year_reference_rurr(),
    lambda: rurr_tot_agg_oil(),
    lambda: 0,
    "_sampleiftrue_rurr_total_agg_fossil_oil_in_reference_year",
)


@component.add(
    name="RURR unconv oil",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_unconv_oil": 1},
    other_deps={
        "_integ_rurr_unconv_oil": {
            "initial": {
                "urr_unconv_oil": 1,
                "cumulated_unconv_oil_extraction_to_1995": 1,
                "separate_conv_and_unconv_oil": 1,
            },
            "step": {"extraction_unconv_oil": 1},
        }
    },
)
def rurr_unconv_oil():
    """
    RURR unconventional oil.
    """
    return _integ_rurr_unconv_oil()


_integ_rurr_unconv_oil = Integ(
    lambda: -extraction_unconv_oil(),
    lambda: urr_unconv_oil()
    - cumulated_unconv_oil_extraction_to_1995() * separate_conv_and_unconv_oil(),
    "_integ_rurr_unconv_oil",
)


@component.add(
    name="RURR unconv oil in reference year",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_unconv_oil_in_reference_year": 1},
    other_deps={
        "_sampleiftrue_rurr_unconv_oil_in_reference_year": {
            "initial": {},
            "step": {"time": 1, "year_reference_rurr": 1, "rurr_unconv_oil": 1},
        }
    },
)
def rurr_unconv_oil_in_reference_year():
    """
    RURR in the year used to calculate the share to leave underground under the policy to leave in the ground the resource.
    """
    return _sampleiftrue_rurr_unconv_oil_in_reference_year()


_sampleiftrue_rurr_unconv_oil_in_reference_year = SampleIfTrue(
    lambda: time() == year_reference_rurr(),
    lambda: rurr_unconv_oil(),
    lambda: 0,
    "_sampleiftrue_rurr_unconv_oil_in_reference_year",
)


@component.add(
    name="scarcity conv oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_extraction_conv_oil_technical": 4,
        "exponent_availability_conv_oil": 1,
        "extraction_conv_oil": 2,
    },
)
def scarcity_conv_oil():
    """
    Priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached. If "scarcity conv oil"=1 there is no more available flow to be extracted from the conventional resource.
    """
    return if_then_else(
        max_extraction_conv_oil_technical() == 0,
        lambda: 0,
        lambda: if_then_else(
            max_extraction_conv_oil_technical() >= extraction_conv_oil(),
            lambda: 1
            - (
                (max_extraction_conv_oil_technical() - extraction_conv_oil())
                / max_extraction_conv_oil_technical()
            )
            ** exponent_availability_conv_oil(),
            lambda: 0,
        ),
    )


@component.add(
    name="scarcity conv oil delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_scarcity_conv_oil_delayed_1yr": 1},
    other_deps={
        "_delayfixed_scarcity_conv_oil_delayed_1yr": {
            "initial": {},
            "step": {"scarcity_conv_oil": 1},
        }
    },
)
def scarcity_conv_oil_delayed_1yr():
    """
    "Scarcity conv gas" variable delayed 1 year. For the initial year we arbitrary chose the value "0" given that it will be endogenously calculated by the model for the following periods.
    """
    return _delayfixed_scarcity_conv_oil_delayed_1yr()


_delayfixed_scarcity_conv_oil_delayed_1yr = DelayFixed(
    lambda: scarcity_conv_oil(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_scarcity_conv_oil_delayed_1yr",
)


@component.add(
    name="scarcity conv oil stock",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_scarcity_conv_oil_stock": 1},
    other_deps={
        "_integ_scarcity_conv_oil_stock": {
            "initial": {},
            "step": {"increase_scarcity_conv_oil": 1},
        }
    },
)
def scarcity_conv_oil_stock():
    """
    Stock which accounts for the relative scarcity of conventional vs unconventional resource. For the initial year we arbitrary chose the value "0".
    """
    return _integ_scarcity_conv_oil_stock()


_integ_scarcity_conv_oil_stock = Integ(
    lambda: increase_scarcity_conv_oil(), lambda: 0, "_integ_scarcity_conv_oil_stock"
)


@component.add(
    name='"separate conv and unconv oil?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_separate_conv_and_unconv_oil"},
)
def separate_conv_and_unconv_oil():
    """
    Switch to disaggregate between conventional and unconventional fuel: "1" = disaggregation, "0" = conv+unconv aggregated (all the oil flows then through the right side of this view, i.e. the "conventional oil" modelling side).
    """
    return _ext_constant_separate_conv_and_unconv_oil()


_ext_constant_separate_conv_and_unconv_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "separate_conv_and_unconv_oil",
    {},
    _root,
    {},
    "_ext_constant_separate_conv_and_unconv_oil",
)


@component.add(
    name="share conv oil vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_unconv_oil_vs_tot_agg": 1},
)
def share_conv_oil_vs_tot_agg():
    return 1 - share_unconv_oil_vs_tot_agg()


@component.add(
    name="share conv vs total oil extraction EU",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_oil_ej": 2, "real_extraction_unconv_oil_ej": 1},
)
def share_conv_vs_total_oil_extraction_eu():
    """
    Share of conventional oil vs total oil extracted.
    """
    return zidz(
        real_extraction_conv_oil_ej(),
        real_extraction_conv_oil_ej() + real_extraction_unconv_oil_ej(),
    )


@component.add(
    name="share RURR conv oil to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_conv_oil_to_leave_underground"
    },
)
def share_rurr_conv_oil_to_leave_underground():
    """
    RURR's conventional fossil oil to be left in the ground as a share of the RURR in the reference year.
    """
    return _ext_constant_share_rurr_conv_oil_to_leave_underground()


_ext_constant_share_rurr_conv_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "share_RURR_conv_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_conv_oil_to_leave_underground",
)


@component.add(
    name="share RURR tot agg fossil oil to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_tot_agg_fossil_oil_to_leave_underground"
    },
)
def share_rurr_tot_agg_fossil_oil_to_leave_underground():
    """
    RURR's total aggregated fossil oil to be left in the ground as a share of the RURR in the reference year.
    """
    return _ext_constant_share_rurr_tot_agg_fossil_oil_to_leave_underground()


_ext_constant_share_rurr_tot_agg_fossil_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "share_RURR_agg_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_tot_agg_fossil_oil_to_leave_underground",
)


@component.add(
    name="share RURR unconv oil to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_rurr_unconv_oil_to_leave_underground"
    },
)
def share_rurr_unconv_oil_to_leave_underground():
    """
    RURR's total aggregated fossil oil to be left in the ground as a share of the RURR in the reference year.
    """
    return _ext_constant_share_rurr_unconv_oil_to_leave_underground()


_ext_constant_share_rurr_unconv_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "share_RURR_unconv_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_unconv_oil_to_leave_underground",
)


@component.add(
    name="share unconv oil vs tot agg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "evolution_share_unconv_oil_vs_tot_agg": 1,
        "historic_unconv_oil_domestic_eu_extracted": 1,
        "ped_total_oil_ej": 1,
    },
)
def share_unconv_oil_vs_tot_agg():
    """
    Evolution of the share of unconventional oil vs total aggregated oil.
    """
    return if_then_else(
        time() > 2012,
        lambda: np.minimum(evolution_share_unconv_oil_vs_tot_agg(), 1),
        lambda: zidz(historic_unconv_oil_domestic_eu_extracted(), ped_total_oil_ej()),
    )


@component.add(
    name="share unconv oil vs tot agg in 2050",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_unconv_oil_vs_tot_agg_in_2050"},
)
def share_unconv_oil_vs_tot_agg_in_2050():
    """
    Share of unconventional oil vs total aggregated oil in 2050 depending on the maximum extraction curve selected for total aggregated oil.
    """
    return _ext_constant_share_unconv_oil_vs_tot_agg_in_2050()


_ext_constant_share_unconv_oil_vs_tot_agg_in_2050 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_unconv_vs_agg_oil_in_2050",
    {},
    _root,
    {},
    "_ext_constant_share_unconv_oil_vs_tot_agg_in_2050",
)


@component.add(
    name="Start year policy leave in ground conv oil",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_leave_in_ground_conv_oil"
    },
)
def start_year_policy_leave_in_ground_conv_oil():
    """
    Year when the policy to progressively leave fossil oil in the ground enters into force.
    """
    return _ext_constant_start_year_policy_leave_in_ground_conv_oil()


_ext_constant_start_year_policy_leave_in_ground_conv_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_conv_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_leave_in_ground_conv_oil",
)


@component.add(
    name="Start year policy leave in ground fossil oil",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_leave_in_ground_fossil_oil"
    },
)
def start_year_policy_leave_in_ground_fossil_oil():
    """
    Year when the policy to progressively leave fossil oil in the ground enters into force.
    """
    return _ext_constant_start_year_policy_leave_in_ground_fossil_oil()


_ext_constant_start_year_policy_leave_in_ground_fossil_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_agg_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_leave_in_ground_fossil_oil",
)


@component.add(
    name="Start year policy leave in ground unconv oil",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_policy_leave_in_ground_unconv_oil"
    },
)
def start_year_policy_leave_in_ground_unconv_oil():
    """
    Year when the policy to progressively leave fossil oil in the ground enters into force.
    """
    return _ext_constant_start_year_policy_leave_in_ground_unconv_oil()


_ext_constant_start_year_policy_leave_in_ground_unconv_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_unconv_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_leave_in_ground_unconv_oil",
)


@component.add(
    name="table max extraction agg oil",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_agg_oil",
        "__lookup__": "_ext_lookup_table_max_extraction_agg_oil",
    },
)
def table_max_extraction_agg_oil(x, final_subs=None):
    return _ext_lookup_table_max_extraction_agg_oil(x, final_subs)


_ext_lookup_table_max_extraction_agg_oil = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_agg_oil",
    "max_extraction_agg_oil",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_agg_oil",
)


@component.add(
    name="table max extraction conv oil",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_conv_oil",
        "__lookup__": "_ext_lookup_table_max_extraction_conv_oil",
    },
)
def table_max_extraction_conv_oil(x, final_subs=None):
    return _ext_lookup_table_max_extraction_conv_oil(x, final_subs)


_ext_lookup_table_max_extraction_conv_oil = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_conv_oil",
    "max_extraction_conv_oil",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_conv_oil",
)


@component.add(
    name="table max extraction unconv oil",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_unconv_oil",
        "__lookup__": "_ext_lookup_table_max_extraction_unconv_oil",
    },
)
def table_max_extraction_unconv_oil(x, final_subs=None):
    return _ext_lookup_table_max_extraction_unconv_oil(x, final_subs)


_ext_lookup_table_max_extraction_unconv_oil = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_unconv_oil",
    "max_extraction_unconv_oil",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_unconv_oil",
)


@component.add(
    name="total agg fossil oil to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_rurr_tot_agg_fossil_oil_to_leave_underground": 1,
        "rurr_total_agg_fossil_oil_in_reference_year": 1,
    },
)
def total_agg_fossil_oil_to_leave_underground():
    """
    Total aggregated fossil oil to be left underground due to the application of policies that leave oil underground.
    """
    return (
        share_rurr_tot_agg_fossil_oil_to_leave_underground()
        * rurr_total_agg_fossil_oil_in_reference_year()
    )


@component.add(
    name="unconv oil to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_unconv_oil_in_reference_year": 1,
        "share_rurr_unconv_oil_to_leave_underground": 1,
    },
)
def unconv_oil_to_leave_underground():
    """
    Unconventional fossil oil to be left underground due to the application of policies that leave oil underground.
    """
    return (
        rurr_unconv_oil_in_reference_year()
        * share_rurr_unconv_oil_to_leave_underground()
    )


@component.add(
    name="URR conv oil",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_oil": 1, "urr_conv_oil_input": 1},
)
def urr_conv_oil():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1, lambda: urr_conv_oil_input(), lambda: 0
    )


@component.add(
    name="URR conv oil input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_conv_oil_input"},
)
def urr_conv_oil_input():
    return _ext_constant_urr_conv_oil_input()


_ext_constant_urr_conv_oil_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_conv_oil",
    {},
    _root,
    {},
    "_ext_constant_urr_conv_oil_input",
)


@component.add(
    name="URR tot agg oil",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_oil": 1, "urr_tot_agg_oil_input": 1},
)
def urr_tot_agg_oil():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1, lambda: 0, lambda: urr_tot_agg_oil_input()
    )


@component.add(
    name="URR tot agg oil input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_tot_agg_oil_input"},
)
def urr_tot_agg_oil_input():
    return _ext_constant_urr_tot_agg_oil_input()


_ext_constant_urr_tot_agg_oil_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_agg_oil",
    {},
    _root,
    {},
    "_ext_constant_urr_tot_agg_oil_input",
)


@component.add(
    name="URR unconv oil",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"separate_conv_and_unconv_oil": 1, "urr_unconv_oil_input": 1},
)
def urr_unconv_oil():
    """
    URR unconventional oil.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1, lambda: urr_unconv_oil_input(), lambda: 0
    )


@component.add(
    name="URR unconv oil input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_unconv_oil_input"},
)
def urr_unconv_oil_input():
    return _ext_constant_urr_unconv_oil_input()


_ext_constant_urr_unconv_oil_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_unconv_oil",
    {},
    _root,
    {},
    "_ext_constant_urr_unconv_oil_input",
)


@component.add(
    name="year 2012", units="year", comp_type="Constant", comp_subtype="Normal"
)
def year_2012():
    return 2012


@component.add(
    name="year 2050", units="year", comp_type="Constant", comp_subtype="Normal"
)
def year_2050():
    return 2050


@component.add(
    name="Year scarcity oil",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_oil_eu": 1, "time": 1},
)
def year_scarcity_oil():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_total_oil_eu() > 0.95, lambda: 0, lambda: time())


@component.add(
    name="year to end conv oil extraction",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_conv_oil": 2,
        "remaining_extractable_conv_oil_with_left_underground": 2,
        "time": 1,
    },
)
def year_to_end_conv_oil_extraction():
    """
    Year when coal extraction has to end in order to comply with leave in ground policy. This year is dinamically determined, accordig to the actual extraction rate.
    """
    return if_then_else(
        np.logical_or(
            extraction_conv_oil() <= 0,
            remaining_extractable_conv_oil_with_left_underground() <= 0,
        ),
        lambda: 0,
        lambda: 2
        * remaining_extractable_conv_oil_with_left_underground()
        / extraction_conv_oil()
        + time(),
    )


@component.add(
    name="year to end fossil oil extraction",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_tot_agg_oil": 2,
        "remaining_extractable_fossil_oil_with_left_underground": 2,
        "time": 1,
    },
)
def year_to_end_fossil_oil_extraction():
    """
    Year when coal extraction has to end in order to comply with leave in ground policy. This year is dinamically determined, accordig to the actual extraction rate.
    """
    return if_then_else(
        np.logical_or(
            extraction_tot_agg_oil() <= 0,
            remaining_extractable_fossil_oil_with_left_underground() <= 0,
        ),
        lambda: 0,
        lambda: 2
        * remaining_extractable_fossil_oil_with_left_underground()
        / extraction_tot_agg_oil()
        + time(),
    )


@component.add(
    name="year to end unconv oil extraction",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_unconv_oil": 2,
        "remaining_extractable_unconv_oil_with_left_underground": 2,
        "time": 1,
    },
)
def year_to_end_unconv_oil_extraction():
    """
    Year when unconv oil extraction has to end in order to comply with leave in ground policy. This year is dinamically determined, accordig to the actual extraction rate.
    """
    return if_then_else(
        np.logical_or(
            extraction_unconv_oil() <= 0,
            remaining_extractable_unconv_oil_with_left_underground() <= 0,
        ),
        lambda: 0,
        lambda: 2
        * remaining_extractable_unconv_oil_with_left_underground()
        / extraction_unconv_oil()
        + time(),
    )
