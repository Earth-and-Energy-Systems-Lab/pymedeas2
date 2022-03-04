"""
Module res_elec_potentials
Translated using PySD version 2.2.1
"""


def available_max_fe_solid_bioe_for_elec_ej():
    """
    Real Name: available max FE solid bioE for elec EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum available (final energy) solid bioenergy for electricity.
    """
    return (
        available_max_pe_solid_bioe_for_elec_ej() * efficiency_conversion_bioe_to_elec()
    )


def desired_share_installed_pv_urban_vs_tot_pv():
    """
    Real Name: desired share installed PV urban vs tot PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Desired share of installed PV in urban areas vs total PV installed.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_share_installed_pv_urban_vs_tot_pv(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: historic_share_installed_pv_urban_vs_tot_pv(),
            lambda: if_then_else(
                time() < target_year_p_growth_res_elec(),
                lambda: historic_share_installed_pv_urban_vs_tot_pv()
                + (
                    p_share_installed_pv_urban_vs_tot_pv()
                    - historic_share_installed_pv_urban_vs_tot_pv()
                )
                * (time() - start_year_p_growth_res_elec())
                / (target_year_p_growth_res_elec() - start_year_p_growth_res_elec()),
                lambda: p_share_installed_pv_urban_vs_tot_pv(),
            ),
        ),
    )


def efficiency_conversion_geot_pe_to_elec():
    """
    Real Name: Efficiency conversion geot PE to Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation from geothermal (primary energy) to electricity.
    """
    return _ext_constant_efficiency_conversion_geot_pe_to_elec()


_ext_constant_efficiency_conversion_geot_pe_to_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_geot_pe_to_elec",
    {},
    _root,
    "_ext_constant_efficiency_conversion_geot_pe_to_elec",
)


def fe_elec_gen_from_solar_pv_on_land_twh():
    """
    Real Name: FE Elec gen from solar PV on land TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation from solar PV on land.
    """
    return float(real_generation_res_elec_twh().loc["solar PV"]) * (
        1 - real_share_pv_urban_vs_total_pv()
    )


def historic_share_installed_pv_urban_vs_tot_pv():
    """
    Real Name: historic share installed PV urban vs tot PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _ext_data_historic_share_installed_pv_urban_vs_tot_pv(time())


_ext_data_historic_share_installed_pv_urban_vs_tot_pv = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_urban_pv_over_total",
    None,
    {},
    _root,
    "_ext_data_historic_share_installed_pv_urban_vs_tot_pv",
)


def max_bioe_twe():
    """
    Real Name: max BioE TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Techno-ecological potential of biomass&waste. This potential is dynamic and dependant on the potential assigned for bioenergy residues.
    """
    return available_max_fe_solid_bioe_for_elec_ej() * twe_per_twh() / ej_per_twh()


def max_csp_on_land_mha():
    """
    Real Name: max CSP on land MHa
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available land for solar CSP taking into account the total land availability for solar and the actual occupation from solar PV on land.
    """
    return max_solar_on_land_mha() - surface_solar_pv_on_land_mha()


def max_csp_twe():
    """
    Real Name: max CSP TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Techno-ecological potential of solar CSP. This potential depends on the assumed land availability for solar CSP power plants ("max solar PV on land MHa") and its power density (1 TWe = 8760 TWh in one year).
    """
    return max_csp_on_land_mha() * power_density_csp()


def max_fe_potential_solid_bioe_for_elec_twe():
    """
    Real Name: max FE potential solid bioE for elec TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available potential (final energy) solid bioenergy for electricity.
    """
    return (
        max_pe_potential_solid_bioe_for_elec_ej()
        * efficiency_conversion_bioe_to_elec()
        * twe_per_twh()
        / ej_per_twh()
    )


def max_geotelec_twe():
    """
    Real Name: "max geot-elec TWe"
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Techno-ecological potential of electric geothermal (1 TWe = 8760 TWh in one year). We assume that the global potential of 0.2 TWe.
    """
    return max_pe_geotelec_twth() * efficiency_conversion_geot_pe_to_elec()


def max_hydro_twe():
    """
    Real Name: max hydro TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Techno-ecological potential of hydro (1 TWe = 8760 TWh in one year).
    """
    return _ext_constant_max_hydro_twe()


_ext_constant_max_hydro_twe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_hydro_potential",
    {},
    _root,
    "_ext_constant_max_hydro_twe",
)


