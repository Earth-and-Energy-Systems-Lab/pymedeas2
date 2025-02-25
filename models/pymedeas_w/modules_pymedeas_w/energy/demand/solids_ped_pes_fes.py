"""
Module energy.demand.solids_ped_pes_fes
Translated using PySD version 3.14.0
"""

@component.add(
    name="a lin reg peat",
    units="EJ/(year*year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def a_lin_reg_peat():
    return -0.00382044


@component.add(
    name="abundance solids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids": 2, "ped_solids": 3},
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
    name="b lin reg peat", units="EJ/year", comp_type="Constant", comp_subtype="Normal"
)
def b_lin_reg_peat():
    return 7.83322


@component.add(
    name="Historic PES peat EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_pes_peat_ej",
        "__data__": "_ext_data_historic_pes_peat_ej",
        "time": 1,
    },
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
    name="modern solid bioenergy",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4, "policy_modern_solid_bioe": 3},
)
def modern_solid_bioenergy():
    """
    IF THEN ELSE(Time<2015, 0, IF THEN ELSE(Time<2020,policy modern solid bioE(2020)*Time/5-2015*policy modern solid bioE(2020)/5,policy modern solid bioE(Time)))
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: if_then_else(
            time() < 2020,
            lambda: policy_modern_solid_bioe(2020) * time() / 5
            - 2015 * policy_modern_solid_bioe(2020) / 5,
            lambda: policy_modern_solid_bioe(time()),
        ),
    )


@component.add(
    name="Other solids required",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def other_solids_required():
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff_ej().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


@component.add(
    name="PED coal EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_solids": 1,
        "losses_in_charcoal_plants_historic": 1,
        "pe_traditional_biomass_ej_delayed": 1,
        "pes_peat": 1,
        "pes_waste": 1,
        "modern_solid_bioenergy": 1,
    },
)
def ped_coal_ej():
    """
    Primary energy demand of coal.
    """
    return np.maximum(
        0,
        ped_solids()
        - (
            pe_traditional_biomass_ej_delayed()
            + pes_peat()
            - losses_in_charcoal_plants_historic()
            + pes_waste()
            + modern_solid_bioenergy()
        ),
    )


@component.add(
    name="PED solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_solids": 1,
        "ped_coal_for_ctl_ej": 2,
        "pe_demand_coal_elec_plants_ej": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "other_solids_required": 1,
        "pes_waste": 1,
        "pes_res_for_heatnc_by_techn": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pe_real_generation_res_elec": 1,
        "pes_waste_for_tfc": 1,
    },
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
        + other_solids_required()
        + pes_waste()
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + ped_coal_for_ctl_ej()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        - pes_waste_for_tfc(),
    )


@component.add(
    name="PES peat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_pes_peat_ej": 1,
        "a_lin_reg_peat": 1,
        "b_lin_reg_peat": 1,
    },
)
def pes_peat():
    """
    MAX(IF THEN ELSE(Time<2014, Historic PES peat EJ, a lin reg peat*(Time)+b lin reg peat),0)
    """
    return np.maximum(
        if_then_else(
            time() < 2014,
            lambda: historic_pes_peat_ej(),
            lambda: a_lin_reg_peat() * time() + b_lin_reg_peat(),
        ),
        0,
    )


@component.add(
    name="PES solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_ej": 1,
        "pe_traditional_biomass_ej_delayed": 1,
        "pes_peat": 1,
        "losses_in_charcoal_plants_historic": 1,
        "pes_waste": 1,
        "modern_solid_bioenergy": 1,
    },
)
def pes_solids():
    """
    Primary energy supply solids.
    """
    return (
        extraction_coal_ej()
        + pe_traditional_biomass_ej_delayed()
        + pes_peat()
        - losses_in_charcoal_plants_historic()
        + pes_waste()
        + modern_solid_bioenergy()
    )


@component.add(
    name="policy modern solid bioE",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_modern_solid_bioe",
        "__lookup__": "_ext_lookup_policy_modern_solid_bioe",
    },
)
def policy_modern_solid_bioe(x, final_subs=None):
    return _ext_lookup_policy_modern_solid_bioe(x, final_subs)


_ext_lookup_policy_modern_solid_bioe = ExtLookup(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_solid_bioe",
    {},
    _root,
    {},
    "_ext_lookup_policy_modern_solid_bioe",
)


@component.add(
    name="Required FED solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
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
    depends_on={"ped_coal_ej": 2, "pe_demand_coal_elec_plants_ej": 1},
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
    depends_on={"ped_coal_ej": 2, "ped_coal_for_heat_plants_ej": 1},
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
    depends_on={"ped_coal_heatnc": 1, "ped_coal_ej": 1},
)
def share_coal_dem_for_heatnc():
    """
    Share of coal demand to cover non-commercial heat consumption in Heat plants.
    """
    return zidz(ped_coal_heatnc(), ped_coal_ej())


@component.add(
    name="share coal for CTL emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl_ej": 1, "ped_coal_ej": 1},
)
def share_coal_for_ctl_emissions_relevant():
    return zidz(ped_coal_for_ctl_ej(), ped_coal_ej())


@component.add(
    name="share coal for Elec emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_demand_coal_elec_plants_ej": 1,
        "share_elec_gen_in_chp_coal": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_elec_emissions_relevant():
    return zidz(
        pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej() * share_elec_gen_in_chp_coal(),
        ped_coal_ej(),
    )


@component.add(
    name="share coal for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_coal_ej": 1,
        "share_coal_for_ctl_emissions_relevant": 1,
        "share_coal_for_elec_emissions_relevant": 1,
        "share_coal_for_heat_emissions_relevant": 1,
    },
)
def share_coal_for_fc_emissions_relevant():
    return (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]), ped_coal_ej()
        )
        - share_coal_for_ctl_emissions_relevant()
        - share_coal_for_elec_emissions_relevant()
        - share_coal_for_heat_emissions_relevant()
    )


@component.add(
    name="share coal for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "share_elec_gen_in_chp_coal": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_heat_emissions_relevant():
    return zidz(
        ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + ped_coal_for_chp_plants_ej() * (1 - share_elec_gen_in_chp_coal()),
        ped_coal_ej(),
    )


@component.add(
    name="share solids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_solids": 1,
        "ped_solids": 1,
        "ped_coal_for_ctl_ej": 1,
        "other_solids_required": 1,
    },
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_solids(),
        ped_solids() - ped_coal_for_ctl_ej() - other_solids_required(),
    )
