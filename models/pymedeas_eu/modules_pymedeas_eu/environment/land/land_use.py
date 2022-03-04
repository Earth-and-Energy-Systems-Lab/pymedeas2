"""
Module land_use
Translated using PySD version 2.2.1
"""


def available_land():
    """
    Real Name: "'Available land'"
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def available_forest_area():
    """
    Real Name: "'Available' forest area"
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def available_to_primary_forest_rate():
    """
    Real Name: "'Available' to primary forest rate"
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def nvs_1_to_m():
    """
    Real Name: "1 to M"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 1000000.0


def agricultural_land():
    """
    Real Name: Agricultural land
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def agricultural_land_until_2015():
    """
    Real Name: agricultural land until 2015
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Agricultural land in EU until the year 2015. From that year, this variable reports the value of agricultural land in 2015.
    """
    return _sampleiftrue_agricultural_land_until_2015()


_sampleiftrue_agricultural_land_until_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: agricultural_land(),
    lambda: agricultural_land(),
    "_sampleiftrue_agricultural_land_until_2015",
)


def aux_reach_available_land():
    """
    Real Name: aux reach available land
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    This variable = 0 when there is no more land available.
    """
    return np.interp(
        available_land(),
        [-1.0e-02, 0.0e00, 1.0e-08, 1.0e-04, 1.0e-02, 1.0e00, 1.0e02],
        [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
    )


def compet_agricultural_land_for_biofuels():
    """
    Real Name: Compet agricultural land for biofuels
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Biofuels plantation on land subject to competition with other agricultural uses.
    """
    return _integ_compet_agricultural_land_for_biofuels()


_integ_compet_agricultural_land_for_biofuels = Integ(
    lambda: compet_land_for_biofuels_rate(),
    lambda: initial_value_land_compet_biofuels_2gen_mha(),
    "_integ_compet_agricultural_land_for_biofuels",
)


def compet_land_for_biofuels_rate():
    """
    Real Name: compet land for biofuels rate
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Biofuels plantation rate on land subject to competition with other agricultural uses.
    """
    return new_biofuels_2gen_land_compet()


def consum_forest_energy_non_traditional_ej():
    """
    Real Name: consum forest energy non traditional EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Part of the forest biomass extration that goes into non energy uses. P wood-energy uses divides the possible extration into the two uses. Traditional biomass is not restricted
    """
    return np.minimum(
        demand_forest_energy_non_tradition_ej(),
        forest_consumption_ej()
        - consum_forest_energy_traditional_ej()
        - consum_wood_products_ej(),
    )


def consum_forest_energy_traditional_ej():
    """
    Real Name: consum forest energy traditional EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Consumption of traditional biomass. Traditional wood extraction is got priority over other uses but is limited by forest extraction, which depends on the stock and the policies taken to protect forests.
    """
    return np.minimum(forest_consumption_ej(), demand_forest_energy_traditional_ej())


def consum_wood_products_ej():
    """
    Real Name: consum wood products EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Priority to energy uses Part of the forest biomass extration that goes into non energy uses. P wood/energy uses divides the possible extration into the two uses. Traditional uses are not restricted
    """
    return np.minimum(
        demand_wood_products_ej(),
        forest_consumption_ej() - consum_forest_energy_traditional_ej(),
    )


def deficit_forest_biomass():
    """
    Real Name: deficit forest biomass
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def deficit_wood_products():
    """
    Real Name: deficit wood products
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Percent of the demand of wood products that cannot be met. I should influence the corresponding economic sector but it does not
    """
    return (
        demand_wood_products_ej() - consum_wood_products_ej()
    ) / demand_wood_products_ej()


def deforestation_rate():
    """
    Real Name: Deforestation rate
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Forest land deforestation rate due to unsustainable loggin and converted to agriculture uses.
    """
    return if_then_else(
        available_forest_area() > p_minimum_forest(),
        lambda: unsustainable_loggin(),
        lambda: 0,
    )


def demand_forest_energy_non_tradition_ej():
    """
    Real Name: demand forest energy non tradition EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of forest products for energy uses in non traditional uses, in terms of energy. Residuals and traditional biomass not included.
    """
    return np.maximum(
        0, solid_bioe_emissions_relevant_ej() - pe_bioe_residues_nonbiofuels_ej()
    )


