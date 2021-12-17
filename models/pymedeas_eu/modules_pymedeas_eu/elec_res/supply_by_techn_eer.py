"""
Module supply_by_techn_eer
Translated using PySD version 2.2.0
"""


def demand_elec_nre_twh():
    """
    Real Name: Demand Elec NRE TWh
    Original Eqn: MAX(0, Total FE Elec demand TWh-FE tot generation all RES elec TWh -FES elec from waste TWh)
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    The model assigns priority to RES generation to cover the electricity
        demand.
    """
    return np.maximum(
        0,
        total_fe_elec_demand_twh()
        - fe_tot_generation_all_res_elec_twh()
        - fes_elec_from_waste_twh(),
    )


def efficiency_conversion_bioe_to_elec():
    """
    Real Name: efficiency conversion bioE to Elec
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_conversion_bioe_to_elec')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation from bioenergy to electricity in both
        electricity plants and CHPs (estimation for 2014 from the IEA balances).
    """
    return _ext_constant_efficiency_conversion_bioe_to_elec()


def fe_elec_generation_from_bioe_twh():
    """
    Real Name: FE Elec generation from bioE TWh
    Original Eqn: real generation RES elec TWh[solid bioE elec]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["solid bioE elec"])


def fe_elec_generation_from_csp_twh():
    """
    Real Name: FE Elec generation from CSP TWh
    Original Eqn: real generation RES elec TWh[CSP]
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["CSP"])


def fe_elec_generation_from_geotelec_twh():
    """
    Real Name: "FE Elec generation from geot-elec TWh"
    Original Eqn: real generation RES elec TWh[geot elec]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["geot elec"])


def fe_elec_generation_from_hydro_twh():
    """
    Real Name: FE Elec generation from hydro TWh
    Original Eqn: real generation RES elec TWh[hydro]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["hydro"])


def fe_elec_generation_from_oceanic_twh():
    """
    Real Name: FE Elec generation from oceanic TWh
    Original Eqn: real generation RES elec TWh[oceanic]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["oceanic"])


def fe_elec_generation_from_offshore_wind_twh():
    """
    Real Name: FE Elec generation from offshore wind TWh
    Original Eqn: real generation RES elec TWh[wind offshore]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["wind offshore"])


def fe_elec_generation_from_onshore_wind_twh():
    """
    Real Name: FE Elec generation from onshore wind TWh
    Original Eqn: real generation RES elec TWh[wind onshore]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["wind onshore"])


def fe_elec_generation_from_solar_pv_twh():
    """
    Real Name: FE Elec generation from solar PV TWh
    Original Eqn: real generation RES elec TWh[solar PV]
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual electricity generation.
    """
    return float(real_generation_res_elec_twh().loc["solar PV"])


def fe_tot_generation_all_res_elec_twh():
    """
    Real Name: FE tot generation all RES elec TWh
    Original Eqn: FE real tot generation RES elec TWh+FES elec from RES with priority TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation from all RES technologies.
    """
    return fe_real_tot_generation_res_elec_twh() + fes_elec_from_res_with_priority_twh()


def fes_elec_from_res_with_priority_twh():
    """
    Real Name: FES elec from RES with priority TWh
    Original Eqn: FES elec from biogas TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fes_elec_from_biogas_twh()


def mtoe_per_ej():
    """
    Real Name: MToe per EJ
    Original Eqn: 23.8846
    Units: MToe/EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion (1000 Mtoe=41.868 EJ)
    """
    return 23.8846


def pe_bioe_for_elec_generation_ej():
    """
    Real Name: PE bioE for Elec generation EJ
    Original Eqn: PE real generation RES elec[solid bioE elec]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["solid bioE elec"])


def pe_biow_for_elec_generation_mtoe():
    """
    Real Name: PE BioW for Elec generation Mtoe
    Original Eqn: PE real generation RES elec[solid bioE elec]*MToe per EJ
    Units: MToe/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["solid bioE elec"]) * mtoe_per_ej()


