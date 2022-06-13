"""
Module final_energy_abundances
Translated using PySD version 3.2.0
"""


@component.add(
    name="Abundance final fuels",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "abundance_liquids": 1,
        "abundance_gases": 1,
        "abundance_solids": 1,
        "abundance_electricity": 1,
        "abundance_heat": 1,
    },
)
def abundance_final_fuels():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["liquids"]] = abundance_liquids()
    value.loc[["gases"]] = abundance_gases()
    value.loc[["solids"]] = abundance_solids()
    value.loc[["electricity"]] = abundance_electricity()
    value.loc[["heat"]] = abundance_heat()
    return value


@component.add(
    name="energy scarcity forgetting time",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_energy_scarcity_forgetting_time"},
)
def energy_scarcity_forgetting_time():
    """
    Time in years that society takes to forget the percepticon of scarcity for economic sectors.
    """
    return _ext_constant_energy_scarcity_forgetting_time()


_ext_constant_energy_scarcity_forgetting_time = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time",
    {},
    _root,
    {},
    "_ext_constant_energy_scarcity_forgetting_time",
)


@component.add(
    name="energy scarcity forgetting time H",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_energy_scarcity_forgetting_time_h"},
)
def energy_scarcity_forgetting_time_h():
    """
    Time in years that households take to forget the percepticon of scarcity.
    """
    return _ext_constant_energy_scarcity_forgetting_time_h()


_ext_constant_energy_scarcity_forgetting_time_h = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "energy_scarcity_forgetting_time_H",
    {},
    _root,
    {},
    "_ext_constant_energy_scarcity_forgetting_time_h",
)


@component.add(
    name="increase in perception FE scarcity",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_final_fuels": 1,
        "sensitivity_to_scarcity": 1,
        "perception_of_final_energy_scarcity": 1,
    },
)
def increase_in_perception_fe_scarcity():
    """
    Increase in the perception of economic sectors of final energy scarcity of each fuel
    """
    return (
        scarcity_final_fuels()
        * sensitivity_to_scarcity()
        * (1 - perception_of_final_energy_scarcity())
    )


@component.add(
    name="increase in perception FE scarcity H",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_final_fuels_h": 1,
        "sensitivity_to_scarcity_h": 1,
        "perception_of_final_energy_scarcity_h": 1,
    },
)
def increase_in_perception_fe_scarcity_h():
    """
    Increase in socieconomic perception of final energy scarcity of each fuel for households.
    """
    return (
        scarcity_final_fuels_h()
        * sensitivity_to_scarcity_h()
        * (1 - perception_of_final_energy_scarcity_h())
    )


@component.add(
    name="perception of final energy scarcity",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_perception_of_final_energy_scarcity": 1},
    other_deps={
        "_integ_perception_of_final_energy_scarcity": {
            "initial": {},
            "step": {
                "increase_in_perception_fe_scarcity": 1,
                "reduction_in_perception_fe_scarcity": 1,
            },
        }
    },
)
def perception_of_final_energy_scarcity():
    """
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


@component.add(
    name="perception of final energy scarcity H",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_perception_of_final_energy_scarcity_h": 1},
    other_deps={
        "_integ_perception_of_final_energy_scarcity_h": {
            "initial": {},
            "step": {
                "increase_in_perception_fe_scarcity_h": 1,
                "reduction_in_perception_fe_scarcity_h": 1,
            },
        }
    },
)
def perception_of_final_energy_scarcity_h():
    """
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


@component.add(
    name='"perception of inter-fuel final energy scarcities H"',
    units="Dmnl",
    subscripts=["final sources", "final sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_to_scarcity_h": 1,
        "perception_of_final_energy_scarcity_h": 2,
    },
)
def perception_of_interfuel_final_energy_scarcities_h():
    """
    Socieconomic perception of final energy scarcity between fuels for households. Matrix 5x5. This perception drives the fuel replacement and efficiency improvement.
    """
    return if_then_else(
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
            perception_of_final_energy_scarcity_h().rename(
                {"final sources": "final sources1"}
            )
            - perception_of_final_energy_scarcity_h(),
            1,
        ),
    ).transpose("final sources", "final sources1")


@component.add(
    name='"perception of inter-fuel final energy scarcities"',
    units="Dmnl",
    subscripts=["final sources", "final sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sensitivity_to_scarcity": 1, "perception_of_final_energy_scarcity": 2},
)
def perception_of_interfuel_final_energy_scarcities():
    """
    Perception of economic sectors of final energy scarcity between fuels. Matrix 5x5. This perception drives the fuel replacement and efficiency improvement.
    """
    return if_then_else(
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
            perception_of_final_energy_scarcity().rename(
                {"final sources": "final sources1"}
            )
            - perception_of_final_energy_scarcity(),
            1,
        ),
    ).transpose("final sources", "final sources1")


