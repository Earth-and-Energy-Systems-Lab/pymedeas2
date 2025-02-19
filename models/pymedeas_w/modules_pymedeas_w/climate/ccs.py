"""
Module climate.ccs
Translated using PySD version 3.14.0
"""

@component.add(
    name="CCS cp",
    units="Dmnl",
    subscripts=[np.str_("CCS tech")],
    comp_type="Constant",
    comp_subtype="Normal",
)
def ccs_cp():
    """
    Capacity factor of the carbon capture and storage technologies
    """
    return xr.DataArray(
        1, {"CCS tech": _subscript_dict["CCS tech"]}, [np.str_("CCS tech")]
    )


@component.add(
    name="CCS efficiency",
    units="TWh/GtCO2",
    subscripts=[np.str_("CCS tech")],
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
    {"CCS tech": _subscript_dict["CCS tech"]},
    _root,
    {"CCS tech": _subscript_dict["CCS tech"]},
    "_ext_constant_ccs_efficiency",
)


@component.add(
    name="CCS energy consumption sector",
    units="TWh/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1, "scarcity_final_fuels": 1},
)
def ccs_energy_consumption_sector():
    return ccs_energy_demand_sect() * (
        1 - float(scarcity_final_fuels().loc["electricity"])
    )


@component.add(
    name="CCS energy demand sect",
    units="TWh/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
            ccs_energy_demand_sect_tech().rename({np.str_("CCS tech"): "CCS tech!"}),
            dim=["CCS tech!"],
        )
        * share_captured_sector_delayed()
    )


@component.add(
    name="CCS energy demand sect tech",
    units="TWh/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS"), np.str_("CCS tech")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_sector_tech": 1, "ccs_cp": 1, "twe_per_twh": 1},
)
def ccs_energy_demand_sect_tech():
    return ccs_sector_tech() * ccs_cp() / twe_per_twh()


@component.add(
    name="CCS policy",
    units="TW",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    _root,
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    "_ext_lookup_ccs_policy",
)


