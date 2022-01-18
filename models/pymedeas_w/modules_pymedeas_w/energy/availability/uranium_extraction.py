"""
Module uranium_extraction
Translated using PySD version 2.2.0
"""


def abundance_uranium():
    """
    Real Name: abundance uranium
    Original Eqn: IF THEN ELSE(PE demand uranium EJ=0, 1, IF THEN ELSE(extraction uranium EJ>PE demand uranium EJ , 1, 1-((PE demand uranium EJ-extraction uranium EJ)/PE demand uranium EJ)))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        pe_demand_uranium_ej() == 0,
        lambda: 1,
        lambda: if_then_else(
            extraction_uranium_ej() > pe_demand_uranium_ej(),
            lambda: 1,
            lambda: 1
            - (
                (pe_demand_uranium_ej() - extraction_uranium_ej())
                / pe_demand_uranium_ej()
            ),
        ),
    )


def cumulated_uranium_extraction():
    """
    Real Name: Cumulated uranium extraction
    Original Eqn: INTEG ( extraction uranium EJ, cumulated uranium extraction to 1995)
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
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'cumulative_uranium_extraction_until_1995')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulated coal extraction to 1995 (EWG 2006).
    """
    return _ext_constant_cumulated_uranium_extraction_to_1995()


def extraction_uranium_ej():
    """
    Real Name: extraction uranium EJ
    Original Eqn: IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited uranium?"=1, PE demand uranium EJ, MIN(PE demand uranium EJ, max extraction uranium EJ))
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of uranium.
    """
    return if_then_else(
        logical_or(unlimited_nre() == 1, unlimited_uranium() == 1),
        lambda: pe_demand_uranium_ej(),
        lambda: np.minimum(pe_demand_uranium_ej(), max_extraction_uranium_ej()),
    )


def extraction_uranium_kt():
    """
    Real Name: extraction uranium kt
    Original Eqn: extraction uranium EJ*kt uranium per EJ
    Units: Kt/year
    Limits: (None, None)
    Type: component
    Subs: None

    Extracción of uranium in kt.
    """
    return extraction_uranium_ej() * kt_uranium_per_ej()


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
    Original Eqn: table max extraction uranium(RURR uranium)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_uranium(rurr_uranium())


def rurr_uranium():
    """
    Real Name: RURR uranium
    Original Eqn: INTEG ( -extraction uranium EJ, URR uranium-cumulated uranium extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR uranium. 720 EJ extracted before 1990.
    """
    return _integ_rurr_uranium()


def table_max_extraction_uranium(x):
    """
    Real Name: table max extraction uranium
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'RURR_uranium', 'max_extraction_uranium')
    Units: EJ/year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_uranium(x)


def unlimited_uranium():
    """
    Real Name: "unlimited uranium?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'E104')
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
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'URR_uranium')
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
    Units: year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_uranium() > 0.95, lambda: 0, lambda: time())


_integ_cumulated_uranium_extraction = Integ(
    lambda: extraction_uranium_ej(),
    lambda: cumulated_uranium_extraction_to_1995(),
    "_integ_cumulated_uranium_extraction",
)


_ext_constant_cumulated_uranium_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_uranium_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_uranium_extraction_to_1995",
)


_integ_rurr_uranium = Integ(
    lambda: -extraction_uranium_ej(),
    lambda: urr_uranium() - cumulated_uranium_extraction_to_1995(),
    "_integ_rurr_uranium",
)


_ext_lookup_table_max_extraction_uranium = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_uranium",
    "max_extraction_uranium",
    {},
    _root,
    "_ext_lookup_table_max_extraction_uranium",
)


_ext_constant_unlimited_uranium = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "E104",
    {},
    _root,
    "_ext_constant_unlimited_uranium",
)


_ext_constant_urr_uranium_input = ExtConstant(
    "../energy.xlsx",
    "World",
    "URR_uranium",
    {},
    _root,
    "_ext_constant_urr_uranium_input",
)
