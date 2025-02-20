"""
Module energy.supply.res_elec_potentials
Translated using PySD version 3.14.0
"""

@component.add(
    name="Efficiency conversion geot PE to Elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_conversion_geot_pe_to_elec"},
)
def efficiency_conversion_geot_pe_to_elec():
    """
    Efficiency of the transformation from geothermal (primary energy) to electricity.
    """
    return _ext_constant_efficiency_conversion_geot_pe_to_elec()


_ext_constant_efficiency_conversion_geot_pe_to_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_geot_pe_to_elec",
    {},
    _root,
    {},
    "_ext_constant_efficiency_conversion_geot_pe_to_elec",
)


@component.add(
    name="max CSP on land MHa",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_solar_on_land_mha": 1, "surface_solar_pv_mha": 1},
)
def max_csp_on_land_mha():
    """
    Available land for solar CSP taking into account the total land availability for solar and the actual occupation from solar PV on land.
    """
    return max_solar_on_land_mha() - surface_solar_pv_mha()


@component.add(
    name='"max PE geot-elec TWth"',
    units="TWe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_pe_geotelec_twth"},
)
def max_pe_geotelec_twth():
    """
    Primary energy of geothermal for electricity.
    """
    return _ext_constant_max_pe_geotelec_twth()


_ext_constant_max_pe_geotelec_twth = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_PE_geot_elect_potential",
    {},
    _root,
    {},
    "_ext_constant_max_pe_geotelec_twth",
)


@component.add(
    name="max potential RES elec TWe",
    units="TW",
    subscripts=[np.str_("RES elec")],
    comp_type="Constant, Auxiliary",
    comp_subtype="External, Normal",
    depends_on={
        "__external__": "_ext_constant_max_potential_res_elec_twe",
        "max_pe_geotelec_twth": 1,
        "efficiency_conversion_geot_pe_to_elec": 1,
        "ej_per_twh": 1,
        "twe_per_twh": 1,
        "available_potential_fe_solid_bioe_for_elec": 1,
        "max_solar_pv_on_land_mha": 1,
        "power_density_res_elec_twemha": 2,
        "max_csp_on_land_mha": 1,
    },
)
def max_potential_res_elec_twe():
    """
    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, [np.str_("RES elec")]
    )
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["hydro"]] = True
    def_subs.loc[["oceanic"]] = True
    def_subs.loc[["wind onshore"]] = True
    def_subs.loc[["wind offshore"]] = True
    value.values[def_subs.values] = _ext_constant_max_potential_res_elec_twe().values[
        def_subs.values
    ]
    value.loc[["geot elec"]] = (
        max_pe_geotelec_twth() * efficiency_conversion_geot_pe_to_elec()
    )
    value.loc[["solid bioE elec"]] = (
        available_potential_fe_solid_bioe_for_elec() / ej_per_twh() * twe_per_twh()
    )
    value.loc[["solar PV"]] = max_solar_pv_on_land_mha() * float(
        power_density_res_elec_twemha().loc["solar PV"]
    )
    value.loc[["CSP"]] = max_csp_on_land_mha() * float(
        power_density_res_elec_twemha().loc["CSP"]
    )
    return value


_ext_constant_max_potential_res_elec_twe = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_hydro_potential",
    {"RES elec": ["hydro"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_max_potential_res_elec_twe",
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx", "World", "max_oceanic_potential", {"RES elec": ["oceanic"]}
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx",
    "World",
    "max_onshore_wind_potential",
    {"RES elec": ["wind onshore"]},
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx",
    "World",
    "max_offshore_wind_potential",
    {"RES elec": ["wind offshore"]},
)


@component.add(
    name="max potential RES elec TWh",
    units="TWh/year",
    subscripts=[np.str_("RES elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_potential_res_elec_twe": 1, "twe_per_twh": 1},
)
def max_potential_res_elec_twh():
    """
    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    return max_potential_res_elec_twe() / twe_per_twh()


@component.add(
    name="max potential tot RES elec TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_res_elec_twh": 1,
        "twe_per_twh": 1,
        "max_potential_phs_twe": 1,
        "share_pes_biogas_for_elec": 1,
        "ej_per_twh": 1,
        "max_biogas_ej": 1,
    },
)
def max_potential_tot_res_elec_twh():
    """
    Maximum total potential of RES for electricity considering an optimal Cp.
    """
    return (
        sum(
            max_potential_res_elec_twh().rename({np.str_("RES elec"): "RES elec!"}),
            dim=["RES elec!"],
        )
        + max_potential_phs_twe() / twe_per_twh()
        + max_biogas_ej() * share_pes_biogas_for_elec() / ej_per_twh()
    )


@component.add(
    name="max solar on land Mha",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_solar_on_land_mha"},
)
def max_solar_on_land_mha():
    """
    Assumed land availability for solar power plants on land (PV and CSP).
    """
    return _ext_constant_max_solar_on_land_mha()


_ext_constant_max_solar_on_land_mha = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_solar_on_land_potential",
    {},
    _root,
    {},
    "_ext_constant_max_solar_on_land_mha",
)


@component.add(
    name="max solar PV on land MHa",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_solar_on_land_mha": 1, "surface_csp_mha": 1},
)
def max_solar_pv_on_land_mha():
    """
    Available land for solar PV taking into account the total land availability for solar and the actual occupation from CSP.
    """
    return max_solar_on_land_mha() - surface_csp_mha()


@component.add(
    name="Percent remaining potential tot RES elec",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"remaining_potential_tot_res_elec": 1},
)
def percent_remaining_potential_tot_res_elec():
    """
    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_elec() * 100


@component.add(
    name="remaining potential",
    units="Dmnl",
    subscripts=[np.str_("RES elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_potential_res_elec_twh": 3, "real_generation_res_elec_twh": 2},
)
def remaining_potential():
    return if_then_else(
        max_potential_res_elec_twh() > real_generation_res_elec_twh(),
        lambda: (max_potential_res_elec_twh() - real_generation_res_elec_twh())
        / max_potential_res_elec_twh(),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="remaining potential tot RES elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_tot_res_elec_twh": 3,
        "fe_tot_generation_all_res_elec_twh": 2,
    },
)
def remaining_potential_tot_res_elec():
    """
    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_potential_tot_res_elec_twh() > fe_tot_generation_all_res_elec_twh(),
        lambda: (
            max_potential_tot_res_elec_twh() - fe_tot_generation_all_res_elec_twh()
        )
        / max_potential_tot_res_elec_twh(),
        lambda: 0,
    )
