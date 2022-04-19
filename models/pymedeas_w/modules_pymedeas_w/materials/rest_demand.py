"""
Module rest_demand
Translated using PySD version 3.0.0
"""


@component.add(
    name="\"'a' extraction projection minerals\"",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
)
def a_extraction_projection_minerals():
    return _ext_constant_a_extraction_projection_minerals()


_ext_constant_a_extraction_projection_minerals = ExtConstant(
    "../materials.xlsx",
    "Global",
    "a_extraction_projection_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {
        "materials": [
            "Adhesive",
            "Aluminium",
            "Aluminium mirrors",
            "Cadmium",
            "Carbon fiber",
            "Cement",
            "Chromium",
            "Copper",
            "diesel",
            "Dy",
            "electronic components",
            "Evacuation lines",
            "Fiberglass",
            "Foam glass",
            "Galium",
            "Glass",
            "Glass reinforcing plastic",
            "gravel",
            "Indium",
            "Iron",
            "KNO3 mined",
            "Asphalt",
            "Lime",
            "Limestone",
            "Lithium",
            "Lubricant",
            "Magnesium",
            "Manganese",
            "Heavy equipment",
            "Concrete",
            "Molybdenum",
            "NaNO3 mined",
            "NaNO3 synthetic",
            "Neodymium",
            "Nickel",
            "over grid 15perc",
            "over grid 5perc",
            "Paint",
            "Lead",
            "Plastics",
            "Polypropylene",
            "Rock",
            "Rock wool",
            "Sand",
            "Silicon sand",
            "Silicon wafer modules",
            "Silver",
            "Site preparation",
            "Tin",
            "soda ash",
            "steel",
            "synthetic oil",
            "tellurium",
            "titanium",
            "titanium dioxide",
            "vanadium",
            "wires",
            "zinc",
        ]
    },
    "_ext_constant_a_extraction_projection_minerals",
)


