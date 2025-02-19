"""
Module materials.demand_for_ev_batteries
Translated using PySD version 3.14.0
"""

@component.add(
    name="cum materials requirements for EV batteries",
    units="Mt",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_requirements_for_ev_batteries": 1},
    other_deps={
        "_integ_cum_materials_requirements_for_ev_batteries": {
            "initial": {
                "initial_cumulated_material_requirements_for_ev_batteries_1995": 1
            },
            "step": {"total_materials_required_for_ev_batteries": 1},
        }
    },
)
def cum_materials_requirements_for_ev_batteries():
    """
    Total cumulative materials requirements for EV batteries.
    """
    return _integ_cum_materials_requirements_for_ev_batteries()


_integ_cum_materials_requirements_for_ev_batteries = Integ(
    lambda: total_materials_required_for_ev_batteries(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_requirements_for_ev_batteries",
)


@component.add(
    name="cum materials to extract for EV batteries",
    units="Mt",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_ev_batteries": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_ev_batteries": {
            "initial": {
                "initial_cumulated_material_requirements_for_ev_batteries_1995": 1
            },
            "step": {"total_materials_to_extract_for_ev_batteries_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_ev_batteries():
    """
    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries()


_integ_cum_materials_to_extract_for_ev_batteries = Integ(
    lambda: total_materials_to_extract_for_ev_batteries_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_ev_batteries",
)


@component.add(
    name="cum materials to extract for EV batteries from 2015",
    units="Mt",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_ev_batteries_from_2015": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_ev_batteries_from_2015": {
            "initial": {
                "initial_cumulated_material_requirements_for_ev_batteries_1995": 1
            },
            "step": {"total_materials_to_extract_for_ev_batteries_from_2015_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_ev_batteries_from_2015():
    """
    Cumulative materials to be mined for EV batteries.
    """
    return _integ_cum_materials_to_extract_for_ev_batteries_from_2015()


_integ_cum_materials_to_extract_for_ev_batteries_from_2015 = Integ(
    lambda: total_materials_to_extract_for_ev_batteries_from_2015_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_ev_batteries_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_ev_batteries_from_2015",
)


@component.add(
    name="initial cumulated material requirements for EV batteries 1995",
    units="Mt",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cumulated_material_requirements_for_ev_batteries_1995():
    return 0


@component.add(
    name="kg per Mt", units="kg/Mt", comp_type="Constant", comp_subtype="Normal"
)
def kg_per_mt():
    """
    Conversion factor from Mt to kg.
    """
    return 1000000000.0


@component.add(
    name="materials per new capacity installed EV batteries",
    units="kg/MW",
    subscripts=[np.str_("materials")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_capacity_installed_ev_batteries"
    },
)
def materials_per_new_capacity_installed_ev_batteries():
    """
    Materials requirements per EV battery.
    """
    return _ext_constant_materials_per_new_capacity_installed_ev_batteries()


_ext_constant_materials_per_new_capacity_installed_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_ev_batteries*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_materials_per_new_capacity_installed_ev_batteries",
)


@component.add(
    name="materials required for EV batteries Mt",
    units="Mt/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "newreplaced_batteries_tw": 1,
        "materials_per_new_capacity_installed_ev_batteries": 1,
        "mw_per_tw": 1,
        "kg_per_mt": 1,
    },
)
def materials_required_for_ev_batteries_mt():
    """
    Annual materials required for the fabrication of EV batteries.
    """
    return (
        newreplaced_batteries_tw()
        * materials_per_new_capacity_installed_ev_batteries()
        * mw_per_tw()
        / kg_per_mt()
    )


@component.add(
    name="Total materials required for EV batteries",
    units="Mt/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"materials_required_for_ev_batteries_mt": 1},
)
def total_materials_required_for_ev_batteries():
    """
    Total annual materials requirements for EV batteries.
    """
    return materials_required_for_ev_batteries_mt()


@component.add(
    name="Total materials to extract for EV batteries from 2015 Mt",
    units="Mt/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "total_materials_to_extract_for_ev_batteries_mt": 1},
)
def total_materials_to_extract_for_ev_batteries_from_2015_mt():
    """
    Annual materials to be mined for EV batteries from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_materials_to_extract_for_ev_batteries_mt(),
    )


@component.add(
    name="Total materials to extract for EV batteries Mt",
    units="Mt/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_ev_batteries": 1,
        "recycling_rates_minerals_alt_techn": 1,
    },
)
def total_materials_to_extract_for_ev_batteries_mt():
    """
    Annual materials to be mined for the construction of EV batteries.
    """
    return total_materials_required_for_ev_batteries() * (
        1 - recycling_rates_minerals_alt_techn()
    )


@component.add(
    name="Total recycled materials for EV batteries Mt",
    units="Mt/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_ev_batteries": 1,
        "total_materials_to_extract_for_ev_batteries_mt": 1,
    },
)
def total_recycled_materials_for_ev_batteries_mt():
    """
    Total recycled materials for EV batteries.
    """
    return (
        total_materials_required_for_ev_batteries()
        - total_materials_to_extract_for_ev_batteries_mt()
    )
