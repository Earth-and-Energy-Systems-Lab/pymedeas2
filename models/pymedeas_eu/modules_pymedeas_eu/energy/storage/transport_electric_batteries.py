"""
Module energy.storage.transport_electric_batteries
Translated using PySD version 3.14.3
"""

@component.add(
    name="bat_number_EV",
    units="batteries",
    subscripts=["battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vehicles_households": 1,
        "vehicles_buses_pkm": 1,
        "vehicles_light_trucks": 1,
        "vehicles_heavy_trucks": 1,
    },
)
def bat_number_ev():
    """
    Required number of electric batteries for electric vehicles
    """
    value = xr.DataArray(
        np.nan, {"battery_modes": _subscript_dict["battery_modes"]}, ["battery_modes"]
    )
    value.loc[["cars"]] = float(vehicles_households().loc["elect"])
    value.loc[["buses"]] = float(vehicles_buses_pkm().loc["elect"])
    value.loc[["light_trucks"]] = float(vehicles_light_trucks().loc["elect"])
    value.loc[["heavy_trucks"]] = float(vehicles_heavy_trucks().loc["elect"])
    return value


@component.add(
    name="bat_number_hib",
    units="batteries",
    subscripts=["battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vehicles_households": 1,
        "bateries_ratio_hib_hv": 4,
        "vehicles_buses_pkm": 1,
        "vehicles_light_trucks": 1,
        "vehicles_heavy_trucks": 1,
    },
)
def bat_number_hib():
    """
    Required number of electric batteries for hybrid vehicles expressed in terms of a stantad a 21,3KWh battery.
    """
    value = xr.DataArray(
        np.nan, {"battery_modes": _subscript_dict["battery_modes"]}, ["battery_modes"]
    )
    value.loc[["cars"]] = (
        float(vehicles_households().loc["hybrid"]) * bateries_ratio_hib_hv()
    )
    value.loc[["buses"]] = (
        float(vehicles_buses_pkm().loc["hybrid"]) * bateries_ratio_hib_hv()
    )
    value.loc[["light_trucks"]] = (
        float(vehicles_light_trucks().loc["hybrid"]) * bateries_ratio_hib_hv()
    )
    value.loc[["heavy_trucks"]] = (
        float(vehicles_heavy_trucks().loc["hybrid"]) * bateries_ratio_hib_hv()
    )
    return value