def demand_forest_energy_traditional_ej():
    """
    Real Name: demand forest energy traditional EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of tradition biomass in terms of EJ
    """
    return pe_traditional_biomass_demand_ej()


def demand_forest_wood_products_pc():
    """
    Real Name: demand forest wood products pc
    Original Eqn:
    Units: m3/people
    Limits: (None, None)
    Type: Constant
    Subs: []

    Demand of forest non energy products per capita, data FAO2016
    """
    return _ext_constant_demand_forest_wood_products_pc()


_ext_constant_demand_forest_wood_products_pc = ExtConstant(
    "../land.xlsx",
    "Global",
    "demand_forest_wood_products",
    {},
    _root,
    "_ext_constant_demand_forest_wood_products_pc",
)


def demand_wood_products_ej():
    """
    Real Name: demand wood products EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of non energy forest products expressed as energy (to compare with other uses)
    """
    return demand_wood_products_m3() * wood_energy_density()


def demand_wood_products_m3():
    """
    Real Name: demand wood products m3
    Original Eqn:
    Units: m3
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of non-energy product forests
    """
    return demand_forest_wood_products_pc() * population()


def eu_forest_energy_imports_from_row():
    """
    Real Name: EU forest energy imports from RoW
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EU imports of wood from RoW.
    """
    return total_demand_forest_biomass_ej() - forest_extraction_ej()


def forest_consumption_ej():
    """
    Real Name: forest consumption EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EU forest consumption.
    """
    return forest_extraction_ej() + eu_forest_energy_imports_from_row()


def forest_loss_to_sustain_agriculture():
    """
    Real Name: Forest loss to sustain agriculture
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Forest loss rate to maintain the area dedicated to agriculture in EU in the year 2015.
    """
    return if_then_else(
        aux_reach_available_land() < 1,
        lambda: agricultural_land_until_2015() - agricultural_land(),
        lambda: 0,
    )


def forest_extraction_ej():
    """
    Real Name: forest extraction EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Forest extration of all kinds of products. If the total demand of forest is greater than sustainable potential multiplied by the overxplotation accepted in policy P_forest_extraction the demand is cut to this amount. If the demand is lower than the sustainable*P_forest_extraction the extraction equals the demand
    """
    return if_then_else(
        available_forest_area() > p_minimum_forest() * forest_extraction_per_ha(),
        lambda: np.minimum(
            total_demand_forest_biomass_ej(),
            max_sustainable_forest_extraction_ej() * (1 + p_forest_overexplotation()),
        ),
        lambda: 0,
    )


def forest_extraction_per_ha():
    """
    Real Name: forest extraction per Ha
    Original Eqn:
    Units: EJ/MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Wood extration from forest in 2015, we assume this extraction is sustainable and it might grow slightly 10% because of better management, average last years
    """
    return _ext_constant_forest_extraction_per_ha()


_ext_constant_forest_extraction_per_ha = ExtConstant(
    "../land.xlsx",
    "Global",
    "forest_extraction",
    {},
    _root,
    "_ext_constant_forest_extraction_per_ha",
)


def forest_stock_ratio():
    """
    Real Name: forest stock ratio
    Original Eqn:
    Units: MHa/EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Forest stock ratio.
    """
    return 1 / (growing_stock_forest_per_ha() * nvs_1_to_m() * wood_energy_density())


def growing_stock_forest_per_ha():
    """
    Real Name: Growing stock forest per Ha
    Original Eqn:
    Units: m3/Ha
    Limits: (None, None)
    Type: Constant
    Subs: []

    Hectares of forest lost per m3 of unsustainable wood extraction, based on stock per extraction ratios, source FAO2015 129m3/Ha for the world.
    """
    return _ext_constant_growing_stock_forest_per_ha()


_ext_constant_growing_stock_forest_per_ha = ExtConstant(
    "../land.xlsx",
    "Global",
    "growing_stock_forest",
    {},
    _root,
    "_ext_constant_growing_stock_forest_per_ha",
)


def hist_variation_primary_forest():
    """
    Real Name: hist variation primary forest
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary forest area historic variation.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_primary_forest(integer(time() + 1))
        - historic_primary_forest(integer(time())),
        lambda: 0,
    )


def hist_variation_urban_land():
    """
    Real Name: hist variation urban land
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual variation of historic urban land.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_urban_land(integer(time() + 1))
        - historic_urban_land(integer(time())),
        lambda: 0,
    )


