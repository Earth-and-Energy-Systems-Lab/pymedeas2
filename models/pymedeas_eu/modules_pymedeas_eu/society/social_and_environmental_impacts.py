"""
Module social_and_environmental_impacts
Translated using PySD version 3.0.1
"""


@component.add(
    name='"Carbon footprint tCO2/person"',
    units="tCO2/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1, "t_per_gt": 1, "population": 1},
)
def carbon_footprint_tco2person():
    """
    CO2 emissions per capita.
    """
    return total_co2_emissions_gtco2() * t_per_gt() / population()


@component.add(
    name='"Carbon footprint tonnesC/person"',
    units="tonnesC/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_footprint_tco2person": 1, "c_per_co2": 1},
)
def carbon_footprint_tonnescperson():
    """
    Carbon footprint.
    """
    return carbon_footprint_tco2person() * c_per_co2()


@component.add(
    name="CO2 emissions per value added",
    units="GtCO2/(Year*T$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1, "gdp_eu": 1},
)
def co2_emissions_per_value_added():
    """
    CO2 emissions per value added (GDP).
    """
    return zidz(total_co2_emissions_gtco2(), gdp_eu())


@component.add(
    name="Potential max HDI",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_tfec_per_capita": 2},
)
def potential_max_hdi():
    """
    Potential HDI that can be reached by a society given its final energy use per capita.
    """
    return if_then_else(
        net_tfec_per_capita() <= 0,
        lambda: 0,
        lambda: np.minimum(1, 0.1395 * np.log(net_tfec_per_capita()) + 0.1508),
    )


@component.add(
    name="t per Gt", units="TonC/GtC", comp_type="Constant", comp_subtype="Normal"
)
def t_per_gt():
    """
    Conversion from tones to Gigatonnes of carbon.
    """
    return 1000000000.0


@component.add(
    name="Total water use per capita",
    units="dam3/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use": 1, "population": 1},
)
def total_water_use_per_capita():
    """
    Total water use (all types aggregated) per capita.
    """
    return total_water_use() / population()


@component.add(
    name="Water use per type per capita",
    units="dam3/person",
    subscripts=["water"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use_by_type": 1, "population": 1},
)
def water_use_per_type_per_capita():
    """
    Water use per type per capita.
    """
    return total_water_use_by_type() / population()
