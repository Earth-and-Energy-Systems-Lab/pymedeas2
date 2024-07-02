"""
Module debug_energy_intensities
Translated using PySD version 3.14.0
"""

@component.add(
    name="energy_consumption_sectors",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_from_households_and_sectors": 1},
)
def energy_consumption_sectors():
    return sum(
        energy_consumption_from_households_and_sectors()
        .loc[:, _subscript_dict["sectors"]]
        .rename({"SECTORS_and_HOUSEHOLDS": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="energy_intensisty_households",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_intensity_of_households": 1},
)
def energy_intensisty_households():
    return sum(
        energy_intensity_of_households().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="energy_intensity_sectors",
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
    name="gross_inland_energy_consumption",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_sectors": 1},
)
def gross_inland_energy_consumption():
    return sum(
        energy_consumption_sectors().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="total_energy_intensity",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_intensisty_households": 1, "energy_intensity_sectors": 1},
)
def total_energy_intensity():
    return energy_intensisty_households() + energy_intensity_sectors()
