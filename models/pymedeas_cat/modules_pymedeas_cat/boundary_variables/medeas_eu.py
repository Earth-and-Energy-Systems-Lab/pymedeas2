"""
Module boundary_variables.medeas_eu
Translated using PySD version 3.14.0
"""

@component.add(
    name="Annual_GDP_growth_rate_EU",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_annual_gdp_growth_rate_eu"},
)
def annual_gdp_growth_rate_eu():
    return _data_annual_gdp_growth_rate_eu(time())


_data_annual_gdp_growth_rate_eu = TabData(
    "Annual_GDP_growth_rate_EU", "annual_gdp_growth_rate_eu", {}, "interpolate"
)


@component.add(
    name="Annual_GDP_growth_rate_EU28",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_gdp_growth_rate_eu": 1},
)
def annual_gdp_growth_rate_eu28():
    return annual_gdp_growth_rate_eu()


@component.add(
    name="GDP_EU",
    units="T$",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_gdp_eu"},
)
def gdp_eu():
    return _data_gdp_eu(time())


_data_gdp_eu = TabData("GDP_EU", "gdp_eu", {}, "interpolate")


@component.add(
    name="GDP_EU28",
    units="Mdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu": 1, "mdollar_per_tdollar": 1},
)
def gdp_eu28():
    return gdp_eu() * mdollar_per_tdollar()


@component.add(
    name="Real_demand_by_sector_EU28",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_demand_by_sector_eu": 1},
)
def real_demand_by_sector_eu28():
    return real_final_demand_by_sector_eu()


@component.add(
    name="Real_final_demand_by_sector_EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_final_demand_by_sector_eu"},
)
def real_final_demand_by_sector_eu():
    return _data_real_final_demand_by_sector_eu(time())


_data_real_final_demand_by_sector_eu = TabData(
    "Real_final_demand_by_sector_EU",
    "real_final_demand_by_sector_eu",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real_final_energy_by_sector_and_fuel_EU",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_final_energy_by_sector_and_fuel_eu"},
)
def real_final_energy_by_sector_and_fuel_eu():
    return _data_real_final_energy_by_sector_and_fuel_eu(time())


_data_real_final_energy_by_sector_and_fuel_eu = TabData(
    "Real_final_energy_by_sector_and_fuel_EU",
    "real_final_energy_by_sector_and_fuel_eu",
    {
        "final_sources": _subscript_dict["final_sources"],
        "sectors": _subscript_dict["sectors"],
    },
    "interpolate",
)


@component.add(
    name="Real_final_energy_by_sector_and_fuel_EU28",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
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
    name="Real_total_output_by_sector_EU",
    units="M$",
    subscripts=[np.str_("sectors")],
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_real_total_output_by_sector_eu"},
)
def real_total_output_by_sector_eu():
    return _data_real_total_output_by_sector_eu(time())


_data_real_total_output_by_sector_eu = TabData(
    "Real_total_output_by_sector_EU",
    "real_total_output_by_sector_eu",
    {"sectors": _subscript_dict["sectors"]},
    "interpolate",
)


@component.add(
    name="Real_total_output_by_sector_EU28",
    units="M$",
    subscripts=[np.str_("sectors")],
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
    name="Total_FE_Elec_generation_TWh_EU",
    units="TWh/year",
    comp_type="Data",
    comp_subtype="Normal",
    depends_on={"time": 1, "__data__": "_data_total_fe_elec_generation_twh_eu"},
)
def total_fe_elec_generation_twh_eu():
    return _data_total_fe_elec_generation_twh_eu(time())


_data_total_fe_elec_generation_twh_eu = TabData(
    "Total_FE_Elec_generation_TWh_EU",
    "total_fe_elec_generation_twh_eu",
    {},
    "interpolate",
)


@component.add(
    name="Total_FE_Elec_generation_TWh_EU28",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_generation_twh_eu": 1},
)
def total_fe_elec_generation_twh_eu28():
    return total_fe_elec_generation_twh_eu()
