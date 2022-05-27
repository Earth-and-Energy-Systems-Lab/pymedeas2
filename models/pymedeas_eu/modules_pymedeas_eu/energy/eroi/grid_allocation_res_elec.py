"""
Module grid_allocation_res_elec
Translated using PySD version 3.0.1
"""


@component.add(
    name="\"'static' EROIgrid RES elec\"",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "static_eroi_res_elec": 2,
        "rt_elec_storage_efficiency": 2,
        "share_res_elec_generation_curtailedstored": 3,
        "esoi_elec_storage": 1,
    },
)
def static_eroigrid_res_elec():
    """
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


@component.add(
    name="\"'static' EROIgrid tot-effective for allocation RES elec\"",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "output_elec_over_lifetime_res_elec_for_allocation2": 1,
        "fei_over_lifetime_res_elec_for_allocation": 1,
    },
)
def static_eroigrid_toteffective_for_allocation_res_elec():
    """
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


@component.add(
    name="\"'static' EROItot-effective for allocation RES elec\"",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "output_elec_over_lifetime_res_elec_for_allocation": 1,
        "fei_over_lifetime_res_elec_for_allocation": 1,
    },
)
def static_eroitoteffective_for_allocation_res_elec():
    """
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


@component.add(
    name="EROI allocation rule per RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "ratio_eroi_per_techn_vs_eroitot_static": 3},
)
def eroi_allocation_rule_per_res_elec():
    """
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


@component.add(
    name="FEI over lifetime RES elec for allocation",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fei_over_lifetime_res_elec": 1,
        "remaining_potential_res_elec_switch": 1,
    },
)
def fei_over_lifetime_res_elec_for_allocation():
    """
    Final energy investments over lifetime for RES elec technologies. Adapted for allocating technologies.
    """
    return fei_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@component.add(
    name="output elec over lifetime RES elec for allocation",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "output_elec_over_lifetime_res_elec": 1,
        "remaining_potential_res_elec_switch": 1,
    },
)
def output_elec_over_lifetime_res_elec_for_allocation():
    return output_elec_over_lifetime_res_elec() * remaining_potential_res_elec_switch()


@component.add(
    name="output elec over lifetime RES elec for allocation2",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "static_eroigrid_res_elec": 1,
        "fei_over_lifetime_res_elec_for_allocation": 1,
        "gquality_of_electricity": 1,
    },
)
def output_elec_over_lifetime_res_elec_for_allocation2():
    return (
        static_eroigrid_res_elec()
        * fei_over_lifetime_res_elec_for_allocation()
        * gquality_of_electricity()
    )


@component.add(
    name='"ratio EROI per techn vs EROItot (static)"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "static_eroigrid_res_elec": 1,
        "static_eroigrid_toteffective_for_allocation_res_elec": 1,
    },
)
def ratio_eroi_per_techn_vs_eroitot_static():
    return xidz(
        static_eroigrid_res_elec(),
        xr.DataArray(
            static_eroigrid_toteffective_for_allocation_res_elec(),
            {"RES elec": _subscript_dict["RES elec"]},
            ["RES elec"],
        ),
        0,
    )


@component.add(
    name='"ratio EROIgrid vs EROI (static)"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"static_eroi_res_elec": 2, "static_eroigrid_res_elec": 1},
)
def ratio_eroigrid_vs_eroi_static():
    return if_then_else(
        static_eroi_res_elec() <= 0,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: static_eroigrid_res_elec() / static_eroi_res_elec(),
    )


@component.add(
    name="remaining potential RES elec switch",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"remaining_potential_res_elec_after_intermitt": 1},
)
def remaining_potential_res_elec_switch():
    """
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


@component.add(
    name='"share RES elec generation curtailed&stored"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def share_res_elec_generation_curtailedstored():
    """
    Share of the generation of electricity from RES technologies curtailed or stored.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = 0
    value.loc[["geot elec"]] = 0
    value.loc[["solid bioE elec"]] = 0
    value.loc[["oceanic"]] = 0
    value.loc[["wind onshore"]] = 0.2
    value.loc[["wind offshore"]] = 0.2
    value.loc[["solar PV"]] = 0.2
    value.loc[["CSP"]] = 0.2
    return value
