"""
Module uranium_extraction_ean
Translated using PySD version 2.2.0
"""


def abundance_uranium():
    """
    Real Name: abundance uranium
    Original Eqn: IF THEN ELSE(PE demand uranium EU EJ=0, 1, IF THEN ELSE((extraction uranium EJ EU+extraction uranium RoW)>PE demand uranium EU EJ , 1, 1-((PE demand uranium EU EJ-extraction uranium EJ EU -extraction uranium RoW)/PE demand uranium EU EJ)) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        pe_demand_uranium_eu_ej() == 0,
        lambda: 1,
        lambda: if_then_else(
            (extraction_uranium_ej_eu() + extraction_uranium_row())
            > pe_demand_uranium_eu_ej(),
            lambda: 1,
            lambda: 1
            - (
                (
                    pe_demand_uranium_eu_ej()
                    - extraction_uranium_ej_eu()
                    - extraction_uranium_row()
                )
                / pe_demand_uranium_eu_ej()
            ),
        ),
    )


def av_past_eu_domestic_uranium_extraction():
    """
    Real Name: av past EU domestic uranium extraction
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'historic_average_domestic_uranium_extraction')
    Units: tonnes
    Limits: (None, None)
    Type: constant
    Subs: None

    Average 2010-2015 past uranium extraction in the UE.
    """
    return _ext_constant_av_past_eu_domestic_uranium_extraction()


def cumulated_uranium_extraction():
    """
    Real Name: Cumulated uranium extraction
    Original Eqn: INTEG ( extraction uranium EJ EU, cumulated uranium extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated uranium extraction.
    """
    return _integ_cumulated_uranium_extraction()


def cumulated_uranium_extraction_kt():
    """
    Real Name: Cumulated uranium extraction kt
    Original Eqn: Cumulated uranium extraction*kt uranium per EJ
    Units: Kt
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated uranium extraction (kt).
    """
    return cumulated_uranium_extraction() * kt_uranium_per_ej()


def cumulated_uranium_extraction_to_1995():
    """
    Real Name: cumulated uranium extraction to 1995
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'cumulative_uranium_extraction_until_1995')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulated coal extraction to 1995 (EWG 2006).
    """
    return _ext_constant_cumulated_uranium_extraction_to_1995()


def extraction_uranium_ej_eu():
    """
    Real Name: extraction uranium EJ EU
    Original Eqn: IF THEN ELSE(RURR uranium<0,0, IF THEN ELSE(Time<2016, Historic uranium domestic EU extracted t/(kt uranium per EJ*tonnes per kt), IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited uranium?"=1, PE demand uranium EU EJ, MIN(PE demand uranium EU EJ, max extraction uranium EJ))))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

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
                logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
                lambda: pe_demand_uranium_eu_ej(),
                lambda: np.minimum(
                    pe_demand_uranium_eu_ej(), max_extraction_uranium_ej()
                ),
            ),
        ),
    )


def extraction_uranium_kt():
    """
    Real Name: extraction uranium kt
    Original Eqn: extraction uranium EJ EU*kt uranium per EJ
    Units: Kt/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Extracción of uranium in kt.
    """
    return extraction_uranium_ej_eu() * kt_uranium_per_ej()


def extraction_uranium_row():
    """
    Real Name: extraction uranium RoW
    Original Eqn: IF THEN ELSE(extraction uranium EJ World>imports EU uranium from RoW EJ ,imports EU uranium from RoW EJ ,extraction uranium EJ World)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        extraction_uranium_ej_world() > imports_eu_uranium_from_row_ej(),
        lambda: imports_eu_uranium_from_row_ej(),
        lambda: extraction_uranium_ej_world(),
    )


def historic_uranium_domestic_eu_extracted_t():
    """
    Real Name: Historic uranium domestic EU extracted t
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_domestic_uranium_extraction')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Historic uranium domestic EU extracted.
    """
    return _ext_data_historic_uranium_domestic_eu_extracted_t(time())


def imports_eu_uranium_from_row_ej():
    """
    Real Name: imports EU uranium from RoW EJ
    Original Eqn: PE demand uranium EU EJ-extraction uranium EJ EU
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pe_demand_uranium_eu_ej() - extraction_uranium_ej_eu()


