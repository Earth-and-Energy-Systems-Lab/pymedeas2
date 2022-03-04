"""
Module solar_potential_in_urban_areas
Translated using PySD version 2.2.1
"""


def av_solar_i():
    """
    Real Name: av solar I
    Original Eqn:
    Units: We/m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average solar irradiance.
    """
    return _ext_constant_av_solar_i()


_ext_constant_av_solar_i = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "average_solar_I",
    {},
    _root,
    "_ext_constant_av_solar_i",
)


def f1_pv_solar_in_target_year():
    """
    Real Name: f1 PV solar in target year
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Cell efficiency solar PV in target year.
    """
    return _ext_constant_f1_pv_solar_in_target_year()


_ext_constant_f1_pv_solar_in_target_year = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "cell_efficiency_target_year",
    {},
    _root,
    "_ext_constant_f1_pv_solar_in_target_year",
)


def f1_solar_pv():
    """
    Real Name: f1 solar PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current cell efficiency conversion of solar PV.
    """
    return _ext_constant_f1ini_solar_pv()


_ext_constant_f1ini_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cell_efficiency_conversion_of_solar_pv",
    {},
    _root,
    "_ext_constant_f1ini_solar_pv",
)


def f2_pf_solar_pv():
    """
    Real Name: f2 PF solar PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average performance ratio over the plant's life cycle (f2).
    """
    return _ext_constant_f2_pf_solar_pv()


_ext_constant_f2_pf_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "performance_ratio_over_the_plant_lifecycle_of_solar_pv",
    {},
    _root,
    "_ext_constant_f2_pf_solar_pv",
)


def f3_solar_pv_on_land():
    """
    Real Name: f3 solar PV on land
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Land occupation ratio (f3).
    """
    return _ext_constant_f3_solar_pv_on_land()


_ext_constant_f3_solar_pv_on_land = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "land_occupation_ratio_of_solar_pv",
    {},
    _root,
    "_ext_constant_f3_solar_pv_on_land",
)


def max_fe_solar_thermal_urban_twth():
    """
    Real Name: max FE solar thermal urban TWth
    Original Eqn:
    Units: TWth
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential of solar thermal in urban areas (final energy).
    """
    return power_density_solar_thermal_in_urban_twemha() * urban_land()


def max_solar_pv_urban():
    """
    Real Name: max solar PV urban
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential of solar PV in urban areas.
    """
    return power_density_solar_pv_in_urban_twemha() * urban_land()


@subs(["RES elec"], _subscript_dict)
def power_density_res_elec_twemha():
    """
    Real Name: "power density RES elec TWe/Mha"
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Power density of renewable energy technologies for electricity generation. TODO
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = float(
        power_density_initial_res_elec_twemha().loc["hydro"]
    ) * (float(cp_res_elec().loc["hydro"]) / float(cpini_res_elec().loc["hydro"]))
    value.loc[{"RES elec": ["geot elec"]}] = float(
        power_density_initial_res_elec_twemha().loc["geot elec"]
    ) * (
        float(cp_res_elec().loc["geot elec"]) / float(cpini_res_elec().loc["geot elec"])
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = float(
        power_density_initial_res_elec_twemha().loc["solid bioE elec"]
    ) * (
        float(cp_res_elec().loc["solid bioE elec"])
        / float(cpini_res_elec().loc["solid bioE elec"])
    )
    value.loc[{"RES elec": ["oceanic"]}] = float(
        power_density_initial_res_elec_twemha().loc["oceanic"]
    ) * (float(cp_res_elec().loc["oceanic"]) / float(cpini_res_elec().loc["oceanic"]))
    value.loc[{"RES elec": ["wind onshore"]}] = float(
        power_density_initial_res_elec_twemha().loc["wind onshore"]
    ) * (
        float(cp_res_elec().loc["wind onshore"])
        / float(cpini_res_elec().loc["wind onshore"])
    )
    value.loc[{"RES elec": ["wind offshore"]}] = float(
        power_density_initial_res_elec_twemha().loc["wind offshore"]
    ) * (
        float(cp_res_elec().loc["wind offshore"])
        / float(cpini_res_elec().loc["wind offshore"])
    )
    value.loc[{"RES elec": ["solar PV"]}] = power_density_solar_pv_on_land_twemha() * (
        float(cp_res_elec().loc["solar PV"]) / float(cpini_res_elec().loc["solar PV"])
    )
    value.loc[{"RES elec": ["CSP"]}] = float(
        power_density_initial_res_elec_twemha().loc["CSP"]
    ) * (float(cp_res_elec().loc["CSP"]) / float(cpini_res_elec().loc["CSP"]))
    return value


def power_density_solar_pv_in_urban_twemha():
    """
    Real Name: "power density solar PV in urban TWe/Mha"
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


@subs(["RES elec"], _subscript_dict)
def power_density_initial_res_elec_twemha():
    """
    Real Name: "power density initial RES elec TWe/Mha"
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Constant
    Subs: ['RES elec']

    Input parameter: power density per RES technology for delivering electricity.
    """
    return _ext_constant_power_density_initial_res_elec_twemha()


_ext_constant_power_density_initial_res_elec_twemha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_power_density_initial_res_elec_twemha",
)


def share_available_roof():
    """
    Real Name: share available roof
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share available roof over total urban land.
    """
    return _ext_constant_share_available_roof()


_ext_constant_share_available_roof = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_available_roof",
    {},
    _root,
    "_ext_constant_share_available_roof",
)


def share_available_roof_for_rooftop_pv():
    """
    Real Name: share available roof for rooftop PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_rooftop_pv()


_ext_constant_share_available_roof_for_rooftop_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_available_roof_for_rooftop_PV",
    {},
    _root,
    "_ext_constant_share_available_roof_for_rooftop_pv",
)


def share_available_roof_for_solar_thermal():
    """
    Real Name: share available roof for solar thermal
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_solar_thermal()


_ext_constant_share_available_roof_for_solar_thermal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_roof_solar_thermal",
    {},
    _root,
    "_ext_constant_share_available_roof_for_solar_thermal",
)


def start_year_p_f1_solar_pv():
    """
    Real Name: Start year P f1 solar PV
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Start year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_start_year_p_f1_solar_pv()


_ext_constant_start_year_p_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_cell_efficency_PV",
    {},
    _root,
    "_ext_constant_start_year_p_f1_solar_pv",
)


def target_year_f1_solar_pv():
    """
    Real Name: Target year f1 solar PV
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Target year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_target_year_f1_solar_pv()


_ext_constant_target_year_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "targ_year_cell_efficiency_PV",
    {},
    _root,
    "_ext_constant_target_year_f1_solar_pv",
)


def twhmha_per_wem2():
    """
    Real Name: "TWh/Mha per We/m2"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion factor.
    """
    return 0.01
