"""
Module final_energy_abundances
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def abundance_final_fuels():
    """
    Real Name: Abundance final fuels
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']


    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = abundance_liquids()
    value.loc[{"final sources": ["gases"]}] = abundance_gases()
    value.loc[{"final sources": ["solids"]}] = abundance_solids()
    value.loc[{"final sources": ["electricity"]}] = abundance_electricity()
    value.loc[{"final sources": ["heat"]}] = abundance_heat()
    return value


def energy_scarcity_forgetting_time():
    """
    Real Name: energy scarcity forgetting time
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Time in years that society takes to forget the percepticon of scarcity for economic sectors.
    """
    return _ext_constant_energy_scarcity_forgetting_time()


_ext_constant_energy_scarcity_forgetting_time = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time",
    {},
    _root,
    "_ext_constant_energy_scarcity_forgetting_time",
)


def energy_scarcity_forgetting_time_h():
    """
    Real Name: energy scarcity forgetting time H
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Time in years that households take to forget the percepticon of scarcity.
    """
    return _ext_constant_energy_scarcity_forgetting_time_h()


_ext_constant_energy_scarcity_forgetting_time_h = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time_H",
    {},
    _root,
    "_ext_constant_energy_scarcity_forgetting_time_h",
)


@subs(["final sources"], _subscript_dict)
def increase_in_perception_fe_scarcity():
    """
    Real Name: increase in perception FE scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Increase in the perception of economic sectors of final energy scarcity of each fuel
    """
    return (
        scarcity_final_fuels()
        * sensitivity_to_scarcity()
        * (1 - perception_of_final_energy_scarcity())
    )


@subs(["final sources"], _subscript_dict)
def increase_in_perception_fe_scarcity_h():
    """
    Real Name: increase in perception FE scarcity H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Increase in socieconomic perception of final energy scarcity of each fuel for households.
    """
    return (
        scarcity_final_fuels_h()
        * sensitivity_to_scarcity_h()
        * (1 - perception_of_final_energy_scarcity_h())
    )


@subs(["final sources"], _subscript_dict)
def perception_of_final_energy_scarcity():
    """
    Real Name: perception of final energy scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']

    Perception of final energy scarcity of each fuel by economic sectors. This perception drives the fuel replacement and efficiency improvement.
    """
    return _integ_perception_of_final_energy_scarcity()


_integ_perception_of_final_energy_scarcity = Integ(
    lambda: increase_in_perception_fe_scarcity()
    - reduction_in_perception_fe_scarcity(),
    lambda: xr.DataArray(
        0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    ),
    "_integ_perception_of_final_energy_scarcity",
)


@subs(["final sources"], _subscript_dict)
def perception_of_final_energy_scarcity_h():
    """
    Real Name: perception of final energy scarcity H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']

    Socieconomic perception of final energy scarcity of each fuel for households. This perception drives the fuel replacement and efficiency improvement.
    """
    return _integ_perception_of_final_energy_scarcity_h()


_integ_perception_of_final_energy_scarcity_h = Integ(
    lambda: increase_in_perception_fe_scarcity_h()
    - reduction_in_perception_fe_scarcity_h(),
    lambda: xr.DataArray(
        0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    ),
    "_integ_perception_of_final_energy_scarcity_h",
)


