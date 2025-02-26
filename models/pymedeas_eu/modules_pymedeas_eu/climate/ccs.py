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
    units="GtCO2/TWh",
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
    r"../../scenarios/scen_eu.xlsx",
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
    r"../climate.xlsx",
    "Europe",
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
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_agr",
    {
        "SECTORS_and_HOUSEHOLDS": ["Agriculture"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_mqes",
    {
        "SECTORS_and_HOUSEHOLDS": ["Mining_quarrying_and_energy_supply"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_fbt",
    {
        "SECTORS_and_HOUSEHOLDS": ["Food_Beverages_and_Tobacco"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_tex",
    {
        "SECTORS_and_HOUSEHOLDS": ["Textiles_and_leather_etc"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
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
    r"../climate.xlsx",
    "Europe",
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
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_om",
    {
        "SECTORS_and_HOUSEHOLDS": ["Other_manufacturing"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_cons",
    {
        "SECTORS_and_HOUSEHOLDS": ["Construction"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_dist",
    {
        "SECTORS_and_HOUSEHOLDS": ["Distribution"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_hr",
    {
        "SECTORS_and_HOUSEHOLDS": ["Hotels_and_restaurant"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_tsc",
    {
        "SECTORS_and_HOUSEHOLDS": ["Transport_storage_and_communication"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_fi",
    {
        "SECTORS_and_HOUSEHOLDS": ["Financial_Intermediation"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_re",
    {
        "SECTORS_and_HOUSEHOLDS": ["Real_estate_renting_and_busine_activitie"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_nms",
    {
        "SECTORS_and_HOUSEHOLDS": ["Non_Market_Service"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)


@component.add(
    name="CO2_captured_by_sector_energy_related",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 2,
        "time": 2,
        "share_ccs_energy_related": 2,
        "co2_emissions_households_and_sectors_fossil_fuels": 2,
        "co2_emissions_per_fuel": 2,
    },
)
def co2_captured_by_sector_energy_related():
    """
    energy-related co2 emissions
    """
    value = xr.DataArray(
        np.nan,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["Mining_quarrying_and_energy_supply"]] = False
    value.values[except_subs.values] = np.minimum(
        co2_policy_captured_sector_ccs() * share_ccs_energy_related(time()),
        co2_emissions_households_and_sectors_fossil_fuels(),
    ).values[except_subs.values]
    value.loc[["Mining_quarrying_and_energy_supply"]] = float(
        np.minimum(
            float(
                co2_policy_captured_sector_ccs().loc[
                    "Mining_quarrying_and_energy_supply"
                ]
            )
            * float(
                share_ccs_energy_related(time()).loc[
                    "Mining_quarrying_and_energy_supply"
                ]
            ),
            float(
                co2_emissions_households_and_sectors_fossil_fuels().loc[
                    "Mining_quarrying_and_energy_supply"
                ]
            )
            + float(co2_emissions_per_fuel().loc["electricity"])
            + float(co2_emissions_per_fuel().loc["heat"]),
        )
    )
    return value


@component.add(
    name="CO2_captured_sector_tech_CCS",
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
def co2_captured_sector_tech_ccs():
    return ccs_sector_tech() * ccs_cp() / twe_per_twh() / ccs_efficiency()


@component.add(
    name="CO2_emissions_households_and_sectors_fossil_fuels",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors_before_ccs": 1},
)
def co2_emissions_households_and_sectors_fossil_fuels():
    """
    CO2 emissions comming from fossil fuel combustion
    """
    return sum(
        co2_emissions_households_and_sectors_before_ccs()
        .loc[_subscript_dict["matter_final_sources"], :]
        .rename({"final_sources": "matter_final_sources!"}),
        dim=["matter_final_sources!"],
    )


@component.add(
    name="CO2_policy_captured_sector_CCS",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_captured_sector_tech_ccs": 1, "scarcity_final_fuels": 1},
)
def co2_policy_captured_sector_ccs():
    """
    CO2 captured by each sector with CCS technologies developed.
    """
    return sum(
        co2_captured_sector_tech_ccs().rename({"CCS_tech": "CCS_tech!"}),
        dim=["CCS_tech!"],
    ) * (1 - float(scarcity_final_fuels().loc["electricity"]))


@component.add(
    name="DAC_CO2_captured",
    units="GtCO2/year",
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
    name="DAC_CO2_captured_energy_per_sector",
    units="GtCO2/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_co2_captured_energy_related": 1, "share_fed_by_sector": 1},
)
def dac_co2_captured_energy_per_sector():
    return dac_co2_captured_energy_related() * share_fed_by_sector()


@component.add(
    name="DAC_CO2_captured_energy_related",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_dac_co2_captured": 1, "share_energy_related_average": 1},
)
def dac_co2_captured_energy_related():
    return total_dac_co2_captured() * share_energy_related_average()


@component.add(
    name="DAC_CO2_captured_process",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_dac_co2_captured": 1, "share_energy_related_average": 1},
)
def dac_co2_captured_process():
    return total_dac_co2_captured() * (1 - share_energy_related_average())


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
    value.loc[:, ["electricity"]] = (
        (dac_per_tech() / twe_per_twh())
        .expand_dims({"final_sources": ["electricity"]}, 1)
        .values
    )
    value.loc[:, ["heat"]] = (
        (dac_per_tech() / twe_per_twh() * share_heat_vs_electricity_in_dac_per_tech())
        .expand_dims({"final_sources": ["heat"]}, 1)
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
    r"../../scenarios/scen_eu.xlsx",
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
    "Europe",
    "year_ccs_tech",
    "dac_tech_share",
    {"dac_tech": _subscript_dict["dac_tech"]},
    _root,
    {"dac_tech": _subscript_dict["dac_tech"]},
    "_ext_lookup_dac_tech_share",
)


@component.add(
    name="process_CO2_captured_CCS",
    units="GtCO2/year",
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
    share of carbon captured that is not captured due to the fact that it has absorbed all the co2 (energy-related) emited by the sector.
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
    """
    Share of the carbon capture capacity absorbing CO2 energy related emissions
    """
    return _ext_lookup_share_ccs_energy_related(x, final_subs)


_ext_lookup_share_ccs_energy_related = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_RES_power",
    "share_ccs_energy",
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    _root,
    {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
    "_ext_lookup_share_ccs_energy_related",
)


@component.add(
    name="share_energy_related_average",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "share_ccs_energy_related": 1},
)
def share_energy_related_average():
    return (
        sum(
            share_ccs_energy_related(time()).rename(
                {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        )
        / 15
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
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_captured_ccs": 1, "total_dac_co2_captured": 1},
)
def total_co2_captured():
    return total_co2_captured_ccs() + total_dac_co2_captured()


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
    name="Total_DAC_CO2_captured",
    units="GtCO2/year",
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
    name="total_energy_demand_sector_CCS",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect": 1},
)
def total_energy_demand_sector_ccs():
    return sum(
        ccs_energy_demand_sect().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )
