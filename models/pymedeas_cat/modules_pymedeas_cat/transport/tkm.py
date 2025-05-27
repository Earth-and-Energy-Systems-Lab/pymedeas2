"""
Module transport.tkm
Translated using PySD version 3.14.2
"""

@component.add(
    name="Desired_tkm_by_mode_and_fuel",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm": 1, "tkm_fuel_share": 1},
)
def desired_tkm_by_mode_and_fuel():
    return tkm() * tkm_fuel_share().rename(
        {"Transport_Modes_pkm_Commercial": "Transport_Modes"}
    )


@component.add(
    name="eficiency_liquids_tkm",
    units="EJ/(ton*km)",
    subscripts=["Transport_Modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_eficiency_liquids_tkm"},
)
def eficiency_liquids_tkm():
    """
    Efficiency of liquids for each transport mode
    """
    return _ext_constant_eficiency_liquids_tkm()


_ext_constant_eficiency_liquids_tkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "EJ_tkm_liquids",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_constant_eficiency_liquids_tkm",
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
    "Catalonia",
    "end_historical_data",
    {},
    _root,
    {},
    "_ext_constant_end_historical_data",
)


@component.add(
    name="energy_by_fuel_tkm",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_tkm": 4},
)
def energy_by_fuel_tkm():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["liquids"]] = sum(
        energy_tkm()
        .loc["liq", :]
        .reset_coords(drop=True)
        .rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    ) + sum(
        energy_tkm()
        .loc["hybrid", :]
        .reset_coords(drop=True)
        .rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )
    value.loc[["gases"]] = sum(
        energy_tkm()
        .loc["gas", :]
        .reset_coords(drop=True)
        .rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )
    value.loc[["electricity"]] = sum(
        energy_tkm()
        .loc["elect", :]
        .reset_coords(drop=True)
        .rename({"Transport_Modes": "Transport_Modes!"}),
        dim=["Transport_Modes!"],
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="Energy_intensity_commercial_transport",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_by_fuel_tkm": 1,
        "energy_commercial_by_fuel_pkm": 1,
        "m_to_t": 1,
        "gdp_by_sector": 1,
        "nvs_1_year": 1,
    },
)
def energy_intensity_commercial_transport():
    return (
        (energy_by_fuel_tkm() + energy_commercial_by_fuel_pkm())
        / (float(gdp_by_sector().loc["Transport_storage_and_communication"]) * m_to_t())
    ) * nvs_1_year()


@component.add(
    name="Energy_intensity_commercial_transport_delayed",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_energy_intensity_commercial_transport_delayed": 1},
    other_deps={
        "_delayfixed_energy_intensity_commercial_transport_delayed": {
            "initial": {"energy_intensity_commercial_transport": 1, "time_step": 1},
            "step": {"energy_intensity_commercial_transport": 1},
        }
    },
)
def energy_intensity_commercial_transport_delayed():
    return _delayfixed_energy_intensity_commercial_transport_delayed()


_delayfixed_energy_intensity_commercial_transport_delayed = DelayFixed(
    lambda: energy_intensity_commercial_transport(),
    lambda: time_step(),
    lambda: energy_intensity_commercial_transport(),
    time_step,
    "_delayfixed_energy_intensity_commercial_transport_delayed",
)


@component.add(
    name="energy_tkm",
    units="EJ/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "saving_ratios_vehicles_tkm": 1,
        "real_tkm_by_mode_and_fuel": 1,
        "eficiency_liquids_tkm": 1,
    },
)
def energy_tkm():
    return (
        saving_ratios_vehicles_tkm()
        * real_tkm_by_mode_and_fuel()
        * eficiency_liquids_tkm()
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_air_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_air",
)


@component.add(
    name="fuel_share_inland_tkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_inland_tkm",
        "__lookup__": "_ext_lookup_fuel_share_inland_tkm",
    },
)
def fuel_share_inland_tkm(x, final_subs=None):
    return _ext_lookup_fuel_share_inland_tkm(x, final_subs)


_ext_lookup_fuel_share_inland_tkm = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_inland_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_inland_tkm",
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
    return _ext_lookup_fuel_share_maritime(x, final_subs)


_ext_lookup_fuel_share_maritime = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_maritime_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime",
)


@component.add(
    name="GDP_delayed_Time_Step",
    units="T$",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_gdp_delayed_time_step": 1},
    other_deps={
        "_delayfixed_gdp_delayed_time_step": {
            "initial": {"gdp_cat": 1, "time_step": 1},
            "step": {"gdp_cat": 1},
        }
    },
)
def gdp_delayed_time_step():
    """
    GDP delayed
    """
    return _delayfixed_gdp_delayed_time_step()


