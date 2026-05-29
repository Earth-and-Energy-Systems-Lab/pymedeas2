"""
Module transport.pkm
Translated using PySD version 3.14.3
"""

@component.add(
    name="aux_GDPpc0pkm",
    units="T$/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "pkm_ref_year": 1, "gdppc": 1, "time_step": 1},
)
def aux_gdppc0pkm():
    return (
        if_then_else(time() == pkm_ref_year(), lambda: gdppc(), lambda: 0) / time_step()
    )


@component.add(
    name="beta_pkm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_pkm"},
)
def beta_pkm():
    return _ext_constant_beta_pkm()


_ext_constant_beta_pkm = ExtConstant(
    r"../transport.xlsx", "Europe", "beta_pkm", {}, _root, {}, "_ext_constant_beta_pkm"
)


@component.add(
    name='"commercial_pkm_vehicles/pkm"',
    units="year*vehicles/(person*km)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_commercial_vehicles": 1,
        "initial_share_pkm_buses": 1,
        "initial_pkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def commercial_pkm_vehiclespkm():
    return (
        sum(
            historic_commercial_vehicles(2023).rename({"fuels": "fuels!"}),
            dim=["fuels!"],
        )
        / (1000000000.0 * initial_pkm() * initial_share_pkm_buses())
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="desired_pkm_by_mode_and_fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pkm": 1, "pkm_fuel_share": 1},
)
def desired_pkm_by_mode_and_fuel():
    """
    Number of pkms by mode and fuel
    """
    return pkm() * pkm_fuel_share()


@component.add(
    name="efficiency_pkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_efficiency_pkm": 1},
    other_deps={
        "_integ_efficiency_pkm": {
            "initial": {
                "initial_efficiency_per_pkm": 1,
                "sensitivity_pkm_efficiency": 1,
            },
            "step": {"variation_efficiency_pkm": 1},
        }
    },
)
def efficiency_pkm():
    return _integ_efficiency_pkm()


_integ_efficiency_pkm = Integ(
    lambda: variation_efficiency_pkm(),
    lambda: initial_efficiency_per_pkm() * sensitivity_pkm_efficiency(),
    "_integ_efficiency_pkm",
)


@component.add(
    name="EI_households_transport",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_pkm": 4,
        "household_demand_total": 3,
        "m_to_t": 3,
        "nvs_1_year": 3,
    },
)
def ei_households_transport():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = (
        float(energy_pkm().loc["elect", "Road_light"])
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["gases"]] = (
        float(energy_pkm().loc["gas", "Road_light"])
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["liquids"]] = (
        (
            float(energy_pkm().loc["liq", "Road_light"])
            + float(energy_pkm().loc["hybrid", "Road_light"])
        )
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="end_historical_pkm", units="year", comp_type="Constant", comp_subtype="Normal"
)
def end_historical_pkm():
    return 2023


