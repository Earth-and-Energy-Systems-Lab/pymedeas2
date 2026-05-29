"""
Module transport.tkm
Translated using PySD version 3.14.3
"""

@component.add(
    name="aux_GPD0_tkm",
    units="T$/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "tkm_ref_year": 1, "gdp_eu": 1, "time_step": 1},
)
def aux_gpd0_tkm():
    return (
        if_then_else(time() == tkm_ref_year(), lambda: gdp_eu(), lambda: 0)
        / time_step()
    )


@component.add(
    name="beta_tkm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_tkm"},
)
def beta_tkm():
    return _ext_constant_beta_tkm()


_ext_constant_beta_tkm = ExtConstant(
    r"../transport.xlsx", "Europe", "beta_tkm", {}, _root, {}, "_ext_constant_beta_tkm"
)


@component.add(
    name="Desired_tkm_by_mode_and_fuel",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm": 1, "tkm_fuel_share": 1},
)
def desired_tkm_by_mode_and_fuel():
    return tkm() * tkm_fuel_share()


@component.add(
    name="efficiency_tkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_efficiency_tkm": 1},
    other_deps={
        "_integ_efficiency_tkm": {
            "initial": {
                "initial_efficiency_per_tkm": 1,
                "sensitivity_tkm_efficiency": 1,
            },
            "step": {"variation_efficiency_tkm": 1},
        }
    },
)
def efficiency_tkm():
    return _integ_efficiency_tkm()


_integ_efficiency_tkm = Integ(
    lambda: variation_efficiency_tkm(),
    lambda: initial_efficiency_per_tkm() * sensitivity_tkm_efficiency(),
    "_integ_efficiency_tkm",
)


@component.add(
    name="end_historical_data",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_end_historical_data"},
)
def end_historical_data():
    return _ext_constant_end_historical_data()


_ext_constant_end_historical_data = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "end_historical_data",
    {},
    _root,
    {},
    "_ext_constant_end_historical_data",
)


