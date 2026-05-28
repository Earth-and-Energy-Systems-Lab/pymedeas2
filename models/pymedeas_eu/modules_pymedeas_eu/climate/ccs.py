"""
Module climate.ccs
Translated using PySD version 3.14.3
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
    units="TWh/yearf",
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
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_households",
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
    "ccs_tech_share_accommodation_food_and_beverage_services",
    {
        "SECTORS_and_HOUSEHOLDS": ["Accommodation_food_and_beverage_services"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_activities_of_membership_organisations",
    {
        "SECTORS_and_HOUSEHOLDS": ["Activities_of_membership_organisations"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_agriculture_livestock_and_related_services",
    {
        "SECTORS_and_HOUSEHOLDS": ["Agriculture_livestock_and_related_services"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_air_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Air_transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_chemical_industry",
    {
        "SECTORS_and_HOUSEHOLDS": ["Chemical_industry"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_coke_and_petroleum_refineries",
    {
        "SECTORS_and_HOUSEHOLDS": ["Coke_and_petroleum_refineries"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_computer_activities_and_information_services",
    {
        "SECTORS_and_HOUSEHOLDS": ["Computer_activities_and_information_services"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_construction",
    {
        "SECTORS_and_HOUSEHOLDS": ["Construction"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_education",
    {"SECTORS_and_HOUSEHOLDS": ["Education"], "CCS_tech": _subscript_dict["CCS_tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_electricity_gas_steam_and_air_conditioning_supply",
    {
        "SECTORS_and_HOUSEHOLDS": ["Electricity_gas_steam_and_airconditioning_supply"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_extractive_industries_mining_and_quarrying",
    {
        "SECTORS_and_HOUSEHOLDS": ["Extractive_industries_mining_and_quarrying"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_financial_intermediation",
    {
        "SECTORS_and_HOUSEHOLDS": ["Financial_intermediation"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_fishing_and_aquaculture",
    {
        "SECTORS_and_HOUSEHOLDS": ["Fishing_and_aquaculture"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_food_beverages_and_tobacco_industries",
    {
        "SECTORS_and_HOUSEHOLDS": ["Food_beverages_and_tobacco_industries"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_forestry_and_logging",
    {
        "SECTORS_and_HOUSEHOLDS": ["Forestry_and_logging"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_graphic_arts_and_recorded_media",
    {
        "SECTORS_and_HOUSEHOLDS": ["Graphic_arts_and_recorded_media"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_healthcare_and_social_work_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Healthcare_and_social_work_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_insurance_and_pension_funds",
    {
        "SECTORS_and_HOUSEHOLDS": ["Insurance_and_pension_funds"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_land_transport_pipeline_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Land_transport_pipeline_transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_computer_electronic_and_optical_products",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Manufacture_of_computer_electronic_and_optical_products"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_electrical_equipment",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_electrical_equipment"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_fabricated_metal_products_except_machinery_and_equipment",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Manufacture_of_fabricated_metal_products_except_machinery_and_equipment"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_furniture_manufacturing_n_e_c",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_furniture_manufacturing_n_e_c"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_machinery_and_equipment_n_e_c",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_machinery_and_equipment_n_e_c"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_motor_vehicles_trailers_and_semi_trailers",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Manufacture_of_motor_vehicles_trailers_and_semitrailers"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_other_non_metallic_mineral_products",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_other_nonmetallic_mineral_products"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_other_transport_equipment",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_other_transport_equipment"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_rubber_and_plastic_products",
    {
        "SECTORS_and_HOUSEHOLDS": ["Manufacture_of_rubber_and_plastic_products"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_maritime_and_inland_water_transport",
    {
        "SECTORS_and_HOUSEHOLDS": ["Maritime_and_inland_water_transport"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_metallurgy",
    {"SECTORS_and_HOUSEHOLDS": ["Metallurgy"], "CCS_tech": _subscript_dict["CCS_tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_other_business_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Other_business_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_other_personal_service_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Other_personal_service_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_paper_and_paper_products_industry",
    {
        "SECTORS_and_HOUSEHOLDS": ["Paper_and_paper_products_industry"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_postal_and_telecommunication_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Postal_and_telecommunication_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_private_households_with_employed_persons",
    {
        "SECTORS_and_HOUSEHOLDS": ["Private_households_with_employed_persons"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_public_administration_defense_and_compulsory_social_security",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Public_administration_defense_and_compulsory_social_security"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_real_estate_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Real_estate_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_recreational_cultural_and_sporting_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Recreational_cultural_and_sporting_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_rental_activities",
    {
        "SECTORS_and_HOUSEHOLDS": ["Rental_activities"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_research_and_development",
    {
        "SECTORS_and_HOUSEHOLDS": ["Research_and_development"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_retail_trade_except_motor_vehicles_and_motorcycles",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Retail_trade_except_motor_vehicles_and_motorcycles"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_sale_and_repair_of_motor_vehicles_and_motorcycles",
    {
        "SECTORS_and_HOUSEHOLDS": ["Sale_and_repair_of_motor_vehicles_and_motorcycles"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_sanitation_waste_management_and_decontamination_activities",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Sanitation_waste_management_and_decontamination_activities"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_support_activities_for_financial_intermediation_and_insurance",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Support_activities_for_financial_intermediation_and_insurance"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_textile_clothing_leather_and_footwear_industries",
    {
        "SECTORS_and_HOUSEHOLDS": ["Textile_clothing_leather_and_footwear_industries"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_warehousing_and_support_activities_for_transportation",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Warehousing_and_support_activities_for_transportation"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_water_collection_treatment_and_supply",
    {
        "SECTORS_and_HOUSEHOLDS": ["Water_collection_treatment_and_supply"],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_wholesale_trade_and_intermediation_except_motor_vehicles",
    {
        "SECTORS_and_HOUSEHOLDS": [
            "Wholesale_trade_and_intermediation_except_motor_vehicles"
        ],
        "CCS_tech": _subscript_dict["CCS_tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Europe",
    "year_ccs_tech",
    "ccs_tech_share_wood_and_cork_industry",
    {
        "SECTORS_and_HOUSEHOLDS": ["Wood_and_cork_industry"],
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
        "share_ccs_energy_related": 2,
        "time": 2,
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
    except_subs.loc[["Electricity_gas_steam_and_airconditioning_supply"]] = False
    value.values[except_subs.values] = np.minimum(
        co2_policy_captured_sector_ccs() * share_ccs_energy_related(time()),
        co2_emissions_households_and_sectors_fossil_fuels(),
    ).values[except_subs.values]
    value.loc[["Electricity_gas_steam_and_airconditioning_supply"]] = float(
        np.minimum(
            float(
                co2_policy_captured_sector_ccs().loc[
                    "Electricity_gas_steam_and_airconditioning_supply"
                ]
            )
            * float(
                share_ccs_energy_related(time()).loc[
                    "Electricity_gas_steam_and_airconditioning_supply"
                ]
            ),
            float(
                co2_emissions_households_and_sectors_fossil_fuels().loc[
                    "Electricity_gas_steam_and_airconditioning_supply"
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
        "share_ccs_energy_related": 1,
        "time": 1,
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
        "co2_captured_by_sector_energy_related": 1,
        "process_co2_captured_ccs": 1,
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


@component.add(
    name="Total_process_emissions_captured",
    units="GtCO2/year",
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
