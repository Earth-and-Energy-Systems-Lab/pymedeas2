"""
Module energy.supply.crops_for_biofuels
Translated using PySD version 3.14.2
"""

@component.add(
    name="BioE_gen_land_marg_available",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_peavail_potential_biofuels_marginal_lands": 2,
        "potential_peavail_biofuels_land_marg_ej": 1,
    },
)
def bioe_gen_land_marg_available():
    """
    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        max_peavail_potential_biofuels_marginal_lands()
        - potential_peavail_biofuels_land_marg_ej(),
        max_peavail_potential_biofuels_marginal_lands(),
    )


@component.add(
    name="BioE_potential_NPP_marginal_lands",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_marginal_lands_mha": 1,
        "land_productivity_biofuels_marg_ej_mha": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def bioe_potential_npp_marginal_lands():
    """
    Potential in marginal lands, i.e. witout competition with current uses. (Field et al., 2008) find that 27 EJ of NPP can be extracted from 386 Mha of marginal lands. We assume that all the production from marginal lands is used for producing liquids.
    """
    return (
        potential_marginal_lands_mha()
        * land_productivity_biofuels_marg_ej_mha()
        / conv_efficiency_from_npp_to_biofuels()
    )


@component.add(
    name="Conv_efficiency_from_NPP_to_biofuels",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_conv_efficiency_from_npp_to_biofuels"},
)
def conv_efficiency_from_npp_to_biofuels():
    """
    Conversion efficiency from net primary productivity (NPP) of biomass to biofuels of 15%. Ref: de Castro & Carpintero (2014).
    """
    return _ext_constant_conv_efficiency_from_npp_to_biofuels()


_ext_constant_conv_efficiency_from_npp_to_biofuels = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "conv_efficiency_from_npp_to_biofuels",
    {},
    _root,
    {},
    "_ext_constant_conv_efficiency_from_npp_to_biofuels",
)


@component.add(
    name="Land_occupation_ratio_biofuels_marg_land",
    units="MHa/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_land_occupation_ratio_biofuels_marg_land"
    },
)
def land_occupation_ratio_biofuels_marg_land():
    """
    Field et al. (2008) found that 27 EJ of NPP can be extracted from 386 MHa of marginal lands. So, the land occupation ratio would be 386 MHa/27 EJ, i.e. 14.3 MHa/EJ NPP.
    """
    return _ext_constant_land_occupation_ratio_biofuels_marg_land()


_ext_constant_land_occupation_ratio_biofuels_marg_land = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "land_occupation_ratio_biofuels_marginal_land",
    {},
    _root,
    {},
    "_ext_constant_land_occupation_ratio_biofuels_marg_land",
)


@component.add(
    name="Land_productivity_biofuels_marg_EJ_MHa",
    units="EJ/(year*MHa)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_land_productivity_biofuels_marg_ej_mha"},
)
def land_productivity_biofuels_marg_ej_mha():
    """
    Energy output per area of biofuels in marginal lands (final energy). Source: Field et al (2008): 27 EJ (NPP) at 15% efficiency in 386 MHa.
    """
    return _ext_constant_land_productivity_biofuels_marg_ej_mha()


_ext_constant_land_productivity_biofuels_marg_ej_mha = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "land_productivity_biofuels_marginal_land",
    {},
    _root,
    {},
    "_ext_constant_land_productivity_biofuels_marg_ej_mha",
)


@component.add(
    name="Land_required_biofuels_land_marg",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_land_marg_ej": 1,
        "land_occupation_ratio_biofuels_marg_land": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def land_required_biofuels_land_marg():
    """
    Marginal lands occupied by biofuels.
    """
    return (
        potential_peavail_biofuels_land_marg_ej()
        * land_occupation_ratio_biofuels_marg_land()
        / conv_efficiency_from_npp_to_biofuels()
    )


@component.add(
    name="Max_PEavail_potential_biofuels_marginal_lands",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bioe_potential_npp_marginal_lands": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def max_peavail_potential_biofuels_marginal_lands():
    """
    Annual biofuels potential (primary energy) available from marginal lands
    """
    return bioe_potential_npp_marginal_lands() * conv_efficiency_from_npp_to_biofuels()


@component.add(
    name="new_biofuels_land_marg",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "start_year_biofuels_land_marg": 3,
        "start_production_biofuels": 1,
        "ej_per_ktoe": 1,
        "potential_marginal_lands_mha": 1,
        "bioe_gen_land_marg_available": 1,
        "check_liquids": 1,
        "constrain_liquids_exogenous_growth": 1,
        "p_biofuels_marg_lands": 1,
        "nvs_1_year": 2,
        "ratio_land_productivity_2gen_vs_marg": 1,
        "potential_peavail_biofuels_land_marg_ej": 2,
        "land_availability_constraint": 1,
    },
)
def new_biofuels_land_marg():
    """
    New annual production from biofuels in marginal lands. For the first 5 years, we assume the same rate of land occupation (MHa/year) than the one achieved by conventional biofuels -this is the reason to take into account the relative land productivity between both types of crops.
    """
    return (
        if_then_else(
            time() < start_year_biofuels_land_marg(),
            lambda: 0,
            lambda: if_then_else(
                potential_marginal_lands_mha() == 0,
                lambda: 0,
                lambda: if_then_else(
                    time() < start_year_biofuels_land_marg() + 5,
                    lambda: start_production_biofuels(
                        time() - start_year_biofuels_land_marg()
                    )
                    / nvs_1_year()
                    * ej_per_ktoe()
                    / ratio_land_productivity_2gen_vs_marg(),
                    lambda: if_then_else(
                        check_liquids() < 0,
                        lambda: constrain_liquids_exogenous_growth()
                        * potential_peavail_biofuels_land_marg_ej()
                        / nvs_1_year(),
                        lambda: p_biofuels_marg_lands()
                        * bioe_gen_land_marg_available()
                        * potential_peavail_biofuels_land_marg_ej(),
                    ),
                ),
            ),
        )
        * land_availability_constraint()
    )


@component.add(
    name="new_land_marg_for_biofuels",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_biofuels_land_marg": 1,
        "land_occupation_ratio_biofuels_marg_land": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
        "nvs_1_year": 1,
    },
)
def new_land_marg_for_biofuels():
    return (
        new_biofuels_land_marg()
        * land_occupation_ratio_biofuels_marg_land()
        / conv_efficiency_from_npp_to_biofuels()
        * nvs_1_year()
    )


@component.add(
    name="P_biofuels_marg_lands",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_biofuels_marg_lands"},
)
def p_biofuels_marg_lands():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_biofuels_marg_lands()


_ext_constant_p_biofuels_marg_lands = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "p_biofuels_land_marg_growth",
    {},
    _root,
    {},
    "_ext_constant_p_biofuels_marg_lands",
)


@component.add(
    name="PE_biofuels_land_marg_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peavail_biofuels_land_marg_ej": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def pe_biofuels_land_marg_ej():
    """
    Total annual primary energy biomass for biofuel production in marginal lands.
    """
    return peavail_biofuels_land_marg_ej() / conv_efficiency_from_npp_to_biofuels()


@component.add(
    name="PEavail_biofuels_land_marg_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_land_marg_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def peavail_biofuels_land_marg_ej():
    """
    Total annual biofuel production in marginal lands.
    """
    return potential_peavail_biofuels_land_marg_ej() * (
        1 - share_biofuels_overcapacity()
    )


@component.add(
    name="Potential_marginal_lands_MHa",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_potential_marginal_lands_mha"},
)
def potential_marginal_lands_mha():
    """
    Global marginal lands as estimated by Field et al (2008).
    """
    return _ext_constant_potential_marginal_lands_mha()


_ext_constant_potential_marginal_lands_mha = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "pot_marg_land_biofuels",
    {},
    _root,
    {},
    "_ext_constant_potential_marginal_lands_mha",
)


@component.add(
    name="Potential_PEavail_biofuels_land_marg_abandonned",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_land_marg_ej": 1,
        "share_biofuels_overcapacity": 1,
        "nvs_1_year": 1,
    },
)
def potential_peavail_biofuels_land_marg_abandonned():
    return (
        potential_peavail_biofuels_land_marg_ej()
        * share_biofuels_overcapacity()
        / nvs_1_year()
    )


@component.add(
    name="Potential_PEavail_biofuels_land_marg_EJ",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_peavail_biofuels_land_marg_ej": 1},
    other_deps={
        "_integ_potential_peavail_biofuels_land_marg_ej": {
            "initial": {},
            "step": {
                "new_biofuels_land_marg": 1,
                "potential_peavail_biofuels_land_marg_abandonned": 1,
            },
        }
    },
)
def potential_peavail_biofuels_land_marg_ej():
    """
    Potential total annual biofuel production in marginal lands.
    """
    return _integ_potential_peavail_biofuels_land_marg_ej()


_integ_potential_peavail_biofuels_land_marg_ej = Integ(
    lambda: new_biofuels_land_marg()
    - potential_peavail_biofuels_land_marg_abandonned(),
    lambda: 0,
    "_integ_potential_peavail_biofuels_land_marg_ej",
)


@component.add(
    name="ratio_land_productivity_2gen_vs_marg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_productivity_biofuels_2gen_ej_mha": 1,
        "land_productivity_biofuels_marg_ej_mha": 1,
    },
)
def ratio_land_productivity_2gen_vs_marg():
    """
    Ratio between the land productivity of biofuels 2gen in competition land vs marginal lands.
    """
    return (
        land_productivity_biofuels_2gen_ej_mha()
        / land_productivity_biofuels_marg_ej_mha()
    )


@component.add(
    name="remaining_potential_biofuels_land_marg",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_peavail_potential_biofuels_marginal_lands": 3,
        "peavail_biofuels_land_marg_ej": 2,
    },
)
def remaining_potential_biofuels_land_marg():
    """
    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_peavail_potential_biofuels_marginal_lands()
        > peavail_biofuels_land_marg_ej(),
        lambda: (
            max_peavail_potential_biofuels_marginal_lands()
            - peavail_biofuels_land_marg_ej()
        )
        / max_peavail_potential_biofuels_marginal_lands(),
        lambda: 0,
    )


@component.add(
    name="start_production_biofuels",
    units="ktoe/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_start_production_biofuels",
        "__lookup__": "_ext_lookup_start_production_biofuels",
    },
)
def start_production_biofuels(x, final_subs=None):
    """
    Exogenous start production scenario from the year "start year biofuels land marg". It mimics the biofuel 2nd generation deployment from the year 2000.
    """
    return _ext_lookup_start_production_biofuels(x, final_subs)


_ext_lookup_start_production_biofuels = ExtLookup(
    r"../energy.xlsx",
    "Catalonia",
    "delta_years",
    "start_production_biofuels",
    {},
    _root,
    {},
    "_ext_lookup_start_production_biofuels",
)


@component.add(
    name="start_year_biofuels_land_marg",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_biofuels_land_marg"},
)
def start_year_biofuels_land_marg():
    """
    First year when the technology "biofuels land marg" is available.
    """
    return _ext_constant_start_year_biofuels_land_marg()


_ext_constant_start_year_biofuels_land_marg = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_biofuels_land_marg",
    {},
    _root,
    {},
    "_ext_constant_start_year_biofuels_land_marg",
)