def max_oceanic_twe():
    """
    Real Name: max oceanic TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Techno-ecological potential of oceanic (1 TWe = 8760 TWh in one year).
    """
    return _ext_constant_max_oceanic_twe()


_ext_constant_max_oceanic_twe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_oceanic_potential",
    {},
    _root,
    "_ext_constant_max_oceanic_twe",
)


def max_offshore_wind_twe():
    """
    Real Name: max offshore wind TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Techno-ecological potential of offshore wind (1 TWe = 8760 TWh in one year).
    """
    return _ext_constant_max_offshore_wind_twe()


_ext_constant_max_offshore_wind_twe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_offshore_wind_potential",
    {},
    _root,
    "_ext_constant_max_offshore_wind_twe",
)


def max_onshore_wind_twe():
    """
    Real Name: max onshore wind TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Techno-ecological potential of onshore wind (1 TWe = 8760 TWh in one year).
    """
    return _ext_constant_max_onshore_wind_twe()


_ext_constant_max_onshore_wind_twe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_onshore_wind_potential",
    {},
    _root,
    "_ext_constant_max_onshore_wind_twe",
)


def max_pe_geotelec_twth():
    """
    Real Name: "max PE geot-elec TWth"
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Primary energy of geothermal for electricity.
    """
    return _ext_constant_max_pe_geotelec_twth()


_ext_constant_max_pe_geotelec_twth = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_PE_geot_elec_potential",
    {},
    _root,
    "_ext_constant_max_pe_geotelec_twth",
)


def max_pe_potential_biogas_for_elec():
    """
    Real Name: max PE potential biogas for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum potential (primary energy) of biogas for electricity.
    """
    return max_pe_biogas_ej() * share_pes_biogas_for_elec()


def max_potential_csp_twe():
    """
    Real Name: max potential CSP TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum potential of CSP PV for producing electricity on land. To distribute the area potential with the CSP, we assume the potential share proportional to the generation share in each time period.
    """
    return (
        max_solar_on_land_mha()
        * power_density_csp()
        * (1 - share_solar_pv_vs_tot_solar_gen())
    )


@subs(["RES elec"], _subscript_dict)
def max_potential_res_elec_twh():
    """
    Real Name: max potential RES elec TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = (
        float(max_res_elec_twe().loc["hydro"]) / twe_per_twh()
    )
    value.loc[{"RES elec": ["geot elec"]}] = (
        float(max_res_elec_twe().loc["geot elec"]) / twe_per_twh()
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = (
        max_fe_potential_solid_bioe_for_elec_twe() / twe_per_twh()
    )
    value.loc[{"RES elec": ["oceanic"]}] = (
        float(max_res_elec_twe().loc["oceanic"]) / twe_per_twh()
    )
    value.loc[{"RES elec": ["wind onshore"]}] = (
        float(max_res_elec_twe().loc["wind onshore"]) / twe_per_twh()
    )
    value.loc[{"RES elec": ["wind offshore"]}] = (
        float(max_res_elec_twe().loc["wind offshore"]) / twe_per_twh()
    )
    value.loc[{"RES elec": ["solar PV"]}] = max_potential_solar_pv_twe() / twe_per_twh()
    value.loc[{"RES elec": ["CSP"]}] = max_potential_csp_twe() / twe_per_twh()
    return value


def max_potential_solar_pv_twe():
    """
    Real Name: max potential solar PV TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum potential of solar PV for producing electricity on land. To distribute the area potential with the CSP, we assume the potential share proportional to the generation share in each time period.
    """
    return (
        max_solar_on_land_mha()
        * power_density_solar_pv_on_land_twemha()
        * share_solar_pv_vs_tot_solar_gen()
    )


def max_potential_tot_res_elec_twh():
    """
    Real Name: max potential tot RES elec TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


