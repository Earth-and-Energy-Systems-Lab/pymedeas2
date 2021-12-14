"""
Module final_energy_abundances_e
Translated using PySD version 2.1.0
"""


@subs(["final sources"], _subscript_dict)
def abundance_final_fuels():
    """
    Real Name: Abundance final fuels
    Original Eqn:
      abundance liquids
      abundance gases
      abundance solids
      Abundance electricity
      Abundance heat
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            abundance_liquids(), ["final sources"], {"final sources": ["liquids"]}
        ),
        rearrange(abundance_gases(), ["final sources"], {"final sources": ["gases"]}),
        rearrange(abundance_solids(), ["final sources"], {"final sources": ["solids"]}),
        rearrange(
            abundance_electricity(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(abundance_heat(), ["final sources"], {"final sources": ["heat"]}),
    )


def energy_scarcity_forgetting_time():
    """
    Real Name: energy scarcity forgetting time
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'energy_scarcity_forgetting_time')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Time in years that society takes to forget the percepticon of scarcity for
        economic sectors.
    """
    return _ext_constant_energy_scarcity_forgetting_time()


def energy_scarcity_forgetting_time_h():
    """
    Real Name: energy scarcity forgetting time H
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'energy_scarcity_forgetting_time_H')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Time in years that households take to forget the percepticon of scarcity.
    """
    return _ext_constant_energy_scarcity_forgetting_time_h()


@subs(["final sources"], _subscript_dict)
def increase_in_perception_fe_scarcity():
    """
    Real Name: increase in perception FE scarcity
    Original Eqn: scarcity final fuels[final sources]*sensitivity to scarcity*(1-perception of final energy scarcity [final sources])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Increase in the perception of economic sectors of final energy scarcity of
        each fuel
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
    Original Eqn: scarcity final fuels H[final sources]*sensitivity to scarcity H*(1-perception of final energy scarcity H[final sources])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Increase in socieconomic perception of final energy scarcity of each fuel
        for households.
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
    Original Eqn: INTEG ( increase in perception FE scarcity[final sources]-reduction in perception FE scarcity[final sources], 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Perception of final energy scarcity of each fuel by economic sectors. This
        perception drives the fuel replacement and efficiency improvement.
    """
    return _integ_perception_of_final_energy_scarcity()


@subs(["final sources"], _subscript_dict)
def perception_of_final_energy_scarcity_h():
    """
    Real Name: perception of final energy scarcity H
    Original Eqn: INTEG ( increase in perception FE scarcity H[final sources]-reduction in perception FE scarcity H[final sources], 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Socieconomic perception of final energy scarcity of each fuel for
        households. This perception drives the fuel replacement and efficiency
        improvement.
    """
    return _integ_perception_of_final_energy_scarcity_h()


@subs(["final sources", "final sources1"], _subscript_dict)
def perception_of_interfuel_final_energy_scarcities_h():
    """
    Real Name: "perception of inter-fuel final energy scarcities H"
    Original Eqn: IF THEN ELSE(sensitivity to scarcity H=0,0,ZIDZ( perception of final energy scarcity H[final sources1]-perception of final energy scarcity H[final sources], 1))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'final sources1']

    Socieconomic perception of final energy scarcity between fuels for
        households. Matrix 5x5. This perception drives the fuel replacement and
        efficiency improvement.
    """
    return if_then_else(
        sensitivity_to_scarcity_h() == 0,
        lambda: 0,
        lambda: zidz(
            rearrange(
                perception_of_final_energy_scarcity_h(),
                ["final sources1"],
                _subscript_dict,
            )
            - perception_of_final_energy_scarcity_h(),
            1,
        ),
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def perception_of_interfuel_final_energy_scarcities():
    """
    Real Name: "perception of inter-fuel final energy scarcities"
    Original Eqn: IF THEN ELSE(sensitivity to scarcity=0,0,ZIDZ( perception of final energy scarcity[final sources1]-perception of final energy scarcity[final sources], 1))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'final sources1']

    Perception of economic sectors of final energy scarcity between fuels.
        Matrix 5x5. This perception drives the fuel replacement and efficiency
        improvement.
    """
    return if_then_else(
        sensitivity_to_scarcity() == 0,
        lambda: 0,
        lambda: zidz(
            rearrange(
                perception_of_final_energy_scarcity(),
                ["final sources1"],
                _subscript_dict,
            )
            - perception_of_final_energy_scarcity(),
            1,
        ),
    )


@subs(["final sources"], _subscript_dict)
def reduction_in_perception_fe_scarcity():
    """
    Real Name: reduction in perception FE scarcity
    Original Eqn: perception of final energy scarcity[final sources]/energy scarcity forgetting time
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Reduction of the perception of energy scarcity of economic sectors due to
        the "forgetting" effect.
    """
    return perception_of_final_energy_scarcity() / energy_scarcity_forgetting_time()


@subs(["final sources"], _subscript_dict)
def reduction_in_perception_fe_scarcity_h():
    """
    Real Name: reduction in perception FE scarcity H
    Original Eqn: perception of final energy scarcity H[final sources]/energy scarcity forgetting time H
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Reduction of the perception of energy scarcity of households due to the
        "forgetting" effect.
    """
    return perception_of_final_energy_scarcity_h() / energy_scarcity_forgetting_time_h()


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels():
    """
    Real Name: scarcity final fuels
    Original Eqn: 1-Abundance final fuels[final sources]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance)        Scarcity=0 while the supply covers the demand; the closest to 1 indicates
        a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_counter():
    """
    Real Name: scarcity final fuels counter
    Original Eqn: INTEG ( IF THEN ELSE(scarcity final fuels flags[final sources]=1, 1, 0 ), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return _integ_scarcity_final_fuels_counter()


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_flags():
    """
    Real Name: scarcity final fuels flags
    Original Eqn: IF THEN ELSE(Abundance final fuels[final sources]<0.999, 1, 0 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return if_then_else(abundance_final_fuels() < 0.999, lambda: 1, lambda: 0)


@subs(["final sources"], _subscript_dict)
def scarcity_final_fuels_h():
    """
    Real Name: scarcity final fuels H
    Original Eqn: 1-Abundance final fuels[final sources]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance)        Scarcity=0 while the supply covers the demand; the closest to 1 indicates
        a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@subs(["final sources"], _subscript_dict)
def scarcity_fuels_flag():
    """
    Real Name: Scarcity fuels flag
    Original Eqn: IF THEN ELSE(scarcity final fuels counter[final sources]>1, 1, 0 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Scarcity indicator for final fuels.
    """
    return if_then_else(scarcity_final_fuels_counter() > 1, lambda: 1, lambda: 0)


@subs(["materials"], _subscript_dict)
def scarcity_reserves_counter():
    """
    Real Name: scarcity reserves counter
    Original Eqn: INTEG ( IF THEN ELSE("materials availability (reserves)"[materials]=0, 1, 0 ), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']


    """
    return _integ_scarcity_reserves_counter()


@subs(["materials"], _subscript_dict)
def scarcity_reserves_flag():
    """
    Real Name: Scarcity reserves flag
    Original Eqn: IF THEN ELSE( scarcity reserves counter[materials]>1,1, 0 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Scarcity indicator for materials reserves.
    """
    return if_then_else(scarcity_reserves_counter() > 1, lambda: 1, lambda: 0)


@subs(["materials"], _subscript_dict)
def scarcity_resources_counter():
    """
    Real Name: scarcity resources counter
    Original Eqn: INTEG ( IF THEN ELSE("materials availability (resources)"[materials]=0, 1, 0 ), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']


    """
    return _integ_scarcity_resources_counter()


@subs(["materials"], _subscript_dict)
def scarcity_resources_flag():
    """
    Real Name: Scarcity resources flag
    Original Eqn: IF THEN ELSE(scarcity resources counter[materials]>1, 1, 0 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Scarcity indicator for materials resources.
    """
    return if_then_else(scarcity_resources_counter() > 1, lambda: 1, lambda: 0)


def sensitivity_to_energy_scarcity_high():
    """
    Real Name: sensitivity to energy scarcity High
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'sensitivity_scarcity_high')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    High value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_high()


def sensitivity_to_energy_scarcity_low():
    """
    Real Name: sensitivity to energy scarcity Low
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'sensitivity_scarcity_low')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Low value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_low()


def sensitivity_to_energy_scarcity_medium():
    """
    Real Name: sensitivity to energy scarcity Medium
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'sensitivity_scarcity_medium')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Medium value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_medium()


def sensitivity_to_scarcity():
    """
    Real Name: sensitivity to scarcity
    Original Eqn: IF THEN ELSE(sensitivity to scarcity option=1,sensitivity to energy scarcity Low,IF THEN ELSE(sensitivity to scarcity option=2,sensitivity to energy scarcity Medium,sensitivity to energy scarcity High))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Sensitivity of the economic sectors to the energy scarcity. Value defined
        by user.
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
    Original Eqn: IF THEN ELSE(sensitivity to scarcity option H=1,sensitivity to energy scarcity Low,IF THEN ELSE(sensitivity to scarcity option H=2,sensitivity to energy scarcity Medium,sensitivity to energy scarcity High))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Sensitivity of the households to the energy scarcity. Value defined by
        user.
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
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'sensitivity_to_scarcity_option')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Option defined by user about the sensitivity of economic sectors to energy scarcity:        1-Low        2-Medium        3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option()


def sensitivity_to_scarcity_option_h():
    """
    Real Name: sensitivity to scarcity option H
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'sensitivity_to_scarcity_option_H')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Option defined by user about the sensitivity of households to the energy scarcity:        1-Low        2-Medium        3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option_h()


@subs(["final sources"], _subscript_dict)
def year_final_scarcity_final_fuels():
    """
    Real Name: Year final scarcity final fuels
    Original Eqn: IF THEN ELSE(scarcity final fuels counter[final sources]>0,Year init scarcity final fuels[final sources]+scarcity final fuels counter[final sources]-1,0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Final year of scarcity of final fuels.
    """
    return if_then_else(
        scarcity_final_fuels_counter() > 0,
        lambda: year_init_scarcity_final_fuels() + scarcity_final_fuels_counter() - 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def year_final_scarcity_reserves():
    """
    Real Name: Year final scarcity reserves
    Original Eqn: IF THEN ELSE(scarcity reserves counter[materials]>0,Year init scarcity reserves[materials]+scarcity reserves counter[materials]-1,0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Final year of scarcity of material reserves.
    """
    return if_then_else(
        scarcity_reserves_counter() > 0,
        lambda: year_init_scarcity_reserves() + scarcity_reserves_counter() - 1,
        lambda: 0,
    )


@subs(["materials"], _subscript_dict)
def year_final_scarcity_resources():
    """
    Real Name: Year final scarcity resources
    Original Eqn: IF THEN ELSE(scarcity resources counter[materials]>0,Year init scarcity resources[materials]+scarcity resources counter[materials]-1,0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Final year of scarcity of materials resources.
    """
    return if_then_else(
        scarcity_resources_counter() > 0,
        lambda: year_init_scarcity_resources() + scarcity_resources_counter() - 1,
        lambda: 0,
    )


@subs(["final sources"], _subscript_dict)
def year_init_scarcity_final_fuels():
    """
    Real Name: Year init scarcity final fuels
    Original Eqn: INTEG ( IF THEN ELSE(scarcity final fuels flags[final sources]=1,(IF THEN ELSE(scarcity final fuels counter[final sources]=1, (Time*1/TIME STEP)-20, 0)), 0), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Initial year of scarcity of final fuels.
    """
    return _integ_year_init_scarcity_final_fuels()


@subs(["materials"], _subscript_dict)
def year_init_scarcity_reserves():
    """
    Real Name: Year init scarcity reserves
    Original Eqn: INTEG ( IF THEN ELSE("materials availability (reserves)"[materials]=0, (IF THEN ELSE( scarcity reserves counter[materials]=1, (Time*1/TIME STEP), 0 )), 0 ), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Initial year of scarcity of material reserves.
    """
    return _integ_year_init_scarcity_reserves()


@subs(["materials"], _subscript_dict)
def year_init_scarcity_resources():
    """
    Real Name: Year init scarcity resources
    Original Eqn: INTEG ( IF THEN ELSE("materials availability (resources)"[materials]=0,(IF THEN ELSE(scarcity resources counter[materials]=1,(Time*1/TIME STEP),0)),0), 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Initial year of scarcity of material resources.
    """
    return _integ_year_init_scarcity_resources()


_ext_constant_energy_scarcity_forgetting_time = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time",
    {},
    _root,
    "_ext_constant_energy_scarcity_forgetting_time",
)


_ext_constant_energy_scarcity_forgetting_time_h = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time_H",
    {},
    _root,
    "_ext_constant_energy_scarcity_forgetting_time_h",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_perception_of_final_energy_scarcity():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_of_final_energy_scarcity
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for perception_of_final_energy_scarcity function
    """
    return 0


@subs(["final sources"], _subscript_dict)
def _integ_input_perception_of_final_energy_scarcity():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_of_final_energy_scarcity
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for perception_of_final_energy_scarcity function
    """
    return increase_in_perception_fe_scarcity() - reduction_in_perception_fe_scarcity()


_integ_perception_of_final_energy_scarcity = Integ(
    _integ_input_perception_of_final_energy_scarcity,
    _integ_init_perception_of_final_energy_scarcity,
    "_integ_perception_of_final_energy_scarcity",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_perception_of_final_energy_scarcity_h():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_of_final_energy_scarcity_h
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for perception_of_final_energy_scarcity_h function
    """
    return 0


@subs(["final sources"], _subscript_dict)
def _integ_input_perception_of_final_energy_scarcity_h():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_of_final_energy_scarcity_h
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for perception_of_final_energy_scarcity_h function
    """
    return (
        increase_in_perception_fe_scarcity_h() - reduction_in_perception_fe_scarcity_h()
    )


_integ_perception_of_final_energy_scarcity_h = Integ(
    _integ_input_perception_of_final_energy_scarcity_h,
    _integ_init_perception_of_final_energy_scarcity_h,
    "_integ_perception_of_final_energy_scarcity_h",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_scarcity_final_fuels_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_final_fuels_counter
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for scarcity_final_fuels_counter function
    """
    return 0


@subs(["final sources"], _subscript_dict)
def _integ_input_scarcity_final_fuels_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_final_fuels_counter
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for scarcity_final_fuels_counter function
    """
    return if_then_else(scarcity_final_fuels_flags() == 1, lambda: 1, lambda: 0)


_integ_scarcity_final_fuels_counter = Integ(
    _integ_input_scarcity_final_fuels_counter,
    _integ_init_scarcity_final_fuels_counter,
    "_integ_scarcity_final_fuels_counter",
)


@subs(["materials"], _subscript_dict)
def _integ_init_scarcity_reserves_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_reserves_counter
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for scarcity_reserves_counter function
    """
    return 0


@subs(["materials"], _subscript_dict)
def _integ_input_scarcity_reserves_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_reserves_counter
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for scarcity_reserves_counter function
    """
    return if_then_else(materials_availability_reserves() == 0, lambda: 1, lambda: 0)


_integ_scarcity_reserves_counter = Integ(
    _integ_input_scarcity_reserves_counter,
    _integ_init_scarcity_reserves_counter,
    "_integ_scarcity_reserves_counter",
)


@subs(["materials"], _subscript_dict)
def _integ_init_scarcity_resources_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_resources_counter
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for scarcity_resources_counter function
    """
    return 0


@subs(["materials"], _subscript_dict)
def _integ_input_scarcity_resources_counter():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for scarcity_resources_counter
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for scarcity_resources_counter function
    """
    return if_then_else(materials_availability_resources() == 0, lambda: 1, lambda: 0)


_integ_scarcity_resources_counter = Integ(
    _integ_input_scarcity_resources_counter,
    _integ_init_scarcity_resources_counter,
    "_integ_scarcity_resources_counter",
)


_ext_constant_sensitivity_to_energy_scarcity_high = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_high",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_high",
)


_ext_constant_sensitivity_to_energy_scarcity_low = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_low",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_low",
)


_ext_constant_sensitivity_to_energy_scarcity_medium = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_medium",
    {},
    _root,
    "_ext_constant_sensitivity_to_energy_scarcity_medium",
)


_ext_constant_sensitivity_to_scarcity_option = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option",
    {},
    _root,
    "_ext_constant_sensitivity_to_scarcity_option",
)


_ext_constant_sensitivity_to_scarcity_option_h = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option_H",
    {},
    _root,
    "_ext_constant_sensitivity_to_scarcity_option_h",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_year_init_scarcity_final_fuels():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_final_fuels
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for year_init_scarcity_final_fuels function
    """
    return 0


@subs(["final sources"], _subscript_dict)
def _integ_input_year_init_scarcity_final_fuels():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_final_fuels
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for year_init_scarcity_final_fuels function
    """
    return if_then_else(
        scarcity_final_fuels_flags() == 1,
        lambda: (
            if_then_else(
                scarcity_final_fuels_counter() == 1,
                lambda: (time() * 1 / time_step()) - 20,
                lambda: 0,
            )
        ),
        lambda: 0,
    )


_integ_year_init_scarcity_final_fuels = Integ(
    _integ_input_year_init_scarcity_final_fuels,
    _integ_init_year_init_scarcity_final_fuels,
    "_integ_year_init_scarcity_final_fuels",
)


@subs(["materials"], _subscript_dict)
def _integ_init_year_init_scarcity_reserves():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_reserves
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for year_init_scarcity_reserves function
    """
    return 0


@subs(["materials"], _subscript_dict)
def _integ_input_year_init_scarcity_reserves():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_reserves
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for year_init_scarcity_reserves function
    """
    return if_then_else(
        materials_availability_reserves() == 0,
        lambda: (
            if_then_else(
                scarcity_reserves_counter() == 1,
                lambda: (time() * 1 / time_step()),
                lambda: 0,
            )
        ),
        lambda: 0,
    )


_integ_year_init_scarcity_reserves = Integ(
    _integ_input_year_init_scarcity_reserves,
    _integ_init_year_init_scarcity_reserves,
    "_integ_year_init_scarcity_reserves",
)


@subs(["materials"], _subscript_dict)
def _integ_init_year_init_scarcity_resources():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_resources
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for year_init_scarcity_resources function
    """
    return 0


@subs(["materials"], _subscript_dict)
def _integ_input_year_init_scarcity_resources():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for year_init_scarcity_resources
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for year_init_scarcity_resources function
    """
    return if_then_else(
        materials_availability_resources() == 0,
        lambda: (
            if_then_else(
                scarcity_resources_counter() == 1,
                lambda: (time() * 1 / time_step()),
                lambda: 0,
            )
        ),
        lambda: 0,
    )


_integ_year_init_scarcity_resources = Integ(
    _integ_input_year_init_scarcity_resources,
    _integ_init_year_init_scarcity_resources,
    "_integ_year_init_scarcity_resources",
)
