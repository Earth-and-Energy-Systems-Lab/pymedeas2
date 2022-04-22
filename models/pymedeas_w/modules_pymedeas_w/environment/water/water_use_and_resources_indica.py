"""
Module water_use_and_resources_indica
Translated using PySD version 3.0.0
"""


@component.add(
    name="AR water", units="km3", comp_type="Constant", comp_subtype="External"
)
def ar_water():
    """
    Accessible runnoff water. Source: UN (2003).
    """
    return _ext_constant_ar_water()


_ext_constant_ar_water = ExtConstant(
    "../parameters.xlsx",
    "World",
    "accessible_runnoff_water",
    {},
    _root,
    {},
    "_ext_constant_ar_water",
)


@component.add(
    name="dam3 per km3", units="km3", comp_type="Constant", comp_subtype="Normal"
)
def dam3_per_km3():
    return 1000000.0


@component.add(
    name="Historic water by type intensities by sector",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_water_by_type_intensities_by_sector():
    return if_then_else(
        time() < 2009,
        lambda: historic_water_use(time())
        .loc[_subscript_dict["sectors"], :]
        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
        / (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "water": _subscript_dict["water"],
                },
                ["sectors", "water"],
            )
            + real_total_output_by_sector()
        ),
        lambda: xr.DataArray(
            0,
            {"sectors": _subscript_dict["sectors"], "water": _subscript_dict["water"]},
            ["sectors", "water"],
        ),
    )


@component.add(
    name="Historic water by type intensities for households",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_water_by_type_intensities_for_households():
    return if_then_else(
        time() < 2009,
        lambda: historic_water_use(time()).loc["Households", :].reset_coords(drop=True)
        / household_demand_total(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@component.add(
    name="Historic water intensities by sector delayed 1yr",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
    name="Historic water intensities for households delayed 1yr",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
    name="Historic water use",
    units="dam3/$",
    subscripts=["SECTORS and HOUSEHOLDS", "water"],
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_water_use(x, final_subs=None):
    """
    Historic water use by type for 35 WIOD sectors and households.
    """
    return _ext_lookup_historic_water_use(x, final_subs)


_ext_lookup_historic_water_use = ExtLookup(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_blue_water",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "water": ["blue water"],
    },
    _root,
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "water": _subscript_dict["water"],
    },
    "_ext_lookup_historic_water_use",
)

_ext_lookup_historic_water_use.add(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_green_water",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "water": ["green water"],
    },
)

_ext_lookup_historic_water_use.add(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_gray_water",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "water": ["gray water"],
    },
)


@component.add(
    name="Initial water intensity by sector",
    units="dam3/Mdollars",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="Initial",
)
def initial_water_intensity_by_sector():
    return _initial_initial_water_intensity_by_sector()


_initial_initial_water_intensity_by_sector = Initial(
    lambda: historic_water_by_type_intensities_by_sector(),
    "_initial_initial_water_intensity_by_sector",
)


@component.add(
    name="Initial water intensity for households",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="Initial",
)
def initial_water_intensity_for_households():
    return _initial_initial_water_intensity_for_households()


_initial_initial_water_intensity_for_households = Initial(
    lambda: historic_water_by_type_intensities_for_households(),
    "_initial_initial_water_intensity_for_households",
)


@component.add(
    name="Mt to dam3", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mt_to_dam3():
    return 1000


@component.add(
    name="Renewable water resources",
    units="km3",
    comp_type="Constant",
    comp_subtype="External",
)
def renewable_water_resources():
    return _ext_constant_renewable_water_resources()


_ext_constant_renewable_water_resources = ExtConstant(
    "../parameters.xlsx",
    "World",
    "renewable_water_resources",
    {},
    _root,
    {},
    "_ext_constant_renewable_water_resources",
)


@component.add(
    name="share blue water use vs AR",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_blue_water_use_vs_ar():
    """
    Share of blue water used vs accessible runoff water.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        ar_water() * dam3_per_km3()
    )


@component.add(
    name="share blue water use vs renewable water resources",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_blue_water_use_vs_renewable_water_resources():
    """
    Share of blue water used vs renewable water resources.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        renewable_water_resources() * dam3_per_km3()
    )


@component.add(
    name="share total water use vs AR",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_total_water_use_vs_ar():
    """
    Share of total water used vs accessible runnoff water.
    """
    return total_water_use() / (ar_water() * dam3_per_km3())


@component.add(
    name="share total water use vs renewable water resources",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_total_water_use_vs_renewable_water_resources():
    """
    Share of total water used vs renewable water resources.
    """
    return total_water_use() / (renewable_water_resources() * dam3_per_km3())


@component.add(
    name='"Total water for O&M required by RES elec dam3"',
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_water_for_om_required_by_res_elec_dam3():
    return total_water_for_om_required_by_res_elec() * mt_to_dam3()


@component.add(
    name="Total water use", units="dam3", comp_type="Auxiliary", comp_subtype="Normal"
)
def total_water_use():
    """
    Total water use (all types aggregated).
    """
    return sum(total_water_use_by_type().rename({"water": "water!"}), dim=["water!"])


@component.add(
    name="Total water use by type",
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="Variation water intensity by sector",
    units="dam3/$1995",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_water_intensity_by_sector():
    """
    Variation of water intensity by type, sector and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: historic_water_by_type_intensities_by_sector()
        - historic_water_intensities_by_sector_delayed_1yr(),
        lambda: xr.DataArray(
            0,
            {"sectors": _subscript_dict["sectors"], "water": _subscript_dict["water"]},
            ["sectors", "water"],
        ),
    )


@component.add(
    name="Variation water intensity households",
    units="dam3/Mdollars",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_water_intensity_households():
    """
    Variation of water intensity for households by type and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: historic_water_by_type_intensities_for_households()
        - historic_water_intensities_for_households_delayed_1yr(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@component.add(
    name="Water intensity by sector",
    units="dam3/$1995",
    subscripts=["sectors", "water"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def water_intensity_by_sector():
    return _integ_water_intensity_by_sector()


_integ_water_intensity_by_sector = Integ(
    lambda: variation_water_intensity_by_sector(),
    lambda: initial_water_intensity_by_sector(),
    "_integ_water_intensity_by_sector",
)


@component.add(
    name="Water intensity for households",
    units="dam3/$1995",
    subscripts=["water"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def water_intensity_for_households():
    return _integ_water_intensity_for_households()


_integ_water_intensity_for_households = Integ(
    lambda: variation_water_intensity_households(),
    lambda: initial_water_intensity_for_households(),
    "_integ_water_intensity_for_households",
)


@component.add(
    name="Water use by households",
    units="dam3",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def water_use_by_households():
    """
    Water use by type by households.
    """
    return water_intensity_for_households() * household_demand_total()


@component.add(
    name="Water use by sector",
    units="dam3",
    subscripts=["sectors", "water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def water_use_by_sector():
    """
    Water use by type by sector.
    """
    return water_intensity_by_sector() * (
        xr.DataArray(
            0,
            {"sectors": _subscript_dict["sectors"], "water": _subscript_dict["water"]},
            ["sectors", "water"],
        )
        + real_total_output_by_sector()
    )