def historic_av_variation_primary_forests_area():
    """
    Real Name: Historic av variation primary forests area
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic average variation (1990-2015) of primary forests area.
    """
    return _ext_constant_historic_av_variation_primary_forests_area()


_ext_constant_historic_av_variation_primary_forests_area = ExtConstant(
    "../land.xlsx",
    "Europe",
    "variation_primary_forests_area",
    {},
    _root,
    "_ext_constant_historic_av_variation_primary_forests_area",
)


def historic_primary_forest(x):
    """
    Real Name: Historic primary forest
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic primary forest evolution.
    """
    return _ext_lookup_historic_primary_forest(x)


_ext_lookup_historic_primary_forest = ExtLookup(
    "../land.xlsx",
    "Europe",
    "time",
    "primary_forest",
    {},
    _root,
    "_ext_lookup_historic_primary_forest",
)


def historic_urban_land(x):
    """
    Real Name: Historic urban land
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic urban land.
    """
    return _ext_lookup_historic_urban_land(x)


_ext_lookup_historic_urban_land = ExtLookup(
    "../land.xlsx",
    "Europe",
    "time",
    "urban_land",
    {},
    _root,
    "_ext_lookup_historic_urban_land",
)


def historic_urban_land_density():
    """
    Real Name: Historic urban land density
    Original Eqn:
    Units: m2/people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic urban land density evolution (defined as urban land vs total population).
    """
    return historic_urban_land(time()) * mha_to_m2() / historic_population(time())


def increase_agricultural_land():
    """
    Real Name: increase agricultural land
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        if_then_else(
            time() < 2014,
            lambda: 0,
            lambda: agricultural_land_until_2015() - agricultural_land(),
        )
        * aux_reach_available_land()
    )


def initial_available_land():
    """
    Real Name: initial 'available land'
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial "available land" as defined in MEDEAS-EU framework, representing the terrestrial land that is currently neither being used by the primary sector (arable land, permanent crops, permanent meadows and pastures and productive forest area) nor built-up, nor occupied by permanent snows&glaciers.
    """
    return _ext_constant_initial_available_land()


_ext_constant_initial_available_land = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_available_land",
    {},
    _root,
    "_ext_constant_initial_available_land",
)


def initial_available_forest_area():
    """
    Real Name: initial 'available' forest area
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Initial "available" forest area.
    """
    return initial_planted_forests() + initial_other_naturally_regen_forest()


def initial_agricultural_area():
    """
    Real Name: initial agricultural area
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_initial_agricultural_area()


_ext_constant_initial_agricultural_area = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_agricultural_area",
    {},
    _root,
    "_ext_constant_initial_agricultural_area",
)


def initial_marginal_land_occupied_by_biofuels():
    """
    Real Name: initial marginal land occupied by biofuels
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial value of marginal land occupied by biofuels.
    """
    return 0


def initial_other_naturally_regen_forest():
    """
    Real Name: initial other naturally regen forest
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial "Other naturally regenerated forests" (FAOSTAT category).
    """
    return _ext_constant_initial_other_naturally_regen_forest()


_ext_constant_initial_other_naturally_regen_forest = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_other_naturally_regen_forest",
    {},
    _root,
    "_ext_constant_initial_other_naturally_regen_forest",
)


def initial_permanent_snowsglaciers_area():
    """
    Real Name: "initial permanent snows&glaciers area"
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial area occupied by permanent snows & glaciers.
    """
    return _ext_constant_initial_permanent_snowsglaciers_area()


_ext_constant_initial_permanent_snowsglaciers_area = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_permanent_snow_glaciers_area",
    {},
    _root,
    "_ext_constant_initial_permanent_snowsglaciers_area",
)


def initial_planted_forests():
    """
    Real Name: initial planted forests
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial "Planted Forests" (FAOSTAT category).
    """
    return _ext_constant_initial_planted_forests()


_ext_constant_initial_planted_forests = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_planted_forests",
    {},
    _root,
    "_ext_constant_initial_planted_forests",
)


