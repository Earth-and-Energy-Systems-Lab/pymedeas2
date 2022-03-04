"""
Module primary_energy_abundances
Translated using PySD version 2.2.1
"""


@subs(["primary sources"], _subscript_dict)
def abundance_primary_sources():
    """
    Real Name: Abundance primary sources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary, Constant
    Subs: ['primary sources']

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    value = xr.DataArray(
        np.nan,
        {"primary sources": _subscript_dict["primary sources"]},
        ["primary sources"],
    )
    value.loc[{"primary sources": ["coal"]}] = abundance_coal_world()
    value.loc[{"primary sources": ["oil"]}] = abundance_total_oil_world()
    value.loc[{"primary sources": ["natural gas"]}] = abundance_total_nat_gas_world()
    value.loc[{"primary sources": ["others"]}] = 1
    return value


@subs(["primary sources"], _subscript_dict)
def increase_in_perception_ps_scarcity():
    """
    Real Name: increase in perception PS scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    Increase in socieconomic perception of primary sources scarcity of each fuel
    """
    return (
        scarcity_primary_sources()
        * sensitivity_to_scarcity()
        * (1 - perception_in_primary_sources_scarcity())
    )


@subs(["primary sources"], _subscript_dict)
def perception_in_primary_sources_scarcity():
    """
    Real Name: perception in primary sources scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: ['primary sources']

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


@subs(["primary sources1", "primary sources"], _subscript_dict)
def perception_of_interfuel_primary_sources_scarcity():
    """
    Real Name: "perception of inter-fuel primary sources scarcity"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources1', 'primary sources']

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
    value.loc[
        {
            "primary sources1": ["coal"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["coal"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
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
    ).values
    value.loc[
        {
            "primary sources1": ["oil"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["oil"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
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
    ).values
    value.loc[
        {
            "primary sources1": ["natural gas"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["natural gas"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
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
    ).values
    value.loc[
        {
            "primary sources1": ["others"],
            "primary sources": ["coal", "oil", "natural gas", "others"],
        }
    ] = (
        xr.DataArray(
            0,
            {
                "primary sources1": ["others"],
                "primary sources": _subscript_dict["primary sources"],
            },
            ["primary sources1", "primary sources"],
        )
        + if_then_else(
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
    ).values
    return value


@subs(["primary sources"], _subscript_dict)
def reduction_in_perception_ps_scarcity():
    """
    Real Name: reduction in perception PS scarcity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    Reduction of the perception of energy scarcity of economic sectors due to the "forgetting" effect.
    """
    return perception_in_primary_sources_scarcity() / energy_scarcity_forgetting_time()


@subs(["primary sources"], _subscript_dict)
def scarcity_primary_sources():
    """
    Real Name: scarcity primary sources
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance) Scarcity=0 while the supply covers the demand; the closest to 1 indicates a higher divergence between supply and demand.
    """
    return 1 - abundance_primary_sources()
