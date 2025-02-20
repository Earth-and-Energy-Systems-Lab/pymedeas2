"""
Module transport.pkm
Translated using PySD version 3.14.0
"""

@component.add(
    name="desired pkm by mode and fuel",
    units="person*km/year",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
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
    name="eficiency liquids pkm",
    units="EJ/(person*km)",
    subscripts=[np.str_("Transport Modes pkm")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eficiency_liquids_pkm"},
)
def eficiency_liquids_pkm():
    return _ext_constant_eficiency_liquids_pkm()


_ext_constant_eficiency_liquids_pkm = ExtConstant(
    "../transport.xlsx",
    "Global",
    "EJ_pkm_liquids",
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    _root,
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    "_ext_constant_eficiency_liquids_pkm",
)


@component.add(
    name="EI households transport",
    units="EJ/T$",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary, Constant",
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
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["electricity"]] = (
        float(energy_pkm().loc["elect", "Househ"])
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["gases"]] = (
        float(energy_pkm().loc["gas", "Househ"])
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["liquids"]] = (
        (
            float(energy_pkm().loc["liq", "Househ"])
            + float(energy_pkm().loc["hybrid", "Househ"])
        )
        / (household_demand_total() * m_to_t())
        * nvs_1_year()
    )
    value.loc[["solids"]] = 0
    value.loc[["heat"]] = 0
    return value


@component.add(
    name="energy commercial by fuel pkm",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 4},
)
def energy_commercial_by_fuel_pkm():
    value = xr.DataArray(
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["liquids"]] = sum(
        energy_pkm()
        .loc["liq", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({np.str_("Transport Modes pkm"): "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    ) + sum(
        energy_pkm()
        .loc["hybrid", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({np.str_("Transport Modes pkm"): "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["gases"]] = sum(
        energy_pkm()
        .loc["gas", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({np.str_("Transport Modes pkm"): "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["electricity"]] = sum(
        energy_pkm()
        .loc["elect", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({np.str_("Transport Modes pkm"): "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="energy pkm",
    units="EJ/year",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "saving_ratios_vehicles_pkm": 1,
        "real_pkm_by_mode_and_fuel": 1,
        "eficiency_liquids_pkm": 1,
    },
)
def energy_pkm():
    """
    Variation on the energy due to the changes on fuel and transport mode
    """
    return (
        saving_ratios_vehicles_pkm()
        * real_pkm_by_mode_and_fuel()
        * eficiency_liquids_pkm()
    )


@component.add(
    name="Energy scarcity shortage by fuel",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_scarcity_feedback_shortage_coeff_cat": 4},
)
def energy_scarcity_shortage_by_fuel():
    value = xr.DataArray(
        np.nan, {"fuels": _subscript_dict["fuels"]}, [np.str_("fuels")]
    )
    value.loc[["liq"]] = float(
        energy_scarcity_feedback_shortage_coeff_cat().loc["liquids"]
    )
    value.loc[["gas"]] = float(
        energy_scarcity_feedback_shortage_coeff_cat().loc["gases"]
    )
    value.loc[["elect"]] = float(
        energy_scarcity_feedback_shortage_coeff_cat().loc["electricity"]
    )
    value.loc[["hybrid"]] = float(
        energy_scarcity_feedback_shortage_coeff_cat().loc["liquids"]
    )
    return value


@component.add(
    name="fuel share air pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_air_pkm",
        "__lookup__": "_ext_lookup_fuel_share_air_pkm",
    },
)
def fuel_share_air_pkm(x, final_subs=None):
    return _ext_lookup_fuel_share_air_pkm(x, final_subs)


_ext_lookup_fuel_share_air_pkm = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_air_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_air_pkm",
)


@component.add(
    name="fuel share households pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_households_pkm",
        "__lookup__": "_ext_lookup_fuel_share_households_pkm",
    },
)
def fuel_share_households_pkm(x, final_subs=None):
    return _ext_lookup_fuel_share_households_pkm(x, final_subs)


_ext_lookup_fuel_share_households_pkm = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_households_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_households_pkm",
)


@component.add(
    name="fuel share inland pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_inland_pkm",
        "__lookup__": "_ext_lookup_fuel_share_inland_pkm",
    },
)
def fuel_share_inland_pkm(x, final_subs=None):
    return _ext_lookup_fuel_share_inland_pkm(x, final_subs)


_ext_lookup_fuel_share_inland_pkm = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_inland_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_inland_pkm",
)


@component.add(
    name="fuel share maritime pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
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
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_maritime_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime_pkm",
)


@component.add(
    name="hist pkm",
    units="person*km/(year)",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_pkm",
        "__lookup__": "_ext_lookup_hist_pkm",
    },
)
def hist_pkm(x, final_subs=None):
    return _ext_lookup_hist_pkm(x, final_subs)


_ext_lookup_hist_pkm = ExtLookup(
    "../transport.xlsx",
    "Catalonia",
    "time_index_2015",
    "historic_pkm_GDP",
    {},
    _root,
    {},
    "_ext_lookup_hist_pkm",
)


@component.add(
    name="hist transport share pkm",
    units="Dmnl",
    subscripts=[np.str_("Transport Modes pkm")],
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
    "../transport.xlsx",
    "Catalonia",
    "time_index_2015",
    "share_transport_mode_hist_pkm",
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    _root,
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    "_ext_lookup_hist_transport_share_pkm",
)


@component.add(
    name='"households vehicles/pkm"',
    units="year*vehicles/(person*km)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_households_vehicles": 1, "initial_pkms_households": 1},
)
def households_vehiclespkm():
    """
    vehicles for pkm
    """
    return initial_households_vehicles() / initial_pkms_households()


@component.add(
    name="initial fuel share air pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_air_pkm"},
)
def initial_fuel_share_air_pkm():
    return _ext_constant_initial_fuel_share_air_pkm()


_ext_constant_initial_fuel_share_air_pkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_air_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_pkm",
)


@component.add(
    name="initial fuel share households pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_households_pkm"},
)
def initial_fuel_share_households_pkm():
    return _ext_constant_initial_fuel_share_households_pkm()


