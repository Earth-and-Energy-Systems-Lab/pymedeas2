"""
Module societysocial_and_environmental_impacts
Translated using PySD version 3.14.0
"""

@component.add(
    name='"Carbon footprint tCO2/person"',
    units="tCO2/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_gtco2_after_capture": 1,
        "tco2_per_gtco2": 1,
        "population": 1,
    },
)
def carbon_footprint_tco2person():
    """
    CO2 emissions per capita.
    """
    return total_co2_emissions_gtco2_after_capture() * tco2_per_gtco2() / population()


@component.add(
    name='"Carbon footprint tC/person"',
    units="tC/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_footprint_tco2person": 1, "tc_per_tco2": 1},
)
def carbon_footprint_tcperson():
    """
    Carbon footprint.
    """
    return carbon_footprint_tco2person() * tc_per_tco2()


@component.add(
    name="CO2 emissions per value added",
    units="GtCO2/(year*T$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2_after_capture": 1, "gdp": 1},
)
def co2_emissions_per_value_added():
    """
    CO2 emissions per value added (GDP).
    """
    return zidz(total_co2_emissions_gtco2_after_capture(), gdp())


@component.add(
    name="Potential max HDI",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_tfec_per_capita": 2, "unit_corr_hdi": 1},
)
def potential_max_hdi():
    """
    Potential HDI that can be reached by a society given its final energy use per capita.
    """
    return if_then_else(
        net_tfec_per_capita() <= 0,
        lambda: 0,
        lambda: np.minimum(
            1, 0.1395 * np.log(net_tfec_per_capita() * unit_corr_hdi()) + 0.1508
        ),
    )


@component.add(
    name="tC per tCO2", units="tC/tCO2", comp_type="Constant", comp_subtype="Normal"
)
def tc_per_tco2():
    return 3 / 11


@component.add(
    name="tCO2 per GtCO2",
    units="tCO2/GtCO2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tco2_per_gtco2():
    """
    Conversion from tones to gigatonnes of carbon.
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
    name="unit corr HDI",
    units="(year*person)/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_corr_hdi():
    return 1


@component.add(
    name="Water use per type per capita",
    units="dam3/person",
    subscripts=[np.str_("water")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_water_use_by_type": 1, "population": 1},
)
def water_use_per_type_per_capita():
    """
    Water use per type per capita.
    """
    return total_water_use_by_type() / population()
