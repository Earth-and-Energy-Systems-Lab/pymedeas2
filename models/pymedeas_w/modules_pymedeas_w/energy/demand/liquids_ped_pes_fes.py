"""
Module liquids_ped_pes_fes
Translated using PySD version 3.0.0
"""


@component.add(
    name="abundance liquids", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def abundance_liquids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_liquids_ej() < pes_liquids_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids_ej() - pes_liquids_ej(), ped_liquids_ej()),
    )


@component.add(
    name="check liquids", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def check_liquids():
    """
    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0, demand<supply (oversupply). Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_liquids_ej() - pes_liquids_ej(), pes_liquids_ej())


@component.add(
    name='"constrain liquids exogenous growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def constrain_liquids_exogenous_growth():
    """
    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > -0.0001, lambda: 1, lambda: check_liquids())


@component.add(
    name="FES total biofuels",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_total_biofuels():
    """
    Total biofuels in final energy
    """
    return share_biofuel_in_pes() * float(real_fe_consumption_by_fuel().loc["liquids"])


@component.add(
    name="Other liquids required EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def other_liquids_required_ej():
    return (
        float(energy_distr_losses_ff_ej().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
    )


@component.add(
    name="Other liquids supply EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def other_liquids_supply_ej():
    """
    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_production_ej()
    )


@component.add(
    name="PED liquids EJ", units="EJ/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def ped_liquids_ej():
    """
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


@component.add(
    name="PED NRE Liquids", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def ped_nre_liquids():
    """
    Primary energy demand of non-renewable energy for the production of liquids.
    """
    return np.maximum(0, ped_liquids_ej() - fes_total_biofuels_production_ej())


@component.add(
    name="PED total oil EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ped_total_oil_ej():
    """
    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


@component.add(
    name="PES Liquids EJ", units="EJ/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_liquids_ej():
    """
    Total primary supply of liquids.
    """
    return pes_oil_ej() + other_liquids_supply_ej()


@component.add(
    name="Required FED by liquids EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def required_fed_by_liquids_ej():
    """
    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


@component.add(
    name="Share biofuel in PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_biofuel_in_pes():
    """
    Share of biofuels in total liquids primary energy
    """
    return zidz(fes_total_biofuels_production_ej(), pes_liquids_ej())


@component.add(
    name='"share liquids dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_liquids_dem_for_heatnc():
    """
    Share of liquids demand for non-commercial Heat plants in relation to the total demand of liquids.
    """
    return zidz(ped_liquids_heatnc(), pes_liquids_ej())


@component.add(
    name="share liquids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_liquids_for_final_energy():
    """
    Share of final energy vs primary energy for liquids.
    """
    return zidz(
        required_fed_by_liquids_ej(), ped_liquids_ej() - other_liquids_required_ej()
    )


@component.add(
    name="share oil dem for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_oil_dem_for_elec():
    """
    Share of oil demand to cover electricity consumption.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: pe_demand_oil_elec_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


@component.add(
    name='"share oil dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_oil_dem_for_heatcom():
    """
    Share of oil demand for commercial Heat plants in relation to the total demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_for_heat_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


@component.add(
    name='"Total demand liquids mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_demand_liquids_mbd():
    """
    Total demand of liquids.
    """
    return ped_liquids_ej() * mbd_per_ejyear()


@component.add(
    name="Year scarcity liquids",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def year_scarcity_liquids():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())
