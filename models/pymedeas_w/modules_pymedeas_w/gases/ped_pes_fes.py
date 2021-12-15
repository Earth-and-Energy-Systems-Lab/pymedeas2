"""
Module ped_pes_fes
Translated using PySD version 2.2.0
"""


def abundance_gases():
    """
    Real Name: abundance gases
    Original Eqn: IF THEN ELSE(PED gases<PES gases, 1, 1-ZIDZ( PED gases -PES gases, PED gases ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        ped_gases() < pes_gases(),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


def check_gases():
    """
    Real Name: check gases
    Original Eqn: ZIDZ( PED gases-PES gases, PES gases )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


def constrain_gas_exogenous_growth():
    """
    Real Name: "constrain gas exogenous growth?"
    Original Eqn: IF THEN ELSE(check gases>-0.01,1,check gases)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If negative, there is oversupply of gas. This variable is used to
        constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


def fes_total_biogas():
    """
    Real Name: FES total biogas
    Original Eqn: Share biogas in PES*real FE consumption by fuel[gases]
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total biogas in final energy
    """
    return share_biogas_in_pes() * float(real_fe_consumption_by_fuel().loc["gases"])


def other_gases_required():
    """
    Real Name: Other gases required
    Original Eqn: +Transformation FF losses EJ[gases]+Energy distr losses FF EJ[gases]+"Non-energy use demand by final fuel EJ"[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
    )


def ped_gases():
    """
    Real Name: PED gases
    Original Eqn: MAX(0, Required FED by gas+"PED nat. gas for GTL EJ"+PE demand gas Elec plants EJ+PED gases for Heat plants EJ+PED gas for CHP plants EJ +"PED gas Heat-nc"+Other gases required)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand total gases.
    """
    return np.maximum(
        0,
        required_fed_by_gas()
        + ped_nat_gas_for_gtl_ej()
        + pe_demand_gas_elec_plants_ej()
        + ped_gases_for_heat_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + other_gases_required(),
    )


def ped_nat_gas_ej():
    """
    Real Name: "PED nat. gas EJ"
    Original Eqn: MAX(0, PED gases-PES biogas for TFC)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


def pes_gases():
    """
    Real Name: PES gases
    Original Eqn: PES nat gas+PES biogas for TFC
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply gas.
    """
    return pes_nat_gas() + pes_biogas_for_tfc()


def required_fed_by_gas():
    """
    Real Name: Required FED by gas
    Original Eqn: Required FED by fuel[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


def share_biogas_in_pes():
    """
    Real Name: Share biogas in PES
    Original Eqn: ZIDZ(PES biogas for TFC, PES gases )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of biogas in total gases primary energy
    """
    return zidz(pes_biogas_for_tfc(), pes_gases())


def share_gases_dem_for_heatnc():
    """
    Real Name: "share gases dem for Heat-nc"
    Original Eqn: ZIDZ("PED gas Heat-nc", (PES gases-"PED nat. gas for GTL EJ" ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand for non-commercial Heat plants in relation to
        the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), (pes_gases() - ped_nat_gas_for_gtl_ej()))


def share_gases_for_final_energy():
    """
    Real Name: share gases for final energy
    Original Eqn: ZIDZ( Required FED by gas, (PED gases-"PED nat. gas for GTL EJ"-Other gases required) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gas(),
        (ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()),
    )


def share_nat_gas_dem_for_elec():
    """
    Real Name: "share nat. gas dem for Elec"
    Original Eqn: IF THEN ELSE("PED nat. gas EJ">0, PE demand gas Elec plants EJ/"PED nat. gas EJ", 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: pe_demand_gas_elec_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


def share_nat_gas_dem_for_heatcom():
    """
    Real Name: "share nat. gas dem for Heat-com"
    Original Eqn: IF THEN ELSE("PED nat. gas EJ">0, PED gases for Heat plants EJ/"PED nat. gas EJ", 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand for commercial Heat plants in relation to the
        demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


def year_scarcity_gases():
    """
    Real Name: Year scarcity gases
    Original Eqn: IF THEN ELSE(abundance gases>0.95, 0, Time)
    Units: year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
