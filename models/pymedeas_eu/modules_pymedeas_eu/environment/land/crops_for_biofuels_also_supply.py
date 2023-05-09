"""
Module environment.land.crops_for_biofuels_also_supply
Translated using PySD version 3.10.0
"""


@component.add(
    name="adapt growth biofuels 2gen",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "past_biofuels_2gen": 2, "p_biofuels_2gen_land_compet": 2},
)
def adapt_growth_biofuels_2gen():
    """
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


@component.add(
    name="Additional land compet available for biofuels",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_additional_land_compet_available_for_biofuels"
    },
)
def additional_land_compet_available_for_biofuels():
    """
    Available land for biofuels in competition with other uses depending on the scenario.
    """
    return _ext_constant_additional_land_compet_available_for_biofuels()


_ext_constant_additional_land_compet_available_for_biofuels = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "additional_land_compet_for_biofuels",
    {},
    _root,
    {},
    "_ext_constant_additional_land_compet_available_for_biofuels",
)


@component.add(
    name="Annual additional historic land use biofuels 2gen",
    units="MHa/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_additional_historic_product_biofuels_2gen": 1,
        "ej_per_ktoe": 1,
        "land_productivity_biofuels_2gen_ej_mha": 1,
    },
)
def annual_additional_historic_land_use_biofuels_2gen():
    return (
        annual_additional_historic_product_biofuels_2gen()
        * ej_per_ktoe()
        / land_productivity_biofuels_2gen_ej_mha()
    )


@component.add(
    name="Annual additional historic product biofuels 2gen",
    units="ktoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_produc_biofuels_2gen": 2},
)
def annual_additional_historic_product_biofuels_2gen():
    """
    Annual additional historic production of liquids from biofuels ethanol and biodiesel, ktoe/Year (1990-2015). Ref: BP 2016.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_produc_biofuels_2gen(integer(time() + 1))
        - historic_produc_biofuels_2gen(integer(time())),
        lambda: 0,
    )


@component.add(
    name="Annual shift from 2gen to 3gen",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_annual_shift_from_2gen_to_3gen"},
)
def annual_shift_from_2gen_to_3gen():
    """
    Share of the land dedicated for biofuels from the 2nd generation shifted to 3rd generation in the next year.
    """
    return _ext_constant_annual_shift_from_2gen_to_3gen()


_ext_constant_annual_shift_from_2gen_to_3gen = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "annual_shift_from_second_generation_to_third_generation",
    {},
    _root,
    {},
    "_ext_constant_annual_shift_from_2gen_to_3gen",
)


@component.add(
    name="Biofuels 3gen land compet available",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_land_compet_biofuels_2gen": 2, "land_compet_biofuels_3gen_mha": 1},
)
def biofuels_3gen_land_compet_available():
    """
    Remaining potential land available (dedicated to 2nd generation) as given as a fraction of unity. We assume that no new land starts directly to produce biofuels 3rd generation biofuels.
    """
    return (
        max_land_compet_biofuels_2gen() - land_compet_biofuels_3gen_mha()
    ) / max_land_compet_biofuels_2gen()


@component.add(
    name="Biofuels land compet available",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_land_compet_biofuels_2gen": 2,
        "land_compet_biofuels_2gen_mha": 1,
        "land_compet_biofuels_3gen_mha": 1,
    },
)
def biofuels_land_compet_available():
    """
    Remaining potential land available as given as a fraction of unity.
    """
    return (
        max_land_compet_biofuels_2gen()
        - land_compet_biofuels_2gen_mha()
        - land_compet_biofuels_3gen_mha()
    ) / max_land_compet_biofuels_2gen()


@component.add(
    name="Efficiency improvement biofuels 3gen",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_improvement_biofuels_3gen"},
)
def efficiency_improvement_biofuels_3gen():
    """
    Efficiency improvements of 3rd generation (cellulosic) in relation to 2nd generation biofuels.
    """
    return _ext_constant_efficiency_improvement_biofuels_3gen()


_ext_constant_efficiency_improvement_biofuels_3gen = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_improvement_biofuels_third_generation",
    {},
    _root,
    {},
    "_ext_constant_efficiency_improvement_biofuels_3gen",
)