_ext_constant_initial_fuel_share_households_pkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_households_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_households_pkm",
)


@component.add(
    name="initial fuel share inland pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_inland_pkm"},
)
def initial_fuel_share_inland_pkm():
    return _ext_constant_initial_fuel_share_inland_pkm()


_ext_constant_initial_fuel_share_inland_pkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_inland_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_inland_pkm",
)


@component.add(
    name="initial fuel share maritime pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_maritime_pkm"},
)
def initial_fuel_share_maritime_pkm():
    return _ext_constant_initial_fuel_share_maritime_pkm()


_ext_constant_initial_fuel_share_maritime_pkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_maritime_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_pkm",
)


@component.add(
    name="Initial households vehicles",
    units="vehicles",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_households_vehicles"},
)
def initial_households_vehicles():
    """
    Initial number of households vehicles
    """
    return _ext_constant_initial_households_vehicles()


_ext_constant_initial_households_vehicles = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_household_vehicles",
    {},
    _root,
    {},
    "_ext_constant_initial_households_vehicles",
)


@component.add(
    name="initial pkms households",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkms_households"},
)
def initial_pkms_households():
    return _ext_constant_initial_pkms_households()


_ext_constant_initial_pkms_households = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_pkm_households",
    {},
    _root,
    {},
    "_ext_constant_initial_pkms_households",
)


@component.add(
    name="mode share pkm",
    units="Dmnl",
    subscripts=[np.str_("Transport Modes pkm")],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_mode_share_pkm",
        "__lookup__": "_ext_lookup_mode_share_pkm",
    },
)
def mode_share_pkm(x, final_subs=None):
    return _ext_lookup_mode_share_pkm(x, final_subs)


