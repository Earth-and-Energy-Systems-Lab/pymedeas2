"""
Module res_elec_supply_by_technology
Translated using PySD version 2.2.3
"""


def demand_elec_nre_twh():
    """
    Real Name: Demand Elec NRE TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The model assigns priority to RES generation to cover the electricity demand.
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation from bioenergy to electricity in both electricity plants and CHPs (estimation for 2014 from the IEA balances).
    """
    return _ext_constant_efficiency_conversion_bioe_to_elec()


_ext_constant_efficiency_conversion_bioe_to_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_to_elec",
    {},
    _root,
    "_ext_constant_efficiency_conversion_bioe_to_elec",
)


def fe_tot_generation_all_res_elec_twh():
    """
    Real Name: FE tot generation all RES elec TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation from all RES technologies.
    """
    return fe_real_tot_generation_res_elec_twh() + fes_elec_from_res_with_priority_twh()


def fes_elec_from_res_with_priority_twh():
    """
    Real Name: FES elec from RES with priority TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return fes_elec_from_biogas_twh()


def mtoe_per_ej():
    """
    Real Name: MToe per EJ
    Original Eqn:
    Units: MToe/EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Unit conversion (1000 Mtoe=41.868 EJ)
    """
    return 23.8846


def pe_biow_for_elec_generation_mtoe():
    """
    Real Name: PE BioW for Elec generation Mtoe
    Original Eqn:
    Units: MToe/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["solid bioE elec"]) * mtoe_per_ej()


def pe_elec_generation_from_res_ej():
    """
    Real Name: PE Elec generation from RES EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy from RES electricity generation. For all sources excepting "Bio" the factor "RES to fossil accounting" is applied for the equivalent primary energy.
    """
    return (
        sum(
            pe_real_generation_res_elec().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + pes_tot_biogas_for_elec()
    )


def pe_losses_bioe_for_elec_ej():
    """
    Real Name: PE losses BioE for Elec EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    (Primary energy) losses due to the production of electricity from solid bioenergy.
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        - float(real_generation_res_elec_twh().loc["solid bioE elec"]) * ej_per_twh()
    )


@subs(["RES elec"], _subscript_dict)
def pe_real_generation_res_elec():
    """
    Real Name: PE real generation RES elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Primary energy supply of electricity production of RES.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[{"RES elec": ["hydro"]}] = (
        float(real_generation_res_elec_twh().loc["hydro"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["geot elec"]}] = (
        float(real_generation_res_elec_twh().loc["geot elec"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = (
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        / efficiency_conversion_bioe_to_elec()
    ) * ej_per_twh()
    value.loc[{"RES elec": ["oceanic"]}] = (
        float(real_generation_res_elec_twh().loc["oceanic"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["wind onshore"]}] = (
        float(real_generation_res_elec_twh().loc["wind onshore"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["wind offshore"]}] = (
        float(real_generation_res_elec_twh().loc["wind offshore"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["solar PV"]}] = (
        float(real_generation_res_elec_twh().loc["solar PV"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[{"RES elec": ["CSP"]}] = (
        float(real_generation_res_elec_twh().loc["CSP"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    return value


def res_to_fossil_accounting():
    """
    Real Name: RES to fossil accounting
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    There are different methods to report primary energy. If=1, it corresponds with the direct equivalent method which counts one unit of secondary energy provided from non-combustible sources as one unit of primary energy, that is, 1 kWh of (useful) electricity or heat is accounted for as 1 kWh = 3.6 MJ of primary energy. For more information see Annex II of (IPCC, 2011).
    """
    return 1


def share_elec_demand_covered_by_res():
    """
    Real Name: share Elec demand covered by RES
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of the electricity demand covered by RES. Condition to avoid error when the denominator is zero (0.5 is an arbitrary value).
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
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return np.maximum(
        total_fe_elec_demand_twh()
        - fes_elec_from_res_with_priority_twh()
        - fes_elec_from_waste_twh(),
        0,
    )
