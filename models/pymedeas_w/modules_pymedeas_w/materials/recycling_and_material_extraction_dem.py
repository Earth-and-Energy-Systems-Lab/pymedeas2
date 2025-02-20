"""
Module materials.recycling_and_material_extraction_dem
Translated using PySD version 3.14.0
"""

@component.add(
    name="a lineal regr rr alt techn",
    units="1/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_rr_minerals_alt_techn": 1,
        "current_recycling_rates_minerals_alt_techn": 1,
        "start_year_p_rr_minerals": 1,
        "target_year_p_rr_minerals": 1,
    },
)
def a_lineal_regr_rr_alt_techn():
    """
    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the recycling rate of each mineral over time ("by mineral rr alt technology").
    """
    return (
        p_rr_minerals_alt_techn() - current_recycling_rates_minerals_alt_techn()
    ) / (target_year_p_rr_minerals() - start_year_p_rr_minerals())


@component.add(
    name="a lineal regr rr Rest",
    units="1/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_rr_minerals_rest": 1,
        "current_recycling_rates_minerals": 1,
        "start_year_p_rr_minerals": 1,
        "target_year_p_rr_minerals": 1,
    },
)
def a_lineal_regr_rr_rest():
    """
    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the recycling rate of each mineral over time ("by mineral rr Rest").
    """
    return (p_rr_minerals_rest() - current_recycling_rates_minerals()) / (
        target_year_p_rr_minerals() - start_year_p_rr_minerals()
    )


@component.add(
    name='"All minerals virgin?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def all_minerals_virgin():
    """
    0. All minerals are virgin: current and future recycling rates set to 0% (pption to compare with results offline MEDEAS). 1. Real share of virgin/recycled minerals (for normal simulations).
    """
    return 1


@component.add(
    name="b lineal regr rr alt techn",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_rr_minerals_alt_techn": 1,
        "target_year_p_rr_minerals": 1,
        "a_lineal_regr_rr_alt_techn": 1,
    },
)
def b_lineal_regr_rr_alt_techn():
    """
    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the recycling rate of each mineral over time ("by mineral rr alt technology").
    """
    return (
        p_rr_minerals_alt_techn()
        - a_lineal_regr_rr_alt_techn() * target_year_p_rr_minerals()
    )


@component.add(
    name="b lineal regr rr Rest",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_rr_minerals_rest": 1,
        "a_lineal_regr_rr_rest": 1,
        "target_year_p_rr_minerals": 1,
    },
)
def b_lineal_regr_rr_rest():
    """
    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the evolution of the recycling rate of each mineral over time ("by mineral rr Rest").
    """
    return p_rr_minerals_rest() - a_lineal_regr_rr_rest() * target_year_p_rr_minerals()


@component.add(
    name="by mineral rr alt techn",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a_lineal_regr_rr_alt_techn": 1,
        "time": 1,
        "b_lineal_regr_rr_alt_techn": 1,
    },
)
def by_mineral_rr_alt_techn():
    """
    Recycling rates over time by mineral for alternative technologies (RES elec & EV batteries).
    """
    return a_lineal_regr_rr_alt_techn() * time() + b_lineal_regr_rr_alt_techn()


@component.add(
    name="by mineral rr alt techn 1yr",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_by_mineral_rr_alt_techn_1yr": 1},
    other_deps={
        "_delayfixed_by_mineral_rr_alt_techn_1yr": {
            "initial": {"current_recycling_rates_minerals_alt_techn": 1},
            "step": {"by_mineral_rr_alt_techn": 1},
        }
    },
)
def by_mineral_rr_alt_techn_1yr():
    """
    Recycling rates over time delayed 1 year by mineral for alternative technologies (RES elec & EV batteries).
    """
    return _delayfixed_by_mineral_rr_alt_techn_1yr()


_delayfixed_by_mineral_rr_alt_techn_1yr = DelayFixed(
    lambda: by_mineral_rr_alt_techn(),
    lambda: 1,
    lambda: current_recycling_rates_minerals_alt_techn(),
    time_step,
    "_delayfixed_by_mineral_rr_alt_techn_1yr",
)


