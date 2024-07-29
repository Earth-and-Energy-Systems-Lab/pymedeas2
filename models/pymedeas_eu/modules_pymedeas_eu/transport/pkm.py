"""
Module transport.pkm
Translated using PySD version 3.14.1
"""

@component.add(
    name='"commercial pkm vehicles/pkm"',
    units="year*vehicles/(person*km)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_commercial_vehicles": 1, "initial_pkm_commercial": 1},
)
def commercial_pkm_vehiclespkm():
    return initial_commercial_vehicles() / initial_pkm_commercial()


@component.add(
    name="desired pkm by mode and fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport Modes pkm"],
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
    subscripts=["Transport Modes pkm"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eficiency_liquids_pkm"},
)
def eficiency_liquids_pkm():
    """
    Efficiency of different transport modes for liquids fuels
    """
    return _ext_constant_eficiency_liquids_pkm()


_ext_constant_eficiency_liquids_pkm = ExtConstant(
    r"../transport.xlsx",
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
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_pkm": 4,
        "m_to_t": 3,
        "household_demand_total": 3,
        "nvs_1_year": 3,
    },
)
def ei_households_transport():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
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
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="energy commercial by fuel pkm",
    units="EJ/year",
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 4},
)
def energy_commercial_by_fuel_pkm():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["liquids"]] = sum(
        energy_pkm()
        .loc["liq", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    ) + sum(
        energy_pkm()
        .loc["hybrid", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["gases"]] = sum(
        energy_pkm()
        .loc["gas", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["electricity"]] = sum(
        energy_pkm()
        .loc["elect", _subscript_dict["Transport Modes pkm Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm Commercial!"}),
        dim=["Transport Modes pkm Commercial!"],
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="energy pkm",
    units="EJ/year",
    subscripts=["fuels", "Transport Modes pkm"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "saving_ratios_vehicles_pkm": 1,
        "real_pkm_by_mode_and_fuel": 1,
        "eficiency_liquids_pkm": 1,
    },
)
def energy_pkm():
    return (
        saving_ratios_vehicles_pkm()
        * real_pkm_by_mode_and_fuel()
        * eficiency_liquids_pkm()
    )


@component.add(
    name="Energy scarcity shortage by fuel",
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
    name="fuel share 1995",
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
    name="fuel share air pkm",
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
    name="fuel share households pkm",
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
    name="fuel share inland pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_inland_pkm",
        "__lookup__": "_ext_lookup_fuel_share_inland_pkm",
    },
)
def fuel_share_inland_pkm(x, final_subs=None):
    """
    Fuel share of inland passenger transport every 5 years
    """
    return _ext_lookup_fuel_share_inland_pkm(x, final_subs)


_ext_lookup_fuel_share_inland_pkm = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
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
    name="hist pkm gdp",
    units="person*km/(year*T$)",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_pkm_gdp",
        "__lookup__": "_ext_lookup_hist_pkm_gdp",
    },
)
def hist_pkm_gdp(x, final_subs=None):
    """
    Historic values of pkm/GDP
    """
    return _ext_lookup_hist_pkm_gdp(x, final_subs)


_ext_lookup_hist_pkm_gdp = ExtLookup(
    r"../transport.xlsx",
    "Europe",
    "time_index_2015",
    "historic_pkm_GDP",
    {},
    _root,
    {},
    "_ext_lookup_hist_pkm_gdp",
)


@component.add(
    name="hist transport share pkm",
    units="Dmnl",
    subscripts=["Transport Modes pkm"],
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
    depends_on={"initial_households_vehicles": 1, "initial_pkm_households": 1},
)
def households_vehiclespkm():
    """
    Number of vehicles/pkm
    """
    return initial_households_vehicles() / initial_pkm_households()


@component.add(
    name="initial commercial vehicles",
    units="vehicles",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_commercial_vehicles"},
)
def initial_commercial_vehicles():
    return _ext_constant_initial_commercial_vehicles()


_ext_constant_initial_commercial_vehicles = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_pkm_vehicles_com",
    {},
    _root,
    {},
    "_ext_constant_initial_commercial_vehicles",
)


@component.add(
    name="initial fuel share air pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_air_pkm"},
)
def initial_fuel_share_air_pkm():
    return _ext_constant_initial_fuel_share_air_pkm()


_ext_constant_initial_fuel_share_air_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_air_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_pkm",
)


@component.add(
    name="initial fuel share households pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_households_pkm"},
)
def initial_fuel_share_households_pkm():
    return _ext_constant_initial_fuel_share_households_pkm()


_ext_constant_initial_fuel_share_households_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_households_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_households_pkm",
)


@component.add(
    name="initial fuel share inland pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_inland_pkm"},
)
def initial_fuel_share_inland_pkm():
    return _ext_constant_initial_fuel_share_inland_pkm()


_ext_constant_initial_fuel_share_inland_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_inland_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_inland_pkm",
)


@component.add(
    name="initial fuel share maritime pkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_maritime_pkm"},
)
def initial_fuel_share_maritime_pkm():
    return _ext_constant_initial_fuel_share_maritime_pkm()


_ext_constant_initial_fuel_share_maritime_pkm = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_fuel_share_maritime_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_pkm",
)


@component.add(
    name="initial households vehicles",
    units="vehicles",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_households_vehicles"},
)
def initial_households_vehicles():
    """
    Initial number of households vehicles 2015
    """
    return _ext_constant_initial_households_vehicles()


_ext_constant_initial_households_vehicles = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_household_vehicles",
    {},
    _root,
    {},
    "_ext_constant_initial_households_vehicles",
)


