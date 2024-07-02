"""
Module climate.carbon_cycle
Translated using PySD version 3.14.0
"""

@component.add(
    name="atm_ocean_mixing_time",
    units="year",
    limits=(0.25, 10.0, 0.25),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_atm_ocean_mixing_time"},
)
def atm_ocean_mixing_time():
    """
    Atmosphere - mixed ocean layer mixing time.
    """
    return _ext_constant_atm_ocean_mixing_time()


_ext_constant_atm_ocean_mixing_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "atm_ocean_mixing_time",
    {},
    _root,
    {},
    "_ext_constant_atm_ocean_mixing_time",
)


@component.add(
    name="biomass_residence_time",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_biomass_residence_time"},
)
def biomass_residence_time():
    """
    Average residence time of carbon in biomass.
    """
    return _ext_constant_biomass_residence_time()


_ext_constant_biomass_residence_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "biomass_residence_time",
    {},
    _root,
    {},
    "_ext_constant_biomass_residence_time",
)


@component.add(
    name="biostim_coeff",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biostim_coeff_index": 1, "biostim_coeff_mean": 1},
)
def biostim_coeff():
    """
    Coefficient for response of primary production to carbon concentration.
    """
    return biostim_coeff_index() * biostim_coeff_mean()


@component.add(
    name="biostim_coeff_index",
    units="Dmnl",
    limits=(0.6, 1.7, 0.05),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_biostim_coeff_index"},
)
def biostim_coeff_index():
    """
    Index of coefficient for response of primary production to carbon concentration, as multiplying factor of the mean value.
    """
    return _ext_constant_biostim_coeff_index()


_ext_constant_biostim_coeff_index = ExtConstant(
    "../climate.xlsx",
    "World",
    "biostim_coeff_index",
    {},
    _root,
    {},
    "_ext_constant_biostim_coeff_index",
)


@component.add(
    name="biostim_coeff_mean",
    units="Dmnl",
    limits=(0.3, 0.7),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_biostim_coeff_mean"},
)
def biostim_coeff_mean():
    """
    Mean coefficient for response of primary production to CO2 concentration. Reflects the increase in NPP with doubling the CO2 level. Goudriaan and Ketner, 1984; Rotmans, 1990
    """
    return _ext_constant_biostim_coeff_mean()


_ext_constant_biostim_coeff_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "biostim_coeff_mean",
    {},
    _root,
    {},
    "_ext_constant_biostim_coeff_mean",
)


@component.add(
    name="buffer_C_coeff",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_buffer_c_coeff"},
)
def buffer_c_coeff():
    """
    Coefficient of CO2 concentration influence on buffer factor.
    """
    return _ext_constant_buffer_c_coeff()


_ext_constant_buffer_c_coeff = ExtConstant(
    "../climate.xlsx",
    "World",
    "buffer_C_coeff",
    {},
    _root,
    {},
    "_ext_constant_buffer_c_coeff",
)


@component.add(
    name="Buffer_Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"_active_initial_buffer_factor": 1},
    other_deps={
        "_active_initial_buffer_factor": {
            "initial": {"ref_buffer_factor": 1},
            "step": {
                "ref_buffer_factor": 1,
                "preindustrial_c_in_mixed_layer": 1,
                "c_in_mixed_layer": 1,
                "buffer_c_coeff": 1,
            },
        }
    },
)
def buffer_factor():
    """
    Buffer factor for atmosphere/mixed ocean carbon equilibration.
    """
    return active_initial(
        __data["time"].stage,
        lambda: ref_buffer_factor()
        * (c_in_mixed_layer() / preindustrial_c_in_mixed_layer()) ** buffer_c_coeff(),
        ref_buffer_factor(),
    )


@component.add(
    name="C_from_CH4_oxidation",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_uptake": 1, "gtch4_per_gtc": 1, "mtch4_per_gtch4": 1},
)
def c_from_ch4_oxidation():
    """
    Flux of C into the atmosphere from the oxidation of CH4, the mode of removal of CH4 from atmosphere.
    """
    return ch4_uptake() / gtch4_per_gtc() / mtch4_per_gtch4()


@component.add(
    name="C_humification_fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_c_humification_fraction"},
)
def c_humification_fraction():
    """
    Fraction of carbon outflow from biomass that enters humus stock.
    """
    return _ext_constant_c_humification_fraction()


