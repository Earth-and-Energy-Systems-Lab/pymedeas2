"""
Module environment.land.land_use
Translated using PySD version 3.14.2
"""

@component.add(
    name="Agricultural_land",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_agricultural_land": 1},
    other_deps={
        "_integ_agricultural_land": {
            "initial": {"initial_agricultural_area": 1},
            "step": {
                "deforestation_rate": 1,
                "forest_loss_to_sustain_agriculture": 1,
                "increase_agricultural_land": 1,
                "compet_land_for_biofuels_rate": 1,
                "urban_land_rate": 1,
            },
        }
    },
)
def agricultural_land():
    """
    Agricultural land includes both categories from FAOSTAT: "Arable land and Permanent crops" and "Permanent pastures".
    """
    return _integ_agricultural_land()


_integ_agricultural_land = Integ(
    lambda: deforestation_rate()
    + forest_loss_to_sustain_agriculture()
    + increase_agricultural_land()
    - compet_land_for_biofuels_rate()
    - urban_land_rate(),
    lambda: initial_agricultural_area(),
    "_integ_agricultural_land",
)


@component.add(
    name="agricultural_land_until_2015",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_agricultural_land_until_2015": 1},
    other_deps={
        "_sampleiftrue_agricultural_land_until_2015": {
            "initial": {"agricultural_land": 1},
            "step": {"time": 1, "agricultural_land": 1},
        }
    },
)
def agricultural_land_until_2015():
    """
    Agricultural land in EU until the year 2015. From that year, this variable reports the value of agricultural land in 2015.
    """
    return _sampleiftrue_agricultural_land_until_2015()


_sampleiftrue_agricultural_land_until_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: agricultural_land(),
    lambda: agricultural_land(),
    "_sampleiftrue_agricultural_land_until_2015",
)


@component.add(
    name="aux_reach_available_land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"available_land": 1},
)
def aux_reach_available_land():
    """
    This variable = 0 when there is no more land available.
    """
    return np.interp(
        available_land(),
        [-1.0e-02, 0.0e00, 1.0e-08, 1.0e-04, 1.0e-02, 1.0e00, 1.0e02],
        [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
    )


@component.add(
    name="\"'Available'_forest_area\"",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_available_forest_area": 1},
    other_deps={
        "_integ_available_forest_area": {
            "initial": {"initial_available_forest_area": 1},
            "step": {
                "deforestation_rate": 1,
                "forest_loss_to_sustain_agriculture": 1,
                "available_to_primary_forest_rate": 1,
            },
        }
    },
)
def available_forest_area():
    """
    Used forests, removing primary forest which are not used for wood extraction
    """
    return _integ_available_forest_area()


_integ_available_forest_area = Integ(
    lambda: -deforestation_rate()
    - forest_loss_to_sustain_agriculture()
    - available_to_primary_forest_rate(),
    lambda: initial_available_forest_area(),
    "_integ_available_forest_area",
)


@component.add(
    name="\"'Available_land'\"",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_available_land": 1},
    other_deps={
        "_integ_available_land": {
            "initial": {"initial_available_land": 1},
            "step": {
                "land_for_res_elec_rate": 1,
                "increase_agricultural_land": 1,
                "marginal_land_for_biofuels_rate": 1,
            },
        }
    },
)
def available_land():
    """
    "Available land" as defined in MEDEAS-EU framework, representing the terrestrial land that is currently neither being used by the primary sector (arable land, permanent crops, permanent meadows and pastures and productive forest area) nor built-up, nor occupied by permanent snows&glaciers.
    """
    return _integ_available_land()


_integ_available_land = Integ(
    lambda: -land_for_res_elec_rate()
    - increase_agricultural_land()
    - marginal_land_for_biofuels_rate(),
    lambda: initial_available_land(),
    "_integ_available_land",
)


@component.add(
    name="\"'Available'_to_primary_forest_rate\"",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "hist_variation_primary_forest": 1,
        "primary_forests_area": 2,
        "start_year_p_variation_primary_forest": 1,
        "p_variation_primary_forest": 1,
        "historic_av_variation_primary_forests_area": 1,
    },
)
def available_to_primary_forest_rate():
    """
    Rate of variation of the area occupied by primary forests.
    """
    return if_then_else(
        time() < 2014,
        lambda: hist_variation_primary_forest(),
        lambda: if_then_else(
            time() < start_year_p_variation_primary_forest(),
            lambda: historic_av_variation_primary_forests_area()
            * primary_forests_area(),
            lambda: p_variation_primary_forest() * primary_forests_area(),
        ),
    )


