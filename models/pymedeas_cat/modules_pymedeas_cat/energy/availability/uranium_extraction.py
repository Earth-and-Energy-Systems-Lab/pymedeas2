"""
Module energy.availability.uranium_extraction
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_uranium",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_demand_uranium_cat_ej": 4,
        "extraction_uranium_row": 2,
        "extraction_uranium_ej_cat": 2,
    },
)
def abundance_uranium():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        np.logical_or(
            pe_demand_uranium_cat_ej() == 0,
            extraction_uranium_ej_cat() + extraction_uranium_row()
            > pe_demand_uranium_cat_ej(),
        ),
        lambda: 1,
        lambda: 1
        - (
            pe_demand_uranium_cat_ej()
            - extraction_uranium_ej_cat()
            - extraction_uranium_row()
        )
        / pe_demand_uranium_cat_ej(),
    )


@component.add(
    name="av_past_CAT_domestic_uranium_extraction",
    units="tonnes/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_av_past_cat_domestic_uranium_extraction"
    },
)
def av_past_cat_domestic_uranium_extraction():
    """
    Average 2010-2015 past uranium extraction in the UE.
    """
    return _ext_constant_av_past_cat_domestic_uranium_extraction()


_ext_constant_av_past_cat_domestic_uranium_extraction = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "historic_average_domestic_uranium_extraction",
    {},
    _root,
    {},
    "_ext_constant_av_past_cat_domestic_uranium_extraction",
)


@component.add(
    name="Cumulated_uranium_extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_uranium_extraction": 1},
    other_deps={
        "_integ_cumulated_uranium_extraction": {
            "initial": {"cumulated_uranium_extraction_to_1995": 1},
            "step": {"extraction_uranium_ej_cat": 1},
        }
    },
)
def cumulated_uranium_extraction():
    """
    Cumulated uranium extraction.
    """
    return _integ_cumulated_uranium_extraction()


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej_cat(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


@component.add(
    name="cumulated_uranium_extraction_to_1995",
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
    r"../energy.xlsx",
    "Catalonia",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


@component.add(
    name="extraction_uranium_EJ_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_uranium": 1,
        "tonnes_per_kt": 1,
        "kt_uranium_per_ej": 1,
        "time": 1,
        "historic_uranium_domestic_extracted": 1,
        "pe_demand_uranium_cat_ej": 1,
        "max_extraction_uranium_ej": 1,
    },
)
def extraction_uranium_ej_cat():
    """
    Annual extraction of uranium.
    """
    return if_then_else(
        rurr_uranium() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2016,
            lambda: historic_uranium_domestic_extracted()
            / (kt_uranium_per_ej() * tonnes_per_kt()),
            lambda: float(
                np.minimum(pe_demand_uranium_cat_ej(), max_extraction_uranium_ej())
            ),
        ),
    )


@component.add(
    name="extraction_uranium_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_uranium_ej_world": 2, "imports_cat_uranium_from_row": 2},
)
def extraction_uranium_row():
    return if_then_else(
        extraction_uranium_ej_world() > imports_cat_uranium_from_row(),
        lambda: imports_cat_uranium_from_row(),
        lambda: extraction_uranium_ej_world(),
    )


@component.add(
    name="Historic_uranium_domestic_extracted",
    units="ton/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_uranium_domestic_extracted",
        "__data__": "_ext_data_historic_uranium_domestic_extracted",
        "time": 1,
    },
)
def historic_uranium_domestic_extracted():
    """
    Historic uranium domestic EU extracted.
    """
    return _ext_data_historic_uranium_domestic_extracted(time())


_ext_data_historic_uranium_domestic_extracted = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_uranium_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_uranium_domestic_extracted",
)


@component.add(
    name="imports_CAT_uranium_from_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_demand_uranium_cat_ej": 1, "extraction_uranium_ej_cat": 1},
)
def imports_cat_uranium_from_row():
    return pe_demand_uranium_cat_ej() - extraction_uranium_ej_cat()


@component.add(
    name="kt_uranium_per_EJ", units="Kt/EJ", comp_type="Constant", comp_subtype="Normal"
)
def kt_uranium_per_ej():
    """
    Unit conversion (1 EJ thermal = 2.3866). See EWG (2006).
    """
    return 2.38663


@component.add(
    name="max_extraction_uranium_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_past_cat_domestic_uranium_extraction": 1,
        "tonnes_per_kt": 1,
        "kt_uranium_per_ej": 1,
        "rurr_uranium": 1,
        "table_max_extraction_uranium": 1,
    },
)
def max_extraction_uranium_ej():
    """
    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        1 == 1,
        lambda: av_past_cat_domestic_uranium_extraction()
        / (kt_uranium_per_ej() * tonnes_per_kt()),
        lambda: table_max_extraction_uranium(rurr_uranium()),
    )


@component.add(
    name="PEC_uranium",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_uranium_ej_cat": 1, "extraction_uranium_row": 1},
)
def pec_uranium():
    return extraction_uranium_ej_cat() + extraction_uranium_row()


@component.add(
    name="RURR_uranium",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_uranium": 1},
    other_deps={
        "_integ_rurr_uranium": {
            "initial": {"urr_uranium": 1, "cumulated_uranium_extraction_to_1995": 1},
            "step": {"extraction_uranium_ej_cat": 1},
        }
    },
)
def rurr_uranium():
    """
    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej_cat(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


@component.add(
    name="share_imports_CAT_uranium_from_RoW_vs_extraction_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_cat_uranium_from_row": 1, "extraction_uranium_ej_world": 1},
)
def share_imports_cat_uranium_from_row_vs_extraction_world():
    """
    Share of EU uranium imports vs total uranium extraction.
    """
    return zidz(imports_cat_uranium_from_row(), extraction_uranium_ej_world())


@component.add(
    name="table_max_extraction_uranium",
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
    r"../energy.xlsx",
    "Catalonia",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_uranium",
)


@component.add(
    name="tonnes_per_kt", units="ton/Kt", comp_type="Constant", comp_subtype="Normal"
)
def tonnes_per_kt():
    return 1000


@component.add(
    name="URR_uranium",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urr_uranium_input": 1},
)
def urr_uranium():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return urr_uranium_input()


@component.add(
    name="URR_uranium_input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_uranium_input"},
)
def urr_uranium_input():
    return _ext_constant_urr_uranium_input()


_ext_constant_urr_uranium_input = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "URR_uranium",
    {},
    _root,
    {},
    "_ext_constant_urr_uranium_input",
)


@component.add(
    name="Year_scarcity_uranium",
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
