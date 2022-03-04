"""
Module total_number_vehicles
Translated using PySD version 2.2.1
"""


def share_elechyb_light_vehicles():
    """
    Real Name: "share elec+hyb light vehicles"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of electricity+hybrid LD vehicles
    """
    return (
        total_number_hybrid_light_vehicles() + total_number_elec_light_vehicles()
    ) / total_number_light_vehicles()


def share_of_electric_light_vehicles():
    """
    Real Name: share of electric light vehicles
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of electric LD vehicles
    """
    return total_number_elec_light_vehicles() / total_number_light_vehicles()


def total_number_elec_light_vehicles():
    """
    Real Name: total number elec light vehicles
    Original Eqn:
    Units: vehicle
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total number of light electric vehicles, households+cargo (battery based+plug in hybrid)
    """
    return float(number_vehicles_h().loc["elec 4wheels"]) + float(
        vehicles_inlandt().loc["LV elec"]
    )


def total_number_gas_light_vehicles():
    """
    Real Name: total number gas light vehicles
    Original Eqn:
    Units: vehicle
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total number of light gas vehicles, households+cargo
    """
    return float(number_vehicles_h().loc["gas 4wheels"]) + float(
        vehicles_inlandt().loc["LV gas"]
    )


def total_number_hybrid_light_vehicles():
    """
    Real Name: total number hybrid light vehicles
    Original Eqn:
    Units: vehicle
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total number of light hybrid vehicles, households+cargo
    """
    return float(number_vehicles_h().loc["hib 4wheels"]) + float(
        vehicles_inlandt().loc["LV hib"]
    )


def total_number_light_vehicles():
    """
    Real Name: total number light vehicles
    Original Eqn:
    Units: Mvehicles
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
