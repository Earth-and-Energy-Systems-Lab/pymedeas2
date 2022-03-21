"""
Module natural_gas_extraction
Translated using PySD version 2.2.3
"""


def abundance_total_nat_gas():
    """
    Real Name: abundance total nat gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_nat_gas_ej() < pes_nat_gas(),
        lambda: 1,
        lambda: 1 - zidz(ped_nat_gas_ej() - pes_nat_gas(), ped_nat_gas_ej()),
    )


def check_gas_delayed_1yr():
    """
    Real Name: check gas delayed 1yr
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def constrain_gas_exogenous_growth_delayed_1yr():
    """
    Real Name: "constrain gas exogenous growth? delayed 1yr"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_constrain_gas_exogenous_growth_delayed_1yr()


_delayfixed_constrain_gas_exogenous_growth_delayed_1yr = DelayFixed(
    lambda: constrain_gas_exogenous_growth(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_constrain_gas_exogenous_growth_delayed_1yr",
)


def conv_gas_to_leave_underground():
    """
    Real Name: conv gas to leave underground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Conventional natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_conv_gas(),
        lambda: 0,
        lambda: rurr_conv_gas_until_start_year_plg()
        * share_rurr_conv_gas_to_leave_underground(),
    )


def cumulated_conv_gas_extraction():
    """
    Real Name: cumulated conv gas extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated conventional gas extraction.
    """
    return _integ_cumulated_conv_gas_extraction()


_integ_cumulated_conv_gas_extraction = Integ(
    lambda: extraction_conv_gas_ej(),
    lambda: cumulated_conv_gas_extraction_to_1995(),
    "_integ_cumulated_conv_gas_extraction",
)


def cumulated_conv_gas_extraction_to_1995():
    """
    Real Name: cumulated conv gas extraction to 1995
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Cumulated conventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_conv_gas_extraction_to_1995()


_ext_constant_cumulated_conv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_conventional_gas_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_conv_gas_extraction_to_1995",
)


def cumulated_tot_agg_gas_extraction():
    """
    Real Name: cumulated tot agg gas extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated total aggregated gas extraction.
    """
    return _integ_cumulated_tot_agg_gas_extraction()


_integ_cumulated_tot_agg_gas_extraction = Integ(
    lambda: extraction_tot_agg_gas_ej(),
    lambda: cumulated_tot_agg_gas_extraction_to_1995(),
    "_integ_cumulated_tot_agg_gas_extraction",
)


def cumulated_tot_agg_gas_extraction_to_1995():
    """
    Real Name: cumulated tot agg gas extraction to 1995
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Cumulated total agg gas extraction to 1995.
    """
    return (
        cumulated_conv_gas_extraction_to_1995()
        + cumulated_unconv_gas_extraction_to_1995()
    )


def cumulated_unconv_gas_extraction():
    """
    Real Name: Cumulated unconv gas extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated unconventional gas extraction.
    """
    return _integ_cumulated_unconv_gas_extraction()


_integ_cumulated_unconv_gas_extraction = Integ(
    lambda: extraction_unconv_gas_ej(),
    lambda: cumulated_unconv_gas_extraction_to_1995(),
    "_integ_cumulated_unconv_gas_extraction",
)


def cumulated_unconv_gas_extraction_to_1995():
    """
    Real Name: cumulated unconv gas extraction to 1995
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Cumulated unconventional gas extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_unconv_gas_extraction_to_1995()


_ext_constant_cumulated_unconv_gas_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_unconventional_gas_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_unconv_gas_extraction_to_1995",
)


def demand_conv_gas():
    """
    Real Name: Demand conv gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of conventional gas. It is assumed that conventional gas covers the rest of the liquids demand after accounting for the contributions from unconventional gas.
    """
    return np.maximum(ped_nat_gas_ej() - extraction_unconv_gas_ej(), 0)


def demand_gas_for_oil_refinery_gains():
    """
    Real Name: demand gas for oil refinery gains
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of natural gas to be used as input in the refineries to obtain the so-called "oil refinery gains".
    """
    return oil_refinery_gains_ej() * efficiency_gas_for_oil_refinery_gains()


def efficiency_gas_for_oil_refinery_gains():
    """
    Real Name: Efficiency gas for oil refinery gains
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    We assume a 100% efficiency as first approximation.
    """
    return _ext_constant_efficiency_gas_for_oil_refinery_gains()


_ext_constant_efficiency_gas_for_oil_refinery_gains = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_gas_for_oil_refinery_gains",
    {},
    _root,
    "_ext_constant_efficiency_gas_for_oil_refinery_gains",
)


