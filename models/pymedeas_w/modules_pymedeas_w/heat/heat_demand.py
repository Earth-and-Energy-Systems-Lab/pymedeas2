"""
Module heat_demand
Translated using PySD version 2.1.0
"""


def fe_heat_demand_consum():
    """
    Real Name: FE heat demand consum
    Original Eqn: Required FED by fuel[heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat demand consumption.
    """
    return float(required_fed_by_fuel().loc["heat"])


def fed_heatcom_after_priorities_ej():
    """
    Real Name: "FED Heat-com after priorities EJ"
    Original Eqn: MAX(0, "Total FED Heat-com EJ"-"FES heat-com from waste EJ"-"FES heat-com from biogas EJ")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total commercial heat demand including distribution losses after
        technologies with priority in the mix (waste and biogas).
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
    Original Eqn: "Required heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand heat commercial.
    """
    return required_heatcom()


def fed_heatcom_nre_ej():
    """
    Real Name: "FED Heat-com NRE EJ"
    Original Eqn: MAX("FED Heat-com after priorities EJ"-"Total FE real supply RES for heat-com EJ",0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of non renewable energy to produce commercial Heat (final energy).
        We give priority to RES.
    """
    return np.maximum(
        fed_heatcom_after_priorities_ej() - total_fe_real_supply_res_for_heatcom_ej(), 0
    )


def fed_heatcom_plants_fossil_fuels_ej():
    """
    Real Name: "FED Heat-com plants fossil fuels EJ"
    Original Eqn: MAX("FED Heat-com NRE EJ"-"FES heat-com fossil fuels CHP plants EJ" -"FES Heat-com nuclear CHP plants EJ",0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of fossil fuels for commercial heat plants. Fossil fuels CHP plants
        have priority due a better efficiency.
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
    Original Eqn: FE heat demand consum-"Required heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy (non-commercial) heat demand.
    """
    return fe_heat_demand_consum() - required_heatcom()


def heatcom_distribution_losses():
    """
    Real Name: "Heat-com distribution losses"
    Original Eqn: "FED Heat-com EJ"*Share heat distribution losses
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Distribution losses associated to heat commercial.
    """
    return fed_heatcom_ej() * share_heat_distribution_losses()


def heatnc_distribution_losses():
    """
    Real Name: "Heat-nc distribution losses"
    Original Eqn: "Total FED Heat-nc EJ"-"FED Heat-nc EJ"
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Distribution losses associated to non-commercial heat.
    """
    return total_fed_heatnc_ej() - fed_heatnc_ej()


def ped_coal_heatnc():
    """
    Real Name: "PED coal Heat-nc"
    Original Eqn: "Total FED NRE Heat-nc"*"share FED coal vs NRE heat-nc"/efficiency coal for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand heat non-commercial to be covered by coal. It
        corresponds to the FEH (final energy use for heat) metric which includes
        the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_coal_vs_nre_heatnc()
        / efficiency_coal_for_heat_plants()
    )


def ped_gas_heatnc():
    """
    Real Name: "PED gas Heat-nc"
    Original Eqn: "Total FED NRE Heat-nc"*"share FED gas vs NRE heat-nc"/efficiency gases for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand heat non-commercial to be covered by natural gas.
        It corresponds to the FEH (final energy use for heat) metric which
        includes the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_gas_vs_nre_heatnc()
        / efficiency_gases_for_heat_plants()
    )


def ped_liquids_heatnc():
    """
    Real Name: "PED liquids Heat-nc"
    Original Eqn: "Total FED NRE Heat-nc"*"share FED liquids vs NRE heat-nc"/efficiency liquids for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand heat non-commercial to be covered by liquids. It
        corresponds to the FEH (final energy use for heat) metric which includes
        the distribution and generation losses (see IEA, 2014).
    """
    return (
        total_fed_nre_heatnc()
        * share_fed_liquids_vs_nre_heatnc()
        / efficiency_liquids_for_heat_plants()
    )


def required_heatcom():
    """
    Real Name: "Required heat-com"
    Original Eqn: Required FED by fuel before heat correction[heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(required_fed_by_fuel_before_heat_correction().loc["heat"])


def share_fed_heatcom_vs_total_heat():
    """
    Real Name: "Share FED heat-com vs total heat"
    Original Eqn: "Total FED Heat-com EJ"/(Total FED Heat EJ+"Total FED Heat-com EJ")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of commercial heat in relation to total final energy use for heat.
    """
    return total_fed_heatcom_ej() / (total_fed_heat_ej() + total_fed_heatcom_ej())


def share_heat_distribution_losses():
    """
    Real Name: Share heat distribution losses
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'share_heat_distribution_losses')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Current share of heat transmission and distribution losses in relation to
        heat consumption. We define these losses at around 6.5% following
        historical data of IEA database.
    """
    return _ext_constant_share_heat_distribution_losses()


def total_fe_real_supply_res_for_heatcom_ej():
    """
    Real Name: "Total FE real supply RES for heat-com EJ"
    Original Eqn: SUM("FE real generation RES heat-com EJ"[RES heat!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy supply delivered by RES for commercial heat.
    """
    return sum(fe_real_generation_res_heatcom_ej(), dim=("RES heat",))


def total_fe_real_supply_res_for_heatnc_ej():
    """
    Real Name: "Total FE real supply RES for heat-nc EJ"
    Original Eqn: SUM("FE real generation RES heat-nc EJ"[RES heat!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy supply delivered by RES for non-commercial heat.
    """
    return sum(fe_real_generation_res_heatnc_ej(), dim=("RES heat",))


def total_fed_heat_ej():
    """
    Real Name: Total FED Heat EJ
    Original Eqn: "Total FED Heat-com EJ"+"Total FED Heat-nc EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy demand (including distribution losses) of heat.
    """
    return total_fed_heatcom_ej() + total_fed_heatnc_ej()


def total_fed_heatcom_ej():
    """
    Real Name: "Total FED Heat-com EJ"
    Original Eqn: "FED Heat-com EJ"*(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total commercial heat demand including distribution losses.
    """
    return fed_heatcom_ej() * (1 + share_heat_distribution_losses())


def total_fed_heatnc_ej():
    """
    Real Name: "Total FED Heat-nc EJ"
    Original Eqn: "FED Heat-nc EJ"*(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total non-commercial heat demand including distribution losses (and
        climate change impacts).
    """
    return fed_heatnc_ej() * (1 + share_heat_distribution_losses())


def total_fed_nre_heatnc():
    """
    Real Name: "Total FED NRE Heat-nc"
    Original Eqn: MAX(0,("Total FED Heat-nc EJ"-"Total FE real supply RES for heat-nc EJ" ))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand heat non-commercial to be covered by NRE (including
        distribution losses and climate change impacts).
    """
    return np.maximum(
        0, (total_fed_heatnc_ej() - total_fe_real_supply_res_for_heatnc_ej())
    )


_ext_constant_share_heat_distribution_losses = ExtConstant(
    "../energy.xlsx",
    "Global",
    "share_heat_distribution_losses",
    {},
    _root,
    "_ext_constant_share_heat_distribution_losses",
)
