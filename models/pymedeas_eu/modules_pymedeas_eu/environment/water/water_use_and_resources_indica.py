"""
Module environment.water.water_use_and_resources_indica
Translated using PySD version 3.14.2
"""

@component.add(
    name="AR_water",
    units="km3",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ar_water"},
)
def ar_water():
    """
    Accessible runnoff water. Source: UN (2003).
    """
    return _ext_constant_ar_water()


_ext_constant_ar_water = ExtConstant(
    r"../parameters.xlsx",
    "Europe",
    "accessible_runnoff_water",
    {},
    _root,
    {},
    "_ext_constant_ar_water",
)


@component.add(
    name="dam3_per_km3", units="dam3/km3", comp_type="Constant", comp_subtype="Normal"
)
def dam3_per_km3():
    return 1000000.0


@component.add(
    name="Historic_water_by_type_intensities_by_sector",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "real_total_output_by_sector_eu": 1,
        "historic_water_use": 1,
    },
)
def historic_water_by_type_intensities_by_sector():
    return if_then_else(
        time() < 2019,
        lambda: historic_water_use(time())
        .loc[_subscript_dict["sectors"], :]
        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
        / real_total_output_by_sector_eu(),
        lambda: xr.DataArray(
            0,
            {"sectors": _subscript_dict["sectors"], "water": _subscript_dict["water"]},
            ["sectors", "water"],
        ),
    )


@component.add(
    name="Historic_water_by_type_intensities_for_households",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_water_use": 1, "household_demand_total": 1},
)
def historic_water_by_type_intensities_for_households():
    return if_then_else(
        time() < 2009,
        lambda: historic_water_use(time()).loc["Households", :].reset_coords(drop=True)
        / household_demand_total(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@component.add(
    name="Historic_water_intensities_by_sector_delayed_1yr",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_historic_water_intensities_by_sector_delayed_1yr": 1},
    other_deps={
        "_delayfixed_historic_water_intensities_by_sector_delayed_1yr": {
            "initial": {"initial_water_intensity_by_sector": 1},
            "step": {"historic_water_by_type_intensities_by_sector": 1},
        }
    },
)
def historic_water_intensities_by_sector_delayed_1yr():
    return _delayfixed_historic_water_intensities_by_sector_delayed_1yr()


_delayfixed_historic_water_intensities_by_sector_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_by_sector(),
    lambda: 1,
    lambda: initial_water_intensity_by_sector(),
    time_step,
    "_delayfixed_historic_water_intensities_by_sector_delayed_1yr",
)


@component.add(
    name="Historic_water_intensities_for_households_delayed_1yr",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_historic_water_intensities_for_households_delayed_1yr": 1},
    other_deps={
        "_delayfixed_historic_water_intensities_for_households_delayed_1yr": {
            "initial": {"initial_water_intensity_for_households": 1},
            "step": {"historic_water_by_type_intensities_for_households": 1},
        }
    },
)
def historic_water_intensities_for_households_delayed_1yr():
    return _delayfixed_historic_water_intensities_for_households_delayed_1yr()


_delayfixed_historic_water_intensities_for_households_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_for_households(),
    lambda: 1,
    lambda: initial_water_intensity_for_households(),
    time_step,
    "_delayfixed_historic_water_intensities_for_households_delayed_1yr",
)


@component.add(
    name="Historic_water_use",
    units="dam3",
    subscripts=["SECTORS_and_HOUSEHOLDS", "water"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_water_use",
        "__lookup__": "_ext_lookup_historic_water_use",
    },
)
def historic_water_use(x, final_subs=None):
    """
    Historic water use by type for 35 WIOD sectors and households.
    """
    return _ext_lookup_historic_water_use(x, final_subs)


_ext_lookup_historic_water_use = ExtLookup(
    r"../water.xlsx",
    "Europe",
    "year",
    "historic_water_use_blue_water",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "water": ["blue_water"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "water": _subscript_dict["water"],
    },
    "_ext_lookup_historic_water_use",
)

_ext_lookup_historic_water_use.add(
    r"../water.xlsx",
    "Europe",
    "year",
    "historic_water_use_green_water",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "water": ["green_water"],
    },
)

_ext_lookup_historic_water_use.add(
    r"../water.xlsx",
    "Europe",
    "year",
    "historic_water_use_gray_water",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "water": ["gray_water"],
    },
)


@component.add(
    name="Initial_water_intensity_by_sector",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_water_intensity_by_sector": 1},
    other_deps={
        "_initial_initial_water_intensity_by_sector": {
            "initial": {"historic_water_by_type_intensities_by_sector": 1},
            "step": {},
        }
    },
)
def initial_water_intensity_by_sector():
    return _initial_initial_water_intensity_by_sector()


_initial_initial_water_intensity_by_sector = Initial(
    lambda: historic_water_by_type_intensities_by_sector(),
    "_initial_initial_water_intensity_by_sector",
)


@component.add(
    name="Initial_water_intensity_for_households",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_water_intensity_for_households": 1},
    other_deps={
        "_initial_initial_water_intensity_for_households": {
            "initial": {"historic_water_by_type_intensities_for_households": 1},
            "step": {},
        }
    },
)
def initial_water_intensity_for_households():
    return _initial_initial_water_intensity_for_households()


_initial_initial_water_intensity_for_households = Initial(
    lambda: historic_water_by_type_intensities_for_households(),
    "_initial_initial_water_intensity_for_households",
)


@component.add(
    name="Mt_to_dam3", units="dam3/Mt", comp_type="Constant", comp_subtype="Normal"
)
def mt_to_dam3():
    return 1000


@component.add(
    name="Percent_share_blue_water_use_vs_AR",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_blue_water_use_vs_ar": 1},
)
def percent_share_blue_water_use_vs_ar():
    """
    Percent of the share of blue water used vs accessible runoff water.
    """
    return share_blue_water_use_vs_ar() * 100


@component.add(
    name="Renewable_water_resources",
    units="km3",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_renewable_water_resources"},
)
def renewable_water_resources():
    return _ext_constant_renewable_water_resources()


_ext_constant_renewable_water_resources = ExtConstant(
    r"../parameters.xlsx",
    "Europe",
    "renewable_water_resources",
    {},
    _root,
    {},
    "_ext_constant_renewable_water_resources",
)


@component.add(
    name="share_blue_water_use_vs_AR",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use_by_type": 1, "ar_water": 1, "dam3_per_km3": 1},
)
def share_blue_water_use_vs_ar():
    """
    Share of blue water used vs accessible runoff water.
    """
    return float(total_water_use_by_type().loc["blue_water"]) / (
        ar_water() * dam3_per_km3()
    )


@component.add(
    name="share_blue_water_use_vs_renewable_water_resources",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_water_use_by_type": 1,
        "renewable_water_resources": 1,
        "dam3_per_km3": 1,
    },
)
def share_blue_water_use_vs_renewable_water_resources():
    """
    Share of blue water used vs renewable water resources.
    """
    return float(total_water_use_by_type().loc["blue_water"]) / (
        renewable_water_resources() * dam3_per_km3()
    )


@component.add(
    name="share_total_water_use_vs_AR",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use": 1, "ar_water": 1, "dam3_per_km3": 1},
)
def share_total_water_use_vs_ar():
    """
    Share of total water used vs accessible runnoff water.
    """
    return total_water_use() / (ar_water() * dam3_per_km3())


@component.add(
    name="share_total_water_use_vs_renewable_water_resources",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_water_use": 1,
        "renewable_water_resources": 1,
        "dam3_per_km3": 1,
    },
)
def share_total_water_use_vs_renewable_water_resources():
    """
    Share of total water used vs renewable water resources.
    """
    return total_water_use() / (renewable_water_resources() * dam3_per_km3())


