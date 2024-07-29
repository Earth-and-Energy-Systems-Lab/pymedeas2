"""
Module climate.ccs
Translated using PySD version 3.14.1
"""

@component.add(
    name="CCS cp",
    units="Dmnl",
    subscripts=["CCS tech"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def ccs_cp():
    """
    Capacity factor of the carbon capture and storage technologies
    """
    return xr.DataArray(1, {"CCS tech": _subscript_dict["CCS tech"]}, ["CCS tech"])


@component.add(
    name="CCS efficiency",
    units="TWh/GtCO2",
    subscripts=["CCS tech"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ccs_efficiency"},
)
def ccs_efficiency():
    return _ext_constant_ccs_efficiency()


_ext_constant_ccs_efficiency = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "ccs_efficiency*",
    {"CCS tech": _subscript_dict["CCS tech"]},
    _root,
    {"CCS tech": _subscript_dict["CCS tech"]},
    "_ext_constant_ccs_efficiency",
)


@component.add(
    name="CCS energy consumption sector",
    units="TWh/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1, "scarcity_final_fuels": 1},
)
def ccs_energy_consumption_sector():
    return ccs_energy_demand_sect() * float(scarcity_final_fuels().loc["electricity"])


@component.add(
    name="CCS energy demand sect",
    units="TWh/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect_tech": 1},
)
def ccs_energy_demand_sect():
    """
    Total energy demand for CCS (electricity) by sector TODO:No té cap limitació
    """
    return sum(
        ccs_energy_demand_sect_tech().rename({"CCS tech": "CCS tech!"}),
        dim=["CCS tech!"],
    )


@component.add(
    name="CCS energy demand sect tech",
    units="TWh/year",
    subscripts=["SECTORS and HOUSEHOLDS", "CCS tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_sector_tech": 1, "ccs_cp": 1, "twe_per_twh": 1},
)
def ccs_energy_demand_sect_tech():
    return ccs_sector_tech() * ccs_cp() / twe_per_twh()


@component.add(
    name="CCS policy",
    units="TW",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_ccs_policy",
        "__lookup__": "_ext_lookup_ccs_policy",
    },
)
def ccs_policy(x, final_subs=None):
    return _ext_lookup_ccs_policy(x, final_subs)


_ext_lookup_ccs_policy = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_CCS",
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    _root,
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    "_ext_lookup_ccs_policy",
)


@component.add(
    name="CCS sector tech",
    units="TW",
    subscripts=["SECTORS and HOUSEHOLDS", "CCS tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "ccs_policy": 1, "ccs_tech_share": 1},
)
def ccs_sector_tech():
    return if_then_else(
        time() < 2020,
        lambda: xr.DataArray(
            0,
            {
                "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                "CCS tech": _subscript_dict["CCS tech"],
            },
            ["SECTORS and HOUSEHOLDS", "CCS tech"],
        ),
        lambda: ccs_policy(time()) * ccs_tech_share(time()),
    )


@component.add(
    name="CCS tech share",
    units="Dmnl",
    subscripts=["SECTORS and HOUSEHOLDS", "CCS tech"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_ccs_tech_share",
        "__lookup__": "_ext_lookup_ccs_tech_share",
    },
)
def ccs_tech_share(x, final_subs=None):
    return _ext_lookup_ccs_tech_share(x, final_subs)


_ext_lookup_ccs_tech_share = ExtLookup(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_hh",
    {"SECTORS and HOUSEHOLDS": ["Households"], "CCS tech": _subscript_dict["CCS tech"]},
    _root,
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
    "_ext_lookup_ccs_tech_share",
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_agr",
    {
        "SECTORS and HOUSEHOLDS": ["Agriculture"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_mqes",
    {
        "SECTORS and HOUSEHOLDS": ["Mining quarrying and energy supply"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fbt",
    {
        "SECTORS and HOUSEHOLDS": ["Food Beverages and Tobacco"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_tex",
    {
        "SECTORS and HOUSEHOLDS": ["Textiles and leather etc"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coke",
    {
        "SECTORS and HOUSEHOLDS": [
            "Coke refined petroleum nuclear fuel and chemicals etc"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_eoete",
    {
        "SECTORS and HOUSEHOLDS": [
            "Electrical and optical equipment and Transport equipment"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_om",
    {
        "SECTORS and HOUSEHOLDS": ["Other manufacturing"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_cons",
    {
        "SECTORS and HOUSEHOLDS": ["Construction"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_dist",
    {
        "SECTORS and HOUSEHOLDS": ["Distribution"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_hr",
    {
        "SECTORS and HOUSEHOLDS": ["Hotels and restaurant"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_tsc",
    {
        "SECTORS and HOUSEHOLDS": ["Transport storage and communication"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fi",
    {
        "SECTORS and HOUSEHOLDS": ["Financial Intermediation"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_re",
    {
        "SECTORS and HOUSEHOLDS": ["Real estate renting and busine activitie"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_nms",
    {
        "SECTORS and HOUSEHOLDS": ["Non Market Service"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)


@component.add(
    name="CO2 captured sector CCS",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_captured_sector_tech_ccs": 1,
        "co2_emissions_households_and_sectors_fossil_fuels": 1,
        "scarcity_final_fuels": 1,
    },
)
def co2_captured_sector_ccs():
    """
    CO2 captured by each sector with CCS technologies developed. TODO: only a share of the emissions can be captured according to the implemented technology.
    """
    return np.minimum(
        sum(
            co2_captured_sector_tech_ccs().rename({"CCS tech": "CCS tech!"}),
            dim=["CCS tech!"],
        ),
        co2_emissions_households_and_sectors_fossil_fuels()
        * float(scarcity_final_fuels().loc["electricity"]),
    )


@component.add(
    name="CO2 captured sector tech CCS",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS", "CCS tech"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "ccs_sector_tech": 1,
        "ccs_cp": 1,
        "twe_per_twh": 1,
        "ccs_efficiency": 1,
    },
)
def co2_captured_sector_tech_ccs():
    value = xr.DataArray(
        np.nan,
        {
            "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
            "CCS tech": _subscript_dict["CCS tech"],
        },
        ["SECTORS and HOUSEHOLDS", "CCS tech"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["SECTORS CCS"], :] = False
    value.values[except_subs.values] = 0
    value.loc[_subscript_dict["SECTORS CCS"], :] = (
        ccs_sector_tech()
        .loc[_subscript_dict["SECTORS CCS"], :]
        .rename({"SECTORS and HOUSEHOLDS": "SECTORS CCS"})
        * ccs_cp()
        / twe_per_twh()
        / ccs_efficiency()
    ).values
    return value


@component.add(
    name="CO2 emissions households and sectors fossil fuels",
    units="GTCO2e/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors_before_ccs": 1},
)
def co2_emissions_households_and_sectors_fossil_fuels():
    return sum(
        co2_emissions_households_and_sectors_before_ccs()
        .loc[_subscript_dict["matter final sources"], :]
        .rename({"final sources": "matter final sources!"}),
        dim=["matter final sources!"],
    )


@component.add(
    name="total CO2 captured CCS",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_captured_sector_ccs": 1},
)
def total_co2_captured_ccs():
    """
    Total yearly CO2 captured by CCS technologies
    """
    return sum(
        co2_captured_sector_ccs().rename(
            {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )
