"""
Module fe_intensity_sectors
Translated using PySD version 2.2.1
"""


@subs(["SECTORS and HOUSEHOLDS"], _subscript_dict)
def activate_bottom_up_method():
    """
    Real Name: Activate BOTTOM UP method
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS']

    Activate BOTTOM UP method or maintain TOP DOWN method. Activate for each sector (by default, only inland transport sector) 0. Bottom-up NOT activated 1. Bottom-up activated
    """
    return xr.DataArray(
        0,
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        ["SECTORS and HOUSEHOLDS"],
    )


@subs(["sectors"], _subscript_dict)
def available_improvement_efficiency():
    """
    Real Name: available improvement efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

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
                .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
                (1 - min_energy_intensity_vs_intial())
                * initial_global_energy_intensity_2009()
                .loc[_subscript_dict["sectors"]]
                .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
            ),
            lambda: xr.DataArray(
                1, {"sectors": _subscript_dict["sectors"]}, ["sectors"]
            ),
        ),
    )


def choose_final_sectoral_energy_intensities_evolution_method():
    """
    Real Name: Choose final sectoral energy intensities evolution method
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0- Dynamic evolution with policies and feedback of final fuel scarcity 1- Constant at 2009 levels 2- Sectoral energy intensity targets defined by user
    """
    return _ext_constant_choose_final_sectoral_energy_intensities_evolution_method()


_ext_constant_choose_final_sectoral_energy_intensities_evolution_method = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "sectoral_FEI_evolution_method",
    {},
    _root,
    "_ext_constant_choose_final_sectoral_energy_intensities_evolution_method",
)


@subs(["sectors", "final sources"], _subscript_dict)
def decrease_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    Real Name: Decrease of intensity due to energy a technology change TOP DOWN
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

    When in one economic sector, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the decrease of (a).
    """
    return if_then_else(
        (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + activate_bottom_up_method()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
            == 0
        ),
        lambda: if_then_else(
            zidz(
                evol_final_energy_intensity_by_sector_and_fuel(),
                (
                    xr.DataArray(
                        0,
                        {
                            "sectors": _subscript_dict["sectors"],
                            "final sources": _subscript_dict["final sources"],
                        },
                        ["sectors", "final sources"],
                    )
                    + global_energy_intensity_by_sector()
                ),
            )
            >= minimum_fraction_source()
            .loc[_subscript_dict["sectors"], :]
            .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
            lambda: (
                max_yearly_change_between_sources()
                .loc[_subscript_dict["sectors"], :]
                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
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
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            ),
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final sources": _subscript_dict["final sources"],
            },
            ["sectors", "final sources"],
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def efficiency_energy_acceleration():
    """
    Real Name: Efficiency energy acceleration
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

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


@subs(["SECTORS and HOUSEHOLDS", "final sources", "final sources1"], _subscript_dict)
def efficiency_rate_of_substitution():
    """
    Real Name: efficiency rate of substitution
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources', 'final sources1']

    It is necessary to take into account that the energy efficiencies of the two technologies exchanged do not necessarily have to be the same. In other words, a decrease in the energy intensity of (a) will not imply the same increase in the energy intensity of (b). This possible difference is compensated through the parameter “Efficiency rate of substitution”.
    """
    return _ext_constant_efficiency_rate_of_substitution()


_ext_constant_efficiency_rate_of_substitution = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_electricity*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["electricity"],
    },
    _root,
    "_ext_constant_efficiency_rate_of_substitution",
)

_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_heat*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["heat"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_liquids*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["liquids"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_gases*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["gases"],
    },
)

_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_solids*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["solids"],
    },
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def energy_intensity_target():
    """
    Real Name: Energy intensity target
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Energy intensity targets by sector and final energy defined by user
    """
    return energy_intensity_target_mdollar() * mdollar_per_tdollar()


@subs(["sectors", "final sources"], _subscript_dict)
def evol_final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Evol final energy intensity by sector and fuel
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors', 'final sources']

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
    .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
    "_integ_evol_final_energy_intensity_by_sector_and_fuel",
)


def exp_rapid_evol_change_energy():
    """
    Real Name: exp rapid evol change energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Parameter that define the speed of application of policies in the rapid way.
    """
    return 1 / 2


def exp_rapid_evol_improve_efficiency():
    """
    Real Name: exp rapid evol improve efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Parameter that define the speed of application of policies in the rapid way.
    """
    return 1 / 2


def exp_slow_evol_change_energy():
    """
    Real Name: exp slow evol change energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


def exp_slow_evol_improve_efficiency():
    """
    Real Name: exp slow evol improve efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_2020():
    """
    Real Name: Final energy intensity 2020
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources', 'sectors']

    Energy intensity by sector and final source in 2009
    """
    return _sampleiftrue_final_energy_intensity_2020()


_sampleiftrue_final_energy_intensity_2020 = SampleIfTrue(
    lambda: xr.DataArray(
        time() < year_energy_intensity_target(),
        {
            "final sources": _subscript_dict["final sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final sources", "sectors"],
    ),
    lambda: (
        xr.DataArray(
            0,
            {
                "final sources": _subscript_dict["final sources"],
                "sectors": _subscript_dict["sectors"],
            },
            ["final sources", "sectors"],
        )
        + evol_final_energy_intensity_by_sector_and_fuel()
    ),
    lambda: (
        xr.DataArray(
            0,
            {
                "final sources": _subscript_dict["final sources"],
                "sectors": _subscript_dict["sectors"],
            },
            ["final sources", "sectors"],
        )
        + evol_final_energy_intensity_by_sector_and_fuel()
    ),
    "_sampleiftrue_final_energy_intensity_2020",
)


@subs(["final sources"], _subscript_dict)
def fuel_scarcity_pressure():
    """
    Real Name: Fuel scarcity pressure
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Pressure due significant variations in the fuel scarcity of each type of final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: perception_of_final_energy_scarcity(),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def energy_intensity_target_mdollar():
    """
    Real Name: energy intensity target Mdollar
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Energy intensity targets by sector and final energy defined by user
    """
    return _ext_constant_energy_intensity_target_mdollar()


_ext_constant_energy_intensity_target_mdollar = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "energy_intensity_target*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_energy_intensity_target_mdollar",
)


def final_year_energy_intensity_target():
    """
    Real Name: final year energy intensity target
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year defined by user in which the energy intensity targets are set.
    """
    return _ext_constant_final_year_energy_intensity_target()


_ext_constant_final_year_energy_intensity_target = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "final_year_energy_intensity_target",
    {},
    _root,
    "_ext_constant_final_year_energy_intensity_target",
)


@subs(["sectors"], _subscript_dict)
def global_energy_intensity_by_sector():
    """
    Real Name: Global energy intensity by sector
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Global energy intensity of one sector considering the energy intensity of five final fuels.
    """
    return sum(
        evol_final_energy_intensity_by_sector_and_fuel().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@subs(["final sources", "SECTORS and HOUSEHOLDS"], _subscript_dict)
def historic_final_energy_intensity(x):
    """
    Real Name: historic final energy intensity
    Original Eqn:
    Units: EJ/Mdollars
    Limits: (None, None)
    Type: Lookup
    Subs: ['final sources', 'SECTORS and HOUSEHOLDS']

    Historic final energy intensity, households + 14 sectors & final sources. US$1995.
    """
    return _ext_lookup_historic_final_energy_intensity(x)


_ext_lookup_historic_final_energy_intensity = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_electricity",
    {
        "final sources": ["electricity"],
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
    },
    _root,
    "_ext_lookup_historic_final_energy_intensity",
)

_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_heat",
    {
        "final sources": ["heat"],
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_liquids",
    {
        "final sources": ["liquids"],
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_gases",
    {
        "final sources": ["gases"],
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
    },
)

_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_solids",
    {
        "final sources": ["solids"],
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
    },
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def historic_mean_rate_energy_intensity():
    """
    Real Name: historic mean rate energy intensity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Historical trend of sectors energy intensity by final source (OLS method).
    """
    return _ext_constant_historic_mean_rate_energy_intensity()


_ext_constant_historic_mean_rate_energy_intensity = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_electricity*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": ["electricity"],
    },
    _root,
    "_ext_constant_historic_mean_rate_energy_intensity",
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_heat*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": ["heat"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_liquids*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": ["liquids"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_gases*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": ["gases"],
    },
)

_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_solids*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": ["solids"],
    },
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def historic_rate_final_energy_intensity():
    """
    Real Name: historic rate final energy intensity
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Historic variation of final energy intensity by final source (WIOD data)
    """
    return (
        xr.DataArray(
            0,
            {
                "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                "final sources": _subscript_dict["final sources"],
            },
            ["SECTORS and HOUSEHOLDS", "final sources"],
        )
        + (
            historic_final_energy_intensity(integer(time() + 1))
            - historic_final_energy_intensity(integer(time()))
        )
        * mdollar_per_tdollar()
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def implementation_policy_to_change_final_energy():
    """
    Real Name: Implementation policy to change final energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

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
                "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                "final sources": _subscript_dict["final sources"],
            },
            ["SECTORS and HOUSEHOLDS", "final sources"],
        ),
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: xr.DataArray(
                1,
                {
                    "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["SECTORS and HOUSEHOLDS", "final sources"],
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
                                "SECTORS and HOUSEHOLDS": _subscript_dict[
                                    "SECTORS and HOUSEHOLDS"
                                ],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["SECTORS and HOUSEHOLDS", "final sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def implementation_policy_to_improve_energy_intensity_efficiency():
    """
    Real Name: Implementation policy to improve energy intensity efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

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
                "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                "final sources": _subscript_dict["final sources"],
            },
            ["SECTORS and HOUSEHOLDS", "final sources"],
        ),
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: xr.DataArray(
                1,
                {
                    "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["SECTORS and HOUSEHOLDS", "final sources"],
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
                                "SECTORS and HOUSEHOLDS": _subscript_dict[
                                    "SECTORS and HOUSEHOLDS"
                                ],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["SECTORS and HOUSEHOLDS", "final sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    Real Name: Increase of intensity due to energy a technology change TOP DOWN
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

    When in one economic sector, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the increase of (b).
    """
    return sum(
        increase_of_intensity_due_to_energy_a_technology_eff().rename(
            {"final sources1": "final sources", "final sources": "final sources1!"}
        ),
        dim=["final sources1!"],
    )


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_eff():
    """
    Real Name: Increase of intensity due to energy a technology eff
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources1', 'final sources']

    Increase of intensity due to change a energy technology by fuel
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename(
            {
                "SECTORS and HOUSEHOLDS": "sectors",
                "final sources": "final sources1",
                "final sources1": "final sources",
            }
        )
        == 0,
        lambda: increase_of_intensity_due_to_energy_a_technology_net(),
        lambda: increase_of_intensity_due_to_energy_a_technology_net()
        * efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename(
            {
                "SECTORS and HOUSEHOLDS": "sectors",
                "final sources": "final sources1",
                "final sources1": "final sources",
            }
        ),
    )


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_net():
    """
    Real Name: Increase of intensity due to energy a technology net
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources1', 'final sources']

    Increase of intensity due to change a energy technology without considering efficieny rate of susbsitution by fuel
    """
    return xr.DataArray(
        0,
        {
            "sectors": _subscript_dict["sectors"],
            "final sources1": _subscript_dict["final sources1"],
            "final sources": _subscript_dict["final sources"],
        },
        ["sectors", "final sources1", "final sources"],
    ) + (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final sources": _subscript_dict["final sources"],
                "final sources1": _subscript_dict["final sources1"],
            },
            ["sectors", "final sources", "final sources1"],
        )
        + decrease_of_intensity_due_to_energy_a_technology_change_top_down()
    ) * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final sources": _subscript_dict["final sources"],
                "final sources1": _subscript_dict["final sources1"],
            },
            ["sectors", "final sources", "final sources1"],
        )
        + share_tech_change_fuel()
    )


@subs(["sectors", "final sources"], _subscript_dict)
def inertial_rate_energy_intensity_top_down():
    """
    Real Name: inertial rate energy intensity TOP DOWN
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

    This variable models the variation of the energy intensity according to the historical trend and represents the variation of the technological energy efficiency in each economic sector for each type of energy. By default it will follow the historical trend but can be modified by policies or market conditions that accelerate change. IF THEN ELSE(Choose final sectoral energy intensities evolution method=3,IF THEN ELSE(Time<2009, historic rate final energy intensity[sectors,final sources],IF THEN ELSE(Time<2020,IF THEN ELSE(Activate BOTTOM UP method [sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources] +Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors],Initial energy intensity 1995 [sectors,final sources] *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[ sectors,final sources])),0), IF THEN ELSE (Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(Efficiency energy acceleration[sectors,final sources])*available improvement efficiency [sectors],Initial energy intensity 1995 [sectors,final sources] *(Efficiency energy acceleration[ sectors,final sources])),0)))+variation energy intensity TARGET[sectors,final sources],IF THEN ELSE(Time>2009, IF THEN ELSE(Activate BOTTOM UP method [sectors]=0:OR:rate change intensity BOTTOM UP[ sectors,final sources]=0, IF THEN ELSE((historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration [sectors,final sources])<0,Evol final energy intensity by sector and fuel [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources] +Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors],Initial energy intensity 1995 [sectors,final sources] *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[ sectors,final sources])),0), historic rate final energy intensity[sectors,final sources]))
    """
    return if_then_else(
        time() < 2009,
        lambda: historic_rate_final_energy_intensity()
        .loc[_subscript_dict["sectors"], :]
        .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
        lambda: if_then_else(
            choose_final_sectoral_energy_intensities_evolution_method() == 1,
            lambda: if_then_else(
                np.logical_or(
                    (
                        xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["sectors", "final sources"],
                        )
                        + activate_bottom_up_method()
                        .loc[_subscript_dict["sectors"]]
                        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        == 0
                    ),
                    rate_change_intensity_bottom_up() == 0,
                ),
                lambda: if_then_else(
                    efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                    < 0,
                    lambda: evol_final_energy_intensity_by_sector_and_fuel()
                    * efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                    * (
                        xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["sectors", "final sources"],
                        )
                        + available_improvement_efficiency()
                    ),
                    lambda: initial_energy_intensity_1995()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                    * efficiency_energy_acceleration()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
                ),
                lambda: xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["sectors", "final sources"],
                ),
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: if_then_else(
                    np.logical_or(
                        (
                            xr.DataArray(
                                0,
                                {
                                    "sectors": _subscript_dict["sectors"],
                                    "final sources": _subscript_dict["final sources"],
                                },
                                ["sectors", "final sources"],
                            )
                            + activate_bottom_up_method()
                            .loc[_subscript_dict["sectors"]]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            == 0
                        ),
                        rate_change_intensity_bottom_up() == 0,
                    ),
                    lambda: if_then_else(
                        historic_mean_rate_energy_intensity()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        + efficiency_energy_acceleration()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        < 0,
                        lambda: evol_final_energy_intensity_by_sector_and_fuel()
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        )
                        * (
                            xr.DataArray(
                                0,
                                {
                                    "sectors": _subscript_dict["sectors"],
                                    "final sources": _subscript_dict["final sources"],
                                },
                                ["sectors", "final sources"],
                            )
                            + available_improvement_efficiency()
                        ),
                        lambda: initial_energy_intensity_1995()
                        .loc[_subscript_dict["sectors"], :]
                        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                        ),
                    ),
                    lambda: xr.DataArray(
                        0,
                        {
                            "sectors": _subscript_dict["sectors"],
                            "final sources": _subscript_dict["final sources"],
                        },
                        ["sectors", "final sources"],
                    ),
                ),
                lambda: if_then_else(
                    choose_final_sectoral_energy_intensities_evolution_method() == 2,
                    lambda: if_then_else(
                        np.logical_or(
                            (
                                xr.DataArray(
                                    0,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "final sources": _subscript_dict[
                                            "final sources"
                                        ],
                                    },
                                    ["sectors", "final sources"],
                                )
                                + activate_bottom_up_method()
                                .loc[_subscript_dict["sectors"]]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                                == 0
                            ),
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            historic_mean_rate_energy_intensity()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            + efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * (
                                historic_mean_rate_energy_intensity()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                                + efficiency_energy_acceleration()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            )
                            * (
                                xr.DataArray(
                                    0,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "final sources": _subscript_dict[
                                            "final sources"
                                        ],
                                    },
                                    ["sectors", "final sources"],
                                )
                                + available_improvement_efficiency()
                            ),
                            lambda: initial_energy_intensity_1995()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            * (
                                historic_mean_rate_energy_intensity()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                                + efficiency_energy_acceleration()
                                .loc[_subscript_dict["sectors"], :]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            ),
                        ),
                        lambda: xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["sectors", "final sources"],
                        ),
                    ),
                    lambda: if_then_else(
                        np.logical_or(
                            (
                                xr.DataArray(
                                    0,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "final sources": _subscript_dict[
                                            "final sources"
                                        ],
                                    },
                                    ["sectors", "final sources"],
                                )
                                + activate_bottom_up_method()
                                .loc[_subscript_dict["sectors"]]
                                .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                                == 0
                            ),
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            * (
                                xr.DataArray(
                                    0,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "final sources": _subscript_dict[
                                            "final sources"
                                        ],
                                    },
                                    ["sectors", "final sources"],
                                )
                                + available_improvement_efficiency()
                            ),
                            lambda: initial_energy_intensity_1995()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                            * efficiency_energy_acceleration()
                            .loc[_subscript_dict["sectors"], :]
                            .rename({"SECTORS and HOUSEHOLDS": "sectors"}),
                        )
                        + variation_energy_intensity_target(),
                        lambda: xr.DataArray(
                            0,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "final sources": _subscript_dict["final sources"],
                            },
                            ["sectors", "final sources"],
                        ),
                    ),
                ),
            ),
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def initial_energy_intensity_1995():
    """
    Real Name: Initial energy intensity 1995
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Initial energy intensity by sector and fuel in 1995
    """
    return (
        xr.DataArray(
            0,
            {
                "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                "final sources": _subscript_dict["final sources"],
            },
            ["SECTORS and HOUSEHOLDS", "final sources"],
        )
        + historic_final_energy_intensity(1995) * mdollar_per_tdollar()
    )


