"""
Module traditional_biomass
Translated using PySD version 2.2.1
"""


def modern_solids_bioe_demand_households():
    """
    Real Name: modern solids BioE demand households
    Original Eqn: Households final energy demand[solids]-PE traditional biomass demand EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of modern solids bioenergy in households.
    """
    return (
        float(households_final_energy_demand().loc["solids"])
        - pe_traditional_biomass_demand_ej()
    )


def pe_consumption_trad_biomass_ref():
    """
    Real Name: PE consumption trad biomass ref
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'pe_consumption_trad_biomass_ref')
    Units: EJ/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Primary energy consumption of trad biomass. From IEA balances, 39.626 EJ
        were consumed as primary solids biofuels for TFC in 2008.
    """
    return _ext_constant_pe_consumption_trad_biomass_ref()


def pe_traditional_biomass_consum_ej():
    """
    Real Name: PE traditional biomass consum EJ
    Original Eqn: consum forest energy traditional EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy consumption of traditional biomass. It also includes charcoal
        and biosolids for solids.        It's limited by the maximum given by the stock of forests  MAX(max E
        forest traditional EJ,Households final energy demand[solids]*share trad
        biomass vs solids in households)
    """
    return consum_forest_energy_traditional_ej()


def pe_traditional_biomass_demand_ej():
    """
    Real Name: PE traditional biomass demand EJ
    Original Eqn: Households final energy demand[solids]*share trad biomass vs solids in households
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy demand of traditional biomass driven by population
        and energy intensity evolution. It also includes charcoal and biosolids
        for solids.
    """
    return (
        float(households_final_energy_demand().loc["solids"])
        * share_trad_biomass_vs_solids_in_households()
    )


def pe_traditional_biomass_ej_delayed_1yr():
    """
    Real Name: PE traditional biomass EJ delayed 1yr
    Original Eqn: DELAY FIXED(PE traditional biomass consum EJ, TIME STEP, 0)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy consumption of traditional biomass. It also includes
        charcoal and biosolids for solids.
    """
    return _delayfixed_pe_traditional_biomass_ej_delayed_1yr()


def people_relying_trad_biomass_ref():
    """
    Real Name: People relying trad biomass ref
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Europe', 'people_relying_on_traditional_biomass')
    Units: people
    Limits: (None, None)
    Type: constant
    Subs: None

    People relying on traditional biomass in 2008. WEO 2010 reportad that in
        2008, 2.5 billion people consumed 724 Mtoe of traditional biomass.
    """
    return _ext_constant_people_relying_trad_biomass_ref()


def pepc_consumption_people_depending_on_trad_biomass():
    """
    Real Name: PEpc consumption people depending on trad biomass
    Original Eqn: ZIDZ( PE consumption trad biomass ref, People relying trad biomass ref )
    Units: MToe/people
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy per capita consumption of people currently depending on
        trad biomass.
    """
    return zidz(pe_consumption_trad_biomass_ref(), people_relying_trad_biomass_ref())


def population_dependent_on_trad_biomass():
    """
    Real Name: Population dependent on trad biomass
    Original Eqn: ZIDZ( PE traditional biomass consum EJ, PEpc consumption people depending on trad biomass)
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Population dependent on traditional biomass.
    """
    return zidz(
        pe_traditional_biomass_consum_ej(),
        pepc_consumption_people_depending_on_trad_biomass(),
    )


def share_global_pop_dependent_on_trad_biomass():
    """
    Real Name: share global pop dependent on trad biomass
    Original Eqn: Population dependent on trad biomass/Population
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return population_dependent_on_trad_biomass() / population()


def share_trad_biomass_vs_solids_in_households():
    """
    Real Name: share trad biomass vs solids in households
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_trad_biomass_vs_solids_in_households')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_share_trad_biomass_vs_solids_in_households()


_ext_constant_pe_consumption_trad_biomass_ref = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "pe_consumption_trad_biomass_ref",
    {},
    _root,
    "_ext_constant_pe_consumption_trad_biomass_ref",
)


_delayfixed_pe_traditional_biomass_ej_delayed_1yr = DelayFixed(
    lambda: pe_traditional_biomass_consum_ej(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_pe_traditional_biomass_ej_delayed_1yr",
)


_ext_constant_people_relying_trad_biomass_ref = ExtConstant(
    "../parameters.xlsx",
    "Europe",
    "people_relying_on_traditional_biomass",
    {},
    _root,
    "_ext_constant_people_relying_trad_biomass_ref",
)


_ext_constant_share_trad_biomass_vs_solids_in_households = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_trad_biomass_vs_solids_in_households",
    {},
    _root,
    "_ext_constant_share_trad_biomass_vs_solids_in_households",
)
