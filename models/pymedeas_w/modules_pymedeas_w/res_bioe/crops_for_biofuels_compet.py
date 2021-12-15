"""
Module crops_for_biofuels_compet
Translated using PySD version 2.2.0
"""


def adapt_growth_biofuels_2gen():
    """
    Real Name: adapt growth biofuels 2gen
    Original Eqn: IF THEN ELSE(Time<2015, 0, IF THEN ELSE(Time<2020, past biofuels 2gen+(P biofuels 2gen-past biofuels 2gen)*(Time-2015)/5, P biofuels 2gen))
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Modeling of a soft transition from current historic annual growth to reach the
        policy-objective 5 years later.        IF THEN ELSE(Time<2015, 0, IF THEN ELSE(Time<2020, past solar+(P
        solar-past solar)*(Time-2015)/5, P solar))
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: if_then_else(
            time() < 2020,
            lambda: past_biofuels_2gen()
            + (p_biofuels_2gen() - past_biofuels_2gen()) * (time() - 2015) / 5,
            lambda: p_biofuels_2gen(),
        ),
    )


def additional_land_compet_available_for_biofuels():
    """
    Real Name: Additional land compet available for biofuels
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C41')
    Units: MHa/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Available land for biofuels in competition with other uses depending on
        the scenario.
    """
    return _ext_constant_additional_land_compet_available_for_biofuels()


def annual_additional_historic_land_use_biofuels_2gen():
    """
    Real Name: Annual additional historic land use biofuels 2gen
    Original Eqn: Annual additional historic product biofuels 2gen*EJ per ktoe/Land productivity biofuels 2gen EJ MHa
    Units: MHa/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        annual_additional_historic_product_biofuels_2gen()
        * ej_per_ktoe()
        / land_productivity_biofuels_2gen_ej_mha()
    )


