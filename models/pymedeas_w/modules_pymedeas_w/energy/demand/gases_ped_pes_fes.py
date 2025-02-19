"""
Module energy.demand.gases_ped_pes_fes
Translated using PySD version 3.14.0
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
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_biogas_in_pes": 1, "real_fe_consumption_by_fuel": 1},
)
def fes_total_biogas():
    """
    Total biogas in final energy
    """
    return share_biogas_in_pes() * float(real_fe_consumption_by_fuel().loc["gases"])


@component.add(
    name="Other gases required",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def other_gases_required():
    return (
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
    )


@component.add(
    name="PED gases",
    units="EJ/year",
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
        "pes_biogas_ej": 1,
        "pes_biogas_for_tfc": 1,
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
        + other_gases_required()
        + pes_biogas_ej()
        - pes_biogas_for_tfc(),
    )


@component.add(
    name='"PED nat. gas EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gases": 1,
        "pes_biogas_ej": 1,
        "synthethic_fuel_generation_delayed": 1,
    },
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(
        0,
        ped_gases()
        - pes_biogas_ej()
        - sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETG"]]
            .rename({np.str_("E to synthetic"): "ETG!"}),
            dim=["ETG!"],
        ),
    )


@component.add(
    name="PES gases",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_nat_gas": 1,
        "synthethic_fuel_generation_delayed": 1,
        "pes_biogas_ej": 1,
    },
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return (
        pes_nat_gas()
        + sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETG"]]
            .rename({np.str_("E to synthetic"): "ETG!"}),
            dim=["ETG!"],
        )
        + pes_biogas_ej()
    )


@component.add(
    name="Required FED by gas",
    units="EJ/year",
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
    """
    Share of biogas in total gases primary energy
    """
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
        "ped_nat_gas_for_gtl_ej": 1,
        "other_gases_required": 1,
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
    return zidz(
        pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej() * share_elec_gen_in_chp_nat_gas(),
        ped_nat_gas_ej(),
    )


@component.add(
    name="share nat gas for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_gases": 2,
        "ped_nat_gas_ej": 1,
        "share_nat_gas_for_elec_emissions_relevant": 1,
        "share_nat_gas_for_gtl_emissions_relevant": 1,
        "share_nat_gas_for_heat_emissions_relevant": 1,
    },
)
def share_nat_gas_for_fc_emissions_relevant():
    """
    1-ZIDZ("Non-energy use demand by final fuel EJ"[gases],"PED nat. gas EJ")-share nat gas for Elec emissions relevant-share nat gas for GTL emissions relevant-share nat gas for Heat emissions relevant
    """
    return (
        1
        - zidz(float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]), ped_gases())
        * ped_nat_gas_ej()
        / ped_gases()
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
    return zidz(ped_nat_gas_for_gtl_ej(), ped_nat_gas_ej())


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
    return zidz(
        ped_gases_for_heat_plants_ej()
        + ped_gas_heatnc()
        + ped_gas_for_chp_plants_ej() * (1 - share_elec_gen_in_chp_nat_gas()),
        ped_nat_gas_ej(),
    )


@component.add(
    name="share nat gas PES",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas": 1, "pes_gases": 1},
)
def share_nat_gas_pes():
    return pes_nat_gas() / pes_gases()


@component.add(
    name="Year scarcity gases",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 1, "time": 1},
)
def year_scarcity_gases():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
