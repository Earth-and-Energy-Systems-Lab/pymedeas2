"""
Module social_and_environmental_impacts
Translated using PySD version 2.2.1
"""


def carbon_footprint_tcperson():
    """
    Real Name: "Carbon footprint tC/person"
    Original Eqn:
    Units: tC/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Carbon footprint.
    """
    return carbon_footprint_tco2person() * c_per_co2()


def carbon_footprint_tco2person():
    """
    Real Name: "Carbon footprint tCO2/person"
    Original Eqn:
    Units: tCO2/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    CO2 emissions per capita.
    """
    return total_co2_emissions_gtco2() * t_per_gt() / population()


def co2_emissions_per_value_added():
    """
    Real Name: CO2 emissions per value added
    Original Eqn:
    Units: GtCO2/(year*T$)
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    CO2 emissions per value added (GDP).
    """
    return zidz(total_co2_emissions_gtco2(), gdp())


def potential_max_hdi():
    """
    Real Name: Potential max HDI
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential HDI that can be reached by a society given its final energy use per capita.
    """
    return if_then_else(
        net_tfec_per_capita() <= 0,
        lambda: 0,
        lambda: np.minimum(1, 0.1395 * np.log(net_tfec_per_capita()) + 0.1508),
    )


def t_per_gt():
    """
    Real Name: t per Gt
    Original Eqn:
    Units: TonC/GtC
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion from tones to gigatonnes of carbon.
    """
    return 1000000000.0


def total_water_use_per_capita():
    """
    Real Name: Total water use per capita
    Original Eqn:
    Units: dam3/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total water use (all types aggregated) per capita.
    """
    return total_water_use() / population()


@subs(["water"], _subscript_dict)
def water_use_per_type_per_capita():
    """
    Real Name: Water use per type per capita
    Original Eqn:
    Units: dam3/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['water']

    Water use per type per capita.
    """
    return total_water_use_by_type() / population()
