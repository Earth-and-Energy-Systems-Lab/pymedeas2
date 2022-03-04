"""
Module total_extraction_demand_vs_stocks
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_alt_techn_from_2015_eu():
    """
    Real Name: cum materials to extract for alt techn from 2015 EU
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
    Units: Mdollars
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Current global mineral reserves.
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
    Units: Mdollars
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Current global mineral resources. Source: global model.
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
        share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world() < 1,
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
        share_cum_materials_to_extract_alt_techn_eu_vs_resources_world() < 1,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@subs(["materials"], _subscript_dict)
def share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world():
    """
    Real Name: share cum materials to extract alt techn EU vs reserves World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual demand of materials for alternative technologies vs. current EU extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_reserves_mt(),
    )


@subs(["materials"], _subscript_dict)
def share_cum_materials_to_extract_alt_techn_eu_vs_resources_world():
    """
    Real Name: share cum materials to extract alt techn EU vs resources World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual demand of materials for alternative technologies vs. current EU extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_resources_mt(),
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_alt_techn_mtyr():
    """
    Real Name: "Total materials to extract alt techn Mt/yr"
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Total materials to extract annually in UE for RES elec and EV batteries.
    """
    return (
        total_materials_to_extract_for_ev_batteries_mt()
        + total_materials_to_extract_for_res_elec_mt()
    )