@component.add(
    name="EJ per ktoe", units="EJ/ktoe", comp_type="Constant", comp_subtype="Normal"
)
def ej_per_ktoe():
    """
    1 ktoe = 0.000041868 EJ.
    """
    return 4.1868e-05


@component.add(
    name="Historic land compet available for biofuels 2gen",
    units="MHa/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ej_per_ktoe": 1, "land_productivity_biofuels_2gen_ej_mha": 1},
)
def historic_land_compet_available_for_biofuels_2gen():
    """
    Land occupied by biofuels in 2015. Biofuels production in 2015: 7,4847.7 ktoe (BP 2016).
    """
    return 74847.7 * ej_per_ktoe() / land_productivity_biofuels_2gen_ej_mha()


@component.add(
    name="Historic produc biofuels 2gen",
    units="ktoe/Year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_produc_biofuels_2gen",
        "__lookup__": "_ext_lookup_historic_produc_biofuels_2gen",
    },
)
def historic_produc_biofuels_2gen(x, final_subs=None):
    """
    Historic production of biofuels 2nd generation (1990-2015).
    """
    return _ext_lookup_historic_produc_biofuels_2gen(x, final_subs)


_ext_lookup_historic_produc_biofuels_2gen = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_production_of_second_generation_biofuels",
    {},
    _root,
    {},
    "_ext_lookup_historic_produc_biofuels_2gen",
)


@component.add(
    name="initial value land compet biofuels 2gen ktoe",
    units="EJ/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe"
    },
)
def initial_value_land_compet_biofuels_2gen_ktoe():
    """
    Initial value in 1995 derived from (BP 2016).
    """
    return _ext_constant_initial_value_land_compet_biofuels_2gen_ktoe()


_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "initial_production_of_second_generation_biofuels",
    {},
    _root,
    {},
    "_ext_constant_initial_value_land_compet_biofuels_2gen_ktoe",
)


@component.add(
    name="initial value land compet biofuels 2gen Mha",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_value_land_compet_biofuels_2gen_ktoe": 1, "ej_per_ktoe": 1},
)
def initial_value_land_compet_biofuels_2gen_mha():
    """
    Initial value of land occupation by biofuels of second generation.
    """
    return initial_value_land_compet_biofuels_2gen_ktoe() * ej_per_ktoe()


@component.add(
    name="land compet 2gen vs total land compet",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_biofuels_2gen_mha": 1,
        "land_compet_required_dedicated_crops_for_biofuels": 1,
    },
)
def land_compet_2gen_vs_total_land_compet():
    """
    Land dedicated to 2nd generation biofuels vs total land competition for biofuels [to prevent stock "Land compet biofuels 2gen Mha" goes negative].
    """
    return (
        land_compet_biofuels_2gen_mha()
        / land_compet_required_dedicated_crops_for_biofuels()
    )


@component.add(
    name="Land compet biofuels 2gen abandonned",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_compet_biofuels_2gen_mha": 1, "share_biofuels_overcapacity": 1},
)
def land_compet_biofuels_2gen_abandonned():
    """
    Land previously dedicated to produce biofuels 2nd generation and abandoned due to reduced liquids demand.
    """
    return land_compet_biofuels_2gen_mha() * share_biofuels_overcapacity()


