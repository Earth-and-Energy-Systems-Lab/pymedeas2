"""
Module total_pes
Translated using PySD version 2.2.0
"""


def pes_heat_res():
    """
    Real Name: PES heat RES
    Original Eqn: "PES tot biogas for heat-com"+SUM("PES RES for heat-com by techn"[RES heat!])+SUM("PES RES for heat-nc by techn" [RES heat!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy of RES for heat.
    """
    return (
        pes_tot_biogas_for_heatcom()
        + sum(pes_res_for_heatcom_by_techn(), dim=("RES heat",))
        + sum(pes_res_for_heatnc_by_techn(), dim=("RES heat",))
    )


def pes_nre_heat():
    """
    Real Name: PES NRE heat
    Original Eqn: "PES NRE Heat-com"+"PES NRE Heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nre_heatcom() + pes_nre_heatnc()


def pes_nre_heatcom():
    """
    Real Name: "PES NRE Heat-com"
    Original Eqn: "PES coal for Heat-com plants"+"PES nat. gas for Heat-com plants" +"PES oil for Heat-com plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pes_coal_for_heatcom_plants()
        + pes_nat_gas_for_heatcom_plants()
        + pes_oil_for_heatcom_plants()
    )


def pes_nre_heatnc():
    """
    Real Name: "PES NRE Heat-nc"
    Original Eqn: "PES coal for Heat-nc plants"+"PES nat. gas for Heat-nc plants" +"PES oil for Heat-nc plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pes_coal_for_heatnc_plants()
        + pes_nat_gas_for_heatnc_plants()
        + pes_oil_for_heatnc_plants()
    )


def tpes_heat():
    """
    Real Name: TPES heat
    Original Eqn: PES NRE heat+PES heat RES+"PES tot waste for heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nre_heat() + pes_heat_res() + pes_tot_waste_for_heatcom()