@component.add(
    name="energy_by_fuel_mode_tkm",
    units="EJ/year",
    subscripts=["final_sources", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_tkm": 5, "historic_share_electricity_hybrid": 2, "time": 2},
)
def energy_by_fuel_mode_tkm():
    """
    Energy demand variation due to the changes in modes and fuels on the freight transport
    """
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
            energy_tkm().loc["liq", :].reset_coords(drop=True)
            + energy_tkm().loc["hybrid", :].reset_coords(drop=True)
            * (1 - historic_share_electricity_hybrid(time()))
        )
        .expand_dims({"final_sources": ["liquids"]}, 0)
        .values
    )
    value.loc[["gases"], :] = (
        energy_tkm()
        .loc["gas", :]
        .reset_coords(drop=True)
        .expand_dims({"final_sources": ["gases"]}, 0)
        .values
    )
    value.loc[["electricity"], :] = (
        (
            energy_tkm().loc["elect", :].reset_coords(drop=True)
            + energy_tkm().loc["hybrid", :].reset_coords(drop=True)
            * historic_share_electricity_hybrid(time())
        )
        .expand_dims({"final_sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = 0
    value.loc[["solids"], :] = 0
    return value


@component.add(
    name="energy_intensity_by_transport_sector",
    units="EJ/(year*T$)",
    subscripts=["final_sources", "sectors_transport"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_transport_by_sector_fuel": 1,
        "total_output_required_by_sector": 1,
        "m_to_t": 1,
    },
)
def energy_intensity_by_transport_sector():
    return (
        energy_transport_by_sector_fuel()
        / total_output_required_by_sector()
        .loc[_subscript_dict["sectors_transport"]]
        .rename({"sectors": "sectors_transport"})
        / m_to_t()
    )


@component.add(
    name="Energy_intensity_commercial_transport_delayed",
    units="EJ/T$",
    subscripts=["final_sources", "sectors_transport"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_energy_intensity_commercial_transport_delayed": 1},
    other_deps={
        "_delayfixed_energy_intensity_commercial_transport_delayed": {
            "initial": {"energy_intensity_by_transport_sector": 1, "time_step": 1},
            "step": {"energy_intensity_by_transport_sector": 1},
        }
    },
)
def energy_intensity_commercial_transport_delayed():
    return _delayfixed_energy_intensity_commercial_transport_delayed()


_delayfixed_energy_intensity_commercial_transport_delayed = DelayFixed(
    lambda: energy_intensity_by_transport_sector(),
    lambda: time_step(),
    lambda: energy_intensity_by_transport_sector(),
    time_step,
    "_delayfixed_energy_intensity_commercial_transport_delayed",
)


@component.add(
    name="Energy_intensity_commercial_transport_variation",
    units="EJ/(T$*year)",
    subscripts=["final_sources", "sectors"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_intensity_by_transport_sector": 1,
        "energy_intensity_commercial_transport_delayed": 1,
        "time_step": 1,
    },
)
def energy_intensity_commercial_transport_variation():
    """
    Variation in the energy intensity of transport sector
    """
    value = xr.DataArray(
        np.nan,
        {
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    )
    value.loc[:, _subscript_dict["sectors_transport"]] = (
        (
            energy_intensity_by_transport_sector()
            - energy_intensity_commercial_transport_delayed()
        )
        / time_step()
    ).values
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[:, _subscript_dict["sectors_transport"]] = False
    value.values[except_subs.values] = 0
    return value


@component.add(
    name="energy_tkm",
    units="EJ/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tkm_by_mode_and_fuel": 1, "efficiency_tkm": 1, "mj_per_ej": 1},
)
def energy_tkm():
    return (
        real_tkm_by_mode_and_fuel()
        * efficiency_tkm().transpose("fuels", "Transport_Modes")
        / mj_per_ej()
    )


@component.add(
    name="energy_tkm_fuel",
    units="EJ/year",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_tkm": 1},
)
def energy_tkm_fuel():
    return sum(
        energy_tkm().rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name="Energy_transport_by_mode_fuel",
    units="EJ/year",
    subscripts=["final_sources", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_by_fuel_mode_tkm": 1, "energy_by_fuel_mode_pkm": 1},
)
def energy_transport_by_mode_fuel():
    return energy_by_fuel_mode_tkm() + energy_by_fuel_mode_pkm()


@component.add(
    name="energy_transport_by_sector_fuel",
    units="EJ/year",
    subscripts=["final_sources", "sectors_transport"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_transport_by_mode_fuel": 3},
)
def energy_transport_by_sector_fuel():
    value = xr.DataArray(
        np.nan,
        {
            "final_sources": _subscript_dict["final_sources"],
            "sectors_transport": _subscript_dict["sectors_transport"],
        },
        ["final_sources", "sectors_transport"],
    )
    value.loc[:, ["Air_transport"]] = (
        energy_transport_by_mode_fuel()
        .loc[:, "Air"]
        .reset_coords(drop=True)
        .expand_dims({"sectors": ["Air_transport"]}, 1)
        .values
    )
    value.loc[:, ["Maritime_and_inland_water_transport"]] = (
        energy_transport_by_mode_fuel()
        .loc[:, "Maritime"]
        .reset_coords(drop=True)
        .expand_dims({"sectors": ["Maritime_and_inland_water_transport"]}, 1)
        .values
    )
    value.loc[:, ["Land_transport_pipeline_transport"]] = (
        sum(
            energy_transport_by_mode_fuel()
            .loc[:, _subscript_dict["Land"]]
            .rename({"Transport_Modes": "Land!"}),
            dim=["Land!"],
        )
        .expand_dims({"sectors": ["Land_transport_pipeline_transport"]}, 1)
        .values
    )
    return value


@component.add(
    name="energy_transport_sector",
    units="EJ/year",
    subscripts=["sectors_transport"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_transport_by_sector_fuel": 1},
)
def energy_transport_sector():
    return sum(
        energy_transport_by_sector_fuel().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="fuel_share_air",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_air",
        "__lookup__": "_ext_lookup_fuel_share_air",
    },
)
def fuel_share_air(x, final_subs=None):
    return _ext_lookup_fuel_share_air(x, final_subs)


_ext_lookup_fuel_share_air = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_air_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_air",
)


@component.add(
    name="fuel_share_maritime",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_maritime",
        "__lookup__": "_ext_lookup_fuel_share_maritime",
    },
)
def fuel_share_maritime(x, final_subs=None):
    """
    Fuel share of maritime transport every 5 years
    """
    return _ext_lookup_fuel_share_maritime(x, final_subs)


_ext_lookup_fuel_share_maritime = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_maritime_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime",
)


@component.add(
    name="fuel_share_rail",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_rail",
        "__lookup__": "_ext_lookup_fuel_share_rail",
    },
)
def fuel_share_rail(x, final_subs=None):
    return _ext_lookup_fuel_share_rail(x, final_subs)


_ext_lookup_fuel_share_rail = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_rail_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_rail",
)


@component.add(
    name="fuel_share_road",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_road",
        "__lookup__": "_ext_lookup_fuel_share_road",
    },
)
def fuel_share_road(x, final_subs=None):
    """
    Fuel share of inland passenger tranport every 5 years
    """
    return _ext_lookup_fuel_share_road(x, final_subs)


