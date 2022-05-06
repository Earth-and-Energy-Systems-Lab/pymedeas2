"""
Module res_elec_overcap_due_to_res_variabi
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="Cp exogenous RES elec reduction",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_exogenous_res_elec_dispatch_reduction": 4,
        "cp_exogenous_res_elec_var_reduction": 4,
    },
)
def cp_exogenous_res_elec_reduction():
    """
    Reduction of Cp of RES elec due to the penetration of RES elec variables (modelling of overcapacities due to the intermittence of RES elec variables).
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = cp_exogenous_res_elec_dispatch_reduction()
    value.loc[["geot elec"]] = cp_exogenous_res_elec_dispatch_reduction()
    value.loc[["solid bioE elec"]] = cp_exogenous_res_elec_dispatch_reduction()
    value.loc[["oceanic"]] = cp_exogenous_res_elec_dispatch_reduction()
    value.loc[["wind onshore"]] = cp_exogenous_res_elec_var_reduction()
    value.loc[["wind offshore"]] = cp_exogenous_res_elec_var_reduction()
    value.loc[["solar PV"]] = cp_exogenous_res_elec_var_reduction()
    value.loc[["CSP"]] = cp_exogenous_res_elec_var_reduction()
    return value


@component.add(
    name="Cp exogenous RES elec dispatch reduction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_variable_res_elec_generation_vs_total_gen": 2},
)
def cp_exogenous_res_elec_dispatch_reduction():
    """
    Reduction of the capacity factor of the dispatchable plants as a function of the penetration of variables RES in the electricity generation (Source: NREL (2012), see MEDEAS D4.1).
    """
    return np.minimum(
        1,
        -0.6209 * share_variable_res_elec_generation_vs_total_gen() ** 2
        - 0.3998 * share_variable_res_elec_generation_vs_total_gen()
        + 1.0222,
    )


@component.add(
    name="Cp exogenous RES elec var reduction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_variable_res_elec_generation_vs_total_gen": 1},
)
def cp_exogenous_res_elec_var_reduction():
    """
    Reduction of the capacity factor of the RES elec variables plants as a function of the penetration of variables RES in the electricity generation (Source: Delarue & Morris (2015), see MEDEAS D4.1).
    """
    return 1 / (
        1 + 0.0001 * np.exp(9.85 * share_variable_res_elec_generation_vs_total_gen())
    )


@component.add(
    name="Elec generation dispatch from RES TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_generation_res_elec_twh": 1, "fes_elec_from_biogas_twh": 1},
)
def elec_generation_dispatch_from_res_twh():
    """
    Base-load electricity generation from RES.
    """
    return (
        sum(
            real_generation_res_elec_twh()
            .loc[_subscript_dict["RES ELEC DISPATCHABLE"]]
            .rename({"RES elec": "RES ELEC DISPATCHABLE!"}),
            dim=["RES ELEC DISPATCHABLE!"],
        )
        + fes_elec_from_biogas_twh()
    )


@component.add(
    name="Elec generation variable from RES TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_generation_res_elec_twh": 1},
)
def elec_generation_variable_from_res_twh():
    """
    Variable electricity generation from RES.
    """
    return sum(
        real_generation_res_elec_twh()
        .loc[_subscript_dict["RES ELEC VARIABLE"]]
        .rename({"RES elec": "RES ELEC VARIABLE!"}),
        dim=["RES ELEC VARIABLE!"],
    )


@component.add(
    name="increase variable RES share elec vs total generation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_variable_res_elec_generation_vs_total": 1,
        "share_variable_res_elec_vs_total_generation_delayed_1yr": 1,
    },
)
def increase_variable_res_share_elec_vs_total_generation():
    return (
        share_variable_res_elec_generation_vs_total()
        - share_variable_res_elec_vs_total_generation_delayed_1yr()
    )


@component.add(
    name="initial share variable RES elec gen vs total",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_share_variable_res_elec_gen_vs_total():
    """
    Initial share of variable RES electricity in relation to the total generation.
    """
    return 0.0071


@component.add(
    name="Share variable RES elec generation vs total",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_nre_twh": 2,
        "elec_generation_variable_from_res_twh": 3,
        "elec_generation_dispatch_from_res_twh": 2,
    },
)
def share_variable_res_elec_generation_vs_total():
    """
    Share of variable vs. total electricity generation. Condition to avoid error when the denominator is zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        fe_elec_generation_from_nre_twh()
        + elec_generation_variable_from_res_twh()
        + elec_generation_dispatch_from_res_twh()
        > 0,
        lambda: elec_generation_variable_from_res_twh()
        / (
            fe_elec_generation_from_nre_twh()
            + elec_generation_variable_from_res_twh()
            + elec_generation_dispatch_from_res_twh()
        ),
        lambda: 0.5,
    )


@component.add(
    name="Share variable RES elec generation vs total gen",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_share_variable_res_elec_generation_vs_total_gen": 1},
    other_deps={
        "_integ_share_variable_res_elec_generation_vs_total_gen": {
            "initial": {"initial_share_variable_res_elec_gen_vs_total": 1},
            "step": {"increase_variable_res_share_elec_vs_total_generation": 1},
        }
    },
)
def share_variable_res_elec_generation_vs_total_gen():
    """
    Share variable RES electricity generation vs total electricity generation. Same variable as "share variable RES elec generation vs total" but introduced as stock in order to avoid simultaneous equations.
    """
    return _integ_share_variable_res_elec_generation_vs_total_gen()


_integ_share_variable_res_elec_generation_vs_total_gen = Integ(
    lambda: increase_variable_res_share_elec_vs_total_generation(),
    lambda: initial_share_variable_res_elec_gen_vs_total(),
    "_integ_share_variable_res_elec_generation_vs_total_gen",
)


@component.add(
    name="Share variable RES elec vs total generation delayed 1yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={
        "_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr": 1
    },
    other_deps={
        "_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr": {
            "initial": {},
            "step": {"share_variable_res_elec_generation_vs_total": 1},
        }
    },
)
def share_variable_res_elec_vs_total_generation_delayed_1yr():
    """
    "Share variable RES elec generation vs total" delayed 1 year.
    """
    return _delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr()


_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr = DelayFixed(
    lambda: share_variable_res_elec_generation_vs_total(),
    lambda: 1,
    lambda: 0.0071,
    time_step,
    "_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr",
)
