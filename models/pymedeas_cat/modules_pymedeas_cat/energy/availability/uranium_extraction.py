"""
Module uranium_extraction
Translated using PySD version 2.2.1
"""


def abundance_uranium():
    """
    Real Name: abundance uranium
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pe_demand_uranium_aut_ej() == 0,
        lambda: 1,
        lambda: if_then_else(
            extraction_uranium_ej_aut() + extraction_uranium_row()
            > pe_demand_uranium_aut_ej(),
            lambda: 1,
            lambda: 1
            - (
                pe_demand_uranium_aut_ej()
                - extraction_uranium_ej_aut()
                - extraction_uranium_row()
            )
            / pe_demand_uranium_aut_ej(),
        ),
    )


def av_past_eu_domestic_uranium_extraction():
    """
    Real Name: av past EU domestic uranium extraction
    Original Eqn:
    Units: tonnes
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average 2010-2015 past uranium extraction in the UE.
    """
    return _ext_constant_av_past_eu_domestic_uranium_extraction()


_ext_constant_av_past_eu_domestic_uranium_extraction = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_average_domestic_uranium_extraction",
    {},
    _root,
    "_ext_constant_av_past_eu_domestic_uranium_extraction",
)


def cumulated_uranium_extraction():
    """
    Real Name: Cumulated uranium extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated uranium extraction.
    """
    return _integ_cumulated_uranium_extraction()


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej_aut(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


def cumulated_uranium_extraction_kt():
    """
    Real Name: Cumulated uranium extraction kt
    Original Eqn:
    Units: Kt
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Cumulated uranium extraction (kt).
    """
    return cumulated_uranium_extraction() * kt_uranium_per_ej()


def cumulated_uranium_extraction_to_1995():
    """
    Real Name: cumulated uranium extraction to 1995
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Cumulated coal extraction to 1995 (EWG 2006).
    """
    return _ext_constant_cumulated_uranium_extraction_to_1995()


_ext_constant_cumulated_uranium_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


def extraction_uranium_ej_aut():
    """
    Real Name: extraction uranium EJ AUT
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual extraction of uranium.
    """
    return if_then_else(
        rurr_uranium() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2016,
            lambda: historic_uranium_domestic_eu_extracted_t()
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


def extraction_uranium_kt():
    """
    Real Name: extraction uranium kt
    Original Eqn:
    Units: Kt/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Extracción of uranium in kt.
    """
    return extraction_uranium_ej_aut() * kt_uranium_per_ej()


def extraction_uranium_row():
    """
    Real Name: extraction uranium RoW
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        extraction_uranium_ej_world() > imports_eu_uranium_from_row_ej(),
        lambda: imports_eu_uranium_from_row_ej(),
        lambda: extraction_uranium_ej_world(),
    )


def historic_uranium_domestic_eu_extracted_t():
    """
    Real Name: Historic uranium domestic EU extracted t
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []

    Historic uranium domestic EU extracted.
    """
    return _ext_data_historic_uranium_domestic_eu_extracted_t(time())


_ext_data_historic_uranium_domestic_eu_extracted_t = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_uranium_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_uranium_domestic_eu_extracted_t",
)


def imports_eu_uranium_from_row_ej():
    """
    Real Name: imports EU uranium from RoW EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pe_demand_uranium_aut_ej() - extraction_uranium_ej_aut()


def kt_uranium_per_ej():
    """
    Real Name: kt uranium per EJ
    Original Eqn:
    Units: Kt/EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Unit conversion (1 EJ thermal = 2.3866). See EWG (2006).
    """
    return 2.38663


def max_extraction_uranium_ej():
    """
    Real Name: max extraction uranium EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        1 == 1,
        lambda: av_past_eu_domestic_uranium_extraction()
        / (kt_uranium_per_ej() * tonnes_per_kt()),
        lambda: table_max_extraction_uranium(rurr_uranium()),
    )


def pec_uranium_eu_ej():
    """
    Real Name: PEC uranium EU EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return extraction_uranium_ej_aut() + extraction_uranium_row()


def pec_uranium_eu_kt():
    """
    Real Name: PEC uranium EU kt
    Original Eqn:
    Units: Kt
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pec_uranium_eu_ej() * kt_uranium_per_ej()


def rurr_uranium():
    """
    Real Name: RURR uranium
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej_aut(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


def share_imports_eu_uranium_from_row_vs_extraction_world():
    """
    Real Name: share imports EU uranium from RoW vs extraction World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of EU uranium imports vs total uranium extraction.
    """
    return zidz(imports_eu_uranium_from_row_ej(), extraction_uranium_ej_world())


def table_max_extraction_uranium(x):
    """
    Real Name: table max extraction uranium
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_max_extraction_uranium(x)


_ext_lookup_table_max_extraction_uranium = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    "_ext_lookup_table_max_extraction_uranium",
)


def tonnes_per_kt():
    """
    Real Name: tonnes per kt
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 1000


def unlimited_uranium():
    """
    Real Name: "unlimited uranium?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Switch to consider if uranium is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_uranium()


_ext_constant_unlimited_uranium = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "unlimited_uranium",
    {},
    _root,
    "_ext_constant_unlimited_uranium",
)


def urr_uranium():
    """
    Real Name: URR uranium
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        np.logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
        lambda: nan,
        lambda: urr_uranium_input(),
    )


def urr_uranium_input():
    """
    Real Name: URR uranium input
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_urr_uranium_input()


_ext_constant_urr_uranium_input = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "URR_uranium",
    {},
    _root,
    "_ext_constant_urr_uranium_input",
)


def year_scarcity_uranium():
    """
    Real Name: Year scarcity uranium
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_uranium() > 0.95, lambda: 0, lambda: time())
