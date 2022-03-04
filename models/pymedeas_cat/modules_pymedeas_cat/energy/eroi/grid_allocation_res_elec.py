"""
Module grid_allocation_res_elec
Translated using PySD version 2.2.1
"""


@subs(["RES elec"], _subscript_dict)
def static_eroigrid_res_elec():
    """
    Real Name: "'static' EROIgrid RES elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    System EROI after accounting for the energy losses of electricity storage. Equation from Barnhart et al (2013).
    """
    return if_then_else(
        static_eroi_res_elec() <= 0,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EROI of the aggregated outputs and inputs of RES for generating electricity.
    """
    return zidz(
        sum(
            output_elec_over_lifetime_res_elec_for_allocation2().rename(
                {"RES elec": "RES elec!"}
            ),
            dim=["RES elec!"],
        ),
        sum(
            fei_over_lifetime_res_elec_for_allocation().rename(
                {"RES elec": "RES elec!"}
            ),
            dim=["RES elec!"],
        ),
    )


def static_eroitoteffective_for_allocation_res_elec():
    """
    Real Name: "'static' EROItot-effective for allocation RES elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EROI of the aggregated outputs and inputs of RES for generating electricity.
    """
    return zidz(
        sum(
            output_elec_over_lifetime_res_elec_for_allocation().rename(
                {"RES elec": "RES elec!"}
            ),
            dim=["RES elec!"],
        ),
        sum(
            fei_over_lifetime_res_elec_for_allocation().rename(
                {"RES elec": "RES elec!"}
            ),
            dim=["RES elec!"],
        ),
    )


@subs(["RES elec"], _subscript_dict)
def eroi_allocation_rule_per_res_elec():
    """
    Real Name: EROI allocation rule per RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Allocation rule for the RES elec technologies based on their EROI.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            1, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: if_then_else(
            ratio_eroi_per_techn_vs_eroitot_static() == 0,
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
            lambda: if_then_else(
                ratio_eroi_per_techn_vs_eroitot_static() < 0.1,
                lambda: xr.DataArray(
                    0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
                ),
                lambda: 0.434294 * np.log(ratio_eroi_per_techn_vs_eroitot_static()) + 1,
            ),
        ),
    )


@subs(["RES elec"], _subscript_dict)
def fei_over_lifetime_res_elec_for_allocation():
    """
    Real Name: FEI over lifetime RES elec for allocation
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Final energy investments over lifetime for RES elec technologies. Adapted for allocating technologies.
    """
    return fei_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@subs(["RES elec"], _subscript_dict)
def output_elec_over_lifetime_res_elec_for_allocation():
    """
    Real Name: output elec over lifetime RES elec for allocation
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']


    """
    return output_elec_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@subs(["RES elec"], _subscript_dict)
def output_elec_over_lifetime_res_elec_for_allocation2():
    """
    Real Name: output elec over lifetime RES elec for allocation2
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']


    """
    return xidz(
        static_eroigrid_res_elec(),
        static_eroigrid_toteffective_for_allocation_res_elec(),
        xr.DataArray(0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]),
    )


@subs(["RES elec"], _subscript_dict)
def ratio_eroigrid_vs_eroi_static():
    """
    Real Name: "ratio EROIgrid vs EROI (static)"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']


    """
    return if_then_else(
        static_eroi_res_elec() <= 0,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: static_eroigrid_res_elec() / static_eroi_res_elec(),
    )


@subs(["RES elec"], _subscript_dict)
def remaining_potential_res_elec_switch():
    """
    Real Name: remaining potential RES elec switch
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    This variable detects when a RES elec technology has (almost, 97.5%) reached its full potential so this technology is not taken into account in the estimation of the total EROI aggregated for the calculation of the mix allocation.
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt() < 0.025,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: xr.DataArray(
            1, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@subs(["RES elec"], _subscript_dict)
def share_res_elec_generation_curtailedstored():
    """
    Real Name: "share RES elec generation curtailed&stored"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['RES elec']

    Share of the generation of electricity from RES technologies curtailed or stored.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = 0
    value.loc[{"RES elec": ["geot elec"]}] = 0
    value.loc[{"RES elec": ["solid bioE elec"]}] = 0
    value.loc[{"RES elec": ["oceanic"]}] = 0
    value.loc[{"RES elec": ["wind onshore"]}] = 0.2
    value.loc[{"RES elec": ["wind offshore"]}] = 0.2
    value.loc[{"RES elec": ["solar PV"]}] = 0.2
    value.loc[{"RES elec": ["CSP"]}] = 0.2
    return value
