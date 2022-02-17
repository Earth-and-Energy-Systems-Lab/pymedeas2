"""
Module recycling_and_material_extraction_dem
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def a_lineal_regr_rr_alt_techn():
    """
    Real Name: a lineal regr rr alt techn
    Original Eqn: (P rr minerals alt techn[materials]-current recycling rates minerals alt techn[materials])/(target year P rr minerals -start year P rr minerals)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the recycling rate of each mineral over time ("by mineral rr
        alt technology").
    """
    return (
        p_rr_minerals_alt_techn() - current_recycling_rates_minerals_alt_techn()
    ) / (target_year_p_rr_minerals() - start_year_p_rr_minerals())


@subs(["materials"], _subscript_dict)
def a_lineal_regr_rr_rest():
    """
    Real Name: a lineal regr rr Rest
    Original Eqn: (P rr minerals Rest[materials]-current recycling rates minerals[materials])/(target year P rr minerals -start year P rr minerals)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    a parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the recycling rate of each mineral over time ("by mineral rr
        Rest").
    """
    return (p_rr_minerals_rest() - current_recycling_rates_minerals()) / (
        target_year_p_rr_minerals() - start_year_p_rr_minerals()
    )


def all_minerals_virgin():
    """
    Real Name: "All minerals virgin?"
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0. All minerals are virgin: current and future recycling rates set to 0% (pption to
        compare with results offline MEDEAS).        1. Real share of virgin/recycled minerals (for normal simulations).
    """
    return 1


@subs(["materials"], _subscript_dict)
def b_lineal_regr_rr_alt_techn():
    """
    Real Name: b lineal regr rr alt techn
    Original Eqn: P rr minerals alt techn[materials]-a lineal regr rr alt techn[materials] *target year P rr minerals
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the recycling rate of each mineral over time ("by mineral rr
        alt technology").
    """
    return (
        p_rr_minerals_alt_techn()
        - a_lineal_regr_rr_alt_techn() * target_year_p_rr_minerals()
    )


@subs(["materials"], _subscript_dict)
def b_lineal_regr_rr_rest():
    """
    Real Name: b lineal regr rr Rest
    Original Eqn: P rr minerals Rest[materials]-a lineal regr rr Rest[materials]*target year P rr minerals
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    b parameter of lineal regression "y=a*TIME+b" where y corresponds to the
        evolution of the recycling rate of each mineral over time ("by mineral rr
        Rest").
    """
    return p_rr_minerals_rest() - a_lineal_regr_rr_rest() * target_year_p_rr_minerals()


@subs(["materials"], _subscript_dict)
def by_mineral_rr_alt_techn():
    """
    Real Name: by mineral rr alt techn
    Original Eqn: a lineal regr rr alt techn[materials]*Time+b lineal regr rr alt techn[materials]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates over time by mineral for alternative technologies (RES
        elec & EV batteries).
    """
    return a_lineal_regr_rr_alt_techn() * time() + b_lineal_regr_rr_alt_techn()


@subs(["materials"], _subscript_dict)
def by_mineral_rr_alt_techn_1yr():
    """
    Real Name: by mineral rr alt techn 1yr
    Original Eqn: DELAY FIXED ( by mineral rr alt techn[materials], 1, current recycling rates minerals alt techn[materials])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates over time delayed 1 year by mineral for alternative
        technologies (RES elec & EV batteries).
    """
    return _delayfixed_by_mineral_rr_alt_techn_1yr()


@subs(["materials"], _subscript_dict)
def by_mineral_rr_rest():
    """
    Real Name: by mineral rr Rest
    Original Eqn: a lineal regr rr Rest[materials]*Time+b lineal regr rr Rest[materials]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates over time by mineral for the rest of the economy.
    """
    return a_lineal_regr_rr_rest() * time() + b_lineal_regr_rr_rest()


@subs(["materials"], _subscript_dict)
def by_mineral_rr_rest_1yr():
    """
    Real Name: by mineral rr Rest 1yr
    Original Eqn: DELAY FIXED ( by mineral rr Rest[materials], 1, current recycling rates minerals alt techn[materials])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates over time delayed 1 year by mineral for the rest of the
        economy.
    """
    return _delayfixed_by_mineral_rr_rest_1yr()


@subs(["materials"], _subscript_dict)
def by_mineral_rr_variation_alt_techn():
    """
    Real Name: by mineral rr variation alt techn
    Original Eqn: IF THEN ELSE(Time<2015, Historic improvement recycling rates minerals[materials], IF THEN ELSE(Time<start year P rr minerals, Historic improvement recycling rates minerals[materials], by mineral rr alt techn[materials]-by mineral rr alt techn 1yr[materials] ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Variation of recycling rates per mineral for alternative technologies (RES
        elec & EV batteries).
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: if_then_else(
            time() < start_year_p_rr_minerals(),
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: by_mineral_rr_alt_techn() - by_mineral_rr_alt_techn_1yr(),
        ),
    )


@subs(["materials"], _subscript_dict)
def by_mineral_rr_variation_rest():
    """
    Real Name: by mineral rr variation Rest
    Original Eqn: IF THEN ELSE(Time<2015, Historic improvement recycling rates minerals[materials], IF THEN ELSE(Time<start year P rr minerals, Historic improvement recycling rates minerals[materials], by mineral rr Rest[materials]-by mineral rr Rest 1yr[materials]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Variation of recycling rates per mineral for the rest of the economy.
    """
    return if_then_else(
        time() < 2015,
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: if_then_else(
            time() < start_year_p_rr_minerals(),
            lambda: historic_improvement_recycling_rates_minerals(),
            lambda: by_mineral_rr_rest() - by_mineral_rr_rest_1yr(),
        ),
    )


def choose_targets_mineral_recycling_rates():
    """
    Real Name: choose targets mineral recycling rates
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'choose_targets_mineral_recycling_rates')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1- Disaggregated by mineral.        2- Common annual variation for all minerals.
    """
    return _ext_constant_choose_targets_mineral_recycling_rates()


@subs(["materials"], _subscript_dict)
def common_rr_minerals_variation_alt_techn():
    """
    Real Name: common rr minerals variation alt techn
    Original Eqn: IF THEN ELSE(Time<start year P common rr minerals alt techn, Historic improvement recycling rates minerals[materials], P common rr minerals variation alt techn)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates of minererals (common annual variation).
    """
    return if_then_else(
        time() < start_year_p_common_rr_minerals_alt_techn(),
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: p_common_rr_minerals_variation_alt_techn(),
    )


@subs(["materials"], _subscript_dict)
def common_rr_minerals_variation_rest():
    """
    Real Name: common rr minerals variation Rest
    Original Eqn: IF THEN ELSE(Time<start year P common rr minerals Rest, Historic improvement recycling rates minerals[materials], P common rr minerals variation Rest)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates of minererals (common annual variation).
    """
    return if_then_else(
        time() < start_year_p_common_rr_minerals_rest(),
        lambda: historic_improvement_recycling_rates_minerals(),
        lambda: p_common_rr_minerals_variation_rest(),
    )


@subs(["materials"], _subscript_dict)
def constrain_rr_improv_for_alt_techn_per_mineral():
    """
    Real Name: constrain rr improv for alt techn per mineral
    Original Eqn: IF THEN ELSE(recycling rates minerals alt techn[materials]<Max recycling rates minerals,1,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Constraint recycling rate improvement for alternative technologies (RES
        elec & EV batteries) per material.
    """
    return if_then_else(
        recycling_rates_minerals_alt_techn() < max_recycling_rates_minerals(),
        lambda: 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def constrain_rr_improv_for_rest_per_mineral():
    """
    Real Name: constrain rr improv for Rest per mineral
    Original Eqn: IF THEN ELSE(recycling rates minerals Rest[materials]<Max recycling rates minerals,1,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Remaining recycling rate improvement for the rest of the economy per
        material.
    """
    return if_then_else(
        recycling_rates_minerals_rest() < max_recycling_rates_minerals(),
        lambda: 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def current_recycling_rates_minerals():
    """
    Real Name: current recycling rates minerals
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'current_recycling_rates_minerals*')
    Units: Mt
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Current recycling rates minerals of the whole economy (UNEP, 2011).
    """
    return _ext_constant_current_recycling_rates_minerals()


@subs(["materials"], _subscript_dict)
def current_recycling_rates_minerals_alt_techn():
    """
    Real Name: current recycling rates minerals alt techn
    Original Eqn: current recycling rates minerals[materials]*"EOL-RR minerals alt techn RES vs. total economy"
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Current recycling rates of minerales for alternative technologies. Since
        these technologies are novel and often include materials which are used in
        small quantities in complex products, the recycling rates of the used
        minerals are lower than for the whole economy (following the parameter
        "EOL-RR minerals alt techn RES vs. total economy").
    """
    return (
        current_recycling_rates_minerals()
        * eolrr_minerals_alt_techn_res_vs_total_economy()
    )


def eolrr_minerals_alt_techn_res_vs_total_economy():
    """
    Real Name: "EOL-RR minerals alt techn RES vs. total economy"
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'eol_rr_minerals_alt_techn_res_vs_total_economy')
    Units: Dnml
    Limits: (None, None)
    Type: constant
    Subs: None

    Recycling rate of minerals used in variable RES technologies in relation
        to the total economy. Since these technologies are novel and often include
        materials which are used in small quantities in complex products, the
        recycling rates of the used minerals are lower than for the whole economy.
    """
    return _ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy()


@subs(["materials"], _subscript_dict)
def historic_improvement_recycling_rates_minerals():
    """
    Real Name: Historic improvement recycling rates minerals
    Original Eqn: 0
    Units: percent
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Due to the large uncertainty and slow evolution of these data, historical
        recycling rates minerals correspond with the current estimates (UNEP,
        2011).
    """
    return xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"])


@subs(["materials"], _subscript_dict)
def improvement_recycling_rates_minerals_alt_techn():
    """
    Real Name: improvement recycling rates minerals alt techn
    Original Eqn: IF THEN ELSE(Time<2015, Historic improvement recycling rates minerals[materials], IF THEN ELSE(choose targets mineral recycling rates=2,common rr minerals variation alt techn[materials] *recycling rates minerals alt techn[materials], by mineral rr variation alt techn[materials]))*constrain rr improv for alt techn per mineral[materials]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual improvement of the recycling rates of minerals for alternative
        technologies (RES elec & EV batteries).
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


@subs(["materials"], _subscript_dict)
def improvement_recycling_rates_minerals_rest():
    """
    Real Name: improvement recycling rates minerals Rest
    Original Eqn: IF THEN ELSE(Time<2015, Historic improvement recycling rates minerals[materials], IF THEN ELSE(choose targets mineral recycling rates=2,common rr minerals variation Rest[materials] *recycling rates minerals Rest[materials], by mineral rr variation Rest[materials]))*constrain rr improv for Rest per mineral [materials]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual improvement of the recycling rates of minerals for the rest of the
        economy.
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


def max_recycling_rates_minerals():
    """
    Real Name: Max recycling rates minerals
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'maximum_recycling_rate_minerals')
    Units: Dnml
    Limits: (None, None)
    Type: constant
    Subs: None

    Maximum assumed recycling rate per mineral.
    """
    return _ext_constant_max_recycling_rates_minerals()


def p_common_rr_minerals_variation_alt_techn():
    """
    Real Name: P common rr minerals variation alt techn
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'P_common_rr_minerals_variation_alt_techn')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual recycling rate improvement per mineral for alternative technologies
        (RES elec & EV batteries).
    """
    return _ext_constant_p_common_rr_minerals_variation_alt_techn()


def p_common_rr_minerals_variation_rest():
    """
    Real Name: P common rr minerals variation Rest
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'P_common_rr_minerals_variation_Rest')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual recycling rate improvement per mineral for the rest of the economy.
    """
    return _ext_constant_p_common_rr_minerals_variation_rest()


@subs(["materials"], _subscript_dict)
def p_rr_minerals_alt_techn():
    """
    Real Name: P rr minerals alt techn
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'P_rr_minerals_alt_techn*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Recycling rates by mineral for alternative technologies (RES elec & EV
        batteries) and rest of the economy selected by user by scenario.
    """
    return xrmerge(
        xr.DataArray(
            0, {"materials": _subscript_dict["MATERIALS NO RECYCABLE"]}, ["materials"]
        ),
        _ext_constant_p_rr_minerals_alt_techn(),
    )


@subs(["materials"], _subscript_dict)
def p_rr_minerals_rest():
    """
    Real Name: P rr minerals Rest
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'P_rr_minerals_Rest*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Recycling rates by mineral for alternative technologies (RES elec & EV
        batteries) and rest of the economy selected by user by scenario.
    """
    return xrmerge(
        xr.DataArray(
            0, {"materials": _subscript_dict["MATERIALS NO RECYCABLE"]}, ["materials"]
        ),
        _ext_constant_p_rr_minerals_rest(),
    )


@subs(["materials"], _subscript_dict)
def recycling_rates_minerals_alt_techn():
    """
    Real Name: recycling rates minerals alt techn
    Original Eqn: INTEG ( improvement recycling rates minerals alt techn[materials], current recycling rates minerals alt techn[materials]*"All minerals virgin?")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates minerals of alternative technologies (RES elec & EV
        batteries).
    """
    return _integ_recycling_rates_minerals_alt_techn()


@subs(["materials"], _subscript_dict)
def recycling_rates_minerals_rest():
    """
    Real Name: recycling rates minerals Rest
    Original Eqn: INTEG ( improvement recycling rates minerals Rest[materials], current recycling rates minerals[materials]*"All minerals virgin?")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Recycling rates minerals for the rest of the economy.
    """
    return _integ_recycling_rates_minerals_rest()


def start_year_p_common_rr_minerals_alt_techn():
    """
    Real Name: start year P common rr minerals alt techn
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_P_common_rr_minerals_alt_techn')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of variation recycling rate of minerals for alternative
        technologies (RES elec & EV batteries).
    """
    return _ext_constant_start_year_p_common_rr_minerals_alt_techn()


def start_year_p_common_rr_minerals_rest():
    """
    Real Name: start year P common rr minerals Rest
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_P_common_rr_minerals_Rest')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of variation recycling rate of minerals of the rest of the
        economy.
    """
    return _ext_constant_start_year_p_common_rr_minerals_rest()


def start_year_p_rr_minerals():
    """
    Real Name: start year P rr minerals
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_P_rr_minerals')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of variation recycling rate of minerals for alternative
        technologies (RES elec & EV batteries) and rest of the economy.
    """
    return _ext_constant_start_year_p_rr_minerals()


def target_year_p_rr_minerals():
    """
    Real Name: target year P rr minerals
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'target_year_P_rr_minerals')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year of variation recycling rate of minerals for alternative
        technologies (RES elec & EV batteries) and rest of the economy.
    """
    return _ext_constant_target_year_p_rr_minerals()


_delayfixed_by_mineral_rr_alt_techn_1yr = DelayFixed(
    lambda: by_mineral_rr_alt_techn(),
    lambda: 1,
    lambda: current_recycling_rates_minerals_alt_techn(),
    time_step,
    "_delayfixed_by_mineral_rr_alt_techn_1yr",
)


_delayfixed_by_mineral_rr_rest_1yr = DelayFixed(
    lambda: by_mineral_rr_rest(),
    lambda: 1,
    lambda: current_recycling_rates_minerals_alt_techn(),
    time_step,
    "_delayfixed_by_mineral_rr_rest_1yr",
)


_ext_constant_choose_targets_mineral_recycling_rates = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "choose_targets_mineral_recycling_rates",
    {},
    _root,
    "_ext_constant_choose_targets_mineral_recycling_rates",
)


_ext_constant_current_recycling_rates_minerals = ExtConstant(
    "../materials.xlsx",
    "Global",
    "current_recycling_rates_minerals*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_current_recycling_rates_minerals",
)


_ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "eol_rr_minerals_alt_techn_res_vs_total_economy",
    {},
    _root,
    "_ext_constant_eolrr_minerals_alt_techn_res_vs_total_economy",
)


_ext_constant_max_recycling_rates_minerals = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "maximum_recycling_rate_minerals",
    {},
    _root,
    "_ext_constant_max_recycling_rates_minerals",
)


_ext_constant_p_common_rr_minerals_variation_alt_techn = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "P_common_rr_minerals_variation_alt_techn",
    {},
    _root,
    "_ext_constant_p_common_rr_minerals_variation_alt_techn",
)


_ext_constant_p_common_rr_minerals_variation_rest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "P_common_rr_minerals_variation_Rest",
    {},
    _root,
    "_ext_constant_p_common_rr_minerals_variation_rest",
)


_ext_constant_p_rr_minerals_alt_techn = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "P_rr_minerals_alt_techn*",
    {"materials": _subscript_dict["MATERIALS RECYCABLE"]},
    _root,
    "_ext_constant_p_rr_minerals_alt_techn",
)


_ext_constant_p_rr_minerals_rest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "P_rr_minerals_Rest*",
    {"materials": _subscript_dict["MATERIALS RECYCABLE"]},
    _root,
    "_ext_constant_p_rr_minerals_rest",
)