@component.add(
    name="Compet_agricultural_land_for_biofuels",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_compet_agricultural_land_for_biofuels": 1},
    other_deps={
        "_integ_compet_agricultural_land_for_biofuels": {
            "initial": {"initial_value_land_compet_biofuels_2gen_mha": 1},
            "step": {"compet_land_for_biofuels_rate": 1},
        }
    },
)
def compet_agricultural_land_for_biofuels():
    """
    Biofuels plantation on land subject to competition with other agricultural uses.
    """
    return _integ_compet_agricultural_land_for_biofuels()


_integ_compet_agricultural_land_for_biofuels = Integ(
    lambda: compet_land_for_biofuels_rate(),
    lambda: initial_value_land_compet_biofuels_2gen_mha(),
    "_integ_compet_agricultural_land_for_biofuels",
)


@component.add(
    name="compet_land_for_biofuels_rate",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_biofuels_2gen_land_compet": 1},
)
def compet_land_for_biofuels_rate():
    """
    Biofuels plantation rate on land subject to competition with other agricultural uses.
    """
    return new_biofuels_2gen_land_compet()


@component.add(
    name="consum_forest_energy_non_traditional_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_forest_energy_non_tradition_ej": 1,
        "consum_forest_energy_traditional_ej": 1,
        "consum_wood_products_ej": 1,
        "forest_consumption_ej": 1,
    },
)
def consum_forest_energy_non_traditional_ej():
    """
    Part of the forest biomass extration that goes into non energy uses. P wood-energy uses divides the possible extration into the two uses. Traditional biomass is not restricted
    """
    return float(
        np.minimum(
            demand_forest_energy_non_tradition_ej(),
            forest_consumption_ej()
            - consum_forest_energy_traditional_ej()
            - consum_wood_products_ej(),
        )
    )


@component.add(
    name="consum_forest_energy_traditional_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_consumption_ej": 1, "demand_forest_energy_traditional_ej": 1},
)
def consum_forest_energy_traditional_ej():
    """
    Consumption of traditional biomass. Traditional wood extraction is got priority over other uses but is limited by forest extraction, which depends on the stock and the policies taken to protect forests.
    """
    return float(
        np.minimum(forest_consumption_ej(), demand_forest_energy_traditional_ej())
    )


@component.add(
    name="consum_wood_products_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_wood_products_ej": 1,
        "consum_forest_energy_traditional_ej": 1,
        "forest_consumption_ej": 1,
    },
)
def consum_wood_products_ej():
    """
    Priority to energy uses Part of the forest biomass extration that goes into non energy uses. P wood/energy uses divides the possible extration into the two uses. Traditional uses are not restricted
    """
    return float(
        np.minimum(
            demand_wood_products_ej(),
            forest_consumption_ej() - consum_forest_energy_traditional_ej(),
        )
    )


@component.add(
    name="deficit_forest_biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_sustainable_forest_extraction_ej": 2,
        "total_demand_forest_biomass_ej": 3,
    },
)
def deficit_forest_biomass():
    """
    Percent of deficit of forest biomass, in terms of forest extraction demand. If maximun extration is greater than demand it is 0
    """
    return if_then_else(
        max_sustainable_forest_extraction_ej() > total_demand_forest_biomass_ej(),
        lambda: 0,
        lambda: (
            total_demand_forest_biomass_ej() - max_sustainable_forest_extraction_ej()
        )
        / total_demand_forest_biomass_ej(),
    )


@component.add(
    name="deficit_wood_products",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_wood_products_ej": 2, "consum_wood_products_ej": 1},
)
def deficit_wood_products():
    """
    Percent of the demand of wood products that cannot be met. I should influence the corresponding economic sector but it does not
    """
    return (
        demand_wood_products_ej() - consum_wood_products_ej()
    ) / demand_wood_products_ej()


@component.add(
    name="Deforestation_rate",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_forest_area": 1,
        "p_minimum_forest": 1,
        "unsustainable_loggin": 1,
    },
)
def deforestation_rate():
    """
    Forest land deforestation rate due to unsustainable loggin and converted to agriculture uses.
    """
    return if_then_else(
        available_forest_area() > p_minimum_forest(),
        lambda: unsustainable_loggin(),
        lambda: 0,
    )


@component.add(
    name="demand_forest_energy_non_tradition_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solid_bioe_emissions_relevant_ej": 1,
        "pe_bioe_residues_nonbiofuels": 1,
    },
)
def demand_forest_energy_non_tradition_ej():
    """
    Demand of forest products for energy uses in non traditional uses, in terms of energy. Residuals and traditional biomass not included.
    """
    return float(
        np.maximum(
            0, solid_bioe_emissions_relevant_ej() - pe_bioe_residues_nonbiofuels()
        )
    )


@component.add(
    name="demand_forest_energy_traditional_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_traditional_biomass_demand_ej": 1},
)
def demand_forest_energy_traditional_ej():
    """
    Demand of tradition biomass in terms of EJ
    """
    return pe_traditional_biomass_demand_ej()


