"""
Module primary_energy_abundances_e
Translated using PySD version 2.1.0
"""


@subs(["primary sources"], _subscript_dict)
def abundance_primary_sources():
    """
    Real Name: Abundance primary sources
    Original Eqn:
      abundance coal World
      abundance total oil World
      "abundance total nat. gas World"
      1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return xrmerge(
        rearrange(
            abundance_coal_world(), ["primary sources"], {"primary sources": ["coal"]}
        ),
        rearrange(
            abundance_total_oil_world(),
            ["primary sources"],
            {"primary sources": ["oil"]},
        ),
        rearrange(
            abundance_total_nat_gas_world(),
            ["primary sources"],
            {"primary sources": ["natural gas"]},
        ),
        xr.DataArray(1, {"primary sources": ["others"]}, ["primary sources"]),
    )


@subs(["primary sources"], _subscript_dict)
def increase_in_perception_ps_scarcity():
    """
    Real Name: increase in perception PS scarcity
    Original Eqn: scarcity primary sources[primary sources]*sensitivity to scarcity *(1-perception in primary sources scarcity[primary sources])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']

    Increase in socieconomic perception of primary sources scarcity of each
        fuel
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
    Original Eqn: INTEG ( increase in perception PS scarcity[primary sources]-reduction in perception PS scarcity[primary sources], 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']

    Perception of primary sources scarcity of each fuel by economic sectors.
        This perception drives the fuel replacement for electriciy and heat.
    """
    return _integ_perception_in_primary_sources_scarcity()


@subs(["primary sources1", "primary sources"], _subscript_dict)
def perception_of_interfuel_primary_sources_scarcity():
    """
    Real Name: "perception of inter-fuel primary sources scarcity"
    Original Eqn:
      IF THEN ELSE(sensitivity to scarcity=0,0,ZIDZ( perception in primary sources scarcity[primary sources]-perception in primary sources scarcity[coal],1))
      IF THEN ELSE(sensitivity to scarcity=0,0,ZIDZ( perception in primary sources scarcity[primary sources]-perception in primary sources scarcity[oil], 1))
      IF THEN ELSE(sensitivity to scarcity=0,0,ZIDZ(perception in primary sources scarcity[primary sources]-perception in primary sources scarcity[natural gas], 1))
      IF THEN ELSE(sensitivity to scarcity=0,0,ZIDZ( perception in primary sources scarcity[primary sources]-perception in primary sources scarcity[others], 1))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources1', 'primary sources']

    Perception of primary energy scarcity between fuels. This perception
        drives the fuel replacement in electricity and heat sectors. TODO
    """
    return xrmerge(
        rearrange(
            if_then_else(
                sensitivity_to_scarcity() == 0,
                lambda: 0,
                lambda: zidz(
                    perception_in_primary_sources_scarcity()
                    - float(perception_in_primary_sources_scarcity().loc["coal"]),
                    1,
                ),
            ),
            ["primary sources1", "primary sources"],
            {
                "primary sources1": ["coal"],
                "primary sources": ["coal", "oil", "natural gas", "others"],
            },
        ),
        rearrange(
            if_then_else(
                sensitivity_to_scarcity() == 0,
                lambda: 0,
                lambda: zidz(
                    perception_in_primary_sources_scarcity()
                    - float(perception_in_primary_sources_scarcity().loc["oil"]),
                    1,
                ),
            ),
            ["primary sources1", "primary sources"],
            {
                "primary sources1": ["oil"],
                "primary sources": ["coal", "oil", "natural gas", "others"],
            },
        ),
        rearrange(
            if_then_else(
                sensitivity_to_scarcity() == 0,
                lambda: 0,
                lambda: zidz(
                    perception_in_primary_sources_scarcity()
                    - float(
                        perception_in_primary_sources_scarcity().loc["natural gas"]
                    ),
                    1,
                ),
            ),
            ["primary sources1", "primary sources"],
            {
                "primary sources1": ["natural gas"],
                "primary sources": ["coal", "oil", "natural gas", "others"],
            },
        ),
        rearrange(
            if_then_else(
                sensitivity_to_scarcity() == 0,
                lambda: 0,
                lambda: zidz(
                    perception_in_primary_sources_scarcity()
                    - float(perception_in_primary_sources_scarcity().loc["others"]),
                    1,
                ),
            ),
            ["primary sources1", "primary sources"],
            {
                "primary sources1": ["others"],
                "primary sources": ["coal", "oil", "natural gas", "others"],
            },
        ),
    )


@subs(["primary sources"], _subscript_dict)
def reduction_in_perception_ps_scarcity():
    """
    Real Name: reduction in perception PS scarcity
    Original Eqn: perception in primary sources scarcity[primary sources]/energy scarcity forgetting time
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']

    Reduction of the perception of energy scarcity of economic sectors due to
        the "forgetting" effect.
    """
    return perception_in_primary_sources_scarcity() / energy_scarcity_forgetting_time()


@subs(["primary sources"], _subscript_dict)
def scarcity_primary_sources():
    """
    Real Name: scarcity primary sources
    Original Eqn: 1-Abundance primary sources[primary sources]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']

    The parameter scarcity varies between (1;0). (Scarcity =1-Abundance)        Scarcity=0 while the supply covers the demand; the closest to 1 indicates
        a higher divergence between supply and demand.
    """
    return 1 - abundance_primary_sources()


@subs(["primary sources"], _subscript_dict)
def _integ_init_perception_in_primary_sources_scarcity():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_in_primary_sources_scarcity
    Limits: None
    Type: setup
    Subs: ['primary sources']

    Provides initial conditions for perception_in_primary_sources_scarcity function
    """
    return 0


@subs(["primary sources"], _subscript_dict)
def _integ_input_perception_in_primary_sources_scarcity():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for perception_in_primary_sources_scarcity
    Limits: None
    Type: component
    Subs: ['primary sources']

    Provides derivative for perception_in_primary_sources_scarcity function
    """
    return increase_in_perception_ps_scarcity() - reduction_in_perception_ps_scarcity()


_integ_perception_in_primary_sources_scarcity = Integ(
    _integ_input_perception_in_primary_sources_scarcity,
    _integ_init_perception_in_primary_sources_scarcity,
    "_integ_perception_in_primary_sources_scarcity",
)
