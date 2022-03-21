"""
Module liquids_ped_pes_fes
Translated using PySD version 2.2.3
"""


def abundance_liquids():
    """
    Real Name: abundance liquids
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_liquids_ej() < pes_liquids_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids_ej() - pes_liquids_ej(), ped_liquids_ej()),
    )


def check_liquids():
    """
    Real Name: check liquids
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0, demand<supply (oversupply). Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_liquids_ej() - pes_liquids_ej(), pes_liquids_ej())


def constrain_liquids_exogenous_growth():
    """
    Real Name: "constrain liquids exogenous growth?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > -0.0001, lambda: 1, lambda: check_liquids())


def fes_total_biofuels():
    """
    Real Name: FES total biofuels
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total biofuels in final energy
    """
    return share_biofuel_in_pes() * float(real_fe_consumption_by_fuel().loc["liquids"])


def other_liquids_required_ej():
    """
    Real Name: Other liquids required EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        float(energy_distr_losses_ff_ej().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
    )


def other_liquids_supply_ej():
    """
    Real Name: Other liquids supply EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_production_ej()
    )


def ped_liquids_ej():
    """
    Real Name: PED liquids EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of total liquids.
    """
    return np.maximum(
        0,
        required_fed_by_liquids_ej()
        + other_liquids_required_ej()
        + pe_demand_oil_elec_plants_ej()
        + ped_oil_for_heat_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_liquids_heatnc(),
    )


def ped_nre_liquids():
    """
    Real Name: PED NRE Liquids
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of non-renewable energy for the production of liquids.
    """
    return np.maximum(0, ped_liquids_ej() - fes_total_biofuels_production_ej())


def ped_total_oil_ej():
    """
    Real Name: PED total oil EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


def pes_liquids_ej():
    """
    Real Name: PES Liquids EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary supply of liquids.
    """
    return pes_oil_ej() + other_liquids_supply_ej()


def required_fed_by_liquids_ej():
    """
    Real Name: Required FED by liquids EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


def share_biofuel_in_pes():
    """
    Real Name: Share biofuel in PES
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of biofuels in total liquids primary energy
    """
    return zidz(fes_total_biofuels_production_ej(), pes_liquids_ej())


def share_liquids_dem_for_heatnc():
    """
    Real Name: "share liquids dem for Heat-nc"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of liquids demand for non-commercial Heat plants in relation to the total demand of liquids.
    """
    return zidz(ped_liquids_heatnc(), pes_liquids_ej())


def share_liquids_for_final_energy():
    """
    Real Name: share liquids for final energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of final energy vs primary energy for liquids.
    """
    return zidz(
        required_fed_by_liquids_ej(), ped_liquids_ej() - other_liquids_required_ej()
    )


def share_oil_dem_for_elec():
    """
    Real Name: share oil dem for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of oil demand to cover electricity consumption.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: pe_demand_oil_elec_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


def share_oil_dem_for_heatcom():
    """
    Real Name: "share oil dem for Heat-com"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of oil demand for commercial Heat plants in relation to the total demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_for_heat_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


def total_demand_liquids_mbd():
    """
    Real Name: "Total demand liquids mb/d"
    Original Eqn:
    Units: Mb/d
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand of liquids.
    """
    return ped_liquids_ej() * mbd_per_ejyear()


def year_scarcity_liquids():
    """
    Real Name: Year scarcity liquids
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())
