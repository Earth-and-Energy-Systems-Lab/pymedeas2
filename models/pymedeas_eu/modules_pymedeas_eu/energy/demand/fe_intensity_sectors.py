"""
Module energy.demand.fe_intensity_sectors
Translated using PySD version 3.14.2
"""

@component.add(
    name="Activate_BOTTOM_UP_method",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def activate_bottom_up_method():
    """
    Activate BOTTOM UP method or maintain TOP DOWN method. Activate for each sector (by default, only inland transport sector) 0. Bottom-up NOT activated 1. Bottom-up activated
    """
    value = xr.DataArray(
        np.nan,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["Land_Transport"]] = False
    except_subs.loc[["Households"]] = False
    value.values[except_subs.values] = 0
    value.loc[["Land_Transport"]] = 0
    value.loc[["Households"]] = 0
    return value


@component.add(
    name="available_improvement_efficiency",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "min_energy_intensity_vs_intial": 2,
        "initial_global_energy_intensity_2009": 2,
        "global_energy_intensity_by_sector": 1,
    },
)
def available_improvement_efficiency():
    """
    Remainig improvement of energy intensity respect to the minimum value.
    """
    return np.minimum(
        1,
        if_then_else(
            time() > 2009,
            lambda: zidz(
                global_energy_intensity_by_sector()
                - min_energy_intensity_vs_intial()
                * initial_global_energy_intensity_2009()
                .loc[_subscript_dict["sectors"]]
                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
                (1 - min_energy_intensity_vs_intial())
                * initial_global_energy_intensity_2009()
                .loc[_subscript_dict["sectors"]]
                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
            ),
            lambda: xr.DataArray(
                1, {"sectors": _subscript_dict["sectors"]}, ["sectors"]
            ),
        ),
    )


@component.add(
    name="Choose_final_sectoral_energy_intensities_evolution_method",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_choose_final_sectoral_energy_intensities_evolution_method"
    },
)
def choose_final_sectoral_energy_intensities_evolution_method():
    """
    0- Dynamic evolution with policies and feedback of final fuel scarcity 1- Constant at 2009 levels 2- Sectoral energy intensity targets defined by user
    """
    return _ext_constant_choose_final_sectoral_energy_intensities_evolution_method()


_ext_constant_choose_final_sectoral_energy_intensities_evolution_method = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "sectoral_FEI_evolution_method",
    {},
    _root,
    {},
    "_ext_constant_choose_final_sectoral_energy_intensities_evolution_method",
)


