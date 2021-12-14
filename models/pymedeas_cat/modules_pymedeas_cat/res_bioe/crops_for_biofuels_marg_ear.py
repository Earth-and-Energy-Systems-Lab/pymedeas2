"""
Module crops_for_biofuels_marg_ear
Translated using PySD version 2.1.0
"""


def bioe_gen_land_marg_available():
    """
    Real Name: BioE gen land marg available
    Original Eqn: ZIDZ( (Max PEavail potential biofuels marginal lands-Potential PEavail biofuels land marg EJ), Max PEavail potential biofuels marginal lands)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        (
            max_peavail_potential_biofuels_marginal_lands()
            - potential_peavail_biofuels_land_marg_ej()
        ),
        max_peavail_potential_biofuels_marginal_lands(),
    )


def bioe_potential_npp_marginal_lands():
    """
    Real Name: BioE potential NPP marginal lands
    Original Eqn: Potential marginal lands MHa*Land productivity biofuels marg EJ MHa/Conv efficiency from NPP to biofuels
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential in marginal lands, i.e. witout competition with current uses.
        (Field et al., 2008) find that 27 EJ of NPP can be extracted from 386 Mha
        of marginal lands. We assume that all the production from marginal lands
        is used for producing liquids.
    """
    return (
        potential_marginal_lands_mha()
        * land_productivity_biofuels_marg_ej_mha()
        / conv_efficiency_from_npp_to_biofuels()
    )


def conv_efficiency_from_npp_to_biofuels():
    """
    Real Name: Conv efficiency from NPP to biofuels
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'conv_efficiency_from_npp_to_biofuels')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion efficiency from net primary productivity (NPP) of biomass to
        biofuels of 15%. Ref: de Castro & Carpintero (2014).
    """
    return _ext_constant_conv_efficiency_from_npp_to_biofuels()


def land_occupation_ratio_biofuels_marg_land():
    """
    Real Name: Land occupation ratio biofuels marg land
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'land_occupation_ratio_biofuels_marginal_land')
    Units: MHa/EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Field et al. (2008) found that 27 EJ of NPP can be extracted from 386 MHa
        of marginal lands. So, the land occupation ratio would be 386 MHa/27 EJ,
        i.e. 14.3 MHa/EJ NPP.
    """
    return _ext_constant_land_occupation_ratio_biofuels_marg_land()


def land_productivity_biofuels_marg_ej_mha():
    """
    Real Name: Land productivity biofuels marg EJ MHa
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'land_productivity_biofuels_marginal_land')
    Units: EJ/MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Energy output per area of biofuels in marginal lands (final energy).
        Source: Field et al (2008): 27 EJ (NPP) at 15% efficiency in 386 MHa.
    """
    return _ext_constant_land_productivity_biofuels_marg_ej_mha()


def land_required_biofuels_land_marg():
    """
    Real Name: Land required biofuels land marg
    Original Eqn: Potential PEavail biofuels land marg EJ*Land occupation ratio biofuels marg land/Conv efficiency from NPP to biofuels
    Units: MHa/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Marginal lands occupied by biofuels.
    """
    return (
        potential_peavail_biofuels_land_marg_ej()
        * land_occupation_ratio_biofuels_marg_land()
        / conv_efficiency_from_npp_to_biofuels()
    )


def max_peavail_potential_biofuels_marginal_lands():
    """
    Real Name: Max PEavail potential biofuels marginal lands
    Original Eqn: BioE potential NPP marginal lands*Conv efficiency from NPP to biofuels
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Annual biofuels potential (primary energy) available from marginal lands
    """
    return bioe_potential_npp_marginal_lands() * conv_efficiency_from_npp_to_biofuels()


def new_biofuels_land_marg():
    """
    Real Name: new biofuels land marg
    Original Eqn: IF THEN ELSE(Time<start year biofuels land marg, 0, IF THEN ELSE(Potential marginal lands MHa=0, 0, IF THEN ELSE(Time<start year biofuels land marg+5, start production biofuels(Time-start year biofuels land marg )*EJ per ktoe/ratio land productivity 2gen vs marg, IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?" *Potential PEavail biofuels land marg EJ ,P biofuels marg lands*BioE gen land marg available*Potential PEavail biofuels land marg EJ ))))*Land availability constraint
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual production from biofuels in marginal lands. For the first 5
        years, we assume the same rate of land occupation (MHa/year) than the one
        achieved by conventional biofuels -this is the reason to take into account
        the relative land productivity between both types of crops.
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
                    * ej_per_ktoe()
                    / ratio_land_productivity_2gen_vs_marg(),
                    lambda: if_then_else(
                        check_liquids() < 0,
                        lambda: constrain_liquids_exogenous_growth()
                        * potential_peavail_biofuels_land_marg_ej(),
                        lambda: p_biofuels_marg_lands()
                        * bioe_gen_land_marg_available()
                        * potential_peavail_biofuels_land_marg_ej(),
                    ),
                ),
            ),
        )
        * land_availability_constraint()
    )


