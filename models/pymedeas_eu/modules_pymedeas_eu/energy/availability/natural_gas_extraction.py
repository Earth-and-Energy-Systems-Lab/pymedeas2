"""
Module natural_gas_extraction
Translated using PySD version 3.0.0
"""


@component.add(
    name='"abundance total nat. gas EU"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def abundance_total_nat_gas_eu():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_nat_gas_ej() < pes_nat_gas_eu(),
        lambda: 1,
        lambda: 1 - zidz(ped_nat_gas_ej() - pes_nat_gas_eu(), ped_nat_gas_ej()),
    )


@component.add(
    name="check gas delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
)
def cumulated_conv_gas_extraction_to_1995():
    """
    Cumulated conventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_conv_gas_extraction_to_1995()


_ext_constant_cumulated_conv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
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
)
def cumulated_unconv_gas_extraction_to_1995():
    """
    Cumulated unconventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_unconv_gas_extraction_to_1995()


_ext_constant_cumulated_unconv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cumulative_unconventional_gas_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_unconv_gas_extraction_to_1995",
)


@component.add(
    name="Demand conv gas",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def demand_conv_gas():
    """
    Demand of conventional gas. It is assumed that conventional gas covers the rest of the liquids demand after accounting for the contributions from unconventional gas.
    """
    return np.maximum(ped_nat_gas_ej() - extraction_unconv_gas_ej(), 0)


@component.add(
    name="demand gas for oil refinery gains",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
)
def evolution_share_unconv_gas_vs_tot_agg():
    """
    Linear relation of the evolution of the share of unconventional gas vs total aggregated gas.
    """
    return (share_unconv_gas_vs_tot_agg_in_2050() - 0.1232) / (2050 - 2012) * time() + (
        share_unconv_gas_vs_tot_agg_in_2050()
        - ((share_unconv_gas_vs_tot_agg_in_2050() - 0.1232) / (2050 - 2012)) * 2050
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
)
def extraction_conv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_conv_gas_vs_tot_agg()


@component.add(
    name="extraction conv gas EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def extraction_conv_gas_ej():
    """
    Annual extraction of conventional gas. IF THEN ELSE(RURR coal<0,0, IF THEN ELSE(Time<2016, PED domestic EU coal EJ, IF THEN ELSE("unlimited NRE?"=1, PED domestic EU coal EJ, IF THEN ELSE("unlimited coal?"=1, PED domestic EU coal EJ,MIN(PED domestic EU coal EJ, max extraction coal EJ)))))
    """
    return if_then_else(
        rurr_conv_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(
                time() < 2016, np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1)
            ),
            lambda: ped_domestic_eu_conv_nat_gas_ej(),
            lambda: np.minimum(
                ped_domestic_eu_conv_nat_gas_ej(), max_extraction_conv_gas_ej()
            ),
        ),
    )


@component.add(
    name="extraction tot agg gas EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def extraction_tot_agg_gas_ej():
    """
    Annual extraction of total aggregated natural gas.
    """
    return if_then_else(
        rurr_tot_agg_gas() < 0,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(
                time() < 2016, np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1)
            ),
            lambda: ped_domestic_eu_total_natgas_ej(),
            lambda: np.minimum(
                ped_domestic_eu_total_natgas_ej(), max_extraction_tot_agg_gas_ej()
            ),
        ),
    )


