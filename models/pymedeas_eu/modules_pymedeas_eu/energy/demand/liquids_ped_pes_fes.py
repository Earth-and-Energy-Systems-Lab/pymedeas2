"""
Module energy.demand.liquids_ped_pes_fes
Translated using PySD version 3.9.1
"""


@component.add(
    name="abundance liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_ej": 3, "pes_liquids_ej": 2},
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
    name="check liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_ej": 1, "pes_liquids_ej": 2},
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
    depends_on={"check_liquids": 2},
)
def constrain_liquids_exogenous_growth():
    """
    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > 0, lambda: 1, lambda: check_liquids())


@component.add(
    name="FES total biofuels",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_biofuel_in_pes": 1, "real_fe_consumption_liquids_ej": 1},
)
def fes_total_biofuels():
    return share_biofuel_in_pes() * real_fe_consumption_liquids_ej()


@component.add(
    name="Historic conv oil domestic EU extracted",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_oil_domestic_eu_extracted",
        "__data__": "_ext_data_historic_conv_oil_domestic_eu_extracted",
        "time": 1,
    },
)
def historic_conv_oil_domestic_eu_extracted():
    return _ext_data_historic_conv_oil_domestic_eu_extracted(time())


_ext_data_historic_conv_oil_domestic_eu_extracted = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_conventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_oil_domestic_eu_extracted",
)


@component.add(
    name='"Historic share conv. oil domestic EU extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_oil_domestic_eu_extracted": 2,
        "historic_unconv_oil_domestic_eu_extracted": 1,
    },
)
def historic_share_conv_oil_domestic_eu_extraction():
    return zidz(
        historic_conv_oil_domestic_eu_extracted(),
        historic_conv_oil_domestic_eu_extracted()
        + historic_unconv_oil_domestic_eu_extracted(),
    )


@component.add(
    name='"Historic share conv. oil domestic EU extraction\\" until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016": {
            "initial": {"historic_share_conv_oil_domestic_eu_extraction": 1},
            "step": {"time": 1, "historic_share_conv_oil_domestic_eu_extraction": 1},
        }
    },
)
def historic_share_conv_oil_domestic_eu_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016()


_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_conv_oil_domestic_eu_extraction(),
    lambda: historic_share_conv_oil_domestic_eu_extraction(),
    "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016",
)


@component.add(
    name="Historic unconv oil domestic EU extracted",
    units="EJ/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_oil_domestic_eu_extracted",
        "__data__": "_ext_data_historic_unconv_oil_domestic_eu_extracted",
        "time": 1,
    },
)
def historic_unconv_oil_domestic_eu_extracted():
    """
    Historic unconventional extraction from Mohr et al (2015).
    """
    return _ext_data_historic_unconv_oil_domestic_eu_extracted(time())


_ext_data_historic_unconv_oil_domestic_eu_extracted = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_oil_domestic_eu_extracted",
)


@component.add(
    name="imports EU conv oil from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_eu_conv_oil_from_row_ej():
    return (
        imports_eu_total_oil_from_row_ej() * share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name="imports EU total oil from RoW EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_oil_flux_eu": 1},
)
def imports_eu_total_oil_from_row_ej():
    """
    ** Name should be changed as well, because the name does not make evident that we are talking about net imports. net oil flux EU IF THEN ELSE(Time<2016, PED EU total oil from RoW, IF THEN ELSE(limit oil imports from RoW=1, PED EU total oil from RoW, IF THEN ELSE (limit oil imports from RoW=2, MIN(PED EU total oil from RoW,Historic share net imports oil until 2016 *Extraction oil EJ World), IF THEN ELSE(limit oil imports from RoW=3, MIN(PED EU total oil from RoW,adapt max share imports oil*Extraction oil EJ World ), PED EU total oil from RoW))))
    """
    return net_oil_flux_eu()


@component.add(
    name="imports EU unconv oil from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_eu_unconv_oil_from_row_ej():
    return imports_eu_total_oil_from_row_ej() * (
        1 - share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name="Other liquids required EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_distr_losses_ff_ej": 1,
        "transformation_ff_losses_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def other_liquids_required_ej():
    return (
        float(energy_distr_losses_ff_ej().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
    )


@component.add(
    name="Other liquids supply EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_refinery_gains_ej": 1,
        "fes_ctlgtl_ej": 1,
        "fes_total_biofuels_production_ej": 1,
    },
)
def other_liquids_supply_ej():
    """
    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_production_ej()
    )


@component.add(
    name="PEC total oil",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_total_oil_ej_eu": 1, "imports_eu_total_oil_from_row_ej": 1},
)
def pec_total_oil():
    return pes_total_oil_ej_eu() + imports_eu_total_oil_from_row_ej()


@component.add(
    name='"PED domestic EU conv. oil EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_domestic_eu_total_oil_ej": 1,
        "historic_share_conv_oil_domestic_eu_extraction_until_2016": 1,
    },
)
def ped_domestic_eu_conv_oil_ej():
    return (
        ped_domestic_eu_total_oil_ej()
        * historic_share_conv_oil_domestic_eu_extraction_until_2016()
    )


