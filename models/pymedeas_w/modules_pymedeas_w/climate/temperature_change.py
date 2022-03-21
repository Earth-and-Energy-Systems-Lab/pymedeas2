"""
Module temperature_change
Translated using PySD version 2.2.3
"""


def nvs_2x_co2_forcing():
    """
    Real Name: "2x CO2 Forcing"
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return reference_co2_radiative_forcing() * np.log(2)


def atm_and_upper_ocean_heat_cap():
    """
    Real Name: Atm and Upper Ocean Heat Cap
    Original Eqn:
    Units: W*year/m2/DegreesC
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Volumetric heat capacity for the land, atmosphere,and upper ocean layer, i.e., upper layer heat capacity Ru.
    """
    return upper_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


def climate_feedback_param():
    """
    Real Name: Climate Feedback Param
    Original Eqn:
    Units: (W/m2)/DegreesC
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Climate Feedback Parameter - determines feedback effect from temperature increase.
    """
    return nvs_2x_co2_forcing() / climate_sensitivity_to_2x_co2()


def climate_sensitivity_to_2x_co2():
    """
    Real Name: climate sensitivity to 2x CO2
    Original Eqn:
    Units: ºC
    Limits: (None, None)
    Type: Constant
    Subs: []

    [Fiddaman] Equilibrium temperature change in response to a 2xCO2 equivalent change in radiative forcing. /2.908 /. [DICE-2013R] t2xco2 Equilibrium temp impact (ºC per doubling CO2) /2.9 /
    """
    return _ext_constant_climate_sensitivity_to_2x_co2()


_ext_constant_climate_sensitivity_to_2x_co2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "climate_sensitivity_to_2x_CO2",
    {},
    _root,
    "_ext_constant_climate_sensitivity_to_2x_co2",
)


@subs(["Layers"], _subscript_dict)
def deep_ocean_heat_cap():
    """
    Real Name: Deep Ocean Heat Cap
    Original Eqn:
    Units: W*year/m2/DegreesC
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['Layers']

    Volumetric heat capacity for the deep ocean by layer, i.e., lower layer heat capacity Ru.
    """
    return lower_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


def earth_surface_area():
    """
    Real Name: earth surface area
    Original Eqn:
    Units: m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    Global surface area.
    """
    return 510000000000000.0


def feedback_cooling():
    """
    Real Name: Feedback Cooling
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Feedback cooling of atmosphere/upper ocean system due to blackbody radiation. [Cowles, pg. 27]
    """
    return temperature_change() * climate_feedback_param()


def heat_diffusion_covar():
    """
    Real Name: heat diffusion covar
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Fraction of heat transfer that depends on eddy diffusion.
    """
    return _ext_constant_heat_diffusion_covar()


_ext_constant_heat_diffusion_covar = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_diffusion_covar",
    {},
    _root,
    "_ext_constant_heat_diffusion_covar",
)


def heat_in_atmosphere_and_upper_ocean():
    """
    Real Name: Heat in Atmosphere and Upper Ocean
    Original Eqn:
    Units: W*year/m2
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