@component.add(
    name="Decrease_of_intensity_due_to_energy_a_technology_change_TOP_DOWN",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_bottom_up_method": 1,
        "global_energy_intensity_by_sector": 1,
        "evol_final_energy_intensity_by_sector_and_fuel": 2,
        "max_yearly_change_between_sources": 1,
        "pressure_to_change_energy_technology": 1,
        "percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities": 1,
        "minimum_fraction_source": 1,
    },
)
def decrease_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    When in one economic sector, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the decrease of (a).
    """
    return if_then_else(
        (
            activate_bottom_up_method()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            == 0
        ).expand_dims({"final_sources": _subscript_dict["final_sources"]}, 1),
        lambda: if_then_else(
            zidz(
                evol_final_energy_intensity_by_sector_and_fuel(),
                global_energy_intensity_by_sector().expand_dims(
                    {"final_sources": _subscript_dict["final_sources"]}, 1
                ),
            )
            >= minimum_fraction_source()
            .loc[_subscript_dict["sectors"], :]
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
            lambda: (
                max_yearly_change_between_sources()
                .loc[_subscript_dict["sectors"], :]
                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                * (
                    1
                    + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
                )
            )
            * evol_final_energy_intensity_by_sector_and_fuel()
            * pressure_to_change_energy_technology(),
            lambda: xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final_sources": _subscript_dict["final_sources"],
                },
                ["sectors", "final_sources"],
            ),
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final_sources": _subscript_dict["final_sources"],
            },
            ["sectors", "final_sources"],
        ),
    )


@component.add(
    name="Efficiency_energy_acceleration",
    units="Dmnl/year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "maximum_yearly_acceleration_of_intensity_improvement": 1,
        "percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities": 1,
        "pressure_to_improve_energy_intensity_efficiency": 1,
    },
)
def efficiency_energy_acceleration():
    """
    This variable represents the acceleration of the process of variation of the energy intensity that can be produced by polítcas or scarcity pressures.
    """
    return (
        -maximum_yearly_acceleration_of_intensity_improvement()
        * (
            1
            + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
        )
        * pressure_to_improve_energy_intensity_efficiency()
    )


@component.add(
    name="efficiency_rate_of_substitution",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources", "final_sources1"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_rate_of_substitution"},
)
def efficiency_rate_of_substitution():
    """
    It is necessary to take into account that the energy efficiencies of the two technologies exchanged do not necessarily have to be the same. In other words, a decrease in the energy intensity of (a) will not imply the same increase in the energy intensity of (b). This possible difference is compensated through the parameter “Efficiency rate of substitution”.
    """
    return _ext_constant_efficiency_rate_of_substitution()


_ext_constant_efficiency_rate_of_substitution = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "efficiency_rate_of_substitution_electricity*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": ["electricity"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": _subscript_dict["final_sources1"],
    },
    "_ext_constant_efficiency_rate_of_substitution",
)

_ext_constant_efficiency_rate_of_substitution.add(
    r"../energy.xlsx",
    "Europe",
    "efficiency_rate_of_substitution_heat*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": ["heat"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    r"../energy.xlsx",
    "Europe",
    "efficiency_rate_of_substitution_liquids*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": ["liquids"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    r"../energy.xlsx",
    "Europe",
    "efficiency_rate_of_substitution_gases*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": ["gases"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    r"../energy.xlsx",
    "Europe",
    "efficiency_rate_of_substitution_solids*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
        "final_sources1": ["solids"],
    },
)


@component.add(
    name="Energy_intensity_target",
    units="EJ/Tdollars",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_intensity_target_mdollar": 1, "mdollar_per_tdollar": 1},
)
def energy_intensity_target():
    """
    Energy intensity targets by sector and final energy defined by user
    """
    return energy_intensity_target_mdollar() * mdollar_per_tdollar()


@component.add(
    name="energy_intensity_target_Mdollar",
    units="EJ/M$",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_energy_intensity_target_mdollar"},
)
def energy_intensity_target_mdollar():
    """
    Energy intensity targets by sector and final energy defined by user
    """
    return _ext_constant_energy_intensity_target_mdollar()


_ext_constant_energy_intensity_target_mdollar = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "energy_intensity_target*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_energy_intensity_target_mdollar",
)


@component.add(
    name="Evol_final_energy_intensity_by_sector_and_fuel",
    units="EJ/Tdollars",
    subscripts=["sectors", "final_sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_evol_final_energy_intensity_by_sector_and_fuel": 1},
    other_deps={
        "_integ_evol_final_energy_intensity_by_sector_and_fuel": {
            "initial": {"initial_energy_intensity_1995": 1},
            "step": {
                "increase_of_intensity_due_to_energy_a_technology_change_top_down": 1,
                "inertial_rate_energy_intensity_top_down": 1,
                "rate_change_intensity_bottom_up": 1,
                "decrease_of_intensity_due_to_energy_a_technology_change_top_down": 1,
            },
        }
    },
)
def evol_final_energy_intensity_by_sector_and_fuel():
    """
    This variable models the dynamic evolution of the matrix of energy intensities of the 35 economic sectors and the 5 types of final energy. It is a 35x5 matrix. The evolution of the intensities is considered to be due to two main effects: (1) the variation of the energy efficiency (flow due to the variable inertial rate energy intensity) and (2) the change of one type of final energy by another, As a consequence of a technological change (flow due to the variables Increase / decrease of intensity due to energy to technology change), as for example the change due to the electrification of the transport.
    """
    return _integ_evol_final_energy_intensity_by_sector_and_fuel()


_integ_evol_final_energy_intensity_by_sector_and_fuel = Integ(
    lambda: increase_of_intensity_due_to_energy_a_technology_change_top_down()
    + inertial_rate_energy_intensity_top_down()
    + rate_change_intensity_bottom_up()
    - decrease_of_intensity_due_to_energy_a_technology_change_top_down(),
    lambda: initial_energy_intensity_1995()
    .loc[_subscript_dict["sectors"], :]
    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
    "_integ_evol_final_energy_intensity_by_sector_and_fuel",
)


@component.add(
    name="exp_rapid_evol_change_energy",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exp_rapid_evol_change_energy():
    """
    Parameter that define the speed of application of policies in the rapid way.
    """
    return 1 / 2


@component.add(
    name="exp_rapid_evol_improve_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exp_rapid_evol_improve_efficiency():
    """
    Parameter that define the speed of application of policies in the rapid way.
    """
    return 1 / 2


@component.add(
    name="exp_slow_evol_change_energy",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exp_slow_evol_change_energy():
    """
    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


@component.add(
    name="exp_slow_evol_improve_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def exp_slow_evol_improve_efficiency():
    """
    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


@component.add(
    name="Final_energy_intensity_2020",
    units="EJ/Tdollars",
    subscripts=["final_sources", "sectors"],
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_final_energy_intensity_2020": 1},
    other_deps={
        "_sampleiftrue_final_energy_intensity_2020": {
            "initial": {"evol_final_energy_intensity_by_sector_and_fuel": 1},
            "step": {
                "time": 1,
                "year_energy_intensity_target": 1,
                "evol_final_energy_intensity_by_sector_and_fuel": 1,
            },
        }
    },
)
def final_energy_intensity_2020():
    """
    Energy intensity by sector and final source in 2009
    """
    return _sampleiftrue_final_energy_intensity_2020()


_sampleiftrue_final_energy_intensity_2020 = SampleIfTrue(
    lambda: xr.DataArray(
        time() < year_energy_intensity_target(),
        {
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    ),
    lambda: evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final_sources", "sectors"
    ),
    lambda: evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final_sources", "sectors"
    ),
    "_sampleiftrue_final_energy_intensity_2020",
)


@component.add(
    name="final_year_energy_intensity_target",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_final_year_energy_intensity_target"},
)
def final_year_energy_intensity_target():
    """
    Year defined by user in which the energy intensity targets are set.
    """
    return _ext_constant_final_year_energy_intensity_target()


_ext_constant_final_year_energy_intensity_target = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "final_year_energy_intensity_target",
    {},
    _root,
    {},
    "_ext_constant_final_year_energy_intensity_target",
)


@component.add(
    name="Fuel_scarcity_pressure",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_feedback_final_fuel_replacement_flag": 1,
        "perception_of_final_energy_scarcity": 1,
    },
)
def fuel_scarcity_pressure():
    """
    Pressure due significant variations in the fuel scarcity of each type of final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: perception_of_final_energy_scarcity(),
        lambda: xr.DataArray(
            0, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )


@component.add(
    name="Global_energy_intensity_by_sector",
    units="EJ/Tdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_by_sector_and_fuel": 1},
)
def global_energy_intensity_by_sector():
    """
    Global energy intensity of one sector considering the energy intensity of five final fuels.
    """
    return sum(
        evol_final_energy_intensity_by_sector_and_fuel().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name="historic_final_energy_intensity",
    units="EJ/Mdollars",
    subscripts=["final_sources", "SECTORS_and_HOUSEHOLDS"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_final_energy_intensity",
        "__lookup__": "_ext_lookup_historic_final_energy_intensity",
    },
)
def historic_final_energy_intensity(x, final_subs=None):
    """
    Historic final energy intensity, households + 14 sectors & final sources. US$1995.
    """
    return _ext_lookup_historic_final_energy_intensity(x, final_subs)


