"""
Module boundary_variables.medeas_w
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_coal",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_coal"},
)
def abundance_coal():
    return _data_abundance_coal(time())


_data_abundance_coal = TabData("abundance_coal", "abundance_coal", {}, "interpolate")


@component.add(
    name="abundance_coal_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_coal": 1},
)
def abundance_coal_world():
    return abundance_coal()


@component.add(
    name="abundance_total_nat_gas",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_total_nat_gas"},
)
def abundance_total_nat_gas():
    return _data_abundance_total_nat_gas(time())


_data_abundance_total_nat_gas = TabData(
    "abundance_total_nat_gas", "abundance_total_nat_gas", {}, "interpolate"
)


@component.add(
    name='"abundance_total_nat._gas_World"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_nat_gas": 1},
)
def abundance_total_nat_gas_world():
    return abundance_total_nat_gas()


@component.add(
    name="abundance_total_oil",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_total_oil"},
)
def abundance_total_oil():
    return _data_abundance_total_oil(time())


_data_abundance_total_oil = TabData(
    "abundance_total_oil", "abundance_total_oil", {}, "interpolate"
)


@component.add(
    name="abundance_total_oil_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_oil": 1},
)
def abundance_total_oil_world():
    return abundance_total_oil()


@component.add(
    name="Annual_GDP_growth_rate",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_annual_gdp_growth_rate"},
)
def annual_gdp_growth_rate():
    """
    Annual GDP growth rate. Source: global model.
    """
    return _data_annual_gdp_growth_rate(time())


_data_annual_gdp_growth_rate = TabData(
    "Annual_GDP_growth_rate", "annual_gdp_growth_rate", {}, "interpolate"
)


@component.add(
    name="Annual_GDP_growth_rate_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_gdp_growth_rate": 1},
)
def annual_gdp_growth_rate_world():
    """
    Annual GDP growth rate. Source: global model.
    """
    return annual_gdp_growth_rate()


@component.add(
    name="extraction_coal_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_extraction_coal_ej"},
)
def extraction_coal_ej():
    """
    Global primary energy supply. Source: global model.
    """
    return _data_extraction_coal_ej(time())


_data_extraction_coal_ej = TabData(
    "extraction_coal_EJ", "extraction_coal_ej", {}, "interpolate"
)


@component.add(
    name="extraction_coal_EJ_World",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej": 1},
)
def extraction_coal_ej_world():
    """
    Global primary energy supply. Source: global model.
    """
    return extraction_coal_ej()


@component.add(
    name='"extraction_nat._gas_EJ_World"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas": 1},
)
def extraction_nat_gas_ej_world():
    """
    Global primary energy supply of natural gas. Source: global model.
    """
    return pes_nat_gas()


@component.add(
    name="Extraction_oil_EJ_World",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_oil_ej": 1},
)
def extraction_oil_ej_world():
    """
    Global primary energy supply of oil. Source: global model.
    """
    return pes_oil_ej()


@component.add(
    name="extraction_uranium_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_extraction_uranium_ej"},
)
def extraction_uranium_ej():
    """
    Global uranium extracted. Source: global model.
    """
    return _data_extraction_uranium_ej(time())


_data_extraction_uranium_ej = TabData(
    "extraction_uranium_EJ", "extraction_uranium_ej", {}, "interpolate"
)


@component.add(
    name="extraction_uranium_EJ_World",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_uranium_ej": 1},
)
def extraction_uranium_ej_world():
    """
    Global uranium extracted. Source: global model.
    """
    return extraction_uranium_ej()


@component.add(
    name="PES_nat_gas",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_pes_nat_gas"},
)
def pes_nat_gas():
    """
    Global primary energy supply of natural gas. Source: global model.
    """
    return _data_pes_nat_gas(time())


_data_pes_nat_gas = TabData("PES_nat_gas", "pes_nat_gas", {}, "interpolate")


@component.add(
    name="PES_oil_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_pes_oil_ej"},
)
def pes_oil_ej():
    """
    Global primary energy supply of oil. Source: global model.
    """
    return _data_pes_oil_ej(time())


_data_pes_oil_ej = TabData("PES_oil_EJ", "pes_oil_ej", {}, "interpolate")


@component.add(
    name="Real_demand_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_demand_by_sector"},
)
def real_demand_by_sector():
    """
    Real demand by sector. Source: global model.
    """
    return _data_real_demand_by_sector(time())


_data_real_demand_by_sector = TabData(
    "Real_demand_by_sector",
    "real_demand_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real_demand_by_sector_World",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_by_sector": 1},
)
def real_demand_by_sector_world():
    """
    Real demand by sector. Source: global model.
    """
    return real_demand_by_sector()


@component.add(
    name="Real_demand_World",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_by_sector_world": 1},
)
def real_demand_world():
    """
    Total World final demand (MEDEAS-World).
    """
    return sum(
        real_demand_by_sector_world().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="Real_final_energy_by_sector_and_fuel",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_final_energy_by_sector_and_fuel"},
)
def real_final_energy_by_sector_and_fuel():
    """
    Real final energy consumed by sector and fuel. Source: global model.
    """
    return _data_real_final_energy_by_sector_and_fuel(time())


_data_real_final_energy_by_sector_and_fuel = TabData(
    "Real_final_energy_by_sector_and_fuel",
    "real_final_energy_by_sector_and_fuel",
    {
        "final_sources": _subscript_dict["final_sources"],
        "sectors": _subscript_dict["sectors"],
    },
    "interpolate",
)


@component.add(
    name="Real_final_energy_by_sector_and_fuel_World",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_energy_by_sector_and_fuel": 1},
)
def real_final_energy_by_sector_and_fuel_world():
    """
    Real final energy consumed by sector and fuel. Source: global model.
    """
    return real_final_energy_by_sector_and_fuel()


@component.add(
    name="Real_total_output_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_total_output_by_sector"},
)
def real_total_output_by_sector():
    """
    Real total output by sector. Source: global model.
    """
    return _data_real_total_output_by_sector(time())


_data_real_total_output_by_sector = TabData(
    "Real_total_output_by_sector",
    "real_total_output_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real_total_output_by_sector_World",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_sector": 1},
)
def real_total_output_by_sector_world():
    """
    Real total output by sector. Source: global model.
    """
    return real_total_output_by_sector()


@component.add(
    name="share_conv_vs_total_gas_extraction",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_share_conv_vs_total_gas_extraction"},
)
def share_conv_vs_total_gas_extraction():
    """
    Share of global conventional vs global total (unconventional + conventional) gas extraction. Source: global model.
    """
    return _data_share_conv_vs_total_gas_extraction(time())


_data_share_conv_vs_total_gas_extraction = TabData(
    "share_conv_vs_total_gas_extraction",
    "share_conv_vs_total_gas_extraction",
    {},
    "interpolate",
)


@component.add(
    name="share_conv_vs_total_gas_extraction_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_conv_vs_total_gas_extraction": 1},
)
def share_conv_vs_total_gas_extraction_world():
    """
    Share of global conventional vs global total (unconventional + conventional) gas extraction. Source: global model.
    """
    return share_conv_vs_total_gas_extraction()


@component.add(
    name="share_conv_vs_total_oil_extraction",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_share_conv_vs_total_oil_extraction"},
)
def share_conv_vs_total_oil_extraction():
    """
    Share of global conventional vs global total (unconventional + conventional) oil extraction. Source: global model.
    """
    return _data_share_conv_vs_total_oil_extraction(time())


_data_share_conv_vs_total_oil_extraction = TabData(
    "share_conv_vs_total_oil_extraction",
    "share_conv_vs_total_oil_extraction",
    {},
    "interpolate",
)


@component.add(
    name="share_conv_vs_total_oil_extraction_World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_conv_vs_total_oil_extraction": 1},
)
def share_conv_vs_total_oil_extraction_world():
    """
    Share of global conventional vs global total (unconventional + conventional) oil extraction. Source: global model.
    """
    return share_conv_vs_total_oil_extraction()


@component.add(
    name="share_E_losses_CC",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_share_e_losses_cc"},
)
def share_e_losses_cc():
    """
    Energy losses due to climate change impacts. Source: global model.
    """
    return _data_share_e_losses_cc(time())


_data_share_e_losses_cc = TabData(
    "share_E_losses_CC", "share_e_losses_cc", {}, "interpolate"
)


@component.add(
    name="Temperature_change",
    units="DegreesC",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_temperature_change"},
)
def temperature_change():
    """
    Temperature change. Source: global model.
    """
    return _data_temperature_change(time())


_data_temperature_change = TabData(
    "Temperature_change", "temperature_change", {}, "interpolate"
)


@component.add(
    name="Total_extraction_NRE_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_total_extraction_nre_ej"},
)
def total_extraction_nre_ej():
    """
    Global total non-renewable primary energy extraction. Source: global model.
    """
    return _data_total_extraction_nre_ej(time())


_data_total_extraction_nre_ej = TabData(
    "Total_extraction_NRE_EJ", "total_extraction_nre_ej", {}, "interpolate"
)


@component.add(
    name="Total_extraction_NRE_EJ_World",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_extraction_nre_ej": 1},
)
def total_extraction_nre_ej_world():
    """
    Global total non-renewable primary energy extraction. Source: global model.
    """
    return total_extraction_nre_ej()