@subs(["RES elec"], _subscript_dict)
def max_res_elec_twe():
    """
    Real Name: max RES elec TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Maximum level of RES for electricity per technology considering an optimal Cp. For most technologies this variable corresponds with the maximum potential, excepting for solids bioenergy and solar, where given to the competing uses (solids bioenergy for heat and electricity) and competing technologies (solar PV and CSP) this variable corresponds to the maximum level from each use and technology.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = max_hydro_twe()
    value.loc[{"RES elec": ["geot elec"]}] = max_geotelec_twe()
    value.loc[{"RES elec": ["solid bioE elec"]}] = max_bioe_twe()
    value.loc[{"RES elec": ["oceanic"]}] = max_oceanic_twe()
    value.loc[{"RES elec": ["wind onshore"]}] = max_onshore_wind_twe()
    value.loc[{"RES elec": ["wind offshore"]}] = max_offshore_wind_twe()
    value.loc[{"RES elec": ["solar PV"]}] = max_tot_solar_pv_twe()
    value.loc[{"RES elec": ["CSP"]}] = max_csp_twe()
    return value


def max_solar_pv_on_land_mha():
    """
    Real Name: max solar PV on land MHa
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available land for solar PV taking into account the total land availability for solar and the actual occupation from CSP.
    """
    return max_solar_on_land_mha() - surface_csp_mha()


def max_solar_pv_on_land_twe():
    """
    Real Name: max solar PV on land TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Techno-ecological potential of solar PV on land. This potential depends on the assumed land availability for solar PV power plants ("max solar PV on land MHa") and its power density (1 TWe = 8760 TWh in one year).
    """
    return max_solar_pv_on_land_mha() * power_density_solar_pv_on_land_twemha()


def max_tot_solar_pv_twe():
    """
    Real Name: max tot solar PV TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Techno-ecological potential of total solar PV (on land + urban)..
    """
    return max_solar_pv_on_land_twe() + max_solar_pv_urban()


def p_share_installed_pv_urban_vs_tot_pv():
    """
    Real Name: P share installed PV urban vs tot PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    User defined share of installed PV in urban areas vs total PV.
    """
    return _ext_constant_p_share_installed_pv_urban_vs_tot_pv()


_ext_constant_p_share_installed_pv_urban_vs_tot_pv = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "share_PV_urban_tot_PV",
    {},
    _root,
    "_ext_constant_p_share_installed_pv_urban_vs_tot_pv",
)


def percent_remaining_potential_tot_res_elec():
    """
    Real Name: Percent remaining potential tot RES elec
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_elec() * 100


def potential_elec_gen_from_solar_pv_on_land_twh():
    """
    Real Name: Potential elec gen from solar PV on land TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential electricity generation from solar PV on land.
    """
    return (
        float(potential_generation_res_elec_twh().loc["solar PV"])
        - potential_elec_gen_from_solar_pv_urban_twh()
    )


def potential_elec_gen_from_solar_pv_urban_twh():
    """
    Real Name: Potential elec gen from solar PV urban TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Potential electricity generation from solar PV in urban areas.
    """
    return _sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh()


_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh = SampleIfTrue(
    lambda: remaining_potential_solar_pv_urban() > 0,
    lambda: potential_elec_gen_from_solar_pv_urban_unconstrained_twh(),
    lambda: potential_elec_gen_from_solar_pv_urban_unconstrained_twh(),
    "_sampleiftrue_potential_elec_gen_from_solar_pv_urban_twh",
)


def potential_elec_gen_from_solar_pv_urban_unconstrained_twh():
    """
    Real Name: Potential elec gen from solar PV urban unconstrained TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Unconstrained potential electricity generation from solar PV in urban areas.
    """
    return (
        float(potential_generation_res_elec_twh().loc["solar PV"])
        * desired_share_installed_pv_urban_vs_tot_pv()
    )


def power_density_csp():
    """
    Real Name: power density CSP
    Original Eqn:
    Units: TWe/MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Power density of CSP power plants.
    """
    return float(power_density_initial_res_elec_twemha().loc["CSP"])


def real_share_pv_urban_vs_total_pv():
    """
    Real Name: real share PV urban vs total PV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of PV in urban areas vs total (urban + on land power plants).
    """
    return np.minimum(
        1,
        zidz(
            potential_elec_gen_from_solar_pv_urban_twh(),
            float(real_generation_res_elec_twh().loc["solar PV"]),
        ),
    )


@subs(["RES elec"], _subscript_dict)
def remaining_potential_res_elec():
    """
    Real Name: remaining potential RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

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


def remaining_potential_solar_pv_urban():
    """
    Real Name: remaining potential solar PV urban
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def remaining_potential_tot_res_elec():
    """
    Real Name: remaining potential tot RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def share_solar_pv_vs_tot_solar_gen():
    """
    Real Name: share solar PV vs tot solar gen
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of solar PV vs CSP generation.
    """
    return zidz(
        fe_elec_gen_from_solar_pv_on_land_twh(),
        float(real_generation_res_elec_twh().loc["CSP"])
        + fe_elec_gen_from_solar_pv_on_land_twh(),
    )
