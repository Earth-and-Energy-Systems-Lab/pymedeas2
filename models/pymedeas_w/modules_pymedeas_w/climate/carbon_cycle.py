"""
Module carbon_cycle
Translated using PySD version 2.1.0
"""


def atm_ocean_mixing_time():
    """
    Real Name: atm ocean mixing time
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'atm_ocean_mixing_time')
    Units: year
    Limits: (0.25, 10.0, 0.25)
    Type: constant
    Subs: None

    Atmosphere - mixed ocean layer mixing time.
    """
    return _ext_constant_atm_ocean_mixing_time()


def biomass_residence_time():
    """
    Real Name: biomass residence time
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'biomass_residence_time')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Average residence time of carbon in biomass.
    """
    return _ext_constant_biomass_residence_time()


def biostim_coeff():
    """
    Real Name: biostim coeff
    Original Eqn: biostim coeff index*biostim coeff mean
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Coefficient for response of primary production to carbon concentration.
    """
    return biostim_coeff_index() * biostim_coeff_mean()


def biostim_coeff_index():
    """
    Real Name: biostim coeff index
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'biostim_coeff_index')
    Units: Dmnl
    Limits: (0.6, 1.7, 0.05)
    Type: constant
    Subs: None

    Index of coefficient for response of primary production to carbon
        concentration, as multiplying factor of the mean value.
    """
    return _ext_constant_biostim_coeff_index()


def biostim_coeff_mean():
    """
    Real Name: biostim coeff mean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'biostim_coeff_mean')
    Units: Dmnl
    Limits: (0.3, 0.7)
    Type: constant
    Subs: None

    Mean coefficient for response of primary production to CO2 concentration. Reflects
        the increase in NPP with doubling the CO2 level.        Goudriaan and Ketner, 1984; Rotmans, 1990
    """
    return _ext_constant_biostim_coeff_mean()


def buffer_c_coeff():
    """
    Real Name: buffer C coeff
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'buffer_C_coeff')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Coefficient of CO2 concentration influence on buffer factor.
    """
    return _ext_constant_buffer_c_coeff()


def buffer_factor():
    """
    Real Name: Buffer Factor
    Original Eqn: ACTIVE INITIAL ( Ref Buffer Factor*(C in Mixed Layer/preindustrial C in mixed layer)^buffer C coeff, Ref Buffer Factor)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Buffer factor for atmosphere/mixed ocean carbon equilibration.
    """
    return active_initial(
        __data["time"],
        lambda: ref_buffer_factor()
        * (c_in_mixed_layer() / preindustrial_c_in_mixed_layer()) ** buffer_c_coeff(),
        ref_buffer_factor(),
    )


def c_from_ch4_oxidation():
    """
    Real Name: C from CH4 oxidation
    Original Eqn: CH4 Uptake/CH4 per C/Mt per Gt
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Flux of C into the atmosphere from the oxidation of CH4, the mode of
        removal of CH4 from atmosphere.
    """
    return ch4_uptake() / ch4_per_c() / mt_per_gt()


def c_humification_fraction():
    """
    Real Name: C humification fraction
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'C_humification_fraction')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Fraction of carbon outflow from biomass that enters humus stock.
    """
    return _ext_constant_c_humification_fraction()


def c_humus_residence_time():
    """
    Real Name: C humus residence time
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'C_humus_residence_time')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Average carbon residence time in humus.
    """
    return _ext_constant_c_humus_residence_time()


def c_in_atmosphere():
    """
    Real Name: C in Atmosphere
    Original Eqn: INTEG ( C from CH4 oxidation+Flux Biomass to Atmosphere+Flux Humus to Atmosphere+Total C anthro emissions-Flux Atm to Biomass-Flux Atm to Ocean+Flux C from permafrost release, init C in atm)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon  in atmosphere.
    """
    return _integ_c_in_atmosphere()


def c_in_biomass():
    """
    Real Name: C in Biomass
    Original Eqn: INTEG ( Flux Atm to Biomass-Flux Biomass to Atmosphere-Flux Biomass to CH4-Flux Biomass to Humus, init C in biomass)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon in biomass.
    """
    return _integ_c_in_biomass()


