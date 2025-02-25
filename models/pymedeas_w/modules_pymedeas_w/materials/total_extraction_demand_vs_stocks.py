"""
Module materials.total_extraction_demand_vs_stocks
Translated using PySD version 3.14.2
"""

@component.add(
    name="cum_materials_to_extract_for_alt_techn_from_2015",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cum_materials_to_extract_for_ev_batteries_from_2015": 1,
        "cum_materials_to_extract_for_res_elec_from_2015": 1,
    },
)
def cum_materials_to_extract_for_alt_techn_from_2015():
    """
    Cumulative materials demand for alternative technologies (RES elec & EV batteries) from the year 2015.
    """
    return (
        cum_materials_to_extract_for_ev_batteries_from_2015()
        + cum_materials_to_extract_for_res_elec_from_2015()
    )


@component.add(
    name="current_mineral_reserves_Mt",
    units="Mt",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_current_mineral_reserves_mt"},
)
def current_mineral_reserves_mt():
    """
    Current mineral reserves.
    """
    return _ext_constant_current_mineral_reserves_mt()


_ext_constant_current_mineral_reserves_mt = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "current_mineral_reserves_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_current_mineral_reserves_mt",
)


@component.add(
    name="current_mineral_resources_Mt",
    units="Mt",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_current_mineral_resources_mt"},
)
def current_mineral_resources_mt():
    """
    Current mineral resources.
    """
    return _ext_constant_current_mineral_resources_mt()


_ext_constant_current_mineral_resources_mt = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "current_mineral_resources_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_current_mineral_resources_mt",
)


@component.add(
    name='"materials_availability_(reserves)"',
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_tot_cum_dem_vs_reserves_materials": 1},
)
def materials_availability_reserves():
    """
    =1 while the cumulative demand is lower than the estimated resources, and =0 when the cumulative demand surpasses the estimated resources.
    """
    return if_then_else(
        share_tot_cum_dem_vs_reserves_materials() < 1,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name='"materials_availability_(resources)"',
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_tot_cum_dem_vs_resources_materials": 1},
)
def materials_availability_resources():
    """
    =1 while the cumulative demand is lower than the estimated reserves, and =0 when the cumulative demand surpasses the estimated reserves.
    """
    return if_then_else(
        share_tot_cum_dem_vs_resources_materials() < 1,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name="share_cum_dem_materials_to_extract_alt_techn_vs_total",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_cumulative_demand_materials_to_extract_from_2015": 2,
        "cum_materials_to_extract_for_alt_techn_from_2015": 1,
    },
)
def share_cum_dem_materials_to_extract_alt_techn_vs_total():
    """
    Yearly share of cumulative demand of materials to extract for alternative technologies (RES elec & EV batteries) vs. total.
    """
    return if_then_else(
        total_cumulative_demand_materials_to_extract_from_2015() <= 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: cum_materials_to_extract_for_alt_techn_from_2015()
        / total_cumulative_demand_materials_to_extract_from_2015(),
    )


@component.add(
    name="share_materials_cum_demand_to_extract_vs_reserves_for_RES_elec",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_reserves_mt": 2,
        "cum_materials_to_extract_for_alt_techn_from_2015": 1,
    },
)
def share_materials_cum_demand_to_extract_vs_reserves_for_res_elec():
    """
    Share of materials cumulative demand to extract in mines for RES elec vs reserves of each material.
    """
    return if_then_else(
        current_mineral_reserves_mt() == 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: cum_materials_to_extract_for_alt_techn_from_2015()
        / current_mineral_reserves_mt(),
    )


@component.add(
    name="share_materials_cum_demand_to_extract_vs_resources_for_RES_elec",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_resources_mt": 2,
        "cum_materials_to_extract_for_alt_techn_from_2015": 1,
    },
)
def share_materials_cum_demand_to_extract_vs_resources_for_res_elec():
    """
    Share of materials cumulative demand to extract in mines for RES elec vs resources of each material.
    """
    return if_then_else(
        current_mineral_resources_mt() == 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: cum_materials_to_extract_for_alt_techn_from_2015()
        / current_mineral_resources_mt(),
    )


@component.add(
    name="share_other_cumulative_demand_to_extract_vs_reserves_materials",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_reserves_mt": 2,
        "cum_materials_to_extract_rest_from_2015": 1,
    },
)
def share_other_cumulative_demand_to_extract_vs_reserves_materials():
    """
    Yearly share of other cumulative demand to be extracted in mines of materials vs. reserves.
    """
    return if_then_else(
        current_mineral_reserves_mt() <= 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: cum_materials_to_extract_rest_from_2015()
        / current_mineral_reserves_mt(),
    )


@component.add(
    name="share_other_cumulative_demand_to_extract_vs_resources_materials",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_resources_mt": 2,
        "cum_materials_to_extract_rest_from_2015": 1,
    },
)
def share_other_cumulative_demand_to_extract_vs_resources_materials():
    """
    Yearly share of other cumulative demand to be extracted in mines of materials vs. resources.
    """
    return if_then_else(
        current_mineral_resources_mt() <= 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: cum_materials_to_extract_rest_from_2015()
        / current_mineral_resources_mt(),
    )


@component.add(
    name="share_tot_cum_dem_vs_reserves_materials",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_reserves_mt": 2,
        "total_cumulative_demand_materials_to_extract_from_2015": 1,
    },
)
def share_tot_cum_dem_vs_reserves_materials():
    """
    Yearly share of total cumulative demand of materials vs. reserves.
    """
    return if_then_else(
        current_mineral_reserves_mt() <= 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_cumulative_demand_materials_to_extract_from_2015()
        / current_mineral_reserves_mt(),
    )


@component.add(
    name="share_tot_cum_dem_vs_resources_materials",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_mineral_resources_mt": 2,
        "total_cumulative_demand_materials_to_extract_from_2015": 1,
    },
)
def share_tot_cum_dem_vs_resources_materials():
    """
    Yearly share of total cumulative demand of materials vs. resources.
    """
    return if_then_else(
        current_mineral_resources_mt() <= 0,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_cumulative_demand_materials_to_extract_from_2015()
        / current_mineral_resources_mt(),
    )


@component.add(
    name="total_cumulative_demand_materials_to_extract_from_2015",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cum_materials_to_extract_for_alt_techn_from_2015": 1,
        "cum_materials_to_extract_rest_from_2015": 1,
    },
)
def total_cumulative_demand_materials_to_extract_from_2015():
    """
    Total cumulative demand materials to extract in mines.
    """
    return (
        cum_materials_to_extract_for_alt_techn_from_2015()
        + cum_materials_to_extract_rest_from_2015()
    )


@component.add(
    name="Total_materials_to_extract_Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "materials_to_extract_rest_mt": 1,
        "total_materials_to_extract_for_res_elec_mt": 1,
        "total_materials_to_extract_for_ev_batteries_mt": 1,
    },
)
def total_materials_to_extract_mt():
    return (
        materials_to_extract_rest_mt()
        + total_materials_to_extract_for_res_elec_mt()
        + total_materials_to_extract_for_ev_batteries_mt()
    )
