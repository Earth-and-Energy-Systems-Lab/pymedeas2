"""
Module oil_extraction
Translated using PySD version 2.2.1
"""


def abundance_total_oil():
    """
    Real Name: abundance total oil
    Original Eqn: IF THEN ELSE(PED total oil EJ<PES oil EJ, 1, 1-ZIDZ( (PED total oil EJ-PES oil EJ), PED total oil EJ ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        ped_total_oil_ej() < pes_oil_ej(),
        lambda: 1,
        lambda: 1 - zidz((ped_total_oil_ej() - pes_oil_ej()), ped_total_oil_ej()),
    )


def abundance_unconv_oil():
    """
    Real Name: abundance unconv oil
    Original Eqn: IF THEN ELSE(PED total oil EJ=0,0, IF THEN ELSE(PED total oil EJ > real extraction unconv oil EJ, (PED total oil EJ-real extraction unconv oil EJ)/PED total oil EJ, 0))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). The closest to 1 indicates
        that unconventional oil extractione is far to cover to whole oil demand,
        if "abundance unconv oil"=0 it means that unconventional oil extraction
        covers the whole demand of oil.
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


def abundance_unconv_oil_delayed_1yr():
    """
    Real Name: abundance unconv oil delayed 1yr
    Original Eqn: DELAY FIXED ( abundance unconv oil, 1, 1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_abundance_unconv_oil_delayed_1yr()


def abundance_unconv_oil_stock():
    """
    Real Name: abundance unconv oil stock
    Original Eqn: INTEG ( increase abundance unconv oil, 1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_abundance_unconv_oil_stock()


def abundance_unconv_oil2():
    """
    Real Name: abundance unconv oil2
    Original Eqn: abundance unconv oil stock
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Adaptation of the parameter abundance for better behaviour of the model.
        This variable limits the growth of a technology supplying a particular
        final energy type when its supply increases its share in relation to the
        total supply of this energy type (to avoid overshootings).
    """
    return abundance_unconv_oil_stock()


def check_liquids_delayed_1yr():
    """
    Real Name: check liquids delayed 1yr
    Original Eqn: DELAY FIXED ( check liquids, 1, 1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return _delayfixed_check_liquids_delayed_1yr()


def constrain_liquids_exogenous_growth_delayed_1yr():
    """
    Real Name: "constrain liquids exogenous growth? delayed 1yr"
    Original Eqn: DELAY FIXED ( "constrain liquids exogenous growth?", 1, 1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_constrain_liquids_exogenous_growth_delayed_1yr()


def conv_oil_to_leave_underground():
    """
    Real Name: conv oil to leave underground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground conv oil,0,RURR conv oil until start year PLG*share RURR conv oil to leave underground)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Conventional oil to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_conv_oil(),
        lambda: 0,
        lambda: rurr_conv_oil_until_start_year_plg()
        * share_rurr_conv_oil_to_leave_underground(),
    )


def cumulated_conv_oil_extraction():
    """
    Real Name: cumulated conv oil extraction
    Original Eqn: INTEG ( extraction conv oil EJ, cumulated conv oil extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated conventional oil extraction.
    """
    return _integ_cumulated_conv_oil_extraction()


def cumulated_conv_oil_extraction_to_1995():
    """
    Real Name: cumulated conv oil extraction to 1995
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'cumulative_conventional_oil_extraction_until_1995')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulated conventional oil extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_conv_oil_extraction_to_1995()


def cumulated_tot_agg_extraction_to_1995():
    """
    Real Name: cumulated tot agg extraction to 1995
    Original Eqn: cumulated conv oil extraction to 1995+cumulated unconv oil extraction to 1995
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated total aggregated oil extraction to 1995.
    """
    return (
        cumulated_conv_oil_extraction_to_1995()
        + cumulated_unconv_oil_extraction_to_1995()
    )


def cumulated_tot_agg_oil_extraction():
    """
    Real Name: cumulated tot agg oil extraction
    Original Eqn: INTEG ( extraction tot agg oil EJ, cumulated tot agg extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated total aggregated oil extraction.
    """
    return _integ_cumulated_tot_agg_oil_extraction()


def cumulated_unconv_oil_extraction():
    """
    Real Name: cumulated unconv oil extraction
    Original Eqn: INTEG ( extraction unconv oil EJ, cumulated unconv oil extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated unconventional oil extracted.
    """
    return _integ_cumulated_unconv_oil_extraction()


def cumulated_unconv_oil_extraction_to_1995():
    """
    Real Name: cumulated unconv oil extraction to 1995
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'cumulative_unconventional_oil_extraction_until_1995')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulated unconventional oil extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_unconv_oil_extraction_to_1995()


def demand_conv_oil_ej():
    """
    Real Name: Demand conv oil EJ
    Original Eqn: MAX(PED total oil EJ-extraction unconv oil EJ, 0)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of conventional oil. It is assumed that conventional oil covers the
        rest of the liquids demand after accounting for the contributions from
        other liquids and unconventional oil.
    """
    return np.maximum(ped_total_oil_ej() - extraction_unconv_oil_ej(), 0)


def evolution_share_unconv_oil_vs_tot_agg():
    """
    Real Name: evolution share unconv oil vs tot agg
    Original Eqn: (share unconv oil vs tot agg in 2050-0.059)/(2050-2012)*Time+(share unconv oil vs tot agg in 2050-((share unconv oil vs tot agg in 2050-0.059)/(2050-2012))*2050)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Linear relation of the evolution of the share of unconventional oil vs
        total aggregated oil.
    """
    return (share_unconv_oil_vs_tot_agg_in_2050() - 0.059) / (2050 - 2012) * time() + (
        share_unconv_oil_vs_tot_agg_in_2050()
        - ((share_unconv_oil_vs_tot_agg_in_2050() - 0.059) / (2050 - 2012)) * 2050
    )


def exponent_availability_conv_oil():
    """
    Real Name: exponent availability conv oil
    Original Eqn: 1/4
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    The smaller the exponent, more priority to conventional vs unconventional oil:        1: lineal        1/2: square root        1/3: cube root        ...
    """
    return 1 / 4


def extraction_conv_oil__tot_agg():
    """
    Real Name: "extraction conv oil - tot agg"
    Original Eqn: extraction tot agg oil EJ*share conv oil vs tot agg
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return extraction_tot_agg_oil_ej() * share_conv_oil_vs_tot_agg()


def extraction_conv_oil_ej():
    """
    Real Name: extraction conv oil EJ
    Original Eqn: IF THEN ELSE(RURR conv oil<0,0, IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited oil?"=1, Demand conv oil EJ, MIN(Demand conv oil EJ, max extraction conv oil EJ)))
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of conventional oil.
    """
    return if_then_else(
        rurr_conv_oil() < 0,
        lambda: 0,
        lambda: if_then_else(
            logical_or(unlimited_nre() == 1, unlimited_oil() == 1),
            lambda: demand_conv_oil_ej(),
            lambda: np.minimum(demand_conv_oil_ej(), max_extraction_conv_oil_ej()),
        ),
    )


def extraction_tot_agg_oil_ej():
    """
    Real Name: extraction tot agg oil EJ
    Original Eqn: IF THEN ELSE(RURR tot agg oil<0,0, IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited oil?"=1, PED total oil EJ, MIN(PED total oil EJ, max extraction tot agg oil EJ)))
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of total aggregated oil.
    """
    return if_then_else(
        rurr_tot_agg_oil() < 0,
        lambda: 0,
        lambda: if_then_else(
            logical_or(unlimited_nre() == 1, unlimited_oil() == 1),
            lambda: ped_total_oil_ej(),
            lambda: np.minimum(ped_total_oil_ej(), max_extraction_tot_agg_oil_ej()),
        ),
    )


def extraction_unconv_oil__tot_agg():
    """
    Real Name: "extraction unconv oil - tot agg"
    Original Eqn: extraction tot agg oil EJ*share unconv oil vs tot agg
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return extraction_tot_agg_oil_ej() * share_unconv_oil_vs_tot_agg()


def extraction_unconv_oil_delayed():
    """
    Real Name: extraction unconv oil delayed
    Original Eqn: DELAY FIXED ( extraction unconv oil EJ, TIME STEP, 1.09)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of unconventional oil delayed 1 year. Data from Mohr et al
        (2015) for 1989.
    """
    return _delayfixed_extraction_unconv_oil_delayed()


def extraction_unconv_oil_ej():
    """
    Real Name: extraction unconv oil EJ
    Original Eqn: MIN(IF THEN ELSE(RURR unconv oil EJ<0,0, IF THEN ELSE(Time>2012, IF THEN ELSE("separate conv and unconv oil?"=1, MIN(max extraction unconv oil, max unconv oil growth extraction EJ ),0), Historic unconv oil)),PED total oil EJ)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of unconventional oil.        MIN(IF THEN ELSE(RURR unconv oil EJ<0,0,        IF THEN ELSE(Time<=2013, Historic unconv oil,        IF THEN ELSE("separate conv and unconv oil?"=1, MIN(max extraction unconv oil, max
        unconv oil growth extraction EJ        ),0))),PED total oil EJ)
    """
    return np.minimum(
        if_then_else(
            rurr_unconv_oil_ej() < 0,
            lambda: 0,
            lambda: if_then_else(
                time() > 2012,
                lambda: if_then_else(
                    separate_conv_and_unconv_oil() == 1,
                    lambda: np.minimum(
                        max_extraction_unconv_oil(),
                        max_unconv_oil_growth_extraction_ej(),
                    ),
                    lambda: 0,
                ),
                lambda: historic_unconv_oil(),
            ),
        ),
        ped_total_oil_ej(),
    )


def flow_conv_oil_left_in_ground():
    """
    Real Name: Flow conv oil left in ground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground conv oil,0, IF THEN ELSE(Time>=Start policy leave in ground conv oil+1,0, conv oil to leave underground))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Flow of conventional oil left in the ground. We assume that this amount is
        removed from the stock of conventional oil available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_conv_oil(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_conv_oil() + 1,
            lambda: 0,
            lambda: conv_oil_to_leave_underground(),
        ),
    )