@component.add(
    name="demand_forest_wood_products_pc",
    units="m3/(year*people)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_demand_forest_wood_products_pc"},
)
def demand_forest_wood_products_pc():
    """
    Demand of forest non energy products per capita, data FAO2016
    """
    return _ext_constant_demand_forest_wood_products_pc()


_ext_constant_demand_forest_wood_products_pc = ExtConstant(
    r"../land.xlsx",
    "Global",
    "demand_forest_wood_products",
    {},
    _root,
    {},
    "_ext_constant_demand_forest_wood_products_pc",
)


@component.add(
    name="demand_wood_products_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_wood_products_m3": 1, "wood_energy_density": 1},
)
def demand_wood_products_ej():
    """
    Demand of non energy forest products expressed as energy (to compare with other uses)
    """
    return demand_wood_products_m3() * wood_energy_density()


@component.add(
    name="demand_wood_products_m3",
    units="m3/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_forest_wood_products_pc": 1, "population": 1},
)
def demand_wood_products_m3():
    """
    Demand of non-energy product forests
    """
    return demand_forest_wood_products_pc() * population()


@component.add(
    name="EU_forest_energy_imports_from_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_demand_forest_biomass_ej": 1, "forest_extraction_ej": 1},
)
def eu_forest_energy_imports_from_row():
    """
    EU imports of wood from RoW.
    """
    return total_demand_forest_biomass_ej() - forest_extraction_ej()


@component.add(
    name="forest_consumption_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_extraction_ej": 1, "eu_forest_energy_imports_from_row": 1},
)
def forest_consumption_ej():
    """
    EU forest consumption.
    """
    return forest_extraction_ej() + eu_forest_energy_imports_from_row()


@component.add(
    name="forest_extraction_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_forest_area": 1,
        "p_minimum_forest": 1,
        "total_demand_forest_biomass_ej": 1,
        "max_sustainable_forest_extraction_ej": 1,
        "p_forest_overexplotation": 1,
    },
)
def forest_extraction_ej():
    """
    Forest extration of all kinds of products. If the total demand of forest is greater than sustainable potential multiplied by the overxplotation accepted in policy P_forest_extraction the demand is cut to this amount. If the demand is lower than the sustainable*P_forest_extraction the extraction equals the demand
    """
    return if_then_else(
        available_forest_area() > p_minimum_forest(),
        lambda: float(
            np.minimum(
                total_demand_forest_biomass_ej(),
                max_sustainable_forest_extraction_ej()
                * (1 + p_forest_overexplotation()),
            )
        ),
        lambda: 0,
    )


@component.add(
    name="forest_extraction_per_MHa",
    units="EJ/(year*MHa)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_forest_extraction_per_mha"},
)
def forest_extraction_per_mha():
    """
    Wood extration from forest in 2015, we assume this extraction is sustainable and it might grow slightly 10% because of better management, average last years
    """
    return _ext_constant_forest_extraction_per_mha()


_ext_constant_forest_extraction_per_mha = ExtConstant(
    r"../land.xlsx",
    "Global",
    "forest_extraction",
    {},
    _root,
    {},
    "_ext_constant_forest_extraction_per_mha",
)


@component.add(
    name="Forest_loss_to_sustain_agriculture",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "aux_reach_available_land": 1,
        "agricultural_land": 1,
        "agricultural_land_until_2015": 1,
        "nvs_1_year": 1,
    },
)
def forest_loss_to_sustain_agriculture():
    """
    Forest loss rate to maintain the area dedicated to agriculture in EU in the year 2015.
    """
    return (
        if_then_else(
            aux_reach_available_land() < 1,
            lambda: agricultural_land_until_2015() - agricultural_land(),
            lambda: 0,
        )
        / nvs_1_year()
    )


@component.add(
    name="forest_stock_ratio",
    units="MHa/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "growing_stock_forest_per_ha": 1,
        "ha_to_mha": 1,
        "wood_energy_density": 1,
    },
)
def forest_stock_ratio():
    """
    Forest stock ratio.
    """
    return 1 / (growing_stock_forest_per_ha() * ha_to_mha() * wood_energy_density())


@component.add(
    name="Growing_stock_forest_per_Ha",
    units="m3/Ha",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_growing_stock_forest_per_ha"},
)
def growing_stock_forest_per_ha():
    """
    Hectares of forest lost per m3 of unsustainable wood extraction, based on stock per extraction ratios, source FAO2015 129m3/Ha for the world.
    """
    return _ext_constant_growing_stock_forest_per_ha()


_ext_constant_growing_stock_forest_per_ha = ExtConstant(
    r"../land.xlsx",
    "Global",
    "growing_stock_forest",
    {},
    _root,
    {},
    "_ext_constant_growing_stock_forest_per_ha",
)


