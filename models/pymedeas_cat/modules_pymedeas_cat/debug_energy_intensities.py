"""
Module debug_energy_intensities
Translated using PySD version 3.9.1
"""


@component.add(
    name="DEBUG historic energy intensities",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_energy_intensities",
        "__lookup__": "_ext_lookup_debug_historic_energy_intensities",
    },
)
def debug_historic_energy_intensities(x, final_subs=None):
    return _ext_lookup_debug_historic_energy_intensities(x, final_subs)


_ext_lookup_debug_historic_energy_intensities = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_historic_ei",
    "historic_energy_intensities",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_energy_intensities",
)


@component.add(
    name="energy consumption sectors",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_from_households_and_sectors": 1},
)
def energy_consumption_sectors():
    return sum(
        energy_consumption_from_households_and_sectors()
        .loc[:, _subscript_dict["sectors"]]
        .rename({"SECTORS and HOUSEHOLDS": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="energy intensisty households",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_intensity_of_households": 1},
)
def energy_intensisty_households():
    return sum(
        energy_intensity_of_households().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="energy intensity sectors",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"global_energy_intensity_by_sector": 1},
)
def energy_intensity_sectors():
    return sum(
        global_energy_intensity_by_sector().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="gross inland energy consumption",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_sectors": 1},
)
def gross_inland_energy_consumption():
    return sum(
        energy_consumption_sectors().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="total energy intensity",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_intensisty_households": 1, "energy_intensity_sectors": 1},
)
def total_energy_intensity():
    return energy_intensisty_households() + energy_intensity_sectors()


@component.add(
    name="total energy intensity CAT",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gross_inland_energy_consumption": 1, "gdp_cat": 1},
)
def total_energy_intensity_cat():
    return gross_inland_energy_consumption() / gdp_cat()
