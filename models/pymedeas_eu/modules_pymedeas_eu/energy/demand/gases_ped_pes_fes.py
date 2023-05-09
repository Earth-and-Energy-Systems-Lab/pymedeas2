"""
Module energy.demand.gases_ped_pes_fes
Translated using PySD version 3.10.0
"""


@component.add(
    name="abundance gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 3, "pes_gases": 2},
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
    name="check gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "pes_gases": 2},
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
    depends_on={"check_gases": 2},
)
def constrain_gas_exogenous_growth():
    """
    If negative, there is oversupply of gas. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


@component.add(
    name="FES total biogas",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_biogas_in_pes": 1, "real_fe_consumption_gases_ej": 1},
)
def fes_total_biogas():
    return share_biogas_in_pes() * real_fe_consumption_gases_ej()


@component.add(
    name='"Historic conv nat. gas domestic EU extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
        "__data__": "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
        "time": 1,
    },
)
def historic_conv_nat_gas_domestic_eu_extracted_ej():
    return _ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
)


@component.add(
    name='"Historic share conv. nat gas domestic EU extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_nat_gas_domestic_eu_extracted_ej": 2,
        "historic_unconv_nat_gas_domestic_eu_extracted_ej": 1,
    },
)
def historic_share_conv_nat_gas_domestic_eu_extraction():
    return zidz(
        historic_conv_nat_gas_domestic_eu_extracted_ej(),
        historic_conv_nat_gas_domestic_eu_extracted_ej()
        + historic_unconv_nat_gas_domestic_eu_extracted_ej(),
    )


@component.add(
    name='"Historic share conv. nat gas domestic EU extraction until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": {
            "initial": {"historic_share_conv_nat_gas_domestic_eu_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_conv_nat_gas_domestic_eu_extraction": 1,
            },
        }
    },
)
def historic_share_conv_nat_gas_domestic_eu_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()


_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016",
    )
)


@component.add(
    name='"Historic unconv nat. gas domestic EU extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
        "__data__": "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_nat_gas_domestic_eu_extracted_ej():
    return _ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
)


@component.add(
    name="imports EU conv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_eu_conv_gas_from_row_ej():
    return imports_eu_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()


@component.add(
    name='"imports EU nat. gas from RoW EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_gas_flux_eu": 1},
)
def imports_eu_nat_gas_from_row_ej():
    """
    ** Name should be changed as well, because the name does not make evident that we are talking about net imports. net gas flux EU IF THEN ELSE(Time<2016, "PED EU nat. gas from RoW", IF THEN ELSE(limit nat gas imports from RoW=1, "PED EU nat. gas from RoW", IF THEN ELSE (limit nat gas imports from RoW=2, MIN("PED EU nat. gas from RoW","Historic share net imports nat. gas until 2016" *"extraction nat. gas EJ World"), IF THEN ELSE(limit nat gas imports from RoW=3, MIN("PED EU nat. gas from RoW",adapt max share imports nat gas*"extraction nat. gas EJ World"), "PED EU nat. gas from RoW"))))
    """
    return net_gas_flux_eu()


@component.add(
    name="imports EU unconv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_eu_unconv_gas_from_row_ej():
    return imports_eu_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name="Other gases required",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 2,
        "energy_distr_losses_ff_ej": 2,
        "nonenergy_use_demand_by_final_fuel_ej": 2,
    },
)
def other_gases_required():
    return if_then_else(
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        < 0,
        lambda: 0,
        lambda: float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]),
    )


@component.add(
    name='"PEC nat. gas"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_eu": 1, "imports_eu_nat_gas_from_row_ej": 1},
)
def pec_nat_gas():
    return pes_nat_gas_eu() + imports_eu_nat_gas_from_row_ej()


@component.add(
    name='"PED domestic EU conv. nat. gas EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_domestic_eu_total_natgas_ej": 1,
        "historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": 1,
    },
)
def ped_domestic_eu_conv_nat_gas_ej():
    return (
        ped_domestic_eu_total_natgas_ej()
        * historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()
    )


@component.add(
    name='"PED domestic EU total nat.gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "imports_eu_nat_gas_from_row_ej": 1},
)
def ped_domestic_eu_total_natgas_ej():
    """
    # "PED nat. gas EJ"*("Historic share conv. nat gas domestic EU extraction until 2016"+"Historic share unconv. nat. gas domestric EU extraction until 2016" )
    """
    return np.maximum(0, ped_nat_gas_ej() - imports_eu_nat_gas_from_row_ej())


@component.add(
    name='"PED EU nat. gas from RoW"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "pes_nat_gas_eu": 1},
)
def ped_eu_nat_gas_from_row():
    return np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_eu())


@component.add(
    name="PED gases",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "pe_demand_gas_elec_plants_ej": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "other_gases_required": 1,
    },
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
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "pes_biogas_for_tfc": 1},
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


@component.add(
    name="PES gases",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_nat_gas": 1, "pes_biogas_for_tfc": 1},
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return pec_nat_gas() + pes_biogas_for_tfc()


@component.add(
    name="real FE consumption gases EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_gases": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "other_gases_required": 1,
        "share_gases_for_final_energy": 1,
    },
)
def real_fe_consumption_gases_ej():
    """
    Real final energy consumption by gases after accounting for energy availability.
    """
    return (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()


@component.add(
    name="Required FED by gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
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
    depends_on={"pes_biogas_for_tfc": 1, "pes_gases": 1},
)
def share_biogas_in_pes():
    return zidz(pes_biogas_for_tfc(), pes_gases())


@component.add(
    name='"share gases dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gas_heatnc": 1, "ped_nat_gas_for_gtl_ej": 1, "pes_gases": 1},
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
    depends_on={
        "required_fed_by_gas": 1,
        "other_gases_required": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "ped_gases": 1,
    },
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
    depends_on={"ped_nat_gas_ej": 2, "pe_demand_gas_elec_plants_ej": 1},
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
    depends_on={"ped_nat_gas_ej": 2, "ped_gases_for_heat_plants_ej": 1},
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
    name="share nat gas for Elec emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_demand_gas_elec_plants_ej": 1,
        "share_elec_gen_in_chp_nat_gas": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_elec_emissions_relevant():
    return (
        pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej() * share_elec_gen_in_chp_nat_gas()
    ) / ped_nat_gas_ej()


@component.add(
    name="share nat gas for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_nat_gas_ej": 1,
        "share_nat_gas_for_elec_emissions_relevant": 1,
        "share_nat_gas_for_gtl_emissions_relevant": 1,
        "share_nat_gas_for_heat_emissions_relevant": 1,
    },
)
def share_nat_gas_for_fc_emissions_relevant():
    return (
        1
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]) / ped_nat_gas_ej()
        - share_nat_gas_for_elec_emissions_relevant()
        - share_nat_gas_for_gtl_emissions_relevant()
        - share_nat_gas_for_heat_emissions_relevant()
    )


@component.add(
    name="share nat gas for GTL emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_for_gtl_ej": 1, "ped_nat_gas_ej": 1},
)
def share_nat_gas_for_gtl_emissions_relevant():
    return ped_nat_gas_for_gtl_ej() / ped_nat_gas_ej()


@component.add(
    name="share nat gas for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "share_elec_gen_in_chp_nat_gas": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_heat_emissions_relevant():
    return (
        ped_gases_for_heat_plants_ej()
        + ped_gas_heatnc()
        + ped_gas_for_chp_plants_ej() * (1 - share_elec_gen_in_chp_nat_gas())
    ) / ped_nat_gas_ej()


@component.add(
    name="Year scarcity gases",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 1, "time": 1},
)
def year_scarcity_gases():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