def evolution_share_unconv_gas_vs_tot_agg():
    """
    Real Name: evolution share unconv gas vs tot agg
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Linear relation of the evolution of the share of unconventional gas vs total aggregated gas.
    """
    return (share_unconv_gas_vs_tot_agg_in_2050() - 0.1268) / (2050 - 2012) * time() + (
        share_unconv_gas_vs_tot_agg_in_2050()
        - ((share_unconv_gas_vs_tot_agg_in_2050() - 0.1268) / (2050 - 2012)) * 2050
    )


def exponent_availability_conv_gas():
    """
    Real Name: exponent availability conv gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    The smaller the exponent, more priority to conventional vs unconventional gas: 1: lineal 1/2: square root 1/3: cube root ...
    """
    return 1 / 4


def extraction_conv_gas__tot_agg():
    """
    Real Name: "extraction conv gas - tot agg"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return extraction_tot_agg_gas_ej() * share_conv_gas_vs_tot_agg()


def extraction_conv_gas_ej():
    """
    Real Name: extraction conv gas EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def extraction_tot_agg_gas_ej():
    """
    Real Name: extraction tot agg gas EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def extraction_unconv_gas__tot_agg():
    """
    Real Name: "extraction unconv gas - tot agg"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return extraction_tot_agg_gas_ej() * share_unconv_gas_vs_tot_agg()


def extraction_unconv_gas_delayed():
    """
    Real Name: extraction unconv gas delayed
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_extraction_unconv_gas_delayed()


_delayfixed_extraction_unconv_gas_delayed = DelayFixed(
    lambda: extraction_unconv_gas_ej(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_extraction_unconv_gas_delayed",
)


def extraction_unconv_gas_ej():
    """
    Real Name: extraction unconv gas EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def flow_conv_gas_left_in_ground():
    """
    Real Name: Flow conv gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def flow_tot_agg_gas_left_in_ground():
    """
    Real Name: Flow tot agg gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def flow_unconv_gas_left_in_ground():
    """
    Real Name: Flow unconv gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def historic_unconv_gas():
    """
    Real Name: Historic unconv gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Data
    Subs: []

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
    "_ext_data_historic_unconv_gas",
)


def increase_scarcity_conv_gas():
    """
    Real Name: increase scarcity conv gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return scarcity_conv_gas_stock() * zidz(
        scarcity_conv_gas() - scarcity_conv_gas_delayed_1yr(), scarcity_conv_gas()
    )


def max_extraction_conv_gas_ej():
    """
    Real Name: max extraction conv gas EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: table_max_extraction_conv_gas(tot_rurr_conv_gas()),
        lambda: 0,
    )


def max_extraction_tot_agg_gas_ej():
    """
    Real Name: max extraction tot agg gas EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 0,
        lambda: table_max_extraction_agg_gas(tot_rurr_tot_agg_gas()),
        lambda: 0,
    )


def max_extraction_unconv_gas():
    """
    Real Name: max extraction unconv gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_unconv_gas(tot_rurr_unconv_gas())


def max_unconv_gas_growth_extraction():
    """
    Real Name: max unconv gas growth extraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Constraint to maximum annual unconventional gas extraction (%).
    """
    return np.maximum(
        0,
        1
        + p_constraint_growth_extraction_unconv_gas()
        * time_step()
        * scarcity_conv_gas_stock(),
    )


def max_unconv_gas_growth_extraction_ej():
    """
    Real Name: max unconv gas growth extraction EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Constrained unconventional gas extraction growth (EJ/year), i.e. maximum annual growth compatible with the constraint selected in the scenario.
    """
    return if_then_else(
        check_gas_delayed_1yr() < -0.01,
        lambda: (1 + constrain_gas_exogenous_growth_delayed_1yr())
        * extraction_unconv_gas_delayed(),
        lambda: extraction_unconv_gas_delayed() * max_unconv_gas_growth_extraction(),
    )


def p_constraint_growth_extraction_unconv_gas():
    """
    Real Name: P constraint growth extraction unconv gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Constant constraint to annual extraction of unconventional gas.
    """
    return _ext_constant_p_constraint_growth_extraction_unconv_gas()


_ext_constant_p_constraint_growth_extraction_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unconv_gas_growth",
    {},
    _root,
    "_ext_constant_p_constraint_growth_extraction_unconv_gas",
)


def ped_nat_gas_without_gtl():
    """
    Real Name: "PED nat. gas without GTL"
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand of natural gas without GTL.
    """
    return np.maximum(0, ped_nat_gas_ej() - ped_nat_gas_for_gtl_ej())