_ext_lookup_fuel_share_road = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_road_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_road",
)


@component.add(
    name="GDP0_tkm",
    units="T$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gdp0_tkm": 1},
    other_deps={"_integ_gdp0_tkm": {"initial": {}, "step": {"aux_gpd0_tkm": 1}}},
)
def gdp0_tkm():
    return _integ_gdp0_tkm()


_integ_gdp0_tkm = Integ(lambda: aux_gpd0_tkm(), lambda: 0, "_integ_gdp0_tkm")


@component.add(
    name="heavy_trucks_per_tkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_heavy_truck_vehicles": 1,
        "initial_tkm": 1,
        "initial_share_road_heavy_tkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def heavy_trucks_per_tkm():
    return (
        sum(
            historic_heavy_truck_vehicles(time()).rename({"fuels": "fuels!"}),
            dim=["fuels!"],
        )
        / (initial_tkm() * initial_share_road_heavy_tkm() * 1000000000.0)
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="hist_tkm",
    units="ton*km/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_tkm",
        "__lookup__": "_ext_lookup_hist_tkm",
    },
)
def hist_tkm(x, final_subs=None):
    return _ext_lookup_hist_tkm(x, final_subs)


_ext_lookup_hist_tkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_tkm",
    {},
    _root,
    {},
    "_ext_lookup_hist_tkm",
)


@component.add(
    name="hist_transport_share_tkm",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_transport_share_tkm",
        "__lookup__": "_ext_lookup_hist_transport_share_tkm",
    },
)
def hist_transport_share_tkm(x, final_subs=None):
    return _ext_lookup_hist_transport_share_tkm(x, final_subs)


_ext_lookup_hist_transport_share_tkm = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "share_transport_mode_hist_tkm",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_hist_transport_share_tkm",
)


@component.add(
    name="historic_fuel_share_rail",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_rail",
        "__lookup__": "_ext_lookup_historic_fuel_share_rail",
    },
)
def historic_fuel_share_rail(x, final_subs=None):
    """
    Historic share of fuels in the rail freight transport
    """
    return _ext_lookup_historic_fuel_share_rail(x, final_subs)


_ext_lookup_historic_fuel_share_rail = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_rail_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_rail",
)


@component.add(
    name="historic_fuel_share_road_heavy",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_road_heavy",
        "__lookup__": "_ext_lookup_historic_fuel_share_road_heavy",
    },
)
def historic_fuel_share_road_heavy(x, final_subs=None):
    return _ext_lookup_historic_fuel_share_road_heavy(x, final_subs)


_ext_lookup_historic_fuel_share_road_heavy = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_road_heavy_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_road_heavy",
)


@component.add(
    name="historic_fuel_share_road_light",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_fuel_share_road_light",
        "__lookup__": "_ext_lookup_historic_fuel_share_road_light",
    },
)
def historic_fuel_share_road_light(x, final_subs=None):
    return _ext_lookup_historic_fuel_share_road_light(x, final_subs)


_ext_lookup_historic_fuel_share_road_light = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_fuel_share_road_light_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_fuel_share_road_light",
)


@component.add(
    name="historic_heavy_truck_vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_heavy_truck_vehicles",
        "__lookup__": "_ext_lookup_historic_heavy_truck_vehicles",
    },
)
def historic_heavy_truck_vehicles(x, final_subs=None):
    return _ext_lookup_historic_heavy_truck_vehicles(x, final_subs)