@component.add(
    name="energy_by_fuel_mode_pkm",
    units="EJ/year",
    subscripts=["final_sources", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 5, "historic_share_electricity_hybrid": 2, "time": 2},
)
def energy_by_fuel_mode_pkm():
    value = xr.DataArray(
        np.nan,
        {
            "final_sources": _subscript_dict["final_sources"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["final_sources", "Transport_Modes"],
    )
    value.loc[["liquids"], :] = (
        (
            energy_pkm().loc["liq", :].reset_coords(drop=True)
            + energy_pkm().loc["hybrid", :].reset_coords(drop=True)
            * (1 - historic_share_electricity_hybrid(time()))
        )
        .expand_dims({"final_sources": ["liquids"]}, 0)
        .values
    )
    value.loc[["gases"], :] = (
        energy_pkm()
        .loc["gas", :]
        .reset_coords(drop=True)
        .expand_dims({"final_sources": ["gases"]}, 0)
        .values
    )
    value.loc[["electricity"], :] = (
        (
            energy_pkm().loc["elect", :].reset_coords(drop=True)
            + energy_pkm().loc["hybrid", :].reset_coords(drop=True)
            * historic_share_electricity_hybrid(time())
        )
        .expand_dims({"final_sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = 0
    value.loc[["solids"], :] = 0
    return value


@component.add(
    name="energy_pkm",
    units="person*km*EJ/(year*pkm)",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_pkm_by_mode_and_fuel": 1, "efficiency_pkm": 1, "mj_per_ej": 1},
)
def energy_pkm():
    return (
        real_pkm_by_mode_and_fuel()
        * efficiency_pkm().transpose("fuels", "Transport_Modes")
        / mj_per_ej()
    )


@component.add(
    name="energy_pkm_fuel",
    units="EJ/year",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 1},
)
def energy_pkm_fuel():
    return sum(
        energy_pkm().rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name="Energy_scarcity_shortage_by_fuel",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_scarcity_feedback_shortage_coeff_eu": 3},
)
def energy_scarcity_shortage_by_fuel():
    value = xr.DataArray(np.nan, {"fuels": _subscript_dict["fuels"]}, ["fuels"])
    value.loc[["liq"]] = 1
    value.loc[["gas"]] = float(
        energy_scarcity_feedback_shortage_coeff_eu().loc["gases"]
    )
    value.loc[["elect"]] = float(
        energy_scarcity_feedback_shortage_coeff_eu().loc["electricity"]
    )
    value.loc[["hybrid"]] = float(
        energy_scarcity_feedback_shortage_coeff_eu().loc["liquids"]
    )
    return value


@component.add(
    name="fuel_share_1995",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def fuel_share_1995():
    value = xr.DataArray(np.nan, {"fuels": _subscript_dict["fuels"]}, ["fuels"])
    value.loc[["liq"]] = 1
    value.loc[["gas"]] = 0
    value.loc[["elect"]] = 0
    value.loc[["hybrid"]] = 0
    return value


@component.add(
    name="fuel_share_air_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_air_pkm",
        "__lookup__": "_ext_lookup_fuel_share_air_pkm",
    },
)
def fuel_share_air_pkm(x, final_subs=None):
    """
    Share of fuel used by passenger air tranport every 5 years
    """
    return _ext_lookup_fuel_share_air_pkm(x, final_subs)


_ext_lookup_fuel_share_air_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_air_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_air_pkm",
)


@component.add(
    name="fuel_share_households_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_households_pkm",
        "__lookup__": "_ext_lookup_fuel_share_households_pkm",
    },
)
def fuel_share_households_pkm(x, final_subs=None):
    """
    Fuels share (liq, gas, elect, hybrid) of households passenger transport every 5 years
    """
    return _ext_lookup_fuel_share_households_pkm(x, final_subs)


_ext_lookup_fuel_share_households_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_households_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_households_pkm",
)


@component.add(
    name="fuel_share_maritime_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_maritime_pkm",
        "__lookup__": "_ext_lookup_fuel_share_maritime_pkm",
    },
)
def fuel_share_maritime_pkm(x, final_subs=None):
    return _ext_lookup_fuel_share_maritime_pkm(x, final_subs)


_ext_lookup_fuel_share_maritime_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_maritime_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime_pkm",
)


@component.add(
    name="fuel_share_rail_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_rail_pkm",
        "__lookup__": "_ext_lookup_fuel_share_rail_pkm",
    },
)
def fuel_share_rail_pkm(x, final_subs=None):
    return _ext_lookup_fuel_share_rail_pkm(x, final_subs)


_ext_lookup_fuel_share_rail_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_rail_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_rail_pkm",
)


@component.add(
    name="fuel_share_road_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_road_pkm",
        "__lookup__": "_ext_lookup_fuel_share_road_pkm",
    },
)
def fuel_share_road_pkm(x, final_subs=None):
    """
    Fuel share of inland passenger transport every 5 years
    """
    return _ext_lookup_fuel_share_road_pkm(x, final_subs)


