"""
Module transport.tkm
Translated using PySD version 3.10.0
"""


@component.add(
    name="Desired tkm by mode and fuel",
    units="tkm",
    subscripts=["fuels", "Transport Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm": 1, "tkm_fuel_share": 1},
)
def desired_tkm_by_mode_and_fuel():
    return tkm() * tkm_fuel_share().rename(
        {"Transport Modes pkm Commercial": "Transport Modes"}
    )


@component.add(
    name="eficiency liquids tkm",
    units="EJ/tkm",
    subscripts=["Transport Modes"],
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
    "../transport.xlsx",
    "Global",
    "EJ_tkm_liquids",
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    _root,
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    "_ext_constant_eficiency_liquids_tkm",
)


@component.add(
    name="end historical data",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_end_historical_data"},
)
def end_historical_data():
    return _ext_constant_end_historical_data()


_ext_constant_end_historical_data = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "end_historical_data",
    {},
    _root,
    {},
    "_ext_constant_end_historical_data",
)


@component.add(
    name="energy by fuel tkm",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"energy_tkm": 4},
)
def energy_by_fuel_tkm():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["liquids"]] = sum(
        energy_tkm()
        .loc["liq", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes": "Transport Modes!"}),
        dim=["Transport Modes!"],
    ) + sum(
        energy_tkm()
        .loc["hybrid", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes": "Transport Modes!"}),
        dim=["Transport Modes!"],
    )
    value.loc[["gases"]] = sum(
        energy_tkm()
        .loc["gas", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes": "Transport Modes!"}),
        dim=["Transport Modes!"],
    )
    value.loc[["electricity"]] = sum(
        energy_tkm()
        .loc["elect", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes": "Transport Modes!"}),
        dim=["Transport Modes!"],
    )
    value.loc[["heat"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="Energy intensity commercial transport",
    units="EJ/T$",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_by_fuel_tkm": 1,
        "energy_commercial_by_fuel_pkm": 1,
        "gdp_trans": 1,
        "time_step": 1,
    },
)
def energy_intensity_commercial_transport():
    return (energy_by_fuel_tkm() + energy_commercial_by_fuel_pkm()) / (
        gdp_trans() * time_step()
    )


@component.add(
    name="Energy intensity commercial transport delayed",
    units="EJ/T$",
    subscripts=["final sources"],
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
    name="energy tkm",
    units="EJ",
    subscripts=["fuels", "Transport Modes"],
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
    name="fuel share air",
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
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_air_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_air",
)


@component.add(
    name="fuel share inland",
    subscripts=["fuels"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_fuel_share_inland",
        "__lookup__": "_ext_lookup_fuel_share_inland",
    },
)
def fuel_share_inland(x, final_subs=None):
    return _ext_lookup_fuel_share_inland(x, final_subs)


_ext_lookup_fuel_share_inland = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_inland_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_inland",
)


@component.add(
    name="fuel share maritime",
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
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_transport_fuel_share_tkm",
    "fuel_share_maritime_tkm",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_lookup_fuel_share_maritime",
)


@component.add(
    name="GDP delayed Time Step",
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
    name="GDP growth",
    units="Dmln",
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
    name="GDP trans",
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
    name="GDP variation",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_growth": 1, "gdp_trans": 1, "time_step": 1},
)
def gdp_variation():
    return (gdp_growth() * gdp_trans()) / time_step()


@component.add(
    name="hist tkm gdp",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_hist_tkm_gdp",
        "__lookup__": "_ext_lookup_hist_tkm_gdp",
    },
)
def hist_tkm_gdp(x, final_subs=None):
    return _ext_lookup_hist_tkm_gdp(x, final_subs)


_ext_lookup_hist_tkm_gdp = ExtLookup(
    "../transport.xlsx",
    "Catalonia",
    "time_index_2015",
    "historic_tkm_GDP",
    {},
    _root,
    {},
    "_ext_lookup_hist_tkm_gdp",
)


@component.add(
    name="hist transport share tkm",
    subscripts=["Transport Modes"],
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
    "../transport.xlsx",
    "Catalonia",
    "time_index_2015",
    "share_transport_mode_hist_tkm",
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    _root,
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    "_ext_lookup_hist_transport_share_tkm",
)


@component.add(
    name="initial fuel share air tkm",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_air_tkm"},
)
def initial_fuel_share_air_tkm():
    return _ext_constant_initial_fuel_share_air_tkm()


_ext_constant_initial_fuel_share_air_tkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_air_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_air_tkm",
)


@component.add(
    name="initial fuel share inland",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_inland"},
)
def initial_fuel_share_inland():
    return _ext_constant_initial_fuel_share_inland()


_ext_constant_initial_fuel_share_inland = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_inland_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_inland",
)


@component.add(
    name="initial fuel share maritime tkm",
    subscripts=["fuels"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_fuel_share_maritime_tkm"},
)
def initial_fuel_share_maritime_tkm():
    return _ext_constant_initial_fuel_share_maritime_tkm()


_ext_constant_initial_fuel_share_maritime_tkm = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_fuel_share_maritime_tkm*",
    {"fuels": _subscript_dict["fuels"]},
    _root,
    {"fuels": _subscript_dict["fuels"]},
    "_ext_constant_initial_fuel_share_maritime_tkm",
)


@component.add(
    name="Initial GDP transport",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_gdp_transport"},
)
def initial_gdp_transport():
    return _ext_constant_initial_gdp_transport()