@component.add(
    name='"Total_water_for_O&M_required_by_RES_elec_dam3"',
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_for_om_required_by_res_elec": 1, "mt_to_dam3": 1},
)
def total_water_for_om_required_by_res_elec_dam3():
    return total_water_for_om_required_by_res_elec() * mt_to_dam3()


@component.add(
    name="Total_water_use",
    units="dam3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use_by_type": 1},
)
def total_water_use():
    """
    Total water use (all types aggregated).
    """
    return sum(total_water_use_by_type().rename({"water": "water!"}), dim=["water!"])


@component.add(
    name="Total_water_use_by_type",
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "water_use_by_sector": 1,
        "water_use_by_households": 1,
        "total_water_for_om_required_by_res_elec_dam3": 1,
    },
)
def total_water_use_by_type():
    """
    Total water consumption by type (green, blue, grey).
    """
    return (
        sum(water_use_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"])
        + water_use_by_households()
        + total_water_for_om_required_by_res_elec_dam3()
    )


@component.add(
    name="Variation_water_intensity_by_sector",
    units="dam3/(Mdollars*year)",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_water_intensities_by_sector_delayed_1yr": 1,
        "historic_water_by_type_intensities_by_sector": 1,
        "nvs_1_year": 1,
    },
)
def variation_water_intensity_by_sector():
    """
    Variation of water intensity by type, sector and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: (
            historic_water_by_type_intensities_by_sector()
            - historic_water_intensities_by_sector_delayed_1yr()
        )
        / nvs_1_year(),
        lambda: xr.DataArray(
            0,
            {"sectors": _subscript_dict["sectors"], "water": _subscript_dict["water"]},
            ["sectors", "water"],
        ),
    )


@component.add(
    name="Variation_water_intensity_households",
    units="dam3/(Mdollars*year)",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_water_intensities_for_households_delayed_1yr": 1,
        "historic_water_by_type_intensities_for_households": 1,
        "nvs_1_year": 1,
    },
)
def variation_water_intensity_households():
    """
    Variation of water intensity for households by type and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: (
            historic_water_by_type_intensities_for_households()
            - historic_water_intensities_for_households_delayed_1yr()
        )
        / nvs_1_year(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@component.add(
    name="Water_intensity_by_sector",
    units="dam3/M$",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_water_intensity_by_sector": 1},
    other_deps={
        "_integ_water_intensity_by_sector": {
            "initial": {"initial_water_intensity_by_sector": 1},
            "step": {"variation_water_intensity_by_sector": 1},
        }
    },
)
def water_intensity_by_sector():
    return _integ_water_intensity_by_sector()


_integ_water_intensity_by_sector = Integ(
    lambda: variation_water_intensity_by_sector(),
    lambda: initial_water_intensity_by_sector(),
    "_integ_water_intensity_by_sector",
)


@component.add(
    name="Water_intensity_for_households",
    units="dam3/M$",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_water_intensity_for_households": 1},
    other_deps={
        "_integ_water_intensity_for_households": {
            "initial": {"initial_water_intensity_for_households": 1},
            "step": {"variation_water_intensity_households": 1},
        }
    },
)
def water_intensity_for_households():
    return _integ_water_intensity_for_households()


_integ_water_intensity_for_households = Integ(
    lambda: variation_water_intensity_households(),
    lambda: initial_water_intensity_for_households(),
    "_integ_water_intensity_for_households",
)


@component.add(
    name="Water_use_by_households",
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"water_intensity_for_households": 1, "household_demand_total": 1},
)
def water_use_by_households():
    """
    Water use by type by households.
    """
    return water_intensity_for_households() * household_demand_total()


@component.add(
    name="Water_use_by_sector",
    units="dam3",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"water_intensity_by_sector": 1, "real_total_output_by_sector_eu": 1},
)
def water_use_by_sector():
    """
    Water use by type by sector.
    """
    return water_intensity_by_sector() * real_total_output_by_sector_eu()
