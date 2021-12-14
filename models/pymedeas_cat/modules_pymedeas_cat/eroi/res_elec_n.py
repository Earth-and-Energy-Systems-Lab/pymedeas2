"""
Module res_elec_n
Translated using PySD version 2.1.0
"""


@subs(["RES elec"], _subscript_dict)
def dynamic_eroi_res_elec_var():
    """
    Real Name: "'dynamic' EROI RES elec var"
    Original Eqn: IF THEN ELSE(FEI RES elec var[RES elec]=0, 0, real generation RES elec EJ[RES elec]/FEI RES elec var [RES elec])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Evolution of EROI over time per RES variable technology, considering CED
        dynamic over time.
    """
    return if_then_else(
        fei_res_elec_var() == 0,
        lambda: 0,
        lambda: real_generation_res_elec_ej() / fei_res_elec_var(),
    )


@subs(["RES elec"], _subscript_dict)
def static_eroi_res_elec():
    """
    Real Name: "'static' EROI RES elec"
    Original Eqn:
      IF THEN ELSE(FEI over lifetime RES elec dispatch[hydro]=0,0,output elec over lifetime RES elec[hydro]/(FEI over lifetime RES elec dispatch[hydro]*"g=quality of electricity"))
        .
        .
        .
      IF THEN ELSE(FEI over lifetime RES elec var[CSP]=0,0,output elec over lifetime RES elec[CSP]/FEI over lifetime RES elec var[CSP])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Energy return on energy invested (over the full lifetime of the
        infrastructure) per RES technology for generating electricity.
    """
    return xrmerge(
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_dispatch().loc["hydro"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["hydro"])
                / (
                    float(fei_over_lifetime_res_elec_dispatch().loc["hydro"])
                    * gquality_of_electricity()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_dispatch().loc["geot elec"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["geot elec"])
                / (
                    float(fei_over_lifetime_res_elec_dispatch().loc["geot elec"])
                    * gquality_of_electricity()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"])
                == 0,
                lambda: 0,
                lambda: float(
                    output_elec_over_lifetime_res_elec().loc["solid bioE elec"]
                )
                / (
                    float(fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"])
                    * gquality_of_electricity()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_dispatch().loc["oceanic"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["oceanic"])
                / (
                    float(fei_over_lifetime_res_elec_dispatch().loc["oceanic"])
                    * gquality_of_electricity()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_var().loc["wind onshore"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["wind onshore"])
                / float(fei_over_lifetime_res_elec_var().loc["wind onshore"]),
            ),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_var().loc["wind offshore"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["wind offshore"])
                / float(fei_over_lifetime_res_elec_var().loc["wind offshore"]),
            ),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_var().loc["solar PV"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["solar PV"])
                / float(fei_over_lifetime_res_elec_var().loc["solar PV"]),
            ),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            if_then_else(
                float(fei_over_lifetime_res_elec_var().loc["CSP"]) == 0,
                lambda: 0,
                lambda: float(output_elec_over_lifetime_res_elec().loc["CSP"])
                / float(fei_over_lifetime_res_elec_var().loc["CSP"]),
            ),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


def static_eroitot_res_elec():
    """
    Real Name: "'static' EROItot RES elec"
    Original Eqn: IF THEN ELSE(SUM(FEI over lifetime RES elec[RES elec!])<0, 0, SUM(output elec over lifetime RES elec [RES elec!])/(SUM(FEI over lifetime RES elec[RES elec!])))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    EROI over the lifetime of the aggregated outputs and inputs of RES for
        generating electricity.
    """
    return if_then_else(
        sum(fei_over_lifetime_res_elec(), dim=("RES elec",)) < 0,
        lambda: 0,
        lambda: sum(output_elec_over_lifetime_res_elec(), dim=("RES elec",))
        / (sum(fei_over_lifetime_res_elec(), dim=("RES elec",))),
    )


@subs(["RES elec"], _subscript_dict)
def ced_decom_res_elec_capacity():
    """
    Real Name: CED decom RES elec capacity
    Original Eqn: ZIDZ( share energy requirements for decom RES elec[RES elec]*CEDtot new cap RES elec var[RES elec]*wear RES elec[RES elec], RES elec capacity under construction TW[RES elec])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Cumulative energy demand (CED) required to decommission RES electricity
        generation plants which have ended their lifetime.
    """
    return zidz(
        share_energy_requirements_for_decom_res_elec()
        * cedtot_new_cap_res_elec_var()
        * wear_res_elec(),
        res_elec_capacity_under_construction_tw(),
    )


@subs(["RES elec", "materials"], _subscript_dict)
def ced_new_cap_per_material_res_elec_var():
    """
    Real Name: CED new cap per material RES elec var
    Original Eqn: materials required for new RES elec Mt[RES elec,materials]*Energy cons per unit of material cons for RES elec[materials]*kg per Mt/MJ per EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Cumulative energy demand per material of new installed capacity of RES
        variables per technology.
    """
    return (
        materials_required_for_new_res_elec_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def ced_om_over_lifetime_per_material_res_elec_var():
    """
    Real Name: "CED O&M over lifetime per material RES elec var"
    Original Eqn: RES elec capacity under construction TW[RES elec]*"materials for O&M per capacity installed RES elec"[RES elec,materials]*Energy cons per unit of material cons for RES elec[materials] *lifetime RES elec[RES elec]*(M per T/kg per Mt)*(kg per Mt/MJ per EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Cumulative energy demand per material for O&M of RES variables per
        technology over all the lifetime of the infrastructure.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * materials_for_om_per_capacity_installed_res_elec()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * lifetime_res_elec()
        * (m_per_t() / kg_per_mt())
        * (kg_per_mt() / mj_per_ej())
    )


@subs(["RES elec"], _subscript_dict)
def ced_om_over_lifetime_res_elec_var():
    """
    Real Name: "CED O&M over lifetime RES elec var"
    Original Eqn: (SUM("CED O&M over lifetime per material RES elec var"[RES elec,materials!] )+SUM("CED O&M over lifetime per water RES elec var" [RES elec,water0!]))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Cumulative energy demand for O&M of RES variables per technology over all
        the lifetime of the infrastructure.
    """
    return sum(
        ced_om_over_lifetime_per_material_res_elec_var(), dim=("materials",)
    ) + sum(ced_om_over_lifetime_per_water_res_elec_var(), dim=("water0",))


@subs(["RES elec", "materials"], _subscript_dict)
def ced_om_per_material_res_elec_var():
    """
    Real Name: "CED O&M per material RES elec var"
    Original Eqn: "materials required for O&M RES elec Mt"[RES elec,materials]*Energy cons per unit of material cons for RES elec[materials]*kg per Mt/MJ per EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Cumulative energy demand per material of new installed capacity of RES
        variables per technology.
    """
    return (
        materials_required_for_om_res_elec_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@subs(["RES elec"], _subscript_dict)
def cedtot_new_cap_res_elec_var():
    """
    Real Name: CEDtot new cap RES elec var
    Original Eqn: SUM(CED new cap per material RES elec var[RES elec,materials!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Cumulative energy demand of new capacity for RES variables per technology.
    """
    return sum(ced_new_cap_per_material_res_elec_var(), dim=("materials",))


@subs(["RES elec"], _subscript_dict)
def cedtot_om_res_elec_var():
    """
    Real Name: "CEDtot O&M RES elec var"
    Original Eqn: SUM("CED O&M per material RES elec var"[RES elec,materials!])+"Total energy requirements O&M for water consumption RES elec"[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Cumulative energy demand of O&M for RES variables per technology.
    """
    return (
        sum(ced_om_per_material_res_elec_var(), dim=("materials",))
        + total_energy_requirements_om_for_water_consumption_res_elec()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def cedtot_per_material_res_elec_var():
    """
    Real Name: CEDtot per material RES elec var
    Original Eqn: CED new cap per material RES elec var[RES elec,materials]+"CED O&M over lifetime per material RES elec var"[RES elec,materials]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Total cumulative energy demand (construction+O&M) per material of RES
        variables per technology.
    """
    return (
        ced_new_cap_per_material_res_elec_var()
        + ced_om_over_lifetime_per_material_res_elec_var()
    )


@subs(["RES elec"], _subscript_dict)
def cedtot_per_tw_over_lifetime_res_elec_dispatch():
    """
    Real Name: CEDtot per TW over lifetime RES elec dispatch
    Original Eqn: ZIDZ( (1-"RES elec variables?"[RES elec])*("Cp-ini RES elec"[RES elec]*lifetime RES elec[RES elec]*EJ per TWh/TWe per TWh) , "EROI-ini RES elec dispatch"[RES elec]*quality of electricity 2015 )
    Units: EJ/TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total cumulative energy demand (including installation of new capacity and
        O&M) per MW for RES dispatchables per technology over the lifetime of the
        infrastructure.
    """
    return zidz(
        (1 - res_elec_variables())
        * (cpini_res_elec() * lifetime_res_elec() * ej_per_twh() / twe_per_twh()),
        eroiini_res_elec_dispatch() * quality_of_electricity_2015(),
    )


@subs(["RES elec", "materials"], _subscript_dict)
def cedtot_per_tw_per_material_res_elec_var():
    """
    Real Name: CEDtot per TW per material RES elec var
    Original Eqn: ZIDZ( CEDtot per material RES elec var[RES elec,materials], RES elec capacity under construction TW[RES elec] )
    Units: EJ/TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Total cumulative energy demand (construction+O&M) per power installed per
        material of RES variables per technology (considering only material
        requirements).
    """
    return zidz(
        cedtot_per_material_res_elec_var(), res_elec_capacity_under_construction_tw()
    )


@subs(["RES elec"], _subscript_dict)
def cedtot_per_tw_res_elec_var():
    """
    Real Name: CEDtot per TW RES elec var
    Original Eqn: SUM(CEDtot per TW per material RES elec var[RES elec,materials!])*1e+06
    Units: MJ/MW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total cumulative energy demand (construction+O&M) per power installed of
        RES variables per technology (considering only material requirements).
    """
    return sum(cedtot_per_tw_per_material_res_elec_var(), dim=("materials",)) * 1e06


def cedtot_solar_pv():
    """
    Real Name: CEDtot solar PV
    Original Eqn: FEI RES elec var[solar PV]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(fei_res_elec_var().loc["solar PV"])


@subs(["RES elec"], _subscript_dict)
def eptb_dynamic():
    """
    Real Name: EPTB dynamic
    Original Eqn: ZIDZ( lifetime RES elec[RES elec], "'dynamic' EROI RES elec var"[RES elec] )
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return zidz(lifetime_res_elec(), dynamic_eroi_res_elec_var())


@subs(["RES elec"], _subscript_dict)
def eroiini_res_elec_dispatch():
    """
    Real Name: "EROI-ini RES elec dispatch"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'eroi_initial_res_elec_dispatch*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Energy return on energy invested of RES technologies for generating
        electricity dispatchables at the initial Cp level.
    """
    return _ext_constant_eroiini_res_elec_dispatch()


@subs(["RES elec"], _subscript_dict)
def fei_over_lifetime_res_elec():
    """
    Real Name: FEI over lifetime RES elec
    Original Eqn:
      FEI over lifetime RES elec dispatch[hydro]
        .
        .
        .
      FEI over lifetime RES elec var[CSP]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Final energy investments over lifetime for RES elec technologies.
    """
    return xrmerge(
        rearrange(
            float(fei_over_lifetime_res_elec_dispatch().loc["hydro"]),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_dispatch().loc["geot elec"]),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_dispatch().loc["solid bioE elec"]),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_dispatch().loc["oceanic"]),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_var().loc["wind onshore"]),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_var().loc["wind offshore"]),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_var().loc["solar PV"]),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            float(fei_over_lifetime_res_elec_var().loc["CSP"]),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


@subs(["RES elec"], _subscript_dict)
def fei_over_lifetime_res_elec_dispatch():
    """
    Real Name: FEI over lifetime RES elec dispatch
    Original Eqn: CEDtot per TW over lifetime RES elec dispatch[RES elec]*RES elec capacity under construction TW[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Final energy invested over lifetime per RES elec dispatchable technology
        (equivalent to the denominator of the EROI (=CED*g).
    """
    return (
        cedtot_per_tw_over_lifetime_res_elec_dispatch()
        * res_elec_capacity_under_construction_tw()
    )


@subs(["RES elec"], _subscript_dict)
def fei_over_lifetime_res_elec_var():
    """
    Real Name: FEI over lifetime RES elec var
    Original Eqn: (CEDtot new cap RES elec var[RES elec]*(1+share energy requirements for decom RES elec[RES elec]+Grid correction factor RES elec [RES elec])+"CED O&M over lifetime RES elec var"[RES elec])*"g=quality of electricity"+output elec over lifetime RES elec[RES elec]*selfelectricity consumption RES elec[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Final energy invested over lifetime per RES elec variable technology
        (equivalent to the denominator of the EROI (=CED*g, with total cumulative
        energy demand (including installation of new capacity and O&M) for RES
        variables per technology over the lifetime of the infrastructure.
    """
    return (
        cedtot_new_cap_res_elec_var()
        * (
            1
            + share_energy_requirements_for_decom_res_elec()
            + grid_correction_factor_res_elec()
        )
        + ced_om_over_lifetime_res_elec_var()
    ) * gquality_of_electricity() + output_elec_over_lifetime_res_elec() * selfelectricity_consumption_res_elec()


@subs(["RES elec"], _subscript_dict)
def fei_res_elec_var():
    """
    Real Name: FEI RES elec var
    Original Eqn: (CEDtot new cap RES elec var[RES elec]*(1+Grid correction factor RES elec[RES elec])+CED decom RES elec capacity [RES elec]+"CEDtot O&M RES elec var"[RES elec])*"g=quality of electricity"+real generation RES elec EJ[RES elec]*selfelectricity consumption RES elec[RES elec]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Final energy invested (equivalent to the denominator of the EROI (=CED*g,
        with total cumulative energy demand including installation of new capacity
        and O&M) for RES variables per technology).
    """
    return (
        cedtot_new_cap_res_elec_var() * (1 + grid_correction_factor_res_elec())
        + ced_decom_res_elec_capacity()
        + cedtot_om_res_elec_var()
    ) * gquality_of_electricity() + real_generation_res_elec_ej() * selfelectricity_consumption_res_elec()


@subs(["RES elec"], _subscript_dict)
def grid_correction_factor_res_elec():
    """
    Real Name: Grid correction factor RES elec
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'grid_correction_factor_res_elec')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Grid correction factor to take into account the electricity losses due to
        Joule effect in each power plant.
    """
    return xrmerge(
        xr.DataArray(
            0, {"RES elec": _subscript_dict["RES ELEC NO MAINTENANCE"]}, ["RES elec"]
        ),
        _ext_constant_grid_correction_factor_res_elec(),
    )


@subs(["RES elec"], _subscript_dict)
def output_elec_over_lifetime_res_elec():
    """
    Real Name: output elec over lifetime RES elec
    Original Eqn: real Cp RES elec[RES elec]*RES elec capacity under construction TW[RES elec]*(1/TWe per TWh)*lifetime RES elec[RES elec]*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total electricity output generated over the full operation of the
        infrastructure of the new capacity installed.
    """
    return (
        real_cp_res_elec()
        * res_elec_capacity_under_construction_tw()
        * (1 / twe_per_twh())
        * lifetime_res_elec()
        * ej_per_twh()
    )


@subs(["RES elec"], _subscript_dict)
def real_generation_res_elec_ej():
    """
    Real Name: real generation RES elec EJ
    Original Eqn: real generation RES elec TWh[RES elec]*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Electricity generation by RES technology.
    """
    return real_generation_res_elec_twh() * ej_per_twh()


@subs(["RES elec"], _subscript_dict)
def res_elec_variables():
    """
    Real Name: "RES elec variables?"
    Original Eqn: 0, 0, 0, 0, 1, 1, 1, 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Vector to distinguis between RES elec variables and dispatchables:        *If=1, RES elec variables (fully endogenous calculation from the materials
        requirements).        *If=0, RES elec dispatchables (partially endogenous calculation requiring
        a value of EROI as starting point).
    """
    return xr.DataArray(
        [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
        {"RES elec": _subscript_dict["RES elec"]},
        ["RES elec"],
    )


@subs(["RES elec"], _subscript_dict)
def selfelectricity_consumption_res_elec():
    """
    Real Name: selfelectricity consumption RES elec
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'self_electricity_consumption_res_elec')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']


    """
    return xrmerge(
        xr.DataArray(
            0, {"RES elec": _subscript_dict["RES ELEC NO MAINTENANCE"]}, ["RES elec"]
        ),
        _ext_constant_selfelectricity_consumption_res_elec(),
    )


@subs(["RES elec"], _subscript_dict)
def share_energy_requirements_for_decom_res_elec():
    """
    Real Name: share energy requirements for decom RES elec
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'share_energy_requirements_for_decom_res_elec')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Share energy requirements for decomissioning power RES plants as a share
        of the energy requirements for the construction of new capacity.
    """
    return xrmerge(
        xr.DataArray(
            0, {"RES elec": _subscript_dict["RES ELEC NO MAINTENANCE"]}, ["RES elec"]
        ),
        _ext_constant_share_energy_requirements_for_decom_res_elec(),
    )


def total_final_energy_invested_res_elec_var():
    """
    Real Name: Total final energy invested RES elec var
    Original Eqn: SUM(FEI RES elec var[RES elec!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy invested is equivalent to the denominator of the EROI
        (=CED*g).
    """
    return sum(fei_res_elec_var(), dim=("RES elec",))


_ext_constant_eroiini_res_elec_dispatch = ExtConstant(
    "../energy.xlsx",
    "Global",
    "eroi_initial_res_elec_dispatch*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_eroiini_res_elec_dispatch",
)


_ext_constant_grid_correction_factor_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "grid_correction_factor_res_elec",
    {"RES elec": _subscript_dict["RES ELEC MAINTENANCE"]},
    _root,
    "_ext_constant_grid_correction_factor_res_elec",
)


_ext_constant_selfelectricity_consumption_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "self_electricity_consumption_res_elec",
    {"RES elec": _subscript_dict["RES ELEC MAINTENANCE"]},
    _root,
    "_ext_constant_selfelectricity_consumption_res_elec",
)


_ext_constant_share_energy_requirements_for_decom_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_res_elec",
    {"RES elec": _subscript_dict["RES ELEC MAINTENANCE"]},
    _root,
    "_ext_constant_share_energy_requirements_for_decom_res_elec",
)
