"""
Module social_and_environmental_impacts
Translated using PySD version 2.2.1
"""


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


def carbon_footprint_tonnescperson():
    """
    Real Name: "Carbon footprint tonnesC/person"
    Original Eqn: "Carbon footprint tCO2/person"*C per CO2
    Units: tonnesC/person
    Limits: (None, None)
    Type: component
    Subs: None

    Carbon footprint.
    """
    return carbon_footprint_tco2person() * c_per_co2()


def co2_emissions_per_value_added():
    """
    Real Name: CO2 emissions per value added
    Original Eqn: ZIDZ( Total CO2 emissions GTCO2, GDP AUT )
    Units: GtCO2/(Year*T$)
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions per value added (GDP).
    """
    return zidz(total_co2_emissions_gtco2(), gdp_aut())


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

    Conversion from tones to Gigatonnes of carbon.
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