_ext_lookup_mode_share_pkm = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "Year_transport_share",
    "pkm_share",
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    _root,
    {"Transport Modes pkm": _subscript_dict["Transport Modes pkm"]},
    "_ext_lookup_mode_share_pkm",
)


@component.add(
    name="pkm",
    units="person*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "pkmgdp_initial": 1,
        "gdp_cat": 1,
        "pkmgdp_slope": 1,
        "hist_pkm": 1,
    },
)
def pkm():
    return if_then_else(
        time() > 2015,
        lambda: (pkmgdp_slope() * time() + pkmgdp_initial()) * gdp_cat(),
        lambda: hist_pkm(time()),
    )


@component.add(
    name="pkm fuel share",
    units="Dmnl",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pkm_fuel_share_inland": 1,
        "pkm_mode_share": 6,
        "pkm_fuel_share_maritime": 1,
        "pkm_fuel_share_air": 1,
        "pkm_fuel_share_households": 1,
    },
)
def pkm_fuel_share():
    value = xr.DataArray(
        np.nan,
        {
            "fuels": _subscript_dict["fuels"],
            "Transport Modes pkm": _subscript_dict["Transport Modes pkm"],
        },
        [np.str_("fuels"), np.str_("Transport Modes pkm")],
    )
    value.loc[:, ["Inland"]] = (
        (
            pkm_fuel_share_inland()
            * float(pkm_mode_share().loc["Inland"])
            * (1 - float(pkm_mode_share().loc["Househ"]))
        )
        .expand_dims({"Transport Modes pkm Commercial": ["Inland"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (pkm_fuel_share_maritime() * float(pkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport Modes pkm Commercial": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (pkm_fuel_share_air() * float(pkm_mode_share().loc["Air"]))
        .expand_dims({"Transport Modes pkm Commercial": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Househ"]] = (
        (
            pkm_fuel_share_households()
            * float(pkm_mode_share().loc["Househ"])
            * float(pkm_mode_share().loc["Inland"])
        )
        .expand_dims({"Transport Modes pkm": ["Househ"]}, 1)
        .values
    )
    return value


@component.add(
    name="pkm fuel share air",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_air_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_air_pkm": 2,
    },
)
def pkm_fuel_share_air():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_air_pkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_air_pkm()
            + (
                (
                    fuel_share_air_pkm(start_year_policies_transport())
                    - initial_fuel_share_air_pkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_air_pkm(time()),
        ),
    )


@component.add(
    name="pkm fuel share households",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_households_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_households_pkm": 2,
    },
)
def pkm_fuel_share_households():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_households_pkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_households_pkm()
            + (
                (
                    fuel_share_households_pkm(start_year_policies_transport())
                    - initial_fuel_share_households_pkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_households_pkm(time()),
        ),
    )


@component.add(
    name="pkm fuel share inland",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_inland_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_inland_pkm": 2,
    },
)
def pkm_fuel_share_inland():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_inland_pkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_inland_pkm()
            + (
                (
                    fuel_share_inland_pkm(start_year_policies_transport())
                    - initial_fuel_share_inland_pkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_inland_pkm(time()),
        ),
    )


@component.add(
    name="pkm fuel share maritime",
    units="Dmnl",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_maritime_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_maritime_pkm": 2,
    },
)
def pkm_fuel_share_maritime():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_maritime_pkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_maritime_pkm()
            + (
                (
                    fuel_share_maritime_pkm(start_year_policies_transport())
                    - initial_fuel_share_maritime_pkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_maritime_pkm(time()),
        ),
    )


@component.add(
    name="pkm mode share",
    units="Dmnl",
    subscripts=[np.str_("Transport Modes pkm")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 5,
        "hist_transport_share_pkm": 3,
        "start_year_policies_transport": 3,
        "mode_share_pkm": 2,
    },
)
def pkm_mode_share():
    return if_then_else(
        time() < end_historical_data(),
        lambda: hist_transport_share_pkm(time()),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: hist_transport_share_pkm(end_historical_data())
            + (
                (
                    mode_share_pkm(start_year_policies_transport())
                    - hist_transport_share_pkm(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: mode_share_pkm(time()),
        ),
    )


@component.add(
    name='"pkm/gdp initial"',
    units="person*km/(year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pkmgdp_initial"},
)
def pkmgdp_initial():
    return _ext_constant_pkmgdp_initial()


_ext_constant_pkmgdp_initial = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "pkm_gdp_2015",
    {},
    _root,
    {},
    "_ext_constant_pkmgdp_initial",
)


@component.add(
    name='"pkm/gdp slope"',
    units="person*km/(year*year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pkmgdp_slope"},
)
def pkmgdp_slope():
    return _ext_constant_pkmgdp_slope()


_ext_constant_pkmgdp_slope = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "pkm_gdp_slope",
    {},
    _root,
    {},
    "_ext_constant_pkmgdp_slope",
)


@component.add(
    name="real pkm by mode and fuel",
    units="person*km/year",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_pkm_by_mode_and_fuel": 1,
        "energy_scarcity_shortage_by_fuel": 1,
    },
)
def real_pkm_by_mode_and_fuel():
    """
    Real pkm variation after the efect of scarcity
    """
    return np.maximum(
        desired_pkm_by_mode_and_fuel() * energy_scarcity_shortage_by_fuel(), 0
    )


