"""
Module energy.availability.primary_energy_abundances
Translated using PySD version 3.14.1
"""

@component.add(
    name="Abundance primary sources",
    units="Dmnl",
    subscripts=["primary sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "abundance_coal_world": 1,
        "abundance_total_oil_world": 1,
        "abundance_total_nat_gas_world": 1,
    },
)
def abundance_primary_sources():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    value = xr.DataArray(
        np.nan,
        {"primary sources": _subscript_dict["primary sources"]},
        ["primary sources"],
    )
    value.loc[["coal"]] = abundance_coal_world()
    value.loc[["oil"]] = abundance_total_oil_world()
    value.loc[["natural gas"]] = abundance_total_nat_gas_world()
    value.loc[["others"]] = 1
    return value


@component.add(
    name="increase in perception PS scarcity",
    units="Dmnl/year",
    subscripts=["primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_primary_sources": 1,
        "sensitivity_to_scarcity": 1,
        "perception_in_primary_sources_scarcity": 1,
        "nvs_1_year": 1,
    },
)
def increase_in_perception_ps_scarcity():
    """
    Increase in socieconomic perception of primary sources scarcity of each fuel
    """
    return (
        scarcity_primary_sources()
        * sensitivity_to_scarcity()
        * (1 - perception_in_primary_sources_scarcity())
        / nvs_1_year()
    )


@component.add(
    name="perception in primary sources scarcity",
    units="Dmnl",
    subscripts=["primary sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_perception_in_primary_sources_scarcity": 1},
    other_deps={
        "_integ_perception_in_primary_sources_scarcity": {
            "initial": {},
            "step": {
                "increase_in_perception_ps_scarcity": 1,
                "reduction_in_perception_ps_scarcity": 1,
            },
        }
    },
)
def perception_in_primary_sources_scarcity():
    """
    Perception of primary sources scarcity of each fuel by economic sectors. This perception drives the fuel replacement for electriciy and heat.
    """
    return _integ_perception_in_primary_sources_scarcity()


_integ_perception_in_primary_sources_scarcity = Integ(
    lambda: increase_in_perception_ps_scarcity()
    - reduction_in_perception_ps_scarcity(),
    lambda: xr.DataArray(
        0, {"primary sources": _subscript_dict["primary sources"]}, ["primary sources"]
    ),
    "_integ_perception_in_primary_sources_scarcity",
)


@component.add(
    name='"perception of inter-fuel primary sources scarcity"',
    units="Dmnl",
    subscripts=["primary sources1", "primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_to_scarcity": 4,
        "perception_in_primary_sources_scarcity": 8,
    },
)
def perception_of_interfuel_primary_sources_scarcity():
    """
    Perception of primary energy scarcity between fuels. This perception drives the fuel replacement in electricity and heat sectors. TODO
    """
    value = xr.DataArray(
        np.nan,
        {
            "primary sources1": _subscript_dict["primary sources1"],
            "primary sources": _subscript_dict["primary sources"],
        },
        ["primary sources1", "primary sources"],
    )
    value.loc[["coal"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["coal"]),
                1,
            ),
        )
        .expand_dims({"fossil fuels": ["coal"]}, 0)
        .values
    )
    value.loc[["oil"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["oil"]),
                1,
            ),
        )
        .expand_dims({"fossil fuels": ["oil"]}, 0)
        .values
    )
    value.loc[["natural gas"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["natural gas"]),
                1,
            ),
        )
        .expand_dims({"fossil fuels": ["natural gas"]}, 0)
        .values
    )
    value.loc[["others"], :] = (
        if_then_else(
            sensitivity_to_scarcity() == 0,
            lambda: xr.DataArray(
                0,
                {"primary sources": _subscript_dict["primary sources"]},
                ["primary sources"],
            ),
            lambda: zidz(
                perception_in_primary_sources_scarcity()
                - float(perception_in_primary_sources_scarcity().loc["others"]),
                1,
            ),
        )
        .expand_dims({"primary sources1": ["others"]}, 0)
        .values
    )
    return value


@component.add(
    name="reduction in perception PS scarcity",
    units="Dmnl/year",
    subscripts=["primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perception_in_primary_sources_scarcity": 1,
        "energy_scarcity_forgetting_time": 1,
    },
)
def reduction_in_perception_ps_scarcity():
    """
    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_in_primary_sources_scarcity() / energy_scarcity_forgetting_time()


@component.add(
    name="scarcity primary sources",
    units="Dmnl",
    subscripts=["primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_primary_sources": 1},
)
def scarcity_primary_sources():
    """
    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_primary_sources()