def pes_nat_gas():
    """
    Real Name: PES nat gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


def pes_nat_gas_without_gtl():
    """
    Real Name: "PES nat. gas without GTL"
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total extraction of conventional gas and unconventional (without GTL).
    """
    return pes_nat_gas() - ped_nat_gas_for_gtl_ej()


def real_extraction_conv_gas_ej():
    """
    Real Name: real extraction conv gas EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_conv_gas_ej(),
        lambda: extraction_conv_gas__tot_agg(),
    )


def real_extraction_conv_gas_emissions_relevant_ej():
    """
    Real Name: real extraction conv gas emissions relevant EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def real_extraction_unconv_gas_ej():
    """
    Real Name: real extraction unconv gas EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: extraction_unconv_gas_ej(),
        lambda: extraction_unconv_gas__tot_agg(),
    )


def real_extraction_unconv_gas_emissions_relevant_ej():
    """
    Real Name: real extraction unconv gas emissions relevant EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def rurr_conv_gas():
    """
    Real Name: RURR conv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR conventional gas.
    """
    return _integ_rurr_conv_gas()


_integ_rurr_conv_gas = Integ(
    lambda: -extraction_conv_gas_ej() - flow_conv_gas_left_in_ground(),
    lambda: urr_conv_gas()
    - cumulated_conv_gas_extraction_to_1995() * separate_conv_and_unconv_gas(),
    "_integ_rurr_conv_gas",
)


def rurr_conv_gas_until_start_year_plg():
    """
    Real Name: RURR conv gas until start year PLG
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_conv_gas_until_start_year_plg()


_sampleiftrue_rurr_conv_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_conv_gas(),
    lambda: rurr_conv_gas(),
    lambda: rurr_conv_gas(),
    "_sampleiftrue_rurr_conv_gas_until_start_year_plg",
)


def rurr_tot_agg_gas():
    """
    Real Name: RURR tot agg gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def rurr_tot_gas_until_start_year_plg():
    """
    Real Name: RURR tot gas until start year PLG
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_tot_gas_until_start_year_plg()


_sampleiftrue_rurr_tot_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_tot_agg_gas(),
    lambda: rurr_tot_agg_gas(),
    lambda: rurr_tot_agg_gas(),
    "_sampleiftrue_rurr_tot_gas_until_start_year_plg",
)


def rurr_unconv_gas():
    """
    Real Name: RURR unconv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR unconventional gas.
    """
    return _integ_rurr_unconv_gas()


_integ_rurr_unconv_gas = Integ(
    lambda: -extraction_unconv_gas_ej() - flow_unconv_gas_left_in_ground(),
    lambda: urr_unconv_gas()
    - cumulated_unconv_gas_extraction_to_1995() * separate_conv_and_unconv_gas(),
    "_integ_rurr_unconv_gas",
)


def rurr_unconv_gas_until_start_year_plg():
    """
    Real Name: RURR unconv gas until start year PLG
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_unconv_gas_until_start_year_plg()


_sampleiftrue_rurr_unconv_gas_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_unconv_gas(),
    lambda: rurr_unconv_gas(),
    lambda: rurr_unconv_gas(),
    "_sampleiftrue_rurr_unconv_gas_until_start_year_plg",
)


def scarcity_conv_gas():
    """
    Real Name: scarcity conv gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def scarcity_conv_gas_delayed_1yr():
    """
    Real Name: scarcity conv gas delayed 1yr
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_scarcity_conv_gas_delayed_1yr()


_delayfixed_scarcity_conv_gas_delayed_1yr = DelayFixed(
    lambda: scarcity_conv_gas(),
    lambda: 1,
    lambda: 0.2502,
    time_step,
    "_delayfixed_scarcity_conv_gas_delayed_1yr",
)


def scarcity_conv_gas_stock():
    """
    Real Name: scarcity conv gas stock
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_scarcity_conv_gas_stock()


_integ_scarcity_conv_gas_stock = Integ(
    lambda: increase_scarcity_conv_gas(),
    lambda: 0.2502,
    "_integ_scarcity_conv_gas_stock",
)


def separate_conv_and_unconv_gas():
    """
    Real Name: "separate conv and unconv gas?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Switch to disaggregate between conventional and unconventional fuel: "1" = disaggregation, "0" = conv+unconv aggregated (all the gas flows then through the right side of this view, i.e. the "conventional gas" modelling side).
    """
    return _ext_constant_separate_conv_and_unconv_gas()


