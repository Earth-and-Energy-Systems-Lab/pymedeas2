"""
Module energy.supply.res_elec_potentials
Translated using PySD version 3.14.2
"""

@component.add(
    name="available_max_FE_solid_bioE_for_elec_EJ",
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
    name="desired_share_installed_PV_urban_vs_tot_PV",
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
    name="Efficiency_conversion_geot_PE_to_Elec",
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
    name="FE_Elec_gen_from_solar_PV_on_land_TWh",
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
    return float(real_generation_res_elec_twh().loc["solar_PV"]) * (
        1 - real_share_pv_urban_vs_total_pv()
    )


@component.add(
    name="historic_share_installed_PV_urban_vs_tot_PV",
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
    name="max_BioE_TWe",
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
    name="max_CSP_on_land_MHa",
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
    name="max_FE_potential_solid_bioE_for_elec_TWe",
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
    name='"max_PE_geot-elec_TWth"',
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
    name="max_PE_potential_biogas_for_elec",
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
    name="max_potential_RES_elec_TWh",
    units="TWh/year",
    subscripts=["RES_elec"],
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
    name="max_potential_tot_RES_elec_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_res_elec_twh": 1,
        "twe_per_twh": 1,
        "max_potential_phs_twe": 1,
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
            max_potential_res_elec_twh().rename({"RES_elec": "RES_elec!"}),
            dim=["RES_elec!"],
        )
        + max_potential_phs_twe() / twe_per_twh()
        + max_pe_potential_biogas_for_elec() / ej_per_twh()
    )


@component.add(
    name="max_RES_elec_TWe",
    units="TWe",
    subscripts=["RES_elec"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal, External",
    depends_on={
        "__external__": "_ext_constant_max_res_elec_twe",
        "max_pe_geotelec_twth": 1,
        "efficiency_conversion_geot_pe_to_elec": 1,
        "max_bioe_twe": 1,
        "max_solar_pv_on_land_twe": 1,
        "max_solar_pv_urban": 1,
        "power_density_csp": 1,
        "max_csp_on_land_mha": 1,
    },
)
def max_res_elec_twe():
    """
    Maximum level of RES for electricity per technology considering an optimal Cp. For most technologies this variable corresponds with the maximum potential, excepting for solids bioenergy and solar, where given to the competing uses (solids bioenergy for heat and electricity) and competing technologies (solar PV and CSP) this variable corresponds to the maximum level from each use and technology.
    """
    value = xr.DataArray(
        np.nan, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
    )
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["hydro"]] = True
    def_subs.loc[["oceanic"]] = True
    def_subs.loc[["wind_onshore"]] = True
    def_subs.loc[["wind_offshore"]] = True
    value.values[def_subs.values] = _ext_constant_max_res_elec_twe().values[
        def_subs.values
    ]
    value.loc[["geot_elec"]] = (
        max_pe_geotelec_twth() * efficiency_conversion_geot_pe_to_elec()
    )
    value.loc[["solid_bioE_elec"]] = max_bioe_twe()
    value.loc[["solar_PV"]] = max_solar_pv_on_land_twe() + max_solar_pv_urban()
    value.loc[["CSP"]] = max_csp_on_land_mha() * power_density_csp()
    return value


_ext_constant_max_res_elec_twe = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "max_hydro_potential",
    {"RES_elec": ["hydro"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_max_res_elec_twe",
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx", "Europe", "max_oceanic_potential", {"RES_elec": ["oceanic"]}
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx",
    "Europe",
    "max_onshore_wind_potential",
    {"RES_elec": ["wind_onshore"]},
)

_ext_constant_max_res_elec_twe.add(
    r"../energy.xlsx",
    "Europe",
    "max_offshore_wind_potential",
    {"RES_elec": ["wind_offshore"]},
)


@component.add(
    name="max_solar_on_land_Mha",
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
    name="max_solar_PV_on_land_MHa",
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
    name="max_solar_PV_on_land_TWe",
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
    name="P_share_installed_PV_urban_vs_tot_PV",
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
    name="Percent_remaining_potential_tot_RES_elec",
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
    name="Potential_elec_gen_from_solar_PV_on_land_TWh",
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
        float(potential_generation_res_elec_twh().loc["solar_PV"])
        - potential_elec_gen_from_solar_pv_urban_twh()
    )


@component.add(
    name="Potential_elec_gen_from_solar_PV_urban_TWh",
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
    name="Potential_elec_gen_from_solar_PV_urban_unconstrained_TWh",
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
        float(potential_generation_res_elec_twh().loc["solar_PV"])
        * desired_share_installed_pv_urban_vs_tot_pv()
    )


@component.add(
    name="power_density_CSP",
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
    name="real_share_PV_urban_vs_total_PV",
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
    return float(
        np.minimum(
            1,
            zidz(
                potential_elec_gen_from_solar_pv_urban_twh(),
                float(real_generation_res_elec_twh().loc["solar_PV"]),
            ),
        )
    )


@component.add(
    name="remaining_potential_RES_elec",
    units="Dmnl",
    subscripts=["RES_elec"],
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
            0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
    )


@component.add(
    name="remaining_potential_solar_PV_urban",
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
    return float(
        np.maximum(
            0,
            zidz(
                max_solar_pv_urban() / twe_per_twh()
                - desired_share_installed_pv_urban_vs_tot_pv()
                * float(potential_generation_res_elec_twh().loc["solar_PV"]),
                max_solar_pv_urban() / twe_per_twh(),
            ),
        )
    )


@component.add(
    name="remaining_potential_tot_RES_elec",
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
    name="share_solar_PV_vs_tot_solar_gen",
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