@component.add(
    name="bateries_ratio_hib_HV",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_bateries_ratio_hib_hv"},
)
def bateries_ratio_hib_hv():
    """
    Ratio between the size of the hybrid HV batteries and the standard batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_hv()


_ext_constant_bateries_ratio_hib_hv = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "bateries_ratio_hib_hv",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_hib_hv",
)


@component.add(
    name='"batteries_EV+hib"',
    units="batteries",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_batteries_evhib": 1},
    other_deps={
        "_integ_batteries_evhib": {
            "initial": {},
            "step": {
                "new_batteries": 1,
                "replacement_batteries": 1,
                "discarded_batteries": 1,
            },
        }
    },
)
def batteries_evhib():
    """
    Number of batteries required for electric and hybrid mobility espreseed in termos of "standard" electric batteries of 21,3KWh
    """
    return _integ_batteries_evhib()


_integ_batteries_evhib = Integ(
    lambda: new_batteries() + replacement_batteries() - discarded_batteries(),
    lambda: xr.DataArray(
        1,
        {
            "battery_modes": _subscript_dict["battery_modes"],
            "EV_bat": _subscript_dict["EV_bat"],
        },
        ["battery_modes", "EV_bat"],
    ),
    "_integ_batteries_evhib",
)


@component.add(
    name="batteries_per_mode_and_tech",
    units="batteries",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_number_standard_batteries": 1,
        "share_battery_per_mode_and_tech": 1,
    },
)
def batteries_per_mode_and_tech():
    return required_number_standard_batteries() * share_battery_per_mode_and_tech()


@component.add(
    name="discarded_batteries",
    units="batteries/year",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"batteries_evhib": 1, "lifetime_ev_batteries": 1},
)
def discarded_batteries():
    """
    Discarded electric batteries due to wear.
    """
    return np.maximum(
        0,
        zidz(
            batteries_evhib(),
            lifetime_ev_batteries().transpose("battery_modes", "EV_bat"),
        ),
    )


@component.add(
    name="EV_batteries_TW",
    units="TW",
    subscripts=["EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"batteries_evhib": 1, "kw_per_battery_ev": 1, "kw_per_tw": 1},
)
def ev_batteries_tw():
    """
    Electric batteries from electric vehicles, expresed in terms of power available (TW)
    """
    return xr.DataArray(
        sum(
            batteries_evhib().rename(
                {"battery_modes": "battery_modes!", "EV_bat": "EV_bat!"}
            ),
            dim=["battery_modes!", "EV_bat!"],
        )
        * kw_per_battery_ev()
        / kw_per_tw(),
        {"EV_bat": _subscript_dict["EV_bat"]},
        ["EV_bat"],
    )


@component.add(
    name="historic_air_pkm_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_air_pkm_vehicles",
        "__lookup__": "_ext_lookup_historic_air_pkm_vehicles",
    },
)
def historic_air_pkm_vehicles(x, final_subs=None):
    return _ext_lookup_historic_air_pkm_vehicles(x, final_subs)


_ext_lookup_historic_air_pkm_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_air_pkm_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_air_pkm_vehicles",
)


@component.add(
    name="historic_air_tkm_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_air_tkm_vehicles",
        "__lookup__": "_ext_lookup_historic_air_tkm_vehicles",
    },
)
def historic_air_tkm_vehicles(x, final_subs=None):
    return _ext_lookup_historic_air_tkm_vehicles(x, final_subs)


_ext_lookup_historic_air_tkm_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_air_tkm_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_air_tkm_vehicles",
)


@component.add(
    name="historic_rail_pkm_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_rail_pkm_vehicles",
        "__lookup__": "_ext_lookup_historic_rail_pkm_vehicles",
    },
)
def historic_rail_pkm_vehicles(x, final_subs=None):
    return _ext_lookup_historic_rail_pkm_vehicles(x, final_subs)


_ext_lookup_historic_rail_pkm_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_rail_pkm_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_rail_pkm_vehicles",
)


@component.add(
    name="historic_rail_tkm_vehicles",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_rail_tkm_vehicles",
        "__lookup__": "_ext_lookup_historic_rail_tkm_vehicles",
    },
)
def historic_rail_tkm_vehicles(x, final_subs=None):
    return _ext_lookup_historic_rail_tkm_vehicles(x, final_subs)


_ext_lookup_historic_rail_tkm_vehicles = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2023",
    "historic_rail_tkm_vehicles",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_historic_rail_tkm_vehicles",
)


@component.add(
    name="historic_share_EV_per_battery",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_share_ev_per_battery",
        "__lookup__": "_ext_lookup_historic_share_ev_per_battery",
    },
)
def historic_share_ev_per_battery(x, final_subs=None):
    return _ext_lookup_historic_share_ev_per_battery(x, final_subs)


_ext_lookup_historic_share_ev_per_battery = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "year_hist_batteries",
    "historic_share_batteries_ev",
    {"battery_modes": ["cars"], "EV_bat": _subscript_dict["EV_bat"]},
    _root,
    {
        "battery_modes": _subscript_dict["battery_modes"],
        "EV_bat": _subscript_dict["EV_bat"],
    },
    "_ext_lookup_historic_share_ev_per_battery",
)

_ext_lookup_historic_share_ev_per_battery.add(
    r"../transport.xlsx",
    "Europe",
    "year_hist_batteries",
    "historic_share_batteries_bus",
    {"battery_modes": ["buses"], "EV_bat": _subscript_dict["EV_bat"]},
)

_ext_lookup_historic_share_ev_per_battery.add(
    r"../transport.xlsx",
    "Europe",
    "year_hist_batteries",
    "historic_share_batteries_trucks",
    {"battery_modes": ["light_trucks"], "EV_bat": _subscript_dict["EV_bat"]},
)

_ext_lookup_historic_share_ev_per_battery.add(
    r"../transport.xlsx",
    "Europe",
    "year_hist_batteries",
    "historic_share_batteries_heavy_trucks",
    {"battery_modes": ["heavy_trucks"], "EV_bat": _subscript_dict["EV_bat"]},
)


@component.add(
    name="initial_pkm_vehicles",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_households_vehicles": 1,
        "historic_commercial_vehicles": 1,
        "historic_air_pkm_vehicles": 1,
        "historic_rail_pkm_vehicles": 1,
    },
)
def initial_pkm_vehicles():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_light"]] = (
        historic_households_vehicles(1995)
        .expand_dims({"Land": ["Road_light"]}, 1)
        .values
    )
    value.loc[:, ["Road_heavy"]] = (
        historic_commercial_vehicles(1995)
        .expand_dims({"Land": ["Road_heavy"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        historic_air_pkm_vehicles(1995)
        .expand_dims({"Transport_Modes": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Rail"]] = (
        historic_rail_pkm_vehicles(1995).expand_dims({"Land": ["Rail"]}, 1).values
    )
    value.loc[:, ["Maritime"]] = 0
    return value


@component.add(
    name="initial_rail_kms",
    units="km",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_rail_kms"},
)
def initial_rail_kms():
    return _ext_constant_initial_rail_kms()


_ext_constant_initial_rail_kms = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_rail_kms",
    {},
    _root,
    {},
    "_ext_constant_initial_rail_kms",
)


@component.add(
    name="initial_tkm_vehicles",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_truck_vehicles": 1,
        "historic_rail_tkm_vehicles": 1,
        "historic_air_tkm_vehicles": 1,
        "historic_heavy_truck_vehicles": 1,
    },
)
def initial_tkm_vehicles():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_light"]] = (
        historic_truck_vehicles(1995).expand_dims({"Land": ["Road_light"]}, 1).values
    )
    value.loc[:, ["Rail"]] = (
        historic_rail_tkm_vehicles(1995).expand_dims({"Land": ["Rail"]}, 1).values
    )
    value.loc[:, ["Air"]] = (
        historic_air_tkm_vehicles(1995)
        .expand_dims({"Transport_Modes": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = 0
    value.loc[:, ["Road_heavy"]] = (
        historic_heavy_truck_vehicles(1995)
        .expand_dims({"Land": ["Road_heavy"]}, 1)
        .values
    )
    return value


@component.add(
    name='"initial_vehicles/km_rail"',
    units="km/vehicles",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_rail_pkm_vehicles": 1,
        "historic_rail_tkm_vehicles": 1,
        "initial_rail_kms": 1,
    },
)
def initial_vehicleskm_rail():
    return (
        sum(
            historic_rail_pkm_vehicles(2023).rename({"fuels": "fuels!"}), dim=["fuels!"]
        )
        + sum(
            historic_rail_tkm_vehicles(2023).rename({"fuels": "fuels!"}), dim=["fuels!"]
        )
    ) / initial_rail_kms()


@component.add(
    name="kW_per_battery_EV",
    units="kW/battery",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_kw_per_battery_ev"},
)
def kw_per_battery_ev():
    """
    Average kW per battery of electrical vehicle.
    """
    return _ext_constant_kw_per_battery_ev()


_ext_constant_kw_per_battery_ev = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "kw_per_battery_ev",
    {},
    _root,
    {},
    "_ext_constant_kw_per_battery_ev",
)


@component.add(
    name="kW_per_TW", units="kW/TW", comp_type="Constant", comp_subtype="Normal"
)
def kw_per_tw():
    return 1000000000.0


@component.add(
    name="kWh_per_battery_EV",
    units="kWh/vehicles",
    subscripts=["battery_modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_kwh_per_battery_ev"},
)
def kwh_per_battery_ev():
    return _ext_constant_kwh_per_battery_ev()


_ext_constant_kwh_per_battery_ev = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "kwh_per_battery_ev*",
    {"battery_modes": _subscript_dict["battery_modes"]},
    _root,
    {"battery_modes": _subscript_dict["battery_modes"]},
    "_ext_constant_kwh_per_battery_ev",
)


@component.add(
    name="lifetime_vehicles_pkm",
    units="Years",
    subscripts=["Transport_Modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_lifetime_vehicles_pkm"},
)
def lifetime_vehicles_pkm():
    return _ext_constant_lifetime_vehicles_pkm()


_ext_constant_lifetime_vehicles_pkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "lifetime_pkm",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_constant_lifetime_vehicles_pkm",
)


@component.add(
    name="lifetime_vehicles_tkm",
    units="Years",
    subscripts=["Transport_Modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_lifetime_vehicles_tkm"},
)
def lifetime_vehicles_tkm():
    return _ext_constant_lifetime_vehicles_tkm()


_ext_constant_lifetime_vehicles_tkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "lifetime_tkm",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_constant_lifetime_vehicles_tkm",
)


@component.add(
    name="new_and_replaced_vehicles_pkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_vehicles_pkm": 1, "replacement_vehicles_pkm": 1},
)
def new_and_replaced_vehicles_pkm():
    return new_vehicles_pkm() + replacement_vehicles_pkm()


@component.add(
    name="new_and_replaced_vehicles_tkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_vehicles": 1, "replacement_vehicles_tkm": 1},
)
def new_and_replaced_vehicles_tkm():
    return new_vehicles() + replacement_vehicles_tkm()


@component.add(
    name="new_batteries",
    units="batteries/year",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smoothed_betteries_mode_tech": 1, "batteries_evhib": 1},
)
def new_batteries():
    """
    New standard electric batteries. The number of batteries converges to the desired number via a logistic funcion. Number 10 is an arbitrary parameter, the bigger the faster the convergence to the desired number of batteries. 5*"batteries EV+hib+2wE"*(1-(MIN(1,"batteries EV+hib+2wE"/required number standard batteries)))
    """
    return np.maximum(0, smoothed_betteries_mode_tech() - batteries_evhib())


@component.add(
    name="new_vehicles",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smoothed_target_vehicles_tkm": 1, "vehicles_mode_and_fuel": 1},
)
def new_vehicles():
    return smoothed_target_vehicles_tkm() - vehicles_mode_and_fuel()


@component.add(
    name="new_vehicles_pkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smoothed_target_vehicles_pkm": 1, "vehicles_mode_fuel_pkm": 1},
)
def new_vehicles_pkm():
    return smoothed_target_vehicles_pkm() - vehicles_mode_fuel_pkm()


@component.add(
    name='"new+replaced_batteries_kWh"',
    units="kWh/year",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kwh_per_battery_ev": 1, "new_batteries": 1},
)
def newreplaced_batteries_kwh():
    return kwh_per_battery_ev() * new_batteries()


@component.add(
    name='"new+replaced_batteries_TW"',
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "new_batteries": 1,
        "replacement_batteries": 1,
        "kw_per_battery_ev": 1,
        "kw_per_tw": 1,
    },
)
def newreplaced_batteries_tw():
    """
    New and replaced electric batteries.
    """
    return (
        (
            sum(
                new_batteries().rename(
                    {"battery_modes": "battery_modes!", "EV_bat": "EV_bat!"}
                ),
                dim=["battery_modes!", "EV_bat!"],
            )
            + sum(
                replacement_batteries().rename(
                    {"battery_modes": "battery_modes!", "EV_bat": "EV_bat!"}
                ),
                dim=["battery_modes!", "EV_bat!"],
            )
        )
        * kw_per_battery_ev()
        / kw_per_tw()
    )


@component.add(
    name="policy_share_battery",
    units="Dmnl",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_share_battery",
        "__lookup__": "_ext_lookup_policy_share_battery",
    },
)
def policy_share_battery(x, final_subs=None):
    return _ext_lookup_policy_share_battery(x, final_subs)


_ext_lookup_policy_share_battery = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_ev_bat",
    "p_ev_bat",
    {"battery_modes": ["cars"], "EV_bat": _subscript_dict["EV_bat"]},
    _root,
    {
        "battery_modes": _subscript_dict["battery_modes"],
        "EV_bat": _subscript_dict["EV_bat"],
    },
    "_ext_lookup_policy_share_battery",
)

_ext_lookup_policy_share_battery.add(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_ev_bat",
    "p_bus_bat",
    {"battery_modes": ["buses"], "EV_bat": _subscript_dict["EV_bat"]},
)

_ext_lookup_policy_share_battery.add(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_ev_bat",
    "p_trucks_bat",
    {"battery_modes": ["light_trucks"], "EV_bat": _subscript_dict["EV_bat"]},
)

_ext_lookup_policy_share_battery.add(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_ev_bat",
    "p_heavy_trucks_bat",
    {"battery_modes": ["heavy_trucks"], "EV_bat": _subscript_dict["EV_bat"]},
)


@component.add(
    name="rail_kms_new",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "initial_rail_kms": 1,
        "vehicles_rail_tkm": 1,
        "historic_rail_pkm_vehicles": 1,
        "vehicles_rail_pkm": 1,
        "historic_rail_tkm_vehicles": 1,
    },
)
def rail_kms_new():
    """
    new kms of rail from 2023
    """
    return if_then_else(
        time() < 2025,
        lambda: 0,
        lambda: float(
            np.maximum(
                0,
                0.5
                * initial_rail_kms()
                * (
                    (
                        sum(
                            vehicles_rail_pkm().rename({"fuels": "fuels!"}),
                            dim=["fuels!"],
                        )
                        + sum(
                            vehicles_rail_tkm().rename({"fuels": "fuels!"}),
                            dim=["fuels!"],
                        )
                    )
                    / (
                        sum(
                            historic_rail_pkm_vehicles(2023).rename(
                                {"fuels": "fuels!"}
                            ),
                            dim=["fuels!"],
                        )
                        + sum(
                            historic_rail_tkm_vehicles(2023).rename(
                                {"fuels": "fuels!"}
                            ),
                            dim=["fuels!"],
                        )
                    )
                    - 2
                ),
            )
        ),
    )


@component.add(
    name="replacement_batteries",
    units="batteries/year",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"discarded_batteries": 1},
)
def replacement_batteries():
    """
    Replacement of electric batteries.due to degradation of existing ones
    """
    return discarded_batteries()


@component.add(
    name="replacement_vehicles_pkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def replacement_vehicles_pkm():
    return xr.DataArray(
        0,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )


@component.add(
    name="replacement_vehicles_tkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def replacement_vehicles_tkm():
    return xr.DataArray(
        0,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )


@component.add(
    name="required_number_standard_batteries",
    units="batteries",
    subscripts=["battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bat_number_ev": 1, "bat_number_hib": 1},
)
def required_number_standard_batteries():
    """
    Required number of electric batteries taking as a stantad a 21,3KWh battery (average size of purely electric vehicle). The batteries of other vehicles are described in terms of this standard one using the batteries ratio coefficient, (relative to the size and amount of minerals). .
    """
    return bat_number_ev() + bat_number_hib()


@component.add(
    name="retirements_vehicles",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"vehicles_mode_and_fuel": 1, "lifetime_vehicles_tkm": 1},
)
def retirements_vehicles():
    return vehicles_mode_and_fuel() / lifetime_vehicles_tkm()


@component.add(
    name="retirements_vehicles_pkm",
    units="vehicles/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"vehicles_mode_fuel_pkm": 1, "lifetime_vehicles_pkm": 1},
)
def retirements_vehicles_pkm():
    return np.maximum(0, vehicles_mode_fuel_pkm() / lifetime_vehicles_pkm())


@component.add(
    name="share_battery_per_mode_and_tech",
    units="Dmnl",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_share_ev_per_battery": 1,
        "policy_share_battery": 1,
    },
)
def share_battery_per_mode_and_tech():
    return if_then_else(
        time() < 2023,
        lambda: historic_share_ev_per_battery(time()),
        lambda: policy_share_battery(time()),
    )


@component.add(
    name="Smoothed_betteries_mode_tech",
    units="vehicles",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_betteries_mode_tech": 1},
    other_deps={
        "_smooth_smoothed_betteries_mode_tech": {
            "initial": {"batteries_per_mode_and_tech": 1},
            "step": {"batteries_per_mode_and_tech": 1},
        }
    },
)
def smoothed_betteries_mode_tech():
    return _smooth_smoothed_betteries_mode_tech()


_smooth_smoothed_betteries_mode_tech = Smooth(
    lambda: batteries_per_mode_and_tech(),
    lambda: xr.DataArray(
        1,
        {
            "battery_modes": _subscript_dict["battery_modes"],
            "EV_bat": _subscript_dict["EV_bat"],
        },
        ["battery_modes", "EV_bat"],
    ),
    lambda: batteries_per_mode_and_tech(),
    lambda: 3,
    "_smooth_smoothed_betteries_mode_tech",
)


@component.add(
    name="Smoothed_Target_Vehicles_pkm",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_target_vehicles_pkm": 1},
    other_deps={
        "_smooth_smoothed_target_vehicles_pkm": {
            "initial": {"vehicles_pkm_mode": 1},
            "step": {"vehicles_pkm_mode": 1},
        }
    },
)
def smoothed_target_vehicles_pkm():
    return _smooth_smoothed_target_vehicles_pkm()


_smooth_smoothed_target_vehicles_pkm = Smooth(
    lambda: vehicles_pkm_mode(),
    lambda: xr.DataArray(
        1,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    ),
    lambda: vehicles_pkm_mode(),
    lambda: 3,
    "_smooth_smoothed_target_vehicles_pkm",
)


@component.add(
    name="Smoothed_Target_Vehicles_tkm",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_target_vehicles_tkm": 1},
    other_deps={
        "_smooth_smoothed_target_vehicles_tkm": {
            "initial": {"vehicles_tkm_mode": 1},
            "step": {"vehicles_tkm_mode": 1},
        }
    },
)
def smoothed_target_vehicles_tkm():
    return _smooth_smoothed_target_vehicles_tkm()


_smooth_smoothed_target_vehicles_tkm = Smooth(
    lambda: vehicles_tkm_mode(),
    lambda: xr.DataArray(
        1,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    ),
    lambda: vehicles_tkm_mode(),
    lambda: 3,
    "_smooth_smoothed_target_vehicles_tkm",
)


@component.add(
    name="vehicles_mode_and_fuel",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_vehicles_mode_and_fuel": 1},
    other_deps={
        "_integ_vehicles_mode_and_fuel": {
            "initial": {"initial_tkm_vehicles": 1},
            "step": {
                "new_vehicles": 1,
                "replacement_vehicles_tkm": 1,
                "retirements_vehicles": 1,
            },
        }
    },
)
def vehicles_mode_and_fuel():
    return _integ_vehicles_mode_and_fuel()


_integ_vehicles_mode_and_fuel = Integ(
    lambda: new_vehicles() + replacement_vehicles_tkm() - retirements_vehicles(),
    lambda: initial_tkm_vehicles(),
    "_integ_vehicles_mode_and_fuel",
)


@component.add(
    name="vehicles_mode_fuel_pkm",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_vehicles_mode_fuel_pkm": 1},
    other_deps={
        "_integ_vehicles_mode_fuel_pkm": {
            "initial": {"initial_pkm_vehicles": 1},
            "step": {
                "new_vehicles_pkm": 1,
                "replacement_vehicles_pkm": 1,
                "retirements_vehicles_pkm": 1,
            },
        }
    },
)
def vehicles_mode_fuel_pkm():
    return _integ_vehicles_mode_fuel_pkm()


_integ_vehicles_mode_fuel_pkm = Integ(
    lambda: new_vehicles_pkm()
    + replacement_vehicles_pkm()
    - retirements_vehicles_pkm(),
    lambda: initial_pkm_vehicles(),
    "_integ_vehicles_mode_fuel_pkm",
)


@component.add(
    name="vehicles_pkm_mode",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vehicles_buses_pkm": 1,
        "vehicles_households": 1,
        "vehicles_rail_pkm": 1,
    },
)
def vehicles_pkm_mode():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_heavy"]] = (
        vehicles_buses_pkm().expand_dims({"Land": ["Road_heavy"]}, 1).values
    )
    value.loc[:, ["Road_light"]] = (
        vehicles_households().expand_dims({"Land": ["Road_light"]}, 1).values
    )
    value.loc[:, ["Rail"]] = (
        vehicles_rail_pkm().expand_dims({"Land": ["Rail"]}, 1).values
    )
    value.loc[:, ["Air"]] = 0
    value.loc[:, ["Maritime"]] = 0
    return value


@component.add(
    name="vehicles_tkm_mode",
    units="vehicles",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vehicles_heavy_trucks": 1,
        "vehicles_light_trucks": 1,
        "vehicles_rail_tkm": 1,
    },
)
def vehicles_tkm_mode():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport_Modes": _subscript_dict["Transport_Modes"],
        },
        ["fuels", "Transport_Modes"],
    )
    value.loc[:, ["Road_heavy"]] = (
        vehicles_heavy_trucks().expand_dims({"Land": ["Road_heavy"]}, 1).values
    )
    value.loc[:, ["Road_light"]] = (
        vehicles_light_trucks().expand_dims({"Land": ["Road_light"]}, 1).values
    )
    value.loc[:, ["Rail"]] = (
        vehicles_rail_tkm().expand_dims({"Land": ["Rail"]}, 1).values
    )
    value.loc[:, ["Air"]] = 0
    value.loc[:, ["Maritime"]] = 0
    return value


@component.add(
    name="vehicles_tkm_mode_delayed",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_vehicles_tkm_mode_delayed": 1},
    other_deps={
        "_delayfixed_vehicles_tkm_mode_delayed": {
            "initial": {"vehicles_tkm_mode": 1},
            "step": {"vehicles_tkm_mode": 1},
        }
    },
)
def vehicles_tkm_mode_delayed():
    return _delayfixed_vehicles_tkm_mode_delayed()


_delayfixed_vehicles_tkm_mode_delayed = DelayFixed(
    lambda: vehicles_tkm_mode(),
    lambda: 1,
    lambda: vehicles_tkm_mode(),
    time_step,
    "_delayfixed_vehicles_tkm_mode_delayed",
)
