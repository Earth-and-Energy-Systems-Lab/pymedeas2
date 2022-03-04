"""
Module res_elec_potentials
Translated using PySD version 2.2.1
"""


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
    return (
        available_potential_fe_solid_bioe_for_elec_ej() * twe_per_twh() / ej_per_twh()
    )


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
    return max_solar_on_land_mha() - surface_solar_pv_mha()


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
    return max_csp_on_land_mha() * float(power_density_res_elec_twemha().loc["CSP"])


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
    "World",
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
    "World",
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
    "World",
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
    "World",
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
    "World",
    "max_PE_geot_elect_potential",
    {},
    _root,
    "_ext_constant_max_pe_geotelec_twth",
)


@subs(["RES elec"], _subscript_dict)
def max_potential_res_elec_twe():
    """
    Real Name: max potential RES elec TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Maximum potential of RES for electricity per technology considering an optimal Cp.
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
    value.loc[{"RES elec": ["solar PV"]}] = max_solar_pv_on_land_twe()
    value.loc[{"RES elec": ["CSP"]}] = max_csp_twe()
    return value


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
    return max_potential_res_elec_twe() / twe_per_twh()


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
        + max_biogas_ej() * share_pes_biogas_for_elec() / ej_per_twh()
    )


def max_solar_on_land_mha():
    """
    Real Name: max solar on land Mha
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Assumed land availability for solar power plants on land (PV and CSP).
    """
    return _ext_constant_max_solar_on_land_mha()


_ext_constant_max_solar_on_land_mha = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_solar_on_land_potential",
    {},
    _root,
    "_ext_constant_max_solar_on_land_mha",
)


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
    return max_solar_pv_on_land_mha() * float(
        power_density_res_elec_twemha().loc["solar PV"]
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


def remaining_potential_bioe():
    """
    Real Name: remaining potential BioE
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["solid bioE elec"])
        > float(real_generation_res_elec_twh().loc["solid bioE elec"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["solid bioE elec"])
            - float(real_generation_res_elec_twh().loc["solid bioE elec"])
        )
        / float(max_potential_res_elec_twh().loc["solid bioE elec"]),
        lambda: 0,
    )


def remaining_potential_csp():
    """
    Real Name: remaining potential CSP
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["CSP"])
        > float(real_generation_res_elec_twh().loc["CSP"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["CSP"])
            - float(real_generation_res_elec_twh().loc["CSP"])
        )
        / float(max_potential_res_elec_twh().loc["CSP"]),
        lambda: 0,
    )


def remaining_potential_geotelec():
    """
    Real Name: "remaining potential geot-elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["geot elec"])
        > float(real_generation_res_elec_twh().loc["geot elec"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["geot elec"])
            - float(real_generation_res_elec_twh().loc["geot elec"])
        )
        / float(max_potential_res_elec_twh().loc["geot elec"]),
        lambda: 0,
    )


def remaining_potential_hydro():
    """
    Real Name: remaining potential hydro
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["hydro"])
        > float(real_generation_res_elec_twh().loc["hydro"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["hydro"])
            - float(real_generation_res_elec_twh().loc["hydro"])
        )
        / float(max_potential_res_elec_twh().loc["hydro"]),
        lambda: 0,
    )


def remaining_potential_oceanic():
    """
    Real Name: remaining potential oceanic
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["oceanic"])
        > float(real_generation_res_elec_twh().loc["oceanic"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["oceanic"])
            - float(real_generation_res_elec_twh().loc["oceanic"])
        )
        / float(max_potential_res_elec_twh().loc["oceanic"]),
        lambda: 0,
    )


def remaining_potential_offshore_wind():
    """
    Real Name: remaining potential offshore wind
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["wind offshore"])
        > float(real_generation_res_elec_twh().loc["wind offshore"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["wind offshore"])
            - float(real_generation_res_elec_twh().loc["wind offshore"])
        )
        / float(max_potential_res_elec_twh().loc["wind offshore"]),
        lambda: 0,
    )


def remaining_potential_onshore_wind():
    """
    Real Name: remaining potential onshore wind
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["wind onshore"])
        > float(real_generation_res_elec_twh().loc["wind onshore"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["wind onshore"])
            - float(real_generation_res_elec_twh().loc["wind onshore"])
        )
        / float(max_potential_res_elec_twh().loc["wind onshore"]),
        lambda: 0,
    )


def remaining_potential_solarelec_pv():
    """
    Real Name: "remaining potential solar-elec PV"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        float(max_potential_res_elec_twh().loc["solar PV"])
        > float(real_generation_res_elec_twh().loc["solar PV"]),
        lambda: (
            float(max_potential_res_elec_twh().loc["solar PV"])
            - float(real_generation_res_elec_twh().loc["solar PV"])
        )
        / float(max_potential_res_elec_twh().loc["solar PV"]),
        lambda: 0,
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
