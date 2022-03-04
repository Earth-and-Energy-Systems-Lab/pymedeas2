"""
Module heat_total_pes_delete
Translated using PySD version 2.2.1
"""


def pes_nre_heat():
    """
    Real Name: PES NRE heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_nre_heatcom() + pes_nre_heatnc()


def pes_nre_heatcom():
    """
    Real Name: "PES NRE Heat-com"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pes_coal_for_heatcom_plants()
        + pes_nat_gas_for_heatcom_plants()
        + pes_oil_for_heatcom_plants()
    )


def pes_nre_heatnc():
    """
    Real Name: "PES NRE Heat-nc"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pes_coal_for_heatnc_plants()
        + pes_nat_gas_for_heatnc_plants()
        + pes_oil_for_heatnc_plants()
    )


@subs(["RES heat"], _subscript_dict)
def pes_res_for_heat_by_techn():
    """
    Real Name: PES RES for heat by techn
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Primary energy supply of heat from renewable energy sources.
    """
    return pes_dem_res_for_heatcom_by_techn() + pes_dem_res_for_heatnc_by_techn()


def pes_tot_res_for_heat():
    """
    Real Name: PES tot RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy of RES for heat (all technologies: biogas, solids bioenergy, solar and geothermal).
    """
    return pes_tot_biogas_for_heatcom() + sum(
        pes_res_for_heat_by_techn().rename({"RES heat": "RES heat!"}), dim=["RES heat!"]
    )


def tpes_heat():
    """
    Real Name: TPES heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_nre_heat() + pes_tot_res_for_heat() + pes_tot_waste_for_heatcom()
