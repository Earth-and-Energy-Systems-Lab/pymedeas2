"""
Module environment.land.res_land_use
Translated using PySD version 3.14.0
"""

@component.add(
    name="Agricultural_land_2015",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_agricultural_land_2015"},
)
def agricultural_land_2015():
    return _ext_constant_agricultural_land_2015()


_ext_constant_agricultural_land_2015 = ExtConstant(
    "../land.xlsx",
    "Catalonia",
    "agricultural_land_2015",
    {},
    _root,
    {},
    "_ext_constant_agricultural_land_2015",
)


@component.add(
    name="Land_requirements_RES_elec_compet_uses",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "surface_hydro_mha": 1,
        "surface_csp_mha": 1,
        "surface_solar_pv_on_land_mha": 1,
        "surface_onshore_wind_mha": 1,
    },
)
def land_requirements_res_elec_compet_uses():
    """
    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro) requiring land and not easily compatible with double uses.
    """
    return (
        surface_hydro_mha()
        + surface_csp_mha()
        + surface_solar_pv_on_land_mha()
        + surface_onshore_wind_mha()
    )


@component.add(
    name="Land_saved_by_urban_PV",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "real_share_pv_urban_vs_total_pv": 1,
        "power_density_res_elec_twemha": 1,
        "twe_per_twh": 1,
    },
)
def land_saved_by_urban_pv():
    """
    Land saved by urban PV.
    """
    return zidz(
        float(potential_generation_res_elec_twh().loc["solar_PV"])
        * real_share_pv_urban_vs_total_pv(),
        float(power_density_res_elec_twemha().loc["solar_PV"]) / twe_per_twh(),
    )


@component.add(
    name="real_share_PV_urban_vs_total_PV_delayed",
    units="percent",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_share_pv_urban_vs_total_pv_delayed": 1},
    other_deps={
        "_delayfixed_real_share_pv_urban_vs_total_pv_delayed": {
            "initial": {"time_step": 1},
            "step": {"real_share_pv_urban_vs_total_pv": 1},
        }
    },
)
def real_share_pv_urban_vs_total_pv_delayed():
    return _delayfixed_real_share_pv_urban_vs_total_pv_delayed()


_delayfixed_real_share_pv_urban_vs_total_pv_delayed = DelayFixed(
    lambda: real_share_pv_urban_vs_total_pv(),
    lambda: time_step(),
    lambda: 0.5,
    time_step,
    "_delayfixed_real_share_pv_urban_vs_total_pv_delayed",
)


@component.add(
    name="Share_land_compet_biofuels",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "agricultural_land_2015": 1,
    },
)
def share_land_compet_biofuels():
    """
    Share of global arable land required by dedicated crops for biofuels (in land competition).
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels() / agricultural_land_2015()
    )


@component.add(
    name="share_land_RES_land_compet_vs_arable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "surface_solar_pv_on_land_mha": 1,
        "surface_csp_mha": 1,
        "surface_hydro_mha": 1,
        "agricultural_land_2015": 1,
    },
)
def share_land_res_land_compet_vs_arable():
    """
    Land requirements for RES that compete with other land-uses (solar on land and biofuels on land competition) as a share of the global arable land.
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels()
        + surface_solar_pv_on_land_mha()
        + surface_csp_mha()
        + surface_hydro_mha()
    ) / agricultural_land_2015()


@component.add(
    name="share_land_total_RES_vs_arable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "agricultural_land_2015": 1},
)
def share_land_total_res_vs_arable():
    """
    Land requirements for all RES as a share of the global arable land.
    """
    return total_land_requirements_renew_mha() / agricultural_land_2015()


@component.add(
    name="share_land_total_RES_vs_urban_surface",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "urban_surface_2015": 1},
)
def share_land_total_res_vs_urban_surface():
    """
    Land requirements for all RES as a share of the global urban land.
    """
    return total_land_requirements_renew_mha() / urban_surface_2015()


@component.add(
    name="surface_CSP_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_csp_mha():
    """
    Area required for CSP.
    """
    return float(surface_res_elec().loc["CSP"])


@component.add(
    name="surface_hydro_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_hydro_mha():
    """
    Surface required by hydropower plants.
    """
    return float(surface_res_elec().loc["hydro"])


@component.add(
    name="surface_onshore_wind_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_onshore_wind_mha():
    """
    Surface required to produce "onshore wind TWe".
    """
    return float(surface_res_elec().loc["wind_onshore"])


@component.add(
    name="surface_RES_elec",
    units="MHa",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "power_density_res_elec_twemha": 4,
        "installed_capacity_res_elec_delayed": 2,
        "real_share_pv_urban_vs_total_pv_delayed": 1,
    },
)
def surface_res_elec():
    """
    Land requirements by renewable technologies for electricity generation.
    """
    value = xr.DataArray(
        np.nan, {"RES_elec": _subscript_dict["RES_elec"]}, [np.str_("RES_elec")]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solar_PV"]] = False
    value.values[except_subs.values] = if_then_else(
        power_density_res_elec_twemha() == 0,
        lambda: xr.DataArray(
            0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
        lambda: installed_capacity_res_elec_delayed() / power_density_res_elec_twemha(),
    ).values[except_subs.values]
    value.loc[["solar_PV"]] = if_then_else(
        float(power_density_res_elec_twemha().loc["solar_PV"]) == 0,
        lambda: 0,
        lambda: float(installed_capacity_res_elec_delayed().loc["solar_PV"])
        / float(power_density_res_elec_twemha().loc["solar_PV"]),
    ) * (1 - real_share_pv_urban_vs_total_pv_delayed())
    return value


@component.add(
    name="surface_solar_PV_on_land_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_solar_pv_on_land_mha():
    """
    Area required for solar PV plants on land.
    """
    return float(surface_res_elec().loc["solar_PV"])


@component.add(
    name="Total_land_requirements_renew_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_requirements_res_elec_compet_uses": 1,
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "nvs_1_year": 1,
        "land_required_biofuels_land_marg": 1,
        "surface_onshore_wind_mha": 1,
    },
)
def total_land_requirements_renew_mha():
    """
    Land required for RES power plants and total bioenergy (land competition + marginal lands).
    """
    return (
        land_requirements_res_elec_compet_uses()
        + land_compet_required_dedicated_crops_for_biofuels()
        + land_required_biofuels_land_marg() * nvs_1_year()
        + surface_onshore_wind_mha()
    )


@component.add(
    name="urban_surface_2015",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urban_surface_2015"},
)
def urban_surface_2015():
    """
    Area currently occupied by human settlement and infraestructures.
    """
    return _ext_constant_urban_surface_2015()


_ext_constant_urban_surface_2015 = ExtConstant(
    "../land.xlsx",
    "Catalonia",
    "urban_surface_2015",
    {},
    _root,
    {},
    "_ext_constant_urban_surface_2015",
)