@component.add(
    name="cum materials to extract Rest",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def cum_materials_to_extract_rest():
    """
    Cumulative materials to be mined for the rest of the economy.
    """
    return _integ_cum_materials_to_extract_rest()


_integ_cum_materials_to_extract_rest = Integ(
    lambda: materials_to_extract_rest_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_rest_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_rest",
)


@component.add(
    name="cum materials to extract Rest from 2015",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def cum_materials_to_extract_rest_from_2015():
    """
    Cumulative materials to be mined for the rest of the economy from 2015.
    """
    return _integ_cum_materials_to_extract_rest_from_2015()


_integ_cum_materials_to_extract_rest_from_2015 = Integ(
    lambda: materials_to_extract_rest_from_2015_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_rest_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_rest_from_2015",
)


@component.add(
    name="Historical extraction minerals Rest",
    units="t",
    subscripts=["materials"],
    comp_type="Lookup",
    comp_subtype="External",
)
def historical_extraction_minerals_rest(x, final_subs=None):
    """
    Historical extraction of minerals of the rest of the economy.
    """
    return _ext_lookup_historical_extraction_minerals_rest(x, final_subs)


_ext_lookup_historical_extraction_minerals_rest = ExtLookup(
    "../materials.xlsx",
    "Global",
    "time",
    "historical_extraction_minerals_rest",
    {"materials": _subscript_dict["materials"]},
    _root,
    {
        "materials": [
            "Adhesive",
            "Aluminium",
            "Aluminium mirrors",
            "Cadmium",
            "Carbon fiber",
            "Cement",
            "Chromium",
            "Copper",
            "diesel",
            "Dy",
            "electronic components",
            "Evacuation lines",
            "Fiberglass",
            "Foam glass",
            "Galium",
            "Glass",
            "Glass reinforcing plastic",
            "gravel",
            "Indium",
            "Iron",
            "KNO3 mined",
            "Asphalt",
            "Lime",
            "Limestone",
            "Lithium",
            "Lubricant",
            "Magnesium",
            "Manganese",
            "Heavy equipment",
            "Concrete",
            "Molybdenum",
            "NaNO3 mined",
            "NaNO3 synthetic",
            "Neodymium",
            "Nickel",
            "over grid 15perc",
            "over grid 5perc",
            "Paint",
            "Lead",
            "Plastics",
            "Polypropylene",
            "Rock",
            "Rock wool",
            "Sand",
            "Silicon sand",
            "Silicon wafer modules",
            "Silver",
            "Site preparation",
            "Tin",
            "soda ash",
            "steel",
            "synthetic oil",
            "tellurium",
            "titanium",
            "titanium dioxide",
            "vanadium",
            "wires",
            "zinc",
        ]
    },
    "_ext_lookup_historical_extraction_minerals_rest",
)


@component.add(
    name="Historical variation minerals extraction Rest",
    units="t",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historical_variation_minerals_extraction_rest():
    """
    Historical variation in the extraction of minerals of the rest of the economy.
    """
    return historical_extraction_minerals_rest(
        time() + 1
    ) - historical_extraction_minerals_rest(time())


@component.add(
    name="initial cumulated material requirements for Rest 1995",
    units="Mt",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cumulated_material_requirements_for_rest_1995():
    return 0


@component.add(
    name="initial minerals extraction Rest",
    units="t",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
)
def initial_minerals_extraction_rest():
    """
    Initial minerals extraction of the rest of the economy.
    """
    return _ext_constant_initial_minerals_extraction_rest()


_ext_constant_initial_minerals_extraction_rest = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_minerals_extraction_rest*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {
        "materials": [
            "Adhesive",
            "Aluminium",
            "Aluminium mirrors",
            "Cadmium",
            "Carbon fiber",
            "Cement",
            "Chromium",
            "Copper",
            "diesel",
            "Dy",
            "electronic components",
            "Evacuation lines",
            "Fiberglass",
            "Foam glass",
            "Galium",
            "Glass",
            "Glass reinforcing plastic",
            "gravel",
            "Indium",
            "Iron",
            "KNO3 mined",
            "Asphalt",
            "Lime",
            "Limestone",
            "Lithium",
            "Lubricant",
            "Magnesium",
            "Manganese",
            "Heavy equipment",
            "Concrete",
            "Molybdenum",
            "NaNO3 mined",
            "NaNO3 synthetic",
            "Neodymium",
            "Nickel",
            "over grid 15perc",
            "over grid 5perc",
            "Paint",
            "Lead",
            "Plastics",
            "Polypropylene",
            "Rock",
            "Rock wool",
            "Sand",
            "Silicon sand",
            "Silicon wafer modules",
            "Silver",
            "Site preparation",
            "Tin",
            "soda ash",
            "steel",
            "synthetic oil",
            "tellurium",
            "titanium",
            "titanium dioxide",
            "vanadium",
            "wires",
            "zinc",
        ]
    },
    "_ext_constant_initial_minerals_extraction_rest",
)


@component.add(
    name="Materials to extract Rest from 2015 Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def materials_to_extract_rest_from_2015_mt():
    """
    Annual materials to be mined for the ithe rest of the economy from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: materials_to_extract_rest_mt(),
    )


@component.add(
    name="Materials to extract Rest Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def materials_to_extract_rest_mt():
    """
    Annual materials to be mined for the rest of the economy.
    """
    return minerals_extraction_projection_rest_with_rr()


@component.add(
    name="Minerals consumption estimation Rest cte rr",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def minerals_consumption_estimation_rest_cte_rr():
    """
    Projection of annual mineral consumption of the rest of the economy using historical data and assuming recycling rates remaing constant.
    """
    return minerals_extraction_projection_rest_cte_rr() / (
        1 - current_recycling_rates_minerals()
    )


@component.add(
    name="Minerals extraction projection Rest cte rr",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def minerals_extraction_projection_rest_cte_rr():
    """
    Projection of annual mineral extraction of the rest of the economy using historical data and assuming recycling rates remaing constant.
    """
    return _integ_minerals_extraction_projection_rest_cte_rr()


_integ_minerals_extraction_projection_rest_cte_rr = Integ(
    lambda: variation_minerals_extraction_rest(),
    lambda: initial_minerals_extraction_rest() * mt_per_t(),
    "_integ_minerals_extraction_projection_rest_cte_rr",
)


@component.add(
    name="Minerals extraction projection Rest with rr",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def minerals_extraction_projection_rest_with_rr():
    """
    Minerals extraction projection of the rest of the economy accounting for the dynamic evolution of recycling rates.
    """
    return minerals_consumption_estimation_rest_cte_rr() * (
        1 - recycling_rates_minerals_rest()
    )


@component.add(
    name="Mt per t", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mt_per_t():
    """
    megatonne per tonne.
    """
    return 1e-06


@component.add(
    name="share minerals consumption alt techn vs total economy",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_minerals_consumption_alt_techn_vs_total_economy():
    return zidz(
        total_materials_required_for_res_elec_ev_batteries_mt(),
        minerals_consumption_estimation_rest_cte_rr()
        + total_materials_required_for_res_elec_ev_batteries_mt(),
    )


@component.add(
    name='"Total materials required for RES elec + EV batteries Mt"',
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_materials_required_for_res_elec_ev_batteries_mt():
    return (
        total_materials_required_for_ev_batteries()
        + total_materials_required_for_res_elec_mt()
    )


@component.add(
    name="Total recycled materials for other Mt",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_recycled_materials_for_other_mt():
    return (
        minerals_consumption_estimation_rest_cte_rr()
        - minerals_extraction_projection_rest_with_rr()
    )


@component.add(
    name="variation minerals extraction Rest",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_minerals_extraction_rest():
    """
    Variation of minerals extraction of the rest of the economy.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: historical_variation_minerals_extraction_rest(),
            lambda: if_then_else(
                minerals_extraction_projection_rest_cte_rr() > 0.01,
                lambda: a_extraction_projection_minerals()
                * (gdp() - gdp_delayed_1yr()),
                lambda: xr.DataArray(
                    0, {"materials": _subscript_dict["materials"]}, ["materials"]
                ),
            ),
        )
        * mt_per_t()
    )
