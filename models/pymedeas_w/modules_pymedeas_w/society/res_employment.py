"""
Module res_employment
Translated using PySD version 2.2.0
"""


def d_jobs_fuel_supply_solids_bioe():
    """
    Real Name: D jobs fuel supply solids bioE
    Original Eqn: PES solids bioE EJ*Employment factor fuel supply solids bioE*1000
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Direct jobs in fuel supply of solids bioenergy.
    """
    return pes_solids_bioe_ej() * employment_factor_fuel_supply_solids_bioe() * 1000


@subs(["RES elec"], _subscript_dict)
def d_jobs_new_installed_res_elec_per_techn():
    """
    Real Name: D jobs new installed RES elec per techn
    Original Eqn: RES elec capacity under construction TW[RES elec]*Employment factors new RES elec[RES elec]*M per T
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual direct jobs new installed RES elec per technology.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * employment_factors_new_res_elec()
        * m_per_t()
    )


@subs(["RES heat"], _subscript_dict)
def d_jobs_new_installed_res_heat_per_techn():
    """
    Real Name: D jobs new installed RES heat per techn
    Original Eqn: ("new RES capacity for heat-com TW"[RES heat]+"replacement RES for heat-com TW"[RES heat]+"new RES capacity for heat-nc TW"[RES heat]+"replacement RES for heat-nc TW"[RES heat])*Employment factors new RES heat[RES heat]*M per T
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Annual direct jobs new installed RES heat per technology.
    """
    return (
        (
            new_res_capacity_for_heatcom_tw()
            + replacement_res_for_heatcom_tw()
            + new_res_capacity_for_heatnc_tw()
            + replacement_res_for_heatnc_tw()
        )
        * employment_factors_new_res_heat()
        * m_per_t()
    )


def employment_factor_biofuels():
    """
    Real Name: Employment factor biofuels
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factor_biofuels')
    Units: people/EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Employment factor (direct+indirect) biofuels.
    """
    return _ext_constant_employment_factor_biofuels()


def employment_factor_fuel_supply_solids_bioe():
    """
    Real Name: Employment factor fuel supply solids bioE
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factor_fuel_supply_solids_bioe')
    Units: people/EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Employment factor of the direct jobs in fuel supply of solids bioE.
    """
    return _ext_constant_employment_factor_fuel_supply_solids_bioe()


@subs(["RES elec"], _subscript_dict)
def employment_factors_new_res_elec():
    """
    Real Name: Employment factors new RES elec
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factors_new_res_elec*')
    Units: people*year/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Employment factors for the manufacture, construction and installation of
        RES power plants for electricity generation.
    """
    return _ext_constant_employment_factors_new_res_elec()


@subs(["RES heat"], _subscript_dict)
def employment_factors_new_res_heat():
    """
    Real Name: Employment factors new RES heat
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factors_new_res_heat*')
    Units: people*year/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    Employment factors for the manufacture, construction and installation of
        RES power plants for heat generation.
    """
    return _ext_constant_employment_factors_new_res_heat()


@subs(["RES elec"], _subscript_dict)
def employment_factors_om_res_elec():
    """
    Real Name: "Employment factors O&M RES elec"
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factors_o_m_res_elec*')
    Units: people/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Employment factors for the O&M of RES power plants for electricity
        generation.
    """
    return _ext_constant_employment_factors_om_res_elec()


@subs(["RES heat"], _subscript_dict)
def employment_factors_om_res_heat():
    """
    Real Name: "Employment factors O&M RES heat"
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'employment_factors_o_m_res_heat*')
    Units: people/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    Employment factors for the O&M of RES power plants for heat generation.
    """
    return _ext_constant_employment_factors_om_res_heat()


@subs(["RES elec"], _subscript_dict)
def jobs_om_res_elec_per_techn():
    """
    Real Name: "Jobs O&M RES elec per techn"
    Original Eqn: installed capacity RES elec TW[RES elec]*"Employment factors O&M RES elec"[RES elec]*M per T
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual jobs operation&maintenance of RES elec per technology.
    """
    return (
        installed_capacity_res_elec_tw() * employment_factors_om_res_elec() * m_per_t()
    )


@subs(["RES heat"], _subscript_dict)
def jobs_om_res_heat_per_techn():
    """
    Real Name: "Jobs O&M RES heat per techn"
    Original Eqn: ("installed capacity RES heat-com TW"[RES heat]+"installed capacity RES heat-nc TW"[RES heat])*"Employment factors O&M RES heat"[RES heat]*M per T
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Annual jobs operation&maintenance of RES heat per technology.
    """
    return (
        (installed_capacity_res_heatcom_tw() + installed_capacity_res_heatnc_tw())
        * employment_factors_om_res_heat()
        * m_per_t()
    )


@subs(["RES elec"], _subscript_dict)
def ratio_total_vs_d_jobs_res_elec():
    """
    Real Name: Ratio total vs D jobs RES elec
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'ratio_total_vs_direct_jobs_res_elec*')
    Units: people*year/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Ratio total (direct+indirect) vs direct jobs RES elec.
    """
    return _ext_constant_ratio_total_vs_d_jobs_res_elec()


@subs(["RES heat"], _subscript_dict)
def ratio_total_vs_d_jobs_res_heat():
    """
    Real Name: Ratio total vs D jobs RES heat
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'ratio_total_vs_direct_jobs_res_heat*')
    Units: people*year/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    Ratio total (direct+indirect) vs direct jobs RES heat.
    """
    return _ext_constant_ratio_total_vs_d_jobs_res_heat()


@subs(["RES elec"], _subscript_dict)
def total_d_jobs_res_elec_per_techn():
    """
    Real Name: Total D jobs RES elec per techn
    Original Eqn: D jobs new installed RES elec per techn[RES elec]+"Jobs O&M RES elec per techn"[RES elec]
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total direct annual jobs for RES elec per technology.
    """
    return d_jobs_new_installed_res_elec_per_techn() + jobs_om_res_elec_per_techn()


@subs(["RES heat"], _subscript_dict)
def total_d_jobs_res_heat_per_techn():
    """
    Real Name: Total D jobs RES heat per techn
    Original Eqn: D jobs new installed RES heat per techn[RES heat]+"Jobs O&M RES heat per techn"[RES heat]
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Total direct annual jobs for RES heat per technology.
    """
    return d_jobs_new_installed_res_heat_per_techn() + jobs_om_res_heat_per_techn()


@subs(["RES elec"], _subscript_dict)
def total_di_jobs_res_elec_per_techn():
    """
    Real Name: "Total D+I jobs RES elec per techn"
    Original Eqn: Total D jobs RES elec per techn[RES elec]*Ratio total vs D jobs RES elec[RES elec]
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total (direct+indirect) jobs RES elec per technology.
    """
    return total_d_jobs_res_elec_per_techn() * ratio_total_vs_d_jobs_res_elec()


@subs(["RES heat"], _subscript_dict)
def total_di_jobs_res_heat_per_techn():
    """
    Real Name: "Total D+I jobs RES heat per techn"
    Original Eqn: Total D jobs RES heat per techn[RES heat]*Ratio total vs D jobs RES heat[RES heat]
    Units: people
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Total (direct+indirect) jobs RES heat per technology.
    """
    return total_d_jobs_res_heat_per_techn() * ratio_total_vs_d_jobs_res_heat()


def total_jobs_biofuels():
    """
    Real Name: total jobs biofuels
    Original Eqn: Employment factor biofuels*FES total biofuels production EJ
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Total (direct+indirect) jobs biofuels.
    """
    return employment_factor_biofuels() * fes_total_biofuels_production_ej()


def total_jobs_res():
    """
    Real Name: Total jobs RES
    Original Eqn: Total jobs RES elec+Total jobs RES heat+D jobs fuel supply solids bioE+total jobs biofuels
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Total jobs RES.
    """
    return (
        total_jobs_res_elec()
        + total_jobs_res_heat()
        + d_jobs_fuel_supply_solids_bioe()
        + total_jobs_biofuels()
    )


def total_jobs_res_elec():
    """
    Real Name: Total jobs RES elec
    Original Eqn: SUM("Total D+I jobs RES elec per techn"[RES elec!])
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Total jobs RES elec.
    """
    return sum(total_di_jobs_res_elec_per_techn(), dim=("RES elec",))


def total_jobs_res_heat():
    """
    Real Name: Total jobs RES heat
    Original Eqn: SUM("Total D+I jobs RES heat per techn"[RES heat!])
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Total jobs RES heat.
    """
    return sum(total_di_jobs_res_heat_per_techn(), dim=("RES heat",))


_ext_constant_employment_factor_biofuels = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factor_biofuels",
    {},
    _root,
    "_ext_constant_employment_factor_biofuels",
)


_ext_constant_employment_factor_fuel_supply_solids_bioe = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factor_fuel_supply_solids_bioe",
    {},
    _root,
    "_ext_constant_employment_factor_fuel_supply_solids_bioe",
)


_ext_constant_employment_factors_new_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_new_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_employment_factors_new_res_elec",
)


_ext_constant_employment_factors_new_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_new_res_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_employment_factors_new_res_heat",
)


_ext_constant_employment_factors_om_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_o_m_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_employment_factors_om_res_elec",
)


_ext_constant_employment_factors_om_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "employment_factors_o_m_res_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_employment_factors_om_res_heat",
)


_ext_constant_ratio_total_vs_d_jobs_res_elec = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "ratio_total_vs_direct_jobs_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_ratio_total_vs_d_jobs_res_elec",
)


_ext_constant_ratio_total_vs_d_jobs_res_heat = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "ratio_total_vs_direct_jobs_res_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_ratio_total_vs_d_jobs_res_heat",
)
