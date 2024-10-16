"""
Module climatetotal_ghg_emissions
Translated using PySD version 3.14.0
"""

@component.add(
    name="correction factor all GHGs",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def correction_factor_all_ghgs():
    """
    Taking as reference data for 2012 (comparing MEDEAS outputs and CAT from INSTM report).
    """
    return 1.22


@component.add(
    name="Cumulative Ce GHG emissions",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_ce_ghg_emissions": 1},
    other_deps={
        "_integ_cumulative_ce_ghg_emissions": {
            "initial": {},
            "step": {"total_ce_all_ghg": 1},
        }
    },
)
def cumulative_ce_ghg_emissions():
    return _integ_cumulative_ce_ghg_emissions()


_integ_cumulative_ce_ghg_emissions = Integ(
    lambda: total_ce_all_ghg(), lambda: 0, "_integ_cumulative_ce_ghg_emissions"
)


@component.add(
    name="GWP 100 years CH4",
    units="GTCO2e/MtCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gwp_100_years_ch4():
    return 34 / 1000


@component.add(
    name="Total Ce all GHG",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2e_gwp100_years": 1,
        "correction_factor_all_ghgs": 1,
        "gtc_per_gtco2": 1,
    },
)
def total_ce_all_ghg():
    return total_co2e_gwp100_years() * correction_factor_all_ghgs() * gtc_per_gtco2()


@component.add(
    name="Total CO2e all GHG",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2e_gwp100_years": 1, "correction_factor_all_ghgs": 1},
)
def total_co2e_all_ghg():
    return total_co2e_gwp100_years() * correction_factor_all_ghgs()


@component.add(
    name='"Total CO2e [GWP=100 years]"',
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_emissions_mtch4": 1,
        "gwp_100_years_ch4": 1,
        "total_co2_emissions_gtco2_after_capture": 1,
    },
)
def total_co2e_gwp100_years():
    return (
        total_ch4_emissions_mtch4() * gwp_100_years_ch4()
        + total_co2_emissions_gtco2_after_capture()
    )
