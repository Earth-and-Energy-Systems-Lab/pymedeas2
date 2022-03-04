"""
Module medeas_w
Translated using PySD version 2.2.1
"""


def abundance_coal():
    """
    Real Name: abundance coal
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_abundance_coal(time())


_data_abundance_coal = TabData("abundance coal", "abundance_coal", {}, "interpolate")


def abundance_coal_world():
    """
    Real Name: abundance coal World
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return abundance_coal()


def abundance_total_nat_gas():
    """
    Real Name: abundance total nat gas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_abundance_total_nat_gas(time())


_data_abundance_total_nat_gas = TabData(
    "abundance total nat gas", "abundance_total_nat_gas", {}, "interpolate"
)


def abundance_total_nat_gas_world():
    """
    Real Name: "abundance total nat. gas World"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return abundance_total_nat_gas()


def abundance_total_oil():
    """
    Real Name: abundance total oil
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_abundance_total_oil(time())


_data_abundance_total_oil = TabData(
    "abundance total oil", "abundance_total_oil", {}, "interpolate"
)


def abundance_total_oil_world():
    """
    Real Name: abundance total oil World
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return abundance_total_oil()


def annual_gdp_growth_rate():
    """
    Real Name: Annual GDP growth rate
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Annual GDP growth rate. Source: global model.
    """
    return _data_annual_gdp_growth_rate(time())


_data_annual_gdp_growth_rate = TabData(
    "Annual GDP growth rate", "annual_gdp_growth_rate", {}, "interpolate"
)


def annual_gdp_growth_rate_world():
    """
    Real Name: Annual GDP growth rate World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual GDP growth rate. Source: global model.
    """
    return annual_gdp_growth_rate()


def extraction_coal_ej():
    """
    Real Name: extraction coal EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Global primary energy supply. Source: global model.
    """
    return _data_extraction_coal_ej(time())


_data_extraction_coal_ej = TabData(
    "extraction coal EJ", "extraction_coal_ej", {}, "interpolate"
)


def extraction_coal_ej_world():
    """
    Real Name: extraction coal EJ World
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global primary energy supply. Source: global model.
    """
    return extraction_coal_ej()


def extraction_nat_gas_ej_world():
    """
    Real Name: "extraction nat. gas EJ World"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global primary energy supply of natural gas. Source: global model.
    """
    return pes_nat_gas()


def extraction_oil_ej_world():
    """
    Real Name: Extraction oil EJ World
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global primary energy supply of oil. Source: global model.
    """
    return pes_oil_ej()


def extraction_uranium_ej():
    """
    Real Name: extraction uranium EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Global uranium extracted. Source: global model.
    """
    return _data_extraction_uranium_ej(time())


_data_extraction_uranium_ej = TabData(
    "extraction uranium EJ", "extraction_uranium_ej", {}, "interpolate"
)


def extraction_uranium_ej_world():
    """
    Real Name: extraction uranium EJ World
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global uranium extracted. Source: global model.
    """
    return extraction_uranium_ej()


def pes_nat_gas():
    """
    Real Name: PES nat gas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Global primary energy supply of natural gas. Source: global model.
    """
    return _data_pes_nat_gas(time())


_data_pes_nat_gas = TabData("PES nat gas", "pes_nat_gas", {}, "interpolate")


def pes_oil_ej():
    """
    Real Name: PES oil EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Global primary energy supply of oil. Source: global model.
    """
    return _data_pes_oil_ej(time())


_data_pes_oil_ej = TabData("PES oil EJ", "pes_oil_ej", {}, "interpolate")


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector():
    """
    Real Name: Real demand by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']

    Real demand by sector. Source: global model.
    """
    return _data_real_demand_by_sector(time())


_data_real_demand_by_sector = TabData(
    "Real demand by sector",
    "real_demand_by_sector",
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "interpolate",
)


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_world():
    """
    Real Name: Real demand by sector World
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real demand by sector. Source: global model.
    """
    return real_demand_by_sector()


def real_demand_world():
    """
    Real Name: Real demand World
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total World final demand (MEDEAS-World).
    """
    return sum(
        real_demand_by_sector_world().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel():
    """
    Real Name: Real final energy by sector and fuel
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: ['final sources', 'sectors']

    Real final energy consumed by sector and fuel. Source: global model.
    """
    return _data_real_final_energy_by_sector_and_fuel(time())


_data_real_final_energy_by_sector_and_fuel = TabData(
    "Real final energy by sector and fuel",
    "real_final_energy_by_sector_and_fuel",
    {
        "final sources": ["electricity", "heat", "liquids", "gases", "solids"],
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ],
    },
    "interpolate",
)


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_world():
    """
    Real Name: Real final energy by sector and fuel World
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
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
    Type: Data
    Subs: ['sectors']

    Real total output by sector. Source: global model.
    """
    return _data_real_total_output_by_sector(time())


_data_real_total_output_by_sector = TabData(
    "Real total output by sector",
    "real_total_output_by_sector",
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "interpolate",
)


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_world():
    """
    Real Name: Real total output by sector World
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
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
    Type: Data
    Subs: []

    Share of global conventional vs global total (unconventional + conventional) gas extraction. Source: global model.
    """
    return _data_share_conv_vs_total_gas_extraction(time())


_data_share_conv_vs_total_gas_extraction = TabData(
    "share conv vs total gas extraction",
    "share_conv_vs_total_gas_extraction",
    {},
    "interpolate",
)


def share_conv_vs_total_gas_extraction_world():
    """
    Real Name: share conv vs total gas extraction World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of global conventional vs global total (unconventional + conventional) gas extraction. Source: global model.
    """
    return share_conv_vs_total_gas_extraction()


def share_conv_vs_total_oil_extraction():
    """
    Real Name: share conv vs total oil extraction
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Share of global conventional vs global total (unconventional + conventional) oil extraction. Source: global model.
    """
    return _data_share_conv_vs_total_oil_extraction(time())


_data_share_conv_vs_total_oil_extraction = TabData(
    "share conv vs total oil extraction",
    "share_conv_vs_total_oil_extraction",
    {},
    "interpolate",
)


def share_conv_vs_total_oil_extraction_world():
    """
    Real Name: share conv vs total oil extraction World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of global conventional vs global total (unconventional + conventional) oil extraction. Source: global model.
    """
    return share_conv_vs_total_oil_extraction()


def share_e_losses_cc():
    """
    Real Name: share E losses CC
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []

    Energy losses due to climate change impacts. Source: global model.
    """
    return _data_share_e_losses_cc(time())


_data_share_e_losses_cc = TabData(
    "share E losses CC", "share_e_losses_cc", {}, "interpolate"
)


def temperature_change():
    """
    Real Name: Temperature change
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Data
    Subs: []

    Temperature change. Source: global model.
    """
    return _data_temperature_change(time())


_data_temperature_change = TabData(
    "Temperature change", "temperature_change", {}, "interpolate"
)


def total_extraction_nre_ej():
    """
    Real Name: Total extraction NRE EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []

    Global total non-renewable primary energy extraction. Source: global model.
    """
    return _data_total_extraction_nre_ej(time())


_data_total_extraction_nre_ej = TabData(
    "Total extraction NRE EJ", "total_extraction_nre_ej", {}, "interpolate"
)


def total_extraction_nre_ej_world():
    """
    Real Name: Total extraction NRE EJ World
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global total non-renewable primary energy extraction. Source: global model.
    """
    return total_extraction_nre_ej()