_ext_constant_separate_conv_and_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "separate_conv_unconv_gas",
    {},
    _root,
    "_ext_constant_separate_conv_and_unconv_gas",
)


def share_conv_gas_vs_tot_agg():
    """
    Real Name: share conv gas vs tot agg
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return 1 - share_unconv_gas_vs_tot_agg()


def share_conv_vs_total_gas_extraction():
    """
    Real Name: share conv vs total gas extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of conventional gas vs total gas extracted.
    """
    return zidz(
        real_extraction_conv_gas_ej(),
        real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej(),
    )


def share_gas_for_oil_refinery_gains():
    """
    Real Name: share gas for oil refinery gains
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of gas to cover oil refinery gains. Condition to avoid error when the total demand of gas without GTL falls to zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        ped_nat_gas_without_gtl() > 0,
        lambda: demand_gas_for_oil_refinery_gains() / ped_nat_gas_without_gtl(),
        lambda: 0.5,
    )


def share_rurr_conv_gas_to_leave_underground():
    """
    Real Name: share RURR conv gas to leave underground
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    RURR's conventional gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_conv_gas_to_leave_underground()


_ext_constant_share_rurr_conv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_conv_gas_underground",
    {},
    _root,
    "_ext_constant_share_rurr_conv_gas_to_leave_underground",
)


def share_rurr_tot_agg_gas_to_leave_underground():
    """
    Real Name: share RURR tot agg gas to leave underground
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    RURR's total aggregated natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_tot_agg_gas_to_leave_underground()


_ext_constant_share_rurr_tot_agg_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_agg_gas_underground",
    {},
    _root,
    "_ext_constant_share_rurr_tot_agg_gas_to_leave_underground",
)


def share_rurr_unconv_gas_to_leave_underground():
    """
    Real Name: share RURR unconv gas to leave underground
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    RURR's unconventional natural gas to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_unconv_gas_to_leave_underground()


_ext_constant_share_rurr_unconv_gas_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_unconv_gas_underground",
    {},
    _root,
    "_ext_constant_share_rurr_unconv_gas_to_leave_underground",
)


def share_unconv_gas_vs_tot_agg():
    """
    Real Name: share unconv gas vs tot agg
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Evolution of the share of unconventional gas vs total aggregated gas.
    """
    return if_then_else(
        time() > 2012,
        lambda: np.minimum(evolution_share_unconv_gas_vs_tot_agg(), 1),
        lambda: historic_unconv_gas() / ped_nat_gas_ej(),
    )


def share_unconv_gas_vs_tot_agg_in_2050():
    """
    Real Name: share unconv gas vs tot agg in 2050
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of unconventional gas vs total aggregated gas in 2050 depending on the maximum extraction curve selected for total aggregated gas.
    """
    return _ext_constant_share_unconv_gas_vs_tot_agg_in_2050()


_ext_constant_share_unconv_gas_vs_tot_agg_in_2050 = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_unconv_vs_agg_gas_in_2050",
    {},
    _root,
    "_ext_constant_share_unconv_gas_vs_tot_agg_in_2050",
)


def start_policy_leave_in_ground_conv_gas():
    """
    Real Name: Start policy leave in ground conv gas
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when the policy to leave in the ground an amount of conventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_conv_gas()


_ext_constant_start_policy_leave_in_ground_conv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_conv_gas_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_conv_gas",
)


def start_policy_leave_in_ground_tot_agg_gas():
    """
    Real Name: Start policy leave in ground tot agg gas
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when the policy to leave in the ground an amount of total aggregated gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_gas()


_ext_constant_start_policy_leave_in_ground_tot_agg_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_agg_gas_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_tot_agg_gas",
)


def start_policy_leave_in_ground_unconv_gas():
    """
    Real Name: Start policy leave in ground unconv gas
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when the policy to leave in the ground an amount of unconventional gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_unconv_gas()


_ext_constant_start_policy_leave_in_ground_unconv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_unconv_gas_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_unconv_gas",
)


def table_max_extraction_agg_gas(x):
    """
    Real Name: table max extraction agg gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_max_extraction_agg_gas(x)


_ext_lookup_table_max_extraction_agg_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_agg_gas",
    "max_extraction_agg_gas",
    {},
    _root,
    "_ext_lookup_table_max_extraction_agg_gas",
)


def table_max_extraction_conv_gas(x):
    """
    Real Name: table max extraction conv gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_max_extraction_conv_gas(x)