@component.add(
    name="CCS sector tech",
    units="TW",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS"), np.str_("CCS tech")],
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
    subscripts=[np.str_("SECTORS and HOUSEHOLDS"), np.str_("CCS tech")],
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
    {"SECTORS and HOUSEHOLDS": ["Households"], "CCS tech": _subscript_dict["CCS tech"]},
    _root,
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
    "_ext_lookup_ccs_tech_share",
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_agr",
    {
        "SECTORS and HOUSEHOLDS": ["Agriculture"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_air_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Air Transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_chemical_and_petrochemical",
    {
        "SECTORS and HOUSEHOLDS": ["Chemical and Petrochemical"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coal_and_peat_mining",
    {
        "SECTORS and HOUSEHOLDS": ["Coal and Peat Mining"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_coke_oven_products",
    {
        "SECTORS and HOUSEHOLDS": ["Coke Oven Products"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_commercial_and_public_services",
    {
        "SECTORS and HOUSEHOLDS": ["Commercial and Public Services"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_construction",
    {
        "SECTORS and HOUSEHOLDS": ["Construction"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_electricity_and_heat_generation",
    {
        "SECTORS and HOUSEHOLDS": ["Electricity and Heat Generation"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_fishing",
    {"SECTORS and HOUSEHOLDS": ["Fishing"], "CCS tech": _subscript_dict["CCS tech"]},
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_food_and_tobacco",
    {
        "SECTORS and HOUSEHOLDS": ["Food and Tobacco"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_iron_and_steel",
    {
        "SECTORS and HOUSEHOLDS": ["Iron and Steel"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_land_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Land Transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_liquefaction_and_regasification_plants",
    {
        "SECTORS and HOUSEHOLDS": ["Liquefaction and Regasification Plants"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_machinery",
    {"SECTORS and HOUSEHOLDS": ["Machinery"], "CCS tech": _subscript_dict["CCS tech"]},
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_mining_and_quarrying",
    {
        "SECTORS and HOUSEHOLDS": ["Mining and Quarrying"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_non_ferrous_metals",
    {
        "SECTORS and HOUSEHOLDS": ["Non Ferrous Metals"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_non_metallic_minerals",
    {
        "SECTORS and HOUSEHOLDS": ["Non Metallic Minerals"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_nuclear_industry",
    {
        "SECTORS and HOUSEHOLDS": ["Nuclear Industry"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_oil_refineries",
    {
        "SECTORS and HOUSEHOLDS": ["Oil Refineries"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_oil_and_gas_extraction",
    {
        "SECTORS and HOUSEHOLDS": ["Oil and Gas Extraction"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_other_industry",
    {
        "SECTORS and HOUSEHOLDS": ["Other Industry"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_paper_pulp_and_print",
    {
        "SECTORS and HOUSEHOLDS": ["Paper Pulp and Print"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_pipeline_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Pipeline Transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_textile_and_leather",
    {
        "SECTORS and HOUSEHOLDS": ["Textile and Leather"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_transport_equipment",
    {
        "SECTORS and HOUSEHOLDS": ["Transport Equipment"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_water_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Water Transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "ccs_tech_share_wood_and_wood_products",
    {
        "SECTORS and HOUSEHOLDS": ["Wood and Wood Products"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)


@component.add(
    name="CO2 captured by sector energy related",
    units="GTCO2e/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 2,
        "time": 4,
        "share_ccs_energy_related": 2,
        "share_beccs": 2,
        "co2_emissions_households_and_sectors_fossil_fuels": 2,
        "co2_emissions_per_fuel": 2,
    },
)
def co2_captured_by_sector_energy_related():
    value = xr.DataArray(
        np.nan,
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        [np.str_("SECTORS and HOUSEHOLDS")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["Electricity and Heat Generation"]] = False
    value.values[except_subs.values] = np.minimum(
        co2_policy_captured_sector_ccs() * share_ccs_energy_related(time()),
        co2_emissions_households_and_sectors_fossil_fuels() * (1 + share_beccs(time())),
    ).values[except_subs.values]
    value.loc[["Electricity and Heat Generation"]] = np.minimum(
        float(co2_policy_captured_sector_ccs().loc["Electricity and Heat Generation"])
        * float(
            share_ccs_energy_related(time()).loc["Electricity and Heat Generation"]
        ),
        (
            float(
                co2_emissions_households_and_sectors_fossil_fuels().loc[
                    "Electricity and Heat Generation"
                ]
            )
            + float(co2_emissions_per_fuel().loc["electricity"])
            + float(co2_emissions_per_fuel().loc["heat"])
        )
        * (1 + share_beccs(time())),
    )
    return value


@component.add(
    name="CO2 emissions households and sectors fossil fuels",
    units="GTCO2e/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors_before_ccs": 1},
)
def co2_emissions_households_and_sectors_fossil_fuels():
    return sum(
        co2_emissions_households_and_sectors_before_ccs()
        .loc[_subscript_dict["matter final sources"], :]
        .rename({np.str_("final sources"): "matter final sources!"}),
        dim=["matter final sources!"],
    )


@component.add(
    name="CO2 policy capture sector tech CCS",
    units="GtCO2/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS"), np.str_("CCS tech")],
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
    name="CO2 policy captured sector CCS",
    units="GtCO2/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_policy_capture_sector_tech_ccs": 1, "scarcity_final_fuels": 1},
)
def co2_policy_captured_sector_ccs():
    """
    CO2 captured by each sector with CCS technologies developed. TODO: only a share of the emissions can be captured according to the implemented technology.
    """
    return sum(
        co2_policy_capture_sector_tech_ccs().rename({np.str_("CCS tech"): "CCS tech!"}),
        dim=["CCS tech!"],
    ) * (1 - float(scarcity_final_fuels().loc["electricity"]))


@component.add(
    name="DAC CO2 captured",
    units="GTCO2e/year",
    subscripts=[np.str_("dac tech")],
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
    name="DAC efficiency",
    units="TWh/GtCO2",
    subscripts=[np.str_("dac tech"), np.str_("dac final sources")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_dac_efficiency"},
)
def dac_efficiency():
    return _ext_constant_dac_efficiency()


_ext_constant_dac_efficiency = ExtConstant(
    "../climate.xlsx",
    "Global",
    "dac_efficiency",
    {
        "dac tech": _subscript_dict["dac tech"],
        "dac final sources": _subscript_dict["dac final sources"],
    },
    _root,
    {
        "dac tech": _subscript_dict["dac tech"],
        "dac final sources": _subscript_dict["dac final sources"],
    },
    "_ext_constant_dac_efficiency",
)


@component.add(
    name="DAC energy consumption by sector and fuel",
    units="TWh/year",
    subscripts=[np.str_("dac final sources"), np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand_per_sector_and_fuel": 1, "scarcity_final_fuels": 1},
)
def dac_energy_consumption_by_sector_and_fuel():
    return dac_energy_demand_per_sector_and_fuel() * (
        1
        - scarcity_final_fuels()
        .loc[_subscript_dict["dac final sources"]]
        .rename({np.str_("final sources"): "dac final sources"})
    )


@component.add(
    name="DAC energy demand",
    units="TWh/year",
    subscripts=[np.str_("dac tech"), np.str_("dac final sources")],
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
            "dac tech": _subscript_dict["dac tech"],
            "dac final sources": _subscript_dict["dac final sources"],
        },
        [np.str_("dac tech"), np.str_("dac final sources")],
    )
    value.loc[:, ["heat"]] = (
        (dac_per_tech() / twe_per_twh() * share_heat_vs_electricity_in_dac_per_tech())
        .expand_dims({"dac final sources": ["heat"]}, 1)
        .values
    )
    value.loc[:, ["electricity"]] = (
        (dac_per_tech() / twe_per_twh())
        .expand_dims({"dac final sources": ["electricity"]}, 1)
        .values
    )
    return value


@component.add(
    name="DAC energy demand per sector and fuel",
    units="TWh/year",
    subscripts=[np.str_("dac final sources"), np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand": 1, "share_fed_by_sector_delayed": 1},
)
def dac_energy_demand_per_sector_and_fuel():
    return (
        sum(
            dac_energy_demand().rename({np.str_("dac tech"): "dac tech!"}),
            dim=["dac tech!"],
        )
        * share_fed_by_sector_delayed()
    )


@component.add(
    name="DAC per tech",
    units="TW",
    subscripts=[np.str_("dac tech")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "dac_policy_electricity": 1, "dac_tech_share": 1},
)
def dac_per_tech():
    return dac_policy_electricity(time()) * dac_tech_share(time())


@component.add(
    name="DAC policy electricity",
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
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_DAC",
    {},
    _root,
    {},
    "_ext_lookup_dac_policy_electricity",
)


@component.add(
    name="DAC tech share",
    units="Dmnl",
    subscripts=[np.str_("dac tech")],
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
    "../climate.xlsx",
    "World",
    "year_ccs_tech",
    "dac_tech_share",
    {"dac tech": _subscript_dict["dac tech"]},
    _root,
    {"dac tech": _subscript_dict["dac tech"]},
    "_ext_lookup_dac_tech_share",
)


@component.add(
    name="Overcapacity CCS process",
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
                {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        ),
        lambda: zidz(
            sum(
                process_co2_captured_ccs().rename(
                    {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
                ),
                dim=["SECTORS and HOUSEHOLDS!"],
            ),
            total_process_emissions(),
        )
        - 1,
        lambda: 0,
    )


@component.add(
    name="process CO2 captured CCS",
    units="GTCO2e/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
    name="share BECCS",
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
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_BECCS",
    {},
    _root,
    {},
    "_ext_lookup_share_beccs",
)


@component.add(
    name="share captured sector",
    units="Dmnl",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
            {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
            ["SECTORS and HOUSEHOLDS"],
        ),
        lambda: zidz(
            co2_captured_by_sector_energy_related() + process_co2_captured_ccs(),
            co2_policy_captured_sector_ccs(),
        ),
    )


@component.add(
    name="share captured sector delayed",
    units="percent",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    ),
    time_step,
    "_delayfixed_share_captured_sector_delayed",
)


@component.add(
    name="share CCS energy related",
    units="Dmnl",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_ccs_energy",
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    _root,
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    "_ext_lookup_share_ccs_energy_related",
)


@component.add(
    name="share fed by sector delayed",
    units="percent",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
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
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    ),
    time_step,
    "_delayfixed_share_fed_by_sector_delayed",
)


@component.add(
    name="share heat vs electricity in DAC per tech",
    units="1",
    subscripts=[np.str_("dac tech")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_efficiency": 2},
)
def share_heat_vs_electricity_in_dac_per_tech():
    return dac_efficiency().loc[:, "heat"].reset_coords(
        drop=True
    ) / dac_efficiency().loc[:, "electricity"].reset_coords(drop=True)


@component.add(
    name="tot ccs",
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
                {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        )
        + total_co2_captured_ccs_energy_related()
    )


@component.add(
    name="total CCS energy demand",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1},
)
def total_ccs_energy_demand():
    return sum(
        ccs_energy_demand_sect().rename(
            {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="Total co2 captured",
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
                {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        )
    )


@component.add(
    name="total CO2 captured CCS",
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
            {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="total co2 captured ccs energy related",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_captured_by_sector_energy_related": 1},
)
def total_co2_captured_ccs_energy_related():
    return sum(
        co2_captured_by_sector_energy_related().rename(
            {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="Total DAC CO2 captured",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_co2_captured": 1},
)
def total_dac_co2_captured():
    return sum(
        dac_co2_captured().rename({np.str_("dac tech"): "dac tech!"}), dim=["dac tech!"]
    )


@component.add(
    name="total DAC energy demand",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand_per_sector_and_fuel": 1},
)
def total_dac_energy_demand():
    return sum(
        dac_energy_demand_per_sector_and_fuel().rename(
            {
                np.str_("dac final sources"): "dac final sources!",
                np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!",
            }
        ),
        dim=["dac final sources!", "SECTORS and HOUSEHOLDS!"],
    )
