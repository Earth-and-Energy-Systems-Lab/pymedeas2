"""
Module ped_pes_fes
Translated using PySD version 2.2.0
"""


def abundance_liquids():
    """
    Real Name: abundance liquids
    Original Eqn: IF THEN ELSE(PED liquids EJ<PES Liquids EJ, 1, 1- ZIDZ( PED liquids EJ-PES Liquids EJ, PED liquids EJ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        ped_liquids_ej() < pes_liquids_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids_ej() - pes_liquids_ej(), ped_liquids_ej()),
    )


def check_liquids():
    """
    Real Name: check liquids
    Original Eqn: ZIDZ( (PED liquids EJ-PES Liquids EJ), PES Liquids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0,
        demand<supply (oversupply). Variable to avoid energy oversupply caused by
        exogenously driven policies.
    """
    return zidz((ped_liquids_ej() - pes_liquids_ej()), pes_liquids_ej())


def constrain_liquids_exogenous_growth():
    """
    Real Name: "constrain liquids exogenous growth?"
    Original Eqn: IF THEN ELSE(check liquids>-0.0001,1,check liquids)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If negative, there is oversupply of liquids. This variable is used to
        constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > -0.0001, lambda: 1, lambda: check_liquids())


def fes_total_biofuels():
    """
    Real Name: FES total biofuels
    Original Eqn: Share biofuel in PES*real FE consumption by fuel[liquids]
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total biofuels in final energy
    """
    return share_biofuel_in_pes() * float(real_fe_consumption_by_fuel().loc["liquids"])


def other_liquids_required_ej():
    """
    Real Name: Other liquids required EJ
    Original Eqn: Energy distr losses FF EJ[liquids]+Transformation FF losses EJ[liquids]+"Non-energy use demand by final fuel EJ"[liquids]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(energy_distr_losses_ff_ej().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
    )


def other_liquids_supply_ej():
    """
    Real Name: Other liquids supply EJ
    Original Eqn: Oil refinery gains EJ+"FES CTL+GTL EJ"+FES total biofuels production EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_production_ej()
    )


def ped_liquids_ej():
    """
    Real Name: PED liquids EJ
    Original Eqn: MAX(0,Required FED by liquids EJ+Other liquids required EJ+PE demand oil Elec plants EJ +PED oil for Heat plants EJ+PED oil for CHP plants EJ+"PED liquids Heat-nc")
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: MAX(0, PED liquids EJ-FES total biofuels production EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of non-renewable energy for the production of
        liquids.
    """
    return np.maximum(0, ped_liquids_ej() - fes_total_biofuels_production_ej())


def ped_total_oil_ej():
    """
    Real Name: PED total oil EJ
    Original Eqn: MAX(0,PED NRE Liquids-"FES CTL+GTL EJ"-Oil refinery gains EJ )
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


def pes_liquids_ej():
    """
    Real Name: PES Liquids EJ
    Original Eqn: PES oil EJ+Other liquids supply EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary supply of liquids.
    """
    return pes_oil_ej() + other_liquids_supply_ej()


def required_fed_by_liquids_ej():
    """
    Real Name: Required FED by liquids EJ
    Original Eqn: Required FED by fuel[liquids]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


def share_biofuel_in_pes():
    """
    Real Name: Share biofuel in PES
    Original Eqn: ZIDZ(FES total biofuels production EJ, PES Liquids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of biofuels in total liquids primary energy
    """
    return zidz(fes_total_biofuels_production_ej(), pes_liquids_ej())


def share_liquids_dem_for_heatnc():
    """
    Real Name: "share liquids dem for Heat-nc"
    Original Eqn: ZIDZ("PED liquids Heat-nc", PES Liquids EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of liquids demand for non-commercial Heat plants in relation to the
        total demand of liquids.
    """
    return zidz(ped_liquids_heatnc(), pes_liquids_ej())


def share_liquids_for_final_energy():
    """
    Real Name: share liquids for final energy
    Original Eqn: ZIDZ( Required FED by liquids EJ, (PED liquids EJ-Other liquids required EJ) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of final energy vs primary energy for liquids.
    """
    return zidz(
        required_fed_by_liquids_ej(), (ped_liquids_ej() - other_liquids_required_ej())
    )


def share_oil_dem_for_elec():
    """
    Real Name: share oil dem for Elec
    Original Eqn: IF THEN ELSE(PED total oil EJ>0, PE demand oil Elec plants EJ/PED total oil EJ, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: IF THEN ELSE(PED total oil EJ>0, PED oil for Heat plants EJ/PED total oil EJ,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of oil demand for commercial Heat plants in relation to the total
        demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_for_heat_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


def total_demand_liquids_mbd():
    """
    Real Name: "Total demand liquids mb/d"
    Original Eqn: PED liquids EJ*"Mb/d per EJ/year"
    Units: Mb/d
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand of liquids.
    """
    return ped_liquids_ej() * mbd_per_ejyear()


def year_scarcity_liquids():
    """
    Real Name: Year scarcity liquids
    Original Eqn: IF THEN ELSE(abundance liquids>0.95, 0, Time)
    Units: year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())
