"""
Module social_and_env_impacts
Translated using PySD version 2.1.0
"""


def annual_work_hours_for_res():
    """
    Real Name: Annual work hours for RES
    Original Eqn: Total jobs RES*Working hours per year
    Units: Hours/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_jobs_res() * working_hours_per_year()


def carbon_footprint_tcperson():
    """
    Real Name: "Carbon footprint tC/person"
    Original Eqn: "Carbon footprint tCO2/person"*C per CO2
    Units: tC/person
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon footprint.
    """
    return carbon_footprint_tco2person() * c_per_co2()


def carbon_footprint_tco2person():
    """
    Real Name: "Carbon footprint tCO2/person"
    Original Eqn: Total CO2 emissions GTCO2*t per Gt/Population
    Units: tCO2/person
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions per capita.
    """
    return total_co2_emissions_gtco2() * t_per_gt() / population()


def co2_emissions_per_value_added():
    """
    Real Name: CO2 emissions per value added
    Original Eqn: ZIDZ( Total CO2 emissions GTCO2, GDP )
    Units: GtCO2/(year*T$)
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions per value added (GDP).
    """
    return zidz(total_co2_emissions_gtco2(), gdp())


def days_per_year():
    """
    Real Name: days per year
    Original Eqn: 365
    Units: days/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Constant: 365 days in a year.
    """
    return 365


def hours_work_per_gj_res_delivered():
    """
    Real Name: Hours work per GJ RES delivered
    Original Eqn: ZIDZ( Annual work hours for RES, (TFEC RES EJ*GJ per EJ) )
    Units: Hours/GJ
    Limits: (None, None)
    Type: component
    Subs: None

    Hours of work per GJ of RES delivered (final energy).
    """
    return zidz(annual_work_hours_for_res(), (tfec_res_ej() * gj_per_ej()))


def potential_max_hdi():
    """
    Real Name: Potential max HDI
    Original Eqn: IF THEN ELSE(Net TFEC per capita<=0, 0, MIN(1, 0.1395*LN(Net TFEC per capita)+0.1508))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Potential HDI that can be reached by a society given its final energy use
        per capita.
    """
    return if_then_else(
        net_tfec_per_capita() <= 0,
        lambda: 0,
        lambda: np.minimum(1, 0.1395 * np.log(net_tfec_per_capita()) + 0.1508),
    )


def t_per_gt():
    """
    Real Name: t per Gt
    Original Eqn: 1e+09
    Units: TonC/GtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion from tones to gigatonnes of carbon.
    """
    return 1e09


def total_water_use_per_capita():
    """
    Real Name: Total water use per capita
    Original Eqn: Total water use/Population
    Units: dam3/person
    Limits: (None, None)
    Type: component
    Subs: None

    Total water use (all types aggregated) per capita.
    """
    return total_water_use() / population()


@subs(["water"], _subscript_dict)
def water_use_per_type_per_capita():
    """
    Real Name: Water use per type per capita
    Original Eqn: Total water use by type[water]/Population
    Units: dam3/person
    Limits: (None, None)
    Type: component
    Subs: ['water']

    Water use per type per capita.
    """
    return total_water_use_by_type() / population()


def working_hours_per_day():
    """
    Real Name: Working hours per day
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'daily_working_hours')
    Units: Hour*people
    Limits: (None, None)
    Type: constant
    Subs: None

    Working hours per day.
    """
    return _ext_constant_working_hours_per_day()


def working_hours_per_year():
    """
    Real Name: Working hours per year
    Original Eqn: Working hours per day*days per year
    Units: Hour*person/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return working_hours_per_day() * days_per_year()


_ext_constant_working_hours_per_day = ExtConstant(
    "../parameters.xlsx",
    "World",
    "daily_working_hours",
    {},
    _root,
    "_ext_constant_working_hours_per_day",
)
