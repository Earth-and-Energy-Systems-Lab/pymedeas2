"""
Module water_use__resources
Translated using PySD version 2.2.0
"""


def ar_water():
    """
    Real Name: AR water
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'accessible_runnoff_water')
    Units: km3
    Limits: (None, None)
    Type: constant
    Subs: None

    Accessible runnoff water. Source: UN (2003).
    """
    return _ext_constant_ar_water()


def dam3_per_km3():
    """
    Real Name: dam3 per km3
    Original Eqn: 1e+06
    Units: km3
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1e06


@subs(["sectors", "water"], _subscript_dict)
def historic_water_by_type_intensities_by_sector():
    """
    Real Name: Historic water by type intensities by sector
    Original Eqn: IF THEN ELSE( Time<2009, Historic water use[sectors,water](Time)/Real total output by sector[ sectors], 0)
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']


    """
    return if_then_else(
        time() < 2009,
        lambda: rearrange(
            historic_water_use(time()), ["sectors", "water"], _subscript_dict
        )
        / real_total_output_by_sector(),
        lambda: 0,
    )


@subs(["water"], _subscript_dict)
def historic_water_by_type_intensities_for_households():
    """
    Real Name: Historic water by type intensities for households
    Original Eqn: IF THEN ELSE( Time<2009, Historic water use[H,water](Time)/Household demand total, 0)
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['water']


    """
    return if_then_else(
        time() < 2009,
        lambda: rearrange(
            historic_water_use(time()).loc["H", :].reset_coords(drop=True),
            ["water"],
            _subscript_dict,
        )
        / household_demand_total(),
        lambda: 0,
    )


@subs(["sectors", "water"], _subscript_dict)
def historic_water_intensities_by_sector_delayed_1yr():
    """
    Real Name: Historic water intensities by sector delayed 1yr
    Original Eqn: DELAY FIXED ( Historic water by type intensities by sector[sectors,water], 1, Initial water intensity by sector[sectors,water])
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']


    """
    return _delayfixed_historic_water_intensities_by_sector_delayed_1yr()


@subs(["water"], _subscript_dict)
def historic_water_intensities_for_households_delayed_1yr():
    """
    Real Name: Historic water intensities for households delayed 1yr
    Original Eqn: DELAY FIXED ( Historic water by type intensities for households[water], 1, Initial water intensity for households[water])
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['water']


    """
    return _delayfixed_historic_water_intensities_for_households_delayed_1yr()


def historic_water_use(x):
    """
    Real Name: Historic water use
    Original Eqn:
      GET DIRECT LOOKUPS('../water.xlsx', 'World', 'year', 'historic_water_use_blue_water')
      GET DIRECT LOOKUPS('../water.xlsx', 'World', 'year', 'historic_water_use_green_water')
      GET DIRECT LOOKUPS('../water.xlsx', 'World', 'year', 'historic_water_use_gray_water')
    Units: dam3/$
    Limits: (None, None)
    Type: lookup
    Subs: ['SECTORS H', 'water']

    Historic water use by type for 35 WIOD sectors and households.
    """
    return _ext_lookup_historic_water_use(x)


@subs(["sectors", "water"], _subscript_dict)
def initial_water_intensity_by_sector():
    """
    Real Name: Initial water intensity by sector
    Original Eqn: INITIAL(Historic water by type intensities by sector[sectors,water])
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']


    """
    return _initial_initial_water_intensity_by_sector()


@subs(["water"], _subscript_dict)
def initial_water_intensity_for_households():
    """
    Real Name: Initial water intensity for households
    Original Eqn: INITIAL(Historic water by type intensities for households[water])
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['water']


    """
    return _initial_initial_water_intensity_for_households()


def mt_to_dam3():
    """
    Real Name: Mt to dam3
    Original Eqn: 1000
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1000


def renewable_water_resources():
    """
    Real Name: Renewable water resources
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'renewable_water_resources')
    Units: km3
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_renewable_water_resources()


def share_blue_water_use_vs_ar():
    """
    Real Name: share blue water use vs AR
    Original Eqn: Total water use by type[blue water]/(AR water*dam3 per km3)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of blue water used vs accessible runoff water.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        ar_water() * dam3_per_km3()
    )


