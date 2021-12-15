"""
Module solar_potential_in_urban_areas_e
Translated using PySD version 2.2.0
"""


def av_solar_i():
    """
    Real Name: av solar I
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'K24')
    Units: We/m2
    Limits: (None, None)
    Type: constant
    Subs: None

    Average solar irradiance.
    """
    return _ext_constant_av_solar_i()


def f1_pv_solar_in_target_year():
    """
    Real Name: f1 PV solar in target year
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G24')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Cell efficiency solar PV in target year.
    """
    return _ext_constant_f1_pv_solar_in_target_year()


def f1_solar_pv():
    """
    Real Name: f1 solar PV
    Original Eqn: IF THEN ELSE(Time<2015, "f1-ini solar PV", IF THEN ELSE(Time<Start year P f1 solar PV, "f1-ini solar PV", IF THEN ELSE(Time<Target year f1 solar PV, "f1-ini solar PV"+(f1 PV solar in target year-"f1-ini solar PV")*(Time-Start year P f1 solar PV)/(Target year f1 solar PV-Start year P f1 solar PV ), f1 PV solar in target year)))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Cell efficiency conversion of solar PV.
    """
    return if_then_else(
        time() < 2015,
        lambda: f1ini_solar_pv(),
        lambda: if_then_else(
            time() < start_year_p_f1_solar_pv(),
            lambda: f1ini_solar_pv(),
            lambda: if_then_else(
                time() < target_year_f1_solar_pv(),
                lambda: f1ini_solar_pv()
                + (f1_pv_solar_in_target_year() - f1ini_solar_pv())
                * (time() - start_year_p_f1_solar_pv())
                / (target_year_f1_solar_pv() - start_year_p_f1_solar_pv()),
                lambda: f1_pv_solar_in_target_year(),
            ),
        ),
    )


def f1ini_solar_pv():
    """
    Real Name: "f1-ini solar PV"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'cell_efficiency_conversion_of_solar_pv')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Current cell efficiency conversion of solar PV.
    """
    return _ext_constant_f1ini_solar_pv()


def f2_pf_solar_pv():
    """
    Real Name: f2 PF solar PV
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'performance_ratio_over_the_plant_lifecycle_of_solar_pv')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Average performance ratio over the plant's life cycle (f2).
    """
    return _ext_constant_f2_pf_solar_pv()


def f3_solar_pv_on_land():
    """
    Real Name: f3 solar PV on land
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'land_occupation_ratio_of_solar_pv')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Land occupation ratio (f3).
    """
    return _ext_constant_f3_solar_pv_on_land()


def max_fe_solar_thermal_urban_twth():
    """
    Real Name: max FE solar thermal urban TWth
    Original Eqn: "power density solar thermal in urban TWe/Mha"*Urban land
    Units: TWth
    Limits: (None, None)
    Type: component
    Subs: None

    Potential of solar thermal in urban areas (final energy).
    """
    return power_density_solar_thermal_in_urban_twemha() * urban_land()


def max_solar_pv_urban():
    """
    Real Name: max solar PV urban
    Original Eqn: "power density solar PV in urban TWe/Mha"*Urban land
    Units: TWe
    Limits: (None, None)
    Type: component
    Subs: None

    Potential of solar PV in urban areas.
    """
    return power_density_solar_pv_in_urban_twemha() * urban_land()


@subs(["RES elec"], _subscript_dict)
def power_density_initial_res_elec_twemha():
    """
    Real Name: "power density initial RES elec TWe/Mha"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'power_density_res_elec*')
    Units: TWe/MHa
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Input parameter: power density per RES technology for delivering
        electricity.
    """
    return _ext_constant_power_density_initial_res_elec_twemha()


@subs(["RES elec"], _subscript_dict)
def power_density_res_elec_twemha():
    """
    Real Name: "power density RES elec TWe/Mha"
    Original Eqn:
      "power density initial RES elec TWe/Mha"[hydro]*(Cp RES elec[hydro]/"Cp-ini RES elec"[hydro])
        .
        .
        .
      "power density initial RES elec TWe/Mha"[CSP]*(Cp RES elec[CSP]/"Cp-ini RES elec"[CSP])
    Units: TWe/MHa
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Power density of renewable energy technologies for electricity generation.
        TODO
    """
    return xrmerge(
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["hydro"])
            * (
                float(cp_res_elec().loc["hydro"]) / float(cpini_res_elec().loc["hydro"])
            ),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["geot elec"])
            * (
                float(cp_res_elec().loc["geot elec"])
                / float(cpini_res_elec().loc["geot elec"])
            ),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["solid bioE elec"])
            * (
                float(cp_res_elec().loc["solid bioE elec"])
                / float(cpini_res_elec().loc["solid bioE elec"])
            ),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["oceanic"])
            * (
                float(cp_res_elec().loc["oceanic"])
                / float(cpini_res_elec().loc["oceanic"])
            ),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["wind onshore"])
            * (
                float(cp_res_elec().loc["wind onshore"])
                / float(cpini_res_elec().loc["wind onshore"])
            ),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["wind offshore"])
            * (
                float(cp_res_elec().loc["wind offshore"])
                / float(cpini_res_elec().loc["wind offshore"])
            ),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            power_density_solar_pv_on_land_twemha()
            * (
                float(cp_res_elec().loc["solar PV"])
                / float(cpini_res_elec().loc["solar PV"])
            ),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            float(power_density_initial_res_elec_twemha().loc["CSP"])
            * (float(cp_res_elec().loc["CSP"]) / float(cpini_res_elec().loc["CSP"])),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