@subs(["SECTORS and HOUSEHOLDS"], _subscript_dict)
def initial_global_energy_intensity_2009():
    """
    Real Name: Initial global energy intensity 2009
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS']

    Initial global energy intensity by sector 2009
    """
    return (
        sum(
            historic_final_energy_intensity(2009).rename(
                {"final sources": "final sources!"}
            ),
            dim=["final sources!"],
        )
        * mdollar_per_tdollar()
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def interfuel_scarcity_pressure():
    """
    Real Name: "Inter-fuel scarcity pressure"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'final sources1']

    Pressure due to variations in the inter-fuel scarcity of each final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: np.maximum(0, perception_of_interfuel_final_energy_scarcities()),
        lambda: xr.DataArray(
            0,
            {
                "final sources": _subscript_dict["final sources"],
                "final sources1": _subscript_dict["final sources1"],
            },
            ["final sources", "final sources1"],
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def max_yearly_change_between_sources():
    """
    Real Name: max yearly change between sources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    maximum annual change for one type of energy in a sector.
    """
    return _ext_constant_max_yearly_change_between_sources()


_ext_constant_max_yearly_change_between_sources = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_yearly_change_between_sources*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_max_yearly_change_between_sources",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def maximum_yearly_acceleration_of_intensity_improvement():
    """
    Real Name: Maximum yearly acceleration of intensity improvement
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Maximum feasible annual changes that could be sustained in the future in the energy intensity of each economic sector have been estimated based on the observation of trends and historical changes in the available data.
    """
    return _ext_constant_maximum_yearly_acceleration_of_intensity_improvement()


_ext_constant_maximum_yearly_acceleration_of_intensity_improvement = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "maximum_yearly_acceleration_of_intensity_improvement*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_maximum_yearly_acceleration_of_intensity_improvement",
)


def mdollar_per_tdollar():
    """
    Real Name: Mdollar per Tdollar
    Original Eqn:
    Units: Mdollar/Tdollar
    Limits: (None, None)
    Type: Constant
    Subs: []

    Million dollars per Tdollar (1 T$ = 1e6 M$).
    """
    return 1000000.0


def min_energy_intensity_vs_intial():
    """
    Real Name: min energy intensity vs intial
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Minimum value that the energy intensity for each economic sector could reach, obviously always above zero. This minimum value is very difficult to estimate, but based on historical values it has been considered that it can reach 30% of the value of 2009. (Capellán-Pérez et al., 2014)
    """
    return _ext_constant_min_energy_intensity_vs_intial()


_ext_constant_min_energy_intensity_vs_intial = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "min_FEI_vs_initial",
    {},
    _root,
    "_ext_constant_min_energy_intensity_vs_intial",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def minimum_fraction_source():
    """
    Real Name: minimum fraction source
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    minimum energy of each type of energy that should be used in each sector because it is irreplaceable
    """
    return _ext_constant_minimum_fraction_source()


_ext_constant_minimum_fraction_source = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "minimum_fraction_source*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_minimum_fraction_source",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def policy_change_energy_speed():
    """
    Real Name: Policy change energy speed
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Selection of the speed of application of the different policies to change the final energy
    """
    return _ext_constant_policy_change_energy_speed()


_ext_constant_policy_change_energy_speed = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "policy_change_energy_speed*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_policy_change_energy_speed",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def policy_to_improve_efficiency_speed():
    """
    Real Name: Policy to improve efficiency speed
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Selection of the speed of application of the different policies to improve the efficiency.
    """
    return _ext_constant_policy_to_improve_efficiency_speed()


_ext_constant_policy_to_improve_efficiency_speed = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "policy_to_improve_efficiency_speed*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_policy_to_improve_efficiency_speed",
)


@subs(["sectors", "final sources"], _subscript_dict)
def pressure_to_change_energy_technology():
    """
    Real Name: Pressure to change energy technology
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

    This variable represents the pressure in one sector for substituting a final energy source for all the other energies.
    """
    return np.minimum(
        1,
        sum(
            pressure_to_change_energy_technology_by_fuel().rename(
                {"final sources": "final sources1!", "final sources1": "final sources"}
            ),
            dim=["final sources1!"],
        ),
    )


@subs(["sectors", "final sources", "final sources1"], _subscript_dict)
def pressure_to_change_energy_technology_by_fuel():
    """
    Real Name: Pressure to change energy technology by fuel
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources', 'final sources1']

    This variable represents the pressure in each economic sector for substituting a final energy source for another. This change depending on the sectors will have different technological difficulty and different cost. This pressure may be due to (1) energy policies, eg substitution of fossil fuels for electrical energy, or (2) by variations in the scarcity of each type of final energy.
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc[_subscript_dict["sectors"], :, :]
        .rename({"SECTORS and HOUSEHOLDS": "sectors"})
        == 0,
        lambda: (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                    "final sources1": _subscript_dict["final sources1"],
                },
                ["sectors", "final sources", "final sources1"],
            )
            + np.minimum(np.maximum(interfuel_scarcity_pressure(), 0), 1)
        ),
        lambda: (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                    "final sources1": _subscript_dict["final sources1"],
                },
                ["sectors", "final sources", "final sources1"],
            )
            + np.minimum(
                np.maximum(
                    (
                        xr.DataArray(
                            0,
                            {
                                "final sources": _subscript_dict["final sources"],
                                "final sources1": _subscript_dict["final sources1"],
                                "sectors": _subscript_dict["sectors"],
                            },
                            ["final sources", "final sources1", "sectors"],
                        )
                        + interfuel_scarcity_pressure()
                    )
                    + (
                        xr.DataArray(
                            0,
                            {
                                "final sources": _subscript_dict["final sources"],
                                "final sources1": _subscript_dict["final sources1"],
                                "sectors": _subscript_dict["sectors"],
                            },
                            ["final sources", "final sources1", "sectors"],
                        )
                        + implementation_policy_to_change_final_energy()
                        .loc[_subscript_dict["sectors"], :]
                        .rename(
                            {
                                "SECTORS and HOUSEHOLDS": "sectors",
                                "final sources": "final sources1",
                            }
                        )
                    ),
                    0,
                ),
                1,
            )
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def pressure_to_improve_energy_intensity_efficiency():
    """
    Real Name: Pressure to improve energy intensity efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    This variable represents the pressure in each economic sector to improve energy efficiency in the technology used. This change according to the sectors will have different technological difficulty and different cost. This pressure may be due to (1) energy policies, eg incentives for energy efficiency, or (2) significant variations in the scarcity of each type of final energy.
    """
    return xr.DataArray(
        0,
        {
            "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
            "final sources": _subscript_dict["final sources"],
        },
        ["SECTORS and HOUSEHOLDS", "final sources"],
    ) + np.minimum(
        1,
        (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                },
                ["final sources", "SECTORS and HOUSEHOLDS"],
            )
            + fuel_scarcity_pressure()
        )
        + (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
                },
                ["final sources", "SECTORS and HOUSEHOLDS"],
            )
            + implementation_policy_to_improve_energy_intensity_efficiency()
        ),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def rate_change_intensity_bottom_up():
    """
    Real Name: rate change intensity BOTTOM UP
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

    Variation of the energy intensity of inland transport in BOTTOM UP method
    """
    return if_then_else(
        (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + activate_bottom_up_method()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS and HOUSEHOLDS": "sectors"})
            == 1
        ),
        lambda: (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + inland_transport_variation_intensity()
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "final sources": _subscript_dict["final sources"],
            },
            ["sectors", "final sources"],
        ),
    )