_ext_lookup_fuel_share_road_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_road_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_road_pkm",
)


@component.add(
    name="GDP0pcpkm",
    units="year*T$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gdp0pcpkm": 1},
    other_deps={"_integ_gdp0pcpkm": {"initial": {}, "step": {"aux_gdppc0pkm": 1}}},
)
def gdp0pcpkm():
    return _integ_gdp0pcpkm()


_integ_gdp0pcpkm = Integ(lambda: aux_gdppc0pkm(), lambda: 0, "_integ_gdp0pcpkm")


@component.add(
    name="hist_pkm",
    units="person*km/(year)",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_pkm",
        "__lookup__": "_ext_lookup_hist_pkm",
    },
)
def hist_pkm(x, final_subs=None):
    """
    Historic values of pkm/GDP
    """
    return _ext_lookup_hist_pkm(x, final_subs)


_ext_lookup_hist_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_pkm",
    {},
    _root,
    {},
    "_ext_lookup_hist_pkm",
)


@component.add(
    name="hist_transport_share_pkm",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_transport_share_pkm",
        "__lookup__": "_ext_lookup_hist_transport_share_pkm",
    },
)
def hist_transport_share_pkm(x, final_subs=None):
    return _ext_lookup_hist_transport_share_pkm(x, final_subs)


_ext_lookup_hist_transport_share_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "share_transport_mode_hist_pkm",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_hist_transport_share_pkm",
)


@component.add(
    name="historic_commercial_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_commercial_vehicles",
        "__lookup__": "_ext_lookup_historic_commercial_vehicles",
    },
)
def historic_commercial_vehicles(x, final_subs=None):
    return _ext_lookup_historic_commercial_vehicles(x, final_subs)


_ext_lookup_historic_commercial_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "initial_pkm_vehicles_com",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_commercial_vehicles",
)


@component.add(
    name="historic_fuel_share_households_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_households_pkm",
        "__lookup__": "_ext_lookup_historic_fuel_share_households_pkm",
    },
)
def historic_fuel_share_households_pkm(x, final_subs=None):
    return _ext_lookup_historic_fuel_share_households_pkm(x, final_subs)


_ext_lookup_historic_fuel_share_households_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_households_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_households_pkm",
)


@component.add(
    name="historic_fuel_share_maritime_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_maritime_pkm",
        "__lookup__": "_ext_lookup_historic_fuel_share_maritime_pkm",
    },
)
def historic_fuel_share_maritime_pkm(x, final_subs=None):
    return _ext_lookup_historic_fuel_share_maritime_pkm(x, final_subs)


_ext_lookup_historic_fuel_share_maritime_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_maritime_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_maritime_pkm",
)


@component.add(
    name="historic_fuel_share_rail_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_rail_pkm",
        "__lookup__": "_ext_lookup_historic_fuel_share_rail_pkm",
    },
)
def historic_fuel_share_rail_pkm(x, final_subs=None):
    """
    Historic share of fuels for rail passenger transport
    """
    return _ext_lookup_historic_fuel_share_rail_pkm(x, final_subs)


_ext_lookup_historic_fuel_share_rail_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_rail_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_rail_pkm",
)


@component.add(
    name="historic_fuel_share_road_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_road_pkm",
        "__lookup__": "_ext_lookup_historic_fuel_share_road_pkm",
    },
)
def historic_fuel_share_road_pkm(x, final_subs=None):
    return _ext_lookup_historic_fuel_share_road_pkm(x, final_subs)


_ext_lookup_historic_fuel_share_road_pkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_inland_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_road_pkm",
)


@component.add(
    name="historic_households_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_households_vehicles",
        "__lookup__": "_ext_lookup_historic_households_vehicles",
    },
)
def historic_households_vehicles(x, final_subs=None):
    """
    Historic households vehicles per fuel
    """
    return _ext_lookup_historic_households_vehicles(x, final_subs)


