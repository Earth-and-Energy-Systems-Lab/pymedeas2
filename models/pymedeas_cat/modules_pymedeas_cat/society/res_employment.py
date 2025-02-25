"""
Module society.res_employment
Translated using PySD version 3.14.0
"""

@component.add(
    name="D_jobs_fuel_supply_solids_bioE",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_solids_bioe_ej": 1,
        "employment_factor_fuel_supply_solids_bioe": 1,
    },
)
def d_jobs_fuel_supply_solids_bioe():
    """
    Direct jobs in fuel supply of solids bioenergy.
    """
    return np.maximum(
        0, pes_solids_bioe_ej() * employment_factor_fuel_supply_solids_bioe() * 1000
    )


@component.add(
    name="D_jobs_new_installed_RES_elec_per_techn",
    units="people/year",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_capacity_under_construction_tw": 1,
        "employment_factors_new_res_elec": 1,
        "mw_per_tw": 1,
    },
)
def d_jobs_new_installed_res_elec_per_techn():
    """
    Annual direct jobs new installed RES elec per technology.
    """
    return np.maximum(
        0,
        res_elec_capacity_under_construction_tw()
        * employment_factors_new_res_elec()
        * mw_per_tw(),
    )


@component.add(
    name="D_jobs_new_installed_RES_heat_per_techn",
    units="people/year",
    subscripts=[np.str_("RES_heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_res_capacity_for_heatcom_tw": 1,
        "replacement_res_for_heatcom_tw": 1,
        "new_res_capacity_for_heatnc_tw": 1,
        "replacement_res_for_heatnc_tw": 1,
        "employment_factors_new_res_heat": 1,
        "mw_per_tw": 1,
    },
)
def d_jobs_new_installed_res_heat_per_techn():
    """
    Annual direct jobs new installed RES heat per technology.
    """
    return np.maximum(
        0,
        (
            new_res_capacity_for_heatcom_tw()
            + replacement_res_for_heatcom_tw()
            + new_res_capacity_for_heatnc_tw()
            + replacement_res_for_heatnc_tw()
        )
        * employment_factors_new_res_heat()
        * mw_per_tw(),
    )


@component.add(
    name="Employment_factor_biofuels",
    units="people/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_employment_factor_biofuels"},
)
def employment_factor_biofuels():
    """
    Employment factor (direct+indirect) biofuels.
    """
    return _ext_constant_employment_factor_biofuels()


_ext_constant_employment_factor_biofuels = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factor_biofuels",
    {},
    _root,
    {},
    "_ext_constant_employment_factor_biofuels",
)


@component.add(
    name="Employment_factor_fuel_supply_solids_bioE",
    units="people/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_employment_factor_fuel_supply_solids_bioe"
    },
)
def employment_factor_fuel_supply_solids_bioe():
    """
    Employment factor of the direct jobs in fuel supply of solids bioE.
    """
    return _ext_constant_employment_factor_fuel_supply_solids_bioe()


_ext_constant_employment_factor_fuel_supply_solids_bioe = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factor_fuel_supply_solids_bioe",
    {},
    _root,
    {},
    "_ext_constant_employment_factor_fuel_supply_solids_bioe",
)


@component.add(
    name="Employment_factors_new_RES_elec",
    units="people/MW",
    subscripts=[np.str_("RES_elec")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_employment_factors_new_res_elec"},
)
def employment_factors_new_res_elec():
    """
    Employment factors for the manufacture, construction and installation of RES power plants for electricity generation.
    """
    return _ext_constant_employment_factors_new_res_elec()


_ext_constant_employment_factors_new_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_new_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_employment_factors_new_res_elec",
)


@component.add(
    name="Employment_factors_new_RES_heat",
    units="people/MW",
    subscripts=[np.str_("RES_heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_employment_factors_new_res_heat"},
)
def employment_factors_new_res_heat():
    """
    Employment factors for the manufacture, construction and installation of RES power plants for heat generation.
    """
    return _ext_constant_employment_factors_new_res_heat()


_ext_constant_employment_factors_new_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_new_res_heat*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_employment_factors_new_res_heat",
)


@component.add(
    name='"Employment_factors_O&M_RES_elec"',
    units="people/(year*MW)",
    subscripts=[np.str_("RES_elec")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_employment_factors_om_res_elec"},
)
def employment_factors_om_res_elec():
    """
    Employment factors for the O&M of RES power plants for electricity generation.
    """
    return _ext_constant_employment_factors_om_res_elec()


_ext_constant_employment_factors_om_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_o_m_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_employment_factors_om_res_elec",
)


@component.add(
    name='"Employment_factors_O&M_RES_heat"',
    units="people/(year*MW)",
    subscripts=[np.str_("RES_heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_employment_factors_om_res_heat"},
)
def employment_factors_om_res_heat():
    """
    Employment factors for the O&M of RES power plants for heat generation.
    """
    return _ext_constant_employment_factors_om_res_heat()


_ext_constant_employment_factors_om_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_o_m_res_heat*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_employment_factors_om_res_heat",
)


@component.add(
    name='"Jobs_O&M_RES_elec_per_techn"',
    units="people/year",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec": 1,
        "employment_factors_om_res_elec": 1,
        "mw_per_tw": 1,
    },
)
def jobs_om_res_elec_per_techn():
    """
    Annual jobs operation&maintenance of RES elec per technology.
    """
    return np.maximum(
        0,
        installed_capacity_res_elec() * employment_factors_om_res_elec() * mw_per_tw(),
    )