@component.add(
    name="Ha_to_MHa", units="Ha/MHa", comp_type="Constant", comp_subtype="Normal"
)
def ha_to_mha():
    return 1000000.0


@component.add(
    name="hist_variation_primary_forest",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_primary_forest": 2, "time_step": 2},
)
def hist_variation_primary_forest():
    """
    Primary forest area historic variation.
    """
    return if_then_else(
        time() < 2014,
        lambda: (
            historic_primary_forest(time() + time_step())
            - historic_primary_forest(time())
        )
        / time_step(),
        lambda: 0,
    )


@component.add(
    name="hist_variation_urban_land",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_urban_land": 2, "time_step": 2},
)
def hist_variation_urban_land():
    """
    Variation of historic urban land.
    """
    return (
        if_then_else(
            time() < 2014,
            lambda: historic_urban_land(time() + time_step())
            - historic_urban_land(time()),
            lambda: 0,
        )
        / time_step()
    )


@component.add(
    name="Historic_av_variation_primary_forests_area",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_historic_av_variation_primary_forests_area"
    },
)
def historic_av_variation_primary_forests_area():
    """
    Historic average annual variation (1990-2015) of primary forests area.
    """
    return _ext_constant_historic_av_variation_primary_forests_area()


_ext_constant_historic_av_variation_primary_forests_area = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "variation_primary_forests_area",
    {},
    _root,
    {},
    "_ext_constant_historic_av_variation_primary_forests_area",
)


@component.add(
    name="Historic_primary_forest",
    units="MHa",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_primary_forest",
        "__lookup__": "_ext_lookup_historic_primary_forest",
    },
)
def historic_primary_forest(x, final_subs=None):
    """
    Historic primary forest evolution.
    """
    return _ext_lookup_historic_primary_forest(x, final_subs)


_ext_lookup_historic_primary_forest = ExtLookup(
    r"../land.xlsx",
    "Europe",
    "time",
    "primary_forest",
    {},
    _root,
    {},
    "_ext_lookup_historic_primary_forest",
)


@component.add(
    name="Historic_urban_land",
    units="MHa",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_urban_land",
        "__lookup__": "_ext_lookup_historic_urban_land",
    },
)
def historic_urban_land(x, final_subs=None):
    """
    Historic urban land.
    """
    return _ext_lookup_historic_urban_land(x, final_subs)


_ext_lookup_historic_urban_land = ExtLookup(
    r"../land.xlsx",
    "Europe",
    "time",
    "urban_land",
    {},
    _root,
    {},
    "_ext_lookup_historic_urban_land",
)


@component.add(
    name="Historic_urban_land_density",
    units="MHa/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_urban_land": 1, "historic_population": 1},
)
def historic_urban_land_density():
    """
    Historic urban land density evolution (defined as urban land vs total population).
    """
    return historic_urban_land(time()) / historic_population(time())


@component.add(
    name="increase_agricultural_land",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "agricultural_land": 1,
        "agricultural_land_until_2015": 1,
        "aux_reach_available_land": 1,
        "nvs_1_year": 1,
    },
)
def increase_agricultural_land():
    return (
        if_then_else(
            time() < 2014,
            lambda: 0,
            lambda: agricultural_land_until_2015() - agricultural_land(),
        )
        * aux_reach_available_land()
        / nvs_1_year()
    )


@component.add(
    name="initial_agricultural_area",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_agricultural_area"},
)
def initial_agricultural_area():
    return _ext_constant_initial_agricultural_area()


_ext_constant_initial_agricultural_area = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_agricultural_area",
    {},
    _root,
    {},
    "_ext_constant_initial_agricultural_area",
)


@component.add(
    name="initial_'available'_forest_area",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_planted_forests": 1,
        "initial_other_naturally_regen_forest": 1,
    },
)
def initial_available_forest_area():
    """
    Initial "available" forest area.
    """
    return initial_planted_forests() + initial_other_naturally_regen_forest()


@component.add(
    name="initial_'available_land'",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_available_land"},
)
def initial_available_land():
    """
    Initial "available land" as defined in MEDEAS-EU framework, representing the terrestrial land that is currently neither being used by the primary sector (arable land, permanent crops, permanent meadows and pastures and productive forest area) nor built-up, nor occupied by permanent snows&glaciers.
    """
    return _ext_constant_initial_available_land()


_ext_constant_initial_available_land = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_available_land",
    {},
    _root,
    {},
    "_ext_constant_initial_available_land",
)