def flow_tot_agg_oil_left_in_ground():
    """
    Real Name: Flow tot agg oil left in ground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground tot agg oil,0, IF THEN ELSE(Time>=Start policy leave in ground tot agg oil+1,0, tot agg oil to leave underground))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Flow of total aggregated oil left in the ground. We assume that this
        amount is removed from the stock of total aggregated oil available in 1
        year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_tot_agg_oil(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_tot_agg_oil() + 1,
            lambda: 0,
            lambda: tot_agg_oil_to_leave_underground(),
        ),
    )


def flow_unconv_oil_left_in_ground():
    """
    Real Name: Flow unconv oil left in ground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground unconv oil,0, IF THEN ELSE(Time>=Start policy leave in ground unconv oil+1,0, unconv oil to leave underground))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Flow of unconventional oil left in the ground. We assume that this amount
        is removed from the stock of unconventional oil available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_unconv_oil(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_unconv_oil() + 1,
            lambda: 0,
            lambda: unconv_oil_to_leave_underground(),
        ),
    )


def historic_unconv_oil():
    """
    Real Name: Historic unconv oil
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_unconventional_oil_extraction')
    Units: EJ/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Historic unconventional extraction from Mohr et al (2015).
    """
    return _ext_data_historic_unconv_oil(time())