def pe_csp_for_elec_generation_ej():
    """
    Real Name: PE CSP for Elec generation EJ
    Original Eqn: PE real generation RES elec[CSP]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["CSP"])


def pe_elec_generation_from_res_ej():
    """
    Real Name: PE Elec generation from RES EJ
    Original Eqn: PE bioE for Elec generation EJ+"PE geot-elec for Elec generation EJ" +PE hydro for Elec generation EJ +PE oceanic for Elec generation EJ+PE solar PV for Elec generation EJ+PE CSP for Elec generation EJ +PE onshore wind for Elec generation EJ+PE offshore wind for Elec generation EJ+PES tot biogas for elec
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy from RES electricity generation. For all sources excepting
        "Bio" the factor "RES to fossil accounting" is applied for the equivalent
        primary energy.
    """
    return (
        pe_bioe_for_elec_generation_ej()
        + pe_geotelec_for_elec_generation_ej()
        + pe_hydro_for_elec_generation_ej()
        + pe_oceanic_for_elec_generation_ej()
        + pe_solar_pv_for_elec_generation_ej()
        + pe_csp_for_elec_generation_ej()
        + pe_onshore_wind_for_elec_generation_ej()
        + pe_offshore_wind_for_elec_generation_ej()
        + pes_tot_biogas_for_elec()
    )


def pe_geotelec_for_elec_generation_ej():
    """
    Real Name: "PE geot-elec for Elec generation EJ"
    Original Eqn: PE real generation RES elec[geot elec]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["geot elec"])


def pe_hydro_for_elec_generation_ej():
    """
    Real Name: PE hydro for Elec generation EJ
    Original Eqn: PE real generation RES elec[hydro]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["hydro"])


def pe_losses_bioe_for_elec_ej():
    """
    Real Name: PE losses BioE for Elec EJ
    Original Eqn: PE real generation RES elec[solid bioE elec]-FE Elec generation from bioE TWh*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    (Primary energy) losses due to the production of electricity from solid
        bioenergy.
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        - fe_elec_generation_from_bioe_twh() * ej_per_twh()
    )


def pe_oceanic_for_elec_generation_ej():
    """
    Real Name: PE oceanic for Elec generation EJ
    Original Eqn: PE real generation RES elec[oceanic]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["oceanic"])


def pe_offshore_wind_for_elec_generation_ej():
    """
    Real Name: PE offshore wind for Elec generation EJ
    Original Eqn: PE real generation RES elec[wind offshore]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["wind offshore"])


def pe_onshore_wind_for_elec_generation_ej():
    """
    Real Name: PE onshore wind for Elec generation EJ
    Original Eqn: PE real generation RES elec[wind onshore]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["wind onshore"])


@subs(["RES elec"], _subscript_dict)
def pe_real_generation_res_elec():
    """
    Real Name: PE real generation RES elec
    Original Eqn:
      real generation RES elec TWh[hydro]*EJ per TWh*RES to fossil accounting
        .
        .
        .
      real generation RES elec TWh[CSP]*EJ per TWh*RES to fossil accounting
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Primary energy supply of electricity production of RES.
    """
    return xrmerge(
        rearrange(
            float(real_generation_res_elec_twh().loc["hydro"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["geot elec"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            (
                float(real_generation_res_elec_twh().loc["solid bioE elec"])
                / efficiency_conversion_bioe_to_elec()
            )
            * ej_per_twh(),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["oceanic"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["wind onshore"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["wind offshore"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["solar PV"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            float(real_generation_res_elec_twh().loc["CSP"])
            * ej_per_twh()
            * res_to_fossil_accounting(),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


def pe_solar_pv_for_elec_generation_ej():
    """
    Real Name: PE solar PV for Elec generation EJ
    Original Eqn: PE real generation RES elec[solar PV]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["solar PV"])


def res_to_fossil_accounting():
    """
    Real Name: RES to fossil accounting
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    There are different methods to report primary energy. If=1, it corresponds
        with the direct equivalent method which counts one unit of secondary
        energy provided from non-combustible sources as one unit of primary
        energy, that is, 1 kWh of (useful) electricity or heat is accounted for as
        1 kWh = 3.6 MJ of primary energy. For more information see Annex II of
        (IPCC, 2011).
    """
    return 1


def share_elec_demand_covered_by_res():
    """
    Real Name: share Elec demand covered by RES
    Original Eqn: IF THEN ELSE(Total FE Elec demand TWh>0, MIN(1, FE tot generation all RES elec TWh/Total FE Elec demand TWh),0.5)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of the electricity demand covered by RES. Condition to avoid error
        when the denominator is zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        total_fe_elec_demand_twh() > 0,
        lambda: np.minimum(
            1, fe_tot_generation_all_res_elec_twh() / total_fe_elec_demand_twh()
        ),
        lambda: 0.5,
    )


def total_fe_elec_demand_after_priorities_twh():
    """
    Real Name: Total FE Elec demand after priorities TWh
    Original Eqn: MAX(Total FE Elec demand TWh-FES elec from RES with priority TWh -FES elec from waste TWh,0)
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.maximum(
        total_fe_elec_demand_twh()
        - fes_elec_from_res_with_priority_twh()
        - fes_elec_from_waste_twh(),
        0,
    )


_ext_constant_efficiency_conversion_bioe_to_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_to_elec",
    {},
    _root,
    "_ext_constant_efficiency_conversion_bioe_to_elec",
)