def new_land_marg_for_biofuels():
    """
    Real Name: new land marg for biofuels
    Original Eqn: new biofuels land marg*Land occupation ratio biofuels marg land/Conv efficiency from NPP to biofuels
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        new_biofuels_land_marg()
        * land_occupation_ratio_biofuels_marg_land()
        / conv_efficiency_from_npp_to_biofuels()
    )


def p_biofuels_marg_lands():
    """
    Real Name: P biofuels marg lands
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'F46')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_biofuels_marg_lands()


def pe_biofuels_land_marg_ej():
    """
    Real Name: PE biofuels land marg EJ
    Original Eqn: PEavail biofuels land marg EJ/Conv efficiency from NPP to biofuels
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual primary energy biomass for biofuel production in marginal
        lands.
    """
    return peavail_biofuels_land_marg_ej() / conv_efficiency_from_npp_to_biofuels()


def peavail_biofuels_land_marg_ej():
    """
    Real Name: PEavail biofuels land marg EJ
    Original Eqn: Potential PEavail biofuels land marg EJ*(1-share biofuels overcapacity )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual biofuel production in marginal lands.
    """
    return potential_peavail_biofuels_land_marg_ej() * (
        1 - share_biofuels_overcapacity()
    )


def potential_marginal_lands_mha():
    """
    Real Name: Potential marginal lands MHa
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C43')
    Units: MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Global marginal lands as estimated by Field et al (2008).
    """
    return _ext_constant_potential_marginal_lands_mha()


def potential_peavail_biofuels_land_marg_abandonned():
    """
    Real Name: Potential PEavail biofuels land marg abandonned
    Original Eqn: Potential PEavail biofuels land marg EJ*share biofuels overcapacity
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return potential_peavail_biofuels_land_marg_ej() * share_biofuels_overcapacity()


def potential_peavail_biofuels_land_marg_ej():
    """
    Real Name: Potential PEavail biofuels land marg EJ
    Original Eqn: INTEG ( new biofuels land marg-Potential PEavail biofuels land marg abandonned , 0)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential total annual biofuel production in marginal lands.
    """
    return _integ_potential_peavail_biofuels_land_marg_ej()


def ratio_land_productivity_2gen_vs_marg():
    """
    Real Name: ratio land productivity 2gen vs marg
    Original Eqn: Land productivity biofuels 2gen EJ MHa/Land productivity biofuels marg EJ MHa
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio between the land productivity of biofuels 2gen in competition land
        vs marginal lands.
    """
    return (
        land_productivity_biofuels_2gen_ej_mha()
        / land_productivity_biofuels_marg_ej_mha()
    )


def remaining_potential_biofuels_land_marg():
    """
    Real Name: remaining potential biofuels land marg
    Original Eqn: IF THEN ELSE(Max PEavail potential biofuels marginal lands > PEavail biofuels land marg EJ, (Max PEavail potential biofuels marginal lands-PEavail biofuels land marg EJ)/Max PEavail potential biofuels marginal lands, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

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


def start_production_biofuels(x):
    """
    Real Name: start production biofuels
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'delta_years', 'start_production_biofuels')
    Units: ktoe/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Exogenous start production scenario from the year "start year biofuels
        land marg". It mimics the biofuel 2nd generation deployment from the year
        2000.
    """
    return _ext_lookup_start_production_biofuels(x)


def start_year_biofuels_land_marg():
    """
    Real Name: start year biofuels land marg
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'F45')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    First year when the technology "biofuels land marg" is available.
    """
    return _ext_constant_start_year_biofuels_land_marg()


_ext_constant_conv_efficiency_from_npp_to_biofuels = ExtConstant(
    "../energy.xlsx",
    "Global",
    "conv_efficiency_from_npp_to_biofuels",
    {},
    _root,
    "_ext_constant_conv_efficiency_from_npp_to_biofuels",
)


_ext_constant_land_occupation_ratio_biofuels_marg_land = ExtConstant(
    "../energy.xlsx",
    "Global",
    "land_occupation_ratio_biofuels_marginal_land",
    {},
    _root,
    "_ext_constant_land_occupation_ratio_biofuels_marg_land",
)


_ext_constant_land_productivity_biofuels_marg_ej_mha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "land_productivity_biofuels_marginal_land",
    {},
    _root,
    "_ext_constant_land_productivity_biofuels_marg_ej_mha",
)


_ext_constant_p_biofuels_marg_lands = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "F46",
    {},
    _root,
    "_ext_constant_p_biofuels_marg_lands",
)


_ext_constant_potential_marginal_lands_mha = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C43",
    {},
    _root,
    "_ext_constant_potential_marginal_lands_mha",
)


_integ_potential_peavail_biofuels_land_marg_ej = Integ(
    lambda: new_biofuels_land_marg()
    - potential_peavail_biofuels_land_marg_abandonned(),
    lambda: 0,
    "_integ_potential_peavail_biofuels_land_marg_ej",
)


_ext_lookup_start_production_biofuels = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "delta_years",
    "start_production_biofuels",
    {},
    _root,
    "_ext_lookup_start_production_biofuels",
)


_ext_constant_start_year_biofuels_land_marg = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "F45",
    {},
    _root,
    "_ext_constant_start_year_biofuels_land_marg",
)