def increase_abundance_unconv_oil():
    """
    Real Name: increase abundance unconv oil
    Original Eqn: abundance unconv oil-abundance unconv oil delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return abundance_unconv_oil() - abundance_unconv_oil_delayed_1yr()


def increase_scarcity_conv_oil():
    """
    Real Name: increase scarcity conv oil
    Original Eqn: scarcity conv oil-scarcity conv oil delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return scarcity_conv_oil() - scarcity_conv_oil_delayed_1yr()


def max_extraction_conv_oil_ej():
    """
    Real Name: max extraction conv oil EJ
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, table max extraction conv oil(Tot RURR conv oil), 0)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: table_max_extraction_conv_oil(tot_rurr_conv_oil()),
        lambda: 0,
    )


def max_extraction_tot_agg_oil_ej():
    """
    Real Name: max extraction tot agg oil EJ
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=0, table max extraction agg oil(Tot RURR tot agg oil), 0)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve for total aggregated oil selected for the
        simulations.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 0,
        lambda: table_max_extraction_agg_oil(tot_rurr_tot_agg_oil()),
        lambda: 0,
    )


def max_extraction_unconv_oil():
    """
    Real Name: max extraction unconv oil
    Original Eqn: table max extraction unconv oil(Tot RURR unconv oil)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_unconv_oil(tot_rurr_unconv_oil())


def max_unconv_oil_growth_extraction():
    """
    Real Name: max unconv oil growth extraction
    Original Eqn: MAX(0, 1+(P constraint growth extraction unconv oil )*TIME STEP*scarcity conv oil stock*abundance unconv oil2)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Constraint to maximum annual unconventional gas extraction (%).
    """
    return np.maximum(
        0,
        1
        + (p_constraint_growth_extraction_unconv_oil())
        * time_step()
        * scarcity_conv_oil_stock()
        * abundance_unconv_oil2(),
    )


def max_unconv_oil_growth_extraction_ej():
    """
    Real Name: max unconv oil growth extraction EJ
    Original Eqn: IF THEN ELSE(check liquids delayed 1yr<-0.0001, (1+"constrain liquids exogenous growth? delayed 1yr" )*extraction unconv oil delayed,extraction unconv oil delayed*max unconv oil growth extraction)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Constrained unconventional oil extraction growth (EJ/year), i.e. maximum
        annual growth compatible with the constraint selected in the scenario.
    """
    return if_then_else(
        check_liquids_delayed_1yr() < -0.0001,
        lambda: (1 + constrain_liquids_exogenous_growth_delayed_1yr())
        * extraction_unconv_oil_delayed(),
        lambda: extraction_unconv_oil_delayed() * max_unconv_oil_growth_extraction(),
    )


def mbd_per_ejyear():
    """
    Real Name: "Mb/d per EJ/year"
    Original Eqn: 0.479726
    Units: Mb*year/(EJ*d)
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion between Mb/d to EJ/year.
    """
    return 0.479726


def oil_refinery_gains_ej():
    """
    Real Name: Oil refinery gains EJ
    Original Eqn: Oil refinery gains share*PES oil EJ delayed
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Oil refinery gains.
    """
    return oil_refinery_gains_share() * pes_oil_ej_delayed()


def oil_refinery_gains_share():
    """
    Real Name: Oil refinery gains share
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'oil_refinery_gains_share')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    We assume these energy gains are reached by applying natural gas as energy
        input. Historically, their share has been growing in the last decades
        (1.9% in 1980). WEO (2010) gives a 2.8% for the year 2009 and BP (2007)
        2.6%. The value 2.7% is taken.
    """
    return _ext_constant_oil_refinery_gains_share()


def p_constraint_growth_extraction_unconv_oil():
    """
    Real Name: P constraint growth extraction unconv oil
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'unconv_oil_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Constant constraint to annual extraction of unconventional oil.
    """
    return _ext_constant_p_constraint_growth_extraction_unconv_oil()


def pes_oil_ej():
    """
    Real Name: PES oil EJ
    Original Eqn: real extraction conv oil EJ+real extraction unconv oil EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total oil (conventional + unconventional) extraction.
    """
    return real_extraction_conv_oil_ej() + real_extraction_unconv_oil_ej()


def pes_oil_ej_delayed():
    """
    Real Name: PES oil EJ delayed
    Original Eqn: DELAY FIXED ( PES oil EJ, TIME STEP, 139.5)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    PES total oil extraction delayed.
    """
    return _delayfixed_pes_oil_ej_delayed()


def pes_oil_mbd():
    """
    Real Name: "PES oil Mb/d"
    Original Eqn: PES oil EJ*"Mb/d per EJ/year"
    Units: Mb/d
    Limits: (None, None)
    Type: component
    Subs: None

    Total oil (conventional + unconventional) extraction.
    """
    return pes_oil_ej() * mbd_per_ejyear()


def real_extraction_conv_oil_ej():
    """
    Real Name: real extraction conv oil EJ
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, extraction conv oil EJ , "extraction conv oil - tot agg")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: extraction_conv_oil_ej(),
        lambda: extraction_conv_oil__tot_agg(),
    )