@component.add(
    name="initial_marginal_land_occupied_by_biofuels",
    units="MHa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_marginal_land_occupied_by_biofuels():
    """
    Initial value of marginal land occupied by biofuels.
    """
    return 0


@component.add(
    name="initial_other_naturally_regen_forest",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_other_naturally_regen_forest"},
)
def initial_other_naturally_regen_forest():
    """
    Initial "Other naturally regenerated forests" (FAOSTAT category).
    """
    return _ext_constant_initial_other_naturally_regen_forest()


_ext_constant_initial_other_naturally_regen_forest = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_other_naturally_regen_forest",
    {},
    _root,
    {},
    "_ext_constant_initial_other_naturally_regen_forest",
)


@component.add(
    name='"initial_permanent_snows&glaciers_area"',
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_permanent_snowsglaciers_area"},
)
def initial_permanent_snowsglaciers_area():
    """
    Initial area occupied by permanent snows & glaciers.
    """
    return _ext_constant_initial_permanent_snowsglaciers_area()


_ext_constant_initial_permanent_snowsglaciers_area = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_permanent_snow_glaciers_area",
    {},
    _root,
    {},
    "_ext_constant_initial_permanent_snowsglaciers_area",
)


@component.add(
    name="initial_planted_forests",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_planted_forests"},
)
def initial_planted_forests():
    """
    Initial "Planted Forests" (FAOSTAT category).
    """
    return _ext_constant_initial_planted_forests()


_ext_constant_initial_planted_forests = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_planted_forests",
    {},
    _root,
    {},
    "_ext_constant_initial_planted_forests",
)


@component.add(
    name="initial_primary_forest_area",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_primary_forest_area"},
)
def initial_primary_forest_area():
    """
    Initial primary forests area.
    """
    return _ext_constant_initial_primary_forest_area()


_ext_constant_initial_primary_forest_area = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_primary_forest",
    {},
    _root,
    {},
    "_ext_constant_initial_primary_forest_area",
)


@component.add(
    name="initial_urban_land",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_urban_land"},
)
def initial_urban_land():
    """
    Artificial surfaces (including urban and associated areas).
    """
    return _ext_constant_initial_urban_land()


_ext_constant_initial_urban_land = ExtConstant(
    r"../land.xlsx",
    "Europe",
    "initial_urban",
    {},
    _root,
    {},
    "_ext_constant_initial_urban_land",
)


@component.add(
    name="Land_availability_constraint",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aux_reach_available_land": 1},
)
def land_availability_constraint():
    """
    Land availability constraint: when this variable is 0 it limits the expansion of biofuel crops.
    """
    return aux_reach_available_land()


@component.add(
    name="Land_for_RES_elec_rate",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_requirements_res_elec_compet_uses": 1,
        "land_requirements_res_elec_compet_uses_t1": 1,
        "nvs_1_year": 1,
        "aux_reach_available_land": 1,
    },
)
def land_for_res_elec_rate():
    """
    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro).
    """
    return (
        (
            land_requirements_res_elec_compet_uses()
            - land_requirements_res_elec_compet_uses_t1()
        )
        / nvs_1_year()
        * aux_reach_available_land()
    )


@component.add(
    name="Land_for_solar_and_hydro_RES",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_land_for_solar_and_hydro_res": 1},
    other_deps={
        "_integ_land_for_solar_and_hydro_res": {
            "initial": {"land_requirements_res_elec_compet_uses": 1},
            "step": {"land_for_res_elec_rate": 1},
        }
    },
)
def land_for_solar_and_hydro_res():
    """
    Land for solar on land and hydro power plants.
    """
    return _integ_land_for_solar_and_hydro_res()


_integ_land_for_solar_and_hydro_res = Integ(
    lambda: land_for_res_elec_rate(),
    lambda: land_requirements_res_elec_compet_uses(),
    "_integ_land_for_solar_and_hydro_res",
)


@component.add(
    name='"Land_requirements_RES_elec_compet_uses_t-1"',
    units="MHa",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_land_requirements_res_elec_compet_uses_t1": 1},
    other_deps={
        "_delayfixed_land_requirements_res_elec_compet_uses_t1": {
            "initial": {"land_requirements_res_elec_compet_uses": 1},
            "step": {"land_requirements_res_elec_compet_uses": 1},
        }
    },
)
def land_requirements_res_elec_compet_uses_t1():
    """
    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro) requiring land and not easily compatible with double uses delayed 1 year.
    """
    return _delayfixed_land_requirements_res_elec_compet_uses_t1()


_delayfixed_land_requirements_res_elec_compet_uses_t1 = DelayFixed(
    lambda: land_requirements_res_elec_compet_uses(),
    lambda: 1,
    lambda: land_requirements_res_elec_compet_uses(),
    time_step,
    "_delayfixed_land_requirements_res_elec_compet_uses_t1",
)