@component.add(
    name='"Jobs_O&M_RES_heat_per_techn"',
    units="people/year",
    subscripts=[np.str_("RES_heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_heatcom_tw": 1,
        "installed_capacity_res_heatnc_tw": 1,
        "employment_factors_om_res_heat": 1,
        "mw_per_tw": 1,
    },
)
def jobs_om_res_heat_per_techn():
    """
    Annual jobs operation&maintenance of RES heat per technology.
    """
    return np.maximum(
        0,
        (installed_capacity_res_heatcom_tw() + installed_capacity_res_heatnc_tw())
        * employment_factors_om_res_heat()
        * mw_per_tw(),
    )


@component.add(
    name="Ratio_total_vs_D_jobs_RES_elec",
    units="Dmnl",
    subscripts=[np.str_("RES_elec")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ratio_total_vs_d_jobs_res_elec"},
)
def ratio_total_vs_d_jobs_res_elec():
    """
    Ratio total (direct+indirect) vs direct jobs RES elec.
    """
    return _ext_constant_ratio_total_vs_d_jobs_res_elec()


_ext_constant_ratio_total_vs_d_jobs_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "ratio_total_vs_direct_jobs_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_ratio_total_vs_d_jobs_res_elec",
)


@component.add(
    name="Ratio_total_vs_D_jobs_RES_heat",
    units="Dmnl",
    subscripts=[np.str_("RES_heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ratio_total_vs_d_jobs_res_heat"},
)
def ratio_total_vs_d_jobs_res_heat():
    """
    Ratio total (direct+indirect) vs direct jobs RES heat.
    """
    return _ext_constant_ratio_total_vs_d_jobs_res_heat()


_ext_constant_ratio_total_vs_d_jobs_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "ratio_total_vs_direct_jobs_res_heat*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_ratio_total_vs_d_jobs_res_heat",
)


@component.add(
    name="Total_D_jobs_RES_elec_per_techn",
    units="people/year",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "d_jobs_new_installed_res_elec_per_techn": 1,
        "jobs_om_res_elec_per_techn": 1,
    },
)
def total_d_jobs_res_elec_per_techn():
    """
    Total direct annual jobs for RES elec per technology.
    """
    return d_jobs_new_installed_res_elec_per_techn() + jobs_om_res_elec_per_techn()


@component.add(
    name="Total_D_jobs_RES_heat_per_techn",
    units="people/year",
    subscripts=[np.str_("RES_heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "d_jobs_new_installed_res_heat_per_techn": 1,
        "jobs_om_res_heat_per_techn": 1,
    },
)
def total_d_jobs_res_heat_per_techn():
    """
    Total direct annual jobs for RES heat per technology.
    """
    return d_jobs_new_installed_res_heat_per_techn() + jobs_om_res_heat_per_techn()


@component.add(
    name='"Total_D+I_jobs_RES_elec_per_techn"',
    units="people/year",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_d_jobs_res_elec_per_techn": 1,
        "ratio_total_vs_d_jobs_res_elec": 1,
    },
)
def total_di_jobs_res_elec_per_techn():
    """
    Total (direct+indirect) jobs RES elec per technology.
    """
    return total_d_jobs_res_elec_per_techn() * ratio_total_vs_d_jobs_res_elec()


@component.add(
    name='"Total_D+I_jobs_RES_heat_per_techn"',
    units="people/year",
    subscripts=[np.str_("RES_heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_d_jobs_res_heat_per_techn": 1,
        "ratio_total_vs_d_jobs_res_heat": 1,
    },
)
def total_di_jobs_res_heat_per_techn():
    """
    Total (direct+indirect) jobs RES heat per technology.
    """
    return total_d_jobs_res_heat_per_techn() * ratio_total_vs_d_jobs_res_heat()


@component.add(
    name="total_jobs_biofuels",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"employment_factor_biofuels": 1, "fes_total_biofuels_ej": 1},
)
def total_jobs_biofuels():
    """
    Total (direct+indirect) jobs biofuels.
    """
    return employment_factor_biofuels() * fes_total_biofuels_ej()


@component.add(
    name="Total_jobs_RES",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_jobs_res_elec": 1,
        "total_jobs_res_heat": 1,
        "d_jobs_fuel_supply_solids_bioe": 1,
        "total_jobs_biofuels": 1,
    },
)
def total_jobs_res():
    """
    Total jobs RES.
    """
    return (
        total_jobs_res_elec()
        + total_jobs_res_heat()
        + d_jobs_fuel_supply_solids_bioe()
        + total_jobs_biofuels()
    )


@component.add(
    name="Total_jobs_RES_elec",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_di_jobs_res_elec_per_techn": 1},
)
def total_jobs_res_elec():
    """
    Total jobs RES elec.
    """
    return sum(
        total_di_jobs_res_elec_per_techn().rename({np.str_("RES_elec"): "RES_elec!"}),
        dim=["RES_elec!"],
    )


@component.add(
    name="Total_jobs_RES_heat",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_di_jobs_res_heat_per_techn": 1},
)
def total_jobs_res_heat():
    """
    Total jobs RES heat.
    """
    return sum(
        total_di_jobs_res_heat_per_techn().rename({np.str_("RES_heat"): "RES_heat!"}),
        dim=["RES_heat!"],
    )