@subs(["materials"], _subscript_dict)
def _integ_init_recycling_rates_minerals_alt_techn():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for recycling_rates_minerals_alt_techn
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for recycling_rates_minerals_alt_techn function
    """
    return current_recycling_rates_minerals_alt_techn() * all_minerals_virgin()


@subs(["materials"], _subscript_dict)
def _integ_input_recycling_rates_minerals_alt_techn():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for recycling_rates_minerals_alt_techn
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for recycling_rates_minerals_alt_techn function
    """
    return improvement_recycling_rates_minerals_alt_techn()


_integ_recycling_rates_minerals_alt_techn = Integ(
    _integ_input_recycling_rates_minerals_alt_techn,
    _integ_init_recycling_rates_minerals_alt_techn,
    "_integ_recycling_rates_minerals_alt_techn",
)


@subs(["materials"], _subscript_dict)
def _integ_init_recycling_rates_minerals_rest():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for recycling_rates_minerals_rest
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for recycling_rates_minerals_rest function
    """
    return current_recycling_rates_minerals() * all_minerals_virgin()


@subs(["materials"], _subscript_dict)
def _integ_input_recycling_rates_minerals_rest():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for recycling_rates_minerals_rest
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for recycling_rates_minerals_rest function
    """
    return improvement_recycling_rates_minerals_rest()


_integ_recycling_rates_minerals_rest = Integ(
    _integ_input_recycling_rates_minerals_rest,
    _integ_init_recycling_rates_minerals_rest,
    "_integ_recycling_rates_minerals_rest",
)


_ext_constant_start_year_p_common_rr_minerals_alt_techn = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_P_common_rr_minerals_alt_techn",
    {},
    _root,
    "_ext_constant_start_year_p_common_rr_minerals_alt_techn",
)


_ext_constant_start_year_p_common_rr_minerals_rest = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_P_common_rr_minerals_Rest",
    {},
    _root,
    "_ext_constant_start_year_p_common_rr_minerals_rest",
)


_ext_constant_start_year_p_rr_minerals = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_P_rr_minerals",
    {},
    _root,
    "_ext_constant_start_year_p_rr_minerals",
)


_ext_constant_target_year_p_rr_minerals = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_P_rr_minerals",
    {},
    _root,
    "_ext_constant_target_year_p_rr_minerals",
)