@component.add(
    name="by mineral rr Rest",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"a_lineal_regr_rr_rest": 1, "time": 1, "b_lineal_regr_rr_rest": 1},
)
def by_mineral_rr_rest():
    """
    Recycling rates over time by mineral for the rest of the economy.
    """
    return a_lineal_regr_rr_rest() * time() + b_lineal_regr_rr_rest()


@component.add(
    name="by mineral rr Rest 1yr",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_by_mineral_rr_rest_1yr": 1},
    other_deps={
        "_delayfixed_by_mineral_rr_rest_1yr": {
            "initial": {"current_recycling_rates_minerals_alt_techn": 1},
            "step": {"by_mineral_rr_rest": 1},
        }
    },
)
def by_mineral_rr_rest_1yr():
    """
    Recycling rates over time delayed 1 year by mineral for the rest of the economy.
    """
    return _delayfixed_by_mineral_rr_rest_1yr()


_delayfixed_by_mineral_rr_rest_1yr = DelayFixed(
    lambda: by_mineral_rr_rest(),
    lambda: 1,
    lambda: current_recycling_rates_minerals_alt_techn(),
    time_step,
    "_delayfixed_by_mineral_rr_rest_1yr",
)


@component.add(
    name="by mineral rr variation alt techn",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_improvement_recycling_rates_minerals": 2,
        "by_mineral_rr_alt_techn": 1,
        "start_year_p_rr_minerals": 1,
        "nvs_1_year": 1,
        "by_mineral_rr_alt_techn_1yr": 1,
    },
)
def by_mineral_rr_variation_alt_techn():
    """
    Variation of recycling rates per mineral for alternative technologies (RES elec & EV batteries).
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: if_then_else(
            time() < start_year_p_rr_minerals(),
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: (by_mineral_rr_alt_techn() - by_mineral_rr_alt_techn_1yr())
            / nvs_1_year(),
        ),
    )


@component.add(
    name="by mineral rr variation Rest",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_improvement_recycling_rates_minerals": 2,
        "by_mineral_rr_rest": 1,
        "start_year_p_rr_minerals": 1,
        "nvs_1_year": 1,
        "by_mineral_rr_rest_1yr": 1,
    },
)
def by_mineral_rr_variation_rest():
    """
    Variation of recycling rates per mineral for the rest of the economy.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: if_then_else(
            time() < start_year_p_rr_minerals(),
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: (by_mineral_rr_rest() - by_mineral_rr_rest_1yr()) / nvs_1_year(),
        ),
    )


@component.add(
    name="choose targets mineral recycling rates",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_targets_mineral_recycling_rates"},
)
def choose_targets_mineral_recycling_rates():
    """
    1- Disaggregated by mineral. 2- Common annual variation for all minerals.
    """
    return _ext_constant_choose_targets_mineral_recycling_rates()


_ext_constant_choose_targets_mineral_recycling_rates = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "choose_targets_mineral_recycling_rates",
    {},
    _root,
    {},
    "_ext_constant_choose_targets_mineral_recycling_rates",
)


@component.add(
    name="common rr minerals variation alt techn",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_year_p_common_rr_minerals_alt_techn": 1,
        "historic_improvement_recycling_rates_minerals": 1,
        "p_common_rr_minerals_variation_alt_techn": 1,
    },
)
def common_rr_minerals_variation_alt_techn():
    """
    Recycling rates of minererals (common annual variation).
    """
    return if_then_else(
        time() < start_year_p_common_rr_minerals_alt_techn(),
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: xr.DataArray(
            p_common_rr_minerals_variation_alt_techn(),
            {"materials": _subscript_dict["materials"]},
            ["materials"],
        ),
    )


@component.add(
    name="common rr minerals variation Rest",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_year_p_common_rr_minerals_rest": 1,
        "historic_improvement_recycling_rates_minerals": 1,
        "p_common_rr_minerals_variation_rest": 1,
    },
)
def common_rr_minerals_variation_rest():
    """
    Recycling rates of minererals (common annual variation).
    """
    return if_then_else(
        time() < start_year_p_common_rr_minerals_rest(),
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: xr.DataArray(
            p_common_rr_minerals_variation_rest(),
            {"materials": _subscript_dict["materials"]},
            ["materials"],
        ),
    )


