"""
Module tped_by_fuel_e
Translated using PySD version 2.2.0
"""


def tped_by_fuel():
    """
    Real Name: TPED by fuel
    Original Eqn: extraction uranium EJ EU+"PE supply RES non-Elec EJ"+PE Elec generation from RES EJ+PED total oil EJ +PED coal EJ+"PED nat. gas EJ"+PES waste EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy demand by fuel.
    """
    return (
        extraction_uranium_ej_eu()
        + pe_supply_res_nonelec_ej()
        + pe_elec_generation_from_res_ej()
        + ped_total_oil_ej()
        + ped_coal_ej()
        + ped_nat_gas_ej()
        + pes_waste_ej()
    )
