"""
Module climate.process_emissions
Translated using PySD version 3.14.0
"""

@component.add(
    name="historic_process_emissions_intensity",
    units="GtCO2/T$/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_process_emissions_intensity",
        "__lookup__": "_ext_lookup_historic_process_emissions_intensity",
    },
)
def historic_process_emissions_intensity(x, final_subs=None):
    return _ext_lookup_historic_process_emissions_intensity(x, final_subs)


_ext_lookup_historic_process_emissions_intensity = ExtLookup(
    "../climate.xlsx",
    "World",
    "years_process_emissions",
    "process_emissions_intensity",
    {},
    _root,
    {},
    "_ext_lookup_historic_process_emissions_intensity",
)


@component.add(
    name="last_year_historic_process_emissions",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_last_year_historic_process_emissions"},
)
def last_year_historic_process_emissions():
    return _ext_constant_last_year_historic_process_emissions()


_ext_constant_last_year_historic_process_emissions = ExtConstant(
    "../climate.xlsx",
    "World",
    "last_year_process_emissions",
    {},
    _root,
    {},
    "_ext_constant_last_year_historic_process_emissions",
)


@component.add(
    name="process_emissions_intensity",
    units="GTCO2e/T$/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "last_year_historic_process_emissions": 7,
        "historic_process_emissions_intensity": 5,
        "process_emissions_reduction_policy": 2,
        "target_year_process_emissions_improvement": 2,
    },
)
def process_emissions_intensity():
    return if_then_else(
        time() < last_year_historic_process_emissions(),
        lambda: historic_process_emissions_intensity(time()),
        lambda: if_then_else(
            time() < target_year_process_emissions_improvement(),
            lambda: historic_process_emissions_intensity(
                last_year_historic_process_emissions()
            )
            + (
                historic_process_emissions_intensity(
                    last_year_historic_process_emissions()
                )
                * (1 - process_emissions_reduction_policy())
                - historic_process_emissions_intensity(
                    last_year_historic_process_emissions()
                )
            )
            / (
                target_year_process_emissions_improvement()
                - last_year_historic_process_emissions()
            )
            * (time() - last_year_historic_process_emissions()),
            lambda: historic_process_emissions_intensity(
                last_year_historic_process_emissions()
            )
            * (1 - process_emissions_reduction_policy()),
        ),
    )


@component.add(
    name="process_emissions_reduction_policy",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_process_emissions_reduction_policy"},
)
def process_emissions_reduction_policy():
    return _ext_constant_process_emissions_reduction_policy()


_ext_constant_process_emissions_reduction_policy = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "policy_improvement_process_emissions_efficiency",
    {},
    _root,
    {},
    "_ext_constant_process_emissions_reduction_policy",
)


@component.add(
    name="target_year_process_emissions_improvement",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_target_year_process_emissions_improvement"
    },
)
def target_year_process_emissions_improvement():
    return _ext_constant_target_year_process_emissions_improvement()


_ext_constant_target_year_process_emissions_improvement = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "target_year_process_emissions",
    {},
    _root,
    {},
    "_ext_constant_target_year_process_emissions_improvement",
)


@component.add(
    name="Total_process_emissions",
    units="GTCO2e/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_total_output_by_sector": 1,
        "m_to_t": 1,
        "process_emissions_intensity": 1,
    },
)
def total_process_emissions():
    """
    Total emissions comming from industrial processes
    """
    return (
        float(
            required_total_output_by_sector().loc[
                "Coke_refined_petroleum_nuclear_fuel_and_chemicals_etc"
            ]
        )
        * m_to_t()
        * process_emissions_intensity()
    )
