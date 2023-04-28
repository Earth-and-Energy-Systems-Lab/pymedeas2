"""
Module debug_emissions
Translated using PySD version 3.9.1
"""


@component.add(
    name="DEBUG historic CO2 emissions",
    units="GtCO2/Year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_co2_emissions",
        "__lookup__": "_ext_lookup_debug_historic_co2_emissions",
    },
)
def debug_historic_co2_emissions(x, final_subs=None):
    return _ext_lookup_debug_historic_co2_emissions(x, final_subs)


_ext_lookup_debug_historic_co2_emissions = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_emissions",
    "CO2_emissions",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_co2_emissions",
)


@component.add(
    name="DEBUG historic ktCO2 emissions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "debug_historic_co2_emissions": 1},
)
def debug_historic_ktco2_emissions():
    return debug_historic_co2_emissions(time()) * 1000000.0


@component.add(
    name="DEBUG model ktCO2 emissions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1},
)
def debug_model_ktco2_emissions():
    return total_co2_emissions_gtco2() * 1000000.0
