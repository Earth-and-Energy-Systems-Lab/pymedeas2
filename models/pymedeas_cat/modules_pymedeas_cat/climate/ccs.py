"""
Module climate.ccs
Translated using PySD version 3.14.3
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
    return xr.DataArray(0.9, {"CCS tech": _subscript_dict["CCS tech"]}, ["CCS tech"])


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
    return ccs_energy_demand_sect() * (
        1 - float(scarcity_final_fuels().loc["electricity"])
    )


@component.add(
    name="CCS energy demand sect",
    units="TWh/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_energy_demand_sect_tech": 1, "share_captured_delayed": 1},
)
def ccs_energy_demand_sect():
    """
    Total energy demand for CCS (electricity) by sector
    """
    return (
        sum(
            ccs_energy_demand_sect_tech().rename({"CCS tech": "CCS tech!"}),
            dim=["CCS tech!"],
        )
        * share_captured_delayed()
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
    """
    Energy demand for CCS by sector and technology
    """
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
    r"../../scenarios/scen_cat.xlsx",
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
    depends_on={"time": 3, "ccs_tech_share": 1, "ccs_policy": 1},
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
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_households",
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
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_accommodation_food_and_beverage_services",
    {
        "SECTORS and HOUSEHOLDS": ["Accommodation food and beverage services"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_activities_of_membership_organisations",
    {
        "SECTORS and HOUSEHOLDS": ["Activities of membership organisations"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_agriculture_livestock_and_related_services",
    {
        "SECTORS and HOUSEHOLDS": ["Agriculture livestock and related services"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_air_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Air transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_chemical_industry",
    {
        "SECTORS and HOUSEHOLDS": ["Chemical industry"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_coke_and_petroleum_refineries",
    {
        "SECTORS and HOUSEHOLDS": ["Coke and petroleum refineries"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_computer_activities_and_information_services",
    {
        "SECTORS and HOUSEHOLDS": ["Computer activities and information services"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_construction",
    {
        "SECTORS and HOUSEHOLDS": ["Construction"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_education",
    {"SECTORS and HOUSEHOLDS": ["Education"], "CCS tech": _subscript_dict["CCS tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_electricity_gas_steam_and_air_conditioning_supply",
    {
        "SECTORS and HOUSEHOLDS": ["Electricity gas steam and airconditioning supply"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_extractive_industries_mining_and_quarrying",
    {
        "SECTORS and HOUSEHOLDS": ["Extractive industries mining and quarrying"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_financial_intermediation",
    {
        "SECTORS and HOUSEHOLDS": ["Financial intermediation"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_fishing_and_aquaculture",
    {
        "SECTORS and HOUSEHOLDS": ["Fishing and aquaculture"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_food_beverages_and_tobacco_industries",
    {
        "SECTORS and HOUSEHOLDS": ["Food beverages and tobacco industries"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_forestry_and_logging",
    {
        "SECTORS and HOUSEHOLDS": ["Forestry and logging"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_graphic_arts_and_recorded_media",
    {
        "SECTORS and HOUSEHOLDS": ["Graphic arts and recorded media"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_healthcare_and_social_work_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Healthcare and social work activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_insurance_and_pension_funds",
    {
        "SECTORS and HOUSEHOLDS": ["Insurance and pension funds"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_land_transport_pipeline_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Land transport pipeline transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_computer_electronic_and_optical_products",
    {
        "SECTORS and HOUSEHOLDS": [
            "Manufacture of computer electronic and optical products"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_electrical_equipment",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of electrical equipment"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_fabricated_metal_products_except_machinery_and_equipment",
    {
        "SECTORS and HOUSEHOLDS": [
            "Manufacture of fabricated metal products except machinery and equipment"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_furniture_manufacturing_n_e_c",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of furniture manufacturing n e c"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_machinery_and_equipment_n_e_c",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of machinery and equipment n e c"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_motor_vehicles_trailers_and_semi_trailers",
    {
        "SECTORS and HOUSEHOLDS": [
            "Manufacture of motor vehicles trailers and semitrailers"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_other_non_metallic_mineral_products",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of other nonmetallic mineral products"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_other_transport_equipment",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of other transport equipment"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_manufacture_of_rubber_and_plastic_products",
    {
        "SECTORS and HOUSEHOLDS": ["Manufacture of rubber and plastic products"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_maritime_and_inland_water_transport",
    {
        "SECTORS and HOUSEHOLDS": ["Maritime and inland water transport"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_metallurgy",
    {"SECTORS and HOUSEHOLDS": ["Metallurgy"], "CCS tech": _subscript_dict["CCS tech"]},
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_other_business_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Other business activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_other_personal_service_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Other personal service activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_paper_and_paper_products_industry",
    {
        "SECTORS and HOUSEHOLDS": ["Paper and paper products industry"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_postal_and_telecommunication_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Postal and telecommunication activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_private_households_with_employed_persons",
    {
        "SECTORS and HOUSEHOLDS": ["Private households with employed persons"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_public_administration_defense_and_compulsory_social_security",
    {
        "SECTORS and HOUSEHOLDS": [
            "Public administration defense and compulsory social security"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_real_estate_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Real estate activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_recreational_cultural_and_sporting_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Recreational cultural and sporting activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_rental_activities",
    {
        "SECTORS and HOUSEHOLDS": ["Rental activities"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_research_and_development",
    {
        "SECTORS and HOUSEHOLDS": ["Research and development"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_retail_trade_except_motor_vehicles_and_motorcycles",
    {
        "SECTORS and HOUSEHOLDS": [
            "Retail trade except motor vehicles and motorcycles"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_sale_and_repair_of_motor_vehicles_and_motorcycles",
    {
        "SECTORS and HOUSEHOLDS": ["Sale and repair of motor vehicles and motorcycles"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_sanitation_waste_management_and_decontamination_activities",
    {
        "SECTORS and HOUSEHOLDS": [
            "Sanitation waste management and decontamination activities"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_support_activities_for_financial_intermediation_and_insurance",
    {
        "SECTORS and HOUSEHOLDS": [
            "Support activities for financial intermediation and insurance"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_textile_clothing_leather_and_footwear_industries",
    {
        "SECTORS and HOUSEHOLDS": ["Textile clothing leather and footwear industries"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_warehousing_and_support_activities_for_transportation",
    {
        "SECTORS and HOUSEHOLDS": [
            "Warehousing and support activities for transportation"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_water_collection_treatment_and_supply",
    {
        "SECTORS and HOUSEHOLDS": ["Water collection treatment and supply"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_wholesale_trade_and_intermediation_except_motor_vehicles",
    {
        "SECTORS and HOUSEHOLDS": [
            "Wholesale trade and intermediation except motor vehicles"
        ],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)

_ext_lookup_ccs_tech_share.add(
    r"../climate.xlsx",
    "Catalonia",
    "year_ccs_tech",
    "ccs_tech_share_wood_and_cork_industry",
    {
        "SECTORS and HOUSEHOLDS": ["Wood and cork industry"],
        "CCS tech": _subscript_dict["CCS tech"],
    },
)


@component.add(
    name="CO2 captured by sector energy related",
    subscripts=["SECTORS and HOUSEHOLDS"],
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
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["Electricity gas steam and airconditioning supply"]] = False
    value.values[except_subs.values] = np.minimum(
        co2_policy_captured_sector_ccs() * share_ccs_energy_related(time()),
        co2_emissions_households_and_sectors_fossil_fuels(),
    ).values[except_subs.values]
    value.loc[["Electricity gas steam and airconditioning supply"]] = float(
        np.minimum(
            float(
                co2_policy_captured_sector_ccs().loc[
                    "Electricity gas steam and airconditioning supply"
                ]
            )
            * float(
                share_ccs_energy_related(time()).loc[
                    "Electricity gas steam and airconditioning supply"
                ]
            ),
            float(
                co2_emissions_households_and_sectors_fossil_fuels().loc[
                    "Electricity gas steam and airconditioning supply"
                ]
            )
            + float(co2_emissions_per_fuel().loc["electricity"])
            + float(co2_emissions_per_fuel().loc["heat"]),
        )
    )
    return value


@component.add(
    name="CO2 captured sector tech CCS",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS", "CCS tech"],
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
    """
    Policy of carbon capture per sector
    """
    return ccs_sector_tech() * ccs_cp() / twe_per_twh() / ccs_efficiency()


@component.add(
    name="CO2 emissions households and sectors fossil fuels",
    units="GtCO2/year",
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
    name="CO2 policy captured sector CCS",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_captured_sector_tech_ccs": 1, "scarcity_final_fuels": 1},
)
def co2_policy_captured_sector_ccs():
    """
    CO2 captured by each sector with CCS technologies developed.
    """
    return sum(
        co2_captured_sector_tech_ccs().rename({"CCS tech": "CCS tech!"}),
        dim=["CCS tech!"],
    ) * (1 - float(scarcity_final_fuels().loc["electricity"]))


@component.add(
    name="DAC CO2 captured",
    units="GtCO2/year",
    subscripts=["dac tech"],
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
    name="DAC CO2 captured energy per sector",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_co2_captured_energy_related": 1, "share_fed_by_sector": 1},
)
def dac_co2_captured_energy_per_sector():
    return dac_co2_captured_energy_related() * share_fed_by_sector()


@component.add(
    name="DAC CO2 captured energy related",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_dac_co2_captured": 1, "share_energy_related_average": 1},
)
def dac_co2_captured_energy_related():
    return total_dac_co2_captured() * share_energy_related_average()


@component.add(
    name="DAC CO2 captured process",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_dac_co2_captured": 1, "share_energy_related_average": 1},
)
def dac_co2_captured_process():
    return total_dac_co2_captured() * (1 - share_energy_related_average())


@component.add(
    name="DAC efficiency",
    units="TWh/GtCO2",
    subscripts=["dac tech", "dac final sources"],
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
    subscripts=["dac final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand_per_sector_and_fuel": 1, "scarcity_final_fuels": 1},
)
def dac_energy_consumption_by_sector_and_fuel():
    return dac_energy_demand_per_sector_and_fuel() * (
        1
        - scarcity_final_fuels()
        .loc[_subscript_dict["dac final sources"]]
        .rename({"final sources": "dac final sources"})
    )


@component.add(
    name="DAC energy demand",
    units="TWh/year",
    subscripts=["dac tech", "dac final sources"],
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
        ["dac tech", "dac final sources"],
    )
    value.loc[:, ["electricity"]] = (
        (dac_per_tech() / twe_per_twh())
        .expand_dims({"dac final sources": ["electricity"]}, 1)
        .values
    )
    value.loc[:, ["heat"]] = (
        (dac_per_tech() / twe_per_twh() * share_heat_vs_electricity_in_dac_per_tech())
        .expand_dims({"dac final sources": ["heat"]}, 1)
        .values
    )
    return value


@component.add(
    name="DAC energy demand per sector and fuel",
    units="TWh/year",
    subscripts=["dac final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_energy_demand": 1, "share_fed_by_sector_delayed": 1},
)
def dac_energy_demand_per_sector_and_fuel():
    return (
        sum(dac_energy_demand().rename({"dac tech": "dac tech!"}), dim=["dac tech!"])
        * share_fed_by_sector_delayed()
    )


@component.add(
    name="DAC per tech",
    units="TW",
    subscripts=["dac tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "dac_policy_electricity": 1, "dac_tech_share": 1},
)
def dac_per_tech():
    """
    TW electric of each technology of DACC
    """
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
    r"../../scenarios/scen_cat.xlsx",
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
    subscripts=["dac tech"],
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
    "Catalonia",
    "year_ccs_tech",
    "dac_tech_share",
    {"dac tech": _subscript_dict["dac tech"]},
    _root,
    {"dac tech": _subscript_dict["dac tech"]},
    "_ext_lookup_dac_tech_share",
)


@component.add(
    name="process CO2 captured CCS",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_policy_captured_sector_ccs": 1,
        "time": 1,
        "share_ccs_energy_related": 1,
    },
)
def process_co2_captured_ccs():
    return co2_policy_captured_sector_ccs() * (1 - share_ccs_energy_related(time()))


@component.add(
    name="share captured delayed",
    units="percent",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_share_captured_delayed": 1},
    other_deps={
        "_delayfixed_share_captured_delayed": {
            "initial": {"time_step": 1},
            "step": {"share_captured_sector": 1},
        }
    },
)
def share_captured_delayed():
    return _delayfixed_share_captured_delayed()


_delayfixed_share_captured_delayed = DelayFixed(
    lambda: share_captured_sector(),
    lambda: time_step(),
    lambda: xr.DataArray(
        1,
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    ),
    time_step,
    "_delayfixed_share_captured_delayed",
)


@component.add(
    name="share captured sector",
    units="Dmnl",
    subscripts=["SECTORS and HOUSEHOLDS"],
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
    share of co2 that is captured
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
    name="share CCS energy related",
    units="Dmnl",
    subscripts=["SECTORS and HOUSEHOLDS"],
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "share_ccs_energy",
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    _root,
    {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
    "_ext_lookup_share_ccs_energy_related",
)


@component.add(
    name="share energy related average",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "share_ccs_energy_related": 1},
)
def share_energy_related_average():
    return (
        sum(
            share_ccs_energy_related(time()).rename(
                {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        )
        / 15
    )


@component.add(
    name="share fed by sector delayed",
    units="percent",
    subscripts=["SECTORS and HOUSEHOLDS"],
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
    subscripts=["dac tech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_efficiency": 2},
)
def share_heat_vs_electricity_in_dac_per_tech():
    return dac_efficiency().loc[:, "heat"].reset_coords(
        drop=True
    ) / dac_efficiency().loc[:, "electricity"].reset_coords(drop=True)


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
            {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
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
            {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="Total DAC CO2 captured",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dac_co2_captured": 1},
)
def total_dac_co2_captured():
    return sum(dac_co2_captured().rename({"dac tech": "dac tech!"}), dim=["dac tech!"])


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
                "dac final sources": "dac final sources!",
                "SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!",
            }
        ),
        dim=["dac final sources!", "SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="Total process CO2 captured",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"process_co2_captured_ccs": 1, "dac_co2_captured_process": 1},
)
def total_process_co2_captured():
    """
    Total process emissions (CO2) captured by CCS and DACC
    """
    return (
        sum(
            process_co2_captured_ccs().rename(
                {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        )
        + dac_co2_captured_process()
    )
