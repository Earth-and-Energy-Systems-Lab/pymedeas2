"""
Module grid_allocation_res_elec_n
Translated using PySD version 2.1.0
"""


@subs(["RES elec"], _subscript_dict)
def static_eroigrid_res_elec():
    """
    Real Name: "'static' EROIgrid RES elec"
    Original Eqn: IF THEN ELSE("'static' EROI RES elec"[RES elec]<=0,0,(1-"share RES elec generation curtailed&stored"[RES elec]+"share RES elec generation curtailed&stored"[RES elec]*rt elec storage efficiency)/(1/"'static' EROI RES elec"[RES elec]+"share RES elec generation curtailed&stored"[RES elec] *rt elec storage efficiency/ESOI elec storage))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    System EROI after accounting for the energy losses of electricity storage.
        Equation from Barnhart et al (2013).
    """
    return if_then_else(
        static_eroi_res_elec() <= 0,
        lambda: 0,
        lambda: (
            1
            - share_res_elec_generation_curtailedstored()
            + share_res_elec_generation_curtailedstored() * rt_elec_storage_efficiency()
        )
        / (
            1 / static_eroi_res_elec()
            + share_res_elec_generation_curtailedstored()
            * rt_elec_storage_efficiency()
            / esoi_elec_storage()
        ),
    )


def static_eroigrid_toteffective_for_allocation_res_elec():
    """
    Real Name: "'static' EROIgrid tot-effective for allocation RES elec"
    Original Eqn: ZIDZ( SUM(output elec over lifetime RES elec for allocation2[RES elec!]),SUM(FEI over lifetime RES elec for allocation[RES elec!]) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    EROI of the aggregated outputs and inputs of RES for generating
        electricity.
    """
    return zidz(
        sum(output_elec_over_lifetime_res_elec_for_allocation2(), dim=("RES elec",)),
        sum(fei_over_lifetime_res_elec_for_allocation(), dim=("RES elec",)),
    )


def static_eroitoteffective_for_allocation_res_elec():
    """
    Real Name: "'static' EROItot-effective for allocation RES elec"
    Original Eqn: ZIDZ( SUM(output elec over lifetime RES elec for allocation[RES elec!]), SUM(FEI over lifetime RES elec for allocation[RES elec!]) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    EROI of the aggregated outputs and inputs of RES for generating
        electricity.
    """
    return zidz(
        sum(output_elec_over_lifetime_res_elec_for_allocation(), dim=("RES elec",)),
        sum(fei_over_lifetime_res_elec_for_allocation(), dim=("RES elec",)),
    )


@subs(["RES elec"], _subscript_dict)
def eroi_allocation_rule_per_res_elec():
    """
    Real Name: EROI allocation rule per RES elec
    Original Eqn: IF THEN ELSE(Time<2015, 1, IF THEN ELSE("ratio EROI per techn vs EROItot (static)"[RES elec]=0,0, IF THEN ELSE("ratio EROI per techn vs EROItot (static)"[RES elec]<0.1,0, 0.434294*LN("ratio EROI per techn vs EROItot (static)"[RES elec])+1)))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Allocation rule for the RES elec technologies based on their EROI.
    """
    return if_then_else(
        time() < 2015,
        lambda: 1,
        lambda: if_then_else(
            ratio_eroi_per_techn_vs_eroitot_static() == 0,
            lambda: 0,
            lambda: if_then_else(
                ratio_eroi_per_techn_vs_eroitot_static() < 0.1,
                lambda: 0,
                lambda: 0.434294 * np.log(ratio_eroi_per_techn_vs_eroitot_static()) + 1,
            ),
        ),
    )


@subs(["RES elec"], _subscript_dict)
def fei_over_lifetime_res_elec_for_allocation():
    """
    Real Name: FEI over lifetime RES elec for allocation
    Original Eqn: FEI over lifetime RES elec[RES elec]*remaining potential RES elec switch[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Final energy investments over lifetime for RES elec technologies. Adapted
        for allocating technologies.
    """
    return fei_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@subs(["RES elec"], _subscript_dict)
