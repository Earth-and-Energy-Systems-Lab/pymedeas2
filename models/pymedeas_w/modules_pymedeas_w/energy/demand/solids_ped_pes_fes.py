"""
Module solids_ped_pes_fes
Translated using PySD version 3.0.0
"""


@component.add(
    name="abundance solids", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def abundance_solids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pes_solids() > ped_solids(),
        lambda: 1,
        lambda: 1 - zidz(ped_solids() - pes_solids(), ped_solids()),
    )


@component.add(
    name="Historic PES peat EJ", units="EJ", comp_type="Data", comp_subtype="External"
)
def historic_pes_peat_ej():
    """
    Historic primary energy supply of peat.
    """
    return _ext_data_historic_pes_peat_ej(time())


_ext_data_historic_pes_peat_ej = ExtData(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_primary_energy_supply_peat",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_pes_peat_ej",
)


@component.add(
    name="Other solids required",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def other_solids_required():
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff_ej().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


@component.add(
    name="PED coal EJ", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def ped_coal_ej():
    return np.maximum(
        0,
        ped_solids()
        - (
            pe_traditional_biomass_ej_delayed_1yr()
            + pes_peat_ej()
            + pes_waste_for_tfc()
            + losses_in_charcoal_plants_ej()
        ),
    )


@component.add(
    name="PED solids", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def ped_solids():
    """
    Primary energy demand of solids.
    """
    return np.maximum(
        0,
        required_fed_solids()
        + ped_coal_for_ctl_ej()
        + pe_demand_coal_elec_plants_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required(),
    )


@component.add(
    name="PES peat EJ", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_peat_ej():
    return np.maximum(
        if_then_else(
            time() > 2014,
            lambda: -0.0125 * time() + 25.3125,
            lambda: historic_pes_peat_ej(),
        ),
        0,
    )


@component.add(
    name="PES solids", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_solids():
    """
    Primary energy supply solids.
    """
    return (
        extraction_coal_ej()
        + pe_traditional_biomass_ej_delayed_1yr()
        + pes_peat_ej()
        + pes_waste_for_tfc()
        + losses_in_charcoal_plants_ej()
    )


@component.add(
    name="Required FED solids", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def required_fed_solids():
    """
    Required final energy demand solids.
    """
    return float(required_fed_by_fuel().loc["solids"])


@component.add(
    name="share coal dem for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_dem_for_elec():
    """
    Share of coal demand to cover electricity consumption in Elec plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: pe_demand_coal_elec_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share coal dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_dem_for_heatcom():
    """
    Share of coal demand to cover commercial heat consumption in Heat plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: ped_coal_for_heat_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share coal dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_dem_for_heatnc():
    """
    Share of coal demand to cover non-commercial heat consumption in Heat plants.
    """
    return zidz(ped_coal_heatnc(), ped_coal_ej())


@component.add(
    name="share solids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_solids(),
        ped_solids() - ped_coal_for_ctl_ej() - other_solids_required(),
    )