def annual_additional_historic_product_biofuels_2gen():
    """
    Real Name: Annual additional historic product biofuels 2gen
    Original Eqn: IF THEN ELSE(Time<2015, Historic produc biofuels 2gen(Time+1)-Historic produc biofuels 2gen(Time), 0)
    Units: ktoe/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual additional historic production of liquids from biofuels ethanol and
        biodiesel, ktoe/year (1990-2015). Ref: BP 2016.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_produc_biofuels_2gen(time() + 1)
        - historic_produc_biofuels_2gen(time()),
        lambda: 0,
    )


def annual_shift_from_2gen_to_3gen():
    """
    Real Name: Annual shift from 2gen to 3gen
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C44')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of the land dedicated for biofuels from the 2nd generation shifted
        to 3rd generation in the next year.
    """
    return _ext_constant_annual_shift_from_2gen_to_3gen()


def biofuels_3gen_land_compet_available():
    """
    Real Name: Biofuels 3gen land compet available
    Original Eqn: (Max land compet biofuels 2gen-Land compet biofuels 3gen Mha)/Max land compet biofuels 2gen
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential land available (dedicated to 2nd generation) as given
        as a fraction of unity. We assume that no new land starts directly to
        produce biofuels 3rd generation biofuels.
    """
    return (
        max_land_compet_biofuels_2gen() - land_compet_biofuels_3gen_mha()
    ) / max_land_compet_biofuels_2gen()


def biofuels_land_compet_available():
    """
    Real Name: Biofuels land compet available
    Original Eqn: (Max land compet biofuels 2gen-Land compet biofuels 2gen Mha-Land compet biofuels 3gen Mha)/Max land compet biofuels 2gen
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential land available as given as a fraction of unity.
    """
    return (
        max_land_compet_biofuels_2gen()
        - land_compet_biofuels_2gen_mha()
        - land_compet_biofuels_3gen_mha()
    ) / max_land_compet_biofuels_2gen()


def efficiency_improvement_biofuels_3gen():
    """
    Real Name: Efficiency improvement biofuels 3gen
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_improvement_biofuels_third_generation')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency improvements of 3rd generation (cellulosic) in relation to 2nd
        generation biofuels.
    """
    return _ext_constant_efficiency_improvement_biofuels_3gen()


def ej_per_ktoe():
    """
    Real Name: EJ per ktoe
    Original Eqn: 4.1868e-05
    Units: EJ/ktoe
    Limits: (None, None)
    Type: constant
    Subs: None

    1 ktoe = 0.000041868 EJ.
    """
    return 4.1868e-05


def historic_land_compet_available_for_biofuels_2gen():
    """
    Real Name: Historic land compet available for biofuels 2gen
    Original Eqn: 74847.7*EJ per ktoe/Land productivity biofuels 2gen EJ MHa
    Units: MHa/year
    Limits: (None, None)
    Type: component
    Subs: None

    Land occupied by biofuels in 2015. Biofuels production in 2015: 7,4847.7
        ktoe (BP 2016).
    """
    return 74847.7 * ej_per_ktoe() / land_productivity_biofuels_2gen_ej_mha()


def historic_produc_biofuels_2gen(x):
    """
    Real Name: Historic produc biofuels 2gen
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'time_historic_data', 'historic_production_of_second_generation_biofuels'))
    Units: ktoe/year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic production of biofuels 2nd generation (1990-2015).
    """
    return _ext_lookup_historic_produc_biofuels_2gen(x)


def initial_value_land_compet_biofuels_2gen_ktoe():
    """
    Real Name: initial value land compet biofuels 2gen ktoe
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'initial_production_of_second_generation_biofuels')
    Units: EJ/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial value in 1995 derived from (BP 2016).
    """
    return _ext_constant_initial_value_land_compet_biofuels_2gen_ktoe()


def initial_value_land_compet_biofuels_2gen_mha():
    """
    Real Name: initial value land compet biofuels 2gen Mha
    Original Eqn: initial value land compet biofuels 2gen ktoe*EJ per ktoe
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Initial value of land occupation by biofuels of second generation.
    """
    return initial_value_land_compet_biofuels_2gen_ktoe() * ej_per_ktoe()


def land_compet_2gen_vs_total_land_compet():
    """
    Real Name: land compet 2gen vs total land compet
    Original Eqn: Land compet biofuels 2gen Mha/Land compet required dedicated crops for biofuels
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Land dedicated to 2nd generation biofuels vs total land competition for
        biofuels [to prevent stock "Land compet biofuels 2gen Mha" goes negative].
    """
    return (
        land_compet_biofuels_2gen_mha()
        / land_compet_required_dedicated_crops_for_biofuels()
    )


def land_compet_biofuels_2gen_mha():
    """
    Real Name: Land compet biofuels 2gen Mha
    Original Eqn: INTEG ( new biofuels 2gen land compet-Land shifted to biofuels 3gen, initial value land compet biofuels 2gen Mha*Land productivity biofuels 2gen EJ MHa)
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual land dedicated to biofuel production in land competing with
        other uses.
    """
    return _integ_land_compet_biofuels_2gen_mha()


def land_compet_biofuels_3gen_mha():
    """
    Real Name: Land compet biofuels 3gen Mha
    Original Eqn: INTEG ( Land shifted to biofuels 3gen, 0)
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land subject to competition dedicated to biofuels 3rd generation as a
        shift of surface previously dedicated to biofuels from the 2nd generation.
    """
    return _integ_land_compet_biofuels_3gen_mha()


def land_compet_required_dedicated_crops_for_biofuels():
    """
    Real Name: Land compet required dedicated crops for biofuels
    Original Eqn: Land compet biofuels 2gen Mha+Land compet biofuels 3gen Mha
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for crops for biofuels 2nd and 3rd generation (in land
        competing with other uses).
    """
    return land_compet_biofuels_2gen_mha() + land_compet_biofuels_3gen_mha()


def land_productivity_biofuels_2gen_ej_mha():
    """
    Real Name: Land productivity biofuels 2gen EJ MHa
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'land_productivity_biofuels_second_generation')
    Units: EJ/MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Energy output per area of biofuels 2nd generation (final energy). Source:
        de Castro et al (2014).
    """
    return _ext_constant_land_productivity_biofuels_2gen_ej_mha()


def land_shifted_to_biofuels_3gen():
    """
    Real Name: Land shifted to biofuels 3gen
    Original Eqn: IF THEN ELSE(Time<start year 3gen,0, IF THEN ELSE(Time<(start year 3gen+5), Annual shift from 2gen to 3gen *Land compet biofuels 2gen Mha*Biofuels 3gen land compet available *land compet 2gen vs total land compet, P biofuels 3gen*Land compet biofuels 3gen Mha*Biofuels 3gen land compet available*land compet 2gen vs total land compet))
    Units: MHa/year
    Limits: (None, None)
    Type: component
    Subs: None

    New land dedicated to biofuels 3rd generation in land competing with other uses as a
        shift of surface previously dedicated to biofuels from the 2nd generation.
        We assume that no new land starts directly to produce biofuels 3rd
        generation biofuels.                IF THEN ELSE(Time<start year 3gen,0,        IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?"*Land compet
        biofuels 3gen Mha,        IF THEN ELSE(Time<(start year 3gen+5), Annual shift from 2gen to 3gen*Land
        compet biofuels 2gen Mha*Biofuels 3gen land compet available*land compet
        2gen vs total land compet, P biofuels 3gen*Land compet biofuels 3gen
        Mha*Biofuels 3gen land compet available*land compet 2gen vs total land
        compet)))
    """
    return if_then_else(
        time() < start_year_3gen(),
        lambda: 0,
        lambda: if_then_else(
            time() < (start_year_3gen() + 5),
            lambda: annual_shift_from_2gen_to_3gen()
            * land_compet_biofuels_2gen_mha()
            * biofuels_3gen_land_compet_available()
            * land_compet_2gen_vs_total_land_compet(),
            lambda: p_biofuels_3gen()
            * land_compet_biofuels_3gen_mha()
            * biofuels_3gen_land_compet_available()
            * land_compet_2gen_vs_total_land_compet(),
        ),
    )


def max_land_compet_biofuels_2gen():
    """
    Real Name: Max land compet biofuels 2gen
    Original Eqn: Additional land compet available for biofuels+Historic land compet available for biofuels 2gen
    Units: MHa/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual potential of biofuels (final energy) 2nd generation competing with
        other land uses.
    """
    return (
        additional_land_compet_available_for_biofuels()
        + historic_land_compet_available_for_biofuels_2gen()
    )


def max_peavail_potential_biofuels_23gen():
    """
    Real Name: "Max PEavail potential biofuels 2-3gen"
    Original Eqn: IF THEN ELSE(Time<start year 3gen, Max land compet biofuels 2gen *Land productivity biofuels 2gen EJ MHa, Max land compet biofuels 2gen*Land productivity biofuels 2gen EJ MHa*(1+Efficiency improvement biofuels 3gen))
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual biofuels potential (primary energy) available from land competition.
    """
    return if_then_else(
        time() < start_year_3gen(),
        lambda: max_land_compet_biofuels_2gen()
        * land_productivity_biofuels_2gen_ej_mha(),
        lambda: max_land_compet_biofuels_2gen()
        * land_productivity_biofuels_2gen_ej_mha()
        * (1 + efficiency_improvement_biofuels_3gen()),
    )


def new_biofuels_2gen_land_compet():
    """
    Real Name: new biofuels 2gen land compet
    Original Eqn: IF THEN ELSE(check liquids<-0.0001, "constrain liquids exogenous growth?"*Land compet biofuels 2gen Mha, MAX(Annual additional historic land use biofuels 2gen+adapt growth biofuels 2gen *Land compet biofuels 2gen Mha*Biofuels land compet available,0))
    Units: MHa/year
    Limits: (None, None)
    Type: component
    Subs: None

    New land dedicated to biofuels 2nd generation in land competing with other
        uses.
    """
    return if_then_else(
        check_liquids() < -0.0001,
        lambda: constrain_liquids_exogenous_growth() * land_compet_biofuels_2gen_mha(),
        lambda: np.maximum(
            annual_additional_historic_land_use_biofuels_2gen()
            + adapt_growth_biofuels_2gen()
            * land_compet_biofuels_2gen_mha()
            * biofuels_land_compet_available(),
            0,
        ),
    )


def p_biofuels_2gen():
    """
    Real Name: P biofuels 2gen
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C40')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_biofuels_2gen()