@component.add(
    name="reduction in perception FE scarcity",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_of_final_energy_scarcity": 1,
        "energy_scarcity_forgetting_time": 1,
    },
)
def reduction_in_perception_fe_scarcity():
    """
    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_of_final_energy_scarcity() / energy_scarcity_forgetting_time()


@component.add(
    name="reduction in perception FE scarcity H",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_of_final_energy_scarcity_h": 1,
        "energy_scarcity_forgetting_time_h": 1,
    },
)
def reduction_in_perception_fe_scarcity_h():
    """
    Reduction of the perception of energy scarcity of households due to the "forgetting" effect.
    """
    return perception_of_final_energy_scarcity_h() / energy_scarcity_forgetting_time_h()


@component.add(
    name="scarcity final fuels",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_final_fuels": 1},
)
def scarcity_final_fuels():
    """
    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@component.add(
    name="scarcity final fuels counter",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_scarcity_final_fuels_counter": 1},
    other_deps={
        "_integ_scarcity_final_fuels_counter": {
            "initial": {},
            "step": {"scarcity_final_fuels_flags": 1},
        }
    },
)
def scarcity_final_fuels_counter():
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


@component.add(
    name="scarcity final fuels flags",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_final_fuels": 1},
)
def scarcity_final_fuels_flags():
    return if_then_else(
        abundance_final_fuels() < 0.999,
        lambda: xr.DataArray(
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@component.add(
    name="scarcity final fuels H",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_final_fuels": 1},
)
def scarcity_final_fuels_h():
    """
    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_final_fuels()


@component.add(
    name="Scarcity fuels flag",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_final_fuels_counter": 1},
)
def scarcity_fuels_flag():
    """
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


@component.add(
    name="scarcity reserves counter",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_scarcity_reserves_counter": 1},
    other_deps={
        "_integ_scarcity_reserves_counter": {
            "initial": {},
            "step": {"materials_availability_reserves": 1},
        }
    },
)
def scarcity_reserves_counter():
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


@component.add(
    name="Scarcity reserves flag",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_reserves_counter": 1},
)
def scarcity_reserves_flag():
    """
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


@component.add(
    name="scarcity resources counter",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_scarcity_resources_counter": 1},
    other_deps={
        "_integ_scarcity_resources_counter": {
            "initial": {},
            "step": {"materials_availability_resources": 1},
        }
    },
)
def scarcity_resources_counter():
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


@component.add(
    name="Scarcity resources flag",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_resources_counter": 1},
)
def scarcity_resources_flag():
    """
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


@component.add(
    name="sensitivity to energy scarcity High",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_to_energy_scarcity_high"},
)
def sensitivity_to_energy_scarcity_high():
    """
    High value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_high()


_ext_constant_sensitivity_to_energy_scarcity_high = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_high",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_to_energy_scarcity_high",
)


@component.add(
    name="sensitivity to energy scarcity Low",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_to_energy_scarcity_low"},
)
def sensitivity_to_energy_scarcity_low():
    """
    Low value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_low()


_ext_constant_sensitivity_to_energy_scarcity_low = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_low",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_to_energy_scarcity_low",
)


@component.add(
    name="sensitivity to energy scarcity Medium",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_to_energy_scarcity_medium"},
)
def sensitivity_to_energy_scarcity_medium():
    """
    Medium value option of sensitivity to energy scarcity.
    """
    return _ext_constant_sensitivity_to_energy_scarcity_medium()


_ext_constant_sensitivity_to_energy_scarcity_medium = ExtConstant(
    "../energy.xlsx",
    "Global",
    "sensitivity_scarcity_medium",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_to_energy_scarcity_medium",
)


@component.add(
    name="sensitivity to scarcity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_to_scarcity_option": 2,
        "sensitivity_to_energy_scarcity_low": 1,
        "sensitivity_to_energy_scarcity_medium": 1,
        "sensitivity_to_energy_scarcity_high": 1,
    },
)
def sensitivity_to_scarcity():
    """
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


@component.add(
    name="sensitivity to scarcity H",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_to_scarcity_option_h": 2,
        "sensitivity_to_energy_scarcity_low": 1,
        "sensitivity_to_energy_scarcity_medium": 1,
        "sensitivity_to_energy_scarcity_high": 1,
    },
)
def sensitivity_to_scarcity_h():
    """
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


