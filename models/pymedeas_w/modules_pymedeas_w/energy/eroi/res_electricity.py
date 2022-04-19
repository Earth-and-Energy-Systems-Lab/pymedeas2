"""
Module res_electricity
Translated using PySD version 3.0.0
"""


@component.add(
    name="\"'dynamic' EROI RES elec var\"",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def dynamic_eroi_res_elec_var():
    """
    Evolution of EROI over time per RES variable technology, considering CED dynamic over time.
    """
    return if_then_else(
        fei_res_elec_var() == 0,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: real_generation_res_elec_ej() / fei_res_elec_var(),
    )


@component.add(
    name="\"'static' EROI RES elec\"",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def static_eroi_res_elec():
    """
    Energy return on energy invested (over the full lifetime of the infrastructure) per RES technology for generating electricity. TODO
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_dispatch().loc["hydro"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["hydro"])
        / (
            float(fei_over_lifetime_res_elec_dispatch().loc["hydro"])
            * quality_of_electricity()
        ),
    )
    value.loc[{"RES elec": ["geot elec"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_dispatch().loc["geot elec"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["geot elec"])
        / (
            float(fei_over_lifetime_res_elec_dispatch().loc["geot elec"])
            * quality_of_electricity()
        ),
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["solid bioE elec"])
        / (
            float(fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"])
            * quality_of_electricity()
        ),
    )
    value.loc[{"RES elec": ["oceanic"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_dispatch().loc["oceanic"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["oceanic"])
        / (
            float(fei_over_lifetime_res_elec_dispatch().loc["oceanic"])
            * quality_of_electricity()
        ),
    )
    value.loc[{"RES elec": ["wind onshore"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_var().loc["wind onshore"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["wind onshore"])
        / float(fei_over_lifetime_res_elec_var().loc["wind onshore"]),
    )
    value.loc[{"RES elec": ["wind offshore"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_var().loc["wind offshore"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["wind offshore"])
        / float(fei_over_lifetime_res_elec_var().loc["wind offshore"]),
    )
    value.loc[{"RES elec": ["solar PV"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_var().loc["solar PV"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["solar PV"])
        / float(fei_over_lifetime_res_elec_var().loc["solar PV"]),
    )
    value.loc[{"RES elec": ["CSP"]}] = if_then_else(
        float(fei_over_lifetime_res_elec_var().loc["CSP"]) == 0,
        lambda: 0,
        lambda: float(output_elec_over_lifetime_res_elec().loc["CSP"])
        / float(fei_over_lifetime_res_elec_var().loc["CSP"]),
    )
    return value


@component.add(
    name="\"'static' EROItot RES elec\"",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def static_eroitot_res_elec():
    """
    EROI over the lifetime of the aggregated outputs and inputs of RES for generating electricity.
    """
    return if_then_else(
        sum(
            fei_over_lifetime_res_elec().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        < 0,
        lambda: 0,
        lambda: sum(
            output_elec_over_lifetime_res_elec().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        / sum(
            fei_over_lifetime_res_elec().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        ),
    )


@component.add(
    name="CED decom RES elec capacity",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_decom_res_elec_capacity():
    """
    Cumulative energy demand (CED) required to decommission RES electricity generation plants which have ended their lifetime.
    """
    return zidz(
        share_energy_requirements_for_decom_res_elec()
        * cedtot_new_cap_res_elec_var()
        * wear_res_elec(),
        res_elec_capacity_under_construction_tw(),
    )


@component.add(
    name="CED new cap per material RES elec var",
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_new_cap_per_material_res_elec_var():
    """
    Cumulative energy demand per material of new installed capacity of RES variables per technology.
    """
    return (
        materials_required_for_new_res_elec_mt()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + energy_cons_per_unit_of_material_cons_for_res_elec()
        )
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name='"CED O&M over lifetime per material RES elec var"',
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_om_over_lifetime_per_material_res_elec_var():
    """
    Cumulative energy demand per material for O&M of RES variables per technology over all the lifetime of the infrastructure.
    """
    return (
        (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + res_elec_capacity_under_construction_tw()
        )
        * materials_for_om_per_capacity_installed_res_elec()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + energy_cons_per_unit_of_material_cons_for_res_elec()
        )
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + lifetime_res_elec()
        )
        * (m_per_t() / kg_per_mt())
        * (kg_per_mt() / mj_per_ej())
    )


@component.add(
    name='"CED O&M over lifetime RES elec var"',
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_om_over_lifetime_res_elec_var():
    """
    Cumulative energy demand for O&M of RES variables per technology over all the lifetime of the infrastructure.
    """
    return sum(
        ced_om_over_lifetime_per_material_res_elec_var().rename(
            {"materials": "materials!"}
        ),
        dim=["materials!"],
    ) + sum(
        ced_om_over_lifetime_per_water_res_elec_var().rename({"water0": "water0!"}),
        dim=["water0!"],
    )


@component.add(
    name='"CED O&M per material RES elec var"',
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_om_per_material_res_elec_var():
    """
    Cumulative energy demand per material of new installed capacity of RES variables per technology.
    """
    return (
        materials_required_for_om_res_elec_mt()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + energy_cons_per_unit_of_material_cons_for_res_elec()
        )
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name="CEDtot new cap RES elec var",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_new_cap_res_elec_var():
    """
    Cumulative energy demand of new capacity for RES variables per technology.
    """
    return sum(
        ced_new_cap_per_material_res_elec_var().rename({"materials": "materials!"}),
        dim=["materials!"],
    )


@component.add(
    name='"CEDtot O&M RES elec var"',
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_om_res_elec_var():
    """
    Cumulative energy demand of O&M for RES variables per technology.
    """
    return (
        sum(
            ced_om_per_material_res_elec_var().rename({"materials": "materials!"}),
            dim=["materials!"],
        )
        + total_energy_requirements_om_for_water_consumption_res_elec()
    )


@component.add(
    name="CEDtot per material RES elec var",
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_per_material_res_elec_var():
    """
    Total cumulative energy demand (construction+O&M) per material of RES variables per technology.
    """
    return (
        ced_new_cap_per_material_res_elec_var()
        + ced_om_over_lifetime_per_material_res_elec_var()
    )


@component.add(
    name="CEDtot per TW over lifetime RES elec dispatch",
    units="EJ/TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_per_tw_over_lifetime_res_elec_dispatch():
    """
    Total cumulative energy demand (including installation of new capacity and O&M) per MW for RES dispatchables per technology over the lifetime of the infrastructure.
    """
    return zidz(
        (1 - res_elec_variables())
        * (cpini_res_elec() * lifetime_res_elec() * ej_per_twh() / twe_per_twh()),
        eroiini_res_elec_dispatch() * quality_of_electricity_2015(),
    )


@component.add(
    name="CEDtot per TW per material RES elec var",
    units="EJ/TW",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_per_tw_per_material_res_elec_var():
    """
    Total cumulative energy demand (construction+O&M) per power installed per material of RES variables per technology (considering only material requirements).
    """
    return zidz(
        cedtot_per_material_res_elec_var(),
        (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + res_elec_capacity_under_construction_tw()
        ),
    )


@component.add(
    name="CEDtot per TW RES elec var",
    units="MJ/MW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_per_tw_res_elec_var():
    """
    Total cumulative energy demand (construction+O&M) per power installed of RES variables per technology (considering only material requirements).
    """
    return (
        sum(
            cedtot_per_tw_per_material_res_elec_var().rename(
                {"materials": "materials!"}
            ),
            dim=["materials!"],
        )
        * 1000000.0
    )


@component.add(
    name='"EROI-ini RES elec dispatch"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def eroiini_res_elec_dispatch():
    """
    Energy return on energy invested of RES technologies for generating electricity dispatchables at the initial Cp level.
    """
    return _ext_constant_eroiini_res_elec_dispatch()


_ext_constant_eroiini_res_elec_dispatch = ExtConstant(
    "../energy.xlsx",
    "Global",
    "eroi_initial_res_elec_dispatch*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {
        "RES elec": [
            "hydro",
            "geot elec",
            "solid bioE elec",
            "oceanic",
            "wind onshore",
            "wind offshore",
            "solar PV",
            "CSP",
        ]
    },
    "_ext_constant_eroiini_res_elec_dispatch",
)


@component.add(
    name="FEI over lifetime RES elec",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fei_over_lifetime_res_elec():
    """
    Final energy investments over lifetime for RES elec technologies.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = float(
        fei_over_lifetime_res_elec_dispatch().loc["hydro"]
    )
    value.loc[{"RES elec": ["geot elec"]}] = float(
        fei_over_lifetime_res_elec_dispatch().loc["geot elec"]
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = float(
        fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"]
    )
    value.loc[{"RES elec": ["oceanic"]}] = float(
        fei_over_lifetime_res_elec_dispatch().loc["oceanic"]
    )
    value.loc[{"RES elec": ["wind onshore"]}] = float(
        fei_over_lifetime_res_elec_var().loc["wind onshore"]
    )
    value.loc[{"RES elec": ["wind offshore"]}] = float(
        fei_over_lifetime_res_elec_var().loc["wind offshore"]
    )
    value.loc[{"RES elec": ["solar PV"]}] = float(
        fei_over_lifetime_res_elec_var().loc["solar PV"]
    )
    value.loc[{"RES elec": ["CSP"]}] = float(
        fei_over_lifetime_res_elec_var().loc["CSP"]
    )
    return value


@component.add(
    name="FEI over lifetime RES elec dispatch",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fei_over_lifetime_res_elec_dispatch():
    """
    Final energy invested over lifetime per RES elec dispatchable technology (equivalent to the denominator of the EROI (=CED*g).
    """
    return (
        cedtot_per_tw_over_lifetime_res_elec_dispatch()
        * res_elec_capacity_under_construction_tw()
    )


@component.add(
    name="FEI over lifetime RES elec var",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fei_over_lifetime_res_elec_var():
    """
    Final energy invested over lifetime per RES elec variable technology (equivalent to the denominator of the EROI (=CED*g, with total cumulative energy demand (including installation of new capacity and O&M) for RES variables per technology over the lifetime of the infrastructure.
    """
    return (
        cedtot_new_cap_res_elec_var()
        * (
            1
            + share_energy_requirements_for_decom_res_elec()
            + grid_correction_factor_res_elec()
        )
        + ced_om_over_lifetime_res_elec_var()
    ) * quality_of_electricity() + output_elec_over_lifetime_res_elec() * selfelectricity_consumption_res_elec()


@component.add(
    name="FEI RES elec var",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fei_res_elec_var():
    """
    Final energy invested (equivalent to the denominator of the EROI (=CED*g, with total cumulative energy demand including installation of new capacity and O&M) for RES variables per technology).
    """
    return (
        cedtot_new_cap_res_elec_var() * (1 + grid_correction_factor_res_elec())
        + ced_decom_res_elec_capacity()
        + cedtot_om_res_elec_var()
    ) * quality_of_electricity() + real_generation_res_elec_ej() * selfelectricity_consumption_res_elec()


@component.add(
    name="Grid correction factor RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External, Normal",
)
def grid_correction_factor_res_elec():
    """
    Grid correction factor to take into account the electricity losses due to Joule effect in each power plant.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro", "geot elec", "solid bioE elec", "oceanic"]}] = 0
    value.loc[
        {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]}
    ] = _ext_constant_grid_correction_factor_res_elec().values
    return value


_ext_constant_grid_correction_factor_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "grid_correction_factor_res_elec",
    {"RES elec": _subscript_dict["RES ELEC VARIABLE"]},
    _root,
    {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]},
    "_ext_constant_grid_correction_factor_res_elec",
)


@component.add(
    name="output elec over lifetime RES elec",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def output_elec_over_lifetime_res_elec():
    """
    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
    """
    return (
        real_cp_res_elec()
        * res_elec_capacity_under_construction_tw()
        * (1 / twe_per_twh())
        * lifetime_res_elec()
        * ej_per_twh()
    )


@component.add(
    name="real generation RES elec EJ",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_generation_res_elec_ej():
    """
    Electricity generation by RES technology.
    """
    return real_generation_res_elec_twh() * ej_per_twh()


@component.add(
    name='"RES elec variables?"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def res_elec_variables():
    """
    Vector to distinguis between RES elec variables and dispatchables: *If=1, RES elec variables (fully endogenous calculation from the materials requirements). *If=0, RES elec dispatchables (partially endogenous calculation requiring a value of EROI as starting point).
    """
    return xr.DataArray(
        [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
        {"RES elec": _subscript_dict["RES elec"]},
        ["RES elec"],
    )


@component.add(
    name="selfelectricity consumption RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External, Normal",
)
def selfelectricity_consumption_res_elec():
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro", "geot elec", "solid bioE elec", "oceanic"]}] = 0
    value.loc[
        {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]}
    ] = _ext_constant_selfelectricity_consumption_res_elec().values
    return value


_ext_constant_selfelectricity_consumption_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "self_electricity_consumption_res_elec",
    {"RES elec": _subscript_dict["RES ELEC VARIABLE"]},
    _root,
    {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]},
    "_ext_constant_selfelectricity_consumption_res_elec",
)


@component.add(
    name="share energy requirements for decom RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External, Normal",
)
def share_energy_requirements_for_decom_res_elec():
    """
    Share energy requirements for decomissioning power RES plants as a share of the energy requirements for the construction of new capacity.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro", "geot elec", "solid bioE elec", "oceanic"]}] = 0
    value.loc[
        {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]}
    ] = _ext_constant_share_energy_requirements_for_decom_res_elec().values
    return value


_ext_constant_share_energy_requirements_for_decom_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_res_elec",
    {"RES elec": _subscript_dict["RES ELEC VARIABLE"]},
    _root,
    {"RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"]},
    "_ext_constant_share_energy_requirements_for_decom_res_elec",
)