def p_biofuels_3gen():
    """
    Real Name: P biofuels 3gen
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C42')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_biofuels_3gen()


def past_biofuels_2gen():
    """
    Real Name: past biofuels 2gen
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'historic_growth_biofuels_second_generation')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Current growth patterns (1990-2015).
    """
    return _ext_constant_past_biofuels_2gen()


def pe_biofuels_prod_2gen3gen_ej():
    """
    Real Name: "PE biofuels prod 2gen+3gen EJ"
    Original Eqn: (PEavail biofuels 2gen land compet EJ+PEavail biofuels 3gen land compet EJ)/Conv efficiency from NPP to biofuels
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual primary energy biomass for biofuel production (2nd and 3rd
        generation) in marginal lands.
    """
    return (
        peavail_biofuels_2gen_land_compet_ej() + peavail_biofuels_3gen_land_compet_ej()
    ) / conv_efficiency_from_npp_to_biofuels()


def peavail_biofuels_2gen_land_compet_ej():
    """
    Real Name: PEavail biofuels 2gen land compet EJ
    Original Eqn: Potential PEavail biofuels 2gen land compet EJ*(1-share biofuels overcapacity)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy available of biofuels from dedicated crops (2nd generation).
    """
    return potential_peavail_biofuels_2gen_land_compet_ej() * (
        1 - share_biofuels_overcapacity()
    )


def peavail_biofuels_3gen_land_compet_ej():
    """
    Real Name: PEavail biofuels 3gen land compet EJ
    Original Eqn: Potential PEavail biofuels prod 3gen EJ*(1-share biofuels overcapacity )
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy available of biofuels from dedicated crops (3rd generation).
    """
    return potential_peavail_biofuels_prod_3gen_ej() * (
        1 - share_biofuels_overcapacity()
    )


def potential_peavail_biofuels_2gen_land_compet_ej():
    """
    Real Name: Potential PEavail biofuels 2gen land compet EJ
    Original Eqn: Land compet biofuels 2gen Mha*Land productivity biofuels 2gen EJ MHa
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential primary energy available of biofuels from dedicated crops (2nd
        generation).
    """
    return land_compet_biofuels_2gen_mha() * land_productivity_biofuels_2gen_ej_mha()


def potential_peavail_biofuels_prod_3gen_ej():
    """
    Real Name: Potential PEavail biofuels prod 3gen EJ
    Original Eqn: Land compet biofuels 3gen Mha*Land productivity biofuels 2gen EJ MHa*(1+Efficiency improvement biofuels 3gen)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential Final Energy production (EJ) of biofuels from dedicated crops
        (3rd generation).
    """
    return (
        land_compet_biofuels_3gen_mha()
        * land_productivity_biofuels_2gen_ej_mha()
        * (1 + efficiency_improvement_biofuels_3gen())
    )


def start_year_3gen():
    """
    Real Name: start year 3gen
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C43')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    First year when 3rd generation biofuels are available.
    """
    return _ext_constant_start_year_3gen()


_ext_constant_additional_land_compet_available_for_biofuels = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C41",
    {},
    _root,
    "_ext_constant_additional_land_compet_available_for_biofuels",
)


_ext_constant_annual_shift_from_2gen_to_3gen = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C44",
    {},
    _root,
    "_ext_constant_annual_shift_from_2gen_to_3gen",
)


_ext_constant_efficiency_improvement_biofuels_3gen = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improvement_biofuels_third_generation",
    {},
    _root,
    "_ext_constant_efficiency_improvement_biofuels_3gen",
)


_ext_lookup_historic_produc_biofuels_2gen = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_production_of_second_generation_biofuels",
    {},
    _root,
    "_ext_lookup_historic_produc_biofuels_2gen",
)


_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_production_of_second_generation_biofuels",
    {},
    _root,
    "_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe",
)


_integ_land_compet_biofuels_2gen_mha = Integ(
    lambda: new_biofuels_2gen_land_compet() - land_shifted_to_biofuels_3gen(),
    lambda: initial_value_land_compet_biofuels_2gen_mha()
    * land_productivity_biofuels_2gen_ej_mha(),
    "_integ_land_compet_biofuels_2gen_mha",
)


_integ_land_compet_biofuels_3gen_mha = Integ(
    lambda: land_shifted_to_biofuels_3gen(),
    lambda: 0,
    "_integ_land_compet_biofuels_3gen_mha",
)


_ext_constant_land_productivity_biofuels_2gen_ej_mha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "land_productivity_biofuels_second_generation",
    {},
    _root,
    "_ext_constant_land_productivity_biofuels_2gen_ej_mha",
)


_ext_constant_p_biofuels_2gen = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C40",
    {},
    _root,
    "_ext_constant_p_biofuels_2gen",
)


_ext_constant_p_biofuels_3gen = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C42",
    {},
    _root,
    "_ext_constant_p_biofuels_3gen",
)


_ext_constant_past_biofuels_2gen = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_biofuels_second_generation",
    {},
    _root,
    "_ext_constant_past_biofuels_2gen",
)


_ext_constant_start_year_3gen = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C43",
    {},
    _root,
    "_ext_constant_start_year_3gen",
)