@component.add(
    name="Marginal_land_for_biofuels",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_marginal_land_for_biofuels": 1},
    other_deps={
        "_integ_marginal_land_for_biofuels": {
            "initial": {"initial_marginal_land_occupied_by_biofuels": 1},
            "step": {"marginal_land_for_biofuels_rate": 1},
        }
    },
)
def marginal_land_for_biofuels():
    """
    Marginal land dedicated to biofuels
    """
    return _integ_marginal_land_for_biofuels()


_integ_marginal_land_for_biofuels = Integ(
    lambda: marginal_land_for_biofuels_rate(),
    lambda: initial_marginal_land_occupied_by_biofuels(),
    "_integ_marginal_land_for_biofuels",
)


@component.add(
    name="Marginal_land_for_biofuels_rate",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_land_marg_for_biofuels": 1, "aux_reach_available_land": 1},
)
def marginal_land_for_biofuels_rate():
    """
    Biofuels plantation rate on marginal lands.
    """
    return new_land_marg_for_biofuels() * aux_reach_available_land()


@component.add(
    name="max_E_forest_available_non_trad",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_e_tot_forest_available": 1,
        "demand_forest_energy_traditional_ej": 1,
    },
)
def max_e_forest_available_non_trad():
    """
    Maximum energy from forest available excluding traditional use of biomasss.
    """
    return float(
        np.maximum(
            0, max_e_tot_forest_available() - demand_forest_energy_traditional_ej()
        )
    )


@component.add(
    name="max_E_forest_energy_non_trad",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_e_forest_available_non_trad": 1, "consum_wood_products_ej": 1},
)
def max_e_forest_energy_non_trad():
    """
    Maximum energy (NPP) from forest available for modern energy uses (i.e. excluding traditional use of biomasss).
    """
    return float(
        np.maximum(0, max_e_forest_available_non_trad() - consum_wood_products_ej())
    )


@component.add(
    name="max_E_tot_forest_available",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_forest_area": 1,
        "forest_extraction_per_mha": 1,
        "p_forest_overexplotation": 1,
    },
)
def max_e_tot_forest_available():
    """
    Potential energy from total forest available (including overexploitation).
    """
    return (
        available_forest_area()
        * forest_extraction_per_mha()
        * (1 + p_forest_overexplotation())
    )


@component.add(
    name="max_sustainable_forest_extraction_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"available_forest_area": 1, "forest_extraction_per_mha": 1},
)
def max_sustainable_forest_extraction_ej():
    """
    Wood that might be extracted from forest according to usable foresta area in terms of energy equivalent
    """
    return available_forest_area() * forest_extraction_per_mha()


@component.add(
    name="Mha_to_m2", units="m2/MHa", comp_type="Constant", comp_subtype="Normal"
)
def mha_to_m2():
    """
    Conversion from Mha to m2.
    """
    return 10000000000.0


@component.add(
    name="P_forest_overexplotation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_forest_overexplotation"},
)
def p_forest_overexplotation():
    """
    Policy of forest extraction for energy uses. Describes the percent of deficit of forest biomass acepted. If gives the percent at which wood for energy and non energy uses must adapt to sustainable potencial. If it's greater than 0 means that overexplotaion of forest leads to forest stock destruction.
    """
    return _ext_constant_p_forest_overexplotation()


_ext_constant_p_forest_overexplotation = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "forest_overexplotation",
    {},
    _root,
    {},
    "_ext_constant_p_forest_overexplotation",
)


@component.add(
    name="P_minimum_forest",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_minimum_forest"},
)
def p_minimum_forest():
    """
    Minimum surface of forest land accepted.
    """
    return _ext_constant_p_minimum_forest()


_ext_constant_p_minimum_forest = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "minimum_forest",
    {},
    _root,
    {},
    "_ext_constant_p_minimum_forest",
)


@component.add(
    name="P_urban_land_density",
    units="m2/people",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_urban_land_density"},
)
def p_urban_land_density():
    """
    Policy target to set urban land density in a target year.
    """
    return _ext_constant_p_urban_land_density()


_ext_constant_p_urban_land_density = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "urban_land_density",
    {},
    _root,
    {},
    "_ext_constant_p_urban_land_density",
)


@component.add(
    name="P_urban_land_density_MHa",
    units="MHa/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_urban_land_density": 1, "mha_to_m2": 1},
)
def p_urban_land_density_mha():
    return p_urban_land_density() / mha_to_m2()


@component.add(
    name="P_variation_primary_forest",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_variation_primary_forest"},
)
def p_variation_primary_forest():
    """
    Policy target to increase/decrease the rate of expansion of primary forest (annual).
    """
    return _ext_constant_p_variation_primary_forest()


_ext_constant_p_variation_primary_forest = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "variation_primary_forest",
    {},
    _root,
    {},
    "_ext_constant_p_variation_primary_forest",
)