_ext_lookup_historic_final_energy_intensity = ExtLookup(
    r"../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_final_energy_intensity_electricity",
    {
        "final_sources": ["electricity"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
    _root,
    {
        "final_sources": _subscript_dict["final_sources"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
    "_ext_lookup_historic_final_energy_intensity",
)

_ext_lookup_historic_final_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_final_energy_intensity_heat",
    {
        "final_sources": ["heat"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_final_energy_intensity_liquids",
    {
        "final_sources": ["liquids"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_final_energy_intensity_gases",
    {
        "final_sources": ["gases"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_final_energy_intensity_solids",
    {
        "final_sources": ["solids"],
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
    },
)


@component.add(
    name="historic_mean_rate_energy_intensity",
    units="Dmnl/year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_historic_mean_rate_energy_intensity"},
)
def historic_mean_rate_energy_intensity():
    """
    Historical trend of sectors energy intensity by final source (OLS method).
    """
    return _ext_constant_historic_mean_rate_energy_intensity()


_ext_constant_historic_mean_rate_energy_intensity = ExtConstant(
    r"../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_electricity*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": ["electricity"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_historic_mean_rate_energy_intensity",
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_heat*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": ["heat"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_liquids*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": ["liquids"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_gases*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": ["gases"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    r"../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_solids*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": ["solids"],
    },
)


@component.add(
    name="historic_rate_final_energy_intensity",
    units="EJ/(year*T$)",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_final_energy_intensity": 2,
        "time_step": 2,
        "mdollar_per_tdollar": 1,
    },
)
def historic_rate_final_energy_intensity():
    """
    Historic variation of final energy intensity by final source (EXIOBASE data) ((historic_final_energy_intensity[final_sources,SECTORS_and_HOUSEHOLDS](Time+TIME_STE P)-historic_final_energy_intensity [final_sources,SECTORS_and_HOUSEHOLDS](Time))*Mdollar_per_Tdollar)/TIME_STE P
    """
    return (
        (
            (
                historic_final_energy_intensity(time())
                - historic_final_energy_intensity(time() - time_step())
            )
            * mdollar_per_tdollar()
        )
        / time_step()
    ).transpose("SECTORS_and_HOUSEHOLDS", "final_sources")


@component.add(
    name="Implementation_policy_to_change_final_energy",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "choose_final_sectoral_energy_intensities_evolution_method": 1,
        "year_policy_change_energy": 9,
        "year_to_finish_energy_intensity_policies": 5,
        "time": 5,
        "exp_slow_evol_change_energy": 1,
        "exp_rapid_evol_change_energy": 1,
        "policy_change_energy_speed": 3,
    },
)
def implementation_policy_to_change_final_energy():
    """
    Pressure due to energy policies, eg incentives for change the final energy
    """
    return if_then_else(
        np.logical_or(
            choose_final_sectoral_energy_intensities_evolution_method() != 2,
            np.logical_or(
                year_policy_change_energy() < 2015,
                np.logical_or(
                    year_policy_change_energy()
                    > year_to_finish_energy_intensity_policies(),
                    time() < year_policy_change_energy(),
                ),
            ),
        ),
        lambda: xr.DataArray(
            0,
            {
                "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
                "final_sources": _subscript_dict["final_sources"],
            },
            ["SECTORS_and_HOUSEHOLDS", "final_sources"],
        ),
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: xr.DataArray(
                1,
                {
                    "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
                    "final_sources": _subscript_dict["final_sources"],
                },
                ["SECTORS_and_HOUSEHOLDS", "final_sources"],
            ),
            lambda: if_then_else(
                policy_change_energy_speed() == 1,
                lambda: (
                    (time() - year_policy_change_energy())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_change_energy()
                    )
                )
                ** exp_rapid_evol_change_energy(),
                lambda: if_then_else(
                    policy_change_energy_speed() == 2,
                    lambda: (time() - year_policy_change_energy())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_change_energy()
                    ),
                    lambda: if_then_else(
                        policy_change_energy_speed() == 3,
                        lambda: (
                            (time() - year_policy_change_energy())
                            / (
                                year_to_finish_energy_intensity_policies()
                                - year_policy_change_energy()
                            )
                        )
                        ** exp_slow_evol_change_energy(),
                        lambda: xr.DataArray(
                            0,
                            {
                                "SECTORS_and_HOUSEHOLDS": _subscript_dict[
                                    "SECTORS_and_HOUSEHOLDS"
                                ],
                                "final_sources": _subscript_dict["final_sources"],
                            },
                            ["SECTORS_and_HOUSEHOLDS", "final_sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Implementation_policy_to_improve_energy_intensity_efficiency",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "choose_final_sectoral_energy_intensities_evolution_method": 1,
        "year_policy_to_improve_efficiency": 9,
        "year_to_finish_energy_intensity_policies": 5,
        "time": 5,
        "exp_rapid_evol_improve_efficiency": 1,
        "policy_to_improve_efficiency_speed": 3,
        "exp_slow_evol_improve_efficiency": 1,
    },
)
def implementation_policy_to_improve_energy_intensity_efficiency():
    """
    Pressure due to energy policies, eg incentives for energy efficiency,
    """
    return if_then_else(
        np.logical_or(
            choose_final_sectoral_energy_intensities_evolution_method() != 2,
            np.logical_or(
                year_policy_to_improve_efficiency() < 2015,
                np.logical_or(
                    year_policy_to_improve_efficiency()
                    > year_to_finish_energy_intensity_policies(),
                    time() < year_policy_to_improve_efficiency(),
                ),
            ),
        ),
        lambda: xr.DataArray(
            0,
            {
                "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
                "final_sources": _subscript_dict["final_sources"],
            },
            ["SECTORS_and_HOUSEHOLDS", "final_sources"],
        ),
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: xr.DataArray(
                1,
                {
                    "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
                    "final_sources": _subscript_dict["final_sources"],
                },
                ["SECTORS_and_HOUSEHOLDS", "final_sources"],
            ),
            lambda: if_then_else(
                policy_to_improve_efficiency_speed() == 1,
                lambda: (
                    (time() - year_policy_to_improve_efficiency())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_to_improve_efficiency()
                    )
                )
                ** exp_rapid_evol_improve_efficiency(),
                lambda: if_then_else(
                    policy_to_improve_efficiency_speed() == 2,
                    lambda: (time() - year_policy_to_improve_efficiency())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_to_improve_efficiency()
                    ),
                    lambda: if_then_else(
                        policy_to_improve_efficiency_speed() == 3,
                        lambda: (
                            (time() - year_policy_to_improve_efficiency())
                            / (
                                year_to_finish_energy_intensity_policies()
                                - year_policy_to_improve_efficiency()
                            )
                        )
                        ** exp_slow_evol_improve_efficiency(),
                        lambda: xr.DataArray(
                            0,
                            {
                                "SECTORS_and_HOUSEHOLDS": _subscript_dict[
                                    "SECTORS_and_HOUSEHOLDS"
                                ],
                                "final_sources": _subscript_dict["final_sources"],
                            },
                            ["SECTORS_and_HOUSEHOLDS", "final_sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Increase_of_intensity_due_to_energy_a_technology_change_TOP_DOWN",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"increase_of_intensity_due_to_energy_a_technology_eff": 1},
)
def increase_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    When in one economic sector, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the increase of (b).
    """
    return sum(
        increase_of_intensity_due_to_energy_a_technology_eff().rename(
            {"final_sources1": "final_sources", "final_sources": "final_sources1!"}
        ),
        dim=["final_sources1!"],
    )


@component.add(
    name="Increase_of_intensity_due_to_energy_a_technology_eff",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_rate_of_substitution": 2,
        "increase_of_intensity_due_to_energy_a_technology_net": 2,
    },
)
def increase_of_intensity_due_to_energy_a_technology_eff():
    """
    Increase of intensity due to change a energy technology by fuel
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename(
            {
                "SECTORS_and_HOUSEHOLDS": "sectors",
                "final_sources": "final_sources1",
                "final_sources1": "final_sources",
            }
        )
        == 0,
        lambda: increase_of_intensity_due_to_energy_a_technology_net(),
        lambda: increase_of_intensity_due_to_energy_a_technology_net()
        * efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename(
            {
                "SECTORS_and_HOUSEHOLDS": "sectors",
                "final_sources": "final_sources1",
                "final_sources1": "final_sources",
            }
        ),
    )


@component.add(
    name="Increase_of_intensity_due_to_energy_a_technology_net",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decrease_of_intensity_due_to_energy_a_technology_change_top_down": 1,
        "share_tech_change_fuel": 1,
    },
)
def increase_of_intensity_due_to_energy_a_technology_net():
    """
    Increase of intensity due to change a energy technology without considering efficieny rate of susbsitution by fuel
    """
    return (
        decrease_of_intensity_due_to_energy_a_technology_change_top_down()
        * share_tech_change_fuel().transpose(
            "sectors", "final_sources", "final_sources1"
        )
    ).transpose("sectors", "final_sources1", "final_sources")


@component.add(
    name="inertial_rate_energy_intensity_TOP_DOWN",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_rate_final_energy_intensity": 1,
        "choose_final_sectoral_energy_intensities_evolution_method": 2,
        "available_improvement_efficiency": 4,
        "evol_final_energy_intensity_by_sector_and_fuel": 4,
        "activate_bottom_up_method": 4,
        "variation_energy_intensity_target": 1,
        "year_energy_intensity_target": 1,
        "initial_energy_intensity_1995": 4,
        "historic_mean_rate_energy_intensity": 6,
        "efficiency_energy_acceleration": 12,
        "rate_change_intensity_bottom_up": 4,
    },
)
def inertial_rate_energy_intensity_top_down():
    """
    This variable models the variation of the energy intensity according to the historical trend and represents the variation of the technological energy efficiency in each economic sector for each type of energy. By default it will follow the historical trend but can be modified by policies or market conditions that accelerate change. IF THEN ELSE(Choose final sectoral energy intensities evolution method=3,IF THEN ELSE(Time<2019, historic rate final energy intensity[sectors,final sources],IF THEN ELSE(Time<2020,IF THEN ELSE(Activate BOTTOM UP method [sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources] +Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors],Initial energy intensity 1995 [sectors,final sources] *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[ sectors,final sources])),0), IF THEN ELSE (Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(Efficiency energy acceleration[sectors,final sources])*available improvement efficiency [sectors],Initial energy intensity 1995 [sectors,final sources] *(Efficiency energy acceleration[ sectors,final sources])),0)))+variation energy intensity TARGET[sectors,final sources],IF THEN ELSE(Time>2019, IF THEN ELSE(Activate BOTTOM UP method [sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources] +Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors],Initial energy intensity 1995 [sectors,final sources] *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[ sectors,final sources])),0), historic rate final energy intensity[sectors,final sources]))
    """
    return if_then_else(
        time() < 2019,
        lambda: historic_rate_final_energy_intensity()
        .loc[_subscript_dict["sectors"], :]
        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
        lambda: if_then_else(
            choose_final_sectoral_energy_intensities_evolution_method() == 1,
            lambda: if_then_else(
                np.logical_or(
                    (
                        activate_bottom_up_method()
                        .loc[_subscript_dict["sectors"]]
                        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        == 0
                    ),
                    rate_change_intensity_bottom_up() == 0,
                ),
                lambda: if_then_else(
                    efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                    < 0,
                    lambda: evol_final_energy_intensity_by_sector_and_fuel()
                    * efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                    * available_improvement_efficiency(),
                    lambda: initial_energy_intensity_1995()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                    * efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
                ),
                lambda: xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "final_sources": _subscript_dict["final_sources"],
                    },
                    ["sectors", "final_sources"],
                ),
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: if_then_else(
                    np.logical_or(
                        (
                            activate_bottom_up_method()
                            .loc[_subscript_dict["sectors"]]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            == 0
                        ),
                        rate_change_intensity_bottom_up() == 0,
                    ),
                    lambda: if_then_else(
                        historic_mean_rate_energy_intensity()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        + efficiency_energy_acceleration()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        < 0,
                        lambda: evol_final_energy_intensity_by_sector_and_fuel()
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        )
                        * available_improvement_efficiency(),
                        lambda: initial_energy_intensity_1995()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                        ),
                    ),
                    lambda: xr.DataArray(
                        0,
                        {
                            "sectors": _subscript_dict["sectors"],
                            "final_sources": _subscript_dict["final_sources"],
                        },
                        ["sectors", "final_sources"],
                    ),
                ),
                lambda: if_then_else(
                    choose_final_sectoral_energy_intensities_evolution_method() == 2,
                    lambda: if_then_else(
                        np.logical_or(
                            (
                                activate_bottom_up_method()
                                .loc[_subscript_dict["sectors"]]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                                == 0
                            ),
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * (
                                historic_mean_rate_energy_intensity()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                                + efficiency_energy_acceleration()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            )
                            * available_improvement_efficiency(),
                            lambda: initial_energy_intensity_1995()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            * (
                                historic_mean_rate_energy_intensity()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                                + efficiency_energy_acceleration()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            ),
                        ),
                        lambda: xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final_sources": _subscript_dict["final_sources"],
                            },
                            ["sectors", "final_sources"],
                        ),
                    ),
                    lambda: if_then_else(
                        np.logical_or(
                            (
                                activate_bottom_up_method()
                                .loc[_subscript_dict["sectors"]]
                                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                                == 0
                            ),
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            * available_improvement_efficiency(),
                            lambda: initial_energy_intensity_1995()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                            * efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"}),
                        )
                        + variation_energy_intensity_target(),
                        lambda: xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final_sources": _subscript_dict["final_sources"],
                            },
                            ["sectors", "final_sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Initial_energy_intensity_1995",
    units="EJ/Tdollars",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_final_energy_intensity": 1, "mdollar_per_tdollar": 1},
)
def initial_energy_intensity_1995():
    """
    Initial energy intensity by sector and fuel in 1995
    """
    return (historic_final_energy_intensity(1995) * mdollar_per_tdollar()).transpose(
        "SECTORS_and_HOUSEHOLDS", "final_sources"
    )


@component.add(
    name="Initial_global_energy_intensity_2009",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_final_energy_intensity": 1, "mdollar_per_tdollar": 1},
)
def initial_global_energy_intensity_2009():
    """
    Initial global energy intensity by sector 2009
    """
    return (
        sum(
            historic_final_energy_intensity(2009).rename(
                {"final_sources": "final_sources!"}
            ),
            dim=["final_sources!"],
        )
        * mdollar_per_tdollar()
    )


@component.add(
    name='"Inter-fuel_scarcity_pressure"',
    units="Dmnl",
    subscripts=["final_sources", "final_sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_feedback_final_fuel_replacement_flag": 1,
        "perception_of_interfuel_final_energy_scarcities": 1,
    },
)
def interfuel_scarcity_pressure():
    """
    Pressure due to variations in the inter-fuel scarcity of each final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: np.maximum(0, perception_of_interfuel_final_energy_scarcities()),
        lambda: xr.DataArray(
            0,
            {
                "final_sources": _subscript_dict["final_sources"],
                "final_sources1": _subscript_dict["final_sources1"],
            },
            ["final_sources", "final_sources1"],
        ),
    )


@component.add(
    name="max_yearly_change_between_sources",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_yearly_change_between_sources"},
)
def max_yearly_change_between_sources():
    """
    maximum annual change for one type of energy in a sector.
    """
    return _ext_constant_max_yearly_change_between_sources()


_ext_constant_max_yearly_change_between_sources = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "max_yearly_change_between_sources*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_max_yearly_change_between_sources",
)


@component.add(
    name="Maximum_yearly_acceleration_of_intensity_improvement",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_maximum_yearly_acceleration_of_intensity_improvement"
    },
)
def maximum_yearly_acceleration_of_intensity_improvement():
    """
    Maximum feasible annual changes that could be sustained in the future in the energy intensity of each economic sector have been estimated based on the observation of trends and historical changes in the available data.
    """
    return _ext_constant_maximum_yearly_acceleration_of_intensity_improvement()


_ext_constant_maximum_yearly_acceleration_of_intensity_improvement = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "maximum_yearly_acceleration_of_intensity_improvement*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_maximum_yearly_acceleration_of_intensity_improvement",
)


@component.add(
    name="Mdollar_per_Tdollar",
    units="Mdollar/Tdollar",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mdollar_per_tdollar():
    """
    Million dollars per Tdollar (1 T$ = 1e6 M$).
    """
    return 1000000.0


@component.add(
    name="min_energy_intensity_vs_intial",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_min_energy_intensity_vs_intial"},
)
def min_energy_intensity_vs_intial():
    """
    Minimum value that the energy intensity for each economic sector could reach, obviously always above zero. This minimum value is very difficult to estimate, but based on historical values it has been considered that it can reach 30% of the value of 2009. (Capellán-Pérez et al., 2014)
    """
    return _ext_constant_min_energy_intensity_vs_intial()


_ext_constant_min_energy_intensity_vs_intial = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "min_FEI_vs_initial",
    {},
    _root,
    {},
    "_ext_constant_min_energy_intensity_vs_intial",
)


@component.add(
    name="minimum_fraction_source",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_minimum_fraction_source"},
)
def minimum_fraction_source():
    """
    minimum energy of each type of energy that should be used in each sector because it is irreplaceable
    """
    return _ext_constant_minimum_fraction_source()


_ext_constant_minimum_fraction_source = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "minimum_fraction_source*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_minimum_fraction_source",
)


@component.add(
    name="Policy_change_energy_speed",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_policy_change_energy_speed"},
)
def policy_change_energy_speed():
    """
    Selection of the speed of application of the different policies to change the final energy
    """
    return _ext_constant_policy_change_energy_speed()


_ext_constant_policy_change_energy_speed = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "policy_change_energy_speed*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_policy_change_energy_speed",
)


@component.add(
    name="Policy_to_improve_efficiency_speed",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_policy_to_improve_efficiency_speed"},
)
def policy_to_improve_efficiency_speed():
    """
    Selection of the speed of application of the different policies to improve the efficiency.
    """
    return _ext_constant_policy_to_improve_efficiency_speed()


_ext_constant_policy_to_improve_efficiency_speed = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "policy_to_improve_efficiency_speed*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_policy_to_improve_efficiency_speed",
)


@component.add(
    name="Pressure_to_change_energy_technology",
    units="Dmnl",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_to_change_energy_technology_by_fuel": 1},
)
def pressure_to_change_energy_technology():
    """
    This variable represents the pressure in one sector for substituting a final energy source for all the other energies.
    """
    return np.minimum(
        1,
        sum(
            pressure_to_change_energy_technology_by_fuel().rename(
                {"final_sources": "final_sources1!", "final_sources1": "final_sources"}
            ),
            dim=["final_sources1!"],
        ),
    )


@component.add(
    name="Pressure_to_change_energy_technology_by_fuel",
    units="Dmnl",
    subscripts=["sectors", "final_sources", "final_sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_rate_of_substitution": 1,
        "interfuel_scarcity_pressure": 2,
        "implementation_policy_to_change_final_energy": 1,
    },
)
def pressure_to_change_energy_technology_by_fuel():
    """
    This variable represents the pressure in each economic sector for substituting a final energy source for another. This change depending on the sectors will have different technological difficulty and different cost. This pressure may be due to (1) energy policies, eg substitution of fossil fuels for electrical energy, or (2) by variations in the scarcity of each type of final energy.
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
        == 0,
        lambda: np.minimum(np.maximum(interfuel_scarcity_pressure(), 0), 1).expand_dims(
            {"sectors": _subscript_dict["sectors"]}, 0
        ),
        lambda: np.minimum(
            np.maximum(
                interfuel_scarcity_pressure()
                + implementation_policy_to_change_final_energy()
                .loc[_subscript_dict["sectors"], :]
                .rename(
                    {
                        "SECTORS_and_HOUSEHOLDS": "sectors",
                        "final_sources": "final_sources1",
                    }
                )
                .transpose("final_sources1", "sectors"),
                0,
            ),
            1,
        ).transpose("sectors", "final_sources", "final_sources1"),
    )


@component.add(
    name="Pressure_to_improve_energy_intensity_efficiency",
    units="Dmnl",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fuel_scarcity_pressure": 1,
        "implementation_policy_to_improve_energy_intensity_efficiency": 1,
    },
)
def pressure_to_improve_energy_intensity_efficiency():
    """
    This variable represents the pressure in each economic sector to improve energy efficiency in the technology used. This change according to the sectors will have different technological difficulty and different cost. This pressure may be due to (1) energy policies, eg incentives for energy efficiency, or (2) significant variations in the scarcity of each type of final energy.
    """
    return np.minimum(
        1,
        fuel_scarcity_pressure()
        + implementation_policy_to_improve_energy_intensity_efficiency().transpose(
            "final_sources", "SECTORS_and_HOUSEHOLDS"
        ),
    ).transpose("SECTORS_and_HOUSEHOLDS", "final_sources")


@component.add(
    name="rate_change_intensity_BOTTOM_UP",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_bottom_up_method": 1,
        "energy_intensity_commercial_transport_variation": 1,
    },
)
def rate_change_intensity_bottom_up():
    """
    Variation of the energy intensity of inland transport in BOTTOM UP method
    """
    return if_then_else(
        (
            activate_bottom_up_method()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            == 1
        ).expand_dims({"final_sources": _subscript_dict["final_sources"]}, 1),
        lambda: energy_intensity_commercial_transport_variation().expand_dims(
            {"sectors": _subscript_dict["sectors"]}, 0
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final_sources": _subscript_dict["final_sources"],
            },
            ["sectors", "final_sources"],
        ),
    )


@component.add(
    name="scarcity_feedback_final_fuel_replacement_flag",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_scarcity_feedback_final_fuel_replacement_flag"
    },
)
def scarcity_feedback_final_fuel_replacement_flag():
    """
    Switch to (de)activate the scarcity feedback fuel replacement.
    """
    return _ext_constant_scarcity_feedback_final_fuel_replacement_flag()


_ext_constant_scarcity_feedback_final_fuel_replacement_flag = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "scarcity_feedback_final_fuel_replacement_flag",
    {},
    _root,
    {},
    "_ext_constant_scarcity_feedback_final_fuel_replacement_flag",
)


