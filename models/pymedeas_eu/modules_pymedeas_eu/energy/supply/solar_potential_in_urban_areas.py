"""
Module solar_potential_in_urban_areas
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="av solar I",
    units="We/m2",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_av_solar_i"},
)
def av_solar_i():
    """
    Average solar irradiance.
    """
    return _ext_constant_av_solar_i()


_ext_constant_av_solar_i = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "average_solar_I",
    {},
    _root,
    {},
    "_ext_constant_av_solar_i",
)


@component.add(
    name="f1 PV solar in target year",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_f1_pv_solar_in_target_year"},
)
def f1_pv_solar_in_target_year():
    """
    Cell efficiency solar PV in target year.
    """
    return _ext_constant_f1_pv_solar_in_target_year()


_ext_constant_f1_pv_solar_in_target_year = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "cell_efficiency_target_year",
    {},
    _root,
    {},
    "_ext_constant_f1_pv_solar_in_target_year",
)


@component.add(
    name="f1 solar PV",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "f1ini_solar_pv": 4,
        "f1_pv_solar_in_target_year": 2,
        "target_year_f1_solar_pv": 2,
        "start_year_p_f1_solar_pv": 3,
    },
)
def f1_solar_pv():
    """
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


@component.add(
    name='"f1-ini solar PV"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_f1ini_solar_pv"},
)
def f1ini_solar_pv():
    """
    Current cell efficiency conversion of solar PV.
    """
    return _ext_constant_f1ini_solar_pv()


_ext_constant_f1ini_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cell_efficiency_conversion_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f1ini_solar_pv",
)


@component.add(
    name="f2 PF solar PV",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_f2_pf_solar_pv"},
)
def f2_pf_solar_pv():
    """
    Average performance ratio over the plant's life cycle (f2).
    """
    return _ext_constant_f2_pf_solar_pv()


_ext_constant_f2_pf_solar_pv = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "performance_ratio_over_the_plant_lifecycle_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f2_pf_solar_pv",
)


@component.add(
    name="f3 solar PV on land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_f3_solar_pv_on_land"},
)
def f3_solar_pv_on_land():
    """
    Land occupation ratio (f3).
    """
    return _ext_constant_f3_solar_pv_on_land()


_ext_constant_f3_solar_pv_on_land = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "land_occupation_ratio_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f3_solar_pv_on_land",
)


@component.add(
    name="max FE solar thermal urban TWth",
    units="TWth",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_density_solar_thermal_in_urban_twemha": 1, "urban_land": 1},
)
def max_fe_solar_thermal_urban_twth():
    """
    Potential of solar thermal in urban areas (final energy).
    """
    return power_density_solar_thermal_in_urban_twemha() * urban_land()


@component.add(
    name="max solar PV urban",
    units="TWe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_density_solar_pv_in_urban_twemha": 1, "urban_land": 1},
)
def max_solar_pv_urban():
    """
    Potential of solar PV in urban areas.
    """
    return power_density_solar_pv_in_urban_twemha() * urban_land()


@component.add(
    name='"power density initial RES elec TWe/Mha"',
    units="TWe/MHa",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_power_density_initial_res_elec_twemha"},
)
def power_density_initial_res_elec_twemha():
    """
    Input parameter: power density per RES technology for delivering electricity.
    """
    return _ext_constant_power_density_initial_res_elec_twemha()


_ext_constant_power_density_initial_res_elec_twemha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_power_density_initial_res_elec_twemha",
)


