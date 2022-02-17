"""
Module res_elec_overcap_due_to_res_variabi
Translated using PySD version 2.2.1
"""


def cp_exogenous_res_elec_dispatch_reduction():
    """
    Real Name: Cp exogenous RES elec dispatch reduction
    Original Eqn: MIN(1, -0.6209*(Share variable RES elec generation vs total gen)^2 - 0.3998*(Share variable RES elec generation vs total gen) + 1.0222)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Reduction of the capacity factor of the dispatchable plants as a function
        of the penetration of variables RES in the electricity generation (Source:
        NREL (2012), see MEDEAS D4.1).
    """
    return np.minimum(
        1,
        -0.6209 * (share_variable_res_elec_generation_vs_total_gen()) ** 2
        - 0.3998 * (share_variable_res_elec_generation_vs_total_gen())
        + 1.0222,
    )


@subs(["RES elec"], _subscript_dict)
def cp_exogenous_res_elec_reduction():
    """
    Real Name: Cp exogenous RES elec reduction
    Original Eqn:
      Cp exogenous RES elec dispatch reduction
        .
        .
        .
      Cp exogenous RES elec var reduction
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Reduction of Cp of RES elec due to the penetration of RES elec variables
        (modelling of overcapacities due to the intermittence of RES elec
        variables).
    """
    return xrmerge(
        rearrange(
            cp_exogenous_res_elec_dispatch_reduction(),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            cp_exogenous_res_elec_dispatch_reduction(),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            cp_exogenous_res_elec_dispatch_reduction(),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            cp_exogenous_res_elec_dispatch_reduction(),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            cp_exogenous_res_elec_var_reduction(),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            cp_exogenous_res_elec_var_reduction(),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            cp_exogenous_res_elec_var_reduction(),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            cp_exogenous_res_elec_var_reduction(), ["RES elec"], {"RES elec": ["CSP"]}
        ),
    )


def cp_exogenous_res_elec_var_reduction():
    """
    Real Name: Cp exogenous RES elec var reduction
    Original Eqn: 1/(1+0.0001*EXP(9.85*Share variable RES elec generation vs total gen))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Reduction of the capacity factor of the RES elec variables plants as a
        function of the penetration of variables RES in the electricity generation
        (Source: Delarue & Morris (2015), see MEDEAS D4.1).
    """
    return 1 / (
        1 + 0.0001 * np.exp(9.85 * share_variable_res_elec_generation_vs_total_gen())
    )


def elec_generation_dispatch_from_res_twh():
    """
    Real Name: Elec generation dispatch from RES TWh
    Original Eqn: SUM(real generation RES elec TWh[RES ELEC DISPATCHABLE!])+FES elec from biogas TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Base-load electricity generation from RES.
    """
    return (
        sum(
            rearrange(
                real_generation_res_elec_twh(),
                ["RES ELEC DISPATCHABLE"],
                _subscript_dict,
            ),
            dim=("RES ELEC DISPATCHABLE",),
        )
        + fes_elec_from_biogas_twh()
    )


def elec_generation_variable_from_res_twh():
    """
    Real Name: Elec generation variable from RES TWh
    Original Eqn: SUM(real generation RES elec TWh[RES ELEC VARIABLE!])
    Units: TWh/year
    Limits: (None, None)
    Type: component
    Subs: None

    Variable electricity generation from RES.
    """
    return sum(
        rearrange(
            real_generation_res_elec_twh(), ["RES ELEC VARIABLE"], _subscript_dict
        ),
        dim=("RES ELEC VARIABLE",),
    )


def increase_variable_res_share_elec_vs_total_generation():
    """
    Real Name: increase variable RES share elec vs total generation
    Original Eqn: Share variable RES elec generation vs total-Share variable RES elec vs total generation delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        share_variable_res_elec_generation_vs_total()
        - share_variable_res_elec_vs_total_generation_delayed_1yr()
    )


def initial_share_variable_res_elec_gen_vs_total():
    """
    Real Name: initial share variable RES elec gen vs total
    Original Eqn: 0.0071
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial share of variable RES electricity in relation to the total
        generation.
    """
    return 0.0071


def share_variable_res_elec_generation_vs_total():
    """
    Real Name: Share variable RES elec generation vs total
    Original Eqn: IF THEN ELSE((FE Elec generation from NRE TWh+Elec generation variable from RES TWh+Elec generation dispatch from RES TWh)>0, Elec generation variable from RES TWh/(FE Elec generation from NRE TWh+Elec generation variable from RES TWh+Elec generation dispatch from RES TWh), 0.5)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of variable vs. total electricity generation. Condition to avoid
        error when the denominator is zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        (
            fe_elec_generation_from_nre_twh()
            + elec_generation_variable_from_res_twh()
            + elec_generation_dispatch_from_res_twh()
        )
        > 0,
        lambda: elec_generation_variable_from_res_twh()
        / (
            fe_elec_generation_from_nre_twh()
            + elec_generation_variable_from_res_twh()
            + elec_generation_dispatch_from_res_twh()
        ),
        lambda: 0.5,
    )


def share_variable_res_elec_generation_vs_total_gen():
    """
    Real Name: Share variable RES elec generation vs total gen
    Original Eqn: INTEG ( increase variable RES share elec vs total generation, initial share variable RES elec gen vs total)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share variable RES electricity generation vs total electricity generation.
        Same variable as "share variable RES elec generation vs total" but
        introduced as stock in order to avoid simultaneous equations.
    """
    return _integ_share_variable_res_elec_generation_vs_total_gen()


def share_variable_res_elec_vs_total_generation_delayed_1yr():
    """
    Real Name: Share variable RES elec vs total generation delayed 1yr
    Original Eqn: DELAY FIXED ( Share variable RES elec generation vs total, 1, 0.0071)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    "Share variable RES elec generation vs total" delayed 1 year.
    """
    return _delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr()


_integ_share_variable_res_elec_generation_vs_total_gen = Integ(
    lambda: increase_variable_res_share_elec_vs_total_generation(),
    lambda: initial_share_variable_res_elec_gen_vs_total(),
    "_integ_share_variable_res_elec_generation_vs_total_gen",
)


_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr = DelayFixed(
    lambda: share_variable_res_elec_generation_vs_total(),
    lambda: 1,
    lambda: 0.0071,
    time_step,
    "_delayfixed_share_variable_res_elec_vs_total_generation_delayed_1yr",
)
