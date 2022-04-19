"""
Module total_number_vehicles
Translated using PySD version 3.0.0
"""


@component.add(
    name='"share elec+hyb light vehicles"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_elechyb_light_vehicles():
    """
    Share of electricity+hybrid LD vehicles
    """
    return (
        total_number_hybrid_light_vehicles() + total_number_elec_light_vehicles()
    ) / total_number_light_vehicles()


@component.add(
    name="share of electric light vehicles",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_of_electric_light_vehicles():
    """
    Share of electric LD vehicles
    """
    return total_number_elec_light_vehicles() / total_number_light_vehicles()


@component.add(
    name="total number elec light vehicles",
    units="vehicle",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_number_elec_light_vehicles():
    """
    Total number of light electric vehicles, households+cargo (battery based+plug in hybrid)
    """
    return float(number_vehicles_h().loc["elec 4wheels"]) + float(
        vehicles_inlandt().loc["LV elec"]
    )


@component.add(
    name="total number gas light vehicles",
    units="vehicle",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_number_gas_light_vehicles():
    """
    Total number of light gas vehicles, households+cargo
    """
    return float(number_vehicles_h().loc["gas 4wheels"]) + float(
        vehicles_inlandt().loc["LV gas"]
    )


@component.add(
    name="total number hybrid light vehicles",
    units="vehicle",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_number_hybrid_light_vehicles():
    """
    Total number of light hybrid vehicles, households+cargo
    """
    return float(number_vehicles_h().loc["hib 4wheels"]) + float(
        vehicles_inlandt().loc["LV hib"]
    )


@component.add(
    name="total number light vehicles",
    units="Mvehicles",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_number_light_vehicles():
    """
    Total number of ligth duty vehicles (cargo+households)
    """
    return (
        float(number_vehicles_h().loc["liq 4wheels"])
        + float(number_vehicles_h().loc["hib 4wheels"])
        + float(number_vehicles_h().loc["elec 4wheels"])
        + float(number_vehicles_h().loc["gas 4wheels"])
        + float(vehicles_inlandt().loc["LV liq"])
        + float(vehicles_inlandt().loc["LV elec"])
        + float(vehicles_inlandt().loc["LV hib"])
        + float(vehicles_inlandt().loc["LV gas"])
    )