def share_blue_water_use_vs_renewable_water_resources():
    """
    Real Name: share blue water use vs renewable water resources
    Original Eqn: Total water use by type[blue water]/(Renewable water resources*dam3 per km3)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of blue water used vs renewable water resources.
    """
    return float(total_water_use_by_type().loc["blue water"]) / (
        renewable_water_resources() * dam3_per_km3()
    )


def share_total_water_use_vs_ar():
    """
    Real Name: share total water use vs AR
    Original Eqn: Total water use/(AR water*dam3 per km3)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total water used vs accessible runnoff water.
    """
    return total_water_use() / (ar_water() * dam3_per_km3())


def share_total_water_use_vs_renewable_water_resources():
    """
    Real Name: share total water use vs renewable water resources
    Original Eqn: Total water use/(Renewable water resources*dam3 per km3)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total water used vs renewable water resources.
    """
    return total_water_use() / (renewable_water_resources() * dam3_per_km3())


@subs(["water"], _subscript_dict)
def total_water_for_om_required_by_res_elec_dam3():
    """
    Real Name: "Total water for O&M required by RES elec dam3"
    Original Eqn: "Total water for O&M required by RES elec"[water]*Mt to dam3
    Units: dam3
    Limits: (None, None)
    Type: component
    Subs: ['water']


    """
    return total_water_for_om_required_by_res_elec() * mt_to_dam3()


def total_water_use():
    """
    Real Name: Total water use
    Original Eqn: SUM(Total water use by type[water!])
    Units: dam3
    Limits: (None, None)
    Type: component
    Subs: None

    Total water use (all types aggregated).
    """
    return sum(total_water_use_by_type(), dim=("water",))


@subs(["water"], _subscript_dict)
def total_water_use_by_type():
    """
    Real Name: Total water use by type
    Original Eqn: SUM(Water use by sector[sectors!,water])+Water use by households[ water]+"Total water for O&M required by RES elec dam3"[water]
    Units: dam3
    Limits: (None, None)
    Type: component
    Subs: ['water']

    Total water consumption by type (green, blue, grey).
    """
    return (
        sum(water_use_by_sector(), dim=("sectors",))
        + water_use_by_households()
        + total_water_for_om_required_by_res_elec_dam3()
    )