_ext_constant_c_humification_fraction = ExtConstant(
    "../climate.xlsx",
    "World",
    "C_humification_fraction",
    {},
    _root,
    {},
    "_ext_constant_c_humification_fraction",
)


@component.add(
    name="C_humus_residence_time",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_c_humus_residence_time"},
)
def c_humus_residence_time():
    """
    Average carbon residence time in humus.
    """
    return _ext_constant_c_humus_residence_time()


_ext_constant_c_humus_residence_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "C_humus_residence_time",
    {},
    _root,
    {},
    "_ext_constant_c_humus_residence_time",
)


@component.add(
    name="C_in_Atmosphere",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_atmosphere": 1},
    other_deps={
        "_integ_c_in_atmosphere": {
            "initial": {"init_c_in_atm": 1},
            "step": {
                "c_from_ch4_oxidation": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_humus_to_atmosphere": 1,
                "total_c_anthro_emissions": 1,
                "flux_atm_to_biomass": 1,
                "flux_atm_to_ocean": 1,
                "flux_c_from_permafrost_release": 1,
            },
        }
    },
)
def c_in_atmosphere():
    """
    Carbon in atmosphere.
    """
    return _integ_c_in_atmosphere()


_integ_c_in_atmosphere = Integ(
    lambda: c_from_ch4_oxidation()
    + flux_biomass_to_atmosphere()
    + flux_humus_to_atmosphere()
    + total_c_anthro_emissions()
    - flux_atm_to_biomass()
    - flux_atm_to_ocean()
    + flux_c_from_permafrost_release(),
    lambda: init_c_in_atm(),
    "_integ_c_in_atmosphere",
)


@component.add(
    name="C_in_Biomass",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_biomass": 1},
    other_deps={
        "_integ_c_in_biomass": {
            "initial": {"init_c_in_biomass": 1},
            "step": {
                "flux_atm_to_biomass": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_biomass_to_ch4": 1,
                "flux_biomass_to_humus": 1,
            },
        }
    },
)
def c_in_biomass():
    """
    Carbon in biomass.
    """
    return _integ_c_in_biomass()


_integ_c_in_biomass = Integ(
    lambda: flux_atm_to_biomass()
    - flux_biomass_to_atmosphere()
    - flux_biomass_to_ch4()
    - flux_biomass_to_humus(),
    lambda: init_c_in_biomass(),
    "_integ_c_in_biomass",
)