@subs(["Layers"], _subscript_dict)
def heat_in_deep_ocean():
    """
    Real Name: Heat in Deep Ocean
    Original Eqn:
    Units: W*year/m2
    Limits: (None, None)
    Type: Stateful
    Subs: ['Layers']

    Heat content of each layer of the deep ocean.
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[
        {"Layers": ["Layer1", "Layer2", "Layer3"]}
    ] = _integ_heat_in_deep_ocean().values
    value.loc[{"Layers": ["Layer4"]}] = _integ_heat_in_deep_ocean_1().values
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


@subs(["Layers"], _subscript_dict)
def heat_transfer():
    """
    Real Name: Heat Transfer
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['Layers']

    Heat Transfer from the Atmosphere & Upper Ocean to the Deep Ocean
    """
    value = xr.DataArray(np.nan, {"Layers": _subscript_dict["Layers"]}, ["Layers"])
    value.loc[{"Layers": ["Layer1"]}] = (
        (temperature_change() - float(relative_deep_ocean_temp().loc["Layer1"]))
        * heat_transfer_coeff()
        / float(mean_depth_of_adjacent_layers().loc["Layer1"])
    )
    value.loc[{"Layers": ["Layer2", "Layer3", "Layer4"]}] = (
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


def heat_transfer_coeff():
    """
    Real Name: Heat Transfer Coeff
    Original Eqn:
    Units: W/m2/(DegreesC/meter)
    Limits: (0.0, 1.0)
    Type: Auxiliary
    Subs: []

    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector, is a function of the ratio of the actual to the mean of the eddy diffusion coefficient, which controls the movement of carbon through the deep ocean.
    """
    return (
        heat_transfer_rate() * float(mean_depth_of_adjacent_layers().loc["Layer1"])
    ) * (
        heat_diffusion_covar() * (eddy_diffusion_coef() / eddy_diffusion_mean())
        + (1 - heat_diffusion_covar())
    )


def heat_transfer_rate():
    """
    Real Name: heat transfer rate
    Original Eqn:
    Units: W/m2/DegreesC
    Limits: (0.0, 2.0)
    Type: Constant
    Subs: []


    """
    return _ext_constant_heat_transfer_rate()


_ext_constant_heat_transfer_rate = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_transfer_rate",
    {},
    _root,
    "_ext_constant_heat_transfer_rate",
)


def init_atm_uppocean_temperature_ano():
    """
    Real Name: init atm uppocean temperature ano
    Original Eqn:
    Units: DegreesC
    Limits: (None, None)
    Type: Constant
    Subs: []

    Global Annual Temperature Anomaly (Land + Ocean) in 1990 from NASA GISS Surface Temperature (GISTEMP): +0.43 ºC. 5-year average: +0.36 ºC. Average 1880-1889 = -0,225. Preindustrial reference: 0,36 + 0,225 = 0,585 http://cdiac.ornl.gov/ftp/trends/temp/hansen/gl_land_ocean.txt
    """
    return _ext_constant_init_atm_uppocean_temperature_ano()


_ext_constant_init_atm_uppocean_temperature_ano = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_atm_uppocean_temperature_ano",
    {},
    _root,
    "_ext_constant_init_atm_uppocean_temperature_ano",
)


@subs(["Layers"], _subscript_dict)
def init_deep_ocean_temperature():
    """
    Real Name: init deep ocean temperature
    Original Eqn:
    Units: ºC
    Limits: (None, None)
    Type: Constant
    Subs: ['Layers']

    C-ROADS simulation
    """
    return _ext_constant_init_deep_ocean_temperature()


_ext_constant_init_deep_ocean_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_deep_ocean_temperature*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    "_ext_constant_init_deep_ocean_temperature",
)


def land_area_fraction():
    """
    Real Name: land area fraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Fraction of global surface area that is land.
    """
    return 0.292


def land_thickness():
    """
    Real Name: land thickness
    Original Eqn:
    Units: m
    Limits: (None, None)
    Type: Constant
    Subs: []

    Effective land area heat capacity, expressed as equivalent water layer thickness.
    """
    return _ext_constant_land_thickness()


_ext_constant_land_thickness = ExtConstant(
    "../climate.xlsx",
    "World",
    "land_thickness",
    {},
    _root,
    "_ext_constant_land_thickness",
)


@subs(["Layers"], _subscript_dict)
def lower_layer_volume_vu():
    """
    Real Name: lower layer volume Vu
    Original Eqn:
    Units: m3
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['Layers']

    Water equivalent volume of the deep ocean by layer.
    """
    return earth_surface_area() * (1 - land_area_fraction()) * layer_depth()


def reference_co2_radiative_forcing():
    """
    Real Name: reference CO2 radiative forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    Coefficient of radiative forcing from CO2 From IPCC
    """
    return _ext_constant_reference_co2_radiative_forcing()


_ext_constant_reference_co2_radiative_forcing = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_CO2_radiative_forcing",
    {},
    _root,
    "_ext_constant_reference_co2_radiative_forcing",
)


@subs(["Layers"], _subscript_dict)
def relative_deep_ocean_temp():
    """
    Real Name: Relative Deep Ocean Temp
    Original Eqn:
    Units: DegreesC
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['Layers']

    Temperature of each layer of the deep ocean.
    """
    return heat_in_deep_ocean() / deep_ocean_heat_cap()


def temperature_change():
    """
    Real Name: Temperature change
    Original Eqn:
    Units: DegreesC
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Temperature of the Atmosphere and Upper Ocean, relative to preindustrial reference period
    """
    return heat_in_atmosphere_and_upper_ocean() / atm_and_upper_ocean_heat_cap()


def upper_layer_volume_vu():
    """
    Real Name: upper layer volume Vu
    Original Eqn:
    Units: m3
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Water equivalent volume of the upper box, which is a weighted combination of land, atmosphere,and upper ocean volumes.
    """
    return earth_surface_area() * (
        land_area_fraction() * land_thickness()
        + (1 - land_area_fraction()) * mixed_layer_depth()
    )


def volumetric_heat_capacity():
    """
    Real Name: volumetric heat capacity
    Original Eqn:
    Units: W*year/m3/ºC
    Limits: (None, None)
    Type: Constant
    Subs: []

    Volumetric heat capacity of water, i.e., amount of heat in watt*year required to raise 1 cubic meter of water by one degree C. Computed from 4.186e6/365/3600/24.
    """
    return 0.132737