_ext_lookup_historic_households_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_household_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_households_vehicles",
)


@component.add(
    name="historic_share_electricity_hybrid",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_share_electricity_hybrid",
        "__lookup__": "_ext_lookup_historic_share_electricity_hybrid",
    },
)
def historic_share_electricity_hybrid(x, final_subs=None):
    return _ext_lookup_historic_share_electricity_hybrid(x, final_subs)


_ext_lookup_historic_share_electricity_hybrid = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "share_hybrid_electricity_pkm",
    {},
    _root,
    {},
    "_ext_lookup_historic_share_electricity_hybrid",
)


@component.add(
    name='"households_vehicles/pkm"',
    units="year*vehicles/(person*km)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_households_vehicles": 1,
        "initial_share_households_pkm": 1,
        "initial_pkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def households_vehiclespkm():
    """
    Number of vehicles/pkm
    """
    return (
        sum(
            historic_households_vehicles(2023).rename({"fuels": "fuels!"}),
            dim=["fuels!"],
        )
        / (initial_pkm() * initial_share_households_pkm() * 1000000000.0)
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="improvement_efficiency_pkm",
    units="Dmnl",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_improvement_efficiency_pkm"},
)
def improvement_efficiency_pkm():
    return _ext_constant_improvement_efficiency_pkm()


_ext_constant_improvement_efficiency_pkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "efficiency_pkm_improvment*",
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    _root,
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    "_ext_constant_improvement_efficiency_pkm",
)


@component.add(
    name="initial_efficiency_per_pkm",
    units="MJ/pkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_efficiency_per_pkm"},
)
def initial_efficiency_per_pkm():
    return _ext_constant_initial_efficiency_per_pkm()


_ext_constant_initial_efficiency_per_pkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "efficiency_pkm*",
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    _root,
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    "_ext_constant_initial_efficiency_per_pkm",
)


@component.add(
    name="initial_fuel_share_air_pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_air_pkm"},
)
def initial_fuel_share_air_pkm():
    """
    Air and maritiem transport 100% liquids in the historical period
    """
    return _ext_constant_initial_fuel_share_air_pkm()


_ext_constant_initial_fuel_share_air_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_air_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_pkm",
)


@component.add(
    name="initial_pkm",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkm"},
)
def initial_pkm():
    """
    Initial number of pkms at 2023
    """
    return _ext_constant_initial_pkm()


_ext_constant_initial_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_pkm",
)


@component.add(
    name="initial_share_households_pkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_households_pkm"},
)
def initial_share_households_pkm():
    return _ext_constant_initial_share_households_pkm()


_ext_constant_initial_share_households_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_private_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_households_pkm",
)


@component.add(
    name="initial_share_pkm_buses",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_pkm_buses"},
)
def initial_share_pkm_buses():
    return _ext_constant_initial_share_pkm_buses()


_ext_constant_initial_share_pkm_buses = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_comercial_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_pkm_buses",
)


@component.add(
    name="initial_share_pkm_rail",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_pkm_rail"},
)
def initial_share_pkm_rail():
    return _ext_constant_initial_share_pkm_rail()


_ext_constant_initial_share_pkm_rail = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_rail_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_pkm_rail",
)


@component.add(
    name="log_pkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predicted_log_pkm_hat": 1, "resid_pkm": 1},
)
def log_pkm():
    return predicted_log_pkm_hat() + resid_pkm()


@component.add(
    name="mode_shar_pkm_policy_last_year",
    units="percent",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"start_year_policies_transport": 1, "mode_share_pkm_policy": 1},
)
def mode_shar_pkm_policy_last_year():
    return mode_share_pkm_policy(start_year_policies_transport())


