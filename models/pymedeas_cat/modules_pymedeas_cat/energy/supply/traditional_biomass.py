"""
Module traditional_biomass
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="modern solids BioE demand households",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "pe_traditional_biomass_demand_ej": 1,
    },
)
def modern_solids_bioe_demand_households():
    """
    Demand of modern solids bioenergy in households.
    """
    return (
        float(households_final_energy_demand().loc["solids"])
        - pe_traditional_biomass_demand_ej()
    )


@component.add(
    name="PE consumption trad biomass ref",
    units="EJ/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pe_consumption_trad_biomass_ref"},
)
def pe_consumption_trad_biomass_ref():
    """
    Primary energy consumption of trad biomass. From IEA balances, 39.626 EJ were consumed as primary solids biofuels for TFC in 2008.
    """
    return _ext_constant_pe_consumption_trad_biomass_ref()


_ext_constant_pe_consumption_trad_biomass_ref = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "pe_consumption_trad_biomass_ref",
    {},
    _root,
    {},
    "_ext_constant_pe_consumption_trad_biomass_ref",
)


@component.add(
    name="PE traditional biomass consum EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"consum_forest_energy_traditional_ej": 1},
)
def pe_traditional_biomass_consum_ej():
    """
    Annual primary energy consumption of traditional biomass. It also includes charcoal and biosolids for solids. It's limited by the maximum given by the stock of forests MAX(max E forest traditional EJ,Households final energy demand[solids]*share trad biomass vs solids in households)
    """
    return consum_forest_energy_traditional_ej()


@component.add(
    name="PE traditional biomass demand EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "share_trad_biomass_vs_solids_in_households": 1,
    },
)
def pe_traditional_biomass_demand_ej():
    """
    Annual primary energy demand of traditional biomass driven by population and energy intensity evolution. It also includes charcoal and biosolids for solids.
    """
    return (
        float(households_final_energy_demand().loc["solids"])
        * share_trad_biomass_vs_solids_in_households()
    )


@component.add(
    name="PE traditional biomass EJ delayed 1yr",
    units="EJ/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_pe_traditional_biomass_ej_delayed_1yr": 1},
    other_deps={
        "_delayfixed_pe_traditional_biomass_ej_delayed_1yr": {
            "initial": {"time_step": 1},
            "step": {"pe_traditional_biomass_consum_ej": 1},
        }
    },
)
def pe_traditional_biomass_ej_delayed_1yr():
    """
    Annual primary energy consumption of traditional biomass. It also includes charcoal and biosolids for solids.
    """
    return _delayfixed_pe_traditional_biomass_ej_delayed_1yr()


_delayfixed_pe_traditional_biomass_ej_delayed_1yr = DelayFixed(
    lambda: pe_traditional_biomass_consum_ej(),
    lambda: time_step(),
    lambda: 0,
    time_step,
    "_delayfixed_pe_traditional_biomass_ej_delayed_1yr",
)


@component.add(
    name="People relying trad biomass ref",
    units="people",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_people_relying_trad_biomass_ref"},
)
def people_relying_trad_biomass_ref():
    """
    People relying on traditional biomass in 2008. WEO 2010 reportad that in 2008, 2.5 billion people consumed 724 Mtoe of traditional biomass.
    """
    return _ext_constant_people_relying_trad_biomass_ref()


_ext_constant_people_relying_trad_biomass_ref = ExtConstant(
    "../parameters.xlsx",
    "Austria",
    "people_relying_on_traditional_biomass",
    {},
    _root,
    {},
    "_ext_constant_people_relying_trad_biomass_ref",
)


@component.add(
    name="PEpc consumption people depending on trad biomass",
    units="MToe/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_consumption_trad_biomass_ref": 1,
        "people_relying_trad_biomass_ref": 1,
    },
)
def pepc_consumption_people_depending_on_trad_biomass():
    """
    Primary energy per capita consumption of people currently depending on trad biomass.
    """
    return zidz(pe_consumption_trad_biomass_ref(), people_relying_trad_biomass_ref())


@component.add(
    name="Population dependent on trad biomass",
    units="people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_traditional_biomass_consum_ej": 1,
        "pepc_consumption_people_depending_on_trad_biomass": 1,
    },
)
def population_dependent_on_trad_biomass():
    """
    Population dependent on traditional biomass.
    """
    return zidz(
        pe_traditional_biomass_consum_ej(),
        pepc_consumption_people_depending_on_trad_biomass(),
    )


@component.add(
    name="share global pop dependent on trad biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_dependent_on_trad_biomass": 1, "population": 1},
)
def share_global_pop_dependent_on_trad_biomass():
    return population_dependent_on_trad_biomass() / population()


@component.add(
    name="share trad biomass vs solids in households",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_trad_biomass_vs_solids_in_households"
    },
)
def share_trad_biomass_vs_solids_in_households():
    return _ext_constant_share_trad_biomass_vs_solids_in_households()


_ext_constant_share_trad_biomass_vs_solids_in_households = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_trad_biomass_vs_solids_in_households",
    {},
    _root,
    {},
    "_ext_constant_share_trad_biomass_vs_solids_in_households",
)