def power_density_solar_pv_in_urban_twemha():
    """
    Real Name: "power density solar PV in urban TWe/Mha"
    Original Eqn: av solar I*f1 solar PV*f2 PF solar PV*share available roof *share available roof for rooftop PV*"TWh/Mha per We/m2"
    Units: TWe/MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Power density of solar PV in urban areas.
    """
    return (
        av_solar_i()
        * f1_solar_pv()
        * f2_pf_solar_pv()
        * share_available_roof()
        * share_available_roof_for_rooftop_pv()
        * twhmha_per_wem2()
    )


def power_density_solar_pv_on_land_twemha():
    """
    Real Name: "power density solar PV on land TWe/Mha"
    Original Eqn: av solar I*f1 solar PV*f2 PF solar PV*f3 solar PV on land*"TWh/Mha per We/m2"
    Units: TWe/MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Power density of solar PV power plants on land.
    """
    return (
        av_solar_i()
        * f1_solar_pv()
        * f2_pf_solar_pv()
        * f3_solar_pv_on_land()
        * twhmha_per_wem2()
    )


def power_density_solar_thermal_in_urban_twemha():
    """
    Real Name: "power density solar thermal in urban TWe/Mha"
    Original Eqn: av solar I*f1 solar panels for heat*Losses solar for heat*share available roof*share available roof for solar thermal*"TWh/Mha per We/m2"
    Units: TWe/MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Power density of solar thermal in urban areas.
    """
    return (
        av_solar_i()
        * f1_solar_panels_for_heat()
        * losses_solar_for_heat()
        * share_available_roof()
        * share_available_roof_for_solar_thermal()
        * twhmha_per_wem2()
    )


def share_available_roof():
    """
    Real Name: share available roof
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G28')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share available roof over total urban land.
    """
    return _ext_constant_share_available_roof()


def share_available_roof_for_rooftop_pv():
    """
    Real Name: share available roof for rooftop PV
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G29')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_rooftop_pv()


def share_available_roof_for_solar_thermal():
    """
    Real Name: share available roof for solar thermal
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G30')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_solar_thermal()


def start_year_p_f1_solar_pv():
    """
    Real Name: Start year P f1 solar PV
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G25')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_start_year_p_f1_solar_pv()


def target_year_f1_solar_pv():
    """
    Real Name: Target year f1 solar PV
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'G26')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_target_year_f1_solar_pv()


def twhmha_per_wem2():
    """
    Real Name: "TWh/Mha per We/m2"
    Original Eqn: 0.01
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion factor.
    """
    return 0.01


_ext_constant_av_solar_i = ExtConstant(
    "../../scenarios/scen_eu.xlsx", "BAU", "K24", {}, _root, "_ext_constant_av_solar_i"
)


_ext_constant_f1_pv_solar_in_target_year = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G24",
    {},
    _root,
    "_ext_constant_f1_pv_solar_in_target_year",
)


_ext_constant_f1ini_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cell_efficiency_conversion_of_solar_pv",
    {},
    _root,
    "_ext_constant_f1ini_solar_pv",
)


_ext_constant_f2_pf_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "performance_ratio_over_the_plant_lifecycle_of_solar_pv",
    {},
    _root,
    "_ext_constant_f2_pf_solar_pv",
)


_ext_constant_f3_solar_pv_on_land = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "land_occupation_ratio_of_solar_pv",
    {},
    _root,
    "_ext_constant_f3_solar_pv_on_land",
)


_ext_constant_power_density_initial_res_elec_twemha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_power_density_initial_res_elec_twemha",
)


_ext_constant_share_available_roof = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G28",
    {},
    _root,
    "_ext_constant_share_available_roof",
)


_ext_constant_share_available_roof_for_rooftop_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G29",
    {},
    _root,
    "_ext_constant_share_available_roof_for_rooftop_pv",
)


_ext_constant_share_available_roof_for_solar_thermal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G30",
    {},
    _root,
    "_ext_constant_share_available_roof_for_solar_thermal",
)


_ext_constant_start_year_p_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G25",
    {},
    _root,
    "_ext_constant_start_year_p_f1_solar_pv",
)


_ext_constant_target_year_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "G26",
    {},
    _root,
    "_ext_constant_target_year_f1_solar_pv",
)