@component.add(
    name="mode_share_pkm",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mode_share_pkm_aux": 2},
)
def mode_share_pkm():
    return mode_share_pkm_aux() / sum(
        mode_share_pkm_aux().rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name="mode_share_pkm_aux",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "mode_share_pkm_policy": 5,
        "sensitivity_rail_mode_share": 5,
        "proportion_mode_share_pkm": 4,
    },
)
def mode_share_pkm_aux():
    value = xr.DataArray(
        np.nan,
        {"Transport_Modes": _subscript_dict["Transport_Modes"]},
        ["Transport_Modes"],
    )
    value.loc[["Rail"]] = float(
        np.maximum(
            0,
            float(
                np.minimum(
                    1,
                    float(mode_share_pkm_policy(time()).loc["Rail"])
                    + sensitivity_rail_mode_share(),
                )
            ),
        )
    )
    value.loc[["Road_light"]] = float(
        np.maximum(
            0,
            float(
                np.minimum(
                    1,
                    float(mode_share_pkm_policy(time()).loc["Road_light"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_pkm().loc["Road_light"]),
                )
            ),
        )
    )
    value.loc[["Road_heavy"]] = float(
        np.maximum(
            0,
            float(
                np.minimum(
                    1,
                    float(mode_share_pkm_policy(time()).loc["Road_heavy"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_pkm().loc["Road_heavy"]),
                )
            ),
        )
    )
    value.loc[["Maritime"]] = float(
        np.maximum(
            0,
            float(
                np.minimum(
                    1,
                    float(mode_share_pkm_policy(time()).loc["Maritime"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_pkm().loc["Maritime"]),
                )
            ),
        )
    )
    value.loc[["Air"]] = float(
        np.maximum(
            0,
            float(
                np.minimum(
                    1,
                    float(mode_share_pkm_policy(time()).loc["Air"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_pkm().loc["Air"]),
                )
            ),
        )
    )
    return value


@component.add(
    name="mode_share_pkm_policy",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_mode_share_pkm_policy",
        "__lookup__": "_ext_lookup_mode_share_pkm_policy",
    },
)
def mode_share_pkm_policy(x, final_subs=None):
    return _ext_lookup_mode_share_pkm_policy(x, final_subs)


_ext_lookup_mode_share_pkm_policy = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "Year_transport_share",
    "pkm_share",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_mode_share_pkm_policy",
)


@component.add(
    name="phi_pkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_phi_pkm"},
)
def phi_pkm():
    return _ext_constant_phi_pkm()


_ext_constant_phi_pkm = ExtConstant(
    r"../transport.xlsx", "Europe", "phi_pkm", {}, _root, {}, "_ext_constant_phi_pkm"
)


@component.add(
    name="pkm",
    units="person*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "end_historical_data": 1, "hist_pkm": 1, "predicted_pkm": 1},
)
def pkm():
    """
    passengers·km variations related to GDP. Amount of pkm at each time step
    """
    return (
        if_then_else(
            time() <= end_historical_data(),
            lambda: hist_pkm(time()),
            lambda: predicted_pkm(),
        )
        * 1000000000.0
    )


@component.add(
    name="pkm0",
    units="person*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "pkm_ref_year": 2, "hist_pkm": 1},
)
def pkm0():
    return if_then_else(
        time() >= pkm_ref_year(), lambda: hist_pkm(pkm_ref_year()), lambda: 0
    )


@component.add(
    name="pkm_fuel_share",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pkm_fuel_share_road": 1,
        "pkm_mode_share": 5,
        "pkm_fuel_share_maritime": 1,
        "pkm_fuel_share_air": 1,
        "pkm_fuel_share_households": 1,
        "pkm_fuel_share_rail": 1,
    },
)
def pkm_fuel_share():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_heavy"]] = (
        (pkm_fuel_share_road() * float(pkm_mode_share().loc["Road_heavy"]))
        .expand_dims({"Land": ["Road_heavy"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (pkm_fuel_share_maritime() * float(pkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport_Modes": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (pkm_fuel_share_air() * float(pkm_mode_share().loc["Air"]))
        .expand_dims({"Transport_Modes": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Road_light"]] = (
        (pkm_fuel_share_households() * float(pkm_mode_share().loc["Road_light"]))
        .expand_dims({"Land": ["Road_light"]}, 1)
        .values
    )
    value.loc[:, ["Rail"]] = (
        (pkm_fuel_share_rail() * float(pkm_mode_share().loc["Rail"]))
        .expand_dims({"Land": ["Rail"]}, 1)
        .values
    )
    return value


@component.add(
    name="pkm_fuel_share_air",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_pkm": 4,
        "initial_fuel_share_air_pkm": 3,
        "fuel_share_1995": 2,
        "fuel_share_air_pkm": 2,
        "start_year_policies_transport": 3,
    },
)
def pkm_fuel_share_air():
    return if_then_else(
        time() < end_historical_pkm(),
        lambda: fuel_share_1995()
        + (
            (initial_fuel_share_air_pkm() - fuel_share_1995())
            / (end_historical_pkm() - 1995)
        )
        * (time() - 1995),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_air_pkm()
            + (
                (
                    fuel_share_air_pkm(start_year_policies_transport())
                    - initial_fuel_share_air_pkm()
                )
                / (start_year_policies_transport() - end_historical_pkm())
            )
            * (time() - end_historical_pkm()),
            lambda: fuel_share_air_pkm(time()),
        ),
    )


@component.add(
    name="pkm_fuel_share_households",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 5,
        "historic_fuel_share_households_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_households_pkm": 2,
    },
)
def pkm_fuel_share_households():
    return if_then_else(
        time() < end_historical_data(),
        lambda: historic_fuel_share_households_pkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_households_pkm(end_historical_data())
            + (
                (
                    fuel_share_households_pkm(start_year_policies_transport())
                    - historic_fuel_share_households_pkm(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_households_pkm(time()),
        ),
    )


@component.add(
    name="pkm_fuel_share_maritime",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_pkm": 5,
        "historic_fuel_share_maritime_pkm": 3,
        "fuel_share_maritime_pkm": 2,
        "start_year_policies_transport": 3,
    },
)
def pkm_fuel_share_maritime():
    return if_then_else(
        time() < end_historical_pkm(),
        lambda: historic_fuel_share_maritime_pkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_maritime_pkm(end_historical_pkm())
            + (
                (
                    fuel_share_maritime_pkm(start_year_policies_transport())
                    - historic_fuel_share_maritime_pkm(end_historical_pkm())
                )
                / (start_year_policies_transport() - end_historical_pkm())
            )
            * (time() - end_historical_pkm()),
            lambda: fuel_share_maritime_pkm(time()),
        ),
    )


@component.add(
    name="pkm_fuel_share_rail",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_pkm": 6,
        "historic_fuel_share_rail_pkm": 3,
        "fuel_share_rail_pkm": 2,
        "start_year_policies_transport": 3,
    },
)
def pkm_fuel_share_rail():
    return if_then_else(
        time() < end_historical_pkm(),
        lambda: historic_fuel_share_rail_pkm(end_historical_pkm()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_rail_pkm(end_historical_pkm())
            + (
                (
                    fuel_share_rail_pkm(start_year_policies_transport())
                    - historic_fuel_share_rail_pkm(end_historical_pkm())
                )
                / (start_year_policies_transport() - end_historical_pkm())
            )
            * (time() - end_historical_pkm()),
            lambda: fuel_share_rail_pkm(time()),
        ),
    )


@component.add(
    name="pkm_fuel_share_road",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_pkm": 5,
        "historic_fuel_share_road_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_road_pkm": 2,
    },
)
def pkm_fuel_share_road():
    return if_then_else(
        time() < end_historical_pkm(),
        lambda: historic_fuel_share_road_pkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_road_pkm(end_historical_pkm())
            + (
                (
                    fuel_share_road_pkm(start_year_policies_transport())
                    - historic_fuel_share_road_pkm(end_historical_pkm())
                )
                / (start_year_policies_transport() - end_historical_pkm())
            )
            * (time() - end_historical_pkm()),
            lambda: fuel_share_road_pkm(time()),
        ),
    )


