"""
Module energysupplytraditional_biomass
Translated using PySD version 3.14.0
"""

@component.add(
    name="modern BioE in households",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "pe_traditional_biomass_consum_ej": 1,
    },
)
def modern_bioe_in_households():
    return (
        float(households_final_energy_demand().loc["solids"])
        - pe_traditional_biomass_consum_ej()
    )


@component.add(
    name="PE consumption trad biomass ref",
    units="EJ/year",
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
    "World",
    "pe_consumption_trad_biomass_ref",
    {},
    _root,
    {},
    "_ext_constant_pe_consumption_trad_biomass_ref",
)


@component.add(
    name="PE traditional biomass consum EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_traditional_biomass_demand_ej": 1},
)
def pe_traditional_biomass_consum_ej():
    """
    Annual primary energy consumption of traditional biomass. It also includes charcoal and biosolids for solids. It's limited by the maximum given by the stock of forests MAX(max E forest traditional EJ,Households final energy demand[solids]*share trad biomass vs solids in households)
    """
    return pe_traditional_biomass_demand_ej()


@component.add(
    name="PE traditional biomass demand EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_final_energy_demand": 1, "share_trad_biomass": 1},
)
def pe_traditional_biomass_demand_ej():
    """
    Annual primary energy demand of traditional biomass driven by population and energy intensity evolution. It also includes charcoal and biosolids for solids.
    """
    return float(households_final_energy_demand().loc["solids"]) * share_trad_biomass()


@component.add(
    name="PE traditional biomass EJ delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_pe_traditional_biomass_ej_delayed": 1},
    other_deps={
        "_delayfixed_pe_traditional_biomass_ej_delayed": {
            "initial": {"time_step": 1},
            "step": {"pe_traditional_biomass_consum_ej": 1},
        }
    },
)
def pe_traditional_biomass_ej_delayed():
    """
    *Annual primary energy consumption of traditional biomass. It also includes charcoal and biosolids for solids. *Original name: PE traditional biomass EJ delayed 1yr *PE traditional biomass consum EJ, 1, 30
    """
    return _delayfixed_pe_traditional_biomass_ej_delayed()


_delayfixed_pe_traditional_biomass_ej_delayed = DelayFixed(
    lambda: pe_traditional_biomass_consum_ej(),
    lambda: time_step(),
    lambda: 30,
    time_step,
    "_delayfixed_pe_traditional_biomass_ej_delayed",
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
    "World",
    "people_relying_on_traditional_biomass",
    {},
    _root,
    {},
    "_ext_constant_people_relying_trad_biomass_ref",
)


@component.add(
    name="PEpc consumption people depending on trad biomass",
    units="EJ/(year*people)",
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
    return pe_consumption_trad_biomass_ref() / people_relying_trad_biomass_ref()


@component.add(
    name='"phase out trad biomass?"',
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_phase_out_trad_biomass"},
)
def phase_out_trad_biomass():
    return _ext_constant_phase_out_trad_biomass()


_ext_constant_phase_out_trad_biomass = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "phase_out_biomass",
    {},
    _root,
    {},
    "_ext_constant_phase_out_trad_biomass",
)


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
    return (
        pe_traditional_biomass_consum_ej()
        / pepc_consumption_people_depending_on_trad_biomass()
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
    name="share trad biomass",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "phase_out_trad_biomass": 1,
        "time": 2,
        "share_trad_biomass_vs_solids_in_households": 4,
    },
)
def share_trad_biomass():
    return if_then_else(
        phase_out_trad_biomass() == 1,
        lambda: if_then_else(
            time() < 2015,
            lambda: share_trad_biomass_vs_solids_in_households(),
            lambda: share_trad_biomass_vs_solids_in_households()
            - share_trad_biomass_vs_solids_in_households()
            / (2050 - 2015)
            * (time() - 2015),
        ),
        lambda: share_trad_biomass_vs_solids_in_households(),
    )


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
    "World",
    "share_trad_biomass_vs_solids_in_households",
    {},
    _root,
    {},
    "_ext_constant_share_trad_biomass_vs_solids_in_households",
)
