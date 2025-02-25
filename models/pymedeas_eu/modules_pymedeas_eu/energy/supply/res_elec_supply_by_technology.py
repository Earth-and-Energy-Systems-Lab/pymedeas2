"""
Module energy.supply.res_elec_supply_by_technology
Translated using PySD version 3.14.1
"""

@component.add(
    name="Demand Elec NRE TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_twh": 1,
        "fe_tot_generation_all_res_elec_twh": 1,
        "fes_elec_from_waste": 1,
    },
)
def demand_elec_nre_twh():
    """
    The model assigns priority to RES generation to cover the electricity demand.
    """
    return np.maximum(
        0,
        total_fe_elec_demand_twh()
        - fe_tot_generation_all_res_elec_twh()
        - fes_elec_from_waste(),
    )


@component.add(
    name="efficiency conversion bioE to Elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_conversion_bioe_to_elec"},
)
def efficiency_conversion_bioe_to_elec():
    """
    Efficiency of the transformation from bioenergy to electricity in both electricity plants and CHPs (estimation for 2014 from the IEA balances).
    """
    return _ext_constant_efficiency_conversion_bioe_to_elec()


_ext_constant_efficiency_conversion_bioe_to_elec = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_to_elec",
    {},
    _root,
    {},
    "_ext_constant_efficiency_conversion_bioe_to_elec",
)


@component.add(
    name="FE tot generation all RES elec TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_real_tot_generation_res_elec": 1,
        "fes_elec_from_res_with_priority": 1,
    },
)
def fe_tot_generation_all_res_elec_twh():
    """
    Electricity generation from all RES technologies.
    """
    return fe_real_tot_generation_res_elec() + fes_elec_from_res_with_priority()


@component.add(
    name="FES elec from RES with priority",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_elec_from_biogas_twh": 1},
)
def fes_elec_from_res_with_priority():
    return fes_elec_from_biogas_twh()


@component.add(
    name="MToe per EJ", units="MToe/EJ", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_per_ej():
    """
    Unit conversion (1000 Mtoe=41.868 EJ)
    """
    return 23.8846


@component.add(
    name="PE BioW for Elec generation Mtoe",
    units="MToe/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_real_generation_res_elec": 1, "mtoe_per_ej": 1},
)
def pe_biow_for_elec_generation_mtoe():
    """
    Annual primary energy to generate electricity (Direct Equivalent Method).
    """
    return float(pe_real_generation_res_elec().loc["solid bioE elec"]) * mtoe_per_ej()


@component.add(
    name="PE Elec generation from RES EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_real_generation_res_elec": 1, "pes_tot_biogas_for_elec": 1},
)
def pe_elec_generation_from_res_ej():
    """
    Primary energy from RES electricity generation. For all sources excepting "Bio" the factor "RES to fossil accounting" is applied for the equivalent primary energy.
    """
    return (
        sum(
            pe_real_generation_res_elec().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + pes_tot_biogas_for_elec()
    )


@component.add(
    name="PE losses BioE for Elec EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_real_generation_res_elec": 1,
        "real_generation_res_elec_twh": 1,
        "ej_per_twh": 1,
    },
)
def pe_losses_bioe_for_elec_ej():
    """
    (Primary energy) losses due to the production of electricity from solid bioenergy.
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        - float(real_generation_res_elec_twh().loc["solid bioE elec"]) * ej_per_twh()
    )


@component.add(
    name="PE real generation RES elec",
    units="EJ/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_generation_res_elec_twh": 8,
        "ej_per_twh": 8,
        "res_to_fossil_accounting": 7,
        "efficiency_conversion_bioe_to_elec": 1,
    },
)
def pe_real_generation_res_elec():
    """
    Primary energy supply of electricity production of RES.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = (
        float(real_generation_res_elec_twh().loc["hydro"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["geot elec"]] = (
        float(real_generation_res_elec_twh().loc["geot elec"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["solid bioE elec"]] = (
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        / efficiency_conversion_bioe_to_elec()
    ) * ej_per_twh()
    value.loc[["oceanic"]] = (
        float(real_generation_res_elec_twh().loc["oceanic"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["wind onshore"]] = (
        float(real_generation_res_elec_twh().loc["wind onshore"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["wind offshore"]] = (
        float(real_generation_res_elec_twh().loc["wind offshore"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["solar PV"]] = (
        float(real_generation_res_elec_twh().loc["solar PV"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    value.loc[["CSP"]] = (
        float(real_generation_res_elec_twh().loc["CSP"])
        * ej_per_twh()
        * res_to_fossil_accounting()
    )
    return value


@component.add(
    name="RES to fossil accounting",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def res_to_fossil_accounting():
    """
    There are different methods to report primary energy. If=1, it corresponds with the direct equivalent method which counts one unit of secondary energy provided from non-combustible sources as one unit of primary energy, that is, 1 kWh of (useful) electricity or heat is accounted for as 1 kWh = 3.6 MJ of primary energy. For more information see Annex II of (IPCC, 2011).
    """
    return 1


@component.add(
    name="share Elec demand covered by RES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_twh": 2, "fe_tot_generation_all_res_elec_twh": 1},
)
def share_elec_demand_covered_by_res():
    """
    Share of the electricity demand covered by RES. Condition to avoid error when the denominator is zero (0.5 is an arbitrary value).
    """
    return if_then_else(
        total_fe_elec_demand_twh() > 0,
        lambda: np.minimum(
            1, fe_tot_generation_all_res_elec_twh() / total_fe_elec_demand_twh()
        ),
        lambda: 0.5,
    )


@component.add(
    name="Total FE Elec demand after priorities",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_twh": 1,
        "fes_elec_from_res_with_priority": 1,
        "fes_elec_from_waste": 1,
    },
)
def total_fe_elec_demand_after_priorities():
    return np.maximum(
        total_fe_elec_demand_twh()
        - fes_elec_from_res_with_priority()
        - fes_elec_from_waste(),
        0,
    )
