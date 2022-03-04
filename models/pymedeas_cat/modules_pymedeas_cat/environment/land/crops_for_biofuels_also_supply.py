"""
Module crops_for_biofuels_also_supply
Translated using PySD version 2.2.1
"""


def adapt_growth_biofuels_2gen():
    """
    Real Name: adapt growth biofuels 2gen
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later. Growth for 2nd generation biofuels in competition and marginal lands.
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: if_then_else(
            time() < 2020,
            lambda: past_biofuels_2gen()
            + (p_biofuels_2gen_land_compet() - past_biofuels_2gen())
            * (time() - 2015)
            / 5,
            lambda: p_biofuels_2gen_land_compet(),
        ),
    )


def additional_land_compet_available_for_biofuels():
    """
    Real Name: Additional land compet available for biofuels
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available land for biofuels in competition with other uses depending on the scenario.
    """
    return agricultural_land() * max_additional_potential_land_for_biofuels_compet()


def annual_additional_historic_land_use_biofuels_2gen():
    """
    Real Name: Annual additional historic land use biofuels 2gen
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        annual_additional_historic_product_biofuels_2gen()
        * ej_per_ktoe()
        / land_productivity_biofuels_2gen_ej_mha()
    )


def annual_additional_historic_product_biofuels_2gen():
    """
    Real Name: Annual additional historic product biofuels 2gen
    Original Eqn:
    Units: ktoe/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual additional historic production of liquids from biofuels ethanol and biodiesel, ktoe/Year (1990-2015). Ref: BP 2016.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_produc_biofuels_2gen(integer(time() + 1))
        - historic_produc_biofuels_2gen(integer(time())),
        lambda: 0,
    )


def annual_shift_from_2gen_to_3gen():
    """
    Real Name: Annual shift from 2gen to 3gen
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of the land dedicated for biofuels from the 2nd generation shifted to 3rd generation in the next year.
    """
    return _ext_constant_annual_shift_from_2gen_to_3gen()


_ext_constant_annual_shift_from_2gen_to_3gen = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "annual_shift_from_second_generation_to_third_generation",
    {},
    _root,
    "_ext_constant_annual_shift_from_2gen_to_3gen",
)


def biofuel_production_2015():
    """
    Real Name: biofuel production 2015
    Original Eqn:
    Units: ktoe/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Biofuel production in 2015 (BP 2016).
    """
    return _ext_constant_biofuel_production_2015()


_ext_constant_biofuel_production_2015 = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "production_of_second_generation_biofuel_2015",
    {},
    _root,
    "_ext_constant_biofuel_production_2015",
)


def biofuels_3gen_land_compet_available():
    """
    Real Name: Biofuels 3gen land compet available
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential land available (dedicated to 2nd generation) as given as a fraction of unity. We assume that no new land starts directly to produce biofuels 3rd generation biofuels.
    """
    return (
        max_land_compet_biofuels_2gen() - land_compet_biofuels_3gen_mha()
    ) / max_land_compet_biofuels_2gen()


def biofuels_land_compet_available():
    """
    Real Name: Biofuels land compet available
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency improvements of 3rd generation (cellulosic) in relation to 2nd generation biofuels.
    """
    return _ext_constant_efficiency_improvement_biofuels_3gen()


_ext_constant_efficiency_improvement_biofuels_3gen = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improvement_biofuels_third_generation",
    {},
    _root,
    "_ext_constant_efficiency_improvement_biofuels_3gen",
)


def ej_per_ktoe():
    """
    Real Name: EJ per ktoe
    Original Eqn:
    Units: EJ/ktoe
    Limits: (None, None)
    Type: Constant
    Subs: []

    1 ktoe = 0.000041868 EJ.
    """
    return 4.1868e-05


def historic_produc_biofuels_2gen(x):
    """
    Real Name: Historic produc biofuels 2gen
    Original Eqn:
    Units: ktoe/Year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic production of biofuels 2nd generation (1990-2015).
    """
    return _ext_lookup_historic_produc_biofuels_2gen(x)


_ext_lookup_historic_produc_biofuels_2gen = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_production_of_second_generation_biofuels",
    {},
    _root,
    "_ext_lookup_historic_produc_biofuels_2gen",
)


def initial_value_land_compet_biofuels_2gen_ktoe():
    """
    Real Name: initial value land compet biofuels 2gen ktoe
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial value in 1995 derived from (BP 2016).
    """
    return _ext_constant_initial_value_land_compet_biofuels_2gen_ktoe()


_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_production_of_second_generation_biofuels",
    {},
    _root,
    "_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe",
)


def initial_value_land_compet_biofuels_2gen_mha():
    """
    Real Name: initial value land compet biofuels 2gen Mha
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Initial value of land occupation by biofuels of second generation.
    """
    return initial_value_land_compet_biofuels_2gen_ktoe() * ej_per_ktoe()


def land_compet_2gen_vs_total_land_compet():
    """
    Real Name: land compet 2gen vs total land compet
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land dedicated to 2nd generation biofuels vs total land competition for biofuels [to prevent stock "Land compet biofuels 2gen Mha" goes negative].
    """
    return (
        land_compet_biofuels_2gen_mha()
        / land_compet_required_dedicated_crops_for_biofuels()
    )


def land_compet_available_for_biofuels_2gen_2015():
    """
    Real Name: Land compet available for biofuels 2gen 2015
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land occupied by biofuels in 2015.
    """
    return (
        biofuel_production_2015()
        * ej_per_ktoe()
        / land_productivity_biofuels_2gen_ej_mha()
    )


def land_compet_biofuels_2gen_abandonned():
    """
    Real Name: Land compet biofuels 2gen abandonned
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land previously dedicated to produce biofuels 2nd generation and abandoned due to reduced liquids demand.
    """
    return land_compet_biofuels_2gen_mha() * share_biofuels_overcapacity()


def land_compet_biofuels_2gen_mha():
    """
    Real Name: Land compet biofuels 2gen Mha
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total annual land dedicated to biofuel production in land competing with other uses.
    """
    return _integ_land_compet_biofuels_2gen_mha()


_integ_land_compet_biofuels_2gen_mha = Integ(
    lambda: new_biofuels_2gen_land_compet()
    - land_compet_biofuels_2gen_abandonned()
    - land_shifted_to_biofuels_3gen(),
    lambda: initial_value_land_compet_biofuels_2gen_mha()
    * land_productivity_biofuels_2gen_ej_mha(),
    "_integ_land_compet_biofuels_2gen_mha",
)


def land_compet_biofuels_3gen_abandonned():
    """
    Real Name: Land compet biofuels 3gen abandonned
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land previously dedicated to produce biofuels 3rd generation and abandoned due to reduced liquids demand.
    """
    return land_compet_biofuels_3gen_mha() * share_biofuels_overcapacity()


def land_compet_biofuels_3gen_mha():
    """
    Real Name: Land compet biofuels 3gen Mha
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Land subject to competition dedicated to biofuels 3rd generation as a shift of surface previously dedicated to biofuels from the 2nd generation.
    """
    return _integ_land_compet_biofuels_3gen_mha()


_integ_land_compet_biofuels_3gen_mha = Integ(
    lambda: land_shifted_to_biofuels_3gen() - land_compet_biofuels_3gen_abandonned(),
    lambda: 0,
    "_integ_land_compet_biofuels_3gen_mha",
)


def land_compet_required_dedicated_crops_for_biofuels():
    """
    Real Name: Land compet required dedicated crops for biofuels
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land requirements for crops for biofuels 2nd and 3rd generation (in land competing with other uses).
    """
    return land_compet_biofuels_2gen_mha() + land_compet_biofuels_3gen_mha()


def land_productivity_biofuels_2gen_ej_mha():
    """
    Real Name: Land productivity biofuels 2gen EJ MHa
    Original Eqn:
    Units: EJ/MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Energy output per area of biofuels 2nd generation (final energy). Source: de Castro et al (2014): 0.155 W/m2.
    """
    return _ext_constant_land_productivity_biofuels_2gen_ej_mha()


_ext_constant_land_productivity_biofuels_2gen_ej_mha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "land_productivity_biofuels_second_generation",
    {},
    _root,
    "_ext_constant_land_productivity_biofuels_2gen_ej_mha",
)


def land_shifted_to_biofuels_3gen():
    """
    Real Name: Land shifted to biofuels 3gen
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New land dedicated to biofuels 3rd generation in land competing with other uses as a shift of surface previously dedicated to biofuels from the 2nd generation. We assume that no new land starts directly to produce biofuels 3rd generation biofuels. IF THEN ELSE(Time<start year 3gen,0, IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?"*Land compet biofuels 3gen Mha, IF THEN ELSE(Time<(start year 3gen+5), Annual shift from 2gen to 3gen*Land compet biofuels 2gen Mha*Biofuels 3gen land compet available*land compet 2gen vs total land compet, P biofuels 3gen*Land compet biofuels 3gen Mha*Biofuels 3gen land compet available*land compet 2gen vs total land compet)))
    """
    return if_then_else(
        time() < start_year_3gen_cellulosic_biofuels(),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_3gen_cellulosic_biofuels() + 5,
            lambda: annual_shift_from_2gen_to_3gen()
            * land_compet_biofuels_2gen_mha()
            * biofuels_3gen_land_compet_available()
            * land_compet_2gen_vs_total_land_compet(),
            lambda: p_biofuels_3gen_land_compet()
            * land_compet_biofuels_3gen_mha()
            * biofuels_3gen_land_compet_available()
            * land_compet_2gen_vs_total_land_compet(),
        ),
    )


def max_additional_potential_land_for_biofuels_compet():
    """
    Real Name: "max additional potential land for biofuels (compet)"
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Additional (apart from historically used) available land for biofuels in competition with other uses as a share of total agricultural land.
    """
    return _ext_constant_max_additional_potential_land_for_biofuels_compet()


_ext_constant_max_additional_potential_land_for_biofuels_compet = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "max_additional_pot_land_biofuels",
    {},
    _root,
    "_ext_constant_max_additional_potential_land_for_biofuels_compet",
)


def max_land_compet_biofuels_2gen():
    """
    Real Name: Max land compet biofuels 2gen
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual potential of biofuels (final energy) 2nd generation competing with other land uses.
    """
    return (
        additional_land_compet_available_for_biofuels()
        + land_compet_available_for_biofuels_2gen_2015()
    )


def max_peavail_potential_biofuels_land_compet():
    """
    Real Name: Max PEavail potential biofuels land compet
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual biofuels potential (primary energy) available from land competition.
    """
    return if_then_else(
        time() < start_year_3gen_cellulosic_biofuels(),
        lambda: max_land_compet_biofuels_2gen()
        * land_productivity_biofuels_2gen_ej_mha(),
        lambda: max_land_compet_biofuels_2gen()
        * land_productivity_biofuels_2gen_ej_mha()
        * (1 + efficiency_improvement_biofuels_3gen()),
    )


def new_biofuels_2gen_land_compet():
    """
    Real Name: new biofuels 2gen land compet
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New land dedicated to biofuels 2nd generation in land competing with other uses.
    """
    return (
        if_then_else(
            check_liquids() < 0,
            lambda: constrain_liquids_exogenous_growth()
            * land_compet_biofuels_2gen_mha(),
            lambda: np.maximum(
                annual_additional_historic_land_use_biofuels_2gen()
                + adapt_growth_biofuels_2gen()
                * land_compet_biofuels_2gen_mha()
                * biofuels_land_compet_available(),
                0,
            ),
        )
        * scarcity_agricultural_land()
    )


def p_biofuels_2gen_land_compet():
    """
    Real Name: P biofuels 2gen land compet
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_biofuels_2gen_land_compet()


_ext_constant_p_biofuels_2gen_land_compet = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_biofuels_2gen_land_compet_growth",
    {},
    _root,
    "_ext_constant_p_biofuels_2gen_land_compet",
)


