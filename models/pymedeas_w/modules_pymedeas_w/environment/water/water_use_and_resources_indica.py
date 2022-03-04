"""
Module water_use_and_resources_indica
Translated using PySD version 2.2.1
"""


def ar_water():
    """
    Real Name: AR water
    Original Eqn:
    Units: km3
    Limits: (None, None)
    Type: Constant
    Subs: []

    Accessible runnoff water. Source: UN (2003).
    """
    return _ext_constant_ar_water()


_ext_constant_ar_water = ExtConstant(
    "../parameters.xlsx",
    "World",
    "accessible_runnoff_water",
    {},
    _root,
    "_ext_constant_ar_water",
)


def dam3_per_km3():
    """
    Real Name: dam3 per km3
    Original Eqn:
    Units: km3
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 1000000.0


@subs(["sectors", "water"], _subscript_dict)
def historic_water_by_type_intensities_by_sector():
    """
    Real Name: Historic water by type intensities by sector
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'water']


    """
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


@subs(["water"], _subscript_dict)
def historic_water_by_type_intensities_for_households():
    """
    Real Name: Historic water by type intensities for households
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']


    """
    return if_then_else(
        time() < 2009,
        lambda: historic_water_use(time()).loc["Households", :].reset_coords(drop=True)
        / household_demand_total(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@subs(["sectors", "water"], _subscript_dict)
def historic_water_intensities_by_sector_delayed_1yr():
    """
    Real Name: Historic water intensities by sector delayed 1yr
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors', 'water']


    """
    return _delayfixed_historic_water_intensities_by_sector_delayed_1yr()


_delayfixed_historic_water_intensities_by_sector_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_by_sector(),
    lambda: 1,
    lambda: initial_water_intensity_by_sector(),
    time_step,
    "_delayfixed_historic_water_intensities_by_sector_delayed_1yr",
)


@subs(["water"], _subscript_dict)
def historic_water_intensities_for_households_delayed_1yr():
    """
    Real Name: Historic water intensities for households delayed 1yr
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['water']


    """
    return _delayfixed_historic_water_intensities_for_households_delayed_1yr()


_delayfixed_historic_water_intensities_for_households_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_for_households(),
    lambda: 1,
    lambda: initial_water_intensity_for_households(),
    time_step,
    "_delayfixed_historic_water_intensities_for_households_delayed_1yr",
)


@subs(["SECTORS and HOUSEHOLDS", "water"], _subscript_dict)
def historic_water_use(x):
    """
    Real Name: Historic water use
    Original Eqn:
    Units: dam3/$
    Limits: (None, None)
    Type: Lookup
    Subs: ['SECTORS and HOUSEHOLDS', 'water']

    Historic water use by type for 35 WIOD sectors and households.
    """
    return _ext_lookup_historic_water_use(x)


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


@subs(["sectors", "water"], _subscript_dict)
def initial_water_intensity_by_sector():
    """
    Real Name: Initial water intensity by sector
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors', 'water']


    """
    return _initial_initial_water_intensity_by_sector()


_initial_initial_water_intensity_by_sector = Initial(
    lambda: historic_water_by_type_intensities_by_sector(),
    "_initial_initial_water_intensity_by_sector",
)


@subs(["water"], _subscript_dict)
def initial_water_intensity_for_households():
    """
    Real Name: Initial water intensity for households
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['water']


    """
    return _initial_initial_water_intensity_for_households()


_initial_initial_water_intensity_for_households = Initial(
    lambda: historic_water_by_type_intensities_for_households(),
    "_initial_initial_water_intensity_for_households",
)


def mt_to_dam3():
    """
    Real Name: Mt to dam3
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 1000


def renewable_water_resources():
    """
    Real Name: Renewable water resources
    Original Eqn:
    Units: km3
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_renewable_water_resources()


_ext_constant_renewable_water_resources = ExtConstant(
    "../parameters.xlsx",
    "World",
    "renewable_water_resources",
    {},
    _root,
    "_ext_constant_renewable_water_resources",
)


def share_blue_water_use_vs_ar():
    """
    Real Name: share blue water use vs AR
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of blue water used vs accessible runoff water.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        ar_water() * dam3_per_km3()
    )


def share_blue_water_use_vs_renewable_water_resources():
    """
    Real Name: share blue water use vs renewable water resources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of blue water used vs renewable water resources.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        renewable_water_resources() * dam3_per_km3()
    )


def share_total_water_use_vs_ar():
    """
    Real Name: share total water use vs AR
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of total water used vs accessible runnoff water.
    """
    return total_water_use() / (ar_water() * dam3_per_km3())


def share_total_water_use_vs_renewable_water_resources():
    """
    Real Name: share total water use vs renewable water resources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of total water used vs renewable water resources.
    """
    return total_water_use() / (renewable_water_resources() * dam3_per_km3())


@subs(["water"], _subscript_dict)
def total_water_for_om_required_by_res_elec_dam3():
    """
    Real Name: "Total water for O&M required by RES elec dam3"
    Original Eqn:
    Units: dam3
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']


    """
    return total_water_for_om_required_by_res_elec() * mt_to_dam3()


def total_water_use():
    """
    Real Name: Total water use
    Original Eqn:
    Units: dam3
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total water use (all types aggregated).
    """
    return sum(total_water_use_by_type().rename({"water": "water!"}), dim=["water!"])


@subs(["water"], _subscript_dict)
def total_water_use_by_type():
    """
    Real Name: Total water use by type
    Original Eqn:
    Units: dam3
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']

    Total water consumption by type (green, blue, grey).
    """
    return (
        sum(water_use_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"])
        + water_use_by_households()
        + total_water_for_om_required_by_res_elec_dam3()
    )


@subs(["sectors", "water"], _subscript_dict)
def variation_water_intensity_by_sector():
    """
    Real Name: Variation water intensity by sector
    Original Eqn:
    Units: dam3/$1995
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'water']

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


@subs(["water"], _subscript_dict)
def variation_water_intensity_households():
    """
    Real Name: Variation water intensity households
    Original Eqn:
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']

    Variation of water intensity for households by type and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: historic_water_by_type_intensities_for_households()
        - historic_water_intensities_for_households_delayed_1yr(),
        lambda: xr.DataArray(0, {"water": _subscript_dict["water"]}, ["water"]),
    )


@subs(["sectors", "water"], _subscript_dict)
def water_intensity_by_sector():
    """
    Real Name: Water intensity by sector
    Original Eqn:
    Units: dam3/$1995
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors', 'water']


    """
    return _integ_water_intensity_by_sector()


_integ_water_intensity_by_sector = Integ(
    lambda: variation_water_intensity_by_sector(),
    lambda: initial_water_intensity_by_sector(),
    "_integ_water_intensity_by_sector",
)


@subs(["water"], _subscript_dict)
def water_intensity_for_households():
    """
    Real Name: Water intensity for households
    Original Eqn:
    Units: dam3/$1995
    Limits: (None, None)
    Type: Stateful
    Subs: ['water']


    """
    return _integ_water_intensity_for_households()


_integ_water_intensity_for_households = Integ(
    lambda: variation_water_intensity_households(),
    lambda: initial_water_intensity_for_households(),
    "_integ_water_intensity_for_households",
)


@subs(["water"], _subscript_dict)
def water_use_by_households():
    """
    Real Name: Water use by households
    Original Eqn:
    Units: dam3
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']

    Water use by type by households.
    """
    return water_intensity_for_households() * household_demand_total()


@subs(["sectors", "water"], _subscript_dict)
def water_use_by_sector():
    """
    Real Name: Water use by sector
    Original Eqn:
    Units: dam3
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'water']

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
