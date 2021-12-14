"""
Module tfes_by_final_fuel
Translated using PySD version 2.1.0
"""


def share_electricity_vs_tfes():
    """
    Real Name: share electricity vs TFES
    Original Eqn: real FE consumption by fuel[electricity]/SUM(real FE consumption by fuel[ final sources!])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of electricity vs TFES.
    """
    return float(real_fe_consumption_by_fuel().loc["electricity"]) / sum(
        real_fe_consumption_by_fuel(), dim=("final sources",)
    )


def share_gases_vs_tfes():
    """
    Real Name: share gases vs TFES
    Original Eqn: real FE consumption by fuel[gases]/SUM(real FE consumption by fuel[ final sources!])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of gases vs TFES.
    """
    return float(real_fe_consumption_by_fuel().loc["gases"]) / sum(
        real_fe_consumption_by_fuel(), dim=("final sources",)
    )


def share_heat_vs_tfes():
    """
    Real Name: share heat vs TFES
    Original Eqn: real FE consumption by fuel[heat]/SUM(real FE consumption by fuel[ final sources!])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of heat vs TFES.
    """
    return float(real_fe_consumption_by_fuel().loc["heat"]) / sum(
        real_fe_consumption_by_fuel(), dim=("final sources",)
    )


def share_liquids_vs_tfes():
    """
    Real Name: share liquids vs TFES
    Original Eqn: real FE consumption by fuel[liquids]/SUM(real FE consumption by fuel[ final sources!])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of liquids vs TFES.
    """
    return float(real_fe_consumption_by_fuel().loc["liquids"]) / sum(
        real_fe_consumption_by_fuel(), dim=("final sources",)
    )


def share_solids_vs_tfes():
    """
    Real Name: share solids vs TFES
    Original Eqn: real FE consumption by fuel[solids]/SUM(real FE consumption by fuel[ final sources!])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of solids vs TFES.
    """
    return float(real_fe_consumption_by_fuel().loc["solids"]) / sum(
        real_fe_consumption_by_fuel(), dim=("final sources",)
    )