@component.add(
    name='"power density RES elec TWe/Mha"',
    units="TWe/MHa",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "power_density_initial_res_elec_twemha": 7,
        "cp_res_elec": 8,
        "cpini_res_elec": 8,
        "power_density_solar_pv_on_land_twemha": 1,
    },
)
def power_density_res_elec_twemha():
    """
    Power density of renewable energy technologies for electricity generation. TODO
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = float(
        power_density_initial_res_elec_twemha().loc["hydro"]
    ) * (float(cp_res_elec().loc["hydro"]) / float(cpini_res_elec().loc["hydro"]))
    value.loc[["geot elec"]] = float(
        power_density_initial_res_elec_twemha().loc["geot elec"]
    ) * (
        float(cp_res_elec().loc["geot elec"]) / float(cpini_res_elec().loc["geot elec"])
    )
    value.loc[["solid bioE elec"]] = float(
        power_density_initial_res_elec_twemha().loc["solid bioE elec"]
    ) * (
        float(cp_res_elec().loc["solid bioE elec"])
        / float(cpini_res_elec().loc["solid bioE elec"])
    )
    value.loc[["oceanic"]] = float(
        power_density_initial_res_elec_twemha().loc["oceanic"]
    ) * (float(cp_res_elec().loc["oceanic"]) / float(cpini_res_elec().loc["oceanic"]))
    value.loc[["wind onshore"]] = float(
        power_density_initial_res_elec_twemha().loc["wind onshore"]
    ) * (
        float(cp_res_elec().loc["wind onshore"])
        / float(cpini_res_elec().loc["wind onshore"])
    )
    value.loc[["wind offshore"]] = float(
        power_density_initial_res_elec_twemha().loc["wind offshore"]
    ) * (
        float(cp_res_elec().loc["wind offshore"])
        / float(cpini_res_elec().loc["wind offshore"])
    )
    value.loc[["solar PV"]] = power_density_solar_pv_on_land_twemha() * (
        float(cp_res_elec().loc["solar PV"]) / float(cpini_res_elec().loc["solar PV"])
    )
    value.loc[["CSP"]] = float(power_density_initial_res_elec_twemha().loc["CSP"]) * (
        float(cp_res_elec().loc["CSP"]) / float(cpini_res_elec().loc["CSP"])
    )
    return value


@component.add(
    name='"power density solar PV in urban TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_pv": 1,
        "f2_pf_solar_pv": 1,
        "share_available_roof": 1,
        "share_available_roof_for_rooftop_pv": 1,
        "twhmha_per_wem2": 1,
    },
)
def power_density_solar_pv_in_urban_twemha():
    """
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


@component.add(
    name='"power density solar PV on land TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_pv": 1,
        "f2_pf_solar_pv": 1,
        "f3_solar_pv_on_land": 1,
        "twhmha_per_wem2": 1,
    },
)
def power_density_solar_pv_on_land_twemha():
    """
    Power density of solar PV power plants on land.
    """
    return (
        av_solar_i()
        * f1_solar_pv()
        * f2_pf_solar_pv()
        * f3_solar_pv_on_land()
        * twhmha_per_wem2()
    )


@component.add(
    name='"power density solar thermal in urban TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_panels_for_heat": 1,
        "losses_solar_for_heat": 1,
        "share_available_roof": 1,
        "share_available_roof_for_solar_thermal": 1,
        "twhmha_per_wem2": 1,
    },
)
def power_density_solar_thermal_in_urban_twemha():
    """
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


@component.add(
    name="share available roof",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_available_roof"},
)
def share_available_roof():
    """
    Share available roof over total urban land.
    """
    return _ext_constant_share_available_roof()


_ext_constant_share_available_roof = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_available_roof",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof",
)


@component.add(
    name="share available roof for rooftop PV",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_available_roof_for_rooftop_pv"},
)
def share_available_roof_for_rooftop_pv():
    """
    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_rooftop_pv()


_ext_constant_share_available_roof_for_rooftop_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_available_roof_for_rooftop_PV",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof_for_rooftop_pv",
)


@component.add(
    name="share available roof for solar thermal",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_available_roof_for_solar_thermal"},
)
def share_available_roof_for_solar_thermal():
    """
    Share of available roof in urban land for rooftop PV.
    """
    return _ext_constant_share_available_roof_for_solar_thermal()


_ext_constant_share_available_roof_for_solar_thermal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_roof_solar_thermal",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof_for_solar_thermal",
)


@component.add(
    name="Start year P f1 solar PV",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_f1_solar_pv"},
)
def start_year_p_f1_solar_pv():
    """
    Start year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_start_year_p_f1_solar_pv()


_ext_constant_start_year_p_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_cell_efficency_PV",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_f1_solar_pv",
)


@component.add(
    name="Target year f1 solar PV",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_target_year_f1_solar_pv"},
)
def target_year_f1_solar_pv():
    """
    Target year of the variation of cell efficiency of solar PV.
    """
    return _ext_constant_target_year_f1_solar_pv()


_ext_constant_target_year_f1_solar_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "targ_year_cell_efficiency_PV",
    {},
    _root,
    {},
    "_ext_constant_target_year_f1_solar_pv",
)


@component.add(
    name='"TWh/Mha per We/m2"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def twhmha_per_wem2():
    """
    Conversion factor.
    """
    return 0.01
