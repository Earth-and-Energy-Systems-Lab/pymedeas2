"""
Module boundary_variables.medeas_w
Translated using PySD version 3.10.0
"""


@component.add(
    name="abundance coal",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_coal"},
)
def abundance_coal():
    return _data_abundance_coal(time())


_data_abundance_coal = TabData("abundance coal", "abundance_coal", {}, "interpolate")


@component.add(
    name="abundance coal World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_coal": 1},
)
def abundance_coal_world():
    return abundance_coal()


@component.add(
    name="abundance total nat gas",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_total_nat_gas"},
)
def abundance_total_nat_gas():
    return _data_abundance_total_nat_gas(time())


_data_abundance_total_nat_gas = TabData(
    "abundance total nat gas", "abundance_total_nat_gas", {}, "interpolate"
)


@component.add(
    name='"abundance total nat. gas World"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_nat_gas": 1},
)
def abundance_total_nat_gas_world():
    return abundance_total_nat_gas()


@component.add(
    name="abundance total oil",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_abundance_total_oil"},
)
def abundance_total_oil():
    return _data_abundance_total_oil(time())


_data_abundance_total_oil = TabData(
    "abundance total oil", "abundance_total_oil", {}, "interpolate"
)


@component.add(
    name="abundance total oil World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_total_oil": 1},
)
def abundance_total_oil_world():
    return abundance_total_oil()


@component.add(
    name="Annual GDP growth rate",
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
    "Annual GDP growth rate", "annual_gdp_growth_rate", {}, "interpolate"
)


@component.add(
    name="Annual GDP growth rate World",
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
    name="extraction coal EJ",
    units="EJ",
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
    "extraction coal EJ", "extraction_coal_ej", {}, "interpolate"
)


@component.add(
    name="extraction coal EJ World",
    units="EJ",
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
    name='"extraction nat. gas EJ World"',
    units="EJ",
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
    name="Extraction oil EJ World",
    units="EJ",
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
    name="extraction uranium EJ",
    units="EJ",
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
    "extraction uranium EJ", "extraction_uranium_ej", {}, "interpolate"
)


@component.add(
    name="extraction uranium EJ World",
    units="EJ",
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
    name="PES nat gas",
    units="EJ",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_pes_nat_gas"},
)
def pes_nat_gas():
    """
    Global primary energy supply of natural gas. Source: global model.
    """
    return _data_pes_nat_gas(time())


_data_pes_nat_gas = TabData("PES nat gas", "pes_nat_gas", {}, "interpolate")


@component.add(
    name="PES oil EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_pes_oil_ej"},
)
def pes_oil_ej():
    """
    Global primary energy supply of oil. Source: global model.
    """
    return _data_pes_oil_ej(time())


_data_pes_oil_ej = TabData("PES oil EJ", "pes_oil_ej", {}, "interpolate")


@component.add(
    name="Real demand by sector",
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
    "Real demand by sector",
    "real_demand_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real demand by sector World",
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
    name="Real demand World",
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
    name="Real final energy by sector and fuel",
    units="EJ",
    subscripts=["final sources", "sectors"],
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
    "Real final energy by sector and fuel",
    "real_final_energy_by_sector_and_fuel",
    {
        "final sources": _subscript_dict["final sources"],
        "sectors": _subscript_dict["sectors"],
    },
    "interpolate",
)


@component.add(
    name="Real final energy by sector and fuel World",
    subscripts=["final sources", "sectors"],
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
    name="Real total output by sector",
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
    "Real total output by sector",
    "real_total_output_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real total output by sector World",
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
    name="share conv vs total gas extraction",
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
    "share conv vs total gas extraction",
    "share_conv_vs_total_gas_extraction",
    {},
    "interpolate",
)


@component.add(
    name="share conv vs total gas extraction World",
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
    name="share conv vs total oil extraction",
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
    "share conv vs total oil extraction",
    "share_conv_vs_total_oil_extraction",
    {},
    "interpolate",
)


@component.add(
    name="share conv vs total oil extraction World",
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
    name="share E losses CC",
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
    "share E losses CC", "share_e_losses_cc", {}, "interpolate"
)


@component.add(
    name="Temperature change",
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
    "Temperature change", "temperature_change", {}, "interpolate"
)


@component.add(
    name="Total extraction NRE EJ",
    units="EJ",
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
    "Total extraction NRE EJ", "total_extraction_nre_ej", {}, "interpolate"
)


@component.add(
    name="Total extraction NRE EJ World",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_extraction_nre_ej": 1},
)
def total_extraction_nre_ej_world():
    """
    Global total non-renewable primary energy extraction. Source: global model.
    """
    return total_extraction_nre_ej()