def initial_primary_forest_area():
    """
    Real Name: initial primary forest area
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial primary forests area.
    """
    return _ext_constant_initial_primary_forest_area()


_ext_constant_initial_primary_forest_area = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_primary_forest",
    {},
    _root,
    "_ext_constant_initial_primary_forest_area",
)


def initial_urban_land():
    """
    Real Name: initial urban land
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Artificial surfaces (including urban and associated areas).
    """
    return _ext_constant_initial_urban_land()


_ext_constant_initial_urban_land = ExtConstant(
    "../land.xlsx",
    "Europe",
    "initial_urban",
    {},
    _root,
    "_ext_constant_initial_urban_land",
)


def land_availability_constraint():
    """
    Real Name: Land availability constraint
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land availability constraint: when this variable is 0 it limits the expansion of biofuel crops.
    """
    return aux_reach_available_land()


def land_for_res_elec_rate():
    """
    Real Name: Land for RES elec rate
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro).
    """
    return (
        land_requirements_res_elec_compet_uses()
        - land_requirements_res_elec_compet_uses_t1()
    ) * aux_reach_available_land()


def land_for_solar_and_hydro_res():
    """
    Real Name: Land for solar and hydro RES
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Land for solar on land and hydro power plants.
    """
    return _integ_land_for_solar_and_hydro_res()


_integ_land_for_solar_and_hydro_res = Integ(
    lambda: land_for_res_elec_rate(), lambda: 0.9, "_integ_land_for_solar_and_hydro_res"
)


def land_requirements_res_elec_compet_uses_t1():
    """
    Real Name: "Land requirements RES elec compet uses t-1"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro) requiring land and not easily compatible with double uses delayed 1 year.
    """
    return _delayfixed_land_requirements_res_elec_compet_uses_t1()


_delayfixed_land_requirements_res_elec_compet_uses_t1 = DelayFixed(
    lambda: land_requirements_res_elec_compet_uses(),
    lambda: 1,
    lambda: 0.9115,
    time_step,
    "_delayfixed_land_requirements_res_elec_compet_uses_t1",
)


def marginal_land_for_biofuels():
    """
    Real Name: Marginal land for biofuels
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Marginal land dedicated to biofuels
    """
    return _integ_marginal_land_for_biofuels()


_integ_marginal_land_for_biofuels = Integ(
    lambda: marginal_land_for_biofuels_rate(),
    lambda: initial_marginal_land_occupied_by_biofuels(),
    "_integ_marginal_land_for_biofuels",
)


def marginal_land_for_biofuels_rate():
    """
    Real Name: Marginal land for biofuels rate
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Biofuels plantation rate on marginal lands.
    """
    return new_land_marg_for_biofuels() * aux_reach_available_land()


def max_e_forest_available_non_trad():
    """
    Real Name: max E forest available non trad
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum energy from forest available excluding traditional use of biomasss.
    """
    return np.maximum(
        0, max_e_tot_forest_available() - demand_forest_energy_traditional_ej()
    )


def max_e_forest_energy_non_trad():
    """
    Real Name: max E forest energy non trad
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum energy (NPP) from forest available for modern energy uses (i.e. excluding traditional use of biomasss).
    """
    return np.maximum(0, max_e_forest_available_non_trad() - consum_wood_products_ej())


def max_e_tot_forest_available():
    """
    Real Name: max E tot forest available
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential energy from total forest available (including overexploitation).
    """
    return (
        available_forest_area()
        * forest_extraction_per_ha()
        * (1 + p_forest_overexplotation())
    )


def max_solar_on_land_mha():
    """
    Real Name: max solar on land Mha
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum area potential to be occupied by solar power plants on land.
    """
    return available_land() + surface_csp_mha() + surface_solar_pv_on_land_mha()


def max_sustainable_forest_extraction_ej():
    """
    Real Name: max sustainable forest extraction EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Wood that might be extracted from forest according to usable foresta area in terms of energy equivalent
    """
    return available_forest_area() * forest_extraction_per_ha()


def mha_to_m2():
    """
    Real Name: Mha to m2
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion from Mha to m2.
    """
    return 10000000000.0


def p_forest_overexplotation():
    """
    Real Name: P forest overexplotation
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of forest extraction for energy uses. Describes the percent of deficit of forest biomass acepted. If gives the percent at which wood for energy and non energy uses must adapt to sustainable potencial. If it's greater than 0 means that overexplotaion of forest leads to forest stock destruction.
    """
    return _ext_constant_p_forest_overexplotation()