@component.add(
    name="PED domestic EU total oil EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "imports_eu_total_oil_from_row_ej": 1},
)
def ped_domestic_eu_total_oil_ej():
    """
    Factor to inspect: PED total oil*("Historic share conv. oil domestic EU extraction
    " until 2016"+"Historic share unconv. oil domestric EU extraction until 2016" )
    """
    return np.maximum(0, ped_total_oil_ej() - imports_eu_total_oil_from_row_ej())


@component.add(
    name='"PED domestic EU unconv. oil EJ"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_domestic_eu_total_oil_ej": 1, "ped_domestic_eu_conv_oil_ej": 1},
)
def ped_domestic_eu_unconv_oil_ej():
    return ped_domestic_eu_total_oil_ej() - ped_domestic_eu_conv_oil_ej()


@component.add(
    name="PED liquids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids_ej": 1,
        "other_liquids_required_ej": 1,
        "ped_oil_elec_plants_ej": 1,
        "ped_oil_for_heat_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_liquids_heatnc": 1,
    },
)
def ped_liquids_ej():
    """
    Primary energy demand of total liquids.
    """
    return np.maximum(
        0,
        required_fed_by_liquids_ej()
        + other_liquids_required_ej()
        + ped_oil_elec_plants_ej()
        + ped_oil_for_heat_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_liquids_heatnc(),
    )


@component.add(
    name="PED NRE Liquids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_ej": 1, "fes_total_biofuels_production_ej": 1},
)
def ped_nre_liquids():
    """
    Primary energy demand of non-renewable energy for the production of liquids.
    """
    return np.maximum(0, ped_liquids_ej() - fes_total_biofuels_production_ej())


@component.add(
    name="PED total oil EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_liquids": 1, "fes_ctlgtl_ej": 1, "oil_refinery_gains_ej": 1},
)
def ped_total_oil_ej():
    """
    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


@component.add(
    name="PES Liquids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "other_liquids_supply_ej": 1},
)
def pes_liquids_ej():
    """
    Total primary supply of liquids.
    """
    return pec_total_oil() + other_liquids_supply_ej()


@component.add(
    name="real FE consumption liquids EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_liquids_ej": 1,
        "other_liquids_required_ej": 1,
        "share_liquids_for_final_energy": 1,
    },
)
def real_fe_consumption_liquids_ej():
    """
    Real final energy consumption by liquids after accounting for energy availability.
    """
    return (
        pes_liquids_ej() - other_liquids_required_ej()
    ) * share_liquids_for_final_energy()


@component.add(
    name="Required FED by liquids EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
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
    depends_on={"fes_total_biofuels_production_ej": 1, "pes_liquids_ej": 1},
)
def share_biofuel_in_pes():
    return zidz(fes_total_biofuels_production_ej(), pes_liquids_ej())


@component.add(
    name='"share liquids dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_heatnc": 1, "pes_liquids_ej": 1},
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
    depends_on={
        "required_fed_by_liquids_ej": 1,
        "other_liquids_required_ej": 1,
        "ped_liquids_ej": 1,
    },
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
    depends_on={"ped_total_oil_ej": 2, "ped_oil_elec_plants_ej": 1},
)
def share_oil_dem_for_elec():
    """
    Share of oil demand to cover electricity consumption.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_elec_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


@component.add(
    name='"share oil dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 2, "ped_oil_for_heat_plants_ej": 1},
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
    name="share oil for Elec emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_elec_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp_oil": 1,
        "ped_total_oil_ej": 1,
    },
)
def share_oil_for_elec_emissions_relevant():
    return zidz(
        ped_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej() * share_elec_gen_in_chp_oil(),
        ped_total_oil_ej(),
    )


@component.add(
    name="share oil for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_total_oil_ej": 1,
        "share_oil_for_elec_emissions_relevant": 1,
        "share_oil_for_heat_emissions_relevant": 1,
    },
)
def share_oil_for_fc_emissions_relevant():
    return (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]),
            ped_total_oil_ej(),
        )
        - share_oil_for_elec_emissions_relevant()
        - share_oil_for_heat_emissions_relevant()
    )


@component.add(
    name="share oil for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_heat_plants_ej": 1,
        "ped_liquids_heatnc": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp_oil": 1,
        "ped_total_oil_ej": 1,
    },
)
def share_oil_for_heat_emissions_relevant():
    return zidz(
        ped_oil_for_heat_plants_ej()
        + ped_liquids_heatnc()
        + ped_oil_for_chp_plants_ej() * (1 - share_elec_gen_in_chp_oil()),
        ped_total_oil_ej(),
    )


@component.add(
    name='"Total demand liquids mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_ej": 1, "mbd_per_ejyear": 1},
)
def total_demand_liquids_mbd():
    """
    Total demand of liquids.
    """
    return ped_liquids_ej() * mbd_per_ejyear()


@component.add(
    name="Year scarcity liquids",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_liquids": 1, "time": 1},
)
def year_scarcity_liquids():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())
