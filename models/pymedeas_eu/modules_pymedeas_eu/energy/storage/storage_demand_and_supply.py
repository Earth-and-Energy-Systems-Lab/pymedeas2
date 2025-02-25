"""
Module energy.storage.storage_demand_and_supply
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_storage",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_storage_capacity": 2, "total_capacity_elec_storage_tw": 3},
)
def abundance_storage():
    """
    Increases the planning of PHS if there is a deficit of electric storage.
    """
    return 1 - if_then_else(
        demand_storage_capacity() <= total_capacity_elec_storage_tw(),
        lambda: 1,
        lambda: float(
            np.maximum(
                0,
                1
                - (demand_storage_capacity() - total_capacity_elec_storage_tw())
                / total_capacity_elec_storage_tw(),
            )
        ),
    )


@component.add(
    name="constraint_elec_storage_availability",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_variables": 1,
        "demand_storage_capacity": 2,
        "total_capacity_elec_storage_tw": 3,
    },
)
def constraint_elec_storage_availability():
    """
    Remaining potential available as a fraction of unity. This feedback ensures that the electricity storage levels required by the penetration of the RES variables for the generation of electricity are respected.
    """
    return if_then_else(
        res_elec_variables() == 0,
        lambda: xr.DataArray(
            1, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
        lambda: xr.DataArray(
            if_then_else(
                demand_storage_capacity() <= total_capacity_elec_storage_tw(),
                lambda: 1,
                lambda: float(
                    np.maximum(
                        0,
                        1
                        - (demand_storage_capacity() - total_capacity_elec_storage_tw())
                        / total_capacity_elec_storage_tw(),
                    )
                ),
            ),
            {"RES_elec": _subscript_dict["RES_elec"]},
            ["RES_elec"],
        ),
    )


@component.add(
    name="Cp_EV_batteries_for_elec_storage",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_ev_batteries_required": 1,
        "max_cp_ev_batteries_for_elec_storage": 1,
    },
)
def cp_ev_batteries_for_elec_storage():
    """
    Dynamic evolution of the Cp of EV batteries for electricity storage.
    """
    return float(
        np.minimum(cp_ev_batteries_required(), max_cp_ev_batteries_for_elec_storage())
    )


@component.add(
    name="Cp_EV_batteries_required",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_ev_batteries_for_elec_storage": 1, "ev_batteries_tw": 1},
)
def cp_ev_batteries_required():
    return float(
        np.maximum(0, zidz(demand_ev_batteries_for_elec_storage(), ev_batteries_tw()))
    )


@component.add(
    name="demand_EV_batteries_for_elec_storage",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_storage_capacity": 1, "installed_capacity_phs": 1},
)
def demand_ev_batteries_for_elec_storage():
    """
    Demand of EV batteries for storage of electricity.
    """
    return float(np.maximum(0, demand_storage_capacity() - installed_capacity_phs()))


@component.add(
    name="demand_storage_capacity",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_capacity_storageres_elec_var": 1,
        "total_installed_capacity_res_elec_var": 1,
    },
)
def demand_storage_capacity():
    """
    Required storage capacity to install to deal with the variability of RES for electricity.
    """
    return (
        share_capacity_storageres_elec_var() * total_installed_capacity_res_elec_var()
    )


@component.add(
    name="ESOI_elec_storage",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "esoi_phs": 1,
        "installed_capacity_phs": 1,
        "esoi_ev_batteries": 1,
        "used_ev_batteries_for_elec_storage": 1,
        "total_capacity_elec_storage_tw": 1,
    },
)
def esoi_elec_storage():
    """
    ESOI of electric storage (PHS and EV batteries).
    """
    return (
        esoi_phs() * installed_capacity_phs()
        + esoi_ev_batteries() * used_ev_batteries_for_elec_storage()
    ) / total_capacity_elec_storage_tw()


@component.add(
    name="max_capacity_elec_storage",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_capacity_potential_phs": 1,
        "used_ev_batteries_for_elec_storage": 1,
    },
)
def max_capacity_elec_storage():
    """
    Maximum capacity potential of electricity storage (PHS and electric bateries).
    """
    return max_capacity_potential_phs() + used_ev_batteries_for_elec_storage()


@component.add(
    name="real_FE_elec_stored_EV_batteries_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"used_ev_batteries_for_elec_storage": 1, "twe_per_twh": 1},
)
def real_fe_elec_stored_ev_batteries_twh():
    """
    installed capacity PHS TW*Cp PHS/TWe per TWh Electricity stored in EV batteries. It does not add up to the electricity generation of other sources since this electricity has already been accounted for! (stored).
    """
    return used_ev_batteries_for_elec_storage() / twe_per_twh()


@component.add(
    name="remaining_potential_elec_storage_by_RES_techn",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_capacity_elec_storage": 3, "demand_storage_capacity": 2},
)
def remaining_potential_elec_storage_by_res_techn():
    """
    Remaining potential available as a fraction of unity.
    """
    return xr.DataArray(
        if_then_else(
            max_capacity_elec_storage() >= demand_storage_capacity(),
            lambda: (max_capacity_elec_storage() - demand_storage_capacity())
            / max_capacity_elec_storage(),
            lambda: 0,
        ),
        {"RES_elec": _subscript_dict["RES_elec"]},
        ["RES_elec"],
    )


@component.add(
    name="rt_elec_storage_efficiency",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rt_storage_efficiency_phs": 1,
        "installed_capacity_phs": 1,
        "rt_storage_efficiency_ev_batteries": 1,
        "used_ev_batteries_for_elec_storage": 1,
        "total_capacity_elec_storage_tw": 1,
    },
)
def rt_elec_storage_efficiency():
    """
    Round-trip storage efficiency of electric storage (PHS and EV batteries).
    """
    return (
        rt_storage_efficiency_phs() * installed_capacity_phs()
        + rt_storage_efficiency_ev_batteries() * used_ev_batteries_for_elec_storage()
    ) / total_capacity_elec_storage_tw()


@component.add(
    name="rt_storage_efficiency_EV_batteries",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_rt_storage_efficiency_ev_batteries"},
)
def rt_storage_efficiency_ev_batteries():
    """
    Round-trip storage efficiency of electric batteries frome electric vehicles.
    """
    return _ext_constant_rt_storage_efficiency_ev_batteries()


_ext_constant_rt_storage_efficiency_ev_batteries = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "round_trip_storage_efficiency_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_rt_storage_efficiency_ev_batteries",
)


@component.add(
    name="rt_storage_efficiency_PHS",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_rt_storage_efficiency_phs"},
)
def rt_storage_efficiency_phs():
    """
    Round-trip storage efficiency.
    """
    return _ext_constant_rt_storage_efficiency_phs()


_ext_constant_rt_storage_efficiency_phs = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "round_trip_storage_efficiency_phs",
    {},
    _root,
    {},
    "_ext_constant_rt_storage_efficiency_phs",
)


@component.add(
    name='"share_capacity_storage/RES_elec_var"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_elec_demand_covered_by_res": 1},
)
def share_capacity_storageres_elec_var():
    """
    Share installed capacity of storage vs installed capacity of variable RES for electricity. Estimation from NREL (2012).
    """
    return 0.099 + 0.1132 * share_elec_demand_covered_by_res()


@component.add(
    name="Total_capacity_elec_storage_TW",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_phs": 1, "used_ev_batteries_for_elec_storage": 1},
)
def total_capacity_elec_storage_tw():
    """
    Total capacity electricity storage installed.
    """
    return installed_capacity_phs() + used_ev_batteries_for_elec_storage()


@component.add(
    name="Total_installed_capacity_RES_elec_var",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_res_elec": 1},
)
def total_installed_capacity_res_elec_var():
    """
    Total installed capacity of RES variables for electricity generation.
    """
    return sum(
        installed_capacity_res_elec()
        .loc[_subscript_dict["RES_ELEC_VARIABLE"]]
        .rename({"RES_elec": "RES_ELEC_VARIABLE!"}),
        dim=["RES_ELEC_VARIABLE!"],
    )


@component.add(
    name="Used_EV_batteries_for_elec_storage",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ev_batteries_tw": 1, "cp_ev_batteries_for_elec_storage": 1},
)
def used_ev_batteries_for_elec_storage():
    """
    Bateries from electric vehicles used for electric storage.
    """
    return ev_batteries_tw() * cp_ev_batteries_for_elec_storage()
