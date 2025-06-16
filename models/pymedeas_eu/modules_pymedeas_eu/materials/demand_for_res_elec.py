"""
Module materials.demand_for_res_elec
Translated using PySD version 3.14.2
"""

@component.add(
    name="cum_materials_requirements_for_RES_elec",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_requirements_for_res_elec": 1},
    other_deps={
        "_integ_cum_materials_requirements_for_res_elec": {
            "initial": {"initial_cumulated_material_requirements_for_res_elec_1995": 1},
            "step": {"total_materials_required_for_res_elec_mt": 1},
        }
    },
)
def cum_materials_requirements_for_res_elec():
    """
    Total cumulative materials requirements for the installation and O&M of RES for electricity generation.
    """
    return _integ_cum_materials_requirements_for_res_elec()


_integ_cum_materials_requirements_for_res_elec = Integ(
    lambda: total_materials_required_for_res_elec_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_res_elec_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_requirements_for_res_elec",
)


@component.add(
    name="cum_materials_to_extract_for_RES_elec",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_res_elec": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_res_elec": {
            "initial": {"initial_cumulated_material_requirements_for_res_elec_1995": 1},
            "step": {"total_materials_to_extract_for_res_elec_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_res_elec():
    """
    Cumulative materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec()


_integ_cum_materials_to_extract_for_res_elec = Integ(
    lambda: total_materials_to_extract_for_res_elec_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_res_elec_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_res_elec",
)


@component.add(
    name="cum_materials_to_extract_for_RES_elec_from_2015",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_res_elec_from_2015": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_res_elec_from_2015": {
            "initial": {"initial_cumulated_material_requirements_for_res_elec_1995": 1},
            "step": {"total_materials_to_extract_for_res_elec_from_2015_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_res_elec_from_2015():
    """
    Cumulative materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec_from_2015()


_integ_cum_materials_to_extract_for_res_elec_from_2015 = Integ(
    lambda: total_materials_to_extract_for_res_elec_from_2015_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_res_elec_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_res_elec_from_2015",
)


@component.add(
    name='"include_materials_for_overgrids?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def include_materials_for_overgrids():
    """
    1. Include materials for overgrids in the CED of RES elec var 0: NOT include materials for overgrids in the CED of RES elec var
    """
    return 0


@component.add(
    name="initial_cumulated_material_requirements_for_RES_elec_1995",
    units="Mt",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cumulated_material_requirements_for_res_elec_1995():
    return 0


@component.add(
    name="materials_for_new_RES_elec_per_capacity_installed",
    units="kg/MW",
    subscripts=["RES_elec", "materials"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "materials_per_new_capacity_installed_res": 1,
        "materials_per_new_res_elec_capacity_installed_material_overgrid_high_power": 1,
        "include_materials_for_overgrids": 1,
        "materials_per_new_res_elec_capacity_installed_hvdcs": 1,
    },
)
def materials_for_new_res_elec_per_capacity_installed():
    value = xr.DataArray(
        np.nan,
        {
            "RES_elec": _subscript_dict["RES_elec"],
            "materials": _subscript_dict["materials"],
        },
        ["RES_elec", "materials"],
    )
    value.loc[_subscript_dict["RES_ELEC_DISPATCHABLE"], :] = 0
    value.loc[_subscript_dict["RES_ELEC_VARIABLE"], :] = (
        materials_per_new_capacity_installed_res()
        + (
            (
                materials_per_new_res_elec_capacity_installed_hvdcs()
                + materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
            )
            * include_materials_for_overgrids()
        )
    ).values
    return value


@component.add(
    name='"materials_for_O&M_per_capacity_installed_RES_elec"',
    units="kg/(MW*year)",
    subscripts=["RES_elec", "materials"],
    comp_type="Constant",
    comp_subtype="Normal, External",
    depends_on={
        "__external__": "_ext_constant_materials_for_om_per_capacity_installed_res_elec"
    },
)
def materials_for_om_per_capacity_installed_res_elec():
    """
    Materials requirements for operation and maintenance per unit of new installed capacity of RES elec.
    """
    value = xr.DataArray(
        np.nan,
        {
            "RES_elec": _subscript_dict["RES_elec"],
            "materials": _subscript_dict["materials"],
        },
        ["RES_elec", "materials"],
    )
    value.loc[_subscript_dict["RES_ELEC_DISPATCHABLE"], :] = 0
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["wind_onshore", "wind_offshore", "solar_PV", "CSP"], :] = True
    value.values[
        def_subs.values
    ] = _ext_constant_materials_for_om_per_capacity_installed_res_elec().values[
        def_subs.values
    ]
    return value


_ext_constant_materials_for_om_per_capacity_installed_res_elec = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "materials_for_om_per_capacity_installed_res_elec*",
    {
        "RES_elec": _subscript_dict["RES_ELEC_VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    {
        "RES_elec": _subscript_dict["RES_elec"],
        "materials": _subscript_dict["materials"],
    },
    "_ext_constant_materials_for_om_per_capacity_installed_res_elec",
)


@component.add(
    name="materials_per_new_capacity_installed_RES",
    units="kg/MW",
    subscripts=["RES_ELEC_VARIABLE", "materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_capacity_installed_res"
    },
)
def materials_per_new_capacity_installed_res():
    """
    Materials requirements per unit of new installed capacity of RES.
    """
    return _ext_constant_materials_per_new_capacity_installed_res()


_ext_constant_materials_per_new_capacity_installed_res = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_res*",
    {
        "RES_ELEC_VARIABLE": _subscript_dict["RES_ELEC_VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    {
        "RES_ELEC_VARIABLE": _subscript_dict["RES_ELEC_VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    "_ext_constant_materials_per_new_capacity_installed_res",
)


@component.add(
    name="materials_per_new_RES_elec_capacity_installed_HVDCs",
    units="kg/MW",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs"
    },
)
def materials_per_new_res_elec_capacity_installed_hvdcs():
    """
    Materials requirements for inter-regional grids (HVDCs) per unit of new installed capacity of RES variable for electricity.
    """
    return _ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs()


_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_hvdcs*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs",
)


@component.add(
    name="materials_per_new_RES_elec_capacity_installed_material_overgrid_high_power",
    units="kg/MW",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power"
    },
)
def materials_per_new_res_elec_capacity_installed_material_overgrid_high_power():
    """
    Materials requirements for overgrid high power per unit of new installed capacity of RES variable for electricity.
    """
    return (
        _ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
    )


_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_material_overgrid_high_power*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power",
)


@component.add(
    name="materials_required_for_new_RES_elec_Mt",
    units="Mt/year",
    subscripts=["RES_elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_capacity_under_construction_tw": 1,
        "materials_for_new_res_elec_per_capacity_installed": 1,
        "mw_per_tw": 1,
        "kg_per_mt": 1,
    },
)
def materials_required_for_new_res_elec_mt():
    """
    Annual materials required for the installation of new capacity of RES for electricity by technology.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * materials_for_new_res_elec_per_capacity_installed()
        * mw_per_tw()
        / kg_per_mt()
    )


@component.add(
    name='"materials_required_for_O&M_RES_elec_Mt"',
    units="Mt/year",
    subscripts=["RES_elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec": 1,
        "materials_for_om_per_capacity_installed_res_elec": 1,
        "mw_per_tw": 1,
        "kg_per_mt": 1,
    },
)
def materials_required_for_om_res_elec_mt():
    """
    Annual materials required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return (
        installed_capacity_res_elec()
        * materials_for_om_per_capacity_installed_res_elec()
        * mw_per_tw()
        / kg_per_mt()
    )


@component.add(
    name="Total_materials_required_for_new_RES_elec_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"materials_required_for_new_res_elec_mt": 1},
)
def total_materials_required_for_new_res_elec_mt():
    """
    Total annual materials requirements per new installed capacity of RES for electricity generation.
    """
    return sum(
        materials_required_for_new_res_elec_mt().rename({"RES_elec": "RES_elec!"}),
        dim=["RES_elec!"],
    )


@component.add(
    name='"Total_materials_required_for_O&M_RES_elec_Mt"',
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"materials_required_for_om_res_elec_mt": 1},
)
def total_materials_required_for_om_res_elec_mt():
    """
    Total annual materials required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return sum(
        materials_required_for_om_res_elec_mt().rename({"RES_elec": "RES_elec!"}),
        dim=["RES_elec!"],
    )


@component.add(
    name="Total_materials_required_for_RES_elec_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_new_res_elec_mt": 1,
        "total_materials_required_for_om_res_elec_mt": 1,
    },
)
def total_materials_required_for_res_elec_mt():
    """
    Total annual materials requirements for the installation and O&M of RES for electricity generation.
    """
    return (
        total_materials_required_for_new_res_elec_mt()
        + total_materials_required_for_om_res_elec_mt()
    )


@component.add(
    name="Total_materials_to_extract_for_RES_elec_from_2015_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "total_materials_to_extract_for_res_elec_mt": 1},
)
def total_materials_to_extract_for_res_elec_from_2015_mt():
    """
    Annual materials to be mined for the installation and O&M of RES for electricity generation from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_materials_to_extract_for_res_elec_mt(),
    )


@component.add(
    name="Total_materials_to_extract_for_RES_elec_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_res_elec_mt": 1,
        "recycling_rates_minerals_alt_techn": 1,
    },
)
def total_materials_to_extract_for_res_elec_mt():
    """
    Annual materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return total_materials_required_for_res_elec_mt() * (
        1 - recycling_rates_minerals_alt_techn()
    )


@component.add(
    name="Total_recycled_materials_for_RES_elec_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_res_elec_mt": 1,
        "total_materials_to_extract_for_res_elec_mt": 1,
    },
)
def total_recycled_materials_for_res_elec_mt():
    """
    Total recycled materials for RES technologies for the generation of electricity.
    """
    return (
        total_materials_required_for_res_elec_mt()
        - total_materials_to_extract_for_res_elec_mt()
    )
