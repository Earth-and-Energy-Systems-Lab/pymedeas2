"""
Module transport_energy_demand
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def share_demand_by_fuel_in_transport():
    """
    Real Name: Share demand by fuel in transport
    Original Eqn: Total transport FED by fuel[final sources]/Transport TFED
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Share demand by fuel in transport
    """
    return total_transport_fed_by_fuel() / transport_tfed()


@subs(["final sources"], _subscript_dict)
def total_transport_fed_by_fuel():
    """
    Real Name: Total transport FED by fuel
    Original Eqn: SUM(Required final energy by sector and fuel EU[final sources,sectors!]*transport fraction[sectors!])+Transport households final energy demand[final sources]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Total energy in transport. This model considers transport the four sector
        in WIOD related with transport and households transport.
    """
    return (
        sum(
            required_final_energy_by_sector_and_fuel_eu() * transport_fraction(),
            dim=("sectors",),
        )
        + transport_households_final_energy_demand()
    )


@subs(["sectors"], _subscript_dict)
def transport_fraction():
    """
    Real Name: transport fraction
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Global', 'transport_fraction')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']


    """
    return _ext_constant_transport_fraction()


def transport_tfed():
    """
    Real Name: Transport TFED
    Original Eqn: SUM(Total transport FED by fuel[final sources!])
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total Final Energy demand in transport
    """
    return sum(total_transport_fed_by_fuel(), dim=("final sources",))


def transport_tfed_energy_intensity():
    """
    Real Name: Transport TFED energy intensity
    Original Eqn: ZIDZ( Transport TFED, GDP EU )
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(transport_tfed(), gdp_eu())


_ext_constant_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_transport_fraction",
)