@component.add(
    name="share_tech_change_fuel",
    units="Dmnl",
    subscripts=["sectors", "final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_to_change_energy_technology_by_fuel": 2},
)
def share_tech_change_fuel():
    """
    Share of the global pressure to change energy technology that corresponds to each fuel.
    """
    return zidz(
        pressure_to_change_energy_technology_by_fuel().rename(
            {"final_sources": "final_sources1", "final_sources1": "final_sources"}
        ),
        sum(
            pressure_to_change_energy_technology_by_fuel().rename(
                {"final_sources": "final_sources1!", "final_sources1": "final_sources"}
            ),
            dim=["final_sources1!"],
        ).expand_dims({"final_sources1": _subscript_dict["final_sources1"]}, 1),
    )


@component.add(
    name="variation_energy_intensity_TARGET",
    units="EJ/(year*Tdollars)",
    subscripts=["sectors", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "choose_energy_intensity_target_method": 1,
        "energy_intensity_target": 1,
        "time": 6,
        "year_energy_intensity_target": 2,
        "evol_final_energy_intensity_by_sector_and_fuel": 2,
        "final_year_energy_intensity_target": 4,
        "final_energy_intensity_2020": 1,
        "pct_change_energy_intensity_target": 1,
    },
)
def variation_energy_intensity_target():
    """
    Variation in energy intensity by sector and final energy defined by user targets.
    """
    return if_then_else(
        choose_energy_intensity_target_method() == 1,
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final_sources": _subscript_dict["final_sources"],
                },
                ["sectors", "final_sources"],
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "final_sources": _subscript_dict["final_sources"],
                    },
                    ["sectors", "final_sources"],
                ),
                lambda: (
                    energy_intensity_target()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                    - evol_final_energy_intensity_by_sector_and_fuel()
                )
                / (final_year_energy_intensity_target() - time()),
            ),
        ),
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: xr.DataArray(
                0,
                {
                    "final_sources": _subscript_dict["final_sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final_sources", "sectors"],
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {
                        "final_sources": _subscript_dict["final_sources"],
                        "sectors": _subscript_dict["sectors"],
                    },
                    ["final_sources", "sectors"],
                ),
                lambda: (
                    final_energy_intensity_2020()
                    * (1 + pct_change_energy_intensity_target())
                    - evol_final_energy_intensity_by_sector_and_fuel().transpose(
                        "final_sources", "sectors"
                    )
                )
                / (final_year_energy_intensity_target() - time()),
            ),
        ).transpose("sectors", "final_sources"),
    )