def real_extraction_conv_oil_emissions_relevant_ej():
    """
    Real Name: real extraction conv oil emissions relevant EJ
    Original Eqn: MAX(0, real extraction conv oil EJ-("Non-energy use demand by final fuel EJ"[liquids])*share conv vs total oil extraction )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of emission-relevant conventional oil, i.e. excepting the
        resource used for non-energy uses. We assume conventional and
        unconventional resource are used for non-energy uses following the same
        share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_conv_oil_ej()
        - (float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]))
        * share_conv_vs_total_oil_extraction(),
    )


def real_extraction_conv_oil_mbd():
    """
    Real Name: "real extraction conv oil Mb/d"
    Original Eqn: real extraction conv oil EJ*"Mb/d per EJ/year"
    Units: Mb/d
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_extraction_conv_oil_ej() * mbd_per_ejyear()


def real_extraction_unconv_oil_ej():
    """
    Real Name: real extraction unconv oil EJ
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, extraction unconv oil EJ , "extraction unconv oil - tot agg" )
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: extraction_unconv_oil_ej(),
        lambda: extraction_unconv_oil__tot_agg(),
    )


def real_extraction_unconv_oil_emissions_relevant_ej():
    """
    Real Name: real extraction unconv oil emissions relevant EJ
    Original Eqn: MAX(0, real extraction unconv oil EJ-("Non-energy use demand by final fuel EJ"[liquids])*(1-share conv vs total oil extraction))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of emission-relevant unconventional oil, i.e. excepting the
        resource used for non-energy uses. We assume conventional and
        unconventional resource are used for non-energy uses following the same
        share as for their relative extraction.
    """
    return np.maximum(
        0,
        real_extraction_unconv_oil_ej()
        - (float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]))
        * (1 - share_conv_vs_total_oil_extraction()),
    )


def rurr_conv_oil():
    """
    Real Name: RURR conv oil
    Original Eqn: INTEG ( -extraction conv oil EJ-Flow conv oil left in ground, URR conv oil-cumulated conv oil extraction to 1995*"separate conv and unconv oil?")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR conventional oil.
    """
    return _integ_rurr_conv_oil()


def rurr_conv_oil_until_start_year_plg():
    """
    Real Name: RURR conv oil until start year PLG
    Original Eqn: SAMPLE IF TRUE(Time<Start policy leave in ground conv oil, RURR conv oil, RURR conv oil)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR until the start of the policy to leave in the ground (PLG) the
        resource.
    """
    return _sample_if_true_rurr_conv_oil_until_start_year_plg()


def rurr_tot_agg_oil():
    """
    Real Name: RURR tot agg oil
    Original Eqn: INTEG ( -extraction tot agg oil EJ-Flow tot agg oil left in ground, IF THEN ELSE("separate conv and unconv oil?"=0,URR tot agg oil -cumulated tot agg extraction to 1995,0))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR total aggregated oil.
    """
    return _integ_rurr_tot_agg_oil()


def rurr_tot_oil_until_start_year_plg():
    """
    Real Name: RURR tot oil until start year PLG
    Original Eqn: SAMPLE IF TRUE(Time<Start policy leave in ground tot agg oil, RURR tot agg oil, RURR tot agg oil)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR until the start of the policy to leave in the ground (PLG) the
        resource.
    """
    return _sample_if_true_rurr_tot_oil_until_start_year_plg()


def rurr_unconv_oil_ej():
    """
    Real Name: RURR unconv oil EJ
    Original Eqn: INTEG ( -extraction unconv oil EJ-Flow unconv oil left in ground, URR unconv oil-cumulated unconv oil extraction to 1995*"separate conv and unconv oil?")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR unconventional oil.
    """
    return _integ_rurr_unconv_oil_ej()


def rurr_unconv_oil_until_start_year_plg():
    """
    Real Name: RURR unconv oil until start year PLG
    Original Eqn: SAMPLE IF TRUE(Time<Start policy leave in ground unconv oil, RURR unconv oil EJ, RURR unconv oil EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR until the start of the policy to leave in the ground (PLG) the
        resource.
    """
    return _sample_if_true_rurr_unconv_oil_until_start_year_plg()


def scarcity_conv_oil():
    """
    Real Name: scarcity conv oil
    Original Eqn: IF THEN ELSE(max extraction conv oil EJ=0,0, IF THEN ELSE(max extraction conv oil EJ>=extraction conv oil EJ , 1-((max extraction conv oil EJ -extraction conv oil EJ)/max extraction conv oil EJ)^exponent availability conv oil,0))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Priority to conventional resource to cover the demand while the maximum
        extraction level of energy/time is not reached. If scarcity=1 there is no
        more available flow to be extracted.
    """
    return if_then_else(
        max_extraction_conv_oil_ej() == 0,
        lambda: 0,
        lambda: if_then_else(
            max_extraction_conv_oil_ej() >= extraction_conv_oil_ej(),
            lambda: 1
            - (
                (max_extraction_conv_oil_ej() - extraction_conv_oil_ej())
                / max_extraction_conv_oil_ej()
            )
            ** exponent_availability_conv_oil(),
            lambda: 0,
        ),
    )


def scarcity_conv_oil_delayed_1yr():
    """
    Real Name: scarcity conv oil delayed 1yr
    Original Eqn: DELAY FIXED ( scarcity conv oil, 1, 0.3989)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_scarcity_conv_oil_delayed_1yr()


def scarcity_conv_oil_stock():
    """
    Real Name: scarcity conv oil stock
    Original Eqn: INTEG ( increase scarcity conv oil, 0.3989)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_scarcity_conv_oil_stock()


def separate_conv_and_unconv_oil():
    """
    Real Name: "separate conv and unconv oil?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'separate_conv_unconv_oi')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to disaggregate between conventional and unconventional fuel: "1" =
        disaggregation, "0" = conv+unconv aggregated (all the oil flows then
        through the right side of this view, i.e. the "conventional oil" modelling
        side).
    """
    return _ext_constant_separate_conv_and_unconv_oil()


def share_conv_oil_vs_tot_agg():
    """
    Real Name: share conv oil vs tot agg
    Original Eqn: 1-share unconv oil vs tot agg
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - share_unconv_oil_vs_tot_agg()


def share_conv_vs_total_oil_extraction():
    """
    Real Name: share conv vs total oil extraction
    Original Eqn: ZIDZ( real extraction conv oil EJ, (real extraction conv oil EJ +real extraction unconv oil EJ) )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Share of conventional oil vs total oil extracted.
    """
    return zidz(
        real_extraction_conv_oil_ej(),
        (real_extraction_conv_oil_ej() + real_extraction_unconv_oil_ej()),
    )


def share_rurr_conv_oil_to_leave_underground():
    """
    Real Name: share RURR conv oil to leave underground
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'share_RURR_conv_oil_underground')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    RURR's conventional oil to be left in the ground as a share of the RURR in
        the year 2015.
    """
    return _ext_constant_share_rurr_conv_oil_to_leave_underground()


def share_rurr_tot_agg_oil_to_leave_underground():
    """
    Real Name: share RURR tot agg oil to leave underground
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'share_RURR_agg_oil_underground')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    RURR's total aggregatoid oil to be left in the ground as a share of the
        RURR in the year 2015.
    """
    return _ext_constant_share_rurr_tot_agg_oil_to_leave_underground()


def share_rurr_unconv_oil_to_leave_underground():
    """
    Real Name: share RURR unconv oil to leave underground
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'share_RURR_unconv_oil_underground')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    RURR's unconventional oil to be left in the ground as a share of the RURR
        in the year 2015.
    """
    return _ext_constant_share_rurr_unconv_oil_to_leave_underground()


def share_unconv_oil_vs_tot_agg():
    """
    Real Name: share unconv oil vs tot agg
    Original Eqn: IF THEN ELSE(Time>2012, MIN(evolution share unconv oil vs tot agg, 1), Historic unconv oil/PED total oil EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Evolution of the share of unconventional oil vs total aggregated oil.
    """
    return if_then_else(
        time() > 2012,
        lambda: np.minimum(evolution_share_unconv_oil_vs_tot_agg(), 1),
        lambda: historic_unconv_oil() / ped_total_oil_ej(),
    )


def share_unconv_oil_vs_tot_agg_in_2050():
    """
    Real Name: share unconv oil vs tot agg in 2050
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'share_unconv_vs_agg_oil_in_2050')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of unconventional oil vs total aggregated oil in 2050 depending on
        the maximum extraction curve selected for total aggregated oil.
    """
    return _ext_constant_share_unconv_oil_vs_tot_agg_in_2050()


def start_policy_leave_in_ground_conv_oil():
    """
    Real Name: Start policy leave in ground conv oil
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'start_policy_year_conv_oil_underground')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when the policy to leave in the ground an amount of conventional oil
        RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_conv_oil()


def start_policy_leave_in_ground_tot_agg_oil():
    """
    Real Name: Start policy leave in ground tot agg oil
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'start_policy_year_agg_oil_underground')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when the policy to leave in the ground an amount of total aggregated
        oil RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_oil()


