"""
Module other_ghg_emissions_and_total_eq
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="CH4 anthro emissions",
    units="Mton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_emissions_fossil_fuels": 1,
        "choose_rcp": 3,
        "ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions": 1,
        "ch4_anthro_emissions_rcp": 4,
    },
)
def ch4_anthro_emissions():
    """
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


@component.add(
    name="CH4 anthro emissions RCP",
    units="Mton/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_ch4_anthro_emissions_rcp",
        "__data__": "_ext_data_ch4_anthro_emissions_rcp",
        "time": 1,
    },
)
def ch4_anthro_emissions_rcp():
    """
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_ch4_anthro_emissions_rcp",
)


@component.add(
    name="Choose RCP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_rcp"},
)
def choose_rcp():
    """
    Choose RCP (Representative Concentration Pathway) 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "RCP_GHG_emissions_select",
    {},
    _root,
    {},
    "_ext_constant_choose_rcp",
)


@component.add(
    name="HFC emissions",
    units="tons/Year",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "hfc_emissions_rcp": 4},
)
def hfc_emissions():
    """
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


@component.add(
    name="HFC emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario", "HFC type"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_hfc_emissions_rcp",
        "__data__": "_ext_data_hfc_emissions_rcp",
        "time": 1,
    },
)
def hfc_emissions_rcp():
    """
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
    {
        "RCP Scenario": _subscript_dict["RCP Scenario"],
        "HFC type": _subscript_dict["HFC type"],
    },
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


@component.add(
    name="N2O Anthro Emissions",
    units="Mton N/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "n2o_anthro_emissions_rcp": 4},
)
def n2o_anthro_emissions():
    """
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


@component.add(
    name="N2O Anthro Emissions RCP",
    units="Mton N/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_n2o_anthro_emissions_rcp",
        "__data__": "_ext_data_n2o_anthro_emissions_rcp",
        "time": 1,
    },
)
def n2o_anthro_emissions_rcp():
    """
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_n2o_anthro_emissions_rcp",
)


@component.add(
    name="PFC emissions",
    units="tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "pfc_emissions_rcp": 4},
)
def pfc_emissions():
    """
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


@component.add(
    name="PFC emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_pfc_emissions_rcp",
        "__data__": "_ext_data_pfc_emissions_rcp",
        "time": 1,
    },
)
def pfc_emissions_rcp():
    """
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_pfc_emissions_rcp",
)


@component.add(
    name="ratio Power Plants Energy Conversion Extraction and Distribution vs total CH4 emissions",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions():
    return 0.2752


@component.add(
    name="SF6 emissions",
    units="tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "sf6_emissions_rcp": 4},
)
def sf6_emissions():
    """
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


@component.add(
    name="SF6 emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sf6_emissions_rcp",
        "__data__": "_ext_data_sf6_emissions_rcp",
        "time": 1,
    },
)
def sf6_emissions_rcp():
    """
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_sf6_emissions_rcp",
)
