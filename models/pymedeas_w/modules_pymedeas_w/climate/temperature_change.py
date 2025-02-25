"""
Module climate.temperature_change
Translated using PySD version 3.14.0
"""

@component.add(
    name="Atm_and_Upper_Ocean_Heat_Cap",
    units="W*year/(m*m)/DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "upper_layer_volume_vu": 1,
        "volumetric_heat_capacity": 1,
        "earth_surface_area": 1,
    },
)
def atm_and_upper_ocean_heat_cap():
    """
    Volumetric heat capacity for the land, atmosphere,and upper ocean layer, i.e., upper layer heat capacity Ru.
    """
    return upper_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


@component.add(
    name="Climate_Feedback_Param",
    units="(W/(m*m))/DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nvs_2x_co2_forcing": 1, "climate_sensitivity_to_2x_co2": 1},
)
def climate_feedback_param():
    """
    Climate Feedback Parameter - determines feedback effect from temperature increase.
    """
    return nvs_2x_co2_forcing() / climate_sensitivity_to_2x_co2()


@component.add(
    name="climate_sensitivity_to_2x_CO2",
    units="ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_climate_sensitivity_to_2x_co2"},
)
def climate_sensitivity_to_2x_co2():
    """
    [Fiddaman] Equilibrium temperature change in response to a 2xCO2 equivalent change in radiative forcing. /2.908 /. [DICE-2013R] t2xco2 Equilibrium temp impact (ºC per doubling CO2) /2.9 /
    """
    return _ext_constant_climate_sensitivity_to_2x_co2()


_ext_constant_climate_sensitivity_to_2x_co2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "climate_sensitivity_to_2x_CO2",
    {},
    _root,
    {},
    "_ext_constant_climate_sensitivity_to_2x_co2",
)


@component.add(
    name="Deep_Ocean_Heat_Cap",
    units="W*year/(m*m)/DegreesC",
    subscripts=[np.str_("Layers")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lower_layer_volume_vu": 1,
        "volumetric_heat_capacity": 1,
        "earth_surface_area": 1,
    },
)
def deep_ocean_heat_cap():
    """
    Volumetric heat capacity for the deep ocean by layer, i.e., lower layer heat capacity Ru.
    """
    return lower_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


@component.add(
    name="earth_surface_area", units="m*m", comp_type="Constant", comp_subtype="Normal"
)
def earth_surface_area():
    """
    Global surface area.
    """
    return 510000000000000.0


@component.add(
    name="Feedback_Cooling",
    units="W/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_change": 1, "climate_feedback_param": 1},
)
def feedback_cooling():
    """
    Feedback cooling of atmosphere/upper ocean system due to blackbody radiation. [Cowles, pg. 27]
    """
    return temperature_change() * climate_feedback_param()


@component.add(
    name="heat_diffusion_covar",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_heat_diffusion_covar"},
)
def heat_diffusion_covar():
    """
    Fraction of heat transfer that depends on eddy diffusion.
    """
    return _ext_constant_heat_diffusion_covar()


_ext_constant_heat_diffusion_covar = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_diffusion_covar",
    {},
    _root,
    {},
    "_ext_constant_heat_diffusion_covar",
)


@component.add(
    name="Heat_in_Atmosphere_and_Upper_Ocean",
    units="W*year/(m*m)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_atmosphere_and_upper_ocean": 1},
    other_deps={
        "_integ_heat_in_atmosphere_and_upper_ocean": {
            "initial": {
                "init_atm_uppocean_temperature_ano": 1,
                "atm_and_upper_ocean_heat_cap": 1,
            },
            "step": {
                "effective_radiative_forcing": 1,
                "feedback_cooling": 1,
                "heat_transfer": 1,
            },
        }
    },
)
def heat_in_atmosphere_and_upper_ocean():
    """
    Heat of the Atmosphere and Upper Ocean
    """
    return _integ_heat_in_atmosphere_and_upper_ocean()


_integ_heat_in_atmosphere_and_upper_ocean = Integ(
    lambda: effective_radiative_forcing()
    - feedback_cooling()
    - float(heat_transfer().loc["Layer1"]),
    lambda: init_atm_uppocean_temperature_ano() * atm_and_upper_ocean_heat_cap(),
    "_integ_heat_in_atmosphere_and_upper_ocean",
)


@component.add(
    name="Heat_in_Deep_Ocean",
    units="W*year/(m*m)",
    subscripts=[np.str_("Layers")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_deep_ocean": 1, "_integ_heat_in_deep_ocean_1": 1},
    other_deps={
        "_integ_heat_in_deep_ocean": {
            "initial": {"init_deep_ocean_temperature": 1, "deep_ocean_heat_cap": 1},
            "step": {"heat_transfer": 2},
        },
        "_integ_heat_in_deep_ocean_1": {
            "initial": {"init_deep_ocean_temperature": 1, "deep_ocean_heat_cap": 1},
            "step": {"heat_transfer": 1},
        },
    },
)
def heat_in_deep_ocean():
    """
    Heat content of each layer of the deep ocean.
    """
    value = xr.DataArray(
        np.nan, {"Layers": _subscript_dict["Layers"]}, [np.str_("Layers")]
    )
    value.loc[_subscript_dict["upper"]] = _integ_heat_in_deep_ocean().values
    value.loc[["Layer4"]] = _integ_heat_in_deep_ocean_1().values
    return value


_integ_heat_in_deep_ocean = Integ(
    lambda: heat_transfer()
    .loc[_subscript_dict["upper"]]
    .rename({np.str_("Layers"): "upper"})
    - xr.DataArray(
        heat_transfer()
        .loc[_subscript_dict["lower"]]
        .rename({np.str_("Layers"): "lower"})
        .values,
        {"upper": _subscript_dict["upper"]},
        ["upper"],
    ),
    lambda: init_deep_ocean_temperature()
    .loc[_subscript_dict["upper"]]
    .rename({np.str_("Layers"): "upper"})
    * deep_ocean_heat_cap()
    .loc[_subscript_dict["upper"]]
    .rename({np.str_("Layers"): "upper"}),
    "_integ_heat_in_deep_ocean",
)

_integ_heat_in_deep_ocean_1 = Integ(
    lambda: xr.DataArray(
        float(heat_transfer().loc["Layer4"]), {"Layers": ["Layer4"]}, ["Layers"]
    ),
    lambda: xr.DataArray(
        float(init_deep_ocean_temperature().loc["Layer4"])
        * float(deep_ocean_heat_cap().loc["Layer4"]),
        {"Layers": ["Layer4"]},
        ["Layers"],
    ),
    "_integ_heat_in_deep_ocean_1",
)


@component.add(
    name="Heat_Transfer",
    units="W/(m*m)",
    subscripts=[np.str_("Layers")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change": 1,
        "relative_deep_ocean_temp": 3,
        "heat_transfer_coeff": 2,
        "mean_depth_of_adjacent_layers": 2,
    },
)
def heat_transfer():
    """
    Heat Transfer from the Atmosphere & Upper Ocean to the Deep Ocean
    """
    value = xr.DataArray(
        np.nan, {"Layers": _subscript_dict["Layers"]}, [np.str_("Layers")]
    )
    value.loc[["Layer1"]] = (
        (temperature_change() - float(relative_deep_ocean_temp().loc["Layer1"]))
        * heat_transfer_coeff()
        / float(mean_depth_of_adjacent_layers().loc["Layer1"])
    )
    value.loc[_subscript_dict["lower"]] = (
        (
            xr.DataArray(
                relative_deep_ocean_temp()
                .loc[_subscript_dict["upper"]]
                .rename({np.str_("Layers"): "upper"})
                .values,
                {"lower": _subscript_dict["lower"]},
                ["lower"],
            )
            - relative_deep_ocean_temp()
            .loc[_subscript_dict["lower"]]
            .rename({np.str_("Layers"): "lower"})
        )
        * heat_transfer_coeff()
        / mean_depth_of_adjacent_layers()
        .loc[_subscript_dict["lower"]]
        .rename({np.str_("Layers"): "lower"})
    ).values
    return value


@component.add(
    name="Heat_Transfer_Coeff",
    units="W/(m*m)/(DegreesC/meter)",
    limits=(0.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_transfer_rate": 1,
        "mean_depth_of_adjacent_layers": 1,
        "heat_diffusion_covar": 2,
        "eddy_diffusion_coef": 1,
        "eddy_diffusion_mean": 1,
    },
)
def heat_transfer_coeff():
    """
    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector, is a function of the ratio of the actual to the mean of the eddy diffusion coefficient, which controls the movement of carbon through the deep ocean.
    """
    return (
        heat_transfer_rate() * float(mean_depth_of_adjacent_layers().loc["Layer1"])
    ) * (
        heat_diffusion_covar() * (eddy_diffusion_coef() / eddy_diffusion_mean())
        + (1 - heat_diffusion_covar())
    )


@component.add(
    name="heat_transfer_rate",
    units="W/(m*m)/DegreesC",
    limits=(0.0, 2.0),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_heat_transfer_rate"},
)
def heat_transfer_rate():
    return _ext_constant_heat_transfer_rate()


_ext_constant_heat_transfer_rate = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_transfer_rate",
    {},
    _root,
    {},
    "_ext_constant_heat_transfer_rate",
)


@component.add(
    name="init_atm_uppocean_temperature_ano",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_atm_uppocean_temperature_ano"},
)
def init_atm_uppocean_temperature_ano():
    """
    Global Annual Temperature Anomaly (Land + Ocean) in 1990 from NASA GISS Surface Temperature (GISTEMP): +0.43 ºC. 5-year average: +0.36 ºC. Average 1880-1889 = -0,225. Preindustrial reference: 0,36 + 0,225 = 0,585 http://cdiac.ornl.gov/ftp/trends/temp/hansen/gl_land_ocean.txt
    """
    return _ext_constant_init_atm_uppocean_temperature_ano()


_ext_constant_init_atm_uppocean_temperature_ano = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_atm_uppocean_temperature_ano",
    {},
    _root,
    {},
    "_ext_constant_init_atm_uppocean_temperature_ano",
)


@component.add(
    name="init_deep_ocean_temperature",
    units="ºC",
    subscripts=[np.str_("Layers")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_deep_ocean_temperature"},
)
def init_deep_ocean_temperature():
    """
    C-ROADS simulation
    """
    return _ext_constant_init_deep_ocean_temperature()


_ext_constant_init_deep_ocean_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_deep_ocean_temperature*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    {"Layers": _subscript_dict["Layers"]},
    "_ext_constant_init_deep_ocean_temperature",
)


@component.add(
    name="land_area_fraction", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def land_area_fraction():
    """
    Fraction of global surface area that is land.
    """
    return 0.292


@component.add(
    name="land_thickness",
    units="m",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_land_thickness"},
)
def land_thickness():
    """
    Effective land area heat capacity, expressed as equivalent water layer thickness.
    """
    return _ext_constant_land_thickness()


_ext_constant_land_thickness = ExtConstant(
    "../climate.xlsx",
    "World",
    "land_thickness",
    {},
    _root,
    {},
    "_ext_constant_land_thickness",
)


@component.add(
    name="lower_layer_volume_Vu",
    units="m*m*m",
    subscripts=[np.str_("Layers")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"earth_surface_area": 1, "land_area_fraction": 1, "layer_depth": 1},
)
def lower_layer_volume_vu():
    """
    Water equivalent volume of the deep ocean by layer.
    """
    return earth_surface_area() * (1 - land_area_fraction()) * layer_depth()


@component.add(
    name='"2x_CO2_Forcing"',
    units="W/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_co2_radiative_forcing": 1},
)
def nvs_2x_co2_forcing():
    return reference_co2_radiative_forcing() * np.log(2)


@component.add(
    name="reference_CO2_radiative_forcing",
    units="W/(m*m)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_reference_co2_radiative_forcing"},
)
def reference_co2_radiative_forcing():
    """
    Coefficient of radiative forcing from CO2 From IPCC
    """
    return _ext_constant_reference_co2_radiative_forcing()


_ext_constant_reference_co2_radiative_forcing = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_CO2_radiative_forcing",
    {},
    _root,
    {},
    "_ext_constant_reference_co2_radiative_forcing",
)


@component.add(
    name="Relative_Deep_Ocean_Temp",
    units="DegreesC",
    subscripts=[np.str_("Layers")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean": 1, "deep_ocean_heat_cap": 1},
)
def relative_deep_ocean_temp():
    """
    Temperature of each layer of the deep ocean.
    """
    return heat_in_deep_ocean() / deep_ocean_heat_cap()


@component.add(
    name="Temperature_change",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_in_atmosphere_and_upper_ocean": 1,
        "atm_and_upper_ocean_heat_cap": 1,
    },
)
def temperature_change():
    """
    Temperature of the Atmosphere and Upper Ocean, relative to preindustrial reference period
    """
    return heat_in_atmosphere_and_upper_ocean() / atm_and_upper_ocean_heat_cap()


@component.add(
    name="upper_layer_volume_Vu",
    units="m*m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "earth_surface_area": 1,
        "mixed_layer_depth": 1,
        "land_area_fraction": 2,
        "land_thickness": 1,
    },
)
def upper_layer_volume_vu():
    """
    Water equivalent volume of the upper box, which is a weighted combination of land, atmosphere,and upper ocean volumes.
    """
    return earth_surface_area() * (
        land_area_fraction() * land_thickness()
        + (1 - land_area_fraction()) * mixed_layer_depth()
    )


@component.add(
    name="volumetric_heat_capacity",
    units="W*year/(m*m*m)/ºC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def volumetric_heat_capacity():
    """
    Volumetric heat capacity of water, i.e., amount of heat in watt*year required to raise 1 cubic meter of water by one degree C. Computed from 4.186e6/365/3600/24.
    """
    return 0.132737
