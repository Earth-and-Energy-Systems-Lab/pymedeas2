"""
Module transport_energy_demand
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def share_demand_by_fuel_in_transport():
    """
    Real Name: Share demand by fuel in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Share demand by fuel in transport
    """
    return total_transport_fed_by_fuel() / transport_tfed()


def share_demand_electricity_in_transport():
    """
    Real Name: Share demand electricity in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of electricity in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["electricity"])


def share_demand_gas_in_transport():
    """
    Real Name: Share demand gas in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of gas in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["gases"])


def share_demand_heat_in_transport():
    """
    Real Name: Share demand heat in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share demand heat in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["heat"])


def share_demand_liquids_in_transport():
    """
    Real Name: Share demand liquids in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of liquids in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["liquids"])


def share_demand_solids_in_transport():
    """
    Real Name: Share demand solids in transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share demand solids in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["solids"])


@subs(["final sources"], _subscript_dict)
def total_transport_fed_by_fuel():
    """
    Real Name: Total transport FED by fuel
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Total energy in transport. This model considers transport the four sector in WIOD related with transport and households transport.
    """
    return (
        sum(
            required_final_energy_by_sector_and_fuel_aut().rename(
                {"sectors": "sectors!"}
            )
            * (
                xr.DataArray(
                    0,
                    {
                        "final sources": _subscript_dict["final sources"],
                        "sectors!": _subscript_dict["sectors"],
                    },
                    ["final sources", "sectors!"],
                )
                + transport_fraction().rename({"sectors": "sectors!"})
            ),
            dim=["sectors!"],
        )
        + transport_households_final_energy_demand()
    )


@subs(["sectors"], _subscript_dict)
def transport_fraction():
    """
    Real Name: transport fraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['sectors']


    """
    return _ext_constant_transport_fraction()


_ext_constant_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_transport_fraction",
)


def transport_tfed():
    """
    Real Name: Transport TFED
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total Final Energy demand in transport
    """
    return sum(
        total_transport_fed_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


def transport_tfed_energy_intensity():
    """
    Real Name: Transport TFED energy intensity
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(transport_tfed(), gdp_aut())