@component.add(
    name="pkm_mode_share",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_pkm": 5,
        "hist_transport_share_pkm": 3,
        "mode_share_pkm": 1,
        "start_year_policies_transport": 2,
        "mode_shar_pkm_policy_last_year": 1,
    },
)
def pkm_mode_share():
    return if_then_else(
        time() < end_historical_pkm(),
        lambda: hist_transport_share_pkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: hist_transport_share_pkm(end_historical_pkm())
            + (
                (
                    mode_shar_pkm_policy_last_year()
                    - hist_transport_share_pkm(end_historical_pkm())
                )
                / (start_year_policies_transport() - end_historical_pkm())
            )
            * (time() - end_historical_pkm()),
            lambda: mode_share_pkm(),
        ),
    )


@component.add(
    name="pkm_ref_year",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pkm_ref_year"},
)
def pkm_ref_year():
    return _ext_constant_pkm_ref_year()


_ext_constant_pkm_ref_year = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "year0_pkm",
    {},
    _root,
    {},
    "_ext_constant_pkm_ref_year",
)


@component.add(
    name="predicted_log_pkm_hat",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdppc": 2, "gdp0pcpkm": 2, "beta_pkm": 1},
)
def predicted_log_pkm_hat():
    return if_then_else(
        zidz(gdppc(), gdp0pcpkm()) > 0,
        lambda: beta_pkm() * float(np.log(gdppc() / gdp0pcpkm())),
        lambda: 0,
    )


