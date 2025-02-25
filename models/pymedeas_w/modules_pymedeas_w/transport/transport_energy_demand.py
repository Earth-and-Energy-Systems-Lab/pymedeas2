"""
Module transport.transport_energy_demand
Translated using PySD version 3.14.2
"""

@component.add(
    name="Share_demand_by_fuel_in_transport",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_transport_fed_by_fuel": 1, "transport_tfed": 1},
)
def share_demand_by_fuel_in_transport():
    """
    Share demand by fuel in transport
    """
    return total_transport_fed_by_fuel() / transport_tfed()


@component.add(
    name="Total_transport_FED_by_fuel",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel": 1,
        "transport_fraction": 1,
        "transport_households_final_energy_demand": 1,
    },
)
def total_transport_fed_by_fuel():
    """
    Total energy in transport. This model considers transport the four sector in WIOD related with transport and households transport.
    """
    return (
        sum(
            required_final_energy_by_sector_and_fuel().rename({"sectors": "sectors!"})
            * transport_fraction().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        + transport_households_final_energy_demand()
    )


@component.add(
    name="transport_fraction",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_transport_fraction"},
)
def transport_fraction():
    """
    Sectors of fraction of the sector that are part of transport.
    """
    return _ext_constant_transport_fraction()


_ext_constant_transport_fraction = ExtConstant(
    r"../economy.xlsx",
    "Global",
    "transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_transport_fraction",
)


@component.add(
    name="Transport_TFED",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_transport_fed_by_fuel": 1},
)
def transport_tfed():
    """
    Total Final Energy demand in transport
    """
    return sum(
        total_transport_fed_by_fuel().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )
