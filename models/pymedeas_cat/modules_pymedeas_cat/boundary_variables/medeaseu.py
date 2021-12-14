"""
Module medeaseu
Translated using PySD version 2.1.0
"""


def annual_gdp_growth_rate_eu():
    """
    Real Name: Annual GDP growth rate EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: None


    """
    return _data_annual_gdp_growth_rate_eu(time())


def annual_gdp_growth_rate_eu28():
    """
    Real Name: Annual GDP growth rate EU28
    Original Eqn: Annual GDP growth rate EU
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return annual_gdp_growth_rate_eu()


def gdp_eu():
    """
    Real Name: GDP EU
    Original Eqn:
    Units: Tdollar
    Limits: (None, None)
    Type: data
    Subs: None


    """
    return _data_gdp_eu(time())


def gdp_eu28():
    """
    Real Name: GDP EU28
    Original Eqn: GDP EU*Mdollar per Tdollar
    Units: Mdollar
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return gdp_eu() * mdollar_per_tdollar()


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_eu28():
    """
    Real Name: Real demand by sector EU28
    Original Eqn: Real final demand by sector EU[sectors]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return real_final_demand_by_sector_eu()


def real_demand_eu28():
    """
    Real Name: Real demand EU28
    Original Eqn: SUM(Real demand by sector EU28[sectors!])
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(real_demand_by_sector_eu28(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def real_final_demand_by_sector_eu():
    """
    Real Name: Real final demand by sector EU
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: data
    Subs: ['sectors']


    """
    return _data_real_final_demand_by_sector_eu(time())


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_eu():
    """
    Real Name: Real final energy by sector and fuel EU
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: data
    Subs: ['final sources', 'sectors']


    """
    return _data_real_final_energy_by_sector_and_fuel_eu(time())


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_eu28():
    """
    Real Name: Real final energy by sector and fuel EU28
    Original Eqn: Real final energy by sector and fuel EU[final sources,sectors]
    Units:
    Limits: (None, None)
    Type: component
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
    Type: data
    Subs: ['sectors']


    """
    return _data_real_total_output_by_sector_eu(time())


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_eu28():
    """
    Real Name: Real total output by sector EU28
    Original Eqn: Real total output by sector EU[sectors]
    Units:
    Limits: (None, None)
    Type: component
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
    Type: data
    Subs: None


    """
    return _data_total_fe_elec_generation_twh_eu(time())


def total_fe_elec_generation_twh_eu28():
    """
    Real Name: Total FE Elec generation TWh EU28
    Original Eqn: Total FE Elec generation TWh EU
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_fe_elec_generation_twh_eu()


_data_annual_gdp_growth_rate_eu = TabData(
    "Annual GDP growth rate EU", "annual_gdp_growth_rate_eu", {}, "interpolate"
)


_data_gdp_eu = TabData("GDP EU", "gdp_eu", {}, "interpolate")


_data_real_final_demand_by_sector_eu = TabData(
    "Real final demand by sector EU",
    "real_final_demand_by_sector_eu",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


_data_real_final_energy_by_sector_and_fuel_eu = TabData(
    "Real final energy by sector and fuel EU",
    "real_final_energy_by_sector_and_fuel_eu",
    {
        "final sources": _subscript_dict["final sources"],
        "sectors": _subscript_dict["sectors"],
    },
    "interpolate",
)


_data_real_total_output_by_sector_eu = TabData(
    "Real total output by sector EU",
    "real_total_output_by_sector_eu",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


_data_total_fe_elec_generation_twh_eu = TabData(
    "Total FE Elec generation TWh EU",
    "total_fe_elec_generation_twh_eu",
    {},
    "interpolate",
)
