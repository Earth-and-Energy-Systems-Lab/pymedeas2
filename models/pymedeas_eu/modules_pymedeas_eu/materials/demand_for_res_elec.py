"""
Module materials.demand_for_res_elec
Translated using PySD version 3.9.1
"""


@component.add(
    name="cum materials requirements for RES elec",
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
    name="initial cumulated material requirements for RES elec 1995",
    units="Mt",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cumulated_material_requirements_for_res_elec_1995():
    return 0


@component.add(
    name="kg per Mt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def kg_per_mt():
    """
    Conversion factor from Mt to kg.
    """
    return 1000000000.0


@component.add(
    name="M per T", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def m_per_t():
    """
    Conversion factor from Tera (T, 1e12) to Mega (M, 1e6).
    """
    return 1000000.0


@component.add(
    name="materials per new capacity installed RES",
    units="kg/MW",
    subscripts=["RES ELEC VARIABLE", "materials"],
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
    "../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_res*",
    {
        "RES ELEC VARIABLE": _subscript_dict["RES ELEC VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    {
        "RES ELEC VARIABLE": _subscript_dict["RES ELEC VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    "_ext_constant_materials_per_new_capacity_installed_res",
)


@component.add(
    name="Total materials required for RES elec Mt",
    units="Mt/Year",
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
