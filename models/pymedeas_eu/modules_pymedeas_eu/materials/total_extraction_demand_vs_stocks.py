"""
Module total_extraction_demand_vs_stocks
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="cum materials to extract for alt techn from 2015 EU",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cum_materials_to_extract_for_ev_batteries_from_2015": 1,
        "cum_materials_to_extract_for_res_elec_from_2015": 1,
    },
)
def cum_materials_to_extract_for_alt_techn_from_2015_eu():
    """
    Cumulative materials demand for alternative technologies (RES elec & EV batteries) from the year 2015.
    """
    return (
        cum_materials_to_extract_for_ev_batteries_from_2015()
        + cum_materials_to_extract_for_res_elec_from_2015()
    )


@component.add(
    name="current mineral reserves Mt",
    units="Mdollars",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_current_mineral_reserves_mt"},
)
def current_mineral_reserves_mt():
    """
    Current global mineral reserves.
    """
    return _ext_constant_current_mineral_reserves_mt()


_ext_constant_current_mineral_reserves_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_reserves_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_current_mineral_reserves_mt",
)


@component.add(
    name="current mineral resources Mt",
    units="Mdollars",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_current_mineral_resources_mt"},
)
def current_mineral_resources_mt():
    """
    Current global mineral resources. Source: global model.
    """
    return _ext_constant_current_mineral_resources_mt()


_ext_constant_current_mineral_resources_mt = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_mineral_resources_mt*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_current_mineral_resources_mt",
)


@component.add(
    name='"materials availability (reserves)"',
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world": 1},
)
def materials_availability_reserves():
    """
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


@component.add(
    name='"materials availability (resources)"',
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_cum_materials_to_extract_alt_techn_eu_vs_resources_world": 1},
)
def materials_availability_resources():
    """
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


@component.add(
    name="share cum materials to extract alt techn EU vs reserves World",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cum_materials_to_extract_for_alt_techn_from_2015_eu": 1,
        "current_mineral_reserves_mt": 1,
    },
)
def share_cum_materials_to_extract_alt_techn_eu_vs_reserves_world():
    """
    Annual demand of materials for alternative technologies vs. current EU extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_reserves_mt(),
    )


@component.add(
    name="share cum materials to extract alt techn EU vs resources World",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cum_materials_to_extract_for_alt_techn_from_2015_eu": 1,
        "current_mineral_resources_mt": 1,
    },
)
def share_cum_materials_to_extract_alt_techn_eu_vs_resources_world():
    """
    Annual demand of materials for alternative technologies vs. current EU extraction of each material.
    """
    return zidz(
        cum_materials_to_extract_for_alt_techn_from_2015_eu(),
        current_mineral_resources_mt(),
    )


@component.add(
    name='"Total materials to extract alt techn Mt/yr"',
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_to_extract_for_ev_batteries_mt": 1,
        "total_materials_to_extract_for_res_elec_mt": 1,
    },
)
def total_materials_to_extract_alt_techn_mtyr():
    """
    Total materials to extract annually in UE for RES elec and EV batteries.
    """
    return (
        total_materials_to_extract_for_ev_batteries_mt()
        + total_materials_to_extract_for_res_elec_mt()
    )