@component.add(
    name="Land compet biofuels 2gen Mha",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_land_compet_biofuels_2gen_mha": 1},
    other_deps={
        "_integ_land_compet_biofuels_2gen_mha": {
            "initial": {
                "initial_value_land_compet_biofuels_2gen_mha": 1,
                "land_productivity_biofuels_2gen_ej_mha": 1,
            },
            "step": {
                "new_biofuels_2gen_land_compet": 1,
                "land_compet_biofuels_2gen_abandonned": 1,
                "land_shifted_to_biofuels_3gen": 1,
            },
        }
    },
)
def land_compet_biofuels_2gen_mha():
    """
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


@component.add(
    name="Land compet biofuels 3gen abandonned",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_compet_biofuels_3gen_mha": 1, "share_biofuels_overcapacity": 1},
)
def land_compet_biofuels_3gen_abandonned():
    """
    Land previously dedicated to produce biofuels 3rd generation and abandoned due to reduced liquids demand.
    """
    return land_compet_biofuels_3gen_mha() * share_biofuels_overcapacity()


@component.add(
    name="Land compet biofuels 3gen Mha",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_land_compet_biofuels_3gen_mha": 1},
    other_deps={
        "_integ_land_compet_biofuels_3gen_mha": {
            "initial": {},
            "step": {
                "land_shifted_to_biofuels_3gen": 1,
                "land_compet_biofuels_3gen_abandonned": 1,
            },
        }
    },
)
def land_compet_biofuels_3gen_mha():
    """
    Land subject to competition dedicated to biofuels 3rd generation as a shift of surface previously dedicated to biofuels from the 2nd generation.
    """
    return _integ_land_compet_biofuels_3gen_mha()


_integ_land_compet_biofuels_3gen_mha = Integ(
    lambda: land_shifted_to_biofuels_3gen() - land_compet_biofuels_3gen_abandonned(),
    lambda: 0,
    "_integ_land_compet_biofuels_3gen_mha",
)


@component.add(
    name="Land compet required dedicated crops for biofuels",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_compet_biofuels_2gen_mha": 1, "land_compet_biofuels_3gen_mha": 1},
)
def land_compet_required_dedicated_crops_for_biofuels():
    """
    Land requirements for crops for biofuels 2nd and 3rd generation (in land competing with other uses).
    """
    return land_compet_biofuels_2gen_mha() + land_compet_biofuels_3gen_mha()


@component.add(
    name="Land productivity biofuels 2gen EJ MHa",
    units="EJ/MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_land_productivity_biofuels_2gen_ej_mha"},
)
def land_productivity_biofuels_2gen_ej_mha():
    """
    Energy output per area of biofuels 2nd generation (final energy). Source: de Castro et al (2014): 0.155 W/m2.
    """
    return _ext_constant_land_productivity_biofuels_2gen_ej_mha()


_ext_constant_land_productivity_biofuels_2gen_ej_mha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "land_productivity_biofuels_second_generation",
    {},
    _root,
    {},
    "_ext_constant_land_productivity_biofuels_2gen_ej_mha",
)


@component.add(
    name="Land shifted to biofuels 3gen",
    units="MHa/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_year_3gen_cellulosic_biofuels": 2,
        "land_compet_biofuels_3gen_mha": 1,
        "annual_shift_from_2gen_to_3gen": 1,
        "land_compet_biofuels_2gen_mha": 1,
        "p_biofuels_3gen_land_compet": 1,
        "biofuels_3gen_land_compet_available": 2,
        "land_compet_2gen_vs_total_land_compet": 2,
    },
)
def land_shifted_to_biofuels_3gen():
    """
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


@component.add(
    name="Max land compet biofuels 2gen",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "additional_land_compet_available_for_biofuels": 1,
        "historic_land_compet_available_for_biofuels_2gen": 1,
    },
)
def max_land_compet_biofuels_2gen():
    """
    Annual potential of biofuels (final energy) 2nd generation competing with other land uses.
    """
    return (
        additional_land_compet_available_for_biofuels()
        + historic_land_compet_available_for_biofuels_2gen()
    )


@component.add(
    name="Max PEavail potential biofuels land compet",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_year_3gen_cellulosic_biofuels": 1,
        "land_productivity_biofuels_2gen_ej_mha": 2,
        "max_land_compet_biofuels_2gen": 2,
        "efficiency_improvement_biofuels_3gen": 1,
    },
)
def max_peavail_potential_biofuels_land_compet():
    """
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


@component.add(
    name="new biofuels 2gen land compet",
    units="MHa/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "check_liquids": 1,
        "constrain_liquids_exogenous_growth": 1,
        "land_compet_biofuels_2gen_mha": 2,
        "adapt_growth_biofuels_2gen": 1,
        "biofuels_land_compet_available": 1,
        "annual_additional_historic_land_use_biofuels_2gen": 1,
        "land_availability_constraint": 1,
    },
)
def new_biofuels_2gen_land_compet():
    """
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
        * land_availability_constraint()
    )


@component.add(
    name="P biofuels 2gen land compet",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_biofuels_2gen_land_compet"},
)
def p_biofuels_2gen_land_compet():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_biofuels_2gen_land_compet()


_ext_constant_p_biofuels_2gen_land_compet = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_biofuels_2gen_land_compet",
    {},
    _root,
    {},
    "_ext_constant_p_biofuels_2gen_land_compet",
)