_ext_lookup_historic_heavy_truck_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_heavy_truck_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_heavy_truck_vehicles",
)


@component.add(
    name="historic_truck_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_truck_vehicles",
        "__lookup__": "_ext_lookup_historic_truck_vehicles",
    },
)
def historic_truck_vehicles(x, final_subs=None):
    return _ext_lookup_historic_truck_vehicles(x, final_subs)


_ext_lookup_historic_truck_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_light_truck_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_truck_vehicles",
)


@component.add(
    name="improvment_efiiciency_tkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_improvment_efiiciency_tkm"},
)
def improvment_efiiciency_tkm():
    return _ext_constant_improvment_efiiciency_tkm()


_ext_constant_improvment_efiiciency_tkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "efficiency_tkm_improvment*",
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    _root,
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    "_ext_constant_improvment_efiiciency_tkm",
)


@component.add(
    name="initial_efficiency_per_tkm",
    units="MJ/tkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_efficiency_per_tkm"},
)
def initial_efficiency_per_tkm():
    return _ext_constant_initial_efficiency_per_tkm()


_ext_constant_initial_efficiency_per_tkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "efficiency_tkm*",
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    _root,
    {
        "Transport_Modes": _subscript_dict["Transport_Modes"],
        "fuels": _subscript_dict["fuels"],
    },
    "_ext_constant_initial_efficiency_per_tkm",
)


@component.add(
    name="initial_fuel_share_air_tkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_air_tkm"},
)
def initial_fuel_share_air_tkm():
    return _ext_constant_initial_fuel_share_air_tkm()


_ext_constant_initial_fuel_share_air_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_air_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_tkm",
)


@component.add(
    name="initial_fuel_share_maritime_tkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_maritime_tkm"},
)
def initial_fuel_share_maritime_tkm():
    """
    air and maritime have the same start value
    """
    return _ext_constant_initial_fuel_share_maritime_tkm()


_ext_constant_initial_fuel_share_maritime_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_air_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_tkm",
)


@component.add(
    name="initial_share_rail_tkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_rail_tkm"},
)
def initial_share_rail_tkm():
    return _ext_constant_initial_share_rail_tkm()


_ext_constant_initial_share_rail_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_rail_tkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_rail_tkm",
)


@component.add(
    name="initial_share_road_heavy_tkm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_road_heavy_tkm"},
)
def initial_share_road_heavy_tkm():
    return _ext_constant_initial_share_road_heavy_tkm()


_ext_constant_initial_share_road_heavy_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_road_heavy_tkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_road_heavy_tkm",
)


@component.add(
    name="initial_share_road_light_tkm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_share_road_light_tkm"},
)
def initial_share_road_light_tkm():
    return _ext_constant_initial_share_road_light_tkm()


_ext_constant_initial_share_road_light_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_share_road_light_tkm",
    {},
    _root,
    {},
    "_ext_constant_initial_share_road_light_tkm",
)


@component.add(
    name="initial_tkm",
    units="tonnes*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_tkm"},
)
def initial_tkm():
    return _ext_constant_initial_tkm()


_ext_constant_initial_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "tkm_initial",
    {},
    _root,
    {},
    "_ext_constant_initial_tkm",
)


@component.add(
    name="light_trucks_per_tkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_truck_vehicles": 1,
        "initial_tkm": 1,
        "initial_share_road_light_tkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def light_trucks_per_tkm():
    return (
        sum(historic_truck_vehicles(time()).rename({"fuels": "fuels!"}), dim=["fuels!"])
        / (initial_tkm() * initial_share_road_light_tkm() * 1000000000.0)
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="log_tkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predicted_log_tkm_hat": 1, "resid": 1},
)
def log_tkm():
    return predicted_log_tkm_hat() + resid()