def start_policy_leave_in_ground_unconv_oil():
    """
    Real Name: Start policy leave in ground unconv oil
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'start_policy_year_unconv_oil_underground')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when the policy to leave in the ground an amount of unconventional
        oil RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_unconv_oil()


def table_max_extraction_agg_oil(x):
    """
    Real Name: table max extraction agg oil
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'RURR_agg_oil', 'max_extraction_agg_oil')
    Units: EJ/year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_agg_oil(x)


def table_max_extraction_conv_oil(x):
    """
    Real Name: table max extraction conv oil
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'RURR_conv_oil', 'max_extraction_conv_oil'))
    Units: EJ/year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_conv_oil(x)


def table_max_extraction_unconv_oil(x):
    """
    Real Name: table max extraction unconv oil
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'RURR_unconv_oil', 'max_extraction_unconv_oil'))
    Units: EJ/year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_unconv_oil(x)


def tot_agg_oil_to_leave_underground():
    """
    Real Name: tot agg oil to leave underground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground tot agg oil, 0, RURR tot oil until start year PLG*share RURR tot agg oil to leave underground)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total aggregated oil to be left underground due to the application of a
        policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_tot_agg_oil(),
        lambda: 0,
        lambda: rurr_tot_oil_until_start_year_plg()
        * share_rurr_tot_agg_oil_to_leave_underground(),
    )


def tot_rurr_conv_oil():
    """
    Real Name: Tot RURR conv oil
    Original Eqn: RURR conv oil+Total conv oil left in ground
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total RURR of conventional oil considering the available RURR and the
        eventual amount of RURR left in the ground as a policy.
    """
    return rurr_conv_oil() + total_conv_oil_left_in_ground()


def tot_rurr_tot_agg_oil():
    """
    Real Name: Tot RURR tot agg oil
    Original Eqn: RURR tot agg oil+Total agg oil left in ground
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total RURR of total aggregated oil considering the available RURR and the
        eventual amount of RURR left in the ground as a policy.
    """
    return rurr_tot_agg_oil() + total_agg_oil_left_in_ground()


def tot_rurr_unconv_oil():
    """
    Real Name: Tot RURR unconv oil
    Original Eqn: RURR unconv oil EJ+Total unconv oil left in ground
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total RURR of unconventional oil considering the available RURR and the
        eventual amount of RURR left in the ground as a policy.
    """
    return rurr_unconv_oil_ej() + total_unconv_oil_left_in_ground()


def total_agg_oil_left_in_ground():
    """
    Real Name: Total agg oil left in ground
    Original Eqn: INTEG ( Flow tot agg oil left in ground, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total amount of aggregated oil left in the ground due to policies.
    """
    return _integ_total_agg_oil_left_in_ground()


def total_conv_oil_left_in_ground():
    """
    Real Name: Total conv oil left in ground
    Original Eqn: INTEG ( Flow conv oil left in ground, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total amount of conventional oil left in the ground due to policies.
    """
    return _integ_total_conv_oil_left_in_ground()


def total_unconv_oil_left_in_ground():
    """
    Real Name: Total unconv oil left in ground
    Original Eqn: INTEG ( Flow unconv oil left in ground, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total amount of unconventional oil left in the ground due to policies.
    """
    return _integ_total_unconv_oil_left_in_ground()


def unconv_oil_to_leave_underground():
    """
    Real Name: unconv oil to leave underground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground unconv oil,0, RURR unconv oil until start year PLG*share RURR unconv oil to leave underground )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Unconventional oil to be left underground due to the application of a
        policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_unconv_oil(),
        lambda: 0,
        lambda: rurr_unconv_oil_until_start_year_plg()
        * share_rurr_unconv_oil_to_leave_underground(),
    )


def unlimited_nre():
    """
    Real Name: "unlimited NRE?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'unlimited_NRE')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to consider if non-renewable resources (oil, gas, coal and uranium)
        are unlimited (1), or if it is limited (0). If limited then the available
        depletion curves are considered.
    """
    return _ext_constant_unlimited_nre()


def unlimited_oil():
    """
    Real Name: "unlimited oil?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'unlimited_oil')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to consider if oil is unlimited (1), or if it is limited (0). If
        limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_oil()


def urr_conv_oil():
    """
    Real Name: URR conv oil
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited oil?"=1, :NA:, URR conv oil input), 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Ultimately Recoverable Resources (URR) associated to the selected
        depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: if_then_else(
            logical_or(unlimited_nre() == 1, unlimited_oil() == 1),
            lambda: np.nan,
            lambda: urr_conv_oil_input(),
        ),
        lambda: 0,
    )


