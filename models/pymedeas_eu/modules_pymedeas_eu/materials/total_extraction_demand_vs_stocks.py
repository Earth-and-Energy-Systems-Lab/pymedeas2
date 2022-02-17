"""
Module total_extraction_demand_vs_stocks
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_alt_techn_from_2015_eu():
    """
    Real Name: cum materials to extract for alt techn from 2015 EU
    Original Eqn: cum materials to extract for EV batteries from 2015[materials]+cum materials to extract for RES elec from 2015[materials]
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials demand for alternative technologies (RES elec & EV
        batteries) from the year 2015.
    """
    return (
        cum_materials_to_extract_for_ev_batteries_from_2015()
        + cum_materials_to_extract_for_res_elec_from_2015()
    )


@subs(["materials"], _subscript_dict)
def current_mineral_reserves_mt():
    """
    Real Name: current mineral reserves Mt
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'current_mineral_reserves_mt*')
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Current global mineral reserves.
    """
    return _ext_constant_current_mineral_reserves_mt()


@subs(["materials"], _subscript_dict)
def current_mineral_resources_mt():
    """
    Real Name: current mineral resources Mt
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'current_mineral_resources_mt*')
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Current global mineral resources. Source: global model.
    """
    return _ext_constant_current_mineral_resources_mt()


@subs(["materials"], _subscript_dict)
def materials_availability_reserves():
    """
    Real Name: "materials availability (reserves)"
    Original Eqn: IF THEN ELSE(share cum materials to extract alt techn EU vs reserves World[materials]<1,1,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    =1 while the cumulative demand is lower than the estimated resources, and
        =0 when the cumulative demand surpasses the estimated resources.
    """
    return if_then_else(
        share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world() < 1,
        lambda: 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def materials_availability_resources():
    """
    Real Name: "materials availability (resources)"
    Original Eqn: IF THEN ELSE(share cum materials to extract alt techn EU vs resources World[materials]<1,1,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    =1 while the cumulative demand is lower than the estimated reserves, and
        =0 when the cumulative demand surpasses the estimated reserves.
    """
    return if_then_else(
        share_cum_materials_to_extract_alt_techn_eu_vs_resources_world() < 1,
        lambda: 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world():
    """
    Real Name: share cum materials to extract alt techn EU vs reserves World
    Original Eqn: ZIDZ( cum materials to extract for alt techn from 2015 EU[materials], current mineral reserves Mt[materials] )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual demand of materials for alternative technologies vs. current EU
        extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_reserves_mt(),
    )


@subs(["materials"], _subscript_dict)
def share_cum_materials_to_extract_alt_techn_eu_vs_resources_world():
    """
    Real Name: share cum materials to extract alt techn EU vs resources World
    Original Eqn: ZIDZ( cum materials to extract for alt techn from 2015 EU[materials], current mineral resources Mt[materials] )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual demand of materials for alternative technologies vs. current EU
        extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_resources_mt(),
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_alt_techn_mtyr():
    """
    Real Name: "Total materials to extract alt techn Mt/yr"
    Original Eqn: Total materials to extract for EV batteries Mt[materials]+Total materials to extract for RES elec Mt[materials]
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total materials to extract annually in UE for RES elec and EV batteries.
    """
    return (
        total_materials_to_extract_for_ev_batteries_mt()
        + total_materials_to_extract_for_res_elec_mt()
    )


_ext_constant_current_mineral_reserves_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_reserves_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_current_mineral_reserves_mt",
)


_ext_constant_current_mineral_resources_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_resources_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_current_mineral_resources_mt",
)