@component.add(
    name="predicted_pkm",
    units="person*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_data": 1,
        "pkm0": 2,
        "log_pkm": 1,
        "gdp0pcpkm": 1,
        "sensitivity_pkm_and_tkm": 1,
        "beta_pkm": 1,
        "gdppc": 1,
    },
)
def predicted_pkm():
    """
    pkm0*EXP(log_pkm)*sensitivity_pkm_and_tkm
    """
    return if_then_else(
        time() <= end_historical_data(),
        lambda: pkm0() * float(np.exp(log_pkm())),
        lambda: pkm0()
        * (gdppc() / gdp0pcpkm()) ** beta_pkm()
        * sensitivity_pkm_and_tkm(),
    )


@component.add(
    name="predicted_pkm_by_mode_and_fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pkm_fuel_share": 1, "predicted_pkm": 1},
)
def predicted_pkm_by_mode_and_fuel():
    return pkm_fuel_share() * predicted_pkm() * 1000000000.0


@component.add(
    name="proportion_mode_share_pkm",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "mode_share_pkm_policy": 2},
)
def proportion_mode_share_pkm():
    return mode_share_pkm_policy(time()) / sum(
        mode_share_pkm_policy(time()).rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name='"rail_vehicle/pkm"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_rail_pkm_vehicles": 1,
        "initial_share_pkm_rail": 1,
        "initial_pkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def rail_vehiclepkm():
    return (
        sum(
            historic_rail_pkm_vehicles(time()).rename({"fuels": "fuels!"}),
            dim=["fuels!"],
        )
        / (1000000000.0 * initial_pkm() * initial_share_pkm_rail())
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="real_pkm_by_mode",
    units="person*km/year",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_pkm_by_mode_and_fuel": 1},
)
def real_pkm_by_mode():
    return sum(real_pkm_by_mode_and_fuel().rename({"fuels": "fuels!"}), dim=["fuels!"])


@component.add(
    name="real_pkm_by_mode_and_fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_pkm_by_mode_and_fuel": 1},
)
def real_pkm_by_mode_and_fuel():
    """
    Real pkm variation after the effect of scarcity
    """
    return desired_pkm_by_mode_and_fuel()