@component.add(
    name="C_in_Deep_Ocean",
    units="GtC",
    subscripts=["Layers"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean": 1, "_integ_c_in_deep_ocean_1": 1},
    other_deps={
        "_integ_c_in_deep_ocean": {
            "initial": {"init_c_in_deep_ocean": 1, "layer_depth": 1},
            "step": {"diffusion_flux": 2},
        },
        "_integ_c_in_deep_ocean_1": {
            "initial": {"init_c_in_deep_ocean": 1, "layer_depth": 1},
            "step": {"diffusion_flux": 1},
        },
    },
)
def c_in_deep_ocean():
    """
    Carbon in deep ocean.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[_subscript_dict["upper"]] = _integ_c_in_deep_ocean().values
    value.loc[["Layer4"]] = _integ_c_in_deep_ocean_1().values
    return value


_integ_c_in_deep_ocean = Integ(
    lambda: diffusion_flux().loc[_subscript_dict["upper"]].rename({"Layers": "upper"})
    - xr.DataArray(
        diffusion_flux()
        .loc[_subscript_dict["lower"]]
        .rename({"Layers": "lower"})
        .values,
        {"upper": _subscript_dict["upper"]},
        ["upper"],
    ),
    lambda: init_c_in_deep_ocean()
    .loc[_subscript_dict["upper"]]
    .rename({"Layers": "upper"})
    * layer_depth().loc[_subscript_dict["upper"]].rename({"Layers": "upper"}),
    "_integ_c_in_deep_ocean",
)

_integ_c_in_deep_ocean_1 = Integ(
    lambda: xr.DataArray(
        float(diffusion_flux().loc["Layer4"]), {"Layers": ["Layer4"]}, ["Layers"]
    ),
    lambda: xr.DataArray(
        float(init_c_in_deep_ocean().loc["Layer4"])
        * float(layer_depth().loc["Layer4"]),
        {"Layers": ["Layer4"]},
        ["Layers"],
    ),
    "_integ_c_in_deep_ocean_1",
)


@component.add(
    name="C_in_deep_ocean_per_meter",
    units="GtC/meter",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean": 1, "layer_depth": 1},
)
def c_in_deep_ocean_per_meter():
    """
    Concentration of carbon in ocean layers.
    """
    return c_in_deep_ocean() / layer_depth()


@component.add(
    name="C_in_Humus",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_humus": 1},
    other_deps={
        "_integ_c_in_humus": {
            "initial": {"init_c_in_humus": 1},
            "step": {
                "flux_biomass_to_humus": 1,
                "flux_humus_to_atmosphere": 1,
                "flux_humus_to_ch4": 1,
            },
        }
    },
)
def c_in_humus():
    """
    Carbon in humus.
    """
    return _integ_c_in_humus()


_integ_c_in_humus = Integ(
    lambda: flux_biomass_to_humus() - flux_humus_to_atmosphere() - flux_humus_to_ch4(),
    lambda: init_c_in_humus(),
    "_integ_c_in_humus",
)


@component.add(
    name="C_in_Mixed_Layer",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_mixed_layer": 1},
    other_deps={
        "_integ_c_in_mixed_layer": {
            "initial": {"init_c_in_mixed_ocean": 1, "mixed_layer_depth": 1},
            "step": {"flux_atm_to_ocean": 1, "diffusion_flux": 1},
        }
    },
)
def c_in_mixed_layer():
    """
    Carbon in mixed layer.
    """
    return _integ_c_in_mixed_layer()


_integ_c_in_mixed_layer = Integ(
    lambda: flux_atm_to_ocean() - float(diffusion_flux().loc["Layer1"]),
    lambda: init_c_in_mixed_ocean() * mixed_layer_depth(),
    "_integ_c_in_mixed_layer",
)


@component.add(
    name="C_in_mixed_layer_per_meter",
    units="GtC/meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def c_in_mixed_layer_per_meter():
    return c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="CH4_generation_rate_from_biomass",
    units="1/year",
    limits=(0.0, 0.00014),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ch4_generation_rate_from_biomass"},
)
def ch4_generation_rate_from_biomass():
    """
    The rate of the natural flux of methane from C in biomass. The sum of the flux of methane from C in humus and the flux of methane from C in biomass yields the natural emissions of methane.
    """
    return _ext_constant_ch4_generation_rate_from_biomass()


_ext_constant_ch4_generation_rate_from_biomass = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_generation_rate_from_biomass",
    {},
    _root,
    {},
    "_ext_constant_ch4_generation_rate_from_biomass",
)


@component.add(
    name="CH4_generation_rate_from_humus",
    units="1/year",
    limits=(0.0, 0.00016),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ch4_generation_rate_from_humus"},
)
def ch4_generation_rate_from_humus():
    """
    The rate of the natural flux of methane from C in humus. The sum of the flux of methane from C in humus and the flux of methane from C in biomass yields the natural emissions of methane.
    """
    return _ext_constant_ch4_generation_rate_from_humus()


_ext_constant_ch4_generation_rate_from_humus = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_generation_rate_from_humus",
    {},
    _root,
    {},
    "_ext_constant_ch4_generation_rate_from_humus",
)


@component.add(
    name="CO2_ppm_concentrations",
    units="ppm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "gtc_per_ppm": 1},
)
def co2_ppm_concentrations():
    """
    1 part per million of atmospheric CO2 is equivalent to 2.13 gigatonnes Carbon. Historical Mauna Loa CO2 Record: ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt
    """
    return c_in_atmosphere() / gtc_per_ppm()


@component.add(
    name="Diffusion_Flux",
    units="GtC/year",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_mixed_layer_per_meter": 1,
        "c_in_deep_ocean_per_meter": 3,
        "eddy_diffusion_coef": 2,
        "mean_depth_of_adjacent_layers": 2,
    },
)
def diffusion_flux():
    """
    Diffusion flux between ocean layers.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[["Layer1"]] = (
        (
            c_in_mixed_layer_per_meter()
            - float(c_in_deep_ocean_per_meter().loc["Layer1"])
        )
        * eddy_diffusion_coef()
        / float(mean_depth_of_adjacent_layers().loc["Layer1"])
    )
    value.loc[_subscript_dict["lower"]] = (
        (
            xr.DataArray(
                c_in_deep_ocean_per_meter()
                .loc[_subscript_dict["upper"]]
                .rename({"Layers": "upper"})
                .values,
                {"lower": _subscript_dict["lower"]},
                ["lower"],
            )
            - c_in_deep_ocean_per_meter()
            .loc[_subscript_dict["lower"]]
            .rename({"Layers": "lower"})
        )
        * eddy_diffusion_coef()
        / mean_depth_of_adjacent_layers()
        .loc[_subscript_dict["lower"]]
        .rename({"Layers": "lower"})
    ).values
    return value


@component.add(
    name="eddy_diffusion_coef",
    units="m*m/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diffusion_coef_index": 1, "eddy_diffusion_mean": 1},
)
def eddy_diffusion_coef():
    """
    Multiplier of eddy diffusion coefficient mean
    """
    return eddy_diffusion_coef_index() * eddy_diffusion_mean()