@subs(["final sources", "final sources1"], _subscript_dict)
def perception_of_interfuel_final_energy_scarcities_h():
    """
    Real Name: "perception of inter-fuel final energy scarcities H"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'final sources1']

    Socieconomic perception of final energy scarcity between fuels for households. Matrix 5x5. This perception drives the fuel replacement and efficiency improvement.
    """
    return xr.DataArray(
        0,
        {
            "final sources": _subscript_dict["final sources"],
            "final sources1": _subscript_dict["final sources1"],
        },
        ["final sources", "final sources1"],
    ) + if_then_else(
        sensitivity_to_scarcity_h() == 0,
        lambda: xr.DataArray(
            0,
            {
                "final sources1": _subscript_dict["final sources1"],
                "final sources": _subscript_dict["final sources"],
            },
            ["final sources1", "final sources"],
        ),
        lambda: zidz(
            (
                xr.DataArray(
                    0,
                    {
                        "final sources1": _subscript_dict["final sources1"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["final sources1", "final sources"],
                )
                + perception_of_final_energy_scarcity_h().rename(
                    {"final sources": "final sources1"}
                )
            )
            - (
                xr.DataArray(
                    0,
                    {
                        "final sources1": _subscript_dict["final sources1"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["final sources1", "final sources"],
                )
                + perception_of_final_energy_scarcity_h()
            ),
            1,
        ),
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def perception_of_interfuel_final_energy_scarcities():
    """
    Real Name: "perception of inter-fuel final energy scarcities"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'final sources1']

    Perception of economic sectors of final energy scarcity between fuels. Matrix 5x5. This perception drives the fuel replacement and efficiency improvement.
    """
    return xr.DataArray(
        0,
        {
            "final sources": _subscript_dict["final sources"],
            "final sources1": _subscript_dict["final sources1"],
        },
        ["final sources", "final sources1"],
    ) + if_then_else(
        sensitivity_to_scarcity() == 0,
        lambda: xr.DataArray(
            0,
            {
                "final sources1": _subscript_dict["final sources1"],
                "final sources": _subscript_dict["final sources"],
            },
            ["final sources1", "final sources"],
        ),
        lambda: zidz(
            (
                xr.DataArray(
                    0,
                    {
                        "final sources1": _subscript_dict["final sources1"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["final sources1", "final sources"],
                )
                + perception_of_final_energy_scarcity().rename(
                    {"final sources": "final sources1"}
                )
            )
            - (
                xr.DataArray(
                    0,
                    {
                        "final sources1": _subscript_dict["final sources1"],
                        "final sources": _subscript_dict["final sources"],
                    },
                    ["final sources1", "final sources"],
                )
                + perception_of_final_energy_scarcity()
            ),
            1,
        ),
    )


@subs(["final sources"], _subscript_dict)
def reduction_in_perception_fe_scarcity():
    """
    Real Name: reduction in perception FE scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_of_final_energy_scarcity() / energy_scarcity_forgetting_time()


@subs(["final sources"], _subscript_dict)
def reduction_in_perception_fe_scarcity_h():
    """
    Real Name: reduction in perception FE scarcity H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Reduction of the perception of energy scarcity of households due to the "forgetting" effect.
    """
    return perception_of_final_energy_scarcity_h() / energy_scarcity_forgetting_time_h()


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels():
    """
    Real Name: scarcity final fuels
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_counter():
    """
    Real Name: scarcity final fuels counter
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']


    """
    return _integ_scarcity_final_fuels_counter()


_integ_scarcity_final_fuels_counter = Integ(
    lambda: if_then_else(
        scarcity_final_fuels_flags() == 1,
        lambda: xr.DataArray(
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    ),
    lambda: xr.DataArray(
        0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    ),
    "_integ_scarcity_final_fuels_counter",
)


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_flags():
    """
    Real Name: scarcity final fuels flags
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']


    """
    return if_then_else(
        abundance_final_fuels() < 0.999,
        lambda: xr.DataArray(
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_h():
    """
    Real Name: scarcity final fuels H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@subs(["final sources"], _subscript_dict)
def scarcity_fuels_flag():
    """
    Real Name: Scarcity fuels flag
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Scarcity indicator for final fuels.
    """
    return if_then_else(
        scarcity_final_fuels_counter() > 1,
        lambda: xr.DataArray(
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@subs(["materials"], _subscript_dict)
def scarcity_reserves_counter():
    """
    Real Name: scarcity reserves counter
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']


    """
    return _integ_scarcity_reserves_counter()


_integ_scarcity_reserves_counter = Integ(
    lambda: if_then_else(
        materials_availability_reserves() == 0,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_scarcity_reserves_counter",
)


@subs(["materials"], _subscript_dict)
def scarcity_reserves_flag():
    """
    Real Name: Scarcity reserves flag
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Scarcity indicator for materials reserves.
    """
    return if_then_else(
        scarcity_reserves_counter() > 1,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@subs(["materials"], _subscript_dict)
def scarcity_resources_counter():
    """
    Real Name: scarcity resources counter
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']


    """
    return _integ_scarcity_resources_counter()


_integ_scarcity_resources_counter = Integ(
    lambda: if_then_else(
        materials_availability_resources() == 0,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_scarcity_resources_counter",
)


@subs(["materials"], _subscript_dict)
def scarcity_resources_flag():
    """
    Real Name: Scarcity resources flag
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Scarcity indicator for materials resources.
    """
    return if_then_else(
        scarcity_resources_counter() > 1,
        lambda: xr.DataArray(
            1, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


def sensitivity_to_energy_scarcity_high():
    """
    Real Name: sensitivity to energy scarcity High
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    High value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_high()


_ext_constant_sensitivity_to_energy_scarcity_high = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_high",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_high",
)


def sensitivity_to_energy_scarcity_low():
    """
    Real Name: sensitivity to energy scarcity Low
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Low value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_low()


_ext_constant_sensitivity_to_energy_scarcity_low = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_low",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_low",
)


def sensitivity_to_energy_scarcity_medium():
    """
    Real Name: sensitivity to energy scarcity Medium
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Medium value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_medium()


_ext_constant_sensitivity_to_energy_scarcity_medium = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_medium",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_medium",
)


def sensitivity_to_scarcity():
    """
    Real Name: sensitivity to scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Sensitivity of the economic sectors to the energy scarcity. Value defined by user.
    """
    return if_then_else(
        sensitivity_to_scarcity_option() == 1,
        lambda: sensitivity_to_energy_scarcity_low(),
        lambda: if_then_else(
            sensitivity_to_scarcity_option() == 2,
            lambda: sensitivity_to_energy_scarcity_medium(),
            lambda: sensitivity_to_energy_scarcity_high(),
        ),
    )


def sensitivity_to_scarcity_h():
    """
    Real Name: sensitivity to scarcity H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Sensitivity of the households to the energy scarcity. Value defined by user.
    """
    return if_then_else(
        sensitivity_to_scarcity_option_h() == 1,
        lambda: sensitivity_to_energy_scarcity_low(),
        lambda: if_then_else(
            sensitivity_to_scarcity_option_h() == 2,
            lambda: sensitivity_to_energy_scarcity_medium(),
            lambda: sensitivity_to_energy_scarcity_high(),
        ),
    )


def sensitivity_to_scarcity_option():
    """
    Real Name: sensitivity to scarcity option
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Option defined by user about the sensitivity of economic sectors to energy scarcity: 1-Low 2-Medium 3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option()


_ext_constant_sensitivity_to_scarcity_option = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option",
    {},
    _root,
    "_ext_constant_sensitivity_to_scarcity_option",
)


def sensitivity_to_scarcity_option_h():
    """
    Real Name: sensitivity to scarcity option H
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Option defined by user about the sensitivity of households to the energy scarcity: 1-Low 2-Medium 3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option_h()


_ext_constant_sensitivity_to_scarcity_option_h = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option_H",
    {},
    _root,
    "_ext_constant_sensitivity_to_scarcity_option_h",
)


@subs(["final sources"], _subscript_dict)
def year_final_scarcity_final_fuels():
    """
    Real Name: Year final scarcity final fuels
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Final year of scarcity of final fuels.
    """
    return if_then_else(
        scarcity_final_fuels_counter() > 0,
        lambda: year_init_scarcity_final_fuels() + scarcity_final_fuels_counter() - 1,
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@subs(["materials"], _subscript_dict)
def year_final_scarcity_reserves():
    """
    Real Name: Year final scarcity reserves
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Final year of scarcity of material reserves.
    """
    return if_then_else(
        scarcity_reserves_counter() > 0,
        lambda: year_init_scarcity_reserves() + scarcity_reserves_counter() - 1,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@subs(["materials"], _subscript_dict)
def year_final_scarcity_resources():
    """
    Real Name: Year final scarcity resources
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['materials']

    Final year of scarcity of materials resources.
    """
    return if_then_else(
        scarcity_resources_counter() > 0,
        lambda: year_init_scarcity_resources() + scarcity_resources_counter() - 1,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@subs(["final sources"], _subscript_dict)
def year_init_scarcity_final_fuels():
    """
    Real Name: Year init scarcity final fuels
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']

    Initial year of scarcity of final fuels.
    """
    return _integ_year_init_scarcity_final_fuels()


_integ_year_init_scarcity_final_fuels = Integ(
    lambda: if_then_else(
        scarcity_final_fuels_flags() == 1,
        lambda: if_then_else(
            scarcity_final_fuels_counter() == 1,
            lambda: xr.DataArray(
                time() * 1 / time_step() - 20,
                {"final sources": _subscript_dict["final sources"]},
                ["final sources"],
            ),
            lambda: xr.DataArray(
                0,
                {"final sources": _subscript_dict["final sources"]},
                ["final sources"],
            ),
        ),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    ),
    lambda: xr.DataArray(
        0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    ),
    "_integ_year_init_scarcity_final_fuels",
)


@subs(["materials"], _subscript_dict)
def year_init_scarcity_reserves():
    """
    Real Name: Year init scarcity reserves
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Initial year of scarcity of material reserves.
    """
    return _integ_year_init_scarcity_reserves()


_integ_year_init_scarcity_reserves = Integ(
    lambda: if_then_else(
        materials_availability_reserves() == 0,
        lambda: if_then_else(
            scarcity_reserves_counter() == 1,
            lambda: xr.DataArray(
                time() * 1 / time_step(),
                {"materials": _subscript_dict["materials"]},
                ["materials"],
            ),
            lambda: xr.DataArray(
                0, {"materials": _subscript_dict["materials"]}, ["materials"]
            ),
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_year_init_scarcity_reserves",
)


@subs(["materials"], _subscript_dict)
def year_init_scarcity_resources():
    """
    Real Name: Year init scarcity resources
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: ['materials']

    Initial year of scarcity of material resources.
    """
    return _integ_year_init_scarcity_resources()


_integ_year_init_scarcity_resources = Integ(
    lambda: if_then_else(
        materials_availability_resources() == 0,
        lambda: if_then_else(
            scarcity_resources_counter() == 1,
            lambda: xr.DataArray(
                time() * 1 / time_step(),
                {"materials": _subscript_dict["materials"]},
                ["materials"],
            ),
            lambda: xr.DataArray(
                0, {"materials": _subscript_dict["materials"]}, ["materials"]
            ),
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_year_init_scarcity_resources",
)
