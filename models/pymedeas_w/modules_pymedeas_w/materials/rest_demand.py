"""
Module rest_demand
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def a_extraction_projection_minerals():
    """
    Real Name: "'a' extraction projection minerals"
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'a_extraction_projection_minerals*')
    Units: Mt/year
    Limits: (None, None)
    Type: constant
    Subs: ['materials']


    """
    return _ext_constant_a_extraction_projection_minerals()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_rest():
    """
    Real Name: cum materials to extract Rest
    Original Eqn: INTEG ( Materials to extract Rest Mt[materials], initial cumulated material requirements for Rest 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for the rest of the economy.
    """
    return _integ_cum_materials_to_extract_rest()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_rest_from_2015():
    """
    Real Name: cum materials to extract Rest from 2015
    Original Eqn: INTEG ( Materials to extract Rest from 2015 Mt[materials], initial cumulated material requirements for Rest 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for the rest of the economy from 2015.
    """
    return _integ_cum_materials_to_extract_rest_from_2015()


def historical_extraction_minerals_rest(x):
    """
    Real Name: Historical extraction minerals Rest
    Original Eqn: ( GET DIRECT LOOKUPS('../materials.xlsx', 'Global', 'time', 'historical_extraction_minerals_rest'))
    Units: t
    Limits: (None, None)
    Type: lookup
    Subs: ['materials']

    Historical extraction of minerals of the rest of the economy.
    """
    return _ext_lookup_historical_extraction_minerals_rest(x)


@subs(["materials"], _subscript_dict)
def historical_variation_minerals_extraction_rest():
    """
    Real Name: Historical variation minerals extraction Rest
    Original Eqn: Historical extraction minerals Rest[materials](Time+1)-Historical extraction minerals Rest[materials](Time)
    Units: t
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Historical variation in the extraction of minerals of the rest of the
        economy.
    """
    return historical_extraction_minerals_rest(
        time() + 1
    ) - historical_extraction_minerals_rest(time())


def initial_cumulated_material_requirements_for_rest_1995():
    """
    Real Name: initial cumulated material requirements for Rest 1995
    Original Eqn: 0
    Units: Mt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0


@subs(["materials"], _subscript_dict)
def initial_minerals_extraction_rest():
    """
    Real Name: initial minerals extraction Rest
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'initial_minerals_extraction_rest*')
    Units: t
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Initial minerals extraction of the rest of the economy.
    """
    return _ext_constant_initial_minerals_extraction_rest()


@subs(["materials"], _subscript_dict)
def materials_to_extract_rest_from_2015_mt():
    """
    Real Name: Materials to extract Rest from 2015 Mt
    Original Eqn: IF THEN ELSE(Time<2015,0,Materials to extract Rest Mt[materials])
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual materials to be mined for the ithe rest of the economy from 2015.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: materials_to_extract_rest_mt()
    )


@subs(["materials"], _subscript_dict)
def materials_to_extract_rest_mt():
    """
    Real Name: Materials to extract Rest Mt
    Original Eqn: Minerals extraction projection Rest with rr[materials]
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual materials to be mined for the rest of the economy.
    """
    return minerals_extraction_projection_rest_with_rr()


@subs(["materials"], _subscript_dict)
def minerals_consumption_estimation_rest_cte_rr():
    """
    Real Name: Minerals consumption estimation Rest cte rr
    Original Eqn: Minerals extraction projection Rest cte rr[materials]/(1-current recycling rates minerals[materials])
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Projection of annual mineral consumption of the rest of the economy using
        historical data and assuming recycling rates remaing constant.
    """
    return minerals_extraction_projection_rest_cte_rr() / (
        1 - current_recycling_rates_minerals()
    )


@subs(["materials"], _subscript_dict)
def minerals_extraction_projection_rest_cte_rr():
    """
    Real Name: Minerals extraction projection Rest cte rr
    Original Eqn: INTEG ( variation minerals extraction Rest[materials], initial minerals extraction Rest[materials]*Mt per t)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Projection of annual mineral extraction of the rest of the economy using
        historical data and assuming recycling rates remaing constant.
    """
    return _integ_minerals_extraction_projection_rest_cte_rr()


@subs(["materials"], _subscript_dict)
def minerals_extraction_projection_rest_with_rr():
    """
    Real Name: Minerals extraction projection Rest with rr
    Original Eqn: Minerals consumption estimation Rest cte rr[materials]*(1-recycling rates minerals Rest[materials])
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Minerals extraction projection of the rest of the economy accounting for
        the dynamic evolution of recycling rates.
    """
    return minerals_consumption_estimation_rest_cte_rr() * (
        1 - recycling_rates_minerals_rest()
    )


def mt_per_t():
    """
    Real Name: Mt per t
    Original Eqn: 1e-06
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    megatonne per tonne.
    """
    return 1e-06


@subs(["materials"], _subscript_dict)
def share_minerals_consumption_alt_techn_vs_total_economy():
    """
    Real Name: share minerals consumption alt techn vs total economy
    Original Eqn: ZIDZ( "Total materials required for RES elec + EV batteries Mt"[materials], (Minerals consumption estimation Rest cte rr[materials]+"Total materials required for RES elec + EV batteries Mt"[materials]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']


    """
    return zidz(
        total_materials_required_for_res_elec__ev_batteries_mt(),
        (
            minerals_consumption_estimation_rest_cte_rr()
            + total_materials_required_for_res_elec__ev_batteries_mt()
        ),
    )


@subs(["materials"], _subscript_dict)
def total_materials_required_for_res_elec__ev_batteries_mt():
    """
    Real Name: "Total materials required for RES elec + EV batteries Mt"
    Original Eqn: Total materials required for EV batteries[materials]+Total materials required for RES elec Mt[materials]
    Units: Mt/year
    Limits: (None, None)
    Type: component
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
    Original Eqn: Minerals consumption estimation Rest cte rr[materials]-Minerals extraction projection Rest with rr[materials]
    Units: Mt
    Limits: (None, None)
    Type: component
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
    Original Eqn: IF THEN ELSE(Time<2015,Historical variation minerals extraction Rest[materials], IF THEN ELSE(Minerals extraction projection Rest cte rr[materials]>0.01,("'a' extraction projection minerals"[materials]*(GDP-GDP delayed 1yr)),0))*Mt per t
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Variation of minerals extraction of the rest of the economy.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: historical_variation_minerals_extraction_rest(),
            lambda: if_then_else(
                minerals_extraction_projection_rest_cte_rr() > 0.01,
                lambda: (
                    a_extraction_projection_minerals() * (gdp() - gdp_delayed_1yr())
                ),
                lambda: 0,
            ),
        )
        * mt_per_t()
    )


_ext_constant_a_extraction_projection_minerals = ExtConstant(
    "../materials.xlsx",
    "Global",
    "a_extraction_projection_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_a_extraction_projection_minerals",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_rest():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_rest
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_rest function
    """
    return initial_cumulated_material_requirements_for_rest_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_rest():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_rest
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_rest function
    """
    return materials_to_extract_rest_mt()


_integ_cum_materials_to_extract_rest = Integ(
    _integ_input_cum_materials_to_extract_rest,
    _integ_init_cum_materials_to_extract_rest,
    "_integ_cum_materials_to_extract_rest",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_rest_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_rest_from_2015
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_rest_from_2015 function
    """
    return initial_cumulated_material_requirements_for_rest_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_rest_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_rest_from_2015
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_rest_from_2015 function
    """
    return materials_to_extract_rest_from_2015_mt()


_integ_cum_materials_to_extract_rest_from_2015 = Integ(
    _integ_input_cum_materials_to_extract_rest_from_2015,
    _integ_init_cum_materials_to_extract_rest_from_2015,
    "_integ_cum_materials_to_extract_rest_from_2015",
)


_ext_lookup_historical_extraction_minerals_rest = ExtLookup(
    "../materials.xlsx",
    "Global",
    "time",
    "historical_extraction_minerals_rest",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_lookup_historical_extraction_minerals_rest",
)


_ext_constant_initial_minerals_extraction_rest = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_minerals_extraction_rest*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_initial_minerals_extraction_rest",
)


@subs(["materials"], _subscript_dict)
def _integ_init_minerals_extraction_projection_rest_cte_rr():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for minerals_extraction_projection_rest_cte_rr
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for minerals_extraction_projection_rest_cte_rr function
    """
    return initial_minerals_extraction_rest() * mt_per_t()


@subs(["materials"], _subscript_dict)
def _integ_input_minerals_extraction_projection_rest_cte_rr():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for minerals_extraction_projection_rest_cte_rr
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for minerals_extraction_projection_rest_cte_rr function
    """
    return variation_minerals_extraction_rest()


_integ_minerals_extraction_projection_rest_cte_rr = Integ(
    _integ_input_minerals_extraction_projection_rest_cte_rr,
    _integ_init_minerals_extraction_projection_rest_cte_rr,
    "_integ_minerals_extraction_projection_rest_cte_rr",
)