@component.add(
    name="mode_share_tkm",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mode_share_tkm_aux": 2},
)
def mode_share_tkm():
    return mode_share_tkm_aux() / sum(
        mode_share_tkm_aux().rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name="mode_share_tkm_aux",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "mode_share_tkm_policy": 5,
        "sensitivity_rail_mode_share": 5,
        "proportion_mode_share_tkm": 4,
    },
)
def mode_share_tkm_aux():
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
                    float(mode_share_tkm_policy(time()).loc["Rail"])
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
                    float(mode_share_tkm_policy(time()).loc["Road_light"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_tkm().loc["Road_light"]),
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
                    float(mode_share_tkm_policy(time()).loc["Road_heavy"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_tkm().loc["Road_heavy"]),
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
                    float(mode_share_tkm_policy(time()).loc["Maritime"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_tkm().loc["Maritime"]),
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
                    float(mode_share_tkm_policy(time()).loc["Air"])
                    - sensitivity_rail_mode_share()
                    * float(proportion_mode_share_tkm().loc["Air"]),
                )
            ),
        )
    )
    return value


@component.add(
    name="mode_share_tkm_policy",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_mode_share_tkm_policy",
        "__lookup__": "_ext_lookup_mode_share_tkm_policy",
    },
)
def mode_share_tkm_policy(x, final_subs=None):
    return _ext_lookup_mode_share_tkm_policy(x, final_subs)


_ext_lookup_mode_share_tkm_policy = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "Year_transport_share",
    "tkm_share",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_mode_share_tkm_policy",
)


@component.add(
    name="mode_share_tkm_policy_last_year",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"start_year_policies_transport": 1, "mode_share_tkm_policy": 1},
)
def mode_share_tkm_policy_last_year():
    return mode_share_tkm_policy(start_year_policies_transport())


@component.add(
    name="phi_tkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_phi_tkm"},
)
def phi_tkm():
    return _ext_constant_phi_tkm()


_ext_constant_phi_tkm = ExtConstant(
    r"../transport.xlsx", "Europe", "phi_tkm", {}, _root, {}, "_ext_constant_phi_tkm"
)


@component.add(
    name="predicted_log_tkm_hat",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu": 2, "gdp0_tkm": 2, "beta_tkm": 1},
)
def predicted_log_tkm_hat():
    return if_then_else(
        zidz(gdp_eu(), gdp0_tkm()) > 0,
        lambda: beta_tkm() * float(np.log(gdp_eu() / gdp0_tkm())),
        lambda: 0,
    )


@component.add(
    name="predicted_tkm",
    units="ton*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_data": 1,
        "tkm0": 2,
        "log_tkm": 1,
        "sensitivity_pkm_and_tkm": 1,
        "gdp_eu": 1,
        "beta_tkm": 1,
        "gdp0_tkm": 1,
    },
)
def predicted_tkm():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: tkm0() * float(np.exp(log_tkm())),
        lambda: tkm0()
        * (gdp_eu() / gdp0_tkm()) ** beta_tkm()
        * sensitivity_pkm_and_tkm(),
    )


@component.add(
    name="predicted_tkm_by_mode_and_fuel",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "hist_tkm": 1,
        "predicted_tkm": 1,
        "tkm_fuel_share": 1,
    },
)
def predicted_tkm_by_mode_and_fuel():
    return (
        if_then_else(
            time() <= end_historical_data(),
            lambda: hist_tkm(time()),
            lambda: predicted_tkm(),
        )
        * tkm_fuel_share()
        * 1000000000.0
    )


@component.add(
    name="proportion_mode_share_tkm",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "mode_share_tkm_policy": 2},
)
def proportion_mode_share_tkm():
    return mode_share_tkm_policy(time()) / sum(
        mode_share_tkm_policy(time()).rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )


@component.add(
    name="rails_per_tkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_rail_tkm_vehicles": 1,
        "initial_tkm": 1,
        "initial_share_rail_tkm": 1,
        "sensitivity_vehicles_efficiency": 1,
    },
)
def rails_per_tkm():
    return (
        sum(
            historic_rail_tkm_vehicles(time()).rename({"fuels": "fuels!"}),
            dim=["fuels!"],
        )
        / (initial_tkm() * initial_share_rail_tkm() * 1000000000.0)
        * sensitivity_vehicles_efficiency()
    )


@component.add(
    name="real_tkm_by_mode",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tkm_by_mode_and_fuel": 1},
)
def real_tkm_by_mode():
    return sum(real_tkm_by_mode_and_fuel().rename({"fuels": "fuels!"}), dim=["fuels!"])


@component.add(
    name="Real_tkm_by_mode_and_fuel",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_tkm_by_mode_and_fuel": 1},
)
def real_tkm_by_mode_and_fuel():
    return desired_tkm_by_mode_and_fuel()


