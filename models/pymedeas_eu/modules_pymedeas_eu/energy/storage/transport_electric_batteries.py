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
    name="new_batteries",
    units="batteries/year",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"batteries_per_mode_and_tech": 1, "batteries_evhib": 1, "time_step": 1},
)
def new_batteries():
    """
    New standard electric batteries. The number of batteries converges to the desired number via a logistic funcion. Number 10 is an arbitrary parameter, the bigger the faster the convergence to the desired number of batteries. 5*"batteries EV+hib+2wE"*(1-(MIN(1,"batteries EV+hib+2wE"/required number standard batteries)))
    """
    return (
        np.maximum(0, batteries_per_mode_and_tech() - batteries_evhib()) / time_step()
    )


@component.add(
    name='"new+replaced_batteries_kWh"',
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
    name="share_battery_per_mode_and_tech",
    units="Dmnl",
    subscripts=["battery_modes", "EV_bat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "end_hist_data": 1,
        "historic_share_ev_per_battery": 1,
        "policy_share_battery": 1,
    },
)
def share_battery_per_mode_and_tech():
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_share_ev_per_battery(time()),
        lambda: policy_share_battery(time()),
    )
