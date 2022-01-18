"""
Module tped_by_fuel
Translated using PySD version 2.2.0
"""


def check_tpe():
    """
    Real Name: check TPE
    Original Eqn: (TPED by fuel-TPES EJ)*100/TPES EJ
    Units: percent
    Limits: (None, None)
    Type: component
    Subs: None

    Comparison between TPED by fuel and TPED by sector (they should
        correspond).
    """
    return (tped_by_fuel() - tpes_ej()) * 100 / tpes_ej()


def tped_by_fuel():
    """
    Real Name: TPED by fuel
    Original Eqn: extraction uranium EJ AUT+"PE supply RES non-Elec EJ"+PE Elec generation from RES EJ+PED total oil EJ +PED coal EJ+"PED nat. gas EJ"+PES waste EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy demand by fuel.
    """
    return (
        extraction_uranium_ej_aut()
        + pe_supply_res_nonelec_ej()
        + pe_elec_generation_from_res_ej()
        + ped_total_oil_ej()
        + ped_coal_ej()
        + ped_nat_gas_ej()
        + pes_waste_ej()
    )
