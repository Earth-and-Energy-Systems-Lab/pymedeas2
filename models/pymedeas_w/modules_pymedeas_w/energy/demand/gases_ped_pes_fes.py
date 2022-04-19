"""
Module gases_ped_pes_fes
Translated using PySD version 3.0.0
"""


@component.add(
    name="abundance gases", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def abundance_gases():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_gases() < pes_gases(),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


@component.add(
    name="check gases", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def check_gases():
    """
    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


@component.add(
    name='"constrain gas exogenous growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def constrain_gas_exogenous_growth():
    """
    If negative, there is oversupply of gas. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


@component.add(
    name="FES total biogas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_total_biogas():
    """
    Total biogas in final energy
    """
    return share_biogas_in_pes() * float(real_fe_consumption_by_fuel().loc["gases"])


@component.add(
    name="Other gases required",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def other_gases_required():
    return (
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
    )


@component.add(
    name="PED gases", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def ped_gases():
    """
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


@component.add(
    name='"PED nat. gas EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


@component.add(
    name="PES gases", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return pes_nat_gas() + pes_biogas_for_tfc()


@component.add(
    name="Required FED by gas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def required_fed_by_gas():
    """
    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


@component.add(
    name="Share biogas in PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_biogas_in_pes():
    """
    Share of biogas in total gases primary energy
    """
    return zidz(pes_biogas_for_tfc(), pes_gases())


@component.add(
    name='"share gases dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_gases_dem_for_heatnc():
    """
    Share of natural gas demand for non-commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), pes_gases() - ped_nat_gas_for_gtl_ej())


@component.add(
    name="share gases for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_gases_for_final_energy():
    """
    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gas(),
        ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required(),
    )


@component.add(
    name='"share nat. gas dem for Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_nat_gas_dem_for_elec():
    """
    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: pe_demand_gas_elec_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name='"share nat. gas dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_nat_gas_dem_for_heatcom():
    """
    Share of natural gas demand for commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name="Year scarcity gases",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def year_scarcity_gases():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
