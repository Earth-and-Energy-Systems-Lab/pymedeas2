"""
Module gas_mix
Translated using PySD version 3.0.0
"""


@component.add(
    name="FED GAS EJ", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fed_gas_ej():
    return float(required_fed_by_fuel().loc["gases"])


@component.add(name="Gas AUT", comp_type="Auxiliary", comp_subtype="Normal")
def gas_aut():
    return pes_nat_gas_aut_1()


@component.add(
    name="Gas Co2 emissions",
    units="GtCO2/Year",
    subscripts=["primary sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gas_co2_emissions():
    return xr.DataArray(
        required_fed_by_gas() * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt(),
        {"primary sources": _subscript_dict["primary sources"]},
        ["primary sources"],
    )


@component.add(name="Gas RoW", comp_type="Auxiliary", comp_subtype="Normal")
def gas_row():
    return imports_aut_nat_gas_from_row_ej()


@component.add(
    name="PES Nat Gas AUT", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_nat_gas_aut():
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


@component.add(
    name="PES Nat Gas RoW", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_nat_gas_row():
    return imports_aut_conv_gas_from_row_ej() + imports_aut_unconv_gas_from_row_ej()


@component.add(
    name="PES total Nat Gas",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_total_nat_gas():
    return pes_nat_gas_aut() + pes_nat_gas_row()


@component.add(
    name="share Biogas total PES Gases AUT",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_biogas_total_pes_gases_aut():
    return zidz(pes_biogas_for_tfc(), total_pes_gases())


@component.add(
    name="share unconv tot gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_unconv_tot_gas():
    return zidz(
        imports_aut_unconv_gas_from_row_ej() + real_extraction_unconv_gas_ej(),
        pes_total_nat_gas(),
    )


@component.add(name="TOTAL Biogas", comp_type="Auxiliary", comp_subtype="Normal")
def total_biogas():
    return pes_biogas_for_tfc()


@component.add(
    name="Total GAS EJ", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="Total GAS PES", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def total_gas_pes():
    return gas_aut() + gas_row() + total_biogas()


@component.add(
    name="Total PES Gases",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_pes_gases():
    return pes_biogas_for_tfc() + pes_total_nat_gas()
