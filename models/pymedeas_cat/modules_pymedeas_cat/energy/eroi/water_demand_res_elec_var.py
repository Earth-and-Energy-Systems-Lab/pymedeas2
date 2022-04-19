"""
Module water_demand_res_elec_var
Translated using PySD version 3.0.0
"""


@component.add(
    name='"CED O&M over lifetime per water RES elec var"',
    units="EJ",
    subscripts=["RES elec", "water0"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_om_over_lifetime_per_water_res_elec_var():
    """
    Cumulative energy demand per water type for O&M of RES variables per technology over all the lifetime of the infrastructure.
    """
    return (
        (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "water0": _subscript_dict["water0"],
                },
                ["RES elec", "water0"],
            )
            + res_elec_capacity_under_construction_tw()
        )
        * water_for_om_res_elec()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "water0": _subscript_dict["water0"],
                },
                ["RES elec", "water0"],
            )
            + energy_requirements_per_unit_of_water_consumption()
        )
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "water0": _subscript_dict["water0"],
                },
                ["RES elec", "water0"],
            )
            + lifetime_res_elec()
        )
        * (m_per_t() / kg_per_mt())
        * (kg_per_mt() / mj_per_ej())
    )


@component.add(
    name='"Energy requirements for O&M for water consumption RES elec"',
    units="EJ",
    subscripts=["RES elec", "water0"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_requirements_for_om_for_water_consumption_res_elec():
    """
    Energy requirements for operation and maintenance of water consumption by RES technology for generating electricity.
    """
    return (
        xr.DataArray(
            0,
            {
                "RES elec": _subscript_dict["RES elec"],
                "water0": _subscript_dict["water0"],
            },
            ["RES elec", "water0"],
        )
        + (
            xr.DataArray(
                0,
                {
                    "water0": _subscript_dict["water0"],
                    "RES elec": _subscript_dict["RES elec"],
                },
                ["water0", "RES elec"],
            )
            + energy_requirements_per_unit_of_water_consumption()
        )
        * (
            xr.DataArray(
                0,
                {
                    "water0": _subscript_dict["water0"],
                    "RES elec": _subscript_dict["RES elec"],
                },
                ["water0", "RES elec"],
            )
            + water_for_om_required_for_res_elec()
        )
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name="Energy requirements per unit of water consumption",
    units="MJ/kg",
    subscripts=["water0"],
    comp_type="Constant",
    comp_subtype="External",
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
    {"water0": ["clean water", "distilled water"]},
    "_ext_constant_energy_requirements_per_unit_of_water_consumption",
)


@component.add(
    name='"Total energy requirements O&M for water consumption RES elec"',
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_requirements_om_for_water_consumption_res_elec():
    """
    Total energy requirements for water consumption (all types) by RES technology for electricity generation.
    """
    return sum(
        energy_requirements_for_om_for_water_consumption_res_elec().rename(
            {"water0": "water0!"}
        ),
        dim=["water0!"],
    )


@component.add(
    name='"Total water for O&M required by RES elec per techn"',
    units="Mt",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_water_for_om_required_by_res_elec_per_techn():
    """
    Annual total water required by RES technology for generating electricity.
    """
    return sum(
        water_for_om_required_for_res_elec().rename({"water0": "water0!"}),
        dim=["water0!"],
    )


@component.add(
    name='"Total water for O&M required by RES elec"',
    units="Mt",
    subscripts=["water"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
)
def total_water_for_om_required_by_res_elec():
    value = xr.DataArray(np.nan, {"water": _subscript_dict["water"]}, ["water"])
    value.loc[{"water": ["blue water"]}] = sum(
        total_water_for_om_required_by_res_elec_per_techn().rename(
            {"RES elec": "RES elec!"}
        ),
        dim=["RES elec!"],
    )
    value.loc[{"water": ["green water"]}] = 0
    value.loc[{"water": ["gray water"]}] = 0
    return value


@component.add(
    name='"water for O&M - RES elec"',
    units="kg/MW",
    subscripts=["RES elec", "water0"],
    comp_type="Constant",
    comp_subtype="External, Normal",
)
def water_for_om_res_elec():
    value = xr.DataArray(
        np.nan,
        {"RES elec": _subscript_dict["RES elec"], "water0": _subscript_dict["water0"]},
        ["RES elec", "water0"],
    )
    value.loc[
        {
            "RES elec": ["hydro", "geot elec", "solid bioE elec", "oceanic"],
            "water0": ["clean water", "distilled water"],
        }
    ] = 0
    value.loc[
        {
            "RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"],
            "water0": ["clean water", "distilled water"],
        }
    ] = _ext_constant_water_for_om_res_elec().values
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
    {
        "RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"],
        "water0": ["clean water", "distilled water"],
    },
    "_ext_constant_water_for_om_res_elec",
)


@component.add(
    name='"Water for O&M required for RES elec"',
    units="Mt",
    subscripts=["RES elec", "water0"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def water_for_om_required_for_res_elec():
    """
    Annual water required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return (
        (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "water0": _subscript_dict["water0"],
                },
                ["RES elec", "water0"],
            )
            + installed_capacity_res_elec_tw()
        )
        * water_for_om_res_elec()
        * m_per_t()
        / kg_per_mt()
    )
