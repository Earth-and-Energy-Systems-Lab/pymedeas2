"""
Module heat_demand
Translated using PySD version 2.2.1
"""


def fed_heatcom_after_priorities_ej():
    """
    Real Name: "FED Heat-com after priorities EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total commercial heat demand including distribution losses after technologies with priority in the mix (waste and biogas).
    """
    return np.maximum(
        0,
        total_fed_heatcom_ej()
        - fes_heatcom_from_waste_ej()
        - fes_heatcom_from_biogas_ej(),
    )


def fed_heatcom_ej():
    """
    Real Name: "FED Heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy demand heat commercial.
    """
    return float(required_fed_by_fuel_before_heat_correction().loc["heat"])


def fed_heatcom_nre_ej():
    """
    Real Name: "FED Heat-com NRE EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of non renewable energy to produce commercial Heat (final energy). We give priority to RES.
    """
    return np.maximum(
        fed_heatcom_after_priorities_ej() - total_fe_real_supply_res_for_heatcom_ej(), 0
    )


def fed_heatcom_plants_fossil_fuels_ej():
    """
    Real Name: "FED Heat-com plants fossil fuels EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of fossil fuels for commercial heat plants. Fossil fuels CHP plants have priority due a better efficiency.
    """
    return np.maximum(
        fed_heatcom_nre_ej()
        - fes_heatcom_fossil_fuels_chp_plants_ej()
        - fes_heatcom_nuclear_chp_plants_ej(),
        0,
    )


def fed_heatnc_ej():
    """
    Real Name: "FED Heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy (non-commercial) heat demand.
    """
    return float(required_fed_by_fuel().loc["heat"]) - float(
        required_fed_by_fuel_before_heat_correction().loc["heat"]
    )


def heatcom_distribution_losses():
    """
    Real Name: "Heat-com distribution losses"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Distribution losses associated to heat commercial.
    """
    return fed_heatcom_ej() * share_heat_distribution_losses()


def heatnc_distribution_losses():
    """
    Real Name: "Heat-nc distribution losses"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Distribution losses associated to non-commercial heat.
    """
    return total_fed_heatnc_ej() - fed_heatnc_ej()


def ped_coal_heatnc():
    """
    Real Name: "PED coal Heat-nc"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand heat non-commercial to be covered by coal. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_coal_vs_nre_heatnc()
        / efficiency_coal_for_heat_plants()
    )


def ped_gas_heatnc():
    """
    Real Name: "PED gas Heat-nc"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand heat non-commercial to be covered by natural gas. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_gas_vs_nre_heatnc()
        / efficiency_gases_for_heat_plants()
    )


def ped_liquids_heatnc():
    """
    Real Name: "PED liquids Heat-nc"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand heat non-commercial to be covered by liquids. It corresponds to the FEH (final energy use for heat) metric which includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_liquids_vs_nre_heatnc()
        / efficiency_liquids_for_heat_plants()
    )


def share_fed_heatcom_vs_total_heat():
    """
    Real Name: "Share FED heat-com vs total heat"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of commercial heat in relation to total final energy use for heat.
    """
    return zidz(total_fed_heatcom_ej(), total_fed_heat_ej() + total_fed_heatcom_ej())


def share_heat_distribution_losses():
    """
    Real Name: Share heat distribution losses
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current share of heat transmission and distribution losses in relation to heat consumption. We define these losses at around 6.5% following historical data of IEA database.
    """
    return _ext_constant_share_heat_distribution_losses()


_ext_constant_share_heat_distribution_losses = ExtConstant(
    "../energy.xlsx",
    "Global",
    "share_heat_distribution_losses",
    {},
    _root,
    "_ext_constant_share_heat_distribution_losses",
)


def total_fe_real_supply_res_for_heatcom_ej():
    """
    Real Name: "Total FE real supply RES for heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy supply delivered by RES for commercial heat.
    """
    return sum(
        fe_real_generation_res_heatcom_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


def total_fe_real_supply_res_for_heatnc_ej():
    """
    Real Name: "Total FE real supply RES for heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy supply delivered by RES for non-commercial heat.
    """
    return sum(
        fe_real_generation_res_heatnc_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


def total_fed_heat_ej():
    """
    Real Name: Total FED Heat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy demand (including distribution losses) of heat.
    """
    return total_fed_heatcom_ej() + total_fed_heatnc_ej()


def total_fed_heatcom_ej():
    """
    Real Name: "Total FED Heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total commercial heat demand including distribution losses.
    """
    return fed_heatcom_ej() * (1 + share_heat_distribution_losses())


def total_fed_heatnc_ej():
    """
    Real Name: "Total FED Heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total non-commercial heat demand including distribution losses (and climate change impacts).
    """
    return fed_heatnc_ej() * (1 + share_heat_distribution_losses())


def total_fed_nre_heatnc():
    """
    Real Name: "Total FED NRE Heat-nc"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy demand heat non-commercial to be covered by NRE (including distribution losses and climate change impacts).
    """
    return np.maximum(
        0, total_fed_heatnc_ej() - total_fe_real_supply_res_for_heatnc_ej()
    )