@component.add(
    name="constrain rr improv for alt techn per mineral",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recycling_rates_minerals_alt_techn": 1,
        "max_recycling_rates_minerals": 1,
    },
)
def constrain_rr_improv_for_alt_techn_per_mineral():
    """
    Constraint recycling rate improvement for alternative technologies (RES elec & EV batteries) per material.
    """
    return if_then_else(
        recycling_rates_minerals_alt_techn() < max_recycling_rates_minerals(),
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name="constrain rr improv for Rest per mineral",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"recycling_rates_minerals_rest": 1, "max_recycling_rates_minerals": 1},
)
def constrain_rr_improv_for_rest_per_mineral():
    """
    Remaining recycling rate improvement for the rest of the economy per material.
    """
    return if_then_else(
        recycling_rates_minerals_rest() < max_recycling_rates_minerals(),
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name="current recycling rates minerals",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_current_recycling_rates_minerals"},
)
def current_recycling_rates_minerals():
    """
    Current recycling rates minerals of the whole economy (UNEP, 2011).
    """
    return _ext_constant_current_recycling_rates_minerals()


_ext_constant_current_recycling_rates_minerals = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_recycling_rates_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_current_recycling_rates_minerals",
)


@component.add(
    name="current recycling rates minerals alt techn",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "current_recycling_rates_minerals": 1,
        "eolrr_minerals_alt_techn_res_vs_total_economy": 1,
    },
)
def current_recycling_rates_minerals_alt_techn():
    """
    Current recycling rates of minerales for alternative technologies. Since these technologies are novel and often include materials which are used in small quantities in complex products, the recycling rates of the used minerals are lower than for the whole economy (following the parameter "EOL-RR minerals alt techn RES vs. total economy").
    """
    return (
        current_recycling_rates_minerals()
        * eolrr_minerals_alt_techn_res_vs_total_economy()
    )


@component.add(
    name='"EOL-RR minerals alt techn RES vs. total economy"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy"
    },
)
def eolrr_minerals_alt_techn_res_vs_total_economy():
    """
    Recycling rate of minerals used in variable RES technologies in relation to the total economy. Since these technologies are novel and often include materials which are used in small quantities in complex products, the recycling rates of the used minerals are lower than for the whole economy.
    """
    return _ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy()


_ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "eol_rr_minerals_alt_techn_res_vs_total_economy",
    {},
    _root,
    {},
    "_ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy",
)


@component.add(
    name="Historic improvement recycling rates minerals",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Constant",
    comp_subtype="Normal",
)
def historic_improvement_recycling_rates_minerals():
    """
    Due to the large uncertainty and slow evolution of these data, historical recycling rates minerals correspond with the current estimates (UNEP, 2011).
    """
    return xr.DataArray(
        0, {"materials": _subscript_dict["materials"]}, [np.str_("materials")]
    )


@component.add(
    name="improvement recycling rates minerals alt techn",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_improvement_recycling_rates_minerals": 1,
        "recycling_rates_minerals_alt_techn": 1,
        "common_rr_minerals_variation_alt_techn": 1,
        "choose_targets_mineral_recycling_rates": 1,
        "by_mineral_rr_variation_alt_techn": 1,
        "constrain_rr_improv_for_alt_techn_per_mineral": 1,
    },
)
def improvement_recycling_rates_minerals_alt_techn():
    """
    Annual improvement of the recycling rates of minerals for alternative technologies (RES elec & EV batteries).
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: if_then_else(
                choose_targets_mineral_recycling_rates() == 2,
                lambda: common_rr_minerals_variation_alt_techn()
                * recycling_rates_minerals_alt_techn(),
                lambda: by_mineral_rr_variation_alt_techn(),
            ),
        )
        * constrain_rr_improv_for_alt_techn_per_mineral()
    )


@component.add(
    name="improvement recycling rates minerals Rest",
    units="Dmnl/year",
    subscripts=[np.str_("materials")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_improvement_recycling_rates_minerals": 1,
        "recycling_rates_minerals_rest": 1,
        "common_rr_minerals_variation_rest": 1,
        "by_mineral_rr_variation_rest": 1,
        "choose_targets_mineral_recycling_rates": 1,
        "constrain_rr_improv_for_rest_per_mineral": 1,
    },
)
def improvement_recycling_rates_minerals_rest():
    """
    Annual improvement of the recycling rates of minerals for the rest of the economy.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: if_then_else(
                choose_targets_mineral_recycling_rates() == 2,
                lambda: common_rr_minerals_variation_rest()
                * recycling_rates_minerals_rest(),
                lambda: by_mineral_rr_variation_rest(),
            ),
        )
        * constrain_rr_improv_for_rest_per_mineral()
    )


