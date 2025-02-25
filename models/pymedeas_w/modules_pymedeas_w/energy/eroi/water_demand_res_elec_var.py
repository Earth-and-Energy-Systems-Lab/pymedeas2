"""
Module energy.eroi.water_demand_res_elec_var
Translated using PySD version 3.14.0
"""

@component.add(
    name='"CED O&M over lifetime per water RES elec var"',
    units="EJ/year",
    subscripts=[np.str_("RES elec"), np.str_("water0")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_capacity_under_construction_tw": 1,
        "water_for_om_res_elec": 1,
        "energy_requirements_per_unit_of_water_consumption": 1,
        "lifetime_res_elec": 1,
        "kg_per_mt": 2,
        "mw_per_tw": 1,
        "mj_per_ej": 1,
        "nvs_1_year": 1,
    },
)
def ced_om_over_lifetime_per_water_res_elec_var():
    """
    Cumulative energy demand per water type for O&M of RES variables per technology over all the lifetime of the infrastructure.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * water_for_om_res_elec()
        * energy_requirements_per_unit_of_water_consumption()
        * lifetime_res_elec()
        * (mw_per_tw() / kg_per_mt())
        * (kg_per_mt() / mj_per_ej())
        / nvs_1_year()
    )


@component.add(
    name='"Energy requirements for O&M for water consumption RES elec"',
    units="EJ/year",
    subscripts=[np.str_("RES elec"), np.str_("water0")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_requirements_per_unit_of_water_consumption": 1,
        "water_for_om_required_for_res_elec": 1,
        "kg_per_mt": 1,
        "mj_per_ej": 1,
        "nvs_1_year": 1,
    },
)
def energy_requirements_for_om_for_water_consumption_res_elec():
    """
    Energy requirements for operation and maintenance of water consumption by RES technology for generating electricity.
    """
    return (
        energy_requirements_per_unit_of_water_consumption()
        * water_for_om_required_for_res_elec().transpose("water0", "RES elec")
        * kg_per_mt()
        / mj_per_ej()
        / nvs_1_year()
    ).transpose("RES elec", "water0")


@component.add(
    name="Energy requirements per unit of water consumption",
    units="MJ/kg",
    subscripts=[np.str_("water0")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_energy_requirements_per_unit_of_water_consumption"
    },
)
def energy_requirements_per_unit_of_water_consumption():
    """
    Energy requirements for water consumption in RES plants for generation of electricity.
    """
    return _ext_constant_energy_requirements_per_unit_of_water_consumption()


_ext_constant_energy_requirements_per_unit_of_water_consumption = ExtConstant(
    "../materials.xlsx",
    "Global",
    "energy_requirements_per_unit_of_water_consumption*",
    {"water0": _subscript_dict["water0"]},
    _root,
    {"water0": _subscript_dict["water0"]},
    "_ext_constant_energy_requirements_per_unit_of_water_consumption",
)


@component.add(
    name='"Total energy requirements O&M for water consumption RES elec"',
    units="EJ/year",
    subscripts=[np.str_("RES elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_requirements_for_om_for_water_consumption_res_elec": 1},
)
def total_energy_requirements_om_for_water_consumption_res_elec():
    """
    Total energy requirements for water consumption (all types) by RES technology for electricity generation.
    """
    return sum(
        energy_requirements_for_om_for_water_consumption_res_elec().rename(
            {np.str_("water0"): "water0!"}
        ),
        dim=["water0!"],
    )


@component.add(
    name='"Total water for O&M required by RES elec"',
    units="Mt",
    subscripts=[np.str_("water")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_for_om_required_by_res_elec_per_techn": 1},
)
def total_water_for_om_required_by_res_elec():
    value = xr.DataArray(
        np.nan, {"water": _subscript_dict["water"]}, [np.str_("water")]
    )
    value.loc[["blue water"]] = sum(
        total_water_for_om_required_by_res_elec_per_techn().rename(
            {np.str_("RES elec"): "RES elec!"}
        ),
        dim=["RES elec!"],
    )
    value.loc[["green water"]] = 0
    value.loc[["gray water"]] = 0
    return value


@component.add(
    name='"Total water for O&M required by RES elec per techn"',
    units="Mt",
    subscripts=[np.str_("RES elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"water_for_om_required_for_res_elec": 1},
)
def total_water_for_om_required_by_res_elec_per_techn():
    """
    Annual total water required by RES technology for generating electricity.
    """
    return sum(
        water_for_om_required_for_res_elec().rename({np.str_("water0"): "water0!"}),
        dim=["water0!"],
    )


@component.add(
    name='"Water for O&M required for RES elec"',
    units="Mt",
    subscripts=[np.str_("RES elec"), np.str_("water0")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec": 1,
        "water_for_om_res_elec": 1,
        "mw_per_tw": 1,
        "kg_per_mt": 1,
    },
)
def water_for_om_required_for_res_elec():
    """
    Annual water required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return (
        installed_capacity_res_elec()
        * water_for_om_res_elec()
        * mw_per_tw()
        / kg_per_mt()
    )


@component.add(
    name='"water for O&M - RES elec"',
    units="kg/MW",
    subscripts=["RES elec", np.str_("water0")],
    comp_type="Constant",
    comp_subtype="Normal, External",
    depends_on={"__external__": "_ext_constant_water_for_om_res_elec"},
)
def water_for_om_res_elec():
    value = xr.DataArray(
        np.nan,
        {"RES elec": _subscript_dict["RES elec"], "water0": _subscript_dict["water0"]},
        ["RES elec", np.str_("water0")],
    )
    value.loc[_subscript_dict["RES ELEC DISPATCHABLE"], :] = 0
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["wind onshore", "wind offshore", "solar PV", "CSP"], :] = True
    value.values[def_subs.values] = _ext_constant_water_for_om_res_elec().values[
        def_subs.values
    ]
    return value


_ext_constant_water_for_om_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "water_for_om_res_elec*",
    {
        "RES elec": _subscript_dict["RES ELEC VARIABLE"],
        "water0": _subscript_dict["water0"],
    },
    _root,
    {"RES elec": _subscript_dict["RES elec"], "water0": _subscript_dict["water0"]},
    "_ext_constant_water_for_om_res_elec",
)