@component.add(
    name="initial pkm commercial",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkm_commercial"},
)
def initial_pkm_commercial():
    return _ext_constant_initial_pkm_commercial()


_ext_constant_initial_pkm_commercial = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_pkm__commercial_inland",
    {},
    _root,
    {},
    "_ext_constant_initial_pkm_commercial",
)


@component.add(
    name="initial pkm households",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkm_households"},
)
def initial_pkm_households():
    """
    Initial number of pkms done by households vehicles
    """
    return _ext_constant_initial_pkm_households()


_ext_constant_initial_pkm_households = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "initial_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_pkm_households",
)


@component.add(
    name='"initial pkm/gdp"',
    units="person*km/(year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkmgdp"},
)
def initial_pkmgdp():
    return _ext_constant_initial_pkmgdp()


_ext_constant_initial_pkmgdp = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "pkm_gdp_2015",
    {},
    _root,
    {},
    "_ext_constant_initial_pkmgdp",
)


@component.add(
    name="mode share pkm",
    units="Dmnl",
    subscripts=["Transport Modes pkm"],
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
    r"../../scenarios/scen_eu.xlsx",
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
        "end_historical_data": 1,
        "initial_pkmgdp": 1,
        "gdp_eu": 2,
        "pkmgdp_slope": 1,
        "hist_pkm_gdp": 1,
    },
)
def pkm():
    """
    passengers·km variations related to GDP. Amount of pkm at each time step
    """
    return if_then_else(
        time() > end_historical_data(),
        lambda: (initial_pkmgdp() + pkmgdp_slope() * time()) * gdp_eu(),
        lambda: hist_pkm_gdp(time()) * gdp_eu(),
    )


@component.add(
    name="pkm fuel share",
    units="Dmnl",
    subscripts=["fuels", "Transport Modes pkm"],
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
        ["fuels", "Transport Modes pkm"],
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
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "fuel_share_1995": 2,
        "initial_fuel_share_air_pkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_air_pkm": 2,
    },
)
def pkm_fuel_share_air():
    return if_then_else(
        time() < end_historical_data(),
        lambda: fuel_share_1995()
        + (
            (initial_fuel_share_air_pkm() - fuel_share_1995())
            / (end_historical_data() - 1995)
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
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_air_pkm(time()),
        ),
    )


@component.add(
    name="pkm fuel share households",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "fuel_share_1995": 2,
        "initial_fuel_share_households_pkm": 3,
        "fuel_share_households_pkm": 2,
        "start_year_policies_transport": 3,
    },
)
def pkm_fuel_share_households():
    return if_then_else(
        time() < end_historical_data(),
        lambda: fuel_share_1995()
        + (
            (initial_fuel_share_households_pkm() - fuel_share_1995())
            / (end_historical_data() - 1995)
        )
        * (time() - 1995),
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
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 3,
        "initial_fuel_share_inland_pkm": 3,
        "end_hist_data": 1,
        "fuel_share_1995": 2,
        "start_year_policies_transport": 3,
        "fuel_share_inland_pkm": 2,
    },
)
def pkm_fuel_share_inland():
    return if_then_else(
        time() < end_historical_data(),
        lambda: fuel_share_1995()
        + (
            (initial_fuel_share_inland_pkm() - fuel_share_1995())
            / (end_hist_data() - 1995)
        )
        * (time() - 1995),
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
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "initial_fuel_share_maritime_pkm": 3,
        "fuel_share_1995": 2,
        "fuel_share_maritime_pkm": 2,
        "start_year_policies_transport": 3,
    },
)
def pkm_fuel_share_maritime():
    return if_then_else(
        time() < end_historical_data(),
        lambda: fuel_share_1995()
        + (
            (initial_fuel_share_maritime_pkm() - fuel_share_1995())
            / (end_historical_data() - 1995)
        )
        * (time() - 1995),
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
    subscripts=["Transport Modes pkm"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 5,
        "hist_transport_share_pkm": 3,
        "mode_share_pkm": 2,
        "start_year_policies_transport": 3,
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
    name='"pkm/gdp slope"',
    units="person*km/(year*year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pkmgdp_slope"},
)
def pkmgdp_slope():
    return _ext_constant_pkmgdp_slope()


_ext_constant_pkmgdp_slope = ExtConstant(
    r"../transport.xlsx",
    "Europe",
    "pkm_gdp_slope",
    {},
    _root,
    {},
    "_ext_constant_pkmgdp_slope",
)


@component.add(
    name="real pkm by mode and fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport Modes pkm"],
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
    name="saving ratios vehicles pkm",
    units="Dmnl",
    subscripts=["fuels", "Transport Modes pkm"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratios_vehicles_pkm"},
)
def saving_ratios_vehicles_pkm():
    """
    Saving ratio of alternative fuels respect to liquids
    """
    return _ext_constant_saving_ratios_vehicles_pkm()


_ext_constant_saving_ratios_vehicles_pkm = ExtConstant(
    r"../transport.xlsx",
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
    name="vehicles commercial pkm",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_pkm_by_mode_and_fuel": 1, "commercial_pkm_vehiclespkm": 1},
)
def vehicles_commercial_pkm():
    return (
        real_pkm_by_mode_and_fuel().loc[:, "Inland"].reset_coords(drop=True)
        * commercial_pkm_vehiclespkm()
    )


@component.add(
    name="vehicles households",
    units="vehicles",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_pkm_by_mode_and_fuel": 1, "households_vehiclespkm": 1},
)
def vehicles_households():
    return (
        real_pkm_by_mode_and_fuel().loc[:, "Househ"].reset_coords(drop=True)
        * households_vehiclespkm()
    )
