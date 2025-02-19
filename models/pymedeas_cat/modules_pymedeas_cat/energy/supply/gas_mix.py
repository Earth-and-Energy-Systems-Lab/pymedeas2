"""
Module gas_mix
Translated using PySD version 3.2.0
"""


@component.add(
    name="FED GAS EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def fed_gas_ej():
    return float(required_fed_by_fuel().loc["gases"])


@component.add(
    name="Gas AUT",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_aut_1": 1},
)
def gas_aut():
    return pes_nat_gas_aut_1()


@component.add(
    name="Gas Co2 emissions",
    units="GtCO2/Year",
    subscripts=["primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gas": 1,
        "gco2_per_mj_conv_gas": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def gas_co2_emissions():
    return xr.DataArray(
        required_fed_by_gas() * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt(),
        {"primary sources": _subscript_dict["primary sources"]},
        ["primary sources"],
    )


@component.add(
    name="Gas RoW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_aut_nat_gas_from_row_ej": 1},
)
def gas_row():
    return imports_aut_nat_gas_from_row_ej()


@component.add(
    name="PES Nat Gas AUT",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_extraction_conv_gas_ej": 1, "real_extraction_unconv_gas_ej": 1},
)
def pes_nat_gas_aut():
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


@component.add(
    name="PES Nat Gas RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_aut_conv_gas_from_row_ej": 1,
        "imports_aut_unconv_gas_from_row_ej": 1,
    },
)
def pes_nat_gas_row():
    return imports_aut_conv_gas_from_row_ej() + imports_aut_unconv_gas_from_row_ej()


@component.add(
    name="PES total Nat Gas",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_aut": 1, "pes_nat_gas_row": 1},
)
def pes_total_nat_gas():
    return pes_nat_gas_aut() + pes_nat_gas_row()


@component.add(
    name="share Biogas total PES Gases AUT",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_tfc": 1, "total_pes_gases": 1},
)
def share_biogas_total_pes_gases_aut():
    return zidz(pes_biogas_for_tfc(), total_pes_gases())


@component.add(
    name="share unconv tot gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_aut_unconv_gas_from_row_ej": 1,
        "real_extraction_unconv_gas_ej": 1,
        "pes_total_nat_gas": 1,
    },
)
def share_unconv_tot_gas():
    return zidz(
        imports_aut_unconv_gas_from_row_ej() + real_extraction_unconv_gas_ej(),
        pes_total_nat_gas(),
    )


@component.add(
    name="TOTAL Biogas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_tfc": 1},
)
def total_biogas():
    return pes_biogas_for_tfc()


@component.add(
    name="Total GAS EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_gases_required": 1,
        "pe_demand_gas_elec_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "required_fed_by_gas": 1,
    },
)
def total_gas_ej():
    return (
        other_gases_required()
        + pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + ped_gases_for_heat_plants_ej()
        + ped_nat_gas_for_gtl_ej()
        + required_fed_by_gas()
    )


@component.add(
    name="Total GAS PES",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_aut": 1, "gas_row": 1, "total_biogas": 1},
)
def total_gas_pes():
    return gas_aut() + gas_row() + total_biogas()


@component.add(
    name="Total PES Gases",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_tfc": 1, "pes_total_nat_gas": 1},
)
def total_pes_gases():
    return pes_biogas_for_tfc() + pes_total_nat_gas()