_ext_constant_p_forest_overexplotation = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "forest_overexplotation",
    {},
    _root,
    "_ext_constant_p_forest_overexplotation",
)


def p_minimum_forest():
    """
    Real Name: P minimum forest
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Minimum surface of forest land accepted.
    """
    return _ext_constant_p_minimum_forest()


_ext_constant_p_minimum_forest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "minimum_forest",
    {},
    _root,
    "_ext_constant_p_minimum_forest",
)


def p_urban_land_density():
    """
    Real Name: P urban land density
    Original Eqn:
    Units: m2/people
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy target to set urban land density in a target year.
    """
    return _ext_constant_p_urban_land_density()


_ext_constant_p_urban_land_density = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "urban_land_density",
    {},
    _root,
    "_ext_constant_p_urban_land_density",
)


def p_variation_primary_forest():
    """
    Real Name: P variation primary forest
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy target to increase/decrease the rate of expansion of primary forest.
    """
    return _ext_constant_p_variation_primary_forest()


_ext_constant_p_variation_primary_forest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "variation_primary_forest",
    {},
    _root,
    "_ext_constant_p_variation_primary_forest",
)


def permanent_snowsglaciers_area():
    """
    Real Name: "permanent snows&glaciers area"
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Permanent snow & glaciers from FAOSTAT.
    """
    return _integ_permanent_snowsglaciers_area()


_integ_permanent_snowsglaciers_area = Integ(
    lambda: 0,
    lambda: initial_permanent_snowsglaciers_area(),
    "_integ_permanent_snowsglaciers_area",
)


def primary_forests_area():
    """
    Real Name: Primary forests area
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Primary forests area.
    """
    return _integ_primary_forests_area()


_integ_primary_forests_area = Integ(
    lambda: available_to_primary_forest_rate(),
    lambda: initial_primary_forest_area(),
    "_integ_primary_forests_area",
)


@subs(["RES elec"], _subscript_dict)
def shortage_bioe_for_elec():
    """
    Real Name: shortage BioE for elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary, Constant
    Subs: ['RES elec']

    Shortage of bioenergy for supplying RES power plants for electricity generation.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = 1
    value.loc[{"RES elec": ["geot elec"]}] = 1
    value.loc[{"RES elec": ["solid bioE elec"]}] = shortage_bioe_non_trad_delayed_1yr()
    value.loc[{"RES elec": ["oceanic"]}] = 1
    value.loc[{"RES elec": ["wind onshore"]}] = 1
    value.loc[{"RES elec": ["wind offshore"]}] = 1
    value.loc[{"RES elec": ["solar PV"]}] = 1
    value.loc[{"RES elec": ["CSP"]}] = 1
    return value


@subs(["RES heat"], _subscript_dict)
def shortage_bioe_for_heat():
    """
    Real Name: shortage BioE for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary, Constant
    Subs: ['RES heat']

    Shortage of bioenergy for supplying RES power plants for heat generation.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = 1
    value.loc[{"RES heat": ["geot heat"]}] = 1
    value.loc[{"RES heat": ["solid bioE heat"]}] = shortage_bioe_non_trad_delayed_1yr()
    return value


def shortage_bioe_non_trad():
    """
    Real Name: shortage BioE non trad
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Shortage of bioenergy for modern energy uses (no traditional).
    """
    return zidz(
        consum_forest_energy_non_traditional_ej(),
        demand_forest_energy_non_tradition_ej(),
    )


