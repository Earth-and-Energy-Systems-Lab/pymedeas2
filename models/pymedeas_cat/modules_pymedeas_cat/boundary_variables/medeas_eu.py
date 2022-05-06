"""
Module medeas_eu
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="Annual GDP growth rate EU",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_annual_gdp_growth_rate_eu"},
)
def annual_gdp_growth_rate_eu():
    return _data_annual_gdp_growth_rate_eu(time())


_data_annual_gdp_growth_rate_eu = TabData(
    "Annual GDP growth rate EU", "annual_gdp_growth_rate_eu", {}, "interpolate"
)


@component.add(
    name="Annual GDP growth rate EU28",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_gdp_growth_rate_eu": 1},
)
def annual_gdp_growth_rate_eu28():
    return annual_gdp_growth_rate_eu()


@component.add(
    name="GDP EU",
    units="Tdollar",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_gdp_eu"},
)
def gdp_eu():
    return _data_gdp_eu(time())


_data_gdp_eu = TabData("GDP EU", "gdp_eu", {}, "interpolate")


@component.add(
    name="GDP EU28",
    units="Mdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu": 1, "mdollar_per_tdollar": 1},
)
def gdp_eu28():
    return gdp_eu() * mdollar_per_tdollar()


@component.add(
    name="Real demand by sector EU28",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_demand_by_sector_eu": 1},
)
def real_demand_by_sector_eu28():
    return real_final_demand_by_sector_eu()


@component.add(
    name="Real demand EU28",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_by_sector_eu28": 1},
)
def real_demand_eu28():
    return sum(
        real_demand_by_sector_eu28().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="Real final demand by sector EU",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_final_demand_by_sector_eu"},
)
def real_final_demand_by_sector_eu():
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


@component.add(
    name="Real final energy by sector and fuel EU",
    units="EJ",
    subscripts=["final sources", "sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_final_energy_by_sector_and_fuel_eu"},
)
def real_final_energy_by_sector_and_fuel_eu():
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


@component.add(
    name="Real final energy by sector and fuel EU28",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_energy_by_sector_and_fuel_eu": 1},
)
def real_final_energy_by_sector_and_fuel_eu28():
    """
    LOAD FROM EU-MODEL
    """
    return real_final_energy_by_sector_and_fuel_eu()


@component.add(
    name="Real total output by sector EU",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_total_output_by_sector_eu"},
)
def real_total_output_by_sector_eu():
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


@component.add(
    name="Real total output by sector EU28",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_sector_eu": 1},
)
def real_total_output_by_sector_eu28():
    """
    LOAD EU-MODEL RESULTS
    """
    return real_total_output_by_sector_eu()


@component.add(
    name="Total FE Elec generation TWh EU",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_total_fe_elec_generation_twh_eu"},
)
def total_fe_elec_generation_twh_eu():
    return _data_total_fe_elec_generation_twh_eu(time())


_data_total_fe_elec_generation_twh_eu = TabData(
    "Total FE Elec generation TWh EU",
    "total_fe_elec_generation_twh_eu",
    {},
    "interpolate",
)


@component.add(
    name="Total FE Elec generation TWh EU28",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_generation_twh_eu": 1},
)
def total_fe_elec_generation_twh_eu28():
    return total_fe_elec_generation_twh_eu()
