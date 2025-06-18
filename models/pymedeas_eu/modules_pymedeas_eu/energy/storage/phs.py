"""
Module energy.storage.phs
Translated using PySD version 3.14.2
"""

@component.add(
    name="Cp_PHS",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cp_phs"},
)
def cp_phs():
    """
    Capacity factor of pumped hydro storage (PHS).
    """
    return _ext_constant_cp_phs()


_ext_constant_cp_phs = ExtConstant(
    r"../energy.xlsx", "Europe", "cp_phs", {}, _root, {}, "_ext_constant_cp_phs"
)


@component.add(
    name="initial_instal_cap_PHS",
    units="TW",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_instal_cap_phs"},
)
def initial_instal_cap_phs():
    """
    Installed capacity of PHS in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_phs()


_ext_constant_initial_instal_cap_phs = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "initial_installed_capacity_phs",
    {},
    _root,
    {},
    "_ext_constant_initial_instal_cap_phs",
)


@component.add(
    name="Installed_capacity_PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_phs_policies": 2, "max_potential_phs_twe": 2},
)
def installed_capacity_phs():
    """
    Installed capacity with techno-ecological limitations implemented
    """
    return if_then_else(
        installed_capacity_phs_policies() >= max_potential_phs_twe(),
        lambda: max_potential_phs_twe(),
        lambda: installed_capacity_phs_policies(),
    )


@component.add(
    name="installed_capacity_PHS_policies",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "table_hist_capacity_phs": 3,
        "start_year_p_growth_res_elec": 3,
        "p_phs_power": 2,
    },
)
def installed_capacity_phs_policies():
    return if_then_else(
        time() < end_hist_data(),
        lambda: table_hist_capacity_phs(time()),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: table_hist_capacity_phs(end_hist_data())
            + (
                (
                    p_phs_power(start_year_p_growth_res_elec())
                    - table_hist_capacity_phs(end_hist_data())
                )
                / (start_year_p_growth_res_elec() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: p_phs_power(time()),
        ),
    )


@component.add(
    name="Installed_capacity_PHS_year_delayed",
    units="TW",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_installed_capacity_phs_year_delayed": 1},
    other_deps={
        "_delayfixed_installed_capacity_phs_year_delayed": {
            "initial": {},
            "step": {"installed_capacity_phs": 1},
        }
    },
)
def installed_capacity_phs_year_delayed():
    return _delayfixed_installed_capacity_phs_year_delayed()


_delayfixed_installed_capacity_phs_year_delayed = DelayFixed(
    lambda: installed_capacity_phs(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_installed_capacity_phs_year_delayed",
)


@component.add(
    name="max_capacity_potential_PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_potential_phs_twe": 1, "cp_phs": 1},
)
def max_capacity_potential_phs():
    """
    Maximum capacity potential of PHS.
    """
    return max_potential_phs_twe() / cp_phs()


@component.add(
    name="max_potential_PHS_TWe",
    units="TWe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_potential_phs_twe"},
)
def max_potential_phs_twe():
    """
    Maximum potential for PHS.
    """
    return _ext_constant_max_potential_phs_twe()


_ext_constant_max_potential_phs_twe = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "max_PHS_potential",
    {},
    _root,
    {},
    "_ext_constant_max_potential_phs_twe",
)


@component.add(
    name="max_potential_PHS_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_capacity_potential_phs": 1, "cp_phs": 1, "twe_per_twh": 1},
)
def max_potential_phs_twh():
    return max_capacity_potential_phs() * cp_phs() / twe_per_twh()


@component.add(
    name="new_PHS_installed",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "installed_capacity_phs": 1,
        "installed_capacity_phs_year_delayed": 1,
    },
)
def new_phs_installed():
    return if_then_else(
        time() > 1995,
        lambda: installed_capacity_phs() - installed_capacity_phs_year_delayed(),
        lambda: 0.001,
    )


@component.add(
    name="output_PHS_over_lifetime",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_phs": 1,
        "phs_capacity_under_construction": 1,
        "twe_per_twh": 1,
        "lifetime_res_elec": 1,
        "ej_per_twh": 1,
    },
)
def output_phs_over_lifetime():
    """
    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
    """
    return (
        cp_phs()
        * phs_capacity_under_construction()
        * (1 / twe_per_twh())
        * float(lifetime_res_elec().loc["hydro"])
        * ej_per_twh()
    )


@component.add(
    name="P_PHS_power",
    units="TW",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_p_phs_power",
        "__lookup__": "_ext_lookup_p_phs_power",
    },
)
def p_phs_power(x, final_subs=None):
    return _ext_lookup_p_phs_power(x, final_subs)


_ext_lookup_p_phs_power = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_RES_power",
    "p_PHS_power",
    {},
    _root,
    {},
    "_ext_lookup_p_phs_power",
)


@component.add(
    name="PHS_capacity_under_construction",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "phs_planned_capacity": 1,
        "new_phs_installed": 1,
        "time_construction_res_elec": 1,
    },
)
def phs_capacity_under_construction():
    return (phs_planned_capacity() + new_phs_installed()) / float(
        time_construction_res_elec().loc["hydro"]
    )


@component.add(
    name="PHS_overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fe_elec_stored_phs": 2, "real_fe_elec_stored_phs_twh": 1},
)
def phs_overcapacity():
    return float(
        np.maximum(
            0,
            zidz(
                potential_fe_elec_stored_phs() - real_fe_elec_stored_phs_twh(),
                potential_fe_elec_stored_phs(),
            ),
        )
    )


@component.add(
    name="PHS_planned_capacity",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_phs_planned_capacity": 1},
    other_deps={
        "_integ_phs_planned_capacity": {
            "initial": {},
            "step": {
                "replacement_capacity_phs": 1,
                "phs_capacity_under_construction": 1,
            },
        }
    },
)
def phs_planned_capacity():
    return _integ_phs_planned_capacity()


_integ_phs_planned_capacity = Integ(
    lambda: replacement_capacity_phs() - phs_capacity_under_construction(),
    lambda: 0,
    "_integ_phs_planned_capacity",
)


@component.add(
    name="potential_FE_elec_stored_PHS",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_phs": 1, "cp_phs": 1, "twe_per_twh": 1},
)
def potential_fe_elec_stored_phs():
    return installed_capacity_phs() * cp_phs() / twe_per_twh()


@component.add(
    name="real_FE_elec_stored_PHS_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_potential_phs_twh": 1, "potential_fe_elec_stored_phs": 1},
)
def real_fe_elec_stored_phs_twh():
    """
    Electricity stored in pumped hydro storage plants. It does not add up to the electricity generation of other sources since this electricity has already been accounted for! (stored).
    """
    return float(np.minimum(max_potential_phs_twh(), potential_fe_elec_stored_phs()))


@component.add(
    name="renewed_capacity_PHS_TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_renewed_capacity_phs_tw": 1},
    other_deps={
        "_integ_renewed_capacity_phs_tw": {
            "initial": {"initial_instal_cap_phs": 1},
            "step": {"phs_capacity_under_construction": 1, "wear_phs": 1},
        }
    },
)
def renewed_capacity_phs_tw():
    return _integ_renewed_capacity_phs_tw()


_integ_renewed_capacity_phs_tw = Integ(
    lambda: phs_capacity_under_construction() - wear_phs(),
    lambda: initial_instal_cap_phs(),
    "_integ_renewed_capacity_phs_tw",
)


@component.add(
    name="replacement_capacity_PHS",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "phs_overcapacity": 1, "wear_phs": 1},
)
def replacement_capacity_phs():
    """
    IF THEN ELSE(Time<2015,0,replacement rate PHS*wear PHS*(1-RES elec tot overcapacity))*remaining potential elec storage by RES techn2[RES elec]
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: wear_phs() * (1 - phs_overcapacity())
    )


@component.add(
    name="table_hist_capacity_PHS",
    units="TW",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_hist_capacity_phs",
        "__lookup__": "_ext_lookup_table_hist_capacity_phs",
    },
)
def table_hist_capacity_phs(x, final_subs=None):
    return _ext_lookup_table_hist_capacity_phs(x, final_subs)


_ext_lookup_table_hist_capacity_phs = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_installed_capacity_phs",
    {},
    _root,
    {},
    "_ext_lookup_table_hist_capacity_phs",
)


@component.add(
    name="wear_PHS",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "renewed_capacity_phs_tw": 1, "lifetime_res_elec": 1},
)
def wear_phs():
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: renewed_capacity_phs_tw() / float(lifetime_res_elec().loc["hydro"]),
    )
