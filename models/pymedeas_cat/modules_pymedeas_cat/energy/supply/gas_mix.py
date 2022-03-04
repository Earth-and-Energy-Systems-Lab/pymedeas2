"""
Module gas_mix
Translated using PySD version 2.2.1
"""


def fed_gas_ej():
    """
    Real Name: FED GAS EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return float(required_fed_by_fuel().loc["gases"])


def gas_aut():
    """
    Real Name: Gas AUT
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_nat_gas_aut_1()


@subs(["primary sources"], _subscript_dict)
def gas_co2_emissions():
    """
    Real Name: Gas Co2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['primary sources']


    """
    return required_fed_by_gas() * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt()


def gas_row():
    """
    Real Name: Gas RoW
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return imports_aut_nat_gas_from_row_ej()


def pes_nat_gas_aut():
    """
    Real Name: PES Nat Gas AUT
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


def pes_nat_gas_row():
    """
    Real Name: PES Nat Gas RoW
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return imports_aut_conv_gas_from_row_ej() + imports_aut_unconv_gas_from_row_ej()


def pes_total_nat_gas():
    """
    Real Name: PES total Nat Gas
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_nat_gas_aut() + pes_nat_gas_row()


def share_biogas_total_pes_gases_aut():
    """
    Real Name: share Biogas total PES Gases AUT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(pes_biogas_for_tfc(), total_pes_gases())


def share_unconv_tot_gas():
    """
    Real Name: share unconv tot gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(
        imports_aut_unconv_gas_from_row_ej() + real_extraction_unconv_gas_ej(),
        pes_total_nat_gas(),
    )


def total_biogas():
    """
    Real Name: TOTAL Biogas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_biogas_for_tfc()


def total_gas_ej():
    """
    Real Name: Total GAS EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        other_gases_required()
        + pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + ped_gases_for_heat_plants_ej()
        + ped_nat_gas_for_gtl_ej()
        + required_fed_by_gas()
    )


def total_gas_pes():
    """
    Real Name: Total GAS PES
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return gas_aut() + gas_row() + total_biogas()


def total_pes_gases():
    """
    Real Name: Total PES Gases
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_biogas_for_tfc() + pes_total_nat_gas()