@component.add(
    name="Primary_forests_area",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_primary_forests_area": 1},
    other_deps={
        "_integ_primary_forests_area": {
            "initial": {"initial_primary_forest_area": 1},
            "step": {"available_to_primary_forest_rate": 1},
        }
    },
)
def primary_forests_area():
    """
    Primary forests area.
    """
    return _integ_primary_forests_area()


_integ_primary_forests_area = Integ(
    lambda: available_to_primary_forest_rate(),
    lambda: initial_primary_forest_area(),
    "_integ_primary_forests_area",
)


@component.add(
    name="shortage_BioE_for_elec",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"shortage_bioe_non_trad_delayed_1yr": 1},
)
def shortage_bioe_for_elec():
    """
    Shortage of bioenergy for supplying RES power plants for electricity generation.
    """
    value = xr.DataArray(
        np.nan, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
    )
    value.loc[["hydro"]] = 1
    value.loc[["geot_elec"]] = 1
    value.loc[["solid_bioE_elec"]] = shortage_bioe_non_trad_delayed_1yr()
    value.loc[["oceanic"]] = 1
    value.loc[["wind_onshore"]] = 1
    value.loc[["wind_offshore"]] = 1
    value.loc[["solar_PV"]] = 1
    value.loc[["CSP"]] = 1
    return value


@component.add(
    name="shortage_BioE_for_heat",
    units="Dmnl",
    subscripts=["RES_heat"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"shortage_bioe_non_trad_delayed_1yr": 1},
)
def shortage_bioe_for_heat():
    """
    Shortage of bioenergy for supplying RES power plants for heat generation.
    """
    value = xr.DataArray(
        np.nan, {"RES_heat": _subscript_dict["RES_heat"]}, ["RES_heat"]
    )
    value.loc[["solar_heat"]] = 1
    value.loc[["geot_heat"]] = 1
    value.loc[["solid_bioE_heat"]] = shortage_bioe_non_trad_delayed_1yr()
    return value


@component.add(
    name="shortage_BioE_non_trad",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "consum_forest_energy_non_traditional_ej": 1,
        "demand_forest_energy_non_tradition_ej": 1,
    },
)
def shortage_bioe_non_trad():
    """
    Shortage of bioenergy for modern energy uses (no traditional).
    """
    return zidz(
        consum_forest_energy_non_traditional_ej(),
        demand_forest_energy_non_tradition_ej(),
    )


@component.add(
    name="shortage_BioE_non_trad_delayed_1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_shortage_bioe_non_trad_delayed_1yr": 1},
    other_deps={
        "_delayfixed_shortage_bioe_non_trad_delayed_1yr": {
            "initial": {},
            "step": {"shortage_bioe_non_trad": 1},
        }
    },
)
def shortage_bioe_non_trad_delayed_1yr():
    """
    Shortage of bioenergy for modern energy uses (no traditional) delayed 1 year.
    """
    return _delayfixed_shortage_bioe_non_trad_delayed_1yr()


_delayfixed_shortage_bioe_non_trad_delayed_1yr = DelayFixed(
    lambda: shortage_bioe_non_trad(),
    lambda: 1,
    lambda: 1,
    time_step,
    "_delayfixed_shortage_bioe_non_trad_delayed_1yr",
)


@component.add(
    name="Start_year_P_urban_land_density",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_urban_land_density"},
)
def start_year_p_urban_land_density():
    """
    Start year of the policy target to modify urban land density.
    """
    return _ext_constant_start_year_p_urban_land_density()


_ext_constant_start_year_p_urban_land_density = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_year_P_urban_land_density",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_urban_land_density",
)


@component.add(
    name="Start_year_P_variation_primary_forest",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_variation_primary_forest"},
)
def start_year_p_variation_primary_forest():
    """
    Start year of the policy target to increase primary forests area.
    """
    return _ext_constant_start_year_p_variation_primary_forest()


_ext_constant_start_year_p_variation_primary_forest = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_year_variation_primary_forest",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_variation_primary_forest",
)


@component.add(
    name="Target_year_P_urban_land_density",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_target_year_p_urban_land_density"},
)
def target_year_p_urban_land_density():
    """
    Target year of the policy target to modify urban land density.
    """
    return _ext_constant_target_year_p_urban_land_density()


_ext_constant_target_year_p_urban_land_density = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "target_year_P_urban_land_density",
    {},
    _root,
    {},
    "_ext_constant_target_year_p_urban_land_density",
)


@component.add(
    name="total_demand_energy_forest_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_forest_energy_non_tradition_ej": 1,
        "demand_forest_energy_traditional_ej": 1,
    },
)
def total_demand_energy_forest_ej():
    """
    Total demand of forest energy.
    """
    return (
        demand_forest_energy_non_tradition_ej() + demand_forest_energy_traditional_ej()
    )


