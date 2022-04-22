"""
Module uranium_extraction
Translated using PySD version 3.0.0
"""


@component.add(
    name="abundance uranium", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def abundance_uranium():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        np.logical_or(
            pe_demand_uranium_aut_ej() == 0,
            extraction_uranium_ej_aut() + extraction_uranium_row()
            > pe_demand_uranium_aut_ej(),
        ),
        lambda: 1,
        lambda: 1
        - (
            pe_demand_uranium_aut_ej()
            - extraction_uranium_ej_aut()
            - extraction_uranium_row()
        )
        / pe_demand_uranium_aut_ej(),
    )


@component.add(
    name="av past AUT domestic uranium extraction",
    units="tonnes",
    comp_type="Constant",
    comp_subtype="External",
)
def av_past_aut_domestic_uranium_extraction():
    """
    Average 2010-2015 past uranium extraction in the UE.
    """
    return _ext_constant_av_past_aut_domestic_uranium_extraction()


_ext_constant_av_past_aut_domestic_uranium_extraction = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_average_domestic_uranium_extraction",
    {},
    _root,
    {},
    "_ext_constant_av_past_aut_domestic_uranium_extraction",
)


@component.add(
    name="extraction uranium EJ AUT",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def extraction_uranium_ej_aut():
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
            lambda: if_then_else(
                np.logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
                lambda: pe_demand_uranium_aut_ej(),
                lambda: np.minimum(
                    pe_demand_uranium_aut_ej(), max_extraction_uranium_ej()
                ),
            ),
        ),
    )


@component.add(
    name="extraction uranium RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def extraction_uranium_row():
    return if_then_else(
        extraction_uranium_ej_world() > imports_aut_uranium_from_row(),
        lambda: imports_aut_uranium_from_row(),
        lambda: extraction_uranium_ej_world(),
    )


@component.add(
    name="Cumulated uranium extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def cumulated_uranium_extraction():
    """
    Cumulated uranium extraction.
    """
    return _integ_cumulated_uranium_extraction()


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej_aut(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


@component.add(
    name="cumulated uranium extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
)
def cumulated_uranium_extraction_to_1995():
    """
    Cumulated coal extraction to 1995 (EWG 2006).
    """
    return _ext_constant_cumulated_uranium_extraction_to_1995()


_ext_constant_cumulated_uranium_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


@component.add(
    name="Historic uranium domestic extracted",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
)
def historic_uranium_domestic_extracted():
    """
    Historic uranium domestic EU extracted.
    """
    return _ext_data_historic_uranium_domestic_extracted(time())


_ext_data_historic_uranium_domestic_extracted = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_uranium_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_uranium_domestic_extracted",
)


@component.add(
    name="imports AUT uranium from RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def imports_aut_uranium_from_row():
    return pe_demand_uranium_aut_ej() - extraction_uranium_ej_aut()


@component.add(
    name="kt uranium per EJ", units="Kt/EJ", comp_type="Constant", comp_subtype="Normal"
)
def kt_uranium_per_ej():
    """
    Unit conversion (1 EJ thermal = 2.3866). See EWG (2006).
    """
    return 2.38663


@component.add(
    name="max extraction uranium EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def max_extraction_uranium_ej():
    """
    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        1 == 1,
        lambda: av_past_aut_domestic_uranium_extraction()
        / (kt_uranium_per_ej() * tonnes_per_kt()),
        lambda: table_max_extraction_uranium(rurr_uranium()),
    )


@component.add(
    name="PEC uranium", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pec_uranium():
    return extraction_uranium_ej_aut() + extraction_uranium_row()


@component.add(
    name="RURR uranium", units="EJ", comp_type="Stateful", comp_subtype="Integ"
)
def rurr_uranium():
    """
    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej_aut(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


@component.add(
    name="share imports AUT uranium from RoW vs extraction World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_imports_aut_uranium_from_row_vs_extraction_world():
    """
    Share of EU uranium imports vs total uranium extraction.
    """
    return zidz(imports_aut_uranium_from_row(), extraction_uranium_ej_world())


@component.add(
    name="table max extraction uranium",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def table_max_extraction_uranium(x, final_subs=None):
    return _ext_lookup_table_max_extraction_uranium(x, final_subs)


_ext_lookup_table_max_extraction_uranium = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_uranium",
)


@component.add(
    name="tonnes per kt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def tonnes_per_kt():
    return 1000


@component.add(
    name='"unlimited uranium?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def unlimited_uranium():
    """
    Switch to consider if uranium is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_uranium()


_ext_constant_unlimited_uranium = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "unlimited_uranium",
    {},
    _root,
    {},
    "_ext_constant_unlimited_uranium",
)


@component.add(
    name="URR uranium", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="URR uranium input", units="EJ", comp_type="Constant", comp_subtype="External"
)
def urr_uranium_input():
    return _ext_constant_urr_uranium_input()


_ext_constant_urr_uranium_input = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "URR_uranium",
    {},
    _root,
    {},
    "_ext_constant_urr_uranium_input",
)


@component.add(
    name="Year scarcity uranium",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def year_scarcity_uranium():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_uranium() > 0.95, lambda: 0, lambda: time())
