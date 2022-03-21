"""
Module rest_demand
Translated using PySD version 2.2.3
"""


@subs(["materials"], _subscript_dict)
def a_extraction_projection_minerals():
    """
    Real Name: "'a' extraction projection minerals"
    Original Eqn:
    Units: Mt/year
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']


    """
    return _ext_constant_a_extraction_projection_minerals()


_ext_constant_a_extraction_projection_minerals = ExtConstant(
    "../materials.xlsx",
    "Global",
    "a_extraction_projection_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_a_extraction_projection_minerals",
)


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_rest():
    """
    Real Name: cum materials to extract Rest
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_rest_from_2015():
    """
    Real Name: cum materials to extract Rest from 2015
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

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


@subs(["materials"], _subscript_dict)
def historical_extraction_minerals_rest(x):
    """
    Real Name: Historical extraction minerals Rest
    Original Eqn:
    Units: t
    Limits: (None, None)
    Type: Lookup
    Subs: ['materials']

    Historical extraction of minerals of the rest of the economy.
    """
    return _ext_lookup_historical_extraction_minerals_rest(x)


_ext_lookup_historical_extraction_minerals_rest = ExtLookup(
    "../materials.xlsx",
    "Global",
    "time",
    "historical_extraction_minerals_rest",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_lookup_historical_extraction_minerals_rest",
)


@subs(["materials"], _subscript_dict)
def historical_variation_minerals_extraction_rest():
    """
    Real Name: Historical variation minerals extraction Rest
    Original Eqn:
    Units: t
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Historical variation in the extraction of minerals of the rest of the economy.
    """
    return historical_extraction_minerals_rest(
        time() + 1
    ) - historical_extraction_minerals_rest(time())


def initial_cumulated_material_requirements_for_rest_1995():
    """
    Real Name: initial cumulated material requirements for Rest 1995
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 0


@subs(["materials"], _subscript_dict)
def initial_minerals_extraction_rest():
    """
    Real Name: initial minerals extraction Rest
    Original Eqn:
    Units: t
    Limits: (None, None)
    Type: Constant
    Subs: ['materials']

    Initial minerals extraction of the rest of the economy.
    """
    return _ext_constant_initial_minerals_extraction_rest()


_ext_constant_initial_minerals_extraction_rest = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_minerals_extraction_rest*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_initial_minerals_extraction_rest",
)


@subs(["materials"], _subscript_dict)
def materials_to_extract_rest_from_2015_mt():
    """
    Real Name: Materials to extract Rest from 2015 Mt
    Original Eqn:
    Units: Mt/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual materials to be mined for the ithe rest of the economy from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: materials_to_extract_rest_mt(),
    )


@subs(["materials"], _subscript_dict)
def materials_to_extract_rest_mt():
    """
    Real Name: Materials to extract Rest Mt
    Original Eqn:
    Units: Mt/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Annual materials to be mined for the rest of the economy.
    """
    return minerals_extraction_projection_rest_with_rr()


@subs(["materials"], _subscript_dict)
def minerals_consumption_estimation_rest_cte_rr():
    """
    Real Name: Minerals consumption estimation Rest cte rr
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Projection of annual mineral consumption of the rest of the economy using historical data and assuming recycling rates remaing constant.
    """
    return minerals_extraction_projection_rest_cte_rr() / (
        1 - current_recycling_rates_minerals()
    )


@subs(["materials"], _subscript_dict)
def minerals_extraction_projection_rest_cte_rr():
    """
    Real Name: Minerals extraction projection Rest cte rr
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Projection of annual mineral extraction of the rest of the economy using historical data and assuming recycling rates remaing constant.
    """
    return _integ_minerals_extraction_projection_rest_cte_rr()


_integ_minerals_extraction_projection_rest_cte_rr = Integ(
    lambda: variation_minerals_extraction_rest(),
    lambda: initial_minerals_extraction_rest() * mt_per_t(),
    "_integ_minerals_extraction_projection_rest_cte_rr",
)


@subs(["materials"], _subscript_dict)
def minerals_extraction_projection_rest_with_rr():
    """
    Real Name: Minerals extraction projection Rest with rr
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Minerals extraction projection of the rest of the economy accounting for the dynamic evolution of recycling rates.
    """
    return minerals_consumption_estimation_rest_cte_rr() * (
        1 - recycling_rates_minerals_rest()
    )


def mt_per_t():
    """
    Real Name: Mt per t
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    megatonne per tonne.
    """
    return 1e-06


@subs(["materials"], _subscript_dict)
def share_minerals_consumption_alt_techn_vs_total_economy():
    """
    Real Name: share minerals consumption alt techn vs total economy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']


    """
    return zidz(
        total_materials_required_for_res_elec__ev_batteries_mt(),
        minerals_consumption_estimation_rest_cte_rr()
        + total_materials_required_for_res_elec__ev_batteries_mt(),
    )


@subs(["materials"], _subscript_dict)
def total_materials_required_for_res_elec__ev_batteries_mt():
    """
    Real Name: "Total materials required for RES elec + EV batteries Mt"
    Original Eqn:
    Units: Mt/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']


    """
    return (
        total_materials_required_for_ev_batteries()
        + total_materials_required_for_res_elec_mt()
    )


@subs(["materials"], _subscript_dict)
def total_recycled_materials_for_other_mt():
    """
    Real Name: Total recycled materials for other Mt
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']


    """
    return (
        minerals_consumption_estimation_rest_cte_rr()
        - minerals_extraction_projection_rest_with_rr()
    )


@subs(["materials"], _subscript_dict)
def variation_minerals_extraction_rest():
    """
    Real Name: variation minerals extraction Rest
    Original Eqn:
    Units: Mt
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

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