@component.add(
    name="Real_tkm_by_mode_and_fuel_delayed",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_tkm_by_mode_and_fuel_delayed": 1},
    other_deps={
        "_delayfixed_real_tkm_by_mode_and_fuel_delayed": {
            "initial": {"real_tkm_by_mode_and_fuel": 1, "time_step": 1},
            "step": {"real_tkm_by_mode_and_fuel": 1},
        }
    },
)
def real_tkm_by_mode_and_fuel_delayed():
    return _delayfixed_real_tkm_by_mode_and_fuel_delayed()


_delayfixed_real_tkm_by_mode_and_fuel_delayed = DelayFixed(
    lambda: real_tkm_by_mode_and_fuel(),
    lambda: time_step(),
    lambda: real_tkm_by_mode_and_fuel(),
    time_step,
    "_delayfixed_real_tkm_by_mode_and_fuel_delayed",
)


@component.add(
    name="required_FED_by_fs_not_transport_sectors",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel_eu": 1,
        "households_final_energy_demand": 1,
        "required_fed_by_fs_transport_sectors": 1,
    },
)
def required_fed_by_fs_not_transport_sectors():
    return (
        sum(
            required_final_energy_by_sector_and_fuel_eu().rename(
                {"sectors": "sectors!"}
            ),
            dim=["sectors!"],
        )
        + households_final_energy_demand()
        - required_fed_by_fs_transport_sectors()
    )


@component.add(
    name="required_FED_by_fs_transport_sectors",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_final_energy_by_sector_and_fuel_eu": 1},
)
def required_fed_by_fs_transport_sectors():
    return sum(
        required_final_energy_by_sector_and_fuel_eu()
        .loc[:, _subscript_dict["sectors_transport"]]
        .rename({"sectors": "sectors_transport!"}),
        dim=["sectors_transport!"],
    )


@component.add(
    name="required_FED_transport_sectors",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fs_transport_sectors": 1},
)
def required_fed_transport_sectors():
    return sum(
        required_fed_by_fs_transport_sectors().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name="resid",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 2,
        "resid_delayed": 1,
        "resid_initial": 1,
        "phi_tkm": 1,
    },
)
def resid():
    return if_then_else(
        time() < end_historical_data(),
        lambda: 0,
        lambda: if_then_else(
            time() == end_historical_data(),
            lambda: resid_initial(),
            lambda: phi_tkm() * resid_delayed(),
        ),
    )


@component.add(
    name="resid_delayed",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_resid_delayed": 1},
    other_deps={"_delayfixed_resid_delayed": {"initial": {}, "step": {"resid": 1}}},
)
def resid_delayed():
    return _delayfixed_resid_delayed()


_delayfixed_resid_delayed = DelayFixed(
    lambda: resid(), lambda: 1, lambda: 0, time_step, "_delayfixed_resid_delayed"
)


@component.add(
    name="resid_initial",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "end_historical_data": 1, "residu_tkm": 1},
)
def resid_initial():
    return if_then_else(time() < end_historical_data(), lambda: 0, lambda: residu_tkm())


@component.add(
    name="residu_tkm",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_residu_tkm"},
)
def residu_tkm():
    return _ext_constant_residu_tkm()


_ext_constant_residu_tkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "res0_tkm",
    {},
    _root,
    {},
    "_ext_constant_residu_tkm",
)


