"""
Module pe_by_energy_source
Translated using PySD version 2.2.0
"""


def pe_biomassheat_generation_ej():
    """
    Real Name: "PE biomass-heat generation EJ"
    Original Eqn: "PES DEM RES for heat-com by techn"[solid bioE heat]+"PES DEM RES for heat-nc by techn"[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(pes_dem_res_for_heatcom_by_techn().loc["solid bioE heat"]) + float(
        pes_dem_res_for_heatnc_by_techn().loc["solid bioE heat"]
    )


def pe_geotheat_generation_ej():
    """
    Real Name: "PE geot-heat generation EJ"
    Original Eqn: "PES DEM RES for heat-com by techn"[geot heat]+"PES DEM RES for heat-nc by techn"[geot heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(pes_dem_res_for_heatcom_by_techn().loc["geot heat"]) + float(
        pes_dem_res_for_heatnc_by_techn().loc["geot heat"]
    )


def pe_geotermical_ej():
    """
    Real Name: PE geotermical EJ
    Original Eqn: "PE geot-elec for Elec generation EJ"+"PE geot-heat generation EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pe_geotelec_for_elec_generation_ej() + pe_geotheat_generation_ej()


def pe_wind_energy_for_elec_ej():
    """
    Real Name: PE wind energy for Elec EJ
    Original Eqn: PE offshore wind for Elec generation EJ+PE onshore wind for Elec generation EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_offshore_wind_for_elec_generation_ej()
        + pe_onshore_wind_for_elec_generation_ej()
    )


def pes_biomass_ej():
    """
    Real Name: PES biomass EJ
    Original Eqn: PE bioE for Elec generation EJ+"PE biomass-heat generation EJ"+"Total PE solid bioE potential heat+elec EJ" +PE traditional biomass demand EJ+PES Biogas EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_bioe_for_elec_generation_ej()
        + pe_biomassheat_generation_ej()
        + total_pe_solid_bioe_potential_heatelec_ej()
        + pe_traditional_biomass_demand_ej()
        + pes_biogas_ej()
    )


def pes_csp_ej():
    """
    Real Name: PES CSP EJ
    Original Eqn: PE CSP for Elec generation EJ+"PES solar-heat for heat"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pe_csp_for_elec_generation_ej() + pes_solarheat_for_heat()


def pes_solarheat_for_heat():
    """
    Real Name: "PES solar-heat for heat"
    Original Eqn: "PES DEM RES for heat-com by techn"[solar heat]+"PES DEM RES for heat-nc by techn"[solar heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(pes_dem_res_for_heatcom_by_techn().loc["solar heat"]) + float(
        pes_dem_res_for_heatnc_by_techn().loc["solar heat"]
    )


def share_res_elect_in_transport():
    """
    Real Name: share RES elect in transport
    Original Eqn: (PE geotermical EJ+PE hydro for Elec generation EJ+PE oceanic for Elec generation EJ+PE solar PV for Elec generation EJ+PE wind energy for Elec EJ+PES CSP EJ)*Share demand electricity in transport
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_geotermical_ej()
        + pe_hydro_for_elec_generation_ej()
        + pe_oceanic_for_elec_generation_ej()
        + pe_solar_pv_for_elec_generation_ej()
        + pe_wind_energy_for_elec_ej()
        + pes_csp_ej()
    ) * share_demand_electricity_in_transport()


def share_res_liquids_in_transport():
    """
    Real Name: share RES liquids in transport
    Original Eqn: ZIDZ(Oil liquids saved by biofuels EJ, Total FEC liquids )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(oil_liquids_saved_by_biofuels_ej(), total_fec_liquids())


def total_fec_liquids():
    """
    Real Name: Total FEC liquids
    Original Eqn: real FE consumption liquids EJ+CTL production+GTL production
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_fe_consumption_liquids_ej() + ctl_production() + gtl_production()