@subs(["sectors", "water"], _subscript_dict)
def variation_water_intensity_by_sector():
    """
    Real Name: Variation water intensity by sector
    Original Eqn: IF THEN ELSE(Time<2008, Historic water by type intensities by sector[sectors,water]-Historic water intensities by sector delayed 1yr[sectors,water], 0)
    Units: dam3/$1995
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']

    Variation of water intensity by type,  sector and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: historic_water_by_type_intensities_by_sector()
        - historic_water_intensities_by_sector_delayed_1yr(),
        lambda: 0,
    )


@subs(["water"], _subscript_dict)
def variation_water_intensity_households():
    """
    Real Name: Variation water intensity households
    Original Eqn: IF THEN ELSE(Time<2008, Historic water by type intensities for households[water]-Historic water intensities for households delayed 1yr [water], 0)
    Units: dam3/Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['water']

    Variation of water intensity for households by type and year.
    """
    return if_then_else(
        time() < 2008,
        lambda: historic_water_by_type_intensities_for_households()
        - historic_water_intensities_for_households_delayed_1yr(),
        lambda: 0,
    )


@subs(["sectors", "water"], _subscript_dict)
def water_intensity_by_sector():
    """
    Real Name: Water intensity by sector
    Original Eqn: INTEG ( Variation water intensity by sector[sectors,water], Initial water intensity by sector[sectors,water])
    Units: dam3/$1995
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']


    """
    return _integ_water_intensity_by_sector()


@subs(["water"], _subscript_dict)
def water_intensity_for_households():
    """
    Real Name: Water intensity for households
    Original Eqn: INTEG ( Variation water intensity households[water], Initial water intensity for households[water])
    Units: dam3/$1995
    Limits: (None, None)
    Type: component
    Subs: ['water']


    """
    return _integ_water_intensity_for_households()


@subs(["water"], _subscript_dict)
def water_use_by_households():
    """
    Real Name: Water use by households
    Original Eqn: Water intensity for households[water]*Household demand total
    Units: dam3
    Limits: (None, None)
    Type: component
    Subs: ['water']

    Water use by type by households.
    """
    return water_intensity_for_households() * household_demand_total()


@subs(["sectors", "water"], _subscript_dict)
def water_use_by_sector():
    """
    Real Name: Water use by sector
    Original Eqn: Water intensity by sector[sectors,water]*Real total output by sector[ sectors]
    Units: dam3
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'water']

    Water use by type by sector.
    """
    return water_intensity_by_sector() * real_total_output_by_sector()


_ext_constant_ar_water = ExtConstant(
    "../parameters.xlsx",
    "World",
    "accessible_runnoff_water",
    {},
    _root,
    "_ext_constant_ar_water",
)


_delayfixed_historic_water_intensities_by_sector_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_by_sector(),
    lambda: 1,
    lambda: initial_water_intensity_by_sector(),
    time_step,
    "_delayfixed_historic_water_intensities_by_sector_delayed_1yr",
)


_delayfixed_historic_water_intensities_for_households_delayed_1yr = DelayFixed(
    lambda: historic_water_by_type_intensities_for_households(),
    lambda: 1,
    lambda: initial_water_intensity_for_households(),
    time_step,
    "_delayfixed_historic_water_intensities_for_households_delayed_1yr",
)


_ext_lookup_historic_water_use = ExtLookup(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_blue_water",
    {"SECTORS H": _subscript_dict["SECTORS H"], "water": ["blue water"]},
    _root,
    "_ext_lookup_historic_water_use",
)


_ext_lookup_historic_water_use.add(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_green_water",
    {"SECTORS H": _subscript_dict["SECTORS H"], "water": ["green water"]},
)


_ext_lookup_historic_water_use.add(
    "../water.xlsx",
    "World",
    "year",
    "historic_water_use_gray_water",
    {"SECTORS H": _subscript_dict["SECTORS H"], "water": ["gray water"]},
)


_initial_initial_water_intensity_by_sector = Initial(
    lambda: historic_water_by_type_intensities_by_sector(),
    "_initial_initial_water_intensity_by_sector",
)


_initial_initial_water_intensity_for_households = Initial(
    lambda: historic_water_by_type_intensities_for_households(),
    "_initial_initial_water_intensity_for_households",
)


_ext_constant_renewable_water_resources = ExtConstant(
    "../parameters.xlsx",
    "World",
    "renewable_water_resources",
    {},
    _root,
    "_ext_constant_renewable_water_resources",
)


@subs(["sectors", "water"], _subscript_dict)
def _integ_init_water_intensity_by_sector():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for water_intensity_by_sector
    Limits: None
    Type: setup
    Subs: ['sectors', 'water']

    Provides initial conditions for water_intensity_by_sector function
    """
    return initial_water_intensity_by_sector()


@subs(["sectors", "water"], _subscript_dict)
def _integ_input_water_intensity_by_sector():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for water_intensity_by_sector
    Limits: None
    Type: component
    Subs: ['sectors', 'water']

    Provides derivative for water_intensity_by_sector function
    """
    return variation_water_intensity_by_sector()


_integ_water_intensity_by_sector = Integ(
    _integ_input_water_intensity_by_sector,
    _integ_init_water_intensity_by_sector,
    "_integ_water_intensity_by_sector",
)


@subs(["water"], _subscript_dict)
def _integ_init_water_intensity_for_households():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for water_intensity_for_households
    Limits: None
    Type: setup
    Subs: ['water']

    Provides initial conditions for water_intensity_for_households function
    """
    return initial_water_intensity_for_households()


@subs(["water"], _subscript_dict)
def _integ_input_water_intensity_for_households():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for water_intensity_for_households
    Limits: None
    Type: component
    Subs: ['water']

    Provides derivative for water_intensity_for_households function
    """
    return variation_water_intensity_households()


_integ_water_intensity_for_households = Integ(
    _integ_input_water_intensity_for_households,
    _integ_init_water_intensity_for_households,
    "_integ_water_intensity_for_households",
)
