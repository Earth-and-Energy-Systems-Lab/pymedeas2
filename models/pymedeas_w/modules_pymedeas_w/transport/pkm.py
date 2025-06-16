"""
Module transport.pkm
Translated using PySD version 3.14.2
"""

@component.add(
    name='"commercial_pkm_vehicles/pkm"',
    units="year*vehicles/(person*km)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_commercial_vehicles": 1, "initial_pkm_commercial": 1},
)
def commercial_pkm_vehiclespkm():
    return initial_commercial_vehicles() / initial_pkm_commercial()


@component.add(
    name="desired_pkm_by_mode_and_fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport_Modes_pkm"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pkm": 1, "pkm_fuel_share": 1},
)
def desired_pkm_by_mode_and_fuel():
    return pkm() * pkm_fuel_share()


@component.add(
    name="eficiency_liquids_pkm",
    units="EJ/(person*km)",
    subscripts=["Transport_Modes_pkm"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eficiency_liquids_pkm"},
)
def eficiency_liquids_pkm():
    return _ext_constant_eficiency_liquids_pkm()


_ext_constant_eficiency_liquids_pkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "EJ_pkm_liquids",
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
    _root,
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
    "_ext_constant_eficiency_liquids_pkm",
)


@component.add(
    name="EI_households_transport",
    units="EJ/T$",
    subscripts=["final_sources"],
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
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
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
    name="energy_commercial_by_fuel_pkm",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 4},
)
def energy_commercial_by_fuel_pkm():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["liquids"]] = sum(
        energy_pkm()
        .loc["liq", _subscript_dict["Transport_Modes_pkm_Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport_Modes_pkm": "Transport_Modes_pkm_Commercial!"}),
        dim=["Transport_Modes_pkm_Commercial!"],
    ) + sum(
        energy_pkm()
        .loc["hybrid", _subscript_dict["Transport_Modes_pkm_Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport_Modes_pkm": "Transport_Modes_pkm_Commercial!"}),
        dim=["Transport_Modes_pkm_Commercial!"],
    )
    value.loc[["gases"]] = sum(
        energy_pkm()
        .loc["gas", _subscript_dict["Transport_Modes_pkm_Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport_Modes_pkm": "Transport_Modes_pkm_Commercial!"}),
        dim=["Transport_Modes_pkm_Commercial!"],
    )
    value.loc[["electricity"]] = sum(
        energy_pkm()
        .loc["elect", _subscript_dict["Transport_Modes_pkm_Commercial"]]
        .reset_coords(drop=True)
        .rename({"Transport_Modes_pkm": "Transport_Modes_pkm_Commercial!"}),
        dim=["Transport_Modes_pkm_Commercial!"],
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="energy_pkm",
    units="EJ/year",
    subscripts=["fuels", "Transport_Modes_pkm"],
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
    Energy demand of the passenger transport at each time step
    """
    return (
        saving_ratios_vehicles_pkm()
        * real_pkm_by_mode_and_fuel()
        * eficiency_liquids_pkm()
    )


@component.add(
    name="Energy_scarcity_shortage_by_fuel",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_scarcity_feedback_shortage_coeff": 4},
)
def energy_scarcity_shortage_by_fuel():
    value = xr.DataArray(np.nan, {"fuels": _subscript_dict["fuels"]}, ["fuels"])
    value.loc[["liq"]] = float(energy_scarcity_feedback_shortage_coeff().loc["liquids"])
    value.loc[["gas"]] = float(energy_scarcity_feedback_shortage_coeff().loc["gases"])
    value.loc[["elect"]] = float(
        energy_scarcity_feedback_shortage_coeff().loc["electricity"]
    )
    value.loc[["hybrid"]] = float(
        energy_scarcity_feedback_shortage_coeff().loc["liquids"]
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
    return _ext_lookup_fuel_share_air_pkm(x, final_subs)


_ext_lookup_fuel_share_air_pkm = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
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
    return _ext_lookup_fuel_share_households_pkm(x, final_subs)


_ext_lookup_fuel_share_households_pkm = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_households_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_households_pkm",
)


@component.add(
    name="fuel_share_inland_pkm",
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
    return _ext_lookup_fuel_share_inland_pkm(x, final_subs)


_ext_lookup_fuel_share_inland_pkm = ExtLookup(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_inland_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_inland_pkm",
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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "year_transport_fuel_share_pkm",
    "fuel_share_maritime_pkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime_pkm",
)


@component.add(
    name="hist_pkm_gdp",
    units="person*km/(year*T$)",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_pkm_gdp",
        "__lookup__": "_ext_lookup_hist_pkm_gdp",
    },
)
def hist_pkm_gdp(x, final_subs=None):
    return _ext_lookup_hist_pkm_gdp(x, final_subs)


_ext_lookup_hist_pkm_gdp = ExtLookup(
    r"../transport.xlsx",
    "World",
    "time_index_2015",
    "historic_pkm_GDP",
    {},
    _root,
    {},
    "_ext_lookup_hist_pkm_gdp",
)


@component.add(
    name="hist_transport_share_pkm",
    units="Dmnl",
    subscripts=["Transport_Modes_pkm"],
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
    "World",
    "time_index_2015",
    "share_transport_mode_hist_pkm",
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
    _root,
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
    "_ext_lookup_hist_transport_share_pkm",
)


@component.add(
    name='"households_vehicles/pkm"',
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
    name="initial_commercial_vehicles",
    units="vehicles",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_commercial_vehicles"},
)
def initial_commercial_vehicles():
    return _ext_constant_initial_commercial_vehicles()


_ext_constant_initial_commercial_vehicles = ExtConstant(
    r"../transport.xlsx",
    "World",
    "initial_pkm_vehicles_com",
    {},
    _root,
    {},
    "_ext_constant_initial_commercial_vehicles",
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
    return _ext_constant_initial_fuel_share_air_pkm()


_ext_constant_initial_fuel_share_air_pkm = ExtConstant(
    r"../transport.xlsx",
    "World",
    "initial_fuel_share_air_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_pkm",
)


@component.add(
    name="initial_fuel_share_households_pkm",
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
    "World",
    "initial_fuel_share_households_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_households_pkm",
)


@component.add(
    name="initial_fuel_share_inland_pkm",
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
    "World",
    "initial_fuel_share_inland_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_inland_pkm",
)


@component.add(
    name="initial_fuel_share_maritime_pkm",
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
    "World",
    "initial_fuel_share_maritime_pkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_pkm",
)


@component.add(
    name="initial_households_energy_intensity",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_households_energy_intensity"},
)
def initial_households_energy_intensity():
    return _ext_constant_initial_households_energy_intensity()


_ext_constant_initial_households_energy_intensity = ExtConstant(
    r"../transport.xlsx",
    "World",
    "initial_ei_households_transport*",
    {"final_sources": _subscript_dict["final_sources"]},
    _root,
    {"final_sources": _subscript_dict["final_sources"]},
    "_ext_constant_initial_households_energy_intensity",
)


@component.add(
    name="initial_households_vehicles",
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
    "World",
    "initial_household_vehicles",
    {},
    _root,
    {},
    "_ext_constant_initial_households_vehicles",
)


@component.add(
    name="initial_pkm_commercial",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkm_commercial"},
)
def initial_pkm_commercial():
    return _ext_constant_initial_pkm_commercial()


_ext_constant_initial_pkm_commercial = ExtConstant(
    r"../transport.xlsx",
    "World",
    "initial_pkm__commercial_inland",
    {},
    _root,
    {},
    "_ext_constant_initial_pkm_commercial",
)


@component.add(
    name="initial_pkm_households",
    units="person*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkm_households"},
)
def initial_pkm_households():
    """
    Initial number of pkms done by households vehicles at 2015
    """
    return _ext_constant_initial_pkm_households()


_ext_constant_initial_pkm_households = ExtConstant(
    r"../transport.xlsx",
    "World",
    "initial_pkm",
    {},
    _root,
    {},
    "_ext_constant_initial_pkm_households",
)


@component.add(
    name='"initial_pkm/gdp"',
    units="person*km/(year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_pkmgdp"},
)
def initial_pkmgdp():
    return _ext_constant_initial_pkmgdp()


_ext_constant_initial_pkmgdp = ExtConstant(
    r"../transport.xlsx",
    "World",
    "pkm_gdp_2015",
    {},
    _root,
    {},
    "_ext_constant_initial_pkmgdp",
)


@component.add(
    name="mode_share_pkm",
    units="Dmnl",
    subscripts=["Transport_Modes_pkm"],
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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "Year_transport_share",
    "pkm_share",
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
    _root,
    {"Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"]},
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
        "pkmgdp_slope": 1,
        "initial_pkmgdp": 1,
        "hist_pkm_gdp": 1,
        "gdp": 1,
    },
)
def pkm():
    """
    passengers·km variations related to GDP
    """
    return (
        if_then_else(
            time() > end_historical_data(),
            lambda: initial_pkmgdp() + pkmgdp_slope() * time(),
            lambda: hist_pkm_gdp(time()),
        )
        * gdp()
    )


@component.add(
    name="pkm_fuel_share",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes_pkm"],
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
            "Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"],
        },
        ["fuels", "Transport_Modes_pkm"],
    )
    value.loc[:, ["Inland"]] = (
        (
            pkm_fuel_share_inland()
            * float(pkm_mode_share().loc["Inland"])
            * (1 - float(pkm_mode_share().loc["Househ"]))
        )
        .expand_dims({"Transport_Modes_pkm": ["Inland"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (pkm_fuel_share_maritime() * float(pkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport_Modes_pkm": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (pkm_fuel_share_air() * float(pkm_mode_share().loc["Air"]))
        .expand_dims({"Transport_Modes_pkm": ["Air"]}, 1)
        .values
    )
    value.loc[:, ["Househ"]] = (
        (
            pkm_fuel_share_households()
            * float(pkm_mode_share().loc["Househ"])
            * float(pkm_mode_share().loc["Inland"])
        )
        .expand_dims({"Transport_Modes_pkm": ["Househ"]}, 1)
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
        "end_historical_data": 4,
        "initial_fuel_share_air_pkm": 3,
        "fuel_share_1995": 2,
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
    name="pkm_fuel_share_households",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "initial_fuel_share_households_pkm": 3,
        "fuel_share_1995": 2,
        "start_year_policies_transport": 3,
        "fuel_share_households_pkm": 2,
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
    name="pkm_fuel_share_inland",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "initial_fuel_share_inland_pkm": 3,
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
            / (end_historical_data() - 1995)
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
    name="pkm_fuel_share_maritime",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 4,
        "initial_fuel_share_maritime_pkm": 3,
        "fuel_share_1995": 2,
        "start_year_policies_transport": 3,
        "fuel_share_maritime_pkm": 2,
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
    name="pkm_mode_share",
    units="Dmnl",
    subscripts=["Transport_Modes_pkm"],
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
    name='"pkm/gdp_slope"',
    units="person*km/(year*year*T$)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pkmgdp_slope"},
)
def pkmgdp_slope():
    return _ext_constant_pkmgdp_slope()


_ext_constant_pkmgdp_slope = ExtConstant(
    r"../transport.xlsx",
    "World",
    "pkm_gdp_slope",
    {},
    _root,
    {},
    "_ext_constant_pkmgdp_slope",
)


@component.add(
    name="real_pkm_by_mode_and_fuel",
    units="person*km/year",
    subscripts=["fuels", "Transport_Modes_pkm"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_pkm_by_mode_and_fuel": 1,
        "energy_scarcity_shortage_by_fuel": 1,
    },
)
def real_pkm_by_mode_and_fuel():
    """
    Real pkm variation after the effect of scarcity
    """
    return desired_pkm_by_mode_and_fuel() * energy_scarcity_shortage_by_fuel()


@component.add(
    name="saving_ratios_vehicles_pkm",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes_pkm"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratios_vehicles_pkm"},
)
def saving_ratios_vehicles_pkm():
    return _ext_constant_saving_ratios_vehicles_pkm()


_ext_constant_saving_ratios_vehicles_pkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "saving_ratios_vehicles_pkm*",
    {
        "fuels": _subscript_dict["fuels"],
        "Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"],
    },
    _root,
    {
        "fuels": _subscript_dict["fuels"],
        "Transport_Modes_pkm": _subscript_dict["Transport_Modes_pkm"],
    },
    "_ext_constant_saving_ratios_vehicles_pkm",
)


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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_policies_transport",
    {},
    _root,
    {},
    "_ext_constant_start_year_policies_transport",
)


@component.add(
    name="vehicles_commercial_pkm",
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
    name="vehicles_Households",
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
