"""
Module energy.supply.solar_potential_in_urban_areas
Translated using PySD version 3.14.2
"""

@component.add(
    name="av_solar_I",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "average_solar_irradiance",
    {},
    _root,
    {},
    "_ext_constant_av_solar_i",
)


@component.add(
    name="f1_PV_solar_in_target_year",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "cell_efficiency_PV_target_year",
    {},
    _root,
    {},
    "_ext_constant_f1_pv_solar_in_target_year",
)


@component.add(
    name="f1_solar_PV",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "f1ini_solar_pv": 4,
        "target_year_f1_solar_pv": 2,
        "f1_pv_solar_in_target_year": 2,
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
    name='"f1-ini_solar_PV"',
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
    r"../energy.xlsx",
    "Catalonia",
    "cell_efficiency_conversion_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f1ini_solar_pv",
)


@component.add(
    name="f2_PF_solar_PV",
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
    r"../energy.xlsx",
    "Catalonia",
    "performance_ratio_over_the_plant_lifecycle_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f2_pf_solar_pv",
)


@component.add(
    name="f3_solar_PV_on_land",
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
    r"../energy.xlsx",
    "Catalonia",
    "land_occupation_ratio_of_solar_pv",
    {},
    _root,
    {},
    "_ext_constant_f3_solar_pv_on_land",
)


@component.add(
    name='"Land_module_activated?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_module_activated():
    """
    Switch to enable/disable Land module: 0- DISABLED 1- ENABLED
    """
    return 1


@component.add(
    name="max_FE_solar_thermal_urban_TWth",
    units="TWth",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_module_activated": 1,
        "power_density_solar_thermal_in_urban_twemha": 2,
        "urban_land": 1,
        "urban_surface_2015": 1,
    },
)
def max_fe_solar_thermal_urban_twth():
    """
    Potential of solar thermal in urban areas (final energy).
    """
    return if_then_else(
        land_module_activated() == 1,
        lambda: power_density_solar_thermal_in_urban_twemha() * urban_land(),
        lambda: power_density_solar_thermal_in_urban_twemha() * urban_surface_2015(),
    )


@component.add(
    name="max_solar_PV_urban",
    units="TWe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_module_activated": 1,
        "power_density_solar_pv_in_urban_twemha": 2,
        "urban_land": 1,
        "urban_surface_2015": 1,
    },
)
def max_solar_pv_urban():
    """
    Potential of solar PV in urban areas.
    """
    return if_then_else(
        land_module_activated() == 1,
        lambda: power_density_solar_pv_in_urban_twemha() * urban_land(),
        lambda: power_density_solar_pv_in_urban_twemha() * urban_surface_2015(),
    )


@component.add(
    name='"power_density_initial_RES_elec_TWe/Mha"',
    units="TWe/MHa",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_power_density_initial_res_elec_twemha",
)


@component.add(
    name='"power_density_RES_elec_TWe/Mha"',
    units="TWe/MHa",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "power_density_initial_res_elec_twemha": 1,
        "cpini_res_elec": 2,
        "cp_res_elec": 4,
        "power_density_solar_pv_on_land_twemha": 1,
    },
)
def power_density_res_elec_twemha():
    """
    Power density of renewable energy technologies for electricity generation.
    """
    value = xr.DataArray(
        np.nan, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solar_PV"]] = False
    value.values[except_subs.values] = (
        power_density_initial_res_elec_twemha()
        * zidz(cp_res_elec(), cpini_res_elec())
        / cp_res_elec()
    ).values[except_subs.values]
    value.loc[["solar_PV"]] = (
        power_density_solar_pv_on_land_twemha()
        * zidz(
            float(cp_res_elec().loc["solar_PV"]),
            float(cpini_res_elec().loc["solar_PV"]),
        )
        / float(cp_res_elec().loc["solar_PV"])
    )
    return value


@component.add(
    name='"power_density_solar_PV_in_urban_TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_pv": 1,
        "f2_pf_solar_pv": 1,
        "share_available_roof": 1,
        "share_available_roof_for_rooftop_pv": 1,
        "twmha_per_wem2": 1,
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
        * twmha_per_wem2()
    )


@component.add(
    name='"power_density_solar_PV_on_land_TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_pv": 1,
        "f2_pf_solar_pv": 1,
        "f3_solar_pv_on_land": 1,
        "twmha_per_wem2": 1,
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
        * twmha_per_wem2()
    )


@component.add(
    name='"power_density_solar_thermal_in_urban_TWe/Mha"',
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "av_solar_i": 1,
        "f1_solar_panels_for_heat": 1,
        "losses_solar_for_heat": 1,
        "share_available_roof": 1,
        "share_available_roof_for_solar_thermal": 1,
        "twmha_per_wem2": 1,
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
        * twmha_per_wem2()
    )


@component.add(
    name="share_available_roof",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_available_roof",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof",
)


@component.add(
    name="share_available_roof_for_rooftop_PV",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_available_roof_for_rooftop_PV",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof_for_rooftop_pv",
)


@component.add(
    name="share_available_roof_for_solar_thermal",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "share_roof_solar_thermal",
    {},
    _root,
    {},
    "_ext_constant_share_available_roof_for_solar_thermal",
)


@component.add(
    name="Start_year_P_f1_solar_PV",
    units="year",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_cell_efficency_PV",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_f1_solar_pv",
)


@component.add(
    name="Target_year_f1_solar_PV",
    units="year",
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "targ_year_cell_efficiency_PV",
    {},
    _root,
    {},
    "_ext_constant_target_year_f1_solar_pv",
)


@component.add(
    name='"TW/Mha_per_We/m2"',
    units="(TW/MHa)/(We/m2)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def twmha_per_wem2():
    """
    Conversion factor.
    """
    return 0.01