@component.add(
    name="res0_pkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "end_historical_data": 1, "residu_pkm": 1},
)
def res0_pkm():
    return if_then_else(time() < end_historical_data(), lambda: 0, lambda: residu_pkm())


@component.add(
    name="resid_pkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 2,
        "res0_pkm": 1,
        "phi_pkm": 1,
        "resid_pkm_delayed": 1,
    },
)
def resid_pkm():
    return if_then_else(
        time() < end_historical_data(),
        lambda: 0,
        lambda: if_then_else(
            time() == end_historical_data(),
            lambda: res0_pkm(),
            lambda: phi_pkm() * resid_pkm_delayed(),
        ),
    )


@component.add(
    name="resid_pkm_delayed",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_resid_pkm_delayed": 1},
    other_deps={
        "_delayfixed_resid_pkm_delayed": {"initial": {}, "step": {"resid_pkm": 1}}
    },
)
def resid_pkm_delayed():
    return _delayfixed_resid_pkm_delayed()


_delayfixed_resid_pkm_delayed = DelayFixed(
    lambda: resid_pkm(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_resid_pkm_delayed",
)


@component.add(
    name="residu_pkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_residu_pkm"},
)
def residu_pkm():
    return _ext_constant_residu_pkm()


_ext_constant_residu_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "res0_pkm",
    {},
    _root,
    {},
    "_ext_constant_residu_pkm",
)


@component.add(
    name="sensitivity_pkm_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_pkm_efficiency():
    """
    Variable used for the sensitivity analysis
    """
    return 1


@component.add(
    name="sensitivity_vehicles_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_vehicles_efficiency():
    return 1


@component.add(
    name="total_energy_pkm",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_pkm_fuel": 1},
)
def total_energy_pkm():
    return sum(energy_pkm_fuel().rename({"fuels": "fuels!"}), dim=["fuels!"])


@component.add(
    name="variation_efficiency_pkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_data": 1,
        "efficiency_pkm": 1,
        "improvement_efficiency_pkm": 1,
    },
)
def variation_efficiency_pkm():
    return if_then_else(
        time() < end_historical_data(),
        lambda: xr.DataArray(
            0,
            {
                "Transport_Modes": _subscript_dict["Transport_Modes"],
                "fuels": _subscript_dict["fuels"],
            },
            ["Transport_Modes", "fuels"],
        ),
        lambda: improvement_efficiency_pkm() * efficiency_pkm(),
    )


@component.add(
    name="vehicles_buses_pkm",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_commercial_vehicles": 1,
        "predicted_pkm_by_mode_and_fuel": 1,
        "commercial_pkm_vehiclespkm": 1,
    },
)
def vehicles_buses_pkm():
    """
    Passenger buses in the system
    """
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_commercial_vehicles(time()),
        lambda: predicted_pkm_by_mode_and_fuel()
        .loc[:, "Road_heavy"]
        .reset_coords(drop=True)
        * commercial_pkm_vehiclespkm(),
    )


@component.add(
    name="vehicles_households",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_households_vehicles": 1,
        "households_vehiclespkm": 1,
        "predicted_pkm_by_mode_and_fuel": 1,
    },
)
def vehicles_households():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_households_vehicles(time()),
        lambda: predicted_pkm_by_mode_and_fuel()
        .loc[:, "Road_light"]
        .reset_coords(drop=True)
        * households_vehiclespkm(),
    )


@component.add(
    name="vehicles_rail_pkm",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_rail_pkm_vehicles": 1,
        "predicted_pkm_by_mode_and_fuel": 1,
        "rail_vehiclepkm": 1,
    },
)
def vehicles_rail_pkm():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_rail_pkm_vehicles(time()),
        lambda: predicted_pkm_by_mode_and_fuel().loc[:, "Rail"].reset_coords(drop=True)
        * rail_vehiclepkm(),
    )
