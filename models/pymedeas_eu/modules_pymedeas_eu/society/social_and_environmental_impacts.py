"""
Module society.social_and_environmental_impacts
Translated using PySD version 3.14.2
"""

@component.add(
    name='"Carbon_footprint_tCO2/person"',
    units="tCO2/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "aux_total_co2_emissions_gtco2": 1,
        "tco2_per_gtco2": 1,
        "population": 1,
    },
)
def carbon_footprint_tco2person():
    """
    CO2 emissions per capita.
    """
    return aux_total_co2_emissions_gtco2() * tco2_per_gtco2() / population()


@component.add(
    name='"Carbon_footprint_tonnesC/person"',
    units="tonnesC/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_footprint_tco2person": 1, "tc_per_tco2": 1},
)
def carbon_footprint_tonnescperson():
    """
    Carbon footprint.
    """
    return carbon_footprint_tco2person() * tc_per_tco2()


@component.add(
    name="CO2_emissions_per_value_added",
    units="GtCO2/(year*T$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aux_total_co2_emissions_gtco2": 1, "gdp_eu": 1},
)
def co2_emissions_per_value_added():
    """
    CO2 emissions per value added (GDP).
    """
    return zidz(aux_total_co2_emissions_gtco2(), gdp_eu())


@component.add(
    name="Potential_max_HDI",
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
        lambda: float(
            np.minimum(
                1,
                0.1395 * float(np.log(net_tfec_per_capita() * unit_corr_hdi()))
                + 0.1508,
            )
        ),
    )


@component.add(
    name="tC_per_tCO2", units="tC/tCO2", comp_type="Constant", comp_subtype="Normal"
)
def tc_per_tco2():
    return 3 / 11


@component.add(
    name="tCO2_per_GtCO2",
    units="tCO2/GtCO2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tco2_per_gtco2():
    """
    Conversion from tones to Gigatonnes of carbon.
    """
    return 1000000000.0


@component.add(
    name="Total_water_use_per_capita",
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
    name="unit_corr_HDI",
    units="(year*person)/GJ",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_corr_hdi():
    return 1


@component.add(
    name="Water_use_per_type_per_capita",
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