def scarcity_feedback_final_fuel_replacement_flag():
    """
    Real Name: scarcity feedback final fuel replacement flag
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Switch to (de)activate the scarcity feedback fuel replacement.
    """
    return _ext_constant_scarcity_feedback_final_fuel_replacement_flag()


_ext_constant_scarcity_feedback_final_fuel_replacement_flag = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "scarcity_feedback_final_fuel_replacement_flag",
    {},
    _root,
    "_ext_constant_scarcity_feedback_final_fuel_replacement_flag",
)


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def share_tech_change_fuel():
    """
    Real Name: share tech change fuel
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources1', 'final sources']

    Share of the global pressure to change energy technology that corresponds to each fuel.
    """
    return zidz(
        pressure_to_change_energy_technology_by_fuel().rename(
            {"final sources": "final sources1", "final sources1": "final sources"}
        ),
        (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources1": _subscript_dict["final sources1"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources1", "final sources"],
            )
            + sum(
                pressure_to_change_energy_technology_by_fuel().rename(
                    {
                        "final sources": "final sources1!",
                        "final sources1": "final sources",
                    }
                ),
                dim=["final sources1!"],
            )
        ),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def variation_energy_intensity_target():
    """
    Real Name: variation energy intensity TARGET
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'final sources']

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
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["sectors", "final sources"],
                ),
                lambda: (
                    energy_intensity_target()
                    .loc[_subscript_dict["sectors"], :]
                    .rename({"SECTORS and HOUSEHOLDS": "sectors"})
                    - evol_final_energy_intensity_by_sector_and_fuel()
                )
                / (final_year_energy_intensity_target() - time()),
            ),
        ),
        lambda: (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + if_then_else(
                time() >= final_year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {
                        "final sources": _subscript_dict["final sources"],
                        "sectors": _subscript_dict["sectors"],
                    },
                    ["final sources", "sectors"],
                ),
                lambda: if_then_else(
                    time() < year_energy_intensity_target(),
                    lambda: xr.DataArray(
                        0,
                        {
                            "final sources": _subscript_dict["final sources"],
                            "sectors": _subscript_dict["sectors"],
                        },
                        ["final sources", "sectors"],
                    ),
                    lambda: (
                        final_energy_intensity_2020()
                        * (1 + pct_change_energy_intensity_target())
                        - (
                            xr.DataArray(
                                0,
                                {
                                    "final sources": _subscript_dict["final sources"],
                                    "sectors": _subscript_dict["sectors"],
                                },
                                ["final sources", "sectors"],
                            )
                            + evol_final_energy_intensity_by_sector_and_fuel()
                        )
                    )
                    / (final_year_energy_intensity_target() - time()),
                ),
            )
        ),
    )


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def year_policy_change_energy():
    """
    Real Name: Year policy change energy
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Year when the policy to change final energy in the sectors start. For each of five final energies.
    """
    return _ext_constant_year_policy_change_energy()


_ext_constant_year_policy_change_energy = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_policy_change_energy*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_policy_change_energy",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def year_policy_to_improve_efficiency():
    """
    Real Name: Year policy to improve efficiency
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Year when the policy to improve efficiency in sectors start. For each of five final energies.
    """
    return _ext_constant_year_policy_to_improve_efficiency()


_ext_constant_year_policy_to_improve_efficiency = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_policy_to_improve_efficiency*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_policy_to_improve_efficiency",
)


@subs(["SECTORS and HOUSEHOLDS", "final sources"], _subscript_dict)
def year_to_finish_energy_intensity_policies():
    """
    Real Name: Year to finish energy intensity policies
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: ['SECTORS and HOUSEHOLDS', 'final sources']

    Year when the policy to improve efficiency in sectors finish.
    """
    return _ext_constant_year_to_finish_energy_intensity_policies()


_ext_constant_year_to_finish_energy_intensity_policies = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_to_finish_energy_intensity_policies*",
    {
        "SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_to_finish_energy_intensity_policies",
)


def year_to_finish_policy_change_energy():
    """
    Real Name: Year to finish policy change energy
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when the policy to change final energy in the sectors finish.
    """
    return 2050
