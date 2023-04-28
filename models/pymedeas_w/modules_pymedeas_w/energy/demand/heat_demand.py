"""
Module energy.demand.heat_demand
Translated using PySD version 3.9.1
"""


@component.add(
    name="FE heat demand consum",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def fe_heat_demand_consum():
    """
    Heat demand consumption.
    """
    return float(required_fed_by_fuel().loc["heat"])


@component.add(
    name='"FED Heat-com after priorities EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_heatcom_ej": 1,
        "fes_heatcom_from_waste_ej": 1,
        "fes_heatcom_from_biogas_ej": 1,
    },
)
def fed_heatcom_after_priorities_ej():
    """
    Total commercial heat demand including distribution losses after technologies with priority in the mix (waste and biogas).
    """
    return np.maximum(
        0,
        total_fed_heatcom_ej()
        - fes_heatcom_from_waste_ej()
        - fes_heatcom_from_biogas_ej(),
    )


@component.add(
    name='"FED Heat-com EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_heatcom": 1},
)
def fed_heatcom_ej():
    """
    Final energy demand heat commercial.
    """
    return required_heatcom()


@component.add(
    name='"FED Heat-com NRE EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_after_priorities_ej": 1,
        "total_fe_real_supply_res_for_heatcom_ej": 1,
    },
)
def fed_heatcom_nre_ej():
    """
    Demand of non renewable energy to produce commercial Heat (final energy). We give priority to RES.
    """
    return np.maximum(
        fed_heatcom_after_priorities_ej() - total_fe_real_supply_res_for_heatcom_ej(), 0
    )


@component.add(
    name='"FED Heat-com plants fossil fuels EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_nre_ej": 1,
        "fes_heatcom_fossil_fuels_chp_plants_ej": 1,
        "fes_heatcom_nuclear_chp_plants_ej": 1,
    },
)
def fed_heatcom_plants_fossil_fuels_ej():
    """
    Demand of fossil fuels for commercial heat plants. Fossil fuels CHP plants have priority due a better efficiency.
    """
    return np.maximum(
        fed_heatcom_nre_ej()
        - fes_heatcom_fossil_fuels_chp_plants_ej()
        - fes_heatcom_nuclear_chp_plants_ej(),
        0,
    )


@component.add(
    name='"FED Heat-nc EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_heat_demand_consum": 1, "required_heatcom": 1},
)
def fed_heatnc_ej():
    """
    Final energy (non-commercial) heat demand.
    """
    return fe_heat_demand_consum() - required_heatcom()


@component.add(
    name='"Heat-com distribution losses"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatcom_ej": 1, "share_heat_distribution_losses": 1},
)
def heatcom_distribution_losses():
    """
    Distribution losses associated to heat commercial.
    """
    return fed_heatcom_ej() * share_heat_distribution_losses()


@component.add(
    name='"Heat-nc distribution losses"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "fed_heatnc_ej": 1},
)
def heatnc_distribution_losses():
    """
    Distribution losses associated to non-commercial heat.
    """
    return total_fed_heatnc_ej() - fed_heatnc_ej()


@component.add(
    name='"PED coal Heat-nc"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_nre_heatnc": 1,
        "share_fed_coal_vs_nre_heatnc": 1,
        "efficiency_coal_for_heat_plants": 1,
    },
)
def ped_coal_heatnc():
    """
    Primary energy demand heat non-commercial to be covered by coal. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_coal_vs_nre_heatnc()
        / efficiency_coal_for_heat_plants()
    )


@component.add(
    name='"PED gas Heat-nc"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_nre_heatnc": 1,
        "share_fed_gas_vs_nre_heatnc": 1,
        "efficiency_gases_for_heat_plants": 1,
    },
)
def ped_gas_heatnc():
    """
    Primary energy demand heat non-commercial to be covered by natural gas. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_gas_vs_nre_heatnc()
        / efficiency_gases_for_heat_plants()
    )


@component.add(
    name='"PED liquids Heat-nc"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_nre_heatnc": 1,
        "share_fed_liquids_vs_nre_heatnc": 1,
        "efficiency_liquids_for_heat_plants": 1,
    },
)
def ped_liquids_heatnc():
    """
    Primary energy demand heat non-commercial to be covered by liquids. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_liquids_vs_nre_heatnc()
        / efficiency_liquids_for_heat_plants()
    )


@component.add(
    name='"Required heat-com"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def required_heatcom():
    return float(required_fed_by_fuel_before_heat_correction().loc["heat"])


@component.add(
    name='"Share FED heat-com vs total heat"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatcom_ej": 2, "total_fed_heat_ej": 1},
)
def share_fed_heatcom_vs_total_heat():
    """
    Share of commercial heat in relation to total final energy use for heat.
    """
    return total_fed_heatcom_ej() / (total_fed_heat_ej() + total_fed_heatcom_ej())


@component.add(
    name="Share heat distribution losses",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_heat_distribution_losses"},
)
def share_heat_distribution_losses():
    """
    Current share of heat transmission and distribution losses in relation to heat consumption. We define these losses at around 6.5% following historical data of IEA database.
    """
    return _ext_constant_share_heat_distribution_losses()


_ext_constant_share_heat_distribution_losses = ExtConstant(
    "../energy.xlsx",
    "Global",
    "share_heat_distribution_losses",
    {},
    _root,
    {},
    "_ext_constant_share_heat_distribution_losses",
)


@component.add(
    name='"Total FE real supply RES for heat-com EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatcom_ej": 1},
)
def total_fe_real_supply_res_for_heatcom_ej():
    """
    Total final energy supply delivered by RES for commercial heat.
    """
    return sum(
        fe_real_generation_res_heatcom_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name='"Total FE real supply RES for heat-nc EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatnc_ej": 1},
)
def total_fe_real_supply_res_for_heatnc_ej():
    """
    Total final energy supply delivered by RES for non-commercial heat.
    """
    return sum(
        fe_real_generation_res_heatnc_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name="Total FED Heat EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatcom_ej": 1, "total_fed_heatnc_ej": 1},
)
def total_fed_heat_ej():
    """
    Total final energy demand (including distribution losses) of heat.
    """
    return total_fed_heatcom_ej() + total_fed_heatnc_ej()


@component.add(
    name='"Total FED Heat-com EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatcom_ej": 1, "share_heat_distribution_losses": 1},
)
def total_fed_heatcom_ej():
    """
    Total commercial heat demand including distribution losses.
    """
    return fed_heatcom_ej() * (1 + share_heat_distribution_losses())


@component.add(
    name='"Total FED Heat-nc EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatnc_ej": 1, "share_heat_distribution_losses": 1},
)
def total_fed_heatnc_ej():
    """
    Total non-commercial heat demand including distribution losses (and climate change impacts).
    """
    return fed_heatnc_ej() * (1 + share_heat_distribution_losses())


@component.add(
    name='"Total FED NRE Heat-nc"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "total_fe_real_supply_res_for_heatnc_ej": 1},
)
def total_fed_nre_heatnc():
    """
    Final energy demand heat non-commercial to be covered by NRE (including distribution losses and climate change impacts).
    """
    return np.maximum(
        0, total_fed_heatnc_ej() - total_fe_real_supply_res_for_heatnc_ej()
    )
