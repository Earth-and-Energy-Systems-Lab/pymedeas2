"""
Module energy.supply.res_elec_potentials
Translated using PySD version 3.14.1
"""

@component.add(
    name="available max FE solid bioE for elec EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_max_pe_solid_bioe_for_elec": 1,
        "efficiency_conversion_bioe_to_elec": 1,
    },
)
def available_max_fe_solid_bioe_for_elec_ej():
    """
    Maximum available (final energy) solid bioenergy for electricity.
    """
    return available_max_pe_solid_bioe_for_elec() * efficiency_conversion_bioe_to_elec()


@component.add(
    name="desired share installed PV urban vs tot PV",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_share_installed_pv_urban_vs_tot_pv": 2,
        "p_share_installed_pv_urban_vs_tot_pv": 1,
        "start_year_p_growth_res_elec": 1,
    },
)
def desired_share_installed_pv_urban_vs_tot_pv():
    """
    Desired share of installed PV in urban areas vs total PV installed.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_share_installed_pv_urban_vs_tot_pv(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: historic_share_installed_pv_urban_vs_tot_pv(),
            lambda: p_share_installed_pv_urban_vs_tot_pv(),
        ),
    )


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
    r"../energy.xlsx",
    "Global",
    "efficiency_conversion_geot_pe_to_elec",
    {},
    _root,
    {},
    "_ext_constant_efficiency_conversion_geot_pe_to_elec",
)


@component.add(
    name="FE Elec gen from solar PV on land TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_generation_res_elec_twh": 1,
        "real_share_pv_urban_vs_total_pv": 1,
    },
)
def fe_elec_gen_from_solar_pv_on_land_twh():
    """
    Electricity generation from solar PV on land.
    """
    return float(real_generation_res_elec_twh().loc["solar PV"]) * (
        1 - real_share_pv_urban_vs_total_pv()
    )


@component.add(
    name="historic share installed PV urban vs tot PV",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_installed_pv_urban_vs_tot_pv",
        "__data__": "_ext_data_historic_share_installed_pv_urban_vs_tot_pv",
        "time": 1,
    },
)
def historic_share_installed_pv_urban_vs_tot_pv():
    return _ext_data_historic_share_installed_pv_urban_vs_tot_pv(time())


_ext_data_historic_share_installed_pv_urban_vs_tot_pv = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_urban_pv_over_total",
    None,
    {},
    _root,
    {},
    "_ext_data_historic_share_installed_pv_urban_vs_tot_pv",
)


@component.add(
    name="max BioE TWe",
    units="TWe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_max_fe_solid_bioe_for_elec_ej": 1,
        "twe_per_twh": 1,
        "ej_per_twh": 1,
    },
)
def max_bioe_twe():
    """
    Techno-ecological potential of biomass&waste. This potential is dynamic and dependant on the potential assigned for bioenergy residues.
    """
    return available_max_fe_solid_bioe_for_elec_ej() * twe_per_twh() / ej_per_twh()


@component.add(
    name="max CSP on land MHa",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_solar_on_land_mha": 1, "surface_solar_pv_on_land_mha": 1},
)
def max_csp_on_land_mha():
    """
    Available land for solar CSP taking into account the total land availability for solar and the actual occupation from solar PV on land.
    """
    return max_solar_on_land_mha() - surface_solar_pv_on_land_mha()


@component.add(
    name="max FE potential solid bioE for elec TWe",
    units="TWe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_pe_potential_solid_bioe_for_elec": 1,
        "efficiency_conversion_bioe_to_elec": 1,
        "twe_per_twh": 1,
        "ej_per_twh": 1,
    },
)
def max_fe_potential_solid_bioe_for_elec_twe():
    """
    Available potential (final energy) solid bioenergy for electricity.
    """
    return (
        max_pe_potential_solid_bioe_for_elec()
        * efficiency_conversion_bioe_to_elec()
        * twe_per_twh()
        / ej_per_twh()
    )


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
    r"../energy.xlsx",
    "Europe",
    "max_PE_geot_elec_potential",
    {},
    _root,
    {},
    "_ext_constant_max_pe_geotelec_twth",
)


@component.add(
    name="max PE potential biogas for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_biogas_ej": 1, "share_pes_biogas_for_elec": 1},
)
def max_pe_potential_biogas_for_elec():
    """
    Maximum potential (primary energy) of biogas for electricity.
    """
    return max_pe_biogas_ej() * share_pes_biogas_for_elec()


@component.add(
    name="max potential RES elec TWh",
    units="TWh/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_res_elec_twe": 1, "twe_per_twh": 1},
)
def max_potential_res_elec_twh():
    """
    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    return max_res_elec_twe() / twe_per_twh()