@component.add(
    name="Year_policy_change_energy",
    units="year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_year_policy_change_energy"},
)
def year_policy_change_energy():
    """
    Year when the policy to change final energy in the sectors start. For each of five final energies.
    """
    return _ext_constant_year_policy_change_energy()


_ext_constant_year_policy_change_energy = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_policy_change_energy*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_year_policy_change_energy",
)


@component.add(
    name="Year_policy_to_improve_efficiency",
    units="year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_year_policy_to_improve_efficiency"},
)
def year_policy_to_improve_efficiency():
    """
    Year when the policy to improve efficiency in sectors start. For each of five final energies.
    """
    return _ext_constant_year_policy_to_improve_efficiency()


_ext_constant_year_policy_to_improve_efficiency = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_policy_to_improve_efficiency*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_year_policy_to_improve_efficiency",
)


@component.add(
    name="Year_to_finish_energy_intensity_policies",
    units="year",
    subscripts=["SECTORS_and_HOUSEHOLDS", "final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_year_to_finish_energy_intensity_policies"
    },
)
def year_to_finish_energy_intensity_policies():
    """
    Year when the policy to improve efficiency in sectors finish.
    """
    return _ext_constant_year_to_finish_energy_intensity_policies()


_ext_constant_year_to_finish_energy_intensity_policies = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_to_finish_energy_intensity_policies*",
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    _root,
    {
        "SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"],
        "final_sources": _subscript_dict["final_sources"],
    },
    "_ext_constant_year_to_finish_energy_intensity_policies",
)


@component.add(
    name="Year_to_finish_policy_change_energy",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_to_finish_policy_change_energy():
    """
    Year when the policy to change final energy in the sectors finish.
    """
    return 2050