@component.add(
    name="eddy_diffusion_coef_index",
    units="Dmnl",
    limits=(0.85, 1.15, 0.05),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eddy_diffusion_coef_index"},
)
def eddy_diffusion_coef_index():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value (defaulted to 4400 m2/year).
    """
    return _ext_constant_eddy_diffusion_coef_index()


_ext_constant_eddy_diffusion_coef_index = ExtConstant(
    "../climate.xlsx",
    "World",
    "eddy_diffusion_coef_index",
    {},
    _root,
    {},
    "_ext_constant_eddy_diffusion_coef_index",
)


@component.add(
    name="eddy_diffusion_mean",
    units="m*m/year",
    limits=(2000.0, 8000.0),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eddy_diffusion_mean"},
)
def eddy_diffusion_mean():
    """
    Rate of vertical transport and mixing in the ocean due to eddy diffusion motion.
    """
    return _ext_constant_eddy_diffusion_mean()


_ext_constant_eddy_diffusion_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "eddy_diffusion_mean",
    {},
    _root,
    {},
    "_ext_constant_eddy_diffusion_mean",
)


@component.add(
    name="Effect_of_Temp_on_DIC_pCO2",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sensitivity_of_pco2_dic_to_temperature": 1, "temperature_change": 1},
)
def effect_of_temp_on_dic_pco2():
    """
    The fractional reduction in the solubility of CO2 in ocean falls with rising temperatures. We assume a linear relationship, likely a good approximation over the typical range for warming by 2100.
    """
    return 1 - sensitivity_of_pco2_dic_to_temperature() * temperature_change()


@component.add(
    name="Effect_of_Warming_on_C_flux_to_biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "strength_of_temp_effect_on_c_flux_to_land": 1,
        "temperature_change": 1,
    },
)
def effect_of_warming_on_c_flux_to_biomass():
    """
    The fractional reduction in the flux of C from the atmosphere to biomass with rising temperatures. We assume a linear relationship, likely a good approxim
    """
    return 1 + strength_of_temp_effect_on_c_flux_to_land() * temperature_change()


@component.add(
    name="Effect_of_Warming_on_CH4_Release_from_Biological_Activity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_methane_emissions_to_temperature": 1,
        "temperature_change": 1,
        "reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration": 1,
    },
)
def effect_of_warming_on_ch4_release_from_biological_activity():
    """
    The fractional increase in the flux of C as CH4 from humus with rising temperatures. We assume a linear relationship, likely a good approximation over the typical range for warming by 2100.
    """
    return (
        1
        + sensitivity_of_methane_emissions_to_temperature()
        * temperature_change()
        / reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration()
    )


@component.add(
    name="Equil_C_in_Mixed_Layer",
    units="GtC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "preindustrial_c_in_mixed_layer": 1,
        "effect_of_temp_on_dic_pco2": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c": 1,
        "buffer_factor": 1,
    },
)
def equil_c_in_mixed_layer():
    """
    Equilibrium carbon content of mixed layer. Determined by the Revelle buffering factor, and by temperature. For simplicity, we assume a linear impact of warming on the equilibrium solubility of CO2 in the ocean.
    """
    return (
        preindustrial_c_in_mixed_layer()
        * effect_of_temp_on_dic_pco2()
        * (c_in_atmosphere() / preindustrial_c()) ** (1 / buffer_factor())
    )


@component.add(
    name="Equilibrium_C_per_meter_in_Mixed_Layer",
    units="GtC/meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equil_c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def equilibrium_c_per_meter_in_mixed_layer():
    """
    The equilibrium concentration of C in the mixed layer, in GtC/meter, based on the total quantity of C in that layer and the average layer depth.
    """
    return equil_c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="Flux_Atm_to_Biomass",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_npp": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c": 1,
        "biostim_coeff": 1,
        "effect_of_warming_on_c_flux_to_biomass": 1,
    },
)
def flux_atm_to_biomass():
    """
    Carbon flux from atmosphere to biosphere (from primary production)
    """
    return (
        init_npp()
        * (1 + biostim_coeff() * np.log(c_in_atmosphere() / preindustrial_c()))
        * effect_of_warming_on_c_flux_to_biomass()
    )


@component.add(
    name="Flux_Atm_to_Ocean",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "equil_c_in_mixed_layer": 1,
        "c_in_mixed_layer": 1,
        "atm_ocean_mixing_time": 1,
    },
)
def flux_atm_to_ocean():
    """
    Carbon flux from atmosphere to mixed ocean layer.
    """
    return (equil_c_in_mixed_layer() - c_in_mixed_layer()) / atm_ocean_mixing_time()


@component.add(
    name="Flux_Biomass_to_Atmosphere",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "biomass_residence_time": 1,
        "c_humification_fraction": 1,
    },
)
def flux_biomass_to_atmosphere():
    """
    Carbon flux from biomass to atmosphere.
    """
    return c_in_biomass() / biomass_residence_time() * (1 - c_humification_fraction())


@component.add(
    name="Flux_Biomass_to_CH4",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "ch4_generation_rate_from_biomass": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
    },
)
def flux_biomass_to_ch4():
    """
    The natural flux of methane from C in biomass. The sum of the flux of methane from C in humus and the flux of methane from C in biomass yields the natural emissions of methane. Adjusted to account for temperature feedback.
    """
    return (
        c_in_biomass()
        * ch4_generation_rate_from_biomass()
        * effect_of_warming_on_ch4_release_from_biological_activity()
    )


@component.add(
    name="Flux_Biomass_to_Humus",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "biomass_residence_time": 1,
        "c_humification_fraction": 1,
    },
)
def flux_biomass_to_humus():
    """
    Carbon flux from biomass to humus.
    """
    return c_in_biomass() / biomass_residence_time() * c_humification_fraction()


@component.add(
    name="Flux_Biosphere_to_CH4",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_biomass_to_ch4": 1, "flux_humus_to_ch4": 1},
)
def flux_biosphere_to_ch4():
    """
    Carbon flux from biosphere as methane, in GtC/year, arising from anaerobic respiration.
    """
    return flux_biomass_to_ch4() + flux_humus_to_ch4()


@component.add(
    name="Flux_Humus_to_Atmosphere",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_humus": 1, "c_humus_residence_time": 1},
)
def flux_humus_to_atmosphere():
    """
    Carbon flux from humus to atmosphere.
    """
    return c_in_humus() / c_humus_residence_time()


@component.add(
    name="Flux_Humus_to_CH4",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_humus": 1,
        "ch4_generation_rate_from_humus": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
    },
)
def flux_humus_to_ch4():
    """
    The natural flux of methane from C in humus. The sum of the flux of methane from C in humus and the flux of methane from C in biomass yields the natural emissions of methane. Adjusted to account for temperature feedback.
    """
    return (
        c_in_humus()
        * ch4_generation_rate_from_humus()
        * effect_of_warming_on_ch4_release_from_biological_activity()
    )


@component.add(
    name="GtC_per_GtCO2", units="GtC/GtCO2", comp_type="Constant", comp_subtype="Normal"
)
def gtc_per_gtco2():
    """
    1 kg of CO2 contains 3/11 of carbon.
    """
    return 3 / 11


@component.add(
    name="GtC_per_ppm", units="(GtC)/ppm", comp_type="Constant", comp_subtype="Normal"
)
def gtc_per_ppm():
    """
    Conversion from ppm to GtC (1 ppm by volume of atmosphere CO2 = 2.13 Gt C (Uses atmospheric mass (Ma) = 5.137 × 10^18 kg)) CDIAC: http://cdiac.ornl.gov/pns/convert.html
    """
    return 2.13


@component.add(
    name="GtCH4_per_GtC", units="GtCH4/GtC", comp_type="Constant", comp_subtype="Normal"
)
def gtch4_per_gtc():
    """
    Molar mass ratio of CH4 to C, 16/12
    """
    return 16 / 12


@component.add(
    name="init_C_in_atm",
    units="GtC",
    limits=(500.0, 1000.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_co2_in_atm_ppm": 1, "gtc_per_ppm": 1},
)
def init_c_in_atm():
    """
    Initial C in atmosphere. [DICE-1994] Initial Greenhouse Gases in Atmosphere 1965 [M(t)] (tC equivalent). [Cowles, pg. 21] /6.77e+011 / [DICE-2013R] mat0: Initial concentration in atmosphere 2010 (GtC) /830.4 /
    """
    return init_co2_in_atm_ppm() * gtc_per_ppm()


@component.add(
    name="init_C_in_biomass",
    units="GtC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_c_in_biomass"},
)
def init_c_in_biomass():
    """
    Initial carbon in biomass.
    """
    return _ext_constant_init_c_in_biomass()


_ext_constant_init_c_in_biomass = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_biomass",
    {},
    _root,
    {},
    "_ext_constant_init_c_in_biomass",
)


@component.add(
    name="init_C_in_deep_ocean",
    units="GtC/meter",
    subscripts=["Layers"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_c_in_deep_ocean"},
)
def init_c_in_deep_ocean():
    """
    Initial carbon concentration in deep ocean layers per meter.
    """
    return _ext_constant_init_c_in_deep_ocean()


_ext_constant_init_c_in_deep_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_deep_ocean*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    {"Layers": _subscript_dict["Layers"]},
    "_ext_constant_init_c_in_deep_ocean",
)


@component.add(
    name="init_C_in_humus",
    units="GtC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_c_in_humus"},
)
def init_c_in_humus():
    """
    Inital carbon in humus.
    """
    return _ext_constant_init_c_in_humus()


_ext_constant_init_c_in_humus = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_humus",
    {},
    _root,
    {},
    "_ext_constant_init_c_in_humus",
)


@component.add(
    name="init_C_in_mixed_ocean",
    units="GtC/meter",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_c_in_mixed_ocean"},
)
def init_c_in_mixed_ocean():
    """
    Initial carbon in mixed ocean layer per meter.
    """
    return _ext_constant_init_c_in_mixed_ocean()


_ext_constant_init_c_in_mixed_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_mixed_ocean",
    {},
    _root,
    {},
    "_ext_constant_init_c_in_mixed_ocean",
)


@component.add(
    name="init_CO2_in_atm_ppm",
    units="ppm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_co2_in_atm_ppm"},
)
def init_co2_in_atm_ppm():
    """
    Initial CO2 in atmosphere. Historical Mauna Loa CO2 Record: Average between 1st and last month of 1990 was: (353.74+355.12)/2=354.43 ppm Historical Mauna Loa CO2 Record: Average between 1st and last month of 1995 was: (359.92+360.68)/2= 360.3 ppm ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt [DICE-1994] Initial Greenhouse Gases in Atmosphere 1965 [M(t)] (tC equivalent). [Cowles, pg. 21] /6.77e+011 / [DICE-2013R] mat0: Initial concentration in atmosphere 2010 (GtC) /830.4 /
    """
    return _ext_constant_init_co2_in_atm_ppm()


_ext_constant_init_co2_in_atm_ppm = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_CO2_in_atm_ppm",
    {},
    _root,
    {},
    "_ext_constant_init_co2_in_atm_ppm",
)


@component.add(
    name="init_NPP",
    units="GtC/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_npp"},
)
def init_npp():
    """
    Initial net primary production. Adapted from Goudriaan, 1984.
    """
    return _ext_constant_init_npp()


_ext_constant_init_npp = ExtConstant(
    "../climate.xlsx", "World", "init_NPP", {}, _root, {}, "_ext_constant_init_npp"
)


@component.add(
    name="layer_depth",
    units="m",
    subscripts=["Layers"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_layer_depth"},
)
def layer_depth():
    """
    Deep ocean layer thicknesses.
    """
    return _ext_constant_layer_depth()


_ext_constant_layer_depth = ExtConstant(
    "../climate.xlsx",
    "World",
    "layer_depth*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    {"Layers": _subscript_dict["Layers"]},
    "_ext_constant_layer_depth",
)


@component.add(
    name="Layer_Time_Constant",
    units="year",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "layer_depth": 2,
        "mean_depth_of_adjacent_layers": 2,
        "eddy_diffusion_coef": 2,
    },
)
def layer_time_constant():
    """
    Time constant of exchange between layers.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[["Layer1"]] = float(layer_depth().loc["Layer1"]) / (
        eddy_diffusion_coef() / float(mean_depth_of_adjacent_layers().loc["Layer1"])
    )
    value.loc[_subscript_dict["lower"]] = (
        layer_depth().loc[_subscript_dict["lower"]].rename({"Layers": "lower"})
        / (
            eddy_diffusion_coef()
            / mean_depth_of_adjacent_layers()
            .loc[_subscript_dict["lower"]]
            .rename({"Layers": "lower"})
        )
    ).values
    return value