def p_biofuels_3gen_land_compet():
    """
    Real Name: P biofuels 3gen land compet
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_biofuels_3gen_land_compet()


_ext_constant_p_biofuels_3gen_land_compet = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_biofuels_3gen_land_compet_growth",
    {},
    _root,
    "_ext_constant_p_biofuels_3gen_land_compet",
)


def past_biofuels_2gen():
    """
    Real Name: past biofuels 2gen
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current growth patterns (1990-2015).
    """
    return _ext_constant_past_biofuels_2gen()


_ext_constant_past_biofuels_2gen = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_biofuels_second_generation",
    {},
    _root,
    "_ext_constant_past_biofuels_2gen",
)


def pe_biofuels_prod_2gen3gen_ej():
    """
    Real Name: "PE biofuels prod 2gen+3gen EJ"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total annual primary energy biomass for biofuel production (2nd and 3rd generation) in marginal lands.
    """
    return (
        peavail_biofuels_2gen_land_compet_ej() + peavail_biofuels_3gen_land_compet_ej()
    ) / conv_efficiency_from_npp_to_biofuels()


def peavail_biofuels_2gen_land_compet_ej():
    """
    Real Name: PEavail biofuels 2gen land compet EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy available of biofuels from dedicated crops (2nd generation).
    """
    return potential_peavail_biofuels_2gen_land_compet_ej() * (
        1 - share_biofuels_overcapacity()
    )


def peavail_biofuels_3gen_land_compet_ej():
    """
    Real Name: PEavail biofuels 3gen land compet EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy available of biofuels from dedicated crops (3rd generation).
    """
    return potential_peavail_biofuels_prod_3gen_ej() * (
        1 - share_biofuels_overcapacity()
    )


def peavail_tot_biofuels_land_compet_ej():
    """
    Real Name: PEavail tot biofuels land compet EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy available of biofuels from dedicated crops -in land competition- (2nd and 3rd generation).
    """
    return (
        peavail_biofuels_2gen_land_compet_ej() + peavail_biofuels_3gen_land_compet_ej()
    )


def potential_peavail_biofuels_2gen_land_compet_ej():
    """
    Real Name: Potential PEavail biofuels 2gen land compet EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential primary energy available of biofuels from dedicated crops (2nd generation).
    """
    return land_compet_biofuels_2gen_mha() * land_productivity_biofuels_2gen_ej_mha()


def potential_peavail_biofuels_prod_3gen_ej():
    """
    Real Name: Potential PEavail biofuels prod 3gen EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential Final Energy production (EJ) of biofuels from dedicated crops (3rd generation).
    """
    return (
        land_compet_biofuels_3gen_mha()
        * land_productivity_biofuels_2gen_ej_mha()
        * (1 + efficiency_improvement_biofuels_3gen())
    )


def remaining_potential_biofuels_land_compet():
    """
    Real Name: remaining potential biofuels land compet
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_peavail_potential_biofuels_land_compet()
        > peavail_tot_biofuels_land_compet_ej(),
        lambda: (
            max_peavail_potential_biofuels_land_compet()
            - peavail_tot_biofuels_land_compet_ej()
        )
        / max_peavail_potential_biofuels_land_compet(),
        lambda: 0,
    )


def start_year_3gen_cellulosic_biofuels():
    """
    Real Name: start year 3gen cellulosic biofuels
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    First year when 3rd generation biofuels are available.
    """
    return _ext_constant_start_year_3gen_cellulosic_biofuels()


_ext_constant_start_year_3gen_cellulosic_biofuels = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "start_year_3gen_cell_biofuels",
    {},
    _root,
    "_ext_constant_start_year_3gen_cellulosic_biofuels",
)