def urr_conv_oil_input():
    """
    Real Name: URR conv oil input
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'URR_conv_oil')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_urr_conv_oil_input()


def urr_tot_agg_oil():
    """
    Real Name: URR tot agg oil
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, 0, IF THEN ELSE("unlimited oil?"=1 :OR: "unlimited NRE?"=1, :NA:, URR tot agg oil input))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Ultimately Recoverable Resources (URR) associated to the selected
        depletion curve.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1,
        lambda: 0,
        lambda: if_then_else(
            logical_or(unlimited_oil() == 1, unlimited_nre() == 1),
            lambda: np.nan,
            lambda: urr_tot_agg_oil_input(),
        ),
    )


def urr_tot_agg_oil_input():
    """
    Real Name: URR tot agg oil input
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'URR_agg_oil')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_urr_tot_agg_oil_input()


def urr_unconv_oil():
    """
    Real Name: URR unconv oil
    Original Eqn: IF THEN ELSE("separate conv and unconv oil?"=1, URR unconv oil input, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    URR unconventional oil.
    """
    return if_then_else(
        separate_conv_and_unconv_oil() == 1, lambda: urr_unconv_oil_input(), lambda: 0
    )


def urr_unconv_oil_input():
    """
    Real Name: URR unconv oil input
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'URR_unconv_oil')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_urr_unconv_oil_input()