@component.add(
    name="real pkm by mode and fuel delayed",
    units="person*km/year",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_pkm_by_mode_and_fuel_delayed": 1},
    other_deps={
        "_delayfixed_real_pkm_by_mode_and_fuel_delayed": {
            "initial": {"real_pkm_by_mode_and_fuel": 1, "time_step": 1},
            "step": {"real_pkm_by_mode_and_fuel": 1},
        }
    },
)
def real_pkm_by_mode_and_fuel_delayed():
    return _delayfixed_real_pkm_by_mode_and_fuel_delayed()


_delayfixed_real_pkm_by_mode_and_fuel_delayed = DelayFixed(
    lambda: real_pkm_by_mode_and_fuel(),
    lambda: time_step(),
    lambda: real_pkm_by_mode_and_fuel(),
    time_step,
    "_delayfixed_real_pkm_by_mode_and_fuel_delayed",
)


@component.add(
    name="saving ratios vehicles pkm",
    units="Dmnl",
    subscripts=[np.str_("fuels"), np.str_("Transport Modes pkm")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratios_vehicles_pkm"},
)
def saving_ratios_vehicles_pkm():
    return _ext_constant_saving_ratios_vehicles_pkm()


_ext_constant_saving_ratios_vehicles_pkm = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratios_vehicles_pkm*",
    {
        "fuels": _subscript_dict["fuels"],
        "Transport Modes pkm": _subscript_dict["Transport Modes pkm"],
    },
    _root,
    {
        "fuels": _subscript_dict["fuels"],
        "Transport Modes pkm": _subscript_dict["Transport Modes pkm"],
    },
    "_ext_constant_saving_ratios_vehicles_pkm",
)


@component.add(
    name="start year policies transport",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_policies_transport"},
)
def start_year_policies_transport():
    return _ext_constant_start_year_policies_transport()


_ext_constant_start_year_policies_transport = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_policies_transport",
    {},
    _root,
    {},
    "_ext_constant_start_year_policies_transport",
)


@component.add(
    name="vehicles households",
    units="vehicles",
    subscripts=[np.str_("fuels")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_pkm_by_mode_and_fuel": 1, "households_vehiclespkm": 1},
)
def vehicles_households():
    """
    Total vehicles
    """
    return (
        real_pkm_by_mode_and_fuel().loc[:, "Househ"].reset_coords(drop=True)
        * households_vehiclespkm()
    )