@component.add(
    name='"extraction unconv gas - tot agg"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def extraction_unconv_gas_tot_agg():
    return extraction_tot_agg_gas_ej() * share_unconv_gas_vs_tot_agg()


@component.add(
    name="extraction unconv gas delayed",
    units="EJ/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    units="EJ/Year",
    comp_type="Data",
    comp_subtype="External",
)
def historic_unconv_gas():
    """
    Historic unconventional extraction from Mohr et al (2015).
    """
    return _ext_data_historic_unconv_gas(time())


_ext_data_historic_unconv_gas = ExtData(
    "../energy.xlsx",
    "Europe",
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
)
def increase_scarcity_conv_gas():
    return scarcity_conv_gas() - scarcity_conv_gas_delayed_1yr()


@component.add(
    name="max extraction conv gas EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
)
def max_unconv_gas_growth_extraction():
    """
    Constraint to maximum annual unconventional gas extraction (%). This constraint is affected by the relative scarcity of conventional vs unconventional resource (priority to conventional resource to cover the demand while the maximum extraction level of energy/time is not reached).
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
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="P constraint growth extraction unconv gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_constraint_growth_extraction_unconv_gas():
    """
    Constant constraint to annual extraction of unconventional gas.
    """
    return _ext_constant_p_constraint_growth_extraction_unconv_gas()


_ext_constant_p_constraint_growth_extraction_unconv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_constraint_growth_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_p_constraint_growth_extraction_unconv_gas",
)


@component.add(
    name="PEC conv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pec_conv_gas():
    return real_extraction_conv_gas_ej() + imports_eu_conv_gas_from_row_ej()


@component.add(
    name="PEC unconv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pec_unconv_gas():
    return real_extraction_unconv_gas_ej() + imports_eu_unconv_gas_from_row_ej()


@component.add(
    name='"PED nat. gas without GTL"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ped_nat_gas_without_gtl():
    """
    Total demand of natural gas without GTL.
    """
    return np.maximum(0, ped_nat_gas_ej() - ped_nat_gas_for_gtl_ej())


@component.add(
    name='"PES nat. gas EU"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_nat_gas_eu():
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


@component.add(
    name='"PES nat. gas without GTL"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_nat_gas_without_gtl():
    """
    Total extraction of conventional gas and unconventional (without GTL).
    """
    return pes_nat_gas_eu() - ped_nat_gas_for_gtl_ej()


@component.add(
    name="real consumption UE conv gas emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_consumption_ue_conv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant conventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        pec_conv_gas()
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        * share_conv_vs_total_gas_extraction_eu(),
    )


@component.add(
    name="real consumption unconv gas emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_consumption_unconv_gas_emissions_relevant_ej():
    """
    Extraction of emission-relevant unconventional gas, i.e. excepting the resource used to produce GTL and for non-energy uses. We assume conventional and unconventional resource are used to produce GTL and for non-energy uses following the same share as for their relative extraction.
    """
    return np.maximum(
        0,
        pec_unconv_gas()
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        * (1 - share_conv_vs_total_gas_extraction_eu()),
    )


@component.add(
    name="real extraction conv gas EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
        * share_conv_vs_total_gas_extraction_eu(),
    )


@component.add(
    name="real extraction unconv gas EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_extraction_unconv_gas_ej():
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_unconv_gas_ej(),
        lambda: extraction_unconv_gas_tot_agg(),
    )


@component.add(
    name="RURR conv gas", units="EJ", comp_type="Stateful", comp_subtype="Integ"
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
    name="RURR tot agg gas", units="EJ", comp_type="Stateful", comp_subtype="Integ"
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
    name="RURR unconv gas", units="EJ", comp_type="Stateful", comp_subtype="Integ"
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
    name="scarcity conv gas", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="scarcity conv gas delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def scarcity_conv_gas_delayed_1yr():
    """
    "Scarcity conv gas" variable delayed 1 year. For the initial year we arbitrary chose the value "0" given that it will be endogenously calculated by the model for the following periods.
    """
    return _delayfixed_scarcity_conv_gas_delayed_1yr()


_delayfixed_scarcity_conv_gas_delayed_1yr = DelayFixed(
    lambda: scarcity_conv_gas(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_scarcity_conv_gas_delayed_1yr",
)


@component.add(
    name="scarcity conv gas stock",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
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
    name='"separate conv and unconv gas?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def separate_conv_and_unconv_gas():
    """
    Switch to disaggregate between conventional and unconventional fuel: "1" = disaggregation, "0" = conv+unconv aggregated (all the gas flows then through the right side of this view, i.e. the "conventional gas" modelling side).
    """
    return _ext_constant_separate_conv_and_unconv_gas()


_ext_constant_separate_conv_and_unconv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "separate_conv_and_unconv_gas",
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
)
def share_conv_gas_vs_tot_agg():
    return 1 - share_unconv_gas_vs_tot_agg()


@component.add(
    name="share conv vs total gas extraction EU",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_conv_vs_total_gas_extraction_eu():
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
)
def share_rurr_conv_gas_to_leave_underground():
    """
    RURR's conventional gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_conv_gas_to_leave_underground()


_ext_constant_share_rurr_conv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
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
)
def share_rurr_tot_agg_gas_to_leave_underground():
    """
    RURR's total aggregated natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_tot_agg_gas_to_leave_underground()


_ext_constant_share_rurr_tot_agg_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
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
)
def share_rurr_unconv_gas_to_leave_underground():
    """
    RURR's unconventional natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_unconv_gas_to_leave_underground()