_ext_constant_initial_gdp_transport = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "initial_economy_transport_tkm",
    {},
    _root,
    {},
    "_ext_constant_initial_gdp_transport",
)


@component.add(
    name="mode share tkm",
    subscripts=["Transport Modes"],
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
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "Year_transport_share",
    "tkm_share",
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    _root,
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    "_ext_lookup_mode_share_tkm",
)


@component.add(
    name="percentage variation EI commercial transport",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_intensity_commercial_transport": 1,
        "energy_intensity_commercial_transport_delayed": 2,
    },
)
def percentage_variation_ei_commercial_transport():
    return zidz(
        energy_intensity_commercial_transport()
        - energy_intensity_commercial_transport_delayed(),
        energy_intensity_commercial_transport_delayed(),
    )


@component.add(
    name="Real tkm by mode and fuel",
    units="tkm",
    subscripts=["fuels", "Transport Modes"],
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
    name="saving ratios vehicles tkm",
    units="Dmnl",
    subscripts=["fuels", "Transport Modes"],
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
    "../transport.xlsx",
    "Global",
    "saving_ratios_vehicles_tkm*",
    {
        "fuels": _subscript_dict["fuels"],
        "Transport Modes": _subscript_dict["Transport Modes"],
    },
    _root,
    {
        "fuels": _subscript_dict["fuels"],
        "Transport Modes": _subscript_dict["Transport Modes"],
    },
    "_ext_constant_saving_ratios_vehicles_tkm",
)


@component.add(
    name="tkm",
    units="tonnes*km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_historical_data": 1,
        "gdp_cat": 1,
        "tkmgdp_slope": 1,
        "tkmgdp_initial": 1,
        "hist_tkm_gdp": 1,
        "time_step": 1,
    },
)
def tkm():
    """
    ton-km obtained from GDP growth
    """
    return np.maximum(
        if_then_else(
            time() > end_historical_data(),
            lambda: tkmgdp_slope() * gdp_cat() + tkmgdp_initial(),
            lambda: hist_tkm_gdp(time()),
        )
        * time_step(),
        0,
    )


@component.add(
    name="tkm fuel share",
    subscripts=["fuels", "Transport Modes pkm Commercial"],
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
            "Transport Modes pkm Commercial": _subscript_dict[
                "Transport Modes pkm Commercial"
            ],
        },
        ["fuels", "Transport Modes pkm Commercial"],
    )
    value.loc[:, ["Inland"]] = (
        (tkm_fuel_share_inland() * float(tkm_mode_share().loc["Inland"]))
        .expand_dims({"Transport Modes pkm Commercial": ["Inland"]}, 1)
        .values
    )
    value.loc[:, ["Maritime"]] = (
        (tkm_fuel_share_maritime() * float(tkm_mode_share().loc["Maritime"]))
        .expand_dims({"Transport Modes pkm Commercial": ["Maritime"]}, 1)
        .values
    )
    value.loc[:, ["Air"]] = (
        (tkm_fuel_share_air() * float(tkm_mode_share().loc["Air"]))
        .expand_dims({"Transport Modes pkm Commercial": ["Air"]}, 1)
        .values
    )
    return value


@component.add(
    name="tkm fuel share air",
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
    name="tkm fuel share delayed",
    subscripts=["fuels", "Transport Modes"],
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
        {"Transport Modes pkm Commercial": "Transport Modes"}
    ),
    lambda: time_step(),
    lambda: tkm_fuel_share().rename(
        {"Transport Modes pkm Commercial": "Transport Modes"}
    ),
    time_step,
    "_delayfixed_tkm_fuel_share_delayed",
)


@component.add(
    name="tkm fuel share inland",
    units="Dmnl",
    subscripts=["fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "end_historical_data": 3,
        "initial_fuel_share_inland": 3,
        "fuel_share_inland": 2,
        "start_year_policies_transport": 3,
    },
)
def tkm_fuel_share_inland():
    return if_then_else(
        time() < end_historical_data(),
        lambda: initial_fuel_share_inland(),
        lambda: if_then_else(
            time() < start_year_policies_transport(),
            lambda: initial_fuel_share_inland()
            + (
                (
                    fuel_share_inland(start_year_policies_transport())
                    - initial_fuel_share_inland()
                )
                / (start_year_policies_transport() - end_historical_data())
            )
            * (time() - end_historical_data()),
            lambda: fuel_share_inland(time()),
        ),
    )


@component.add(
    name="tkm fuel share maritime",
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
    name="tkm mode share",
    subscripts=["Transport Modes"],
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
    name='"tkm/gdp initial"',
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tkmgdp_initial"},
)
def tkmgdp_initial():
    return _ext_constant_tkmgdp_initial()


_ext_constant_tkmgdp_initial = ExtConstant(
    "../transport.xlsx",
    "Catalonia",
    "tkm_gdp_2015",
    {},
    _root,
    {},
    "_ext_constant_tkmgdp_initial",
)


@component.add(
    name='"tkm/gdp slope"',
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tkmgdp_slope"},
)
def tkmgdp_slope():
    return _ext_constant_tkmgdp_slope()


_ext_constant_tkmgdp_slope = ExtConstant(
    "../transport.xlsx",
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
    subscripts=["fuels", "Transport Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tkm_fuel_share": 1, "tkm_fuel_share_delayed": 1},
)
def variation():
    """
    Percentage of variation of fuel for each transport mode
    """
    return (
        tkm_fuel_share().rename({"Transport Modes pkm Commercial": "Transport Modes"})
        - tkm_fuel_share_delayed()
    )
