"""
Module climate.emissions_per_sector
Translated using PySD version 3.9.1
"""


@component.add(
    name="CH4 emissions households and sectors",
    units="GtCO2/Year",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def ch4_emissions_households_and_sectors():
    return (
        ch4_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="CO2 emissions households and sectors",
    units="GtCO2/Year",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def co2_emissions_households_and_sectors():
    return (
        co2_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="DEBUG total CO2 emissions per sector",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors": 1},
)
def debug_total_co2_emissions_per_sector():
    return sum(
        co2_emissions_households_and_sectors().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@component.add(
    name="energy consumption from households and sectors",
    units="EJ",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "real_final_energy_by_sector_and_fuel_cat": 1,
    },
)
def energy_consumption_from_households_and_sectors():
    value = xr.DataArray(
        np.nan,
        {
            "final sources": _subscript_dict["final sources"],
            "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        },
        ["final sources", "SECTORS and HOUSEHOLDS"],
    )
    value.loc[:, ["Households"]] = (
        households_final_energy_demand()
        .expand_dims({"SECTORS and HOUSEHOLDS": ["Households"]}, 1)
        .values
    )
    value.loc[
        :, _subscript_dict["sectors"]
    ] = real_final_energy_by_sector_and_fuel_cat().values
    return value


@component.add(
    name="share energy consumption from households and sectors",
    units="Dmnl",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_from_households_and_sectors": 2},
)
def share_energy_consumption_from_households_and_sectors():
    return zidz(
        energy_consumption_from_households_and_sectors(),
        sum(
            energy_consumption_from_households_and_sectors().rename(
                {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
            ),
            dim=["SECTORS and HOUSEHOLDS!"],
        ).expand_dims(
            {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]}, 1
        ),
    )
