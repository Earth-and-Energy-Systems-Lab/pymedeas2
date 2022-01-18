"""
Module adjust_noncommercial_heat_demand
Translated using PySD version 2.2.0
"""


@subs(["final sources"], _subscript_dict)
def fed_by_fuel_for_heatnc():
    """
    Real Name: "FED by fuel for heat-nc"
    Original Eqn:
      0
      0
      "FED oil for heat-nc"
      "FED nat. gas for heat-nc"
      "FED coal for heat-nc"+"FED solid bioE for heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: ['final sources']

    Final energy demand (excluding distribution and generation losses) of
        non-commercial heat by final fuel.
    """
    return xrmerge(
        xr.DataArray(0, {"final sources": ["electricity"]}, ["final sources"]),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
        rearrange(
            fed_oil_for_heatnc(), ["final sources"], {"final sources": ["liquids"]}
        ),
        rearrange(
            fed_nat_gas_for_heatnc(), ["final sources"], {"final sources": ["gases"]}
        ),
        rearrange(
            fed_coal_for_heatnc() + fed_solid_bioe_for_heatnc(),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


def fed_coal_for_heatnc():
    """
    Real Name: "FED coal for heat-nc"
    Original Eqn: Required FED by fuel before heat correction[solids]*(share FEH over FED by final fuel[solids]-share FEH over FED solid bioE)*efficiency coal for heat plants /(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand (excluding distribution and generation losses) of
        non-commercial heat from coal.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["solids"])
        * (
            float(share_feh_over_fed_by_final_fuel().loc["solids"])
            - share_feh_over_fed_solid_bioe()
        )
        * efficiency_coal_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


def fed_nat_gas_for_heatnc():
    """
    Real Name: "FED nat. gas for heat-nc"
    Original Eqn: Required FED by fuel before heat correction[gases]*share FEH over FED by final fuel[gases]*efficiency gases for heat plants/(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand (excluding distribution and generation losses) of
        non-commercial heat from natural gas.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["gases"])
        * float(share_feh_over_fed_by_final_fuel().loc["gases"])
        * efficiency_gases_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


def fed_nre_for_heatnc():
    """
    Real Name: "FED NRE for heat-nc"
    Original Eqn: "FED coal for heat-nc"+"FED nat. gas for heat-nc"+"FED oil for heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fed_coal_for_heatnc() + fed_nat_gas_for_heatnc() + fed_oil_for_heatnc()


def fed_oil_for_heatnc():
    """
    Real Name: "FED oil for heat-nc"
    Original Eqn: Required FED by fuel before heat correction[liquids]*share FEH over FED by final fuel[liquids]*efficiency liquids for heat plants/(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand (excluding distribution and generation losses) of
        non-commercial heat from oil.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["liquids"])
        * float(share_feh_over_fed_by_final_fuel().loc["liquids"])
        * efficiency_liquids_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


def fed_solid_bioe_for_heatnc():
    """
    Real Name: "FED solid bioE for heat-nc"
    Original Eqn: Required FED by fuel before heat correction[solids]*share FEH over FED solid bioE*Efficiency conversion BioE plants to heat/(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand (excluding distribution and generation losses) of
        non-commercial heat from solid bioenergy.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["solids"])
        * share_feh_over_fed_solid_bioe()
        * efficiency_conversion_bioe_plants_to_heat()
        / (1 + share_heat_distribution_losses())
    )


def ratio_fed_for_heatnc_vs_fed_for_heatcom():
    """
    Real Name: "ratio FED for heat-nc vs FED for heat-com"
    Original Eqn: SUM("FED by fuel for heat-nc"[final sources!])*ZIDZ( 1, Required FED by fuel before heat correction[heat] )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio FED for non-commercial heat vs FED for commercial heat (before
        climate change impacts).
    """
    return sum(fed_by_fuel_for_heatnc(), dim=("final sources",)) * zidz(
        1, float(required_fed_by_fuel_before_heat_correction().loc["heat"])
    )


def share_fed_coal_vs_nre_heatnc():
    """
    Real Name: "share FED coal vs NRE heat-nc"
    Original Eqn: ZIDZ( "FED coal for heat-nc", "FED NRE for heat-nc" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share coal vs non-renewable energy sources for non-commercial heat
        generation.
    """
    return zidz(fed_coal_for_heatnc(), fed_nre_for_heatnc())


def share_fed_gas_vs_nre_heatnc():
    """
    Real Name: "share FED gas vs NRE heat-nc"
    Original Eqn: ZIDZ( "FED nat. gas for heat-nc", "FED NRE for heat-nc" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share gas vs non-renewable energy sources for non-commercial heat
        generation.
    """
    return zidz(fed_nat_gas_for_heatnc(), fed_nre_for_heatnc())


def share_fed_liquids_vs_nre_heatnc():
    """
    Real Name: "share FED liquids vs NRE heat-nc"
    Original Eqn: ZIDZ( "FED oil for heat-nc", "FED NRE for heat-nc" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share liquids vs non-renewable energy sources for non-commercial heat
        generation.
    """
    return zidz(fed_oil_for_heatnc(), fed_nre_for_heatnc())


@subs(["final sources"], _subscript_dict)
def share_feh_over_fed_by_final_fuel():
    """
    Real Name: share FEH over FED by final fuel
    Original Eqn:
      0
      0
      share FEH over FED oil
      "share FEH over FED nat. gas"
      (share FEH over FED coal+share FEH over FED solid bioE)
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['final sources']

    Share FEH over FED by final fuel.
    """
    return xrmerge(
        xr.DataArray(0, {"final sources": ["electricity"]}, ["final sources"]),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
        rearrange(
            share_feh_over_fed_oil(), ["final sources"], {"final sources": ["liquids"]}
        ),
        rearrange(
            share_feh_over_fed_nat_gas(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            (share_feh_over_fed_coal() + share_feh_over_fed_solid_bioe()),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


def share_feh_over_fed_coal():
    """
    Real Name: share FEH over FED coal
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_feh_over_fed_coal')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Estimated share of FEH over FED for coal solids (IEA, 2014 and own
        calculations).
    """
    return _ext_constant_share_feh_over_fed_coal()


def share_feh_over_fed_nat_gas():
    """
    Real Name: "share FEH over FED nat. gas"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_feh_over_fed_nat_gas')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Estimated share of FEH over FED for gases (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_nat_gas()


def share_feh_over_fed_oil():
    """
    Real Name: share FEH over FED oil
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_feh_over_fed_oil')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Estimated share of FEH over FED for liquids (IEA, 2014 and own
        calculations).
    """
    return _ext_constant_share_feh_over_fed_oil()


def share_feh_over_fed_solid_bioe():
    """
    Real Name: share FEH over FED solid bioE
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'share_feh_over_fed_solids_bioe')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Estimated share of FEH over FED for solid bioenergy for the year 2011
        (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_solid_bioe()


_ext_constant_share_feh_over_fed_coal = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_feh_over_fed_coal",
    {},
    _root,
    "_ext_constant_share_feh_over_fed_coal",
)


_ext_constant_share_feh_over_fed_nat_gas = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_feh_over_fed_nat_gas",
    {},
    _root,
    "_ext_constant_share_feh_over_fed_nat_gas",
)


_ext_constant_share_feh_over_fed_oil = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_feh_over_fed_oil",
    {},
    _root,
    "_ext_constant_share_feh_over_fed_oil",
)


_ext_constant_share_feh_over_fed_solid_bioe = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "share_feh_over_fed_solids_bioe",
    {},
    _root,
    "_ext_constant_share_feh_over_fed_solid_bioe",
)