@component.add(
    name="Max recycling rates minerals",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_recycling_rates_minerals"},
)
def max_recycling_rates_minerals():
    """
    Maximum assumed recycling rate per mineral.
    """
    return _ext_constant_max_recycling_rates_minerals()


_ext_constant_max_recycling_rates_minerals = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "maximum_recycling_rate_minerals",
    {},
    _root,
    {},
    "_ext_constant_max_recycling_rates_minerals",
)


@component.add(
    name="P common rr minerals variation alt techn",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_p_common_rr_minerals_variation_alt_techn"
    },
)
def p_common_rr_minerals_variation_alt_techn():
    """
    Annual recycling rate improvement per mineral for alternative technologies (RES elec & EV batteries).
    """
    return _ext_constant_p_common_rr_minerals_variation_alt_techn()


_ext_constant_p_common_rr_minerals_variation_alt_techn = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "P_common_rr_minerals_variation_alt_techn",
    {},
    _root,
    {},
    "_ext_constant_p_common_rr_minerals_variation_alt_techn",
)


@component.add(
    name="P common rr minerals variation Rest",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_common_rr_minerals_variation_rest"},
)
def p_common_rr_minerals_variation_rest():
    """
    Annual recycling rate improvement per mineral for the rest of the economy.
    """
    return _ext_constant_p_common_rr_minerals_variation_rest()


_ext_constant_p_common_rr_minerals_variation_rest = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "P_common_rr_minerals_variation_Rest",
    {},
    _root,
    {},
    "_ext_constant_p_common_rr_minerals_variation_rest",
)


@component.add(
    name="P rr minerals alt techn",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External, Normal",
    depends_on={"__external__": "_ext_constant_p_rr_minerals_alt_techn"},
)
def p_rr_minerals_alt_techn():
    """
    Recycling rates by mineral for alternative technologies (RES elec & EV batteries) and rest of the economy selected by user by scenario.
    """
    value = xr.DataArray(
        np.nan, {"materials": _subscript_dict["materials"]}, ["materials"]
    )
    value.loc[_subscript_dict["MATERIALS NO RECYCABLE"]] = 0
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[
        [
            "Aluminium",
            "Cadmium",
            "Chromium",
            "Copper",
            "Galium",
            "Indium",
            "Iron",
            "Lithium",
            "Magnesium",
            "Manganese",
            "Molybdenum",
            "Nickel",
            "Lead",
            "Silver",
            "Tin",
            "tellurium",
            "titanium",
            "vanadium",
            "zinc",
        ]
    ] = True
    value.values[def_subs.values] = _ext_constant_p_rr_minerals_alt_techn().values[
        def_subs.values
    ]
    return value


_ext_constant_p_rr_minerals_alt_techn = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "P_rr_minerals_alt_techn*",
    {"materials": _subscript_dict["MATERIALS RECYCABLE"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_p_rr_minerals_alt_techn",
)


@component.add(
    name="P rr minerals Rest",
    units="Dmnl",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External, Normal",
    depends_on={"__external__": "_ext_constant_p_rr_minerals_rest"},
)
def p_rr_minerals_rest():
    """
    Recycling rates by mineral for alternative technologies (RES elec & EV batteries) and rest of the economy selected by user by scenario.
    """
    value = xr.DataArray(
        np.nan, {"materials": _subscript_dict["materials"]}, ["materials"]
    )
    value.loc[_subscript_dict["MATERIALS NO RECYCABLE"]] = 0
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[
        [
            "Aluminium",
            "Cadmium",
            "Chromium",
            "Copper",
            "Galium",
            "Indium",
            "Iron",
            "Lithium",
            "Magnesium",
            "Manganese",
            "Molybdenum",
            "Nickel",
            "Lead",
            "Silver",
            "Tin",
            "tellurium",
            "titanium",
            "vanadium",
            "zinc",
        ]
    ] = True
    value.values[def_subs.values] = _ext_constant_p_rr_minerals_rest().values[
        def_subs.values
    ]
    return value


_ext_constant_p_rr_minerals_rest = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "P_rr_minerals_Rest*",
    {"materials": _subscript_dict["MATERIALS RECYCABLE"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_p_rr_minerals_rest",
)


@component.add(
    name="recycling rates minerals alt techn",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_recycling_rates_minerals_alt_techn": 1},
    other_deps={
        "_integ_recycling_rates_minerals_alt_techn": {
            "initial": {
                "current_recycling_rates_minerals_alt_techn": 1,
                "all_minerals_virgin": 1,
            },
            "step": {"improvement_recycling_rates_minerals_alt_techn": 1},
        }
    },
)
def recycling_rates_minerals_alt_techn():
    """
    Recycling rates minerals of alternative technologies (RES elec & EV batteries).
    """
    return _integ_recycling_rates_minerals_alt_techn()


_integ_recycling_rates_minerals_alt_techn = Integ(
    lambda: improvement_recycling_rates_minerals_alt_techn(),
    lambda: current_recycling_rates_minerals_alt_techn() * all_minerals_virgin(),
    "_integ_recycling_rates_minerals_alt_techn",
)


@component.add(
    name="recycling rates minerals Rest",
    units="Dmnl",
    subscripts=[np.str_("materials")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_recycling_rates_minerals_rest": 1},
    other_deps={
        "_integ_recycling_rates_minerals_rest": {
            "initial": {
                "current_recycling_rates_minerals": 1,
                "all_minerals_virgin": 1,
            },
            "step": {"improvement_recycling_rates_minerals_rest": 1},
        }
    },
)
def recycling_rates_minerals_rest():
    """
    Recycling rates minerals for the rest of the economy.
    """
    return _integ_recycling_rates_minerals_rest()


_integ_recycling_rates_minerals_rest = Integ(
    lambda: improvement_recycling_rates_minerals_rest(),
    lambda: current_recycling_rates_minerals() * all_minerals_virgin(),
    "_integ_recycling_rates_minerals_rest",
)


@component.add(
    name="start year P common rr minerals alt techn",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_p_common_rr_minerals_alt_techn"
    },
)
def start_year_p_common_rr_minerals_alt_techn():
    """
    Start year of variation recycling rate of minerals for alternative technologies (RES elec & EV batteries).
    """
    return _ext_constant_start_year_p_common_rr_minerals_alt_techn()


_ext_constant_start_year_p_common_rr_minerals_alt_techn = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_P_common_rr_minerals_alt_techn",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_common_rr_minerals_alt_techn",
)


@component.add(
    name="start year P common rr minerals Rest",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_common_rr_minerals_rest"},
)
def start_year_p_common_rr_minerals_rest():
    """
    Start year of variation recycling rate of minerals of the rest of the economy.
    """
    return _ext_constant_start_year_p_common_rr_minerals_rest()


_ext_constant_start_year_p_common_rr_minerals_rest = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_P_common_rr_minerals_Rest",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_common_rr_minerals_rest",
)


@component.add(
    name="start year P rr minerals",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_rr_minerals"},
)
def start_year_p_rr_minerals():
    """
    Start year of variation recycling rate of minerals for alternative technologies (RES elec & EV batteries) and rest of the economy.
    """
    return _ext_constant_start_year_p_rr_minerals()


_ext_constant_start_year_p_rr_minerals = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_P_rr_minerals",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_rr_minerals",
)


@component.add(
    name="target year P rr minerals",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_target_year_p_rr_minerals"},
)
def target_year_p_rr_minerals():
    """
    Target year of variation recycling rate of minerals for alternative technologies (RES elec & EV batteries) and rest of the economy.
    """
    return _ext_constant_target_year_p_rr_minerals()


_ext_constant_target_year_p_rr_minerals = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "target_year_P_rr_minerals",
    {},
    _root,
    {},
    "_ext_constant_target_year_p_rr_minerals",
)
