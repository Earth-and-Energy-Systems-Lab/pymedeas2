"""
Module temperature_change
Translated using PySD version 2.2.1
"""


def nvs_2x_co2_forcing():
    """
    Real Name: "2x CO2 Forcing"
    Original Eqn: reference CO2 radiative forcing*LN(2)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return reference_co2_radiative_forcing() * np.log(2)


def atm_and_upper_ocean_heat_cap():
    """
    Real Name: Atm and Upper Ocean Heat Cap
    Original Eqn: upper layer volume Vu*volumetric heat capacity/earth surface area
    Units: W*year/m2/DegreesC
    Limits: (None, None)
    Type: component
    Subs: None

    Volumetric heat capacity for the land, atmosphere,and upper ocean layer,
        i.e., upper layer heat capacity Ru.
    """
    return upper_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


def climate_feedback_param():
    """
    Real Name: Climate Feedback Param
    Original Eqn: "2x CO2 Forcing"/climate sensitivity to 2x CO2
    Units: (W/m2)/DegreesC
    Limits: (None, None)
    Type: component
    Subs: None

    Climate Feedback Parameter - determines feedback effect from temperature
        increase.
    """
    return nvs_2x_co2_forcing() / climate_sensitivity_to_2x_co2()


def climate_sensitivity_to_2x_co2():
    """
    Real Name: climate sensitivity to 2x CO2
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'climate_sensitivity_to_2x_CO2')
    Units: ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    [Fiddaman] Equilibrium temperature change in response to a 2xCO2 equivalent change
        in radiative forcing. /2.908 /.        [DICE-2013R] t2xco2 Equilibrium temp impact (ºC per doubling CO2) /2.9 /
    """
    return _ext_constant_climate_sensitivity_to_2x_co2()


@subs(["Layers"], _subscript_dict)
def deep_ocean_heat_cap():
    """
    Real Name: Deep Ocean Heat Cap
    Original Eqn: lower layer volume Vu[Layers]*volumetric heat capacity/earth surface area
    Units: W*year/m2/DegreesC
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Volumetric heat capacity for the deep ocean by layer, i.e., lower layer
        heat capacity Ru.
    """
    return lower_layer_volume_vu() * volumetric_heat_capacity() / earth_surface_area()


def earth_surface_area():
    """
    Real Name: earth surface area
    Original Eqn: 5.1e+14
    Units: m2
    Limits: (None, None)
    Type: constant
    Subs: None

    Global surface area.
    """
    return 5.1e14


def eddy_diffusion_coef():
    """
    Real Name: eddy diffusion coef
    Original Eqn:
      e
        .
        .
        .
      n
    Units: m2/year
    Limits: (None, None)
    Type: component
    Subs: None

    Multiplier of eddy diffusion coefficient mean
    """
    return eddy_diffusion_coef_index() * eddy_diffusion_mean()


def eddy_diffusion_coef_index():
    """
    Real Name: eddy diffusion coef index
    Original Eqn:
      G
        .
        .
        .
      )
    Units: Dmnl
    Limits: (0.85, 1.15, 0.05)
    Type: constant
    Subs: None

    Index of coefficient for rate at which carbon is mixed in the ocean due to
            eddy motion, where 1 is equivalent to the expected value (defaulted to
            4400 m2/year).
    """
    return _ext_constant_eddy_diffusion_coef_index()


def eddy_diffusion_mean():
    """
    Real Name: eddy diffusion mean
    Original Eqn:
      G
        .
        .
        .
      )
    Units: m2/year
    Limits: (2000.0, 8000.0)
    Type: constant
    Subs: None

    Rate of vertical transport and mixing in the ocean due to eddy diffusion
            motion.
    """
    return _ext_constant_eddy_diffusion_mean()


def feedback_cooling():
    """
    Real Name: Feedback Cooling
    Original Eqn: Temperature change*Climate Feedback Param
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Feedback cooling of atmosphere/upper ocean system due to blackbody
        radiation. [Cowles, pg. 27]
    """
    return temperature_change() * climate_feedback_param()


def heat_diffusion_covar():
    """
    Real Name: heat diffusion covar
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'heat_diffusion_covar')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Fraction of heat transfer that depends on eddy diffusion.
    """
    return _ext_constant_heat_diffusion_covar()


def heat_in_atmosphere_and_upper_ocean():
    """
    Real Name: Heat in Atmosphere and Upper Ocean
    Original Eqn: INTEG ( Effective Radiative Forcing -Feedback Cooling -Heat Transfer[Layer1], init atm uppocean temperature ano*Atm and Upper Ocean Heat Cap)
    Units: W*year/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Heat of the Atmosphere and Upper Ocean
    """
    return _integ_heat_in_atmosphere_and_upper_ocean()


@subs(["Layers"], _subscript_dict)
def heat_in_deep_ocean():
    """
    Real Name: Heat in Deep Ocean
    Original Eqn:
      INTEG ( Heat Transfer[upper]-Heat Transfer[lower], init deep ocean temperature[upper]*Deep Ocean Heat Cap[upper])
      INTEG ( Heat Transfer[Layer4], init deep ocean temperature[Layer4]*Deep Ocean Heat Cap[Layer4])
    Units: W*year/m2
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Heat content of each layer of the deep ocean.
    """
    return xrmerge(
        rearrange(
            _integ_heat_in_deep_ocean(),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(_integ_heat_in_deep_ocean(), ["Layers"], {"Layers": ["Layer4"]}),
    )


@subs(["Layers"], _subscript_dict)
def heat_transfer():
    """
    Real Name: Heat Transfer
    Original Eqn:
      (Temperature change-Relative Deep Ocean Temp[Layer1])*Heat Transfer Coeff/Mean Depth of Adjacent Layers [Layer1]
      (Relative Deep Ocean Temp[upper]-Relative Deep Ocean Temp[lower]) *Heat Transfer Coeff/Mean Depth of Adjacent Layers[lower]
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Heat Transfer from the Atmosphere & Upper Ocean to the Deep Ocean
    """
    return xrmerge(
        rearrange(
            (temperature_change() - float(relative_deep_ocean_temp().loc["Layer1"]))
            * heat_transfer_coeff()
            / float(mean_depth_of_adjacent_layers().loc["Layer1"]),
            ["Layers"],
            {"Layers": ["Layer1"]},
        ),
        rearrange(
            (
                rearrange(
                    rearrange(relative_deep_ocean_temp(), ["upper"], _subscript_dict),
                    ["lower"],
                    _subscript_dict,
                )
                - rearrange(relative_deep_ocean_temp(), ["lower"], _subscript_dict)
            )
            * heat_transfer_coeff()
            / rearrange(mean_depth_of_adjacent_layers(), ["lower"], _subscript_dict),
            ["Layers"],
            {"Layers": ["Layer2", "Layer3", "Layer4"]},
        ),
    )


def heat_transfer_coeff():
    """
    Real Name: Heat Transfer Coeff
    Original Eqn: (heat transfer rate*Mean Depth of Adjacent Layers[Layer1]) *(heat diffusion covar*(eddy diffusion coef/eddy diffusion mean)+(1-heat diffusion covar))
    Units: W/m2/(DegreesC/meter)
    Limits: (0.0, 1.0)
    Type: component
    Subs: None

    The ratio of the actual to the mean of the heat transfer coefficient,
        which controls the movement of heat through the climate sector, is a
        function of the ratio of the actual to the mean of the eddy diffusion
        coefficient, which controls the movement of carbon through the deep ocean.
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
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'heat_transfer_rate')
    Units: W/m2/DegreesC
    Limits: (0.0, 2.0)
    Type: constant
    Subs: None


    """
    return _ext_constant_heat_transfer_rate()


def init_atm_uppocean_temperature_ano():
    """
    Real Name: init atm uppocean temperature ano
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_atm_uppocean_temperature_ano')
    Units: DegreesC
    Limits: (None, None)
    Type: constant
    Subs: None

    Global Annual Temperature Anomaly (Land + Ocean) in 1990 from NASA GISS Surface
        Temperature (GISTEMP): +0.43 ºC.        5-year average: +0.36 ºC. Average 1880-1889 = -0,225. Preindustrial reference: 0,36
        + 0,225 = 0,585        http://cdiac.ornl.gov/ftp/trends/temp/hansen/gl_land_ocean.txt
    """
    return _ext_constant_init_atm_uppocean_temperature_ano()


@subs(["Layers"], _subscript_dict)
def init_deep_ocean_temperature():
    """
    Real Name: init deep ocean temperature
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_deep_ocean_temperature*')
    Units: ºC
    Limits: (None, None)
    Type: constant
    Subs: ['Layers']

    C-ROADS simulation
    """
    return _ext_constant_init_deep_ocean_temperature()


def land_area_fraction():
    """
    Real Name: land area fraction
    Original Eqn: 0.292
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Fraction of global surface area that is land.
    """
    return 0.292


def land_thickness():
    """
    Real Name: land thickness
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'land_thickness')
    Units: m
    Limits: (None, None)
    Type: constant
    Subs: None

    Effective land area heat capacity, expressed as equivalent water layer
        thickness.
    """
    return _ext_constant_land_thickness()


@subs(["Layers"], _subscript_dict)
def lower_layer_volume_vu():
    """
    Real Name: lower layer volume Vu
    Original Eqn: earth surface area*(1-land area fraction)*layer depth[Layers]
    Units: m3
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Water equivalent volume of the deep ocean by layer.
    """
    return earth_surface_area() * (1 - land_area_fraction()) * layer_depth()


def reference_co2_radiative_forcing():
    """
    Real Name: reference CO2 radiative forcing
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'reference_CO2_radiative_forcing')
    Units: W/m2
    Limits: (None, None)
    Type: constant
    Subs: None

    Coefficient of radiative forcing from CO2        From IPCC
    """
    return _ext_constant_reference_co2_radiative_forcing()


@subs(["Layers"], _subscript_dict)
def relative_deep_ocean_temp():
    """
    Real Name: Relative Deep Ocean Temp
    Original Eqn: Heat in Deep Ocean[Layers]/Deep Ocean Heat Cap[Layers]
    Units: DegreesC
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Temperature of each layer of the deep ocean.
    """
    return heat_in_deep_ocean() / deep_ocean_heat_cap()


def temperature_change():
    """
    Real Name: Temperature change
    Original Eqn: Heat in Atmosphere and Upper Ocean/Atm and Upper Ocean Heat Cap
    Units: DegreesC
    Limits: (None, None)
    Type: component
    Subs: None

    Temperature of the Atmosphere and Upper Ocean, relative to preindustrial
        reference period
    """
    return heat_in_atmosphere_and_upper_ocean() / atm_and_upper_ocean_heat_cap()


def upper_layer_volume_vu():
    """
    Real Name: upper layer volume Vu
    Original Eqn: earth surface area*(land area fraction*land thickness+(1-land area fraction)*mixed layer depth)
    Units: m3
    Limits: (None, None)
    Type: component
    Subs: None

    Water equivalent volume of the upper box, which is a weighted combination
        of land, atmosphere,and upper ocean volumes.
    """
    return earth_surface_area() * (
        land_area_fraction() * land_thickness()
        + (1 - land_area_fraction()) * mixed_layer_depth()
    )


def volumetric_heat_capacity():
    """
    Real Name: volumetric heat capacity
    Original Eqn: 0.132737
    Units: W*year/m3/ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    Volumetric heat capacity of water, i.e., amount of heat in watt*year
        required to raise 1 cubic meter of water by one degree C. Computed from
        4.186e6/365/3600/24.
    """
    return 0.132737


_ext_constant_climate_sensitivity_to_2x_co2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "climate_sensitivity_to_2x_CO2",
    {},
    _root,
    "_ext_constant_climate_sensitivity_to_2x_co2",
)


_ext_constant_eddy_diffusion_coef_index = ExtConstant(
    "../climate.xlsx",
    "World",
    "eddy_diffusion_coef_index",
    {},
    _root,
    "_ext_constant_eddy_diffusion_coef_index",
)


_ext_constant_eddy_diffusion_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "eddy_diffusion_mean",
    {},
    _root,
    "_ext_constant_eddy_diffusion_mean",
)


_ext_constant_heat_diffusion_covar = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_diffusion_covar",
    {},
    _root,
    "_ext_constant_heat_diffusion_covar",
)


_integ_heat_in_atmosphere_and_upper_ocean = Integ(
    lambda: effective_radiative_forcing()
    - feedback_cooling()
    - float(heat_transfer().loc["Layer1"]),
    lambda: init_atm_uppocean_temperature_ano() * atm_and_upper_ocean_heat_cap(),
    "_integ_heat_in_atmosphere_and_upper_ocean",
)


@subs(["Layers"], _subscript_dict)
def _integ_init_heat_in_deep_ocean():
    """
    Real Name: Implicit
    Original Eqn:
      None
      None
    Units: See docs for heat_in_deep_ocean
    Limits: None
    Type: setup
    Subs: ['Layers']

    Provides initial conditions for heat_in_deep_ocean function
    """
    return xrmerge(
        rearrange(
            rearrange(init_deep_ocean_temperature(), ["upper"], _subscript_dict)
            * rearrange(deep_ocean_heat_cap(), ["upper"], _subscript_dict),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(
            float(init_deep_ocean_temperature().loc["Layer4"])
            * float(deep_ocean_heat_cap().loc["Layer4"]),
            ["Layers"],
            {"Layers": ["Layer4"]},
        ),
    )


@subs(["Layers"], _subscript_dict)
def _integ_input_heat_in_deep_ocean():
    """
    Real Name: Implicit
    Original Eqn:
      None
      None
    Units: See docs for heat_in_deep_ocean
    Limits: None
    Type: component
    Subs: ['Layers']

    Provides derivative for heat_in_deep_ocean function
    """
    return xrmerge(
        rearrange(
            rearrange(heat_transfer(), ["upper"], _subscript_dict)
            - rearrange(
                rearrange(heat_transfer(), ["lower"], _subscript_dict),
                ["upper"],
                _subscript_dict,
            ),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(
            float(heat_transfer().loc["Layer4"]), ["Layers"], {"Layers": ["Layer4"]}
        ),
    )


_integ_heat_in_deep_ocean = Integ(
    _integ_input_heat_in_deep_ocean,
    _integ_init_heat_in_deep_ocean,
    "_integ_heat_in_deep_ocean",
)


_ext_constant_heat_transfer_rate = ExtConstant(
    "../climate.xlsx",
    "World",
    "heat_transfer_rate",
    {},
    _root,
    "_ext_constant_heat_transfer_rate",
)


_ext_constant_init_atm_uppocean_temperature_ano = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_atm_uppocean_temperature_ano",
    {},
    _root,
    "_ext_constant_init_atm_uppocean_temperature_ano",
)


_ext_constant_init_deep_ocean_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_deep_ocean_temperature*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    "_ext_constant_init_deep_ocean_temperature",
)


_ext_constant_land_thickness = ExtConstant(
    "../climate.xlsx",
    "World",
    "land_thickness",
    {},
    _root,
    "_ext_constant_land_thickness",
)


_ext_constant_reference_co2_radiative_forcing = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_CO2_radiative_forcing",
    {},
    _root,
    "_ext_constant_reference_co2_radiative_forcing",
)
