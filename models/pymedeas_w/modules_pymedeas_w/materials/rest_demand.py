"""
Module materials.rest_demand
Translated using PySD version 3.14.1
"""

@component.add(
    name="\"'a' extraction projection minerals\"",
    units="t/(year*year*T$)",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_a_extraction_projection_minerals"},
)
def a_extraction_projection_minerals():
    return _ext_constant_a_extraction_projection_minerals()


_ext_constant_a_extraction_projection_minerals = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "a_extraction_projection_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_a_extraction_projection_minerals",
)


@component.add(
    name="cum materials to extract Rest",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_rest": 1},
    other_deps={
        "_integ_cum_materials_to_extract_rest": {
            "initial": {"initial_cumulated_material_requirements_for_rest_1995": 1},
            "step": {"materials_to_extract_rest_mt": 1},
        }
    },
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
    depends_on={"_integ_cum_materials_to_extract_rest_from_2015": 1},
    other_deps={
        "_integ_cum_materials_to_extract_rest_from_2015": {
            "initial": {"initial_cumulated_material_requirements_for_rest_1995": 1},
            "step": {"materials_to_extract_rest_from_2015_mt": 1},
        }
    },
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
    units="t/year",
    subscripts=["materials"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historical_extraction_minerals_rest",
        "__lookup__": "_ext_lookup_historical_extraction_minerals_rest",
    },
)
def historical_extraction_minerals_rest(x, final_subs=None):
    """
    Historical extraction of minerals of the rest of the economy.
    """
    return _ext_lookup_historical_extraction_minerals_rest(x, final_subs)


_ext_lookup_historical_extraction_minerals_rest = ExtLookup(
    r"../materials.xlsx",
    "Global",
    "time",
    "historical_extraction_minerals_rest",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_lookup_historical_extraction_minerals_rest",
)


@component.add(
    name="Historical variation minerals extraction Rest",
    units="t/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "time_step": 1, "historical_extraction_minerals_rest": 2},
)
def historical_variation_minerals_extraction_rest():
    """
    Historical variation in the extraction of minerals of the rest of the economy.
    """
    return historical_extraction_minerals_rest(
        time() + time_step()
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
    units="t/year",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_minerals_extraction_rest"},
)
def initial_minerals_extraction_rest():
    """
    Initial minerals extraction of the rest of the economy.
    """
    return _ext_constant_initial_minerals_extraction_rest()


_ext_constant_initial_minerals_extraction_rest = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "initial_minerals_extraction_rest*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_initial_minerals_extraction_rest",
)


@component.add(
    name="Materials to extract Rest from 2015 Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "materials_to_extract_rest_mt": 1},
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
    depends_on={"minerals_extraction_projection_rest_with_rr": 1},
)
def materials_to_extract_rest_mt():
    """
    Annual materials to be mined for the rest of the economy.
    """
    return minerals_extraction_projection_rest_with_rr()


@component.add(
    name="Minerals consumption estimation Rest cte rr",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minerals_extraction_projection_rest_cte_rr": 1,
        "current_recycling_rates_minerals": 1,
    },
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
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_minerals_extraction_projection_rest_cte_rr": 1},
    other_deps={
        "_integ_minerals_extraction_projection_rest_cte_rr": {
            "initial": {"initial_minerals_extraction_rest": 1, "mt_per_t": 1},
            "step": {"variation_minerals_extraction_rest": 1},
        }
    },
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
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minerals_consumption_estimation_rest_cte_rr": 1,
        "recycling_rates_minerals_rest": 1,
    },
)
def minerals_extraction_projection_rest_with_rr():
    """
    Minerals extraction projection of the rest of the economy accounting for the dynamic evolution of recycling rates.
    """
    return minerals_consumption_estimation_rest_cte_rr() * (
        1 - recycling_rates_minerals_rest()
    )


@component.add(
    name="Mt per t", units="Mt/t", comp_type="Constant", comp_subtype="Normal"
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
    depends_on={
        "total_materials_required_for_res_elec_ev_batteries_mt": 2,
        "minerals_consumption_estimation_rest_cte_rr": 1,
    },
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
    depends_on={
        "total_materials_required_for_ev_batteries": 1,
        "total_materials_required_for_res_elec_mt": 1,
    },
)
def total_materials_required_for_res_elec_ev_batteries_mt():
    return (
        total_materials_required_for_ev_batteries()
        + total_materials_required_for_res_elec_mt()
    )


@component.add(
    name="Total recycled materials for other Mt",
    units="Mt/year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minerals_consumption_estimation_rest_cte_rr": 1,
        "minerals_extraction_projection_rest_with_rr": 1,
    },
)
def total_recycled_materials_for_other_mt():
    return (
        minerals_consumption_estimation_rest_cte_rr()
        - minerals_extraction_projection_rest_with_rr()
    )


@component.add(
    name="variation minerals extraction Rest",
    units="Mt/(year*year)",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historical_variation_minerals_extraction_rest": 1,
        "time_step": 1,
        "gdp_delayed_1yr": 1,
        "minerals_extraction_projection_rest_cte_rr": 1,
        "gdp": 1,
        "a_extraction_projection_minerals": 1,
        "mt_per_t": 1,
    },
)
def variation_minerals_extraction_rest():
    """
    Variation of minerals extraction of the rest of the economy.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: historical_variation_minerals_extraction_rest() / time_step(),
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