@component.add(
    name="P biofuels 3gen land compet",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_biofuels_3gen_land_compet"},
)
def p_biofuels_3gen_land_compet():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_biofuels_3gen_land_compet()


_ext_constant_p_biofuels_3gen_land_compet = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_biofuels_3gen_land_compet",
    {},
    _root,
    {},
    "_ext_constant_p_biofuels_3gen_land_compet",
)


@component.add(
    name="past biofuels 2gen",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_past_biofuels_2gen"},
)
def past_biofuels_2gen():
    """
    Current growth patterns (1990-2015).
    """
    return _ext_constant_past_biofuels_2gen()


_ext_constant_past_biofuels_2gen = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "historic_growth_biofuels_second_generation",
    {},
    _root,
    {},
    "_ext_constant_past_biofuels_2gen",
)


@component.add(
    name='"PE biofuels prod 2gen+3gen EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peavail_biofuels_2gen_land_compet_ej": 1,
        "peavail_biofuels_3gen_land_compet_ej": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def pe_biofuels_prod_2gen3gen_ej():
    """
    Total annual primary energy biomass for biofuel production (2nd and 3rd generation) in marginal lands.
    """
    return (
        peavail_biofuels_2gen_land_compet_ej() + peavail_biofuels_3gen_land_compet_ej()
    ) / conv_efficiency_from_npp_to_biofuels()


@component.add(
    name="PEavail biofuels 2gen land compet EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_2gen_land_compet_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def peavail_biofuels_2gen_land_compet_ej():
    """
    Primary energy available of biofuels from dedicated crops (2nd generation).
    """
    return potential_peavail_biofuels_2gen_land_compet_ej() * (
        1 - share_biofuels_overcapacity()
    )


@component.add(
    name="PEavail biofuels 3gen land compet EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_prod_3gen_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def peavail_biofuels_3gen_land_compet_ej():
    """
    Primary energy available of biofuels from dedicated crops (3rd generation).
    """
    return potential_peavail_biofuels_prod_3gen_ej() * (
        1 - share_biofuels_overcapacity()
    )


@component.add(
    name="PEavail tot biofuels land compet EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peavail_biofuels_2gen_land_compet_ej": 1,
        "peavail_biofuels_3gen_land_compet_ej": 1,
    },
)
def peavail_tot_biofuels_land_compet_ej():
    """
    Primary energy available of biofuels from dedicated crops -in land competition- (2nd and 3rd generation).
    """
    return (
        peavail_biofuels_2gen_land_compet_ej() + peavail_biofuels_3gen_land_compet_ej()
    )


@component.add(
    name="Potential PEavail biofuels 2gen land compet EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_biofuels_2gen_mha": 1,
        "land_productivity_biofuels_2gen_ej_mha": 1,
    },
)
def potential_peavail_biofuels_2gen_land_compet_ej():
    """
    Potential primary energy available of biofuels from dedicated crops (2nd generation).
    """
    return land_compet_biofuels_2gen_mha() * land_productivity_biofuels_2gen_ej_mha()


@component.add(
    name="Potential PEavail biofuels prod 3gen EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_biofuels_3gen_mha": 1,
        "land_productivity_biofuels_2gen_ej_mha": 1,
        "efficiency_improvement_biofuels_3gen": 1,
    },
)
def potential_peavail_biofuels_prod_3gen_ej():
    """
    Potential Final Energy production (EJ) of biofuels from dedicated crops (3rd generation).
    """
    return (
        land_compet_biofuels_3gen_mha()
        * land_productivity_biofuels_2gen_ej_mha()
        * (1 + efficiency_improvement_biofuels_3gen())
    )


@component.add(
    name="remaining potential biofuels land compet",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_peavail_potential_biofuels_land_compet": 3,
        "peavail_tot_biofuels_land_compet_ej": 2,
    },
)
def remaining_potential_biofuels_land_compet():
    """
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


@component.add(
    name="start year 3gen cellulosic biofuels",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_3gen_cellulosic_biofuels"},
)
def start_year_3gen_cellulosic_biofuels():
    """
    First year when 3rd generation biofuels are available.
    """
    return _ext_constant_start_year_3gen_cellulosic_biofuels()


_ext_constant_start_year_3gen_cellulosic_biofuels = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_year_3gen_cell_biofuels",
    {},
    _root,
    {},
    "_ext_constant_start_year_3gen_cellulosic_biofuels",
)