@component.add(
    name="Mean_Depth_of_Adjacent_Layers",
    units="meter",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mixed_layer_depth": 1, "layer_depth": 3},
)
def mean_depth_of_adjacent_layers():
    """
    The mean depth of adjacent ocean layers.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[["Layer1"]] = (
        mixed_layer_depth() + float(layer_depth().loc["Layer1"])
    ) / 2
    value.loc[_subscript_dict["lower"]] = (
        (
            xr.DataArray(
                layer_depth()
                .loc[_subscript_dict["upper"]]
                .rename({"Layers": "upper"})
                .values,
                {"lower": _subscript_dict["lower"]},
                ["lower"],
            )
            + layer_depth().loc[_subscript_dict["lower"]].rename({"Layers": "lower"})
        )
        / 2
    ).values
    return value


@component.add(
    name="mixed_layer_depth",
    units="meter",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mixed_layer_depth"},
)
def mixed_layer_depth():
    """
    Mixed ocean layer depth.
    """
    return _ext_constant_mixed_layer_depth()


_ext_constant_mixed_layer_depth = ExtConstant(
    "../climate.xlsx",
    "World",
    "mixed_layer_depth",
    {},
    _root,
    {},
    "_ext_constant_mixed_layer_depth",
)


@component.add(
    name="MtCH4_per_GtCH4",
    units="MtCH4/GtCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mtch4_per_gtch4():
    """
    Converts megatonnes to gigatonnes.
    """
    return 1000


@component.add(
    name="natural_CH4_emissions",
    units="MtCH4/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_biosphere_to_ch4": 1, "gtch4_per_gtc": 1, "mtch4_per_gtch4": 1},
)
def natural_ch4_emissions():
    """
    Flux of methane from anaerobic respiration in the biosphere, in megatonnes CH4/year.
    """
    return flux_biosphere_to_ch4() * gtch4_per_gtc() * mtch4_per_gtch4()


@component.add(
    name="preindustrial_C",
    units="GtC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_c"},
)
def preindustrial_c():
    """
    Preindustrial C content of atmosphere.
    """
    return _ext_constant_preindustrial_c()


_ext_constant_preindustrial_c = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_C",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_c",
)


@component.add(
    name="preindustrial_C_in_mixed_layer",
    units="GtC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"preindustrial_c_in_ocean": 1, "mixed_layer_depth": 1},
)
def preindustrial_c_in_mixed_layer():
    """
    Initial carbon concentration of mixed ocean layer.
    """
    return preindustrial_c_in_ocean() * mixed_layer_depth()


@component.add(
    name="preindustrial_C_in_ocean",
    units="GtC/m",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_c_in_ocean"},
)
def preindustrial_c_in_ocean():
    """
    Preindustrial ocean carbon content per meter. Corresponds with 767.8 GtC in a 75m layer.
    """
    return _ext_constant_preindustrial_c_in_ocean()


_ext_constant_preindustrial_c_in_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "preind_C_in_ocean",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_c_in_ocean",
)


@component.add(
    name="Ref_Buffer_Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ref_buffer_factor"},
)
def ref_buffer_factor():
    """
    Normal buffer factor.
    """
    return _ext_constant_ref_buffer_factor()


_ext_constant_ref_buffer_factor = ExtConstant(
    "../climate.xlsx",
    "World",
    "ref_buffer_factor",
    {},
    _root,
    {},
    "_ext_constant_ref_buffer_factor",
)


@component.add(
    name="reference_temperature_change_for_effect_of_warming_on_CH4_from_respiration",
    units="ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration"
    },
)
def reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration():
    """
    Temperature change at which the C as CH4 release from humus doubles for the sensitivity of methane emissions to temperature=1.
    """
    return (
        _ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration()
    )


_ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_temperature_change_for_effect_of_warming_on_CH4_from_respiration",
    {},
    _root,
    {},
    "_ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration",
)


@component.add(
    name="sensitivity_of_C_uptake_to_temperature",
    units="Dmnl",
    limits=(0.0, 2.5, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_of_c_uptake_to_temperature"},
)
def sensitivity_of_c_uptake_to_temperature():
    """
    Strength of the feedback effect of temperature on uptake of C by land and oceans. 0 means no temperature-carbon uptake feedback and default of 1 yields the average value found in Friedlingstein et al., 2006. Climate-Carbon Cycle Feedback Analysis: ResuMCS from the C4MIP Model Intercomparison. Journal of Climate. p3337-3353.
    """
    return _ext_constant_sensitivity_of_c_uptake_to_temperature()


_ext_constant_sensitivity_of_c_uptake_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_C_uptake_to_temperature",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_of_c_uptake_to_temperature",
)


@component.add(
    name="sensitivity_of_methane_emissions_to_temperature",
    units="Dmnl",
    limits=(0.0, 2.5, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_sensitivity_of_methane_emissions_to_temperature"
    },
)
def sensitivity_of_methane_emissions_to_temperature():
    """
    Allows users to control the strength of the feedback effect of temperature on release of C as CH4 from humus. Default of 0 means no temperature feedback and 1 is mean feedback.
    """
    return _ext_constant_sensitivity_of_methane_emissions_to_temperature()


_ext_constant_sensitivity_of_methane_emissions_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_methane_emissions_to_temperature",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_of_methane_emissions_to_temperature",
)


@component.add(
    name="sensitivity_of_pCO2_DIC_to_temperature",
    units="1/ºC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_c_uptake_to_temperature": 1,
        "sensitivity_of_pco2_dic_to_temperature_mean": 1,
    },
)
def sensitivity_of_pco2_dic_to_temperature():
    """
    Sensitivity of pCO2 of dissolved inorganic carbon in ocean to temperature.
    """
    return (
        sensitivity_of_c_uptake_to_temperature()
        * sensitivity_of_pco2_dic_to_temperature_mean()
    )


@component.add(
    name="sensitivity_of_pCO2_DIC_to_temperature_mean",
    units="1/ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_sensitivity_of_pco2_dic_to_temperature_mean"
    },
)
def sensitivity_of_pco2_dic_to_temperature_mean():
    """
    Sensitivity of equilibrium concentration of dissolved inorganic carbon to temperature. Calibrated to be consistent with Friedlingstein et al., 2006. Climate-Carbon Cycle Feedback Analysis: ResuMCS from the C4MIP Model Intercomparison. Journal of Climate. p3337-3353. Default sensitivity of C uptake to temperature of 1 corresponds to mean value from the 11 models tested.
    """
    return _ext_constant_sensitivity_of_pco2_dic_to_temperature_mean()


_ext_constant_sensitivity_of_pco2_dic_to_temperature_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_pCO2_DIC_to_temperature_mean",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_of_pco2_dic_to_temperature_mean",
)


@component.add(
    name="Strength_of_Temp_Effect_on_C_Flux_to_Land",
    units="1/ºC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_c_uptake_to_temperature": 1,
        "strength_of_temp_effect_on_land_c_flux_mean": 1,
    },
)
def strength_of_temp_effect_on_c_flux_to_land():
    """
    Strength of temperature effect on C flux to the land.
    """
    return (
        sensitivity_of_c_uptake_to_temperature()
        * strength_of_temp_effect_on_land_c_flux_mean()
    )


@component.add(
    name="Strength_of_temp_effect_on_land_C_flux_mean",
    units="1/ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_strength_of_temp_effect_on_land_c_flux_mean"
    },
)
def strength_of_temp_effect_on_land_c_flux_mean():
    """
    Average effect of temperature on flux of carbon to land. Calibrated to be consistent with Friedlingstein et al., 2006. Climate-Carbon Cycle Feedback Analysis: ResuMCS from the C4MIP Model Intercomparison. Journal of Climate. p3337-3353. Default sensitivity of C uptake to temperature of 1 corresponds to mean value from the 11 models tested.
    """
    return _ext_constant_strength_of_temp_effect_on_land_c_flux_mean()


_ext_constant_strength_of_temp_effect_on_land_c_flux_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "strength_of_temp_effect_on_land_C_flux_mean",
    {},
    _root,
    {},
    "_ext_constant_strength_of_temp_effect_on_land_c_flux_mean",
)


@component.add(
    name="Total_C_anthro_emissions",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1, "gtc_per_gtco2": 1},
)
def total_c_anthro_emissions():
    """
    Total annual CO2 emissions converted to GtC/year.
    """
    return total_co2_emissions_gtco2() * gtc_per_gtco2()