@component.add(
    name="sensitivity_pkm_and_tkm",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_pkm_and_tkm():
    return 1


@component.add(
    name="sensitivity_rail_mode_share",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_rail_mode_share():
    return 0


@component.add(
    name="sensitivity_tkm_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_tkm_efficiency():
    return 1


@component.add(
    name="start_year_policies_transport",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_policies_transport"},
)
def start_year_policies_transport():
    return _ext_constant_start_year_policies_transport()


_ext_constant_start_year_policies_transport = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_year_policies_transport",
    {},
    _root,
    {},
    "_ext_constant_start_year_policies_transport",
)


@component.add(
    name="sum_tkm_fuel_share",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm_fuel_share": 1},
)
def sum_tkm_fuel_share():
    return sum(
        tkm_fuel_share().rename(
            {"fuels": "fuels!", "Transport_Modes": "Transport_Modes!"}
        ),
        dim=["fuels!", "Transport_Modes!"],
    )


@component.add(
    name="tau_tkm",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1, "phi_tkm": 1},
)
def tau_tkm():
    return -time_step() / float(np.log(phi_tkm()))


@component.add(
    name="tkm",
    units="ton*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "end_historical_data": 1, "hist_tkm": 1, "predicted_tkm": 1},
)
def tkm():
    return (
        if_then_else(
            time() <= end_historical_data(),
            lambda: hist_tkm(time()),
            lambda: predicted_tkm(),
        )
        * 1000000000.0
    )


@component.add(
    name="tkm0",
    units="ton*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "tkm_ref_year": 2, "hist_tkm": 1},
)
def tkm0():
    return if_then_else(
        time() >= tkm_ref_year(), lambda: hist_tkm(tkm_ref_year()), lambda: 0
    )


@component.add(
    name="tkm_fuel_share",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tkm_fuel_share_road_heavy": 1,
        "tkm_mode_share": 5,
        "tkm_fuel_share_maritime": 1,
        "tkm_fuel_share_air": 1,
        "tkm_fuel_share_rail": 1,
        "tkm_fuel_share_road_light": 1,
    },
)
def tkm_fuel_share():
    """
    Percentage of the total tkm of each mode and fuel
    """
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_heavy"]] = (
        (tkm_fuel_share_road_heavy() * float(tkm_mode_share().loc["Road_heavy"]))
        .expand_dims({"Land": ["Road_heavy"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (tkm_fuel_share_maritime() * float(tkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport_Modes": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (tkm_fuel_share_air() * float(tkm_mode_share().loc["Air"]))
        .expand_dims({"Transport_Modes": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Rail"]] = (
        (tkm_fuel_share_rail() * float(tkm_mode_share().loc["Rail"]))
        .expand_dims({"Land": ["Rail"]}, 1)
        .values
    )
    value.loc[:, ["Road_light"]] = (
        (tkm_fuel_share_road_light() * float(tkm_mode_share().loc["Road_light"]))
        .expand_dims({"Land": ["Road_light"]}, 1)
        .values
    )
    return value


@component.add(
    name="tkm_fuel_share_air",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_air_tkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_air": 2,
    },
)
def tkm_fuel_share_air():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_air_tkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_air_tkm()
            + (
                (
                    fuel_share_air(start_year_policies_transport())
                    - initial_fuel_share_air_tkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_air(time()),
        ),
    )


@component.add(
    name="tkm_fuel_share_maritime",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_maritime_tkm": 3,
        "fuel_share_maritime": 2,
        "start_year_policies_transport": 3,
    },
)
def tkm_fuel_share_maritime():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_maritime_tkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_maritime_tkm()
            + (
                (
                    fuel_share_maritime(start_year_policies_transport())
                    - initial_fuel_share_maritime_tkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_maritime(time()),
        ),
    )


@component.add(
    name="tkm_fuel_share_rail",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 5,
        "historic_fuel_share_rail": 3,
        "fuel_share_rail": 2,
        "start_year_policies_transport": 3,
    },
)
def tkm_fuel_share_rail():
    return if_then_else(
        time() < end_historical_data(),
        lambda: historic_fuel_share_rail(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_rail(end_historical_data())
            + (
                (
                    fuel_share_rail(start_year_policies_transport())
                    - historic_fuel_share_rail(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_rail(time()),
        ),
    )


@component.add(
    name="tkm_fuel_share_road_heavy",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 6,
        "historic_fuel_share_road_heavy": 3,
        "fuel_share_road": 2,
        "start_year_policies_transport": 3,
    },
)
def tkm_fuel_share_road_heavy():
    return if_then_else(
        time() < end_historical_data(),
        lambda: historic_fuel_share_road_heavy(end_historical_data()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_road_heavy(end_historical_data())
            + (
                (
                    fuel_share_road(start_year_policies_transport())
                    - historic_fuel_share_road_heavy(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_road(time()),
        ),
    )


@component.add(
    name="tkm_fuel_share_road_light",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 6,
        "historic_fuel_share_road_light": 3,
        "fuel_share_road": 2,
        "start_year_policies_transport": 3,
    },
)
def tkm_fuel_share_road_light():
    return if_then_else(
        time() < end_historical_data(),
        lambda: historic_fuel_share_road_light(end_historical_data()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: historic_fuel_share_road_light(end_historical_data())
            + (
                (
                    fuel_share_road(start_year_policies_transport())
                    - historic_fuel_share_road_light(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_road(time()),
        ),
    )


@component.add(
    name="tkm_mode_share",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 5,
        "hist_transport_share_tkm": 3,
        "mode_share_tkm_policy_last_year": 1,
        "mode_share_tkm": 1,
        "start_year_policies_transport": 2,
    },
)
def tkm_mode_share():
    return if_then_else(
        time() < end_historical_data(),
        lambda: hist_transport_share_tkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: hist_transport_share_tkm(end_historical_data())
            + (
                (
                    mode_share_tkm_policy_last_year()
                    - hist_transport_share_tkm(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: mode_share_tkm(),
        ),
    )


@component.add(
    name="tkm_ref_year",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tkm_ref_year"},
)
def tkm_ref_year():
    return _ext_constant_tkm_ref_year()


_ext_constant_tkm_ref_year = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "year0_tkm",
    {},
    _root,
    {},
    "_ext_constant_tkm_ref_year",
)


@component.add(
    name="total_energy_tkm",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_tkm_fuel": 1},
)
def total_energy_tkm():
    return sum(energy_tkm_fuel().rename({"fuels": "fuels!"}), dim=["fuels!"])


@component.add(
    name="total_energy_transport",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_energy_tkm": 1, "total_energy_pkm": 1},
)
def total_energy_transport():
    return total_energy_tkm() + total_energy_pkm()


@component.add(
    name="total_energy_transport_by_fuel",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_tkm_fuel": 1, "energy_pkm_fuel": 1},
)
def total_energy_transport_by_fuel():
    return energy_tkm_fuel() + energy_pkm_fuel()


@component.add(
    name="total_energy_transport_final_source",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_energy_transport_by_fuel": 3},
)
def total_energy_transport_final_source():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["liquids"]] = float(total_energy_transport_by_fuel().loc["liq"])
    value.loc[["gases"]] = float(total_energy_transport_by_fuel().loc["gas"])
    value.loc[["electricity"]] = float(total_energy_transport_by_fuel().loc["elect"])
    value.loc[["solids"]] = 0
    value.loc[["heat"]] = 0
    return value


@component.add(
    name="variation_efficiency_tkm",
    subscripts=["Transport_Modes", "fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_data": 1,
        "efficiency_tkm": 1,
        "improvment_efiiciency_tkm": 1,
    },
)
def variation_efficiency_tkm():
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
        lambda: efficiency_tkm() * improvment_efiiciency_tkm(),
    )


@component.add(
    name="vehicles_heavy_trucks",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_heavy_truck_vehicles": 1,
        "predicted_tkm_by_mode_and_fuel": 1,
        "heavy_trucks_per_tkm": 1,
    },
)
def vehicles_heavy_trucks():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_heavy_truck_vehicles(time()),
        lambda: predicted_tkm_by_mode_and_fuel()
        .loc[:, "Road_heavy"]
        .reset_coords(drop=True)
        * heavy_trucks_per_tkm(),
    )


@component.add(
    name="vehicles_light_trucks",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_truck_vehicles": 1,
        "predicted_tkm_by_mode_and_fuel": 1,
        "light_trucks_per_tkm": 1,
    },
)
def vehicles_light_trucks():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_truck_vehicles(time()),
        lambda: predicted_tkm_by_mode_and_fuel()
        .loc[:, "Road_light"]
        .reset_coords(drop=True)
        * light_trucks_per_tkm(),
    )


@component.add(
    name="vehicles_rail_tkm",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "historic_rail_tkm_vehicles": 1,
        "predicted_tkm_by_mode_and_fuel": 1,
        "rails_per_tkm": 1,
    },
)
def vehicles_rail_tkm():
    return if_then_else(
        time() <= end_historical_data(),
        lambda: historic_rail_tkm_vehicles(time()),
        lambda: predicted_tkm_by_mode_and_fuel().loc[:, "Rail"].reset_coords(drop=True)
        * rails_per_tkm(),
    )