def kt_uranium_per_ej():
    """
    Real Name: kt uranium per EJ
    Original Eqn: 2.38663
    Units: Kt/EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion (1 EJ thermal = 2.3866). See EWG (2006).
    """
    return 2.38663


def max_extraction_uranium_ej():
    """
    Real Name: max extraction uranium EJ
    Original Eqn: IF THEN ELSE(1=1, av past EU domestic uranium extraction/(kt uranium per EJ*1000), table max extraction uranium(RURR uranium))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return if_then_else(
        1 == 1,
        lambda: av_past_eu_domestic_uranium_extraction() / (kt_uranium_per_ej() * 1000),
        lambda: table_max_extraction_uranium(rurr_uranium()),
    )


def pec_uranium_eu_ej():
    """
    Real Name: PEC uranium EU EJ
    Original Eqn: extraction uranium EJ EU+extraction uranium RoW
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return extraction_uranium_ej_eu() + extraction_uranium_row()


def pec_uranium_eu_kt():
    """
    Real Name: PEC uranium EU kt
    Original Eqn: PEC uranium EU EJ*kt uranium per EJ
    Units: Kt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pec_uranium_eu_ej() * kt_uranium_per_ej()


def rurr_uranium():
    """
    Real Name: RURR uranium
    Original Eqn: INTEG ( -extraction uranium EJ EU, URR uranium-cumulated uranium extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


def share_imports_eu_uranium_from_row_vs_extraction_world():
    """
    Real Name: share imports EU uranium from RoW vs extraction World
    Original Eqn: ZIDZ(imports EU uranium from RoW EJ, extraction uranium EJ World )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of EU uranium imports vs total uranium extraction.
    """
    return zidz(imports_eu_uranium_from_row_ej(), extraction_uranium_ej_world())


def table_max_extraction_uranium(x):
    """
    Real Name: table max extraction uranium
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Europe', 'RURR_uranium', 'max_extraction_uranium'))
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_uranium(x)


def tonnes_per_kt():
    """
    Real Name: tonnes per kt
    Original Eqn: 1000
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1000


def unlimited_uranium():
    """
    Real Name: "unlimited uranium?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'E104')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to consider if uranium is unlimited (1), or if it is limited (0).
        If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_uranium()


def urr_uranium():
    """
    Real Name: URR uranium
    Original Eqn: IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited uranium?"=1, :NA:, URR uranium input)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Ultimately Recoverable Resources (URR) associated to the selected
        depletion curve.
    """
    return if_then_else(
        logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
        lambda: np.nan,
        lambda: urr_uranium_input(),
    )


def urr_uranium_input():
    """
    Real Name: URR uranium input
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'URR_uranium')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_urr_uranium_input()


def year_scarcity_uranium():
    """
    Real Name: Year scarcity uranium
    Original Eqn: IF THEN ELSE(abundance uranium>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_uranium() > 0.95, lambda: 0, lambda: time())


_ext_constant_av_past_eu_domestic_uranium_extraction = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "historic_average_domestic_uranium_extraction",
    {},
    _root,
    "_ext_constant_av_past_eu_domestic_uranium_extraction",
)


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej_eu(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


_ext_constant_cumulated_uranium_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


_ext_data_historic_uranium_domestic_eu_extracted_t = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_uranium_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_uranium_domestic_eu_extracted_t",
)


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej_eu(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


_ext_lookup_table_max_extraction_uranium = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    "_ext_lookup_table_max_extraction_uranium",
)


_ext_constant_unlimited_uranium = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "E104",
    {},
    _root,
    "_ext_constant_unlimited_uranium",
)


_ext_constant_urr_uranium_input = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "URR_uranium",
    {},
    _root,
    "_ext_constant_urr_uranium_input",
)