def year_scarcity_oil():
    """
    Real Name: Year scarcity oil
    Original Eqn: IF THEN ELSE(abundance total oil>0.95, 0, Time)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_total_oil() > 0.95, lambda: 0, lambda: time())


_delayfixed_abundance_unconv_oil_delayed_1yr = DelayFixed(
    lambda: abundance_unconv_oil(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_abundance_unconv_oil_delayed_1yr",
)


_integ_abundance_unconv_oil_stock = Integ(
    lambda: increase_abundance_unconv_oil(),
    lambda: 1,
    "_integ_abundance_unconv_oil_stock",
)


_delayfixed_check_liquids_delayed_1yr = DelayFixed(
    lambda: check_liquids(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_check_liquids_delayed_1yr",
)


_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr = DelayFixed(
    lambda: constrain_liquids_exogenous_growth(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_constrain_liquids_exogenous_growth_delayed_1yr",
)


_integ_cumulated_conv_oil_extraction = Integ(
    lambda: extraction_conv_oil_ej(),
    lambda: cumulated_conv_oil_extraction_to_1995(),
    "_integ_cumulated_conv_oil_extraction",
)


_ext_constant_cumulated_conv_oil_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_conventional_oil_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_conv_oil_extraction_to_1995",
)


_integ_cumulated_tot_agg_oil_extraction = Integ(
    lambda: extraction_tot_agg_oil_ej(),
    lambda: cumulated_tot_agg_extraction_to_1995(),
    "_integ_cumulated_tot_agg_oil_extraction",
)


_integ_cumulated_unconv_oil_extraction = Integ(
    lambda: extraction_unconv_oil_ej(),
    lambda: cumulated_unconv_oil_extraction_to_1995(),
    "_integ_cumulated_unconv_oil_extraction",
)


_ext_constant_cumulated_unconv_oil_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_unconventional_oil_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_unconv_oil_extraction_to_1995",
)


_delayfixed_extraction_unconv_oil_delayed = DelayFixed(
    lambda: extraction_unconv_oil_ej(),
    lambda: time_step(),
    lambda: 1.09,
    time_step,
    "_delayfixed_extraction_unconv_oil_delayed",
)


_ext_data_historic_unconv_oil = ExtData(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_unconv_oil",
)


_ext_constant_oil_refinery_gains_share = ExtConstant(
    "../energy.xlsx",
    "Global",
    "oil_refinery_gains_share",
    {},
    _root,
    "_ext_constant_oil_refinery_gains_share",
)


_ext_constant_p_constraint_growth_extraction_unconv_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unconv_oil_growth",
    {},
    _root,
    "_ext_constant_p_constraint_growth_extraction_unconv_oil",
)


_delayfixed_pes_oil_ej_delayed = DelayFixed(
    lambda: pes_oil_ej(),
    lambda: time_step(),
    lambda: 139.5,
    time_step,
    "_delayfixed_pes_oil_ej_delayed",
)


_integ_rurr_conv_oil = Integ(
    lambda: -extraction_conv_oil_ej() - flow_conv_oil_left_in_ground(),
    lambda: urr_conv_oil()
    - cumulated_conv_oil_extraction_to_1995() * separate_conv_and_unconv_oil(),
    "_integ_rurr_conv_oil",
)


_sample_if_true_rurr_conv_oil_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_conv_oil(),
    lambda: rurr_conv_oil(),
    lambda: rurr_conv_oil(),
    "_sample_if_true_rurr_conv_oil_until_start_year_plg",
)


_integ_rurr_tot_agg_oil = Integ(
    lambda: -extraction_tot_agg_oil_ej() - flow_tot_agg_oil_left_in_ground(),
    lambda: if_then_else(
        separate_conv_and_unconv_oil() == 0,
        lambda: urr_tot_agg_oil() - cumulated_tot_agg_extraction_to_1995(),
        lambda: 0,
    ),
    "_integ_rurr_tot_agg_oil",
)


_sample_if_true_rurr_tot_oil_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_tot_agg_oil(),
    lambda: rurr_tot_agg_oil(),
    lambda: rurr_tot_agg_oil(),
    "_sample_if_true_rurr_tot_oil_until_start_year_plg",
)


_integ_rurr_unconv_oil_ej = Integ(
    lambda: -extraction_unconv_oil_ej() - flow_unconv_oil_left_in_ground(),
    lambda: urr_unconv_oil()
    - cumulated_unconv_oil_extraction_to_1995() * separate_conv_and_unconv_oil(),
    "_integ_rurr_unconv_oil_ej",
)


_sample_if_true_rurr_unconv_oil_until_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_unconv_oil(),
    lambda: rurr_unconv_oil_ej(),
    lambda: rurr_unconv_oil_ej(),
    "_sample_if_true_rurr_unconv_oil_until_start_year_plg",
)


_delayfixed_scarcity_conv_oil_delayed_1yr = DelayFixed(
    lambda: scarcity_conv_oil(),
    lambda: 1,
    lambda: 0.3989,
    time_step,
    "_delayfixed_scarcity_conv_oil_delayed_1yr",
)


_integ_scarcity_conv_oil_stock = Integ(
    lambda: increase_scarcity_conv_oil(),
    lambda: 0.3989,
    "_integ_scarcity_conv_oil_stock",
)


_ext_constant_separate_conv_and_unconv_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "separate_conv_unconv_oi",
    {},
    _root,
    "_ext_constant_separate_conv_and_unconv_oil",
)


_ext_constant_share_rurr_conv_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_conv_oil_underground",
    {},
    _root,
    "_ext_constant_share_rurr_conv_oil_to_leave_underground",
)


_ext_constant_share_rurr_tot_agg_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_agg_oil_underground",
    {},
    _root,
    "_ext_constant_share_rurr_tot_agg_oil_to_leave_underground",
)


_ext_constant_share_rurr_unconv_oil_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_unconv_oil_underground",
    {},
    _root,
    "_ext_constant_share_rurr_unconv_oil_to_leave_underground",
)


_ext_constant_share_unconv_oil_vs_tot_agg_in_2050 = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_unconv_vs_agg_oil_in_2050",
    {},
    _root,
    "_ext_constant_share_unconv_oil_vs_tot_agg_in_2050",
)


_ext_constant_start_policy_leave_in_ground_conv_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_conv_oil_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_conv_oil",
)


_ext_constant_start_policy_leave_in_ground_tot_agg_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_agg_oil_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_tot_agg_oil",
)


_ext_constant_start_policy_leave_in_ground_unconv_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_unconv_oil_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_unconv_oil",
)


_ext_lookup_table_max_extraction_agg_oil = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_agg_oil",
    "max_extraction_agg_oil",
    {},
    _root,
    "_ext_lookup_table_max_extraction_agg_oil",
)


_ext_lookup_table_max_extraction_conv_oil = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_conv_oil",
    "max_extraction_conv_oil",
    {},
    _root,
    "_ext_lookup_table_max_extraction_conv_oil",
)


_ext_lookup_table_max_extraction_unconv_oil = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_unconv_oil",
    "max_extraction_unconv_oil",
    {},
    _root,
    "_ext_lookup_table_max_extraction_unconv_oil",
)


_integ_total_agg_oil_left_in_ground = Integ(
    lambda: flow_tot_agg_oil_left_in_ground(),
    lambda: 0,
    "_integ_total_agg_oil_left_in_ground",
)


_integ_total_conv_oil_left_in_ground = Integ(
    lambda: flow_conv_oil_left_in_ground(),
    lambda: 0,
    "_integ_total_conv_oil_left_in_ground",
)


_integ_total_unconv_oil_left_in_ground = Integ(
    lambda: flow_unconv_oil_left_in_ground(),
    lambda: 0,
    "_integ_total_unconv_oil_left_in_ground",
)


_ext_constant_unlimited_nre = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_NRE",
    {},
    _root,
    "_ext_constant_unlimited_nre",
)


_ext_constant_unlimited_oil = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_oil",
    {},
    _root,
    "_ext_constant_unlimited_oil",
)


_ext_constant_urr_conv_oil_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_conv_oil",
    {},
    _root,
    "_ext_constant_urr_conv_oil_input",
)


_ext_constant_urr_tot_agg_oil_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_agg_oil",
    {},
    _root,
    "_ext_constant_urr_tot_agg_oil_input",
)


_ext_constant_urr_unconv_oil_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_unconv_oil",
    {},
    _root,
    "_ext_constant_urr_unconv_oil_input",
)
