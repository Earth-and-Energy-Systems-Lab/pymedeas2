"""
Module heat_total_pes_delete
Translated using PySD version 3.0.1
"""


@component.add(
    name="PES heat RES",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_tot_biogas_for_heatcom": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
    },
)
def pes_heat_res():
    """
    Primary energy of RES for heat.
    """
    return (
        pes_tot_biogas_for_heatcom()
        + sum(
            pes_res_for_heatcom_by_techn().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
        + sum(
            pes_res_for_heatnc_by_techn().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
    )


@component.add(
    name="PES NRE heat",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nre_heatcom": 1, "pes_nre_heatnc": 1},
)
def pes_nre_heat():
    return pes_nre_heatcom() + pes_nre_heatnc()


@component.add(
    name='"PES NRE Heat-com"',
    units="EJ",
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
    name='"PES NRE Heat-nc"',
    units="EJ",
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
    name="TPES heat",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nre_heat": 1, "pes_heat_res": 1, "pes_tot_waste_for_heatcom": 1},
)
def tpes_heat():
    return pes_nre_heat() + pes_heat_res() + pes_tot_waste_for_heatcom()