@component.add(
    name="max potential tot RES elec TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_res_elec_twh": 1,
        "max_potential_phs_twe": 1,
        "twe_per_twh": 1,
        "ej_per_twh": 1,
        "max_pe_potential_biogas_for_elec": 1,
    },
)
def max_potential_tot_res_elec_twh():
    """
    Maximum total potential of RES for electricity considering an optimal Cp.
    """
    return (
        sum(
            max_potential_res_elec_twh().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + max_potential_phs_twe() / twe_per_twh()
        + max_pe_potential_biogas_for_elec() / ej_per_twh()
    )


@component.add(
    name="max RES elec TWe",
    units="TWe",
    subscripts=["RES elec"],
    comp_type="Constant, Auxiliary",
    comp_subtype="External, Normal",
    depends_on={
        "__external__": "_ext_constant_max_res_elec_twe",
        "max_pe_geotelec_twth": 1,
        "efficiency_conversion_geot_pe_to_elec": 1,
        "max_bioe_twe": 1,
        "max_solar_pv_on_land_twe": 1,
        "max_solar_pv_urban": 1,
        "max_csp_on_land_mha": 1,
        "power_density_csp": 1,
    },
)
def max_res_elec_twe():
    """
    Maximum level of RES for electricity per technology considering an optimal Cp. For most technologies this variable corresponds with the maximum potential, excepting for solids bioenergy and solar, where given to the competing uses (solids bioenergy for heat and electricity) and competing technologies (solar PV and CSP) this variable corresponds to the maximum level from each use and technology.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["hydro"]] = True
    def_subs.loc[["oceanic"]] = True
    def_subs.loc[["wind onshore"]] = True
    def_subs.loc[["wind offshore"]] = True
    value.values[def_subs.values] = _ext_constant_max_res_elec_twe().values[
        def_subs.values
    ]
    value.loc[["geot elec"]] = (
        max_pe_geotelec_twth() * efficiency_conversion_geot_pe_to_elec()
    )
    value.loc[["solid bioE elec"]] = max_bioe_twe()
    value.loc[["solar PV"]] = max_solar_pv_on_land_twe() + max_solar_pv_urban()
    value.loc[["CSP"]] = max_csp_on_land_mha() * power_density_csp()
    return value


_ext_constant_max_res_elec_twe = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "max_hydro_potential",
    {"RES elec": ["hydro"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_max_res_elec_twe",
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx", "Europe", "max_oceanic_potential", {"RES elec": ["oceanic"]}
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx",
    "Europe",
    "max_onshore_wind_potential",
    {"RES elec": ["wind onshore"]},
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx",
    "Europe",
    "max_offshore_wind_potential",
    {"RES elec": ["wind offshore"]},
)


@component.add(
    name="max solar on land Mha",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_solar_on_land_mha"},
)
def max_solar_on_land_mha():
    return _ext_constant_max_solar_on_land_mha()


_ext_constant_max_solar_on_land_mha = ExtConstant(
    r"../energy.xlsx",
    "Europe",
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
    name="max solar PV on land TWe",
    units="TWe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_solar_pv_on_land_mha": 1,
        "power_density_solar_pv_on_land_twemha": 1,
    },
)
def max_solar_pv_on_land_twe():
    """
    Techno-ecological potential of solar PV on land. This potential depends on the assumed land availability for solar PV power plants ("max solar PV on land MHa") and its power density (1 TWe = 8760 TWh in one year).
    """
    return max_solar_pv_on_land_mha() * power_density_solar_pv_on_land_twemha()


@component.add(
    name="P share installed PV urban vs tot PV",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_share_installed_pv_urban_vs_tot_pv"},
)
def p_share_installed_pv_urban_vs_tot_pv():
    """
    User defined share of installed PV in urban areas vs total PV.
    """
    return _ext_constant_p_share_installed_pv_urban_vs_tot_pv()


_ext_constant_p_share_installed_pv_urban_vs_tot_pv = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "share_PV_urban_tot_PV",
    {},
    _root,
    {},
    "_ext_constant_p_share_installed_pv_urban_vs_tot_pv",
)


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
    name="Potential elec gen from solar PV on land TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "potential_elec_gen_from_solar_pv_urban_twh": 1,
    },
)
def potential_elec_gen_from_solar_pv_on_land_twh():
    """
    Potential electricity generation from solar PV on land.
    """
    return (
        float(potential_generation_res_elec_twh().loc["solar PV"])
        - potential_elec_gen_from_solar_pv_urban_twh()
    )


@component.add(
    name="Potential elec gen from solar PV urban TWh",
    units="TWh/year",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh": 1},
    other_deps={
        "_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh": {
            "initial": {"potential_elec_gen_from_solar_pv_urban_unconstrained_twh": 1},
            "step": {
                "remaining_potential_solar_pv_urban": 1,
                "potential_elec_gen_from_solar_pv_urban_unconstrained_twh": 1,
            },
        }
    },
)
def potential_elec_gen_from_solar_pv_urban_twh():
    """
    Potential electricity generation from solar PV in urban areas.
    """
    return _sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh()


_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh = SampleIfTrue(
    lambda: remaining_potential_solar_pv_urban() > 0,
    lambda: potential_elec_gen_from_solar_pv_urban_unconstrained_twh(),
    lambda: potential_elec_gen_from_solar_pv_urban_unconstrained_twh(),
    "_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh",
)


@component.add(
    name="Potential elec gen from solar PV urban unconstrained TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "desired_share_installed_pv_urban_vs_tot_pv": 1,
    },
)
def potential_elec_gen_from_solar_pv_urban_unconstrained_twh():
    """
    Unconstrained potential electricity generation from solar PV in urban areas.
    """
    return (
        float(potential_generation_res_elec_twh().loc["solar PV"])
        * desired_share_installed_pv_urban_vs_tot_pv()
    )


@component.add(
    name="power density CSP",
    units="TWe/MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_density_initial_res_elec_twemha": 1},
)
def power_density_csp():
    """
    Power density of CSP power plants.
    """
    return float(power_density_initial_res_elec_twemha().loc["CSP"])


@component.add(
    name="real share PV urban vs total PV",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_elec_gen_from_solar_pv_urban_twh": 1,
        "real_generation_res_elec_twh": 1,
    },
)
def real_share_pv_urban_vs_total_pv():
    """
    Share of PV in urban areas vs total (urban + on land power plants).
    """
    return np.minimum(
        1,
        zidz(
            potential_elec_gen_from_solar_pv_urban_twh(),
            float(real_generation_res_elec_twh().loc["solar PV"]),
        ),
    )


@component.add(
    name="remaining potential RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_potential_res_elec_twh": 3, "real_generation_res_elec_twh": 2},
)
def remaining_potential_res_elec():
    """
    Remaining potential of renewables for electricity by technology.
    """
    return if_then_else(
        max_potential_res_elec_twh() > real_generation_res_elec_twh(),
        lambda: (max_potential_res_elec_twh() - real_generation_res_elec_twh())
        / max_potential_res_elec_twh(),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="remaining potential solar PV urban",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_solar_pv_urban": 2,
        "twe_per_twh": 2,
        "desired_share_installed_pv_urban_vs_tot_pv": 1,
        "potential_generation_res_elec_twh": 1,
    },
)
def remaining_potential_solar_pv_urban():
    """
    Remaining potential of solar PV in urban areas.
    """
    return np.maximum(
        0,
        zidz(
            max_solar_pv_urban() / twe_per_twh()
            - desired_share_installed_pv_urban_vs_tot_pv()
            * float(potential_generation_res_elec_twh().loc["solar PV"]),
            max_solar_pv_urban() / twe_per_twh(),
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


@component.add(
    name="share solar PV vs tot solar gen",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_gen_from_solar_pv_on_land_twh": 2,
        "real_generation_res_elec_twh": 1,
    },
)
def share_solar_pv_vs_tot_solar_gen():
    """
    Share of solar PV vs CSP generation.
    """
    return zidz(
        fe_elec_gen_from_solar_pv_on_land_twh(),
        float(real_generation_res_elec_twh().loc["CSP"])
        + fe_elec_gen_from_solar_pv_on_land_twh(),
    )