_ext_lookup_table_max_extraction_conv_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_conv_gas",
    "max_extraction_conv_gas",
    {},
    _root,
    "_ext_lookup_table_max_extraction_conv_gas",
)


def table_max_extraction_unconv_gas(x):
    """
    Real Name: table max extraction unconv gas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_max_extraction_unconv_gas(x)


_ext_lookup_table_max_extraction_unconv_gas = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_unconv_gas",
    "max_extraction_unconv_gas",
    {},
    _root,
    "_ext_lookup_table_max_extraction_unconv_gas",
)


def tot_agg_gas_to_leave_underground():
    """
    Real Name: tot agg gas to leave underground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total aggregated natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_tot_agg_gas(),
        lambda: 0,
        lambda: rurr_tot_gas_until_start_year_plg()
        * share_rurr_tot_agg_gas_to_leave_underground(),
    )


def tot_rurr_conv_gas():
    """
    Real Name: Tot RURR conv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total RURR of conventional natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_conv_gas() + total_conv_gas_left_in_ground()


def tot_rurr_tot_agg_gas():
    """
    Real Name: Tot RURR tot agg gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total RURR of total aggregated natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_tot_agg_gas() + total_agg_gas_left_in_ground()


def tot_rurr_unconv_gas():
    """
    Real Name: Tot RURR unconv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total RURR of unconventional natural gas considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_unconv_gas() + total_unconv_gas_left_in_ground()


def total_agg_gas_left_in_ground():
    """
    Real Name: Total agg gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total amount of aggregated natural gas left in the ground due to policies.
    """
    return _integ_total_agg_gas_left_in_ground()


_integ_total_agg_gas_left_in_ground = Integ(
    lambda: flow_tot_agg_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_agg_gas_left_in_ground",
)


def total_conv_gas_left_in_ground():
    """
    Real Name: Total conv gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total amount of conventional natural gas left in the ground due to policies.
    """
    return _integ_total_conv_gas_left_in_ground()


_integ_total_conv_gas_left_in_ground = Integ(
    lambda: flow_conv_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_conv_gas_left_in_ground",
)


def total_unconv_gas_left_in_ground():
    """
    Real Name: Total unconv gas left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total amount of unconventional natural gas left in the ground due to policies.
    """
    return _integ_total_unconv_gas_left_in_ground()


_integ_total_unconv_gas_left_in_ground = Integ(
    lambda: flow_unconv_gas_left_in_ground(),
    lambda: 0,
    "_integ_total_unconv_gas_left_in_ground",
)


def unconv_gas_to_leave_underground():
    """
    Real Name: unconv gas to leave underground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Unconventional natural gas to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_unconv_gas(),
        lambda: 0,
        lambda: rurr_unconv_gas_until_start_year_plg()
        * share_rurr_unconv_gas_to_leave_underground(),
    )


def unlimited_gas():
    """
    Real Name: "unlimited gas?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Switch to consider if gas is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_gas()


_ext_constant_unlimited_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_gas",
    {},
    _root,
    "_ext_constant_unlimited_gas",
)


def urr_conv_gas():
    """
    Real Name: URR conv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: 1e32,
            lambda: urr_conv_gas_input(),
        ),
        lambda: 0,
    )


def urr_conv_gas_input():
    """
    Real Name: URR conv gas input
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_urr_conv_gas_input()


_ext_constant_urr_conv_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_conv_gas",
    {},
    _root,
    "_ext_constant_urr_conv_gas_input",
)


def urr_tot_agg_gas():
    """
    Real Name: URR tot agg gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_gas() == 1),
            lambda: 1e32,
            lambda: urr_total_gas_input(),
        ),
    )


def urr_total_gas_input():
    """
    Real Name: URR total gas input
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_urr_total_gas_input()


_ext_constant_urr_total_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_agg_gas",
    {},
    _root,
    "_ext_constant_urr_total_gas_input",
)


def urr_unconv_gas():
    """
    Real Name: URR unconv gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    RURR unconventional gas.
    """
    return if_then_else(
        separate_conv_and_unconv_gas() == 1, lambda: urr_unconv_gas_input(), lambda: 0
    )


def urr_unconv_gas_input():
    """
    Real Name: URR unconv gas input
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_urr_unconv_gas_input()


_ext_constant_urr_unconv_gas_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_unconv_gas",
    {},
    _root,
    "_ext_constant_urr_unconv_gas_input",
)


def year_scarcity_total_nat_gas():
    """
    Real Name: "Year scarcity total nat. gas"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_total_nat_gas() > 0.95, lambda: 0, lambda: time())