_ext_constant_share_rurr_unconv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
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
)
def share_unconv_gas_vs_tot_agg():
    """
    Evolution of the share of unconventional gas vs total aggregated gas.
    """
    return if_then_else(
        time() > 2012,
        lambda: np.minimum(evolution_share_unconv_gas_vs_tot_agg(), 1),
        lambda: zidz(historic_unconv_gas(), ped_nat_gas_ej()),
    )


@component.add(
    name="share unconv gas vs tot agg in 2050",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_unconv_gas_vs_tot_agg_in_2050():
    """
    Share of unconventional gas vs total aggregated gas in 2050 depending on the maximum extraction curve selected for total aggregated gas.
    """
    return _ext_constant_share_unconv_gas_vs_tot_agg_in_2050()


_ext_constant_share_unconv_gas_vs_tot_agg_in_2050 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_unconv_vs_agg_gas_in_2050",
    {},
    _root,
    {},
    "_ext_constant_share_unconv_gas_vs_tot_agg_in_2050",
)


@component.add(
    name="Start policy leave in ground conv gas",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def start_policy_leave_in_ground_conv_gas():
    """
    Year when the policy to leave in the ground an amount of conventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_conv_gas()


_ext_constant_start_policy_leave_in_ground_conv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_policy_year_conv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_conv_gas",
)


@component.add(
    name="Start policy leave in ground tot agg gas",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def start_policy_leave_in_ground_tot_agg_gas():
    """
    Year when the policy to leave in the ground an amount of total aggregated gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_gas()


_ext_constant_start_policy_leave_in_ground_tot_agg_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_policy_year_agg_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_tot_agg_gas",
)


@component.add(
    name="Start policy leave in ground unconv gas",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def start_policy_leave_in_ground_unconv_gas():
    """
    Year when the policy to leave in the ground an amount of unconventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_unconv_gas()


_ext_constant_start_policy_leave_in_ground_unconv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_policy_year_unconv_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_unconv_gas",
)


@component.add(
    name="table max extraction agg gas",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def table_max_extraction_agg_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_agg_gas(x, final_subs)


_ext_lookup_table_max_extraction_agg_gas = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_agg_gas",
    "max_extraction_agg_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_agg_gas",
)


@component.add(
    name="table max extraction conv gas",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def table_max_extraction_conv_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_conv_gas(x, final_subs)


_ext_lookup_table_max_extraction_conv_gas = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_conv_gas",
    "max_extraction_conv_gas",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_conv_gas",
)


@component.add(
    name="table max extraction unconv gas",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def table_max_extraction_unconv_gas(x, final_subs=None):
    return _ext_lookup_table_max_extraction_unconv_gas(x, final_subs)


_ext_lookup_table_max_extraction_unconv_gas = ExtLookup(
    "../energy.xlsx",
    "Europe",
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
    name="Tot RURR conv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
)
def tot_rurr_tot_agg_gas():
    """
    Total RURR of total aggregated natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_tot_agg_gas() + total_agg_gas_left_in_ground()


@component.add(
    name="Tot RURR unconv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
    name='"unlimited gas?"', units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def unlimited_gas():
    """
    Switch to consider if gas is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_gas()


_ext_constant_unlimited_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "unlimited_gas",
    {},
    _root,
    {},
    "_ext_constant_unlimited_gas",
)


@component.add(
    name="URR conv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="URR conv gas input", units="EJ", comp_type="Constant", comp_subtype="External"
)
def urr_conv_gas_input():
    return _ext_constant_urr_conv_gas_input()


_ext_constant_urr_conv_gas_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_conv_gas_input",
)


@component.add(
    name="URR tot agg gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
)
def urr_total_gas_input():
    return _ext_constant_urr_total_gas_input()


_ext_constant_urr_total_gas_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_agg_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_total_gas_input",
)


@component.add(
    name="URR unconv gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
)
def urr_unconv_gas_input():
    return _ext_constant_urr_unconv_gas_input()


_ext_constant_urr_unconv_gas_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_urr_unconv_gas_input",
)


@component.add(
    name='"Year scarcity total nat. gas"', comp_type="Auxiliary", comp_subtype="Normal"
)
def year_scarcity_total_nat_gas():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_total_nat_gas_eu() > 0.95, lambda: 0, lambda: time())
