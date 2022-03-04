"""
Module other_ghg_emissions_and_total_eq
Translated using PySD version 2.2.1
"""


def ch4_anthro_emissions():
    """
    Real Name: CH4 anthro emissions
    Original Eqn:
    Units: Mton/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) except Power Plants, Energy Conversion, Extraction, and Distribution. Corrected with endogenous data "Total CH4 emissions fossil fuels" Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return total_ch4_emissions_fossil_fuels() + if_then_else(
        choose_rcp() == 1,
        lambda: float(ch4_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(ch4_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(ch4_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(ch4_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    ) * (
        1
        - ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions()
    )


@subs(["RCP Scenario"], _subscript_dict)
def ch4_anthro_emissions_rcp():
    """
    Real Name: CH4 anthro emissions RCP
    Original Eqn:
    Units: Mton/Year
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario']

    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_ch4_anthro_emissions_rcp(time())


_ext_data_ch4_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "CH4_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_ch4_anthro_emissions_rcp",
)


def choose_rcp():
    """
    Real Name: Choose RCP
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Choose RCP (Representative Concentration Pathway) 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "RCP_GHG_emissions_select",
    {},
    _root,
    "_ext_constant_choose_rcp",
)


@subs(["HFC type"], _subscript_dict)
def hfc_emissions():
    """
    Real Name: HFC emissions
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: hfc_emissions_rcp().loc["RCP26", :].reset_coords(drop=True),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: hfc_emissions_rcp().loc["RCP45", :].reset_coords(drop=True),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: hfc_emissions_rcp().loc["RCP60", :].reset_coords(drop=True),
                lambda: hfc_emissions_rcp().loc["RCP85", :].reset_coords(drop=True),
            ),
        ),
    )


@subs(["RCP Scenario", "HFC type"], _subscript_dict)
def hfc_emissions_rcp():
    """
    Real Name: HFC emissions RCP
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario', 'HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_hfc_emissions_rcp(time())


_ext_data_hfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC134a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC134a"]},
    _root,
    "_ext_data_hfc_emissions_rcp",
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC23_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC23"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC32_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC32"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC125_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC125"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC143a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC143a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC152a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC152a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC227ea_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC227ea"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC245ca_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC245ca"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC4310mee_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC4310mee"]},
)


def n2o_anthro_emissions():
    """
    Real Name: N2O Anthro Emissions
    Original Eqn:
    Units: Mton N/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(n2o_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(n2o_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(n2o_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(n2o_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@subs(["RCP Scenario"], _subscript_dict)
def n2o_anthro_emissions_rcp():
    """
    Real Name: N2O Anthro Emissions RCP
    Original Eqn:
    Units: Mton N/Year
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_n2o_anthro_emissions_rcp(time())


_ext_data_n2o_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "N2O_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_n2o_anthro_emissions_rcp",
)


def pfc_emissions():
    """
    Real Name: PFC emissions
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(pfc_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(pfc_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(pfc_emissions_rcp().loc["RCP60"]),
                lambda: float(pfc_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@subs(["RCP Scenario"], _subscript_dict)
def pfc_emissions_rcp():
    """
    Real Name: PFC emissions RCP
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_pfc_emissions_rcp(time())


_ext_data_pfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "PFCs_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_pfc_emissions_rcp",
)


def ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions():
    """
    Real Name: ratio Power Plants Energy Conversion Extraction and Distribution vs total CH4 emissions
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 0.2752


def sf6_emissions():
    """
    Real Name: SF6 emissions
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(sf6_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(sf6_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(sf6_emissions_rcp().loc["RCP60"]),
                lambda: float(sf6_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@subs(["RCP Scenario"], _subscript_dict)
def sf6_emissions_rcp():
    """
    Real Name: SF6 emissions RCP
    Original Eqn:
    Units: tons/Year
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_sf6_emissions_rcp(time())


_ext_data_sf6_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "SF6_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_sf6_emissions_rcp",
)