def output_elec_over_lifetime_res_elec_for_allocation():
    """
    Real Name: output elec over lifetime RES elec for allocation
    Original Eqn: output elec over lifetime RES elec[RES elec]*remaining potential RES elec switch[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return output_elec_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@subs(["RES elec"], _subscript_dict)
def output_elec_over_lifetime_res_elec_for_allocation2():
    """
    Real Name: output elec over lifetime RES elec for allocation2
    Original Eqn: "'static' EROIgrid RES elec"[RES elec]*FEI over lifetime RES elec for allocation[RES elec]*"g=quality of electricity"
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return (
        static_eroigrid_res_elec()
        * fei_over_lifetime_res_elec_for_allocation()
        * gquality_of_electricity()
    )


@subs(["RES elec"], _subscript_dict)
def ratio_eroi_per_techn_vs_eroitot_static():
    """
    Real Name: "ratio EROI per techn vs EROItot (static)"
    Original Eqn: XIDZ( "'static' EROIgrid RES elec"[RES elec], "'static' EROIgrid tot-effective for allocation RES elec", 0 )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return xidz(
        static_eroigrid_res_elec(),
        static_eroigrid_toteffective_for_allocation_res_elec(),
        0,
    )


@subs(["RES elec"], _subscript_dict)
def ratio_eroigrid_vs_eroi_static():
    """
    Real Name: "ratio EROIgrid vs EROI (static)"
    Original Eqn: IF THEN ELSE("'static' EROI RES elec"[RES elec]<=0,0,"'static' EROIgrid RES elec"[RES elec]/"'static' EROI RES elec"[RES elec])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return if_then_else(
        static_eroi_res_elec() <= 0,
        lambda: 0,
        lambda: static_eroigrid_res_elec() / static_eroi_res_elec(),
    )


def real_generation_res_elec_var_twh():
    """
    Real Name: real generation RES elec var TWh
    Original Eqn: real generation RES elec TWh[wind onshore]+real generation RES elec TWh[wind offshore]+real generation RES elec TWh[solar PV]+real generation RES elec TWh[CSP]
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(real_generation_res_elec_twh().loc["wind onshore"])
        + float(real_generation_res_elec_twh().loc["wind offshore"])
        + float(real_generation_res_elec_twh().loc["solar PV"])
        + float(real_generation_res_elec_twh().loc["CSP"])
    )


@subs(["RES elec"], _subscript_dict)
def remaining_potential_res_elec_switch():
    """
    Real Name: remaining potential RES elec switch
    Original Eqn: IF THEN ELSE(remaining potential RES elec after intermitt[RES elec]<0.025,0,1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    This variable detects when a RES elec technology has (almost, 97.5%)
        reached its full potential so this technology is not taken into account in
        the estimation of the total EROI aggregated for the calculation of the mix
        allocation.
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt() < 0.025, lambda: 0, lambda: 1
    )


@subs(["RES elec"], _subscript_dict)
def share_res_elec_generation_curtailedstored():
    """
    Real Name: "share RES elec generation curtailed&stored"
    Original Eqn:
      0
        .
        .
        .
      0.2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Share of the generation of electricity from RES technologies curtailed or
        stored.
    """
    return xrmerge(
        xr.DataArray(0, {"RES elec": ["hydro"]}, ["RES elec"]),
        xr.DataArray(0, {"RES elec": ["geot elec"]}, ["RES elec"]),
        xr.DataArray(0, {"RES elec": ["solid bioE elec"]}, ["RES elec"]),
        xr.DataArray(0, {"RES elec": ["oceanic"]}, ["RES elec"]),
        xr.DataArray(0.2, {"RES elec": ["wind onshore"]}, ["RES elec"]),
        xr.DataArray(0.2, {"RES elec": ["wind offshore"]}, ["RES elec"]),
        xr.DataArray(0.2, {"RES elec": ["solar PV"]}, ["RES elec"]),
        xr.DataArray(0.2, {"RES elec": ["CSP"]}, ["RES elec"]),
    )


def share_res_elec_generation_stored_endogenous():
    """
    Real Name: share RES elec generation stored ENDOGENOUS
    Original Eqn: ZIDZ((real FE elec stored EV batteries TWh+real FE elec stored PHS TWh ), real generation RES elec var TWh )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(
        (real_fe_elec_stored_ev_batteries_twh() + real_fe_elec_stored_phs_twh()),
        real_generation_res_elec_var_twh(),
    )
