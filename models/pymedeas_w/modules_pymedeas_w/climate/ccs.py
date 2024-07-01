"""
Module climate.ccs
Translated using PySD version 3.14.0
"""

@component.add(
    name="CCS_cp",
    units="Dmnl",
    subscripts=["CCS_tech"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def ccs_cp():
    """
    Capacity factor of the carbon capture and storage technologies
    """
    return xr.DataArray(1, {"CCS_tech": _subscript_dict["CCS_tech"]}, ["CCS_tech"])


@component.add(
    name="CCS_efficiency",
    units="TWh/GtCO2",
    subscripts=["CCS_tech"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ccs_efficiency"},
)
def ccs_efficiency():
    return _ext_constant_ccs_efficiency()


_ext_constant_ccs_efficiency = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ccs_efficiency*",
    {"CCS_tech": _subscript_dict["CCS_tech"]},
    _root,
    {"CCS_tech": _subscript_dict["CCS_tech"]},
    "_ext_constant_ccs_efficiency",
)


@component.add(
    name="CCS_energy_consumption_sector",
    units="TWh/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1, "scarcity_final_fuels": 1},
)
def ccs_energy_consumption_sector():
    return ccs_energy_demand_sect() * float(scarcity_final_fuels().loc["electricity"])


@component.add(
    name="CCS_energy_demand_sect",
    units="TWh/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect_tech": 1},
)
def ccs_energy_demand_sect():
    """
    Total energy demand for CCS (electricity) by sector TODO:No té cap limitació
    """
    return sum(
        ccs_energy_demand_sect_tech().rename({"CCS_tech": "CCS_tech!"}),
        dim=["CCS_tech!"],
    )


@component.add(
    name="CCS_energy_demand_sect_tech",
    units="TWh/year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_sector_tech": 1, "ccs_cp": 1, "twe_per_twh": 1},
)
def ccs_energy_demand_sect_tech():
    return ccs_sector_tech() * ccs_cp() / twe_per_twh()


@component.add(
    name="CCS_policy",
    units="TW",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
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
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_CCS",
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    _root,
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    "_ext_lookup_ccs_policy",
)


@component.add(
    name="CCS_sector_tech",
    units="TW",
    subscripts=["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
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
                "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
                "CCS_tech": _subscript_dict["CCS_tech"],
            },
            ["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
        ),
        lambda: ccs_policy(time()) * ccs_tech_share(time()),
    )


@component.add(
    name="CCS_tech_share",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
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
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_hh",
    {"SECTORS_and_HOUSEHOLDS": ["Households"], "CCS_tech": _subscript_dict["CCS_tech"]},
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
    "_ext_lookup_ccs_tech_share",
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_agr",
    {
        "SECTORS_and_HOUSEHOLDS": ["Agriculture"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_mqes",
    {
        "SECTORS_and_HOUSEHOLDS": ["Mining_quarrying_and_energy_supply"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fbt",
    {
        "SECTORS_and_HOUSEHOLDS": ["Food_Beverages_and_Tobacco"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_tex",
    {
        "SECTORS_and_HOUSEHOLDS": ["Textiles_and_leather_etc"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coke",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Coke_refined_petroleum_nuclear_fuel_and_chemicals_etc"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_eoete",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Electrical_and_optical_equipment_and_Transport_equipment"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_om",
    {
        "SECTORS_and_HOUSEHOLDS": ["Other_manufacturing"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_cons",
    {
        "SECTORS_and_HOUSEHOLDS": ["Construction"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_dist",
    {
        "SECTORS_and_HOUSEHOLDS": ["Distribution"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_hr",
    {
        "SECTORS_and_HOUSEHOLDS": ["Hotels_and_restaurant"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_tsc",
    {
        "SECTORS_and_HOUSEHOLDS": ["Transport_storage_and_communication"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fi",
    {
        "SECTORS_and_HOUSEHOLDS": ["Financial_Intermediation"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_re",
    {
        "SECTORS_and_HOUSEHOLDS": ["Real_estate_renting_and_busine_activitie"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_nms",
    {
        "SECTORS_and_HOUSEHOLDS": ["Non_Market_Service"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)


@component.add(
    name="CO2_captured_sector_CCS",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
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
            co2_captured_sector_tech_ccs().rename({"CCS_tech": "CCS_tech!"}),
            dim=["CCS_tech!"],
        ),
        co2_emissions_households_and_sectors_fossil_fuels()
        * float(scarcity_final_fuels().loc["electricity"]),
    )


@component.add(
    name="CO2_captured_sector_tech_CCS",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
    comp_type="Constant, Auxiliary",
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
            "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
            "CCS_tech": _subscript_dict["CCS_tech"],
        },
        ["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["SECTORS_CCS"], :] = False
    value.values[except_subs.values] = 0
    value.loc[_subscript_dict["SECTORS_CCS"], :] = (
        ccs_sector_tech()
        .loc[_subscript_dict["SECTORS_CCS"], :]
        .rename({"SECTORS_and_HOUSEHOLDS": "SECTORS_CCS"})
        * ccs_cp()
        / twe_per_twh()
        / ccs_efficiency()
    ).values
    return value


@component.add(
    name="CO2_emissions_households_and_sectors_fossil_fuels",
    units="GTCO2e/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors_before_ccs": 1},
)
def co2_emissions_households_and_sectors_fossil_fuels():
    return sum(
        co2_emissions_households_and_sectors_before_ccs()
        .loc[_subscript_dict["matter_final_sources"], :]
        .rename({"final_sources": "matter_final_sources!"}),
        dim=["matter_final_sources!"],
    )


@component.add(
    name="total_CO2_captured_CCS",
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
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )
