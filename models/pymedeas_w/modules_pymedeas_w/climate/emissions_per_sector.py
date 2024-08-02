"""
Module climate.emissions_per_sector
Translated using PySD version 3.14.1
"""

@component.add(
    name="CH4 emissions households and sectors",
    units="MtCH4/year",
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
    name="CO2 emissions from year",
    units="GtCO2/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "year_co2": 1, "co2_emissions_households_and_sectors": 1},
)
def co2_emissions_from_year():
    return if_then_else(
        time() < year_co2(),
        lambda: xr.DataArray(
            0,
            {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
            ["SECTORS and HOUSEHOLDS"],
        ),
        lambda: co2_emissions_households_and_sectors(),
    )


@component.add(
    name="CO2 emissions households and sectors",
    units="GTCO2e/year",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_households_and_sectors_before_ccs": 1,
        "co2_captured_by_sector_energy_related": 1,
        "dac_co2_captured_energy_per_sector": 1,
    },
)
def co2_emissions_households_and_sectors():
    """
    CO2 emissions after substracting the CCS and DACC absorbed emissions
    """
    return (
        sum(
            co2_emissions_households_and_sectors_before_ccs().rename(
                {"final sources": "final sources!"}
            ),
            dim=["final sources!"],
        )
        - co2_captured_by_sector_energy_related()
        - dac_co2_captured_energy_per_sector()
    )


@component.add(
    name="CO2 emissions households and sectors before ccs",
    units="GtCO2/year",
    subscripts=["final sources", "SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def co2_emissions_households_and_sectors_before_ccs():
    """
    CO2 emissions per sector/househols and final source substracting the captured by CCS technologies. The electricity and heat emissions correspond to the emissions produced by burning fossil fuels to generate electricity and heat for that sector/households.
    """
    return (
        co2_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="cumulated CO2 emissions",
    units="GtCO2",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_co2_emissions": 1},
    other_deps={
        "_integ_cumulated_co2_emissions": {
            "initial": {},
            "step": {"co2_emissions_from_year": 1},
        }
    },
)
def cumulated_co2_emissions():
    return _integ_cumulated_co2_emissions()


_integ_cumulated_co2_emissions = Integ(
    lambda: co2_emissions_from_year(),
    lambda: xr.DataArray(
        0,
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    ),
    "_integ_cumulated_co2_emissions",
)


@component.add(
    name="energy consumption from households and sectors",
    units="EJ/year",
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
    value.loc[:, _subscript_dict["sectors"]] = (
        real_final_energy_by_sector_and_fuel().values
    )
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


@component.add(
    name="Total CO2 emissions after LULUCF",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_gtco2": 1,
        "co2_soilluc_emissions": 1,
        "afforestation_program_2020_gtco2": 1,
    },
)
def total_co2_emissions_after_lulucf():
    """
    Total emissions taking into account the carbon capture technologies and the LULUCF
    """
    return (
        total_co2_emissions_gtco2()
        + co2_soilluc_emissions()
        - afforestation_program_2020_gtco2()
    )


@component.add(
    name="Total CO2 emissions GTCO2",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors": 1},
)
def total_co2_emissions_gtco2():
    """
    Total emissions taking into account the carbon capture technologies
    """
    return sum(
        co2_emissions_households_and_sectors().rename(
            {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="Total cumulated CO2 emissions",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cumulated_co2_emissions": 1},
)
def total_cumulated_co2_emissions():
    return sum(
        cumulated_co2_emissions().rename(
            {"SECTORS and HOUSEHOLDS": "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name="year co2", units="year", comp_type="Constant", comp_subtype="Normal"
)
def year_co2():
    return 2020
