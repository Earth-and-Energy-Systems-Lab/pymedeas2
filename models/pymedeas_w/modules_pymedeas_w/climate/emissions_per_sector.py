"""
Module climate.emissions_per_sector
Translated using PySD version 3.10.0
"""


@component.add(
    name="CH4 emissions households and sectors",
    units="GtCO2/year",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def ch4_emissions_households_and_sectors():
    """
    CH2 emissions per sector/househols and final source. The electricity and heat emissions correspond to the emissions produced by burning fossil fuels to generate electricity and heat for that sector/households.
    """
    return (
        ch4_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="CO2 emissions households and sectors",
    units="GtCO2/year",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def co2_emissions_households_and_sectors():
    """
    CO2 emissions per sector/househols and final source. The electricity and heat emissions correspond to the emissions produced by burning fossil fuels to generate electricity and heat for that sector/households.
    """
    return (
        co2_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="energy consumption from households and sectors",
    units="EJ",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "real_final_energy_by_sector_and_fuel": 1,
    },
)
def energy_consumption_from_households_and_sectors():
    """
    Final energy consumption of a given sector (or households) by fuel. This consumption is emissions relevant.
    """
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
    ] = real_final_energy_by_sector_and_fuel().values
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
    """
    Share of each fuel energy direct consumption per sector and household.
    """
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