def shortage_bioe_non_trad_delayed_1yr():
    """
    Real Name: shortage BioE non trad delayed 1yr
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def start_year_p_urban_land_density():
    """
    Real Name: Start year P urban land density
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Start year of the policy target to modify urban land density.
    """
    return _ext_constant_start_year_p_urban_land_density()


_ext_constant_start_year_p_urban_land_density = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_P_urban_land_density",
    {},
    _root,
    "_ext_constant_start_year_p_urban_land_density",
)


def start_year_p_variation_primary_forest():
    """
    Real Name: Start year P variation primary forest
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Start year of the policy target to increase primary forests area.
    """
    return _ext_constant_start_year_p_variation_primary_forest()


_ext_constant_start_year_p_variation_primary_forest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_variation_primary_forest",
    {},
    _root,
    "_ext_constant_start_year_p_variation_primary_forest",
)


def target_year_p_urban_land_density():
    """
    Real Name: Target year P urban land density
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Target year of the policy target to modify urban land density.
    """
    return _ext_constant_target_year_p_urban_land_density()


_ext_constant_target_year_p_urban_land_density = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_P_urban_land_density",
    {},
    _root,
    "_ext_constant_target_year_p_urban_land_density",
)


def total_demand_energy_forest_ej():
    """
    Real Name: total demand energy forest EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand of forest energy.
    """
    return (
        demand_forest_energy_non_tradition_ej() + demand_forest_energy_traditional_ej()
    )


def total_demand_forest_biomass_ej():
    """
    Real Name: total demand forest biomass EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand of wood products from forest for all uses
    """
    return (
        demand_forest_energy_non_tradition_ej()
        + demand_forest_energy_traditional_ej()
        + demand_wood_products_ej()
    )


def total_eu_land_endogenous():
    """
    Real Name: Total EU land endogenous
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        agricultural_land()
        + compet_agricultural_land_for_biofuels()
        + available_forest_area()
        + land_for_solar_and_hydro_res()
        + marginal_land_for_biofuels()
        + permanent_snowsglaciers_area()
        + primary_forests_area()
        + urban_land()
        + available_land()
    )


def total_land_occupied_by_res():
    """
    Real Name: Total land occupied by RES
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total land occupied by RES (biofuel crops and RES elec PV on land, CSP and hydro).
    """
    return (
        compet_agricultural_land_for_biofuels()
        + land_for_solar_and_hydro_res()
        + marginal_land_for_biofuels()
    )


def unsustainable_loggin():
    """
    Real Name: unsustainable loggin
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Loss of forest land due to overexplotation of forest for energy uses.
    """
    return np.maximum(
        0,
        (forest_extraction_ej() - max_sustainable_forest_extraction_ej())
        * forest_stock_ratio(),
    )


def urban_land():
    """
    Real Name: Urban land
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Land for urban uses and infraestructures. Corresponds with FAOSTAT category "Artificial surfaces (including urban and associated areas)".
    """
    return _integ_urban_land()


_integ_urban_land = Integ(
    lambda: urban_land_rate(), lambda: initial_urban_land(), "_integ_urban_land"
)


def urban_land_density():
    """
    Real Name: urban land density
    Original Eqn:
    Units: m2/people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
                + (p_urban_land_density() - historic_urban_land_density())
                * (time() - start_year_p_urban_land_density())
                / (
                    target_year_p_urban_land_density()
                    - start_year_p_urban_land_density()
                ),
                lambda: p_urban_land_density(),
            ),
        ),
    )


def urban_land_density_t1():
    """
    Real Name: "urban land density t-1"
    Original Eqn:
    Units: m2/person
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Policy target to set urban land density in a target year delayed 1 year.
    """
    return _delayfixed_urban_land_density_t1()


_delayfixed_urban_land_density_t1 = DelayFixed(
    lambda: urban_land_density(),
    lambda: 1,
    lambda: 108.5,
    time_step,
    "_delayfixed_urban_land_density_t1",
)


def urban_land_density_variation():
    """
    Real Name: urban land density variation
    Original Eqn:
    Units: m2/people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Urban land density annual variation.
    """
    return urban_land_density() - urban_land_density_t1()


def urban_land_rate():
    """
    Real Name: urban land rate
    Original Eqn:
    Units: MHa/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Rate of urban surface rate.
    """
    return if_then_else(
        time() < 2014,
        lambda: hist_variation_urban_land(),
        lambda: 0.0478639 * urban_land_density_variation()
        + 1.99746 * 1e-08 * pop_variation(),
    )


def wood_energy_density():
    """
    Real Name: wood energy density
    Original Eqn:
    Units: EJ/m3
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average energy of wood products.
    """
    return _ext_constant_wood_energy_density()


_ext_constant_wood_energy_density = ExtConstant(
    "../land.xlsx",
    "Global",
    "wood_energy_density",
    {},
    _root,
    "_ext_constant_wood_energy_density",
)
