"""
Module energy.demand_shares_ped_pes
Translated using PySD version 3.10.0
"""


@component.add(
    name="oil TFC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_liquids": 1, "share_oil_for_fc_emissions_relevant": 1},
)
def oil_tfc():
    return ped_nre_liquids() * share_oil_for_fc_emissions_relevant()


@component.add(
    name="share coal dem for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "ped_coal_elec_plants_ej": 1},
)
def share_coal_dem_for_elec():
    """
    Share of coal demand to cover electricity consumption in Elec plants.
    """
    return if_then_else(
        ped_coal_ej() > 0, lambda: ped_coal_elec_plants_ej() / ped_coal_ej(), lambda: 0
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
    name="share coal elec plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_elec_plants_ej": 1, "ped_coal_ej": 1},
)
def share_coal_elec_plants():
    return zidz(ped_coal_elec_plants_ej(), ped_coal_ej())


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
        "ped_coal_elec_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_elec_emissions_relevant():
    return zidz(
        ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej() * float(share_elec_gen_in_chp().loc["coal"]),
        ped_coal_ej(),
    )


@component.add(
    name="share coal for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_ej": 2,
        "ped_coal_for_conversion": 1,
        "share_fed_vs_nonenergy_solids": 1,
    },
)
def share_coal_for_fc_emissions_relevant():
    return (
        zidz(ped_coal_ej() - ped_coal_for_conversion(), ped_coal_ej())
        * share_fed_vs_nonenergy_solids()
    )


@component.add(
    name="share coal for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "share_elec_gen_in_chp": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_heat_emissions_relevant():
    return zidz(
        ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + ped_coal_for_chp_plants_ej()
        * (1 - float(share_elec_gen_in_chp().loc["coal"])),
        ped_coal_ej(),
    )


@component.add(
    name="share gas elec plants",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gas_elec_plants_ej": 1, "ped_nat_gas_ej": 1},
)
def share_gas_elec_plants():
    return zidz(ped_gas_elec_plants_ej(), ped_nat_gas_ej())


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
    name='"share liquids dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_heatnc": 1, "pes_liquids": 1},
)
def share_liquids_dem_for_heatnc():
    """
    Share of liquids demand for non-commercial Heat plants in relation to the total demand of liquids.
    """
    return zidz(ped_liquids_heatnc(), pes_liquids())


@component.add(
    name='"share nat. gas dem for Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 2, "ped_gas_elec_plants_ej": 1},
)
def share_nat_gas_dem_for_elec():
    """
    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gas_elec_plants_ej() / ped_nat_gas_ej(),
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
        "ped_gas_elec_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_elec_emissions_relevant():
    return zidz(
        ped_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        * float(share_elec_gen_in_chp().loc["natural gas"]),
        ped_nat_gas_ej(),
    )


@component.add(
    name="share nat gas for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 2,
        "ped_nat_gas_for_conversion": 1,
        "share_fed_vs_nonenergy": 1,
    },
)
def share_nat_gas_for_fc_emissions_relevant():
    return (
        zidz(ped_nat_gas_ej() - ped_nat_gas_for_conversion(), ped_nat_gas_ej())
        * share_fed_vs_nonenergy()
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
        "share_elec_gen_in_chp": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_heat_emissions_relevant():
    return zidz(
        ped_gases_for_heat_plants_ej()
        + ped_gas_heatnc()
        + ped_gas_for_chp_plants_ej()
        * (1 - float(share_elec_gen_in_chp().loc["natural gas"])),
        ped_nat_gas_ej(),
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
        lambda: zidz(ped_oil_elec_plants_ej(), ped_total_oil_ej()),
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
    name="share oil elec plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_oil_elec_plants_ej": 1, "ped_total_oil_ej": 1},
)
def share_oil_elec_plants():
    return zidz(ped_oil_elec_plants_ej(), ped_total_oil_ej())


@component.add(
    name="share oil for Elec emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_elec_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
    },
)
def share_oil_for_elec_emissions_relevant():
    return zidz(
        ped_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej() * float(share_elec_gen_in_chp().loc["oil"]),
        ped_total_oil_ej(),
    )


@component.add(
    name="share oil for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_liquids": 2,
        "ped_oil_for_conversion": 1,
        "share_fed_vs_nonenergy_liquids": 1,
    },
)
def share_oil_for_fc_emissions_relevant():
    return (
        zidz(ped_nre_liquids() - ped_oil_for_conversion(), ped_nre_liquids())
        * share_fed_vs_nonenergy_liquids()
    )


@component.add(
    name="share oil for heat CHP plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
        "share_elec_gen_in_chp": 1,
    },
)
def share_oil_for_heat_chp_plants():
    return zidz(ped_oil_for_chp_plants_ej(), ped_total_oil_ej()) * (
        1 - float(share_elec_gen_in_chp().loc["oil"])
    )


@component.add(
    name="share oil for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_heat_plants_ej": 1,
        "ped_liquids_heatnc": 1,
        "share_elec_gen_in_chp": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
    },
)
def share_oil_for_heat_emissions_relevant():
    return zidz(
        ped_oil_for_heat_plants_ej()
        + ped_liquids_heatnc()
        + ped_oil_for_chp_plants_ej() * (1 - float(share_elec_gen_in_chp().loc["oil"])),
        ped_total_oil_ej(),
    )
