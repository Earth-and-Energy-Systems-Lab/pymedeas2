"""
Module medeas_eu
Translated using PySD version 2.2.1
"""


def annual_gdp_growth_rate_eu():
    """
    Real Name: Annual GDP growth rate EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_annual_gdp_growth_rate_eu(time())


_data_annual_gdp_growth_rate_eu = TabData(
    "Annual GDP growth rate EU", "annual_gdp_growth_rate_eu", {}, "interpolate"
)


def annual_gdp_growth_rate_eu28():
    """
    Real Name: Annual GDP growth rate EU28
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return annual_gdp_growth_rate_eu()


def gdp_eu():
    """
    Real Name: GDP EU
    Original Eqn:
    Units: Tdollar
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_gdp_eu(time())


_data_gdp_eu = TabData("GDP EU", "gdp_eu", {}, "interpolate")


def gdp_eu28():
    """
    Real Name: GDP EU28
    Original Eqn:
    Units: Mdollar
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return gdp_eu() * mdollar_per_tdollar()


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_eu28():
    """
    Real Name: Real demand by sector EU28
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return real_final_demand_by_sector_eu()


def real_demand_eu28():
    """
    Real Name: Real demand EU28
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return sum(
        real_demand_by_sector_eu28().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@subs(["sectors"], _subscript_dict)
def real_final_demand_by_sector_eu():
    """
    Real Name: Real final demand by sector EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']


    """
    return _data_real_final_demand_by_sector_eu(time())


_data_real_final_demand_by_sector_eu = TabData(
    "Real final demand by sector EU",
    "real_final_demand_by_sector_eu",
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


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_eu():
    """
    Real Name: Real final energy by sector and fuel EU
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: ['final sources', 'sectors']


    """
    return _data_real_final_energy_by_sector_and_fuel_eu(time())


_data_real_final_energy_by_sector_and_fuel_eu = TabData(
    "Real final energy by sector and fuel EU",
    "real_final_energy_by_sector_and_fuel_eu",
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
def real_final_energy_by_sector_and_fuel_eu28():
    """
    Real Name: Real final energy by sector and fuel EU28
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    LOAD FROM EU-MODEL
    """
    return real_final_energy_by_sector_and_fuel_eu()


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_eu():
    """
    Real Name: Real total output by sector EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']


    """
    return _data_real_total_output_by_sector_eu(time())


_data_real_total_output_by_sector_eu = TabData(
    "Real total output by sector EU",
    "real_total_output_by_sector_eu",
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
def real_total_output_by_sector_eu28():
    """
    Real Name: Real total output by sector EU28
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    LOAD EU-MODEL RESULTS
    """
    return real_total_output_by_sector_eu()


def total_fe_elec_generation_twh_eu():
    """
    Real Name: Total FE Elec generation TWh EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _data_total_fe_elec_generation_twh_eu(time())


_data_total_fe_elec_generation_twh_eu = TabData(
    "Total FE Elec generation TWh EU",
    "total_fe_elec_generation_twh_eu",
    {},
    "interpolate",
)


def total_fe_elec_generation_twh_eu28():
    """
    Real Name: Total FE Elec generation TWh EU28
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return total_fe_elec_generation_twh_eu()
