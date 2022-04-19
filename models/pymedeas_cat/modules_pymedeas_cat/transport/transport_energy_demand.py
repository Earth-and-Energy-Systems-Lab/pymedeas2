"""
Module transport_energy_demand
Translated using PySD version 3.0.0
"""


@component.add(
    name="Share demand by fuel in transport",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_by_fuel_in_transport():
    """
    Share demand by fuel in transport
    """
    return total_transport_fed_by_fuel() / transport_tfed()


@component.add(
    name="Share demand electricity in transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_electricity_in_transport():
    """
    Share of electricity in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["electricity"])


@component.add(
    name="Share demand gas in transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_gas_in_transport():
    """
    Share of gas in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["gases"])


@component.add(
    name="Share demand heat in transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_heat_in_transport():
    """
    Share demand heat in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["heat"])


@component.add(
    name="Share demand liquids in transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_liquids_in_transport():
    """
    Share of liquids in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["liquids"])


@component.add(
    name="Share demand solids in transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_demand_solids_in_transport():
    """
    Share demand solids in transport
    """
    return float(share_demand_by_fuel_in_transport().loc["solids"])


@component.add(
    name="Total transport FED by fuel",
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_transport_fed_by_fuel():
    """
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


@component.add(
    name="transport fraction",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
)
def transport_fraction():
    return _ext_constant_transport_fraction()


_ext_constant_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "_ext_constant_transport_fraction",
)


@component.add(
    name="Transport TFED", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def transport_tfed():
    """
    Total Final Energy demand in transport
    """
    return sum(
        total_transport_fed_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Transport TFED energy intensity",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def transport_tfed_energy_intensity():
    return zidz(transport_tfed(), gdp_aut())
