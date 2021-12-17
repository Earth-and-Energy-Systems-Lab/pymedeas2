"""
Module total_pes__eh
Translated using PySD version 2.2.0
"""


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


@subs(["RES heat"], _subscript_dict)
def pes_res_for_heat_by_techn():
    """
    Real Name: PES RES for heat by techn
    Original Eqn: "PES DEM RES for heat-com by techn"[RES heat]+"PES DEM RES for heat-nc by techn"[RES heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Primary energy supply of heat from renewable energy sources.
    """
    return pes_dem_res_for_heatcom_by_techn() + pes_dem_res_for_heatnc_by_techn()


def pes_tot_res_for_heat():
    """
    Real Name: PES tot RES for heat
    Original Eqn: "PES tot biogas for heat-com"+SUM(PES RES for heat by techn[RES heat!] )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy of RES for heat (all technologies: biogas, solids
        bioenergy, solar and geothermal).
    """
    return pes_tot_biogas_for_heatcom() + sum(
        pes_res_for_heat_by_techn(), dim=("RES heat",)
    )


def tpes_heat():
    """
    Real Name: TPES heat
    Original Eqn: PES NRE heat+PES tot RES for heat+"PES tot waste for heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nre_heat() + pes_tot_res_for_heat() + pes_tot_waste_for_heatcom()
