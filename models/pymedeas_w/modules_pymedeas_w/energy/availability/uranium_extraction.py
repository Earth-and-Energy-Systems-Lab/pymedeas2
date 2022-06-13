"""
Module uranium_extraction
Translated using PySD version 3.2.0
"""


@component.add(
    name="abundance uranium",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_demand_uranium": 4, "extraction_uranium_ej": 2},
)
def abundance_uranium():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pe_demand_uranium() == 0,
        lambda: 1,
        lambda: if_then_else(
            extraction_uranium_ej() > pe_demand_uranium(),
            lambda: 1,
            lambda: 1
            - (pe_demand_uranium() - extraction_uranium_ej()) / pe_demand_uranium(),
        ),
    )


@component.add(
    name="Cumulated uranium extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_uranium_extraction": 1},
    other_deps={
        "_integ_cumulated_uranium_extraction": {
            "initial": {"cumulated_uranium_extraction_to_1995": 1},
            "step": {"extraction_uranium_ej": 1},
        }
    },
)
def cumulated_uranium_extraction():
    """
    Cumulated uranium extraction.
    """
    return _integ_cumulated_uranium_extraction()


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


@component.add(
    name="cumulated uranium extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulated_uranium_extraction_to_1995"},
)
def cumulated_uranium_extraction_to_1995():
    """
    Cumulated coal extraction to 1995 (EWG 2006).
    """
    return _ext_constant_cumulated_uranium_extraction_to_1995()


_ext_constant_cumulated_uranium_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


@component.add(
    name="extraction uranium EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unlimited_nre": 1,
        "unlimited_uranium": 1,
        "pe_demand_uranium": 2,
        "max_extraction_uranium": 1,
    },
)
def extraction_uranium_ej():
    """
    Annual extraction of uranium.
    """
    return if_then_else(
        np.logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
        lambda: pe_demand_uranium(),
        lambda: np.minimum(pe_demand_uranium(), max_extraction_uranium()),
    )


@component.add(
    name="max extraction uranium",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_uranium": 1, "table_max_extraction_uranium": 1},
)
def max_extraction_uranium():
    """
    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_uranium(rurr_uranium())


@component.add(
    name="RURR uranium",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_uranium": 1},
    other_deps={
        "_integ_rurr_uranium": {
            "initial": {"urr_uranium": 1, "cumulated_uranium_extraction_to_1995": 1},
            "step": {"extraction_uranium_ej": 1},
        }
    },
)
def rurr_uranium():
    """
    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


@component.add(
    name="table max extraction uranium",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_uranium",
        "__lookup__": "_ext_lookup_table_max_extraction_uranium",
    },
)
def table_max_extraction_uranium(x, final_subs=None):
    return _ext_lookup_table_max_extraction_uranium(x, final_subs)


_ext_lookup_table_max_extraction_uranium = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_uranium",
)


@component.add(
    name='"unlimited uranium?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_unlimited_uranium"},
)
def unlimited_uranium():
    """
    Switch to consider if uranium is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_uranium()


_ext_constant_unlimited_uranium = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_uranium",
    {},
    _root,
    {},
    "_ext_constant_unlimited_uranium",
)


@component.add(
    name="URR uranium",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unlimited_nre": 1, "unlimited_uranium": 1, "urr_uranium_input": 1},
)
def urr_uranium():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        np.logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
        lambda: np.nan,
        lambda: urr_uranium_input(),
    )


@component.add(
    name="URR uranium input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_uranium_input"},
)
def urr_uranium_input():
    return _ext_constant_urr_uranium_input()


_ext_constant_urr_uranium_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_uranium",
    {},
    _root,
    {},
    "_ext_constant_urr_uranium_input",
)


@component.add(
    name="Year scarcity uranium",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_uranium": 1, "time": 1},
)
def year_scarcity_uranium():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_uranium() > 0.95, lambda: 0, lambda: time())