_delayfixed_gdp_delayed_time_step = DelayFixed(
    lambda: gdp_cat(),
    lambda: time_step(),
    lambda: gdp_cat(),
    time_step,
    "_delayfixed_gdp_delayed_time_step",
)


@component.add(
    name="GDP_growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_cat": 2, "gdp_delayed_time_step": 1},
)
def gdp_growth():
    """
    GDP growth
    """
    return zidz(gdp_cat() - gdp_delayed_time_step(), gdp_cat())


@component.add(
    name="GDP_trans",
    units="T$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gdp_trans": 1},
    other_deps={
        "_integ_gdp_trans": {
            "initial": {"initial_gdp_transport": 1},
            "step": {"gdp_variation": 1},
        }
    },
)
def gdp_trans():
    return _integ_gdp_trans()


_integ_gdp_trans = Integ(
    lambda: gdp_variation(), lambda: initial_gdp_transport(), "_integ_gdp_trans"
)


@component.add(
    name="GDP_variation",
    units="T$/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_growth": 1, "gdp_trans": 1, "time_step": 1},
)
def gdp_variation():
    return (gdp_growth() * gdp_trans()) / time_step()


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
    "Catalonia",
    "time_index_2015",
    "historic_tkm_GDP",
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
    "Catalonia",
    "time_index_2015",
    "share_transport_mode_hist_tkm",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_hist_transport_share_tkm",
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
    "Catalonia",
    "initial_fuel_share_air_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_tkm",
)


@component.add(
    name="initial_fuel_share_inland_tkm",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_inland_tkm"},
)
def initial_fuel_share_inland_tkm():
    return _ext_constant_initial_fuel_share_inland_tkm()


_ext_constant_initial_fuel_share_inland_tkm = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_inland_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_inland_tkm",
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
    return _ext_constant_initial_fuel_share_maritime_tkm()


_ext_constant_initial_fuel_share_maritime_tkm = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_maritime_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_tkm",
)


@component.add(
    name="Initial_GDP_transport",
    units="T$",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_gdp_transport"},
)
def initial_gdp_transport():
    return _ext_constant_initial_gdp_transport()


_ext_constant_initial_gdp_transport = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "initial_economy_transport_tkm",
    {},
    _root,
    {},
    "_ext_constant_initial_gdp_transport",
)


@component.add(
    name="mode_share_tkm",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_mode_share_tkm",
        "__lookup__": "_ext_lookup_mode_share_tkm",
    },
)
def mode_share_tkm(x, final_subs=None):
    return _ext_lookup_mode_share_tkm(x, final_subs)


_ext_lookup_mode_share_tkm = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "Year_transport_share",
    "tkm_share",
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    _root,
    {"Transport_Modes": _subscript_dict["Transport_Modes"]},
    "_ext_lookup_mode_share_tkm",
)


@component.add(
    name="percentage_variation_EI_commercial_transport",
    units="Dmnl/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_intensity_commercial_transport": 1,
        "energy_intensity_commercial_transport_delayed": 2,
        "time_step": 1,
    },
)
def percentage_variation_ei_commercial_transport():
    return zidz(
        (
            energy_intensity_commercial_transport()
            - energy_intensity_commercial_transport_delayed()
        )
        / time_step(),
        energy_intensity_commercial_transport_delayed(),
    )


@component.add(
    name="Real_tkm_by_mode_and_fuel",
    units="ton*km/year",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_tkm_by_mode_and_fuel": 1,
        "energy_scarcity_shortage_by_fuel": 1,
    },
)
def real_tkm_by_mode_and_fuel():
    return desired_tkm_by_mode_and_fuel() * energy_scarcity_shortage_by_fuel()


@component.add(
    name="saving_ratios_vehicles_tkm",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratios_vehicles_tkm"},
)
def saving_ratios_vehicles_tkm():
    """
    Saving ratio of alternative fuels respect to the liquids
    """
    return _ext_constant_saving_ratios_vehicles_tkm()


_ext_constant_saving_ratios_vehicles_tkm = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "saving_ratios_vehicles_tkm*",
    {
        "fuels": _subscript_dict["fuels"],
        "Transport_Modes": _subscript_dict["Transport_Modes"],
    },
    _root,
    {
        "fuels": _subscript_dict["fuels"],
        "Transport_Modes": _subscript_dict["Transport_Modes"],
    },
    "_ext_constant_saving_ratios_vehicles_tkm",
)