@component.add(
    name="total_demand_forest_biomass_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "demand_forest_energy_non_tradition_ej": 1,
        "demand_forest_energy_traditional_ej": 1,
        "demand_wood_products_ej": 1,
    },
)
def total_demand_forest_biomass_ej():
    """
    Total demand of wood products from forest for all uses
    """
    return (
        demand_forest_energy_non_tradition_ej()
        + demand_forest_energy_traditional_ej()
        + demand_wood_products_ej()
    )


@component.add(
    name="Total_EU_land_endogenous",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "compet_agricultural_land_for_biofuels": 1,
        "available_forest_area": 1,
        "land_for_solar_and_hydro_res": 1,
        "marginal_land_for_biofuels": 1,
        "initial_permanent_snowsglaciers_area": 1,
        "primary_forests_area": 1,
        "urban_land": 1,
        "available_land": 1,
    },
)
def total_eu_land_endogenous():
    return (
        agricultural_land()
        + compet_agricultural_land_for_biofuels()
        + available_forest_area()
        + land_for_solar_and_hydro_res()
        + marginal_land_for_biofuels()
        + initial_permanent_snowsglaciers_area()
        + primary_forests_area()
        + urban_land()
        + available_land()
    )


@component.add(
    name="Total_land_occupied_by_RES",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "compet_agricultural_land_for_biofuels": 1,
        "land_for_solar_and_hydro_res": 1,
        "marginal_land_for_biofuels": 1,
    },
)
def total_land_occupied_by_res():
    """
    Total land occupied by RES (biofuel crops and RES elec PV on land, CSP and hydro).
    """
    return (
        compet_agricultural_land_for_biofuels()
        + land_for_solar_and_hydro_res()
        + marginal_land_for_biofuels()
    )


@component.add(
    name="unsustainable_loggin",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_extraction_ej": 1,
        "max_sustainable_forest_extraction_ej": 1,
        "forest_stock_ratio": 1,
    },
)
def unsustainable_loggin():
    """
    Loss of forest land due to overexplotation of forest for energy uses.
    """
    return float(
        np.maximum(
            0,
            (forest_extraction_ej() - max_sustainable_forest_extraction_ej())
            * forest_stock_ratio(),
        )
    )


@component.add(
    name="Urban_land",
    units="MHa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_urban_land": 1},
    other_deps={
        "_integ_urban_land": {
            "initial": {"initial_urban_land": 1},
            "step": {"urban_land_rate": 1},
        }
    },
)
def urban_land():
    """
    Land for urban uses and infraestructures. Corresponds with FAOSTAT category "Artificial surfaces (including urban and associated areas)".
    """
    return _integ_urban_land()


_integ_urban_land = Integ(
    lambda: urban_land_rate(), lambda: initial_urban_land(), "_integ_urban_land"
)


@component.add(
    name="urban_land_density",
    units="MHa/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "historic_urban_land_density": 4,
        "target_year_p_urban_land_density": 2,
        "p_urban_land_density_mha": 2,
        "start_year_p_urban_land_density": 3,
    },
)
def urban_land_density():
    """
    Urban land density evolution as a result of the application of a policy target.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_urban_land_density(),
        lambda: if_then_else(
            time() < start_year_p_urban_land_density(),
            lambda: historic_urban_land_density(),
            lambda: if_then_else(
                time() < target_year_p_urban_land_density(),
                lambda: historic_urban_land_density()
                + (p_urban_land_density_mha() - historic_urban_land_density())
                * (time() - start_year_p_urban_land_density())
                / (
                    target_year_p_urban_land_density()
                    - start_year_p_urban_land_density()
                ),
                lambda: p_urban_land_density_mha(),
            ),
        ),
    )


@component.add(
    name="urban_land_rate",
    units="MHa/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "hist_variation_urban_land": 1,
        "urban_land_density": 1,
        "pop_variation": 1,
    },
)
def urban_land_rate():
    """
    Rate of urban surface rate. IF THEN ELSE(Time<2014, hist variation urban land, 0.0478639*urban land density variation+1.99746*pop variation/m2 per MHa)
    """
    return if_then_else(
        time() < 2014,
        lambda: hist_variation_urban_land(),
        lambda: urban_land_density() * pop_variation(),
    )


@component.add(
    name="wood_energy_density",
    units="EJ/m3",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_wood_energy_density"},
)
def wood_energy_density():
    """
    Average energy of wood products.
    """
    return _ext_constant_wood_energy_density()


_ext_constant_wood_energy_density = ExtConstant(
    r"../land.xlsx",
    "Global",
    "wood_energy_density",
    {},
    _root,
    {},
    "_ext_constant_wood_energy_density",
)
