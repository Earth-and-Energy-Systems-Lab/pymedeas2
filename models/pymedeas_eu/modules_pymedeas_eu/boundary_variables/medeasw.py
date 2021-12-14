"""
Module medeasw
Translated using PySD version 2.1.0
"""


def abundance_coal():
    """
    Real Name: abundance coal
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None


    """
    return _data_abundance_coal(time())


def abundance_coal_world():
    """
    Real Name: abundance coal World
    Original Eqn: abundance coal
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return abundance_coal()


def abundance_total_nat_gas():
    """
    Real Name: abundance total nat gas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None


    """
    return _data_abundance_total_nat_gas(time())


def abundance_total_nat_gas_world():
    """
    Real Name: "abundance total nat. gas World"
    Original Eqn: abundance total nat gas
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return abundance_total_nat_gas()


def abundance_total_oil():
    """
    Real Name: abundance total oil
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None


    """
    return _data_abundance_total_oil(time())


def abundance_total_oil_world():
    """
    Real Name: abundance total oil World
    Original Eqn: abundance total oil
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return abundance_total_oil()


def annual_gdp_growth_rate():
    """
    Real Name: Annual GDP growth rate
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Annual GDP growth rate. Source: global model.
    """
    return _data_annual_gdp_growth_rate(time())


def annual_gdp_growth_rate_world():
    """
    Real Name: Annual GDP growth rate World
    Original Eqn: Annual GDP growth rate
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual GDP growth rate. Source: global model.
    """
    return annual_gdp_growth_rate()


def extraction_coal_ej():
    """
    Real Name: extraction coal EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Global primary energy supply. Source: global model.
    """
    return _data_extraction_coal_ej(time())


def extraction_coal_ej_world():
    """
    Real Name: extraction coal EJ World
    Original Eqn: extraction coal EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Global primary energy supply. Source: global model.
    """
    return extraction_coal_ej()


def extraction_nat_gas_ej_world():
    """
    Real Name: "extraction nat. gas EJ World"
    Original Eqn: PES nat gas
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Global primary energy supply of natural gas. Source: global model.
    """
    return pes_nat_gas()


def extraction_oil_ej_world():
    """
    Real Name: Extraction oil EJ World
    Original Eqn: PES oil EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Global primary energy supply of oil. Source: global model.
    """
    return pes_oil_ej()


def extraction_uranium_ej():
    """
    Real Name: extraction uranium EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Global uranium extracted. Source: global model.
    """
    return _data_extraction_uranium_ej(time())


def extraction_uranium_ej_world():
    """
    Real Name: extraction uranium EJ World
    Original Eqn: extraction uranium EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Global uranium extracted. Source: global model.
    """
    return extraction_uranium_ej()


def pes_nat_gas():
    """
    Real Name: PES nat gas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Global primary energy supply of natural gas. Source: global model.
    """
    return _data_pes_nat_gas(time())


def pes_oil_ej():
    """
    Real Name: PES oil EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Global primary energy supply of oil. Source: global model.
    """
    return _data_pes_oil_ej(time())


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector():
    """
    Real Name: Real demand by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: data
    Subs: ['sectors']

    Real demand by sector. Source: global model.
    """
    return _data_real_demand_by_sector(time())


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_world():
    """
    Real Name: Real demand by sector World
    Original Eqn: Real demand by sector[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real demand by sector. Source: global model.
    """
    return real_demand_by_sector()


def real_demand_world():
    """
    Real Name: Real demand World
    Original Eqn: SUM(Real demand by sector World[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total World final demand (MEDEAS-World).
    """
    return sum(real_demand_by_sector_world(), dim=("sectors",))


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel():
    """
    Real Name: Real final energy by sector and fuel
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: ['final sources', 'sectors']

    Real final energy consumed by sector and fuel. Source: global model.
    """
    return _data_real_final_energy_by_sector_and_fuel(time())


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_world():
    """
    Real Name: Real final energy by sector and fuel World
    Original Eqn: Real final energy by sector and fuel[final sources,sectors]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real final energy consumed by sector and fuel. Source: global model.
    """
    return real_final_energy_by_sector_and_fuel()


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector():
    """
    Real Name: Real total output by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: data
    Subs: ['sectors']

    Real total output by sector. Source: global model.
    """
    return _data_real_total_output_by_sector(time())


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_world():
    """
    Real Name: Real total output by sector World
    Original Eqn: Real total output by sector[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real total output by sector. Source: global model.
    """
    return real_total_output_by_sector()


def share_conv_vs_total_gas_extraction():
    """
    Real Name: share conv vs total gas extraction
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Share of global conventional vs global total (unconventional +
        conventional) gas extraction. Source: global model.
    """
    return _data_share_conv_vs_total_gas_extraction(time())


def share_conv_vs_total_gas_extraction_world():
    """
    Real Name: share conv vs total gas extraction World
    Original Eqn: share conv vs total gas extraction
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of global conventional vs global total (unconventional +
        conventional) gas extraction. Source: global model.
    """
    return share_conv_vs_total_gas_extraction()


def share_conv_vs_total_oil_extraction():
    """
    Real Name: share conv vs total oil extraction
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Share of global conventional vs global total (unconventional +
        conventional) oil extraction. Source: global model.
    """
    return _data_share_conv_vs_total_oil_extraction(time())


def share_conv_vs_total_oil_extraction_world():
    """
    Real Name: share conv vs total oil extraction World
    Original Eqn: share conv vs total oil extraction
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of global conventional vs global total (unconventional +
        conventional) oil extraction. Source: global model.
    """
    return share_conv_vs_total_oil_extraction()


def share_e_losses_cc():
    """
    Real Name: share E losses CC
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None

    Energy losses due to climate change impacts. Source: global model.
    """
    return _data_share_e_losses_cc(time())


def temperature_change():
    """
    Real Name: Temperature change
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: data
    Subs: None

    Temperature change. Source: global model.
    """
    return _data_temperature_change(time())


def total_extraction_nre_ej():
    """
    Real Name: Total extraction NRE EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: data
    Subs: None

    Global total non-renewable primary energy extraction. Source: global model.
    """
    return _data_total_extraction_nre_ej(time())


def total_extraction_nre_ej_world():
    """
    Real Name: Total extraction NRE EJ World
    Original Eqn: Total extraction NRE EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Global total non-renewable primary energy extraction. Source: global model.
    """
    return total_extraction_nre_ej()


_data_abundance_coal = TabData("abundance coal", "abundance_coal", {}, "interpolate")


_data_abundance_total_nat_gas = TabData(
    "abundance total nat gas", "abundance_total_nat_gas", {}, "interpolate"
)


_data_abundance_total_oil = TabData(
    "abundance total oil", "abundance_total_oil", {}, "interpolate"
)


_data_annual_gdp_growth_rate = TabData(
    "Annual GDP growth rate", "annual_gdp_growth_rate", {}, "interpolate"
)


_data_extraction_coal_ej = TabData(
    "extraction coal EJ", "extraction_coal_ej", {}, "interpolate"
)


_data_extraction_uranium_ej = TabData(
    "extraction uranium EJ", "extraction_uranium_ej", {}, "interpolate"
)


_data_pes_nat_gas = TabData("PES nat gas", "pes_nat_gas", {}, "interpolate")


_data_pes_oil_ej = TabData("PES oil EJ", "pes_oil_ej", {}, "interpolate")


_data_real_demand_by_sector = TabData(
    "Real demand by sector",
    "real_demand_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


_data_real_final_energy_by_sector_and_fuel = TabData(
    "Real final energy by sector and fuel",
    "real_final_energy_by_sector_and_fuel",
    {
        "final sources": _subscript_dict["final sources"],
        "sectors": _subscript_dict["sectors"],
    },
    "interpolate",
)


_data_real_total_output_by_sector = TabData(
    "Real total output by sector",
    "real_total_output_by_sector",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


_data_share_conv_vs_total_gas_extraction = TabData(
    "share conv vs total gas extraction",
    "share_conv_vs_total_gas_extraction",
    {},
    "interpolate",
)


_data_share_conv_vs_total_oil_extraction = TabData(
    "share conv vs total oil extraction",
    "share_conv_vs_total_oil_extraction",
    {},
    "interpolate",
)


_data_share_e_losses_cc = TabData(
    "share E losses CC", "share_e_losses_cc", {}, "interpolate"
)


_data_temperature_change = TabData(
    "Temperature change", "temperature_change", {}, "interpolate"
)


_data_total_extraction_nre_ej = TabData(
    "Total extraction NRE EJ", "total_extraction_nre_ej", {}, "interpolate"
)