@component.add(
    name="tkm",
    units="tonnes*km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "tkmgdp_slope": 1,
        "gdp_cat": 1,
        "tkm_initial": 1,
        "hist_tkm": 1,
    },
)
def tkm():
    """
    ton-km obtained from GDP growth
    """
    return float(
        np.maximum(
            if_then_else(
                time() > end_historical_data(),
                lambda: tkmgdp_slope() * gdp_cat() + tkm_initial(),
                lambda: hist_tkm(time()),
            ),
            0,
        )
    )


@component.add(
    name="tkm_fuel_share",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes_pkm_Commercial"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tkm_fuel_share_inland": 1,
        "tkm_mode_share": 3,
        "tkm_fuel_share_maritime": 1,
        "tkm_fuel_share_air": 1,
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
            "Transport_Modes_pkm_Commercial": _subscript_dict[
                "Transport_Modes_pkm_Commercial"
            ],
        },
        ["fuels", "Transport_Modes_pkm_Commercial"],
    )
    value.loc[:, ["Inland"]] = (
        (tkm_fuel_share_inland() * float(tkm_mode_share().loc["Inland"]))
        .expand_dims({"Transport_Modes_pkm_Commercial": ["Inland"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (tkm_fuel_share_maritime() * float(tkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport_Modes_pkm_Commercial": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (tkm_fuel_share_air() * float(tkm_mode_share().loc["Air"]))
        .expand_dims({"Transport_Modes_pkm_Commercial": ["Air"]}, 1)
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
    name="tkm_fuel_share_delayed",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_tkm_fuel_share_delayed": 1},
    other_deps={
        "_delayfixed_tkm_fuel_share_delayed": {
            "initial": {"tkm_fuel_share": 1, "time_step": 1},
            "step": {"tkm_fuel_share": 1},
        }
    },
)
def tkm_fuel_share_delayed():
    return _delayfixed_tkm_fuel_share_delayed()


_delayfixed_tkm_fuel_share_delayed = DelayFixed(
    lambda: tkm_fuel_share().rename(
        {"Transport_Modes_pkm_Commercial": "Transport_Modes"}
    ),
    lambda: time_step(),
    lambda: tkm_fuel_share().rename(
        {"Transport_Modes_pkm_Commercial": "Transport_Modes"}
    ),
    time_step,
    "_delayfixed_tkm_fuel_share_delayed",
)


@component.add(
    name="tkm_fuel_share_inland",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_inland_tkm": 3,
        "start_year_policies_transport": 3,
        "fuel_share_inland_tkm": 2,
    },
)
def tkm_fuel_share_inland():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_inland_tkm(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_inland_tkm()
            + (
                (
                    fuel_share_inland_tkm(start_year_policies_transport())
                    - initial_fuel_share_inland_tkm()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_inland_tkm(time()),
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
        "start_year_policies_transport": 3,
        "fuel_share_maritime": 2,
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
    name="tkm_initial",
    units="ton*km/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tkm_initial"},
)
def tkm_initial():
    return _ext_constant_tkm_initial()


_ext_constant_tkm_initial = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "tkm_gdp_2015",
    {},
    _root,
    {},
    "_ext_constant_tkm_initial",
)


@component.add(
    name="tkm_mode_share",
    units="Dmnl",
    subscripts=["Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_historical_data": 5,
        "hist_transport_share_tkm": 3,
        "start_year_policies_transport": 3,
        "mode_share_tkm": 2,
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
                    mode_share_tkm(start_year_policies_transport())
                    - hist_transport_share_tkm(end_historical_data())
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: mode_share_tkm(time()),
        ),
    )


@component.add(
    name='"tkm/gdp_slope"',
    units="ton*km/(T$*year)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tkmgdp_slope"},
)
def tkmgdp_slope():
    return _ext_constant_tkmgdp_slope()


_ext_constant_tkmgdp_slope = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "tkm_gdp_slope",
    {},
    _root,
    {},
    "_ext_constant_tkmgdp_slope",
)


@component.add(
    name="variation",
    units="Dmnl",
    subscripts=["fuels", "Transport_Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm_fuel_share": 1, "tkm_fuel_share_delayed": 1},
)
def variation():
    """
    Percentage of variation of fuel for each transport mode
    """
    return (
        tkm_fuel_share().rename({"Transport_Modes_pkm_Commercial": "Transport_Modes"})
        - tkm_fuel_share_delayed()
    )