@component.add(
    name="sensitivity to scarcity option",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_to_scarcity_option"},
)
def sensitivity_to_scarcity_option():
    """
    Option defined by user about the sensitivity of economic sectors to energy scarcity: 1-Low 2-Medium 3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option()


_ext_constant_sensitivity_to_scarcity_option = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_to_scarcity_option",
)


@component.add(
    name="sensitivity to scarcity option H",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sensitivity_to_scarcity_option_h"},
)
def sensitivity_to_scarcity_option_h():
    """
    Option defined by user about the sensitivity of households to the energy scarcity: 1-Low 2-Medium 3-High
    """
    return _ext_constant_sensitivity_to_scarcity_option_h()


_ext_constant_sensitivity_to_scarcity_option_h = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "sensitivity_to_scarcity_option_H",
    {},
    _root,
    {},
    "_ext_constant_sensitivity_to_scarcity_option_h",
)


@component.add(
    name="Year final scarcity final fuels",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_final_fuels_counter": 2, "year_init_scarcity_final_fuels": 1},
)
def year_final_scarcity_final_fuels():
    """
    Final year of scarcity of final fuels.
    """
    return if_then_else(
        scarcity_final_fuels_counter() > 0,
        lambda: year_init_scarcity_final_fuels() + scarcity_final_fuels_counter() - 1,
        lambda: xr.DataArray(
            0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@component.add(
    name="Year final scarcity reserves",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_reserves_counter": 2, "year_init_scarcity_reserves": 1},
)
def year_final_scarcity_reserves():
    """
    Final year of scarcity of material reserves.
    """
    return if_then_else(
        scarcity_reserves_counter() > 0,
        lambda: year_init_scarcity_reserves() + scarcity_reserves_counter() - 1,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name="Year final scarcity resources",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scarcity_resources_counter": 2, "year_init_scarcity_resources": 1},
)
def year_final_scarcity_resources():
    """
    Final year of scarcity of materials resources.
    """
    return if_then_else(
        scarcity_resources_counter() > 0,
        lambda: year_init_scarcity_resources() + scarcity_resources_counter() - 1,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    )


@component.add(
    name="Year init scarcity final fuels",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_year_init_scarcity_final_fuels": 1},
    other_deps={
        "_integ_year_init_scarcity_final_fuels": {
            "initial": {},
            "step": {"scarcity_final_fuels_flags": 1, "time_step": 1, "time": 1},
        }
    },
)
def year_init_scarcity_final_fuels():
    """
    Initial year of scarcity of final fuels.
    """
    return _integ_year_init_scarcity_final_fuels()


_integ_year_init_scarcity_final_fuels = Integ(
    lambda: if_then_else(
        scarcity_final_fuels_flags() == 1,
        lambda: xr.DataArray(
            time() / time_step() - 20,
            {"final sources": _subscript_dict["final sources"]},
            ["final sources"],
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


@component.add(
    name="Year init scarcity reserves",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_year_init_scarcity_reserves": 1},
    other_deps={
        "_integ_year_init_scarcity_reserves": {
            "initial": {},
            "step": {"materials_availability_reserves": 1, "time_step": 1, "time": 1},
        }
    },
)
def year_init_scarcity_reserves():
    """
    Initial year of scarcity of material reserves.
    """
    return _integ_year_init_scarcity_reserves()


_integ_year_init_scarcity_reserves = Integ(
    lambda: if_then_else(
        materials_availability_reserves() == 0,
        lambda: xr.DataArray(
            time() * 1 / time_step(),
            {"materials": _subscript_dict["materials"]},
            ["materials"],
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_year_init_scarcity_reserves",
)


@component.add(
    name="Year init scarcity resources",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_year_init_scarcity_resources": 1},
    other_deps={
        "_integ_year_init_scarcity_resources": {
            "initial": {},
            "step": {"materials_availability_resources": 1, "time_step": 1, "time": 1},
        }
    },
)
def year_init_scarcity_resources():
    """
    Initial year of scarcity of material resources.
    """
    return _integ_year_init_scarcity_resources()


_integ_year_init_scarcity_resources = Integ(
    lambda: if_then_else(
        materials_availability_resources() == 0,
        lambda: xr.DataArray(
            time() * 1 / time_step(),
            {"materials": _subscript_dict["materials"]},
            ["materials"],
        ),
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
    ),
    lambda: xr.DataArray(0, {"materials": _subscript_dict["materials"]}, ["materials"]),
    "_integ_year_init_scarcity_resources",
)
