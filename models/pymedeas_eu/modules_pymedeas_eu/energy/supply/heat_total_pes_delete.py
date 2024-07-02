"""
Module energy.supply.heat_total_pes_delete
Translated using PySD version 3.14.0
"""

@component.add(
    name="PES_NRE_heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nre_heatcom": 1, "pes_nre_heatnc": 1},
)
def pes_nre_heat():
    return pes_nre_heatcom() + pes_nre_heatnc()


@component.add(
    name='"PES_NRE_Heat-com"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_coal_for_heatcom_plants": 1,
        "pes_nat_gas_for_heatcom_plants": 1,
        "pes_oil_for_heatcom_plants": 1,
    },
)
def pes_nre_heatcom():
    return (
        pes_coal_for_heatcom_plants()
        + pes_nat_gas_for_heatcom_plants()
        + pes_oil_for_heatcom_plants()
    )


@component.add(
    name='"PES_NRE_Heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_coal_for_heatnc_plants": 1,
        "pes_nat_gas_for_heatnc_plants": 1,
        "pes_oil_for_heatnc_plants": 1,
    },
)
def pes_nre_heatnc():
    return (
        pes_coal_for_heatnc_plants()
        + pes_nat_gas_for_heatnc_plants()
        + pes_oil_for_heatnc_plants()
    )


@component.add(
    name="PES_RES_for_heat_by_techn",
    units="EJ/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_dem_res_for_heatcom_by_techn": 1,
        "pes_dem_res_for_heatnc_by_techn": 1,
    },
)
def pes_res_for_heat_by_techn():
    """
    Primary energy supply of heat from renewable energy sources.
    """
    return pes_dem_res_for_heatcom_by_techn() + pes_dem_res_for_heatnc_by_techn()


@component.add(
    name="PES_tot_RES_for_heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_heatcom": 1, "pes_res_for_heat_by_techn": 1},
)
def pes_tot_res_for_heat():
    """
    Total primary energy of RES for heat (all technologies: biogas, solids bioenergy, solar and geothermal).
    """
    return pes_tot_biogas_for_heatcom() + sum(
        pes_res_for_heat_by_techn().rename({"RES_heat": "RES_heat!"}), dim=["RES_heat!"]
    )


@component.add(
    name="TPES_heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_nre_heat": 1,
        "pes_tot_res_for_heat": 1,
        "pes_tot_waste_for_heatcom": 1,
    },
)
def tpes_heat():
    return pes_nre_heat() + pes_tot_res_for_heat() + pes_tot_waste_for_heatcom()
