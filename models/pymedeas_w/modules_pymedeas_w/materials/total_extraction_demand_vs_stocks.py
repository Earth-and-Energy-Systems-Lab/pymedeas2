"""
Module total_extraction_demand_vs_stocks
Translated using PySD version 2.2.3
"""


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_alt_techn_from_2015():
    """
    Real Name: cum materials to extract for alt techn from 2015
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Cumulative materials demand for alternative technologies (RES elec & EV batteries) from the year 2015.
    """
    return (
        cum_materials_to_extract_for_ev_batteries_from_2015()
        + cum_materials_to_extract_for_res_elec_from_2015()
    )


@subs(["materials"], _subscript_dict)
def current_mineral_reserves_mt():
    """
    Real Name: current mineral reserves Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Current mineral reserves.
    """
    return _ext_constant_current_mineral_reserves_mt()


_ext_constant_current_mineral_reserves_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_reserves_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_current_mineral_reserves_mt",
)


@subs(["materials"], _subscript_dict)
def current_mineral_resources_mt():
    """
    Real Name: current mineral resources Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Current mineral resources.
    """
    return _ext_constant_current_mineral_resources_mt()


_ext_constant_current_mineral_resources_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_resources_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_current_mineral_resources_mt",
)


@subs(["materials"], _subscript_dict)
def materials_availability_reserves():
    """
    Real Name: "materials availability (reserves)"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def materials_availability_resources():
    """
    Real Name: "materials availability (resources)"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_cum_dem_materials_to_extract_alt_techn_vs_total():
    """
    Real Name: share cum dem materials to extract alt techn vs total
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_materials_cum_demand_to_extract_vs_reserves_for_res_elec():
    """
    Real Name: share materials cum demand to extract vs reserves for RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_materials_cum_demand_to_extract_vs_resources_for_res_elec():
    """
    Real Name: share materials cum demand to extract vs resources for RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_other_cumulative_demand_to_extract_vs_reserves_materials():
    """
    Real Name: share other cumulative demand to extract vs reserves materials
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_other_cumulative_demand_to_extract_vs_resources_materials():
    """
    Real Name: share other cumulative demand to extract vs resources materials
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_tot_cum_dem_vs_reserves_materials():
    """
    Real Name: share tot cum dem vs reserves materials
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def share_tot_cum_dem_vs_resources_materials():
    """
    Real Name: share tot cum dem vs resources materials
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def total_cumulative_demand_materials_to_extract_from_2015():
    """
    Real Name: total cumulative demand materials to extract from 2015
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Total cumulative demand materials to extract in mines.
    """
    return (
        cum_materials_to_extract_for_alt_techn_from_2015()
        + cum_materials_to_extract_rest_from_2015()
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_mt():
    """
    Real Name: Total materials to extract Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']


    """
    return (
        materials_to_extract_rest_mt()
        + total_materials_to_extract_for_res_elec_mt()
        + total_materials_to_extract_for_ev_batteries_mt()
    )
