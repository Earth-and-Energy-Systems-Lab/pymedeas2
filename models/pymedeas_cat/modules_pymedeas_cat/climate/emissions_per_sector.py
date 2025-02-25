"""
Module climate.emissions_per_sector
Translated using PySD version 3.14.0
"""

@component.add(
    name="CH4_emissions_households_and_sectors",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources"), np.str_("SECTORS_and_HOUSEHOLDS")],
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
    name="CO2_emissions_from_year",
    units="GtCO2/year",
    subscripts=[np.str_("SECTORS_and_HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "year_co2": 1, "co2_emissions_households_and_sectors": 1},
)
def co2_emissions_from_year():
    return if_then_else(
        time() < year_co2(),
        lambda: xr.DataArray(
            0,
            {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
            ["SECTORS_and_HOUSEHOLDS"],
        ),
        lambda: co2_emissions_households_and_sectors(),
    )


@component.add(
    name="CO2_emissions_households_and_sectors",
    units="GtCO2/year",
    subscripts=[np.str_("SECTORS_and_HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_households_and_sectors_before_ccs": 1,
        "co2_captured_by_sector_energy_related": 1,
    },
)
def co2_emissions_households_and_sectors():
    """
    CO2 emissions after substracting the CCS absorbed emissions
    """
    return (
        sum(
            co2_emissions_households_and_sectors_before_ccs().rename(
                {np.str_("final_sources"): "final_sources!"}
            ),
            dim=["final_sources!"],
        )
        - co2_captured_by_sector_energy_related()
    )


@component.add(
    name="CO2_emissions_households_and_sectors_before_ccs",
    units="GtCO2/year",
    subscripts=[np.str_("final_sources"), np.str_("SECTORS_and_HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_per_fuel": 1,
        "share_energy_consumption_from_households_and_sectors": 1,
    },
)
def co2_emissions_households_and_sectors_before_ccs():
    """
    CO2 emissions per sector/househols and final source before substracting the captured by CCS technologies. The electricity and heat emissions correspond to the emissions produced by burning fossil fuels to generate electricity and heat for that sector/households.
    """
    return (
        co2_emissions_per_fuel()
        * share_energy_consumption_from_households_and_sectors()
    )


@component.add(
    name="CO2_emissions_sectors_and_households_including_process",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_process_emissions": 2,
        "process_co2_captured_ccs": 2,
        "co2_emissions_households_and_sectors": 2,
    },
)
def co2_emissions_sectors_and_households_including_process():
    return if_then_else(
        total_process_emissions()
        > sum(
            process_co2_captured_ccs().rename(
                {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        ),
        lambda: sum(
            co2_emissions_households_and_sectors().rename(
                {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        )
        + total_process_emissions()
        - sum(
            process_co2_captured_ccs().rename(
                {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        ),
        lambda: sum(
            co2_emissions_households_and_sectors().rename(
                {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        ),
    )


@component.add(
    name="cumulated_CO2_emissions",
    units="GtCO2",
    subscripts=[np.str_("SECTORS_and_HOUSEHOLDS")],
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
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    ),
    "_integ_cumulated_co2_emissions",
)


@component.add(
    name="energy_consumption_from_households_and_sectors",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("SECTORS_and_HOUSEHOLDS")],
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
            "final_sources": _subscript_dict["final_sources"],
            "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        },
        [np.str_("final_sources"), np.str_("SECTORS_and_HOUSEHOLDS")],
    )
    value.loc[:, ["Households"]] = (
        households_final_energy_demand()
        .expand_dims({"SECTORS_and_HOUSEHOLDS": ["Households"]}, 1)
        .values
    )
    value.loc[:, _subscript_dict["sectors"]] = (
        real_final_energy_by_sector_and_fuel_cat().values
    )
    return value


@component.add(
    name="share_energy_consumption_from_households_and_sectors",
    units="Dmnl",
    subscripts=[np.str_("final_sources"), np.str_("SECTORS_and_HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_consumption_from_households_and_sectors": 2},
)
def share_energy_consumption_from_households_and_sectors():
    return zidz(
        energy_consumption_from_households_and_sectors(),
        sum(
            energy_consumption_from_households_and_sectors().rename(
                {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
            ),
            dim=["SECTORS_and_HOUSEHOLDS!"],
        ).expand_dims(
            {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]}, 1
        ),
    )


@component.add(
    name="Total_CO2_emissions_after_LULUCF",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_gtco2": 1,
        "co2_soillucf_emissions": 1,
        "afforestation_program_2020_gtco2": 1,
    },
)
def total_co2_emissions_after_lulucf():
    return (
        total_co2_emissions_gtco2()
        + co2_soillucf_emissions()
        - afforestation_program_2020_gtco2()
    )


@component.add(
    name="Total_CO2_emissions_GTCO2",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_sectors_and_households_including_process": 1,
        "total_dac_co2_captured": 1,
    },
)
def total_co2_emissions_gtco2():
    """
    Total emissions taking into account the carbon capture technologies
    """
    return (
        co2_emissions_sectors_and_households_including_process()
        - total_dac_co2_captured()
    )


@component.add(
    name="Total_CO2_emissions_GTCO2_before_CCS",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_households_and_sectors_before_ccs": 1},
)
def total_co2_emissions_gtco2_before_ccs():
    return sum(
        co2_emissions_households_and_sectors_before_ccs().rename(
            {
                np.str_("final_sources"): "final_sources!",
                np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!",
            }
        ),
        dim=["final_sources!", "SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="Total_cumulated_CO2_emissions",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cumulated_co2_emissions": 1},
)
def total_cumulated_co2_emissions():
    return sum(
        cumulated_co2_emissions().rename(
            {np.str_("SECTORS_and_HOUSEHOLDS"): "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="year_co2", units="year", comp_type="Constant", comp_subtype="Normal"
)
def year_co2():
    return 1995
