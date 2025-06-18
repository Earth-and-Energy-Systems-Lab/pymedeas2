"""
Module climate.ccs
Translated using PySD version 3.14.2
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
    r"../climate.xlsx",
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
    return ccs_energy_demand_sect() * (
        1 - float(scarcity_final_fuels().loc["electricity"])
    )


@component.add(
    name="CCS_energy_demand_sect",
    units="TWh/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect_tech": 1, "share_captured_sector_delayed": 1},
)
def ccs_energy_demand_sect():
    """
    Total energy demand for CCS (electricity) by sector TODO:No té cap limitació
    """
    return (
        sum(
            ccs_energy_demand_sect_tech().rename({"CCS_tech": "CCS_tech!"}),
            dim=["CCS_tech!"],
        )
        * share_captured_sector_delayed()
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
    r"../../scenarios/scen_w.xlsx",
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
    depends_on={"time": 3, "ccs_tech_share": 1, "ccs_policy": 1},
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
    r"../climate.xlsx",
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
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_agr",
    {
        "SECTORS_and_HOUSEHOLDS": ["Agriculture"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_air_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Air_Transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_chemical_and_petrochemical",
    {
        "SECTORS_and_HOUSEHOLDS": ["Chemical_and_Petrochemical"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coal_and_peat_mining",
    {
        "SECTORS_and_HOUSEHOLDS": ["Coal_and_Peat_Mining"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coke_oven_products",
    {
        "SECTORS_and_HOUSEHOLDS": ["Coke_Oven_Products"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_commercial_and_public_services",
    {
        "SECTORS_and_HOUSEHOLDS": ["Commercial_and_Public_Services"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_construction",
    {
        "SECTORS_and_HOUSEHOLDS": ["Construction"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_electricity_and_heat_generation",
    {
        "SECTORS_and_HOUSEHOLDS": ["Electricity_and_Heat_Generation"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fishing",
    {"SECTORS_and_HOUSEHOLDS": ["Fishing"], "CCS_tech": _subscript_dict["CCS_tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_food_and_tobacco",
    {
        "SECTORS_and_HOUSEHOLDS": ["Food_and_Tobacco"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_iron_and_steel",
    {
        "SECTORS_and_HOUSEHOLDS": ["Iron_and_Steel"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_land_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Land_Transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_liquefaction_and_regasification_plants",
    {
        "SECTORS_and_HOUSEHOLDS": ["Liquefaction_and_Regasification_Plants"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_machinery",
    {"SECTORS_and_HOUSEHOLDS": ["Machinery"], "CCS_tech": _subscript_dict["CCS_tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_mining_and_quarrying",
    {
        "SECTORS_and_HOUSEHOLDS": ["Mining_and_Quarrying"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_non_ferrous_metals",
    {
        "SECTORS_and_HOUSEHOLDS": ["Non_Ferrous_Metals"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_non_metallic_minerals",
    {
        "SECTORS_and_HOUSEHOLDS": ["Non_Metallic_Minerals"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_nuclear_industry",
    {
        "SECTORS_and_HOUSEHOLDS": ["Nuclear_Industry"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_oil_refineries",
    {
        "SECTORS_and_HOUSEHOLDS": ["Oil_Refineries"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_oil_and_gas_extraction",
    {
        "SECTORS_and_HOUSEHOLDS": ["Oil_and_Gas_Extraction"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_other_industry",
    {
        "SECTORS_and_HOUSEHOLDS": ["Other_Industry"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_paper_pulp_and_print",
    {
        "SECTORS_and_HOUSEHOLDS": ["Paper_Pulp_and_Print"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_pipeline_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Pipeline_Transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_textile_and_leather",
    {
        "SECTORS_and_HOUSEHOLDS": ["Textile_and_Leather"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_transport_equipment",
    {
        "SECTORS_and_HOUSEHOLDS": ["Transport_Equipment"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_water_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Water_Transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_wood_and_wood_products",
    {
        "SECTORS_and_HOUSEHOLDS": ["Wood_and_Wood_Products"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)


@component.add(
    name="CO2_captured_by_sector_energy_related",
    units="GTCO2e/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 2,
        "time": 4,
        "share_ccs_energy_related": 2,
        "co2_emissions_households_and_sectors_fossil_fuels": 2,
        "share_beccs": 2,
        "co2_emissions_per_fuel": 2,
    },
)
def co2_captured_by_sector_energy_related():
    value = xr.DataArray(
        np.nan,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["Electricity_and_Heat_Generation"]] = False
    value.values[except_subs.values] = np.minimum(
        co2_policy_captured_sector_ccs() * share_ccs_energy_related(time()),
        co2_emissions_households_and_sectors_fossil_fuels() * (1 + share_beccs(time())),
    ).values[except_subs.values]
    value.loc[["Electricity_and_Heat_Generation"]] = float(
        np.minimum(
            float(
                co2_policy_captured_sector_ccs().loc["Electricity_and_Heat_Generation"]
            )
            * float(
                share_ccs_energy_related(time()).loc["Electricity_and_Heat_Generation"]
            ),
            (
                float(
                    co2_emissions_households_and_sectors_fossil_fuels().loc[
                        "Electricity_and_Heat_Generation"
                    ]
                )
                + float(co2_emissions_per_fuel().loc["electricity"])
                + float(co2_emissions_per_fuel().loc["heat"])
            )
            * (1 + share_beccs(time())),
        )
    )
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
    name="CO2_policy_capture_sector_tech_CCS",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "CCS_tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ccs_sector_tech": 1,
        "ccs_cp": 1,
        "twe_per_twh": 1,
        "ccs_efficiency": 1,
    },
)
def co2_policy_capture_sector_tech_ccs():
    return ccs_sector_tech() * ccs_cp() / twe_per_twh() / ccs_efficiency()


@component.add(
    name="CO2_policy_captured_sector_CCS",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_policy_capture_sector_tech_ccs": 1, "scarcity_final_fuels": 1},
)
def co2_policy_captured_sector_ccs():
    """
    CO2 captured by each sector with CCS technologies developed. TODO: only a share of the emissions can be captured according to the implemented technology.
    """
    return sum(
        co2_policy_capture_sector_tech_ccs().rename({"CCS_tech": "CCS_tech!"}),
        dim=["CCS_tech!"],
    ) * (1 - float(scarcity_final_fuels().loc["electricity"]))


@component.add(
    name="DAC_CO2_captured",
    units="GTCO2e/year",
    subscripts=["dac_tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_per_tech": 1, "dac_efficiency": 1, "twe_per_twh": 1},
)
def dac_co2_captured():
    return (
        dac_per_tech()
        / dac_efficiency().loc[:, "electricity"].reset_coords(drop=True)
        / twe_per_twh()
    )


@component.add(
    name="DAC_efficiency",
    units="TWh/GtCO2",
    subscripts=["dac_tech", "dac_final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_dac_efficiency"},
)
def dac_efficiency():
    return _ext_constant_dac_efficiency()


_ext_constant_dac_efficiency = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "dac_efficiency",
    {
        "dac_tech": _subscript_dict["dac_tech"],
        "dac_final_sources": _subscript_dict["dac_final_sources"],
    },
    _root,
    {
        "dac_tech": _subscript_dict["dac_tech"],
        "dac_final_sources": _subscript_dict["dac_final_sources"],
    },
    "_ext_constant_dac_efficiency",
)


@component.add(
    name="DAC_energy_consumption_by_sector_and_fuel",
    units="TWh/year",
    subscripts=["dac_final_sources", "SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand_per_sector_and_fuel": 1, "scarcity_final_fuels": 1},
)
def dac_energy_consumption_by_sector_and_fuel():
    return dac_energy_demand_per_sector_and_fuel() * (
        1
        - scarcity_final_fuels()
        .loc[_subscript_dict["dac_final_sources"]]
        .rename({"final_sources": "dac_final_sources"})
    )


@component.add(
    name="DAC_energy_demand",
    units="TWh/year",
    subscripts=["dac_tech", "dac_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "dac_per_tech": 2,
        "twe_per_twh": 2,
        "share_heat_vs_electricity_in_dac_per_tech": 1,
    },
)
def dac_energy_demand():
    value = xr.DataArray(
        np.nan,
        {
            "dac_tech": _subscript_dict["dac_tech"],
            "dac_final_sources": _subscript_dict["dac_final_sources"],
        },
        ["dac_tech", "dac_final_sources"],
    )
    value.loc[:, ["heat"]] = (
        (dac_per_tech() / twe_per_twh() * share_heat_vs_electricity_in_dac_per_tech())
        .expand_dims({"dac_final_sources": ["heat"]}, 1)
        .values
    )
    value.loc[:, ["electricity"]] = (
        (dac_per_tech() / twe_per_twh())
        .expand_dims({"dac_final_sources": ["electricity"]}, 1)
        .values
    )
    return value


@component.add(
    name="DAC_energy_demand_per_sector_and_fuel",
    units="TWh/year",
    subscripts=["dac_final_sources", "SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand": 1, "share_fed_by_sector_delayed": 1},
)
def dac_energy_demand_per_sector_and_fuel():
    return (
        sum(dac_energy_demand().rename({"dac_tech": "dac_tech!"}), dim=["dac_tech!"])
        * share_fed_by_sector_delayed()
    )


@component.add(
    name="DAC_per_tech",
    units="TW",
    subscripts=["dac_tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "dac_policy_electricity": 1, "dac_tech_share": 1},
)
def dac_per_tech():
    return dac_policy_electricity(time()) * dac_tech_share(time())


@component.add(
    name="DAC_policy_electricity",
    units="TW",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_dac_policy_electricity",
        "__lookup__": "_ext_lookup_dac_policy_electricity",
    },
)
def dac_policy_electricity(x, final_subs=None):
    return _ext_lookup_dac_policy_electricity(x, final_subs)


_ext_lookup_dac_policy_electricity = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_DAC",
    {},
    _root,
    {},
    "_ext_lookup_dac_policy_electricity",
)


@component.add(
    name="DAC_tech_share",
    units="Dmnl",
    subscripts=["dac_tech"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_dac_tech_share",
        "__lookup__": "_ext_lookup_dac_tech_share",
    },
)
def dac_tech_share(x, final_subs=None):
    return _ext_lookup_dac_tech_share(x, final_subs)


_ext_lookup_dac_tech_share = ExtLookup(
    r"../climate.xlsx",
    "World",
    "year_ccs_tech",
    "dac_tech_share",
    {"dac_tech": _subscript_dict["dac_tech"]},
    _root,
    {"dac_tech": _subscript_dict["dac_tech"]},
    "_ext_lookup_dac_tech_share",
)


@component.add(
    name="Overcapacity_CCS_process",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_process_emissions": 2, "process_co2_captured_ccs": 2},
)
def overcapacity_ccs_process():
    return if_then_else(
        total_process_emissions()
        < sum(
            process_co2_captured_ccs().rename(
                {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        ),
        lambda: zidz(
            sum(
                process_co2_captured_ccs().rename(
                    {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
                ),
                dim=["SECTORS_and_HOUSEHOLDS!"],
            ),
            total_process_emissions(),
        )
        - 1,
        lambda: 0,
    )


@component.add(
    name="process_CO2_captured_CCS",
    units="GTCO2e/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 1,
        "time": 1,
        "share_ccs_energy_related": 1,
    },
)
def process_co2_captured_ccs():
    """
    Process emissions captured by CCS technologies
    """
    return co2_policy_captured_sector_ccs() * (1 - share_ccs_energy_related(time()))


@component.add(
    name="share_BECCS",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_share_beccs",
        "__lookup__": "_ext_lookup_share_beccs",
    },
)
def share_beccs(x, final_subs=None):
    return _ext_lookup_share_beccs(x, final_subs)


_ext_lookup_share_beccs = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_BECCS",
    {},
    _root,
    {},
    "_ext_lookup_share_beccs",
)


@component.add(
    name="share_captured_sector",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 2,
        "process_co2_captured_ccs": 1,
        "co2_captured_by_sector_energy_related": 1,
    },
)
def share_captured_sector():
    """
    share of carbon captured that is not captured due to the fact that it has used absorbed all the co2 (energy-related) emited by the sector.
    """
    return if_then_else(
        co2_policy_captured_sector_ccs() == 0,
        lambda: xr.DataArray(
            1,
            {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
            ["SECTORS_and_HOUSEHOLDS"],
        ),
        lambda: zidz(
            co2_captured_by_sector_energy_related() + process_co2_captured_ccs(),
            co2_policy_captured_sector_ccs(),
        ),
    )


@component.add(
    name="share_captured_sector_delayed",
    units="percent",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_share_captured_sector_delayed": 1},
    other_deps={
        "_delayfixed_share_captured_sector_delayed": {
            "initial": {"time_step": 1},
            "step": {"share_captured_sector": 1},
        }
    },
)
def share_captured_sector_delayed():
    return _delayfixed_share_captured_sector_delayed()


_delayfixed_share_captured_sector_delayed = DelayFixed(
    lambda: share_captured_sector(),
    lambda: time_step(),
    lambda: xr.DataArray(
        1,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    ),
    time_step,
    "_delayfixed_share_captured_sector_delayed",
)


@component.add(
    name="share_CCS_energy_related",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_share_ccs_energy_related",
        "__lookup__": "_ext_lookup_share_ccs_energy_related",
    },
)
def share_ccs_energy_related(x, final_subs=None):
    return _ext_lookup_share_ccs_energy_related(x, final_subs)


_ext_lookup_share_ccs_energy_related = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_ccs_energy",
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    _root,
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    "_ext_lookup_share_ccs_energy_related",
)


@component.add(
    name="share_fed_by_sector_delayed",
    units="percent",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_share_fed_by_sector_delayed": 1},
    other_deps={
        "_delayfixed_share_fed_by_sector_delayed": {
            "initial": {"time_step": 1},
            "step": {"share_fed_by_sector": 1},
        }
    },
)
def share_fed_by_sector_delayed():
    return _delayfixed_share_fed_by_sector_delayed()


_delayfixed_share_fed_by_sector_delayed = DelayFixed(
    lambda: share_fed_by_sector(),
    lambda: time_step(),
    lambda: xr.DataArray(
        0,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    ),
    time_step,
    "_delayfixed_share_fed_by_sector_delayed",
)


@component.add(
    name="share_heat_vs_electricity_in_DAC_per_tech",
    units="1",
    subscripts=["dac_tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_efficiency": 2},
)
def share_heat_vs_electricity_in_dac_per_tech():
    return dac_efficiency().loc[:, "heat"].reset_coords(
        drop=True
    ) / dac_efficiency().loc[:, "electricity"].reset_coords(drop=True)


@component.add(
    name="tot_ccs",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "process_co2_captured_ccs": 1,
        "total_co2_captured_ccs_energy_related": 1,
    },
)
def tot_ccs():
    return (
        sum(
            process_co2_captured_ccs().rename(
                {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        )
        + total_co2_captured_ccs_energy_related()
    )


@component.add(
    name="total_CCS_energy_demand",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1},
)
def total_ccs_energy_demand():
    return sum(
        ccs_energy_demand_sect().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="Total_co2_captured",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_captured_ccs_energy_related": 1,
        "total_dac_co2_captured": 1,
        "process_co2_captured_ccs": 1,
    },
)
def total_co2_captured():
    return (
        total_co2_captured_ccs_energy_related()
        + total_dac_co2_captured()
        + sum(
            process_co2_captured_ccs().rename(
                {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        )
    )


@component.add(
    name="total_CO2_captured_CCS",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_policy_captured_sector_ccs": 1},
)
def total_co2_captured_ccs():
    """
    Total yearly CO2 captured by CCS technologies
    """
    return sum(
        co2_policy_captured_sector_ccs().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="total_co2_captured_ccs_energy_related",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_captured_by_sector_energy_related": 1},
)
def total_co2_captured_ccs_energy_related():
    return sum(
        co2_captured_by_sector_energy_related().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="Total_DAC_CO2_captured",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_co2_captured": 1},
)
def total_dac_co2_captured():
    return sum(dac_co2_captured().rename({"dac_tech": "dac_tech!"}), dim=["dac_tech!"])


@component.add(
    name="total_DAC_energy_demand",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand_per_sector_and_fuel": 1},
)
def total_dac_energy_demand():
    return sum(
        dac_energy_demand_per_sector_and_fuel().rename(
            {
                "dac_final_sources": "dac_final_sources!",
                "SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!",
            }
        ),
        dim=["dac_final_sources!", "SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="Total_process_emissions_captured",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"process_co2_captured_ccs": 1},
)
def total_process_emissions_captured():
    return sum(
        process_co2_captured_ccs().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )
