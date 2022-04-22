"""
Module temperature_change
Translated using PySD version 3.0.0
"""


@component.add(
    name='"2x CO2 Forcing"', units="W/m2", comp_type="Auxiliary", comp_subtype="Normal"
)
def nvs_2x_co2_forcing():
    return reference_co2_radiative_forcing() * np.log(2)


@component.add(
    name="Atm and Upper Ocean Heat Cap",
    units="W*year/m2/DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def atm_and_upper_ocean_heat_cap():
    """
    Volumetric heat capacity for the land, atmosphere,and upper ocean layer, i.e., upper layer heat capacity Ru.
    """
    return upper_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


@component.add(
    name="Climate Feedback Param",
    units="(W/m2)/DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def climate_feedback_param():
    """
    Climate Feedback Parameter - determines feedback effect from temperature increase.
    """
    return nvs_2x_co2_forcing() / climate_sensitivity_to_2x_co2()


@component.add(
    name="climate sensitivity to 2x CO2",
    units="ºC",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Deep Ocean Heat Cap",
    units="W*year/m2/DegreesC",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def deep_ocean_heat_cap():
    """
    Volumetric heat capacity for the deep ocean by layer, i.e., lower layer heat capacity Ru.
    """
    return lower_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


@component.add(
    name="earth surface area", units="m2", comp_type="Constant", comp_subtype="Normal"
)
def earth_surface_area():
    """
    Global surface area.
    """
    return 510000000000000.0


@component.add(
    name="Feedback Cooling", units="W/m2", comp_type="Auxiliary", comp_subtype="Normal"
)
def feedback_cooling():
    """
    Feedback cooling of atmosphere/upper ocean system due to blackbody radiation. [Cowles, pg. 27]
    """
    return temperature_change() * climate_feedback_param()


@component.add(
    name="heat diffusion covar",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Heat in Atmosphere and Upper Ocean",
    units="W*year/m2",
    comp_type="Stateful",
    comp_subtype="Integ",
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
    name="Heat in Deep Ocean",
    units="W*year/m2",
    subscripts=["Layers"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def heat_in_deep_ocean():
    """
    Heat content of each layer of the deep ocean.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[_subscript_dict["upper"]] = _integ_heat_in_deep_ocean().values
    value.loc[["Layer4"]] = _integ_heat_in_deep_ocean_1().values
    return value


_integ_heat_in_deep_ocean = Integ(
    lambda: heat_transfer().loc[_subscript_dict["upper"]].rename({"Layers": "upper"})
    - xr.DataArray(
        heat_transfer()
        .loc[_subscript_dict["lower"]]
        .rename({"Layers": "lower"})
        .values,
        {"upper": _subscript_dict["upper"]},
        ["upper"],
    ),
    lambda: init_deep_ocean_temperature()
    .loc[_subscript_dict["upper"]]
    .rename({"Layers": "upper"})
    * deep_ocean_heat_cap().loc[_subscript_dict["upper"]].rename({"Layers": "upper"}),
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
    name="Heat Transfer",
    units="W/m2",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def heat_transfer():
    """
    Heat Transfer from the Atmosphere & Upper Ocean to the Deep Ocean
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
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
                .rename({"Layers": "upper"})
                .values,
                {"lower": _subscript_dict["lower"]},
                ["lower"],
            )
            - relative_deep_ocean_temp()
            .loc[_subscript_dict["lower"]]
            .rename({"Layers": "lower"})
        )
        * heat_transfer_coeff()
        / mean_depth_of_adjacent_layers()
        .loc[_subscript_dict["lower"]]
        .rename({"Layers": "lower"})
    ).values
    return value


@component.add(
    name="Heat Transfer Coeff",
    units="W/m2/(DegreesC/meter)",
    limits=(0.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="heat transfer rate",
    units="W/m2/DegreesC",
    limits=(0.0, 2.0),
    comp_type="Constant",
    comp_subtype="External",
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
    name="init atm uppocean temperature ano",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="External",
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
    name="init deep ocean temperature",
    units="ºC",
    subscripts=["Layers"],
    comp_type="Constant",
    comp_subtype="External",
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
    name="land area fraction", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def land_area_fraction():
    """
    Fraction of global surface area that is land.
    """
    return 0.292


@component.add(
    name="land thickness", units="m", comp_type="Constant", comp_subtype="External"
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
    name="lower layer volume Vu",
    units="m3",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def lower_layer_volume_vu():
    """
    Water equivalent volume of the deep ocean by layer.
    """
    return earth_surface_area() * (1 - land_area_fraction()) * layer_depth()


@component.add(
    name="reference CO2 radiative forcing",
    units="W/m2",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Relative Deep Ocean Temp",
    units="DegreesC",
    subscripts=["Layers"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def relative_deep_ocean_temp():
    """
    Temperature of each layer of the deep ocean.
    """
    return heat_in_deep_ocean() / deep_ocean_heat_cap()


@component.add(
    name="Temperature change",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def temperature_change():
    """
    Temperature of the Atmosphere and Upper Ocean, relative to preindustrial reference period
    """
    return heat_in_atmosphere_and_upper_ocean() / atm_and_upper_ocean_heat_cap()


@component.add(
    name="upper layer volume Vu",
    units="m3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="volumetric heat capacity",
    units="W*year/m3/ºC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def volumetric_heat_capacity():
    """
    Volumetric heat capacity of water, i.e., amount of heat in watt*year required to raise 1 cubic meter of water by one degree C. Computed from 4.186e6/365/3600/24.
    """
    return 0.132737