@subs(["Layers"], _subscript_dict)
def c_in_deep_ocean():
    """
    Real Name: C in Deep Ocean
    Original Eqn:
      INTEG ( Diffusion Flux[upper]-Diffusion Flux[lower], init C in deep ocean[upper]*layer depth[upper])
      INTEG ( Diffusion Flux[Layer4], init C in deep ocean[Layer4]*layer depth[Layer4])
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Carbon in deep ocean.
    """
    return xrmerge(
        rearrange(
            _integ_c_in_deep_ocean(),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(_integ_c_in_deep_ocean(), ["Layers"], {"Layers": ["Layer4"]}),
    )


@subs(["Layers"], _subscript_dict)
def c_in_deep_ocean_per_meter():
    """
    Real Name: C in deep ocean per meter
    Original Eqn: C in Deep Ocean[Layers]/layer depth[Layers]
    Units: GtC/meter
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Concentration of carbon in ocean layers.
    """
    return c_in_deep_ocean() / layer_depth()


def c_in_humus():
    """
    Real Name: C in Humus
    Original Eqn: INTEG (Flux Biomass to Humus-Flux Humus to Atmosphere-Flux Humus to CH4, init C in humus)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon in humus.
    """
    return _integ_c_in_humus()


def c_in_mixed_layer():
    """
    Real Name: C in Mixed Layer
    Original Eqn: INTEG ( Flux Atm to Ocean-Diffusion Flux[Layer1], init C in mixed ocean*mixed layer depth)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon in mixed layer.
    """
    return _integ_c_in_mixed_layer()


def c_in_mixed_layer_per_meter():
    """
    Real Name: C in mixed layer per meter
    Original Eqn: C in Mixed Layer/mixed layer depth
    Units: GtC/meter
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return c_in_mixed_layer() / mixed_layer_depth()


def ch4_generation_rate_from_biomass():
    """
    Real Name: CH4 generation rate from biomass
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_generation_rate_from_biomass')
    Units: 1/year
    Limits: (0.0, 0.00014)
    Type: constant
    Subs: None

    The rate of the natural flux of methane from C in biomass. The sum of the
        flux of methane from C in humus and the flux of methane from C in biomass
        yields the natural emissions of methane.
    """
    return _ext_constant_ch4_generation_rate_from_biomass()


def ch4_generation_rate_from_humus():
    """
    Real Name: CH4 generation rate from humus
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_generation_rate_from_humus')
    Units: 1/year
    Limits: (0.0, 0.00016)
    Type: constant
    Subs: None

    The rate of the natural flux of methane from C in humus. The sum of the
        flux of methane from C in humus and the flux of methane from C in biomass
        yields the natural emissions of methane.
    """
    return _ext_constant_ch4_generation_rate_from_humus()


def ch4_per_c():
    """
    Real Name: CH4 per C
    Original Eqn: 16/12
    Units: Mt/MtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Molar mass ratio of CH4 to C, 16/12
    """
    return 16 / 12


def co2_ppm_concentrations():
    """
    Real Name: CO2 ppm concentrations
    Original Eqn: C in Atmosphere / 2.13
    Units: ppm
    Limits: (None, None)
    Type: component
    Subs: None

    1 part per million of atmospheric CO2 is equivalent to 2.13 gigatonnes Carbon.                Historical Mauna Loa CO2 Record:
        ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt
    """
    return c_in_atmosphere() / 2.13


@subs(["Layers"], _subscript_dict)
def diffusion_flux():
    """
    Real Name: Diffusion Flux
    Original Eqn:
      (C in mixed layer per meter-C in deep ocean per meter[Layer1])*eddy diffusion coef/Mean Depth of Adjacent Layers[Layer1]
      (C in deep ocean per meter[upper] -C in deep ocean per meter[lower]) *eddy diffusion coef/Mean Depth of Adjacent Layers[lower]
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Diffusion flux between ocean layers.
    """
    return xrmerge(
        rearrange(
            (
                c_in_mixed_layer_per_meter()
                - float(c_in_deep_ocean_per_meter().loc["Layer1"])
            )
            * eddy_diffusion_coef()
            / float(mean_depth_of_adjacent_layers().loc["Layer1"]),
            ["Layers"],
            {"Layers": ["Layer1"]},
        ),
        rearrange(
            (
                rearrange(
                    rearrange(c_in_deep_ocean_per_meter(), ["upper"], _subscript_dict),
                    ["lower"],
                    _subscript_dict,
                )
                - rearrange(c_in_deep_ocean_per_meter(), ["lower"], _subscript_dict)
            )
            * eddy_diffusion_coef()
            / rearrange(mean_depth_of_adjacent_layers(), ["lower"], _subscript_dict),
            ["Layers"],
            {"Layers": ["Layer2", "Layer3", "Layer4"]},
        ),
    )


def eddy_diffusion_coef():
    """
    Real Name: eddy diffusion coef
    Original Eqn: eddy diffusion coef index*eddy diffusion mean
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
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'eddy_diffusion_coef_index')
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
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'eddy_diffusion_mean')
    Units: m2/year
    Limits: (2000.0, 8000.0)
    Type: constant
    Subs: None

    Rate of vertical transport and mixing in the ocean due to eddy diffusion
        motion.
    """
    return _ext_constant_eddy_diffusion_mean()


def effect_of_temp_on_dic_pco2():
    """
    Real Name: Effect of Temp on DIC pCO2
    Original Eqn: 1-sensitivity of pCO2 DIC to temperature*Temperature change
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The fractional reduction in the solubility of CO2 in ocean falls with
        rising temperatures.  We assume a linear relationship, likely a good
        approximation over the typical range for warming by 2100.
    """
    return 1 - sensitivity_of_pco2_dic_to_temperature() * temperature_change()


def effect_of_warming_on_c_flux_to_biomass():
    """
    Real Name: Effect of Warming on C flux to biomass
    Original Eqn: 1+Strength of Temp Effect on C Flux to Land*Temperature change
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The fractional reduction in the flux of C from the atmosphere to biomass
        with rising temperatures.  We assume a linear relationship, likely a good
        approxim
    """
    return 1 + strength_of_temp_effect_on_c_flux_to_land() * temperature_change()


def effect_of_warming_on_ch4_release_from_biological_activity():
    """
    Real Name: Effect of Warming on CH4 Release from Biological Activity
    Original Eqn: 1+sensitivity of methane emissions to temperature*(Temperature change)/(reference temperature change for effect of warming on CH4 from respiration )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The fractional increase in the flux of C as CH4 from humus with rising
        temperatures. We assume a linear relationship, likely a good approximation
        over the typical range for warming by 2100.
    """
    return 1 + sensitivity_of_methane_emissions_to_temperature() * (
        temperature_change()
    ) / (reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration())


def equil_c_in_mixed_layer():
    """
    Real Name: Equil C in Mixed Layer
    Original Eqn: preindustrial C in mixed layer*Effect of Temp on DIC pCO2*(C in Atmosphere /preindustrial C)^(1/Buffer Factor)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Equilibrium carbon content of mixed layer.  Determined by the Revelle
        buffering factor, and by temperature.  For simplicity, we assume a linear
        impact of warming on the equilibrium solubility of CO2 in the ocean.
    """
    return (
        preindustrial_c_in_mixed_layer()
        * effect_of_temp_on_dic_pco2()
        * (c_in_atmosphere() / preindustrial_c()) ** (1 / buffer_factor())
    )


def equilibrium_c_per_meter_in_mixed_layer():
    """
    Real Name: Equilibrium C per meter in Mixed Layer
    Original Eqn: Equil C in Mixed Layer/mixed layer depth
    Units: GtC/meter
    Limits: (None, None)
    Type: component
    Subs: None

    The equilibrium concentration of C in the mixed layer, in GtC/meter, based
        on the total quantity of C in that layer and the average layer depth.
    """
    return equil_c_in_mixed_layer() / mixed_layer_depth()


def flux_atm_to_biomass():
    """
    Real Name: Flux Atm to Biomass
    Original Eqn: init NPP* (1+ biostim coeff* LN(C in Atmosphere/preindustrial C))*Effect of Warming on C flux to biomass
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from atmosphere to biosphere (from primary production)
    """
    return (
        init_npp()
        * (1 + biostim_coeff() * np.log(c_in_atmosphere() / preindustrial_c()))
        * effect_of_warming_on_c_flux_to_biomass()
    )


def flux_atm_to_ocean():
    """
    Real Name: Flux Atm to Ocean
    Original Eqn: ((Equil C in Mixed Layer-C in Mixed Layer)/atm ocean mixing time)
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from atmosphere to mixed ocean layer.
    """
    return (equil_c_in_mixed_layer() - c_in_mixed_layer()) / atm_ocean_mixing_time()


def flux_biomass_to_atmosphere():
    """
    Real Name: Flux Biomass to Atmosphere
    Original Eqn: C in Biomass/biomass residence time*(1-C humification fraction)
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from biomass to atmosphere.
    """
    return c_in_biomass() / biomass_residence_time() * (1 - c_humification_fraction())


def flux_biomass_to_ch4():
    """
    Real Name: Flux Biomass to CH4
    Original Eqn: C in Biomass*CH4 generation rate from biomass*Effect of Warming on CH4 Release from Biological Activity
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    The natural flux of methane from C in biomass. The sum of the flux of
        methane from C in humus and the flux of methane from C in biomass yields
        the natural emissions of methane.  Adjusted to account for temperature
        feedback.
    """
    return (
        c_in_biomass()
        * ch4_generation_rate_from_biomass()
        * effect_of_warming_on_ch4_release_from_biological_activity()
    )


def flux_biomass_to_humus():
    """
    Real Name: Flux Biomass to Humus
    Original Eqn: C in Biomass/biomass residence time*C humification fraction
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from biomass to humus.
    """
    return c_in_biomass() / biomass_residence_time() * c_humification_fraction()


def flux_biosphere_to_ch4():
    """
    Real Name: Flux Biosphere to CH4
    Original Eqn: Flux Biomass to CH4+Flux Humus to CH4
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from biosphere as methane, in GtC/year, arising from anaerobic
        respiration.
    """
    return flux_biomass_to_ch4() + flux_humus_to_ch4()


def flux_humus_to_atmosphere():
    """
    Real Name: Flux Humus to Atmosphere
    Original Eqn: C in Humus/C humus residence time
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon flux from humus to atmosphere.
    """
    return c_in_humus() / c_humus_residence_time()


def flux_humus_to_ch4():
    """
    Real Name: Flux Humus to CH4
    Original Eqn: C in Humus*CH4 generation rate from humus*Effect of Warming on CH4 Release from Biological Activity
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    The natural flux of methane from C in humus. The sum of the flux of
        methane from C in humus and the flux of methane from C in biomass yields
        the natural emissions of methane. Adjusted to account for temperature
        feedback.
    """
    return (
        c_in_humus()
        * ch4_generation_rate_from_humus()
        * effect_of_warming_on_ch4_release_from_biological_activity()
    )


def gtc_per_ppm():
    """
    Real Name: GtC per ppm
    Original Eqn: 2.13
    Units: GtC/ppm
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion from ppm to GtC (1 ppm by volume of atmosphere CO2 = 2.13 Gt C        (Uses atmospheric mass (Ma) = 5.137 × 10^18 kg)) CDIAC:
        http://cdiac.ornl.gov/pns/convert.html
    """
    return 2.13


def init_c_in_atm():
    """
    Real Name: init C in atm
    Original Eqn: init CO2 in atm ppm*GtC per ppm
    Units: GtC
    Limits: (500.0, 1000.0)
    Type: component
    Subs: None

    Initial C in atmosphere.                [DICE-1994] Initial Greenhouse Gases in Atmosphere 1965 [M(t)] (tC equivalent).
        [Cowles, pg. 21] /6.77e+011 /        [DICE-2013R] mat0: Initial concentration in atmosphere 2010 (GtC) /830.4 /
    """
    return init_co2_in_atm_ppm() * gtc_per_ppm()


def init_c_in_biomass():
    """
    Real Name: init C in biomass
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_C_in_biomass')
    Units: GtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial carbon in biomass.
    """
    return _ext_constant_init_c_in_biomass()


@subs(["Layers"], _subscript_dict)
def init_c_in_deep_ocean():
    """
    Real Name: init C in deep ocean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_C_in_deep_ocean*')
    Units: GtC/meter
    Limits: (None, None)
    Type: constant
    Subs: ['Layers']

    Initial carbon concentration in deep ocean layers per meter.
    """
    return _ext_constant_init_c_in_deep_ocean()


def init_c_in_humus():
    """
    Real Name: init C in humus
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_C_in_humus')
    Units: GtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Inital carbon in humus.
    """
    return _ext_constant_init_c_in_humus()


def init_c_in_mixed_ocean():
    """
    Real Name: init C in mixed ocean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_C_in_mixed_ocean')
    Units: GtC/meter
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial carbon in mixed ocean layer per meter.
    """
    return _ext_constant_init_c_in_mixed_ocean()


def init_co2_in_atm_ppm():
    """
    Real Name: init CO2 in atm ppm
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_CO2_in_atm_ppm')
    Units: ppm
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial CO2 in atmosphere.        Historical Mauna Loa CO2 Record: Average between 1st and last month of 1990 was:
        (353.74+355.12)/2=354.43 ppm        Historical Mauna Loa CO2 Record: Average between 1st and last month of 1995 was:
        (359.92+360.68)/2= 360.3 ppm        ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt                [DICE-1994] Initial Greenhouse Gases in Atmosphere 1965 [M(t)] (tC equivalent).
        [Cowles, pg. 21] /6.77e+011 /        [DICE-2013R] mat0: Initial concentration in atmosphere 2010 (GtC) /830.4 /
    """
    return _ext_constant_init_co2_in_atm_ppm()


def init_npp():
    """
    Real Name: init NPP
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_NPP')
    Units: GtC/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial net primary production. Adapted from Goudriaan, 1984.
    """
    return _ext_constant_init_npp()


@subs(["Layers"], _subscript_dict)
def layer_depth():
    """
    Real Name: layer depth
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'layer_depth*')
    Units: m
    Limits: (None, None)
    Type: constant
    Subs: ['Layers']

    Deep ocean layer thicknesses.
    """
    return _ext_constant_layer_depth()


@subs(["Layers"], _subscript_dict)
def layer_time_constant():
    """
    Real Name: Layer Time Constant
    Original Eqn:
      layer depth[Layer1]/(eddy diffusion coef/Mean Depth of Adjacent Layers[Layer1])
      layer depth[lower]/(eddy diffusion coef/Mean Depth of Adjacent Layers[lower])
    Units: year
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    Time constant of exchange between layers.
    """
    return xrmerge(
        rearrange(
            float(layer_depth().loc["Layer1"])
            / (
                eddy_diffusion_coef()
                / float(mean_depth_of_adjacent_layers().loc["Layer1"])
            ),
            ["Layers"],
            {"Layers": ["Layer1"]},
        ),
        rearrange(
            rearrange(layer_depth(), ["lower"], _subscript_dict)
            / (
                eddy_diffusion_coef()
                / rearrange(mean_depth_of_adjacent_layers(), ["lower"], _subscript_dict)
            ),
            ["Layers"],
            {"Layers": ["Layer2", "Layer3", "Layer4"]},
        ),
    )


@subs(["Layers"], _subscript_dict)
def mean_depth_of_adjacent_layers():
    """
    Real Name: Mean Depth of Adjacent Layers
    Original Eqn:
      (mixed layer depth+layer depth[Layer1])/2
      (layer depth[upper]+layer depth[lower])/2
    Units: meter
    Limits: (None, None)
    Type: component
    Subs: ['Layers']

    The mean depth of adjacent ocean layers.
    """
    return xrmerge(
        rearrange(
            (mixed_layer_depth() + float(layer_depth().loc["Layer1"])) / 2,
            ["Layers"],
            {"Layers": ["Layer1"]},
        ),
        rearrange(
            (
                rearrange(
                    rearrange(layer_depth(), ["upper"], _subscript_dict),
                    ["lower"],
                    _subscript_dict,
                )
                + rearrange(layer_depth(), ["lower"], _subscript_dict)
            )
            / 2,
            ["Layers"],
            {"Layers": ["Layer2", "Layer3", "Layer4"]},
        ),
    )


def mixed_layer_depth():
    """
    Real Name: mixed layer depth
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'mixed_layer_depth')
    Units: meter
    Limits: (None, None)
    Type: constant
    Subs: None

    Mixed ocean layer depth.
    """
    return _ext_constant_mixed_layer_depth()


def mt_per_gt():
    """
    Real Name: Mt per Gt
    Original Eqn:
      1
      0
      0
      0
    Units: Mt/Gt
    Limits: (None, None)
    Type: constant
    Subs: None

    Converts megatonnes to gigatonnes.
    """
    return 1000


def natural_ch4_emissions():
    """
    Real Name: natural CH4 emissions
    Original Eqn: Flux Biosphere to CH4*CH4 per C*Mt per Gt
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None

    Flux of methane from anaerobic respiration in the biosphere, in megatonnes
        CH4/year.
    """
    return flux_biosphere_to_ch4() * ch4_per_c() * mt_per_gt()


def preindustrial_c():
    """
    Real Name: preindustrial C
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preindustrial_C')
    Units: GtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Preindustrial C content of atmosphere.
    """
    return _ext_constant_preindustrial_c()


def preindustrial_c_in_mixed_layer():
    """
    Real Name: preindustrial C in mixed layer
    Original Eqn: preindustrial C in ocean*mixed layer depth
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Initial carbon concentration of mixed ocean layer.
    """
    return preindustrial_c_in_ocean() * mixed_layer_depth()


def preindustrial_c_in_ocean():
    """
    Real Name: preindustrial C in ocean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preind_C_in_ocean')
    Units: GtC/m
    Limits: (None, None)
    Type: constant
    Subs: None

    Preindustrial ocean carbon content per meter. Corresponds with 767.8 GtC
        in a 75m layer.
    """
    return _ext_constant_preindustrial_c_in_ocean()


def ref_buffer_factor():
    """
    Real Name: Ref Buffer Factor
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'ref_buffer_factor')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Normal buffer factor.
    """
    return _ext_constant_ref_buffer_factor()


def reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration():
    """
    Real Name: reference temperature change for effect of warming on CH4 from respiration
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'reference_temperature_change_for_effect_of_warming_on_CH4_from_respiration')
    Units: ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    Temperature change at which the C as CH4 release from humus doubles for
        the sensitivity of methane emissions to temperature=1.
    """
    return (
        _ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration()
    )


def sensitivity_of_c_uptake_to_temperature():
    """
    Real Name: sensitivity of C uptake to temperature
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'sensitivity_of_C_uptake_to_temperature')
    Units: Dmnl
    Limits: (0.0, 2.5, 0.1)
    Type: constant
    Subs: None

    Strength of the feedback effect of temperature on uptake of C by land and
        oceans. 0 means no temperature-carbon uptake feedback and default of 1
        yields the average value found in Friedlingstein et al., 2006.
        Climate-Carbon Cycle Feedback Analysis: ResuMCS from the C4MIP Model
        Intercomparison.  Journal of Climate. p3337-3353.
    """
    return _ext_constant_sensitivity_of_c_uptake_to_temperature()


def sensitivity_of_methane_emissions_to_temperature():
    """
    Real Name: sensitivity of methane emissions to temperature
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'sensitivity_of_methane_emissions_to_temperature')
    Units: Dmnl
    Limits: (0.0, 2.5, 0.1)
    Type: constant
    Subs: None

    Allows users to control the strength of the feedback effect of temperature
        on release of C as CH4 from humus. Default of 0 means no temperature
        feedback and 1 is mean feedback.
    """
    return _ext_constant_sensitivity_of_methane_emissions_to_temperature()


def sensitivity_of_pco2_dic_to_temperature():
    """
    Real Name: sensitivity of pCO2 DIC to temperature
    Original Eqn: sensitivity of C uptake to temperature*sensitivity of pCO2 DIC to temperature mean
    Units: 1/ºC
    Limits: (None, None)
    Type: component
    Subs: None

    Sensitivity of pCO2 of dissolved inorganic carbon in ocean to temperature.
    """
    return (
        sensitivity_of_c_uptake_to_temperature()
        * sensitivity_of_pco2_dic_to_temperature_mean()
    )


def sensitivity_of_pco2_dic_to_temperature_mean():
    """
    Real Name: sensitivity of pCO2 DIC to temperature mean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'sensitivity_of_pCO2_DIC_to_temperature_mean')
    Units: 1/ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    Sensitivity of equilibrium concentration of dissolved inorganic carbon to
        temperature.  Calibrated to be consistent with Friedlingstein et al.,
        2006.  Climate-Carbon Cycle Feedback Analysis: ResuMCS from the C4MIP
        Model Intercomparison.  Journal of Climate. p3337-3353.  Default
        sensitivity of C uptake to temperature of 1 corresponds to mean value from
        the 11 models tested.
    """
    return _ext_constant_sensitivity_of_pco2_dic_to_temperature_mean()


def strength_of_temp_effect_on_c_flux_to_land():
    """
    Real Name: Strength of Temp Effect on C Flux to Land
    Original Eqn: sensitivity of C uptake to temperature*Strength of temp effect on land C flux mean
    Units: 1/ºC
    Limits: (None, None)
    Type: component
    Subs: None

    Strength of temperature effect on C flux to the land.
    """
    return (
        sensitivity_of_c_uptake_to_temperature()
        * strength_of_temp_effect_on_land_c_flux_mean()
    )


def strength_of_temp_effect_on_land_c_flux_mean():
    """
    Real Name: Strength of temp effect on land C flux mean
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'strength_of_temp_effect_on_land_C_flux_mean')
    Units: 1/ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    Average effect of temperature on flux of carbon to land. Calibrated to be
        consistent with Friedlingstein et al., 2006.  Climate-Carbon Cycle
        Feedback Analysis: ResuMCS from the C4MIP Model Intercomparison.  Journal
        of Climate. p3337-3353.  Default sensitivity of C uptake to temperature of
        1 corresponds to mean value from the 11 models tested.
    """
    return _ext_constant_strength_of_temp_effect_on_land_c_flux_mean()


def total_c_anthro_emissions():
    """
    Real Name: Total C anthro emissions
    Original Eqn: Total CO2 emissions GTCO2*C per CO2
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual CO2 emissions converted to  GtC/year.
    """
    return total_co2_emissions_gtco2() * c_per_co2()


_ext_constant_atm_ocean_mixing_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "atm_ocean_mixing_time",
    {},
    _root,
    "_ext_constant_atm_ocean_mixing_time",
)


_ext_constant_biomass_residence_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "biomass_residence_time",
    {},
    _root,
    "_ext_constant_biomass_residence_time",
)


_ext_constant_biostim_coeff_index = ExtConstant(
    "../climate.xlsx",
    "World",
    "biostim_coeff_index",
    {},
    _root,
    "_ext_constant_biostim_coeff_index",
)


_ext_constant_biostim_coeff_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "biostim_coeff_mean",
    {},
    _root,
    "_ext_constant_biostim_coeff_mean",
)


_ext_constant_buffer_c_coeff = ExtConstant(
    "../climate.xlsx",
    "World",
    "buffer_C_coeff",
    {},
    _root,
    "_ext_constant_buffer_c_coeff",
)


_ext_constant_c_humification_fraction = ExtConstant(
    "../climate.xlsx",
    "World",
    "C_humification_fraction",
    {},
    _root,
    "_ext_constant_c_humification_fraction",
)


_ext_constant_c_humus_residence_time = ExtConstant(
    "../climate.xlsx",
    "World",
    "C_humus_residence_time",
    {},
    _root,
    "_ext_constant_c_humus_residence_time",
)


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


_integ_c_in_biomass = Integ(
    lambda: flux_atm_to_biomass()
    - flux_biomass_to_atmosphere()
    - flux_biomass_to_ch4()
    - flux_biomass_to_humus(),
    lambda: init_c_in_biomass(),
    "_integ_c_in_biomass",
)


@subs(["Layers"], _subscript_dict)
def _integ_init_c_in_deep_ocean():
    """
    Real Name: Implicit
    Original Eqn:
      None
      None
    Units: See docs for c_in_deep_ocean
    Limits: None
    Type: setup
    Subs: ['Layers']

    Provides initial conditions for c_in_deep_ocean function
    """
    return xrmerge(
        rearrange(
            rearrange(init_c_in_deep_ocean(), ["upper"], _subscript_dict)
            * rearrange(layer_depth(), ["upper"], _subscript_dict),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(
            float(init_c_in_deep_ocean().loc["Layer4"])
            * float(layer_depth().loc["Layer4"]),
            ["Layers"],
            {"Layers": ["Layer4"]},
        ),
    )


@subs(["Layers"], _subscript_dict)
def _integ_input_c_in_deep_ocean():
    """
    Real Name: Implicit
    Original Eqn:
      None
      None
    Units: See docs for c_in_deep_ocean
    Limits: None
    Type: component
    Subs: ['Layers']

    Provides derivative for c_in_deep_ocean function
    """
    return xrmerge(
        rearrange(
            rearrange(diffusion_flux(), ["upper"], _subscript_dict)
            - rearrange(
                rearrange(diffusion_flux(), ["lower"], _subscript_dict),
                ["upper"],
                _subscript_dict,
            ),
            ["Layers"],
            {"Layers": ["Layer1", "Layer2", "Layer3"]},
        ),
        rearrange(
            float(diffusion_flux().loc["Layer4"]), ["Layers"], {"Layers": ["Layer4"]}
        ),
    )


_integ_c_in_deep_ocean = Integ(
    _integ_input_c_in_deep_ocean, _integ_init_c_in_deep_ocean, "_integ_c_in_deep_ocean"
)


_integ_c_in_humus = Integ(
    lambda: flux_biomass_to_humus() - flux_humus_to_atmosphere() - flux_humus_to_ch4(),
    lambda: init_c_in_humus(),
    "_integ_c_in_humus",
)


_integ_c_in_mixed_layer = Integ(
    lambda: flux_atm_to_ocean() - float(diffusion_flux().loc["Layer1"]),
    lambda: init_c_in_mixed_ocean() * mixed_layer_depth(),
    "_integ_c_in_mixed_layer",
)


_ext_constant_ch4_generation_rate_from_biomass = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_generation_rate_from_biomass",
    {},
    _root,
    "_ext_constant_ch4_generation_rate_from_biomass",
)


_ext_constant_ch4_generation_rate_from_humus = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_generation_rate_from_humus",
    {},
    _root,
    "_ext_constant_ch4_generation_rate_from_humus",
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


_ext_constant_init_c_in_biomass = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_biomass",
    {},
    _root,
    "_ext_constant_init_c_in_biomass",
)


_ext_constant_init_c_in_deep_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_deep_ocean*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    "_ext_constant_init_c_in_deep_ocean",
)


_ext_constant_init_c_in_humus = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_humus",
    {},
    _root,
    "_ext_constant_init_c_in_humus",
)


_ext_constant_init_c_in_mixed_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_C_in_mixed_ocean",
    {},
    _root,
    "_ext_constant_init_c_in_mixed_ocean",
)


_ext_constant_init_co2_in_atm_ppm = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_CO2_in_atm_ppm",
    {},
    _root,
    "_ext_constant_init_co2_in_atm_ppm",
)


_ext_constant_init_npp = ExtConstant(
    "../climate.xlsx", "World", "init_NPP", {}, _root, "_ext_constant_init_npp"
)


_ext_constant_layer_depth = ExtConstant(
    "../climate.xlsx",
    "World",
    "layer_depth*",
    {"Layers": _subscript_dict["Layers"]},
    _root,
    "_ext_constant_layer_depth",
)


_ext_constant_mixed_layer_depth = ExtConstant(
    "../climate.xlsx",
    "World",
    "mixed_layer_depth",
    {},
    _root,
    "_ext_constant_mixed_layer_depth",
)


_ext_constant_preindustrial_c = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_C",
    {},
    _root,
    "_ext_constant_preindustrial_c",
)


_ext_constant_preindustrial_c_in_ocean = ExtConstant(
    "../climate.xlsx",
    "World",
    "preind_C_in_ocean",
    {},
    _root,
    "_ext_constant_preindustrial_c_in_ocean",
)


_ext_constant_ref_buffer_factor = ExtConstant(
    "../climate.xlsx",
    "World",
    "ref_buffer_factor",
    {},
    _root,
    "_ext_constant_ref_buffer_factor",
)


_ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_temperature_change_for_effect_of_warming_on_CH4_from_respiration",
    {},
    _root,
    "_ext_constant_reference_temperature_change_for_effect_of_warming_on_ch4_from_respiration",
)


_ext_constant_sensitivity_of_c_uptake_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_C_uptake_to_temperature",
    {},
    _root,
    "_ext_constant_sensitivity_of_c_uptake_to_temperature",
)


_ext_constant_sensitivity_of_methane_emissions_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_methane_emissions_to_temperature",
    {},
    _root,
    "_ext_constant_sensitivity_of_methane_emissions_to_temperature",
)


_ext_constant_sensitivity_of_pco2_dic_to_temperature_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "sensitivity_of_pCO2_DIC_to_temperature_mean",
    {},
    _root,
    "_ext_constant_sensitivity_of_pco2_dic_to_temperature_mean",
)


_ext_constant_strength_of_temp_effect_on_land_c_flux_mean = ExtConstant(
    "../climate.xlsx",
    "World",
    "strength_of_temp_effect_on_land_C_flux_mean",
    {},
    _root,
    "_ext_constant_strength_of_temp_effect_on_land_c_flux_mean",
)
