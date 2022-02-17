"""
Module other_ghg_emissions_and_total_eq
Translated using PySD version 2.2.1
"""


def ch4_anthro_emissions():
    """
    Real Name: CH4 anthro emissions
    Original Eqn: Total CH4 emissions fossil fuels+IF THEN ELSE(Choose RCP=1, CH4 anthro emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, CH4 anthro emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, CH4 anthro emissions RCP[RCP60], CH4 anthro emissions RCP[RCP85])))*(1-ratio Power Plants Energy Conversion Extraction and Distribution vs total CH4 emissions)
    Units: Mton/Year
    Limits: (None, None)
    Type: component
    Subs: None

    "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
        except  Power Plants, Energy Conversion, Extraction, and Distribution.
        Corrected with endogenous data "Total CH4 emissions fossil fuels"        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'CH4_emissions')
    Units: Mton/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_ch4_anthro_emissions_rcp(time())


def choose_rcp():
    """
    Real Name: Choose RCP
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'RCP_GHG_emissions_select')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Choose RCP (Representative Concentration Pathway)        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


@subs(["HFC type"], _subscript_dict)
def hfc_emissions():
    """
    Real Name: HFC emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, HFC emissions RCP[RCP26, HFC type], IF THEN ELSE(Choose RCP=2, HFC emissions RCP[RCP45, HFC type], IF THEN ELSE(Choose RCP=3, HFC emissions RCP[RCP60, HFC type], HFC emissions RCP[RCP85, HFC type])))
    Units: tons/Year
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: rearrange(
            hfc_emissions_rcp().loc["RCP26", :].reset_coords(drop=True),
            ["HFC type"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: rearrange(
                hfc_emissions_rcp().loc["RCP45", :].reset_coords(drop=True),
                ["HFC type"],
                _subscript_dict,
            ),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: rearrange(
                    hfc_emissions_rcp().loc["RCP60", :].reset_coords(drop=True),
                    ["HFC type"],
                    _subscript_dict,
                ),
                lambda: rearrange(
                    hfc_emissions_rcp().loc["RCP85", :].reset_coords(drop=True),
                    ["HFC type"],
                    _subscript_dict,
                ),
            ),
        ),
    )


@subs(["RCP Scenario", "HFC type"], _subscript_dict)
def hfc_emissions_rcp():
    """
    Real Name: HFC emissions RCP
    Original Eqn:
      GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'HFC134a_emissions')
        .
        .
        .
      GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'HFC4310mee_emissions')
    Units: tons/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario', 'HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_hfc_emissions_rcp(time())


def n2o_anthro_emissions():
    """
    Real Name: N2O Anthro Emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, N2O Anthro Emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, N2O Anthro Emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, N2O Anthro Emissions RCP[RCP60], N2O Anthro Emissions RCP[RCP85])))
    Units: Mton N/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'N2O_emissions')
    Units: Mton N/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_n2o_anthro_emissions_rcp(time())


def pfc_emissions():
    """
    Real Name: PFC emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, PFC emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, PFC emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3,PFC emissions RCP[RCP60], PFC emissions RCP[RCP85])))
    Units: tons/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'PFCs_emissions')
    Units: tons/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_pfc_emissions_rcp(time())


def ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions():
    """
    Real Name: ratio Power Plants Energy Conversion Extraction and Distribution vs total CH4 emissions
    Original Eqn: 0.2752
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.2752


def sf6_emissions():
    """
    Real Name: SF6 emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, SF6 emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, SF6 emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, SF6 emissions RCP[RCP60], SF6 emissions RCP[RCP85])))
    Units: tons/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'Europe', 'year_emissions', 'SF6_emissions')
    Units: tons/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_sf6_emissions_rcp(time())


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


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "RCP_GHG_emissions_select",
    {},
    _root,
    "_ext_constant_choose_rcp",
)


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
