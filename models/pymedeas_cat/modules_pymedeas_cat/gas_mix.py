"""
Module gas_mix
Translated using PySD version 2.1.0
"""


def fed_gas_ej():
    """
    Real Name: FED GAS EJ
    Original Eqn: Required FED by fuel[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(required_fed_by_fuel().loc["gases"])


def gas_aut():
    """
    Real Name: Gas AUT
    Original Eqn: "PES nat. gas AUT"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nat_gas_aut_1()


@subs(["primary sources"], _subscript_dict)
def gas_co2_emissions():
    """
    Real Name: Gas Co2 emissions
    Original Eqn: Required FED by gas*gCO2 per MJ conv gas*MJ per EJ/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: ['primary sources']


    """
    return required_fed_by_gas() * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt()


def gas_row():
    """
    Real Name: Gas RoW
    Original Eqn: "imports AUT nat. gas from RoW EJ"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return imports_aut_nat_gas_from_row_ej()


def pes_nat_gas_aut():
    """
    Real Name: PES Nat Gas AUT
    Original Eqn: real extraction conv gas EJ+real extraction unconv gas EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_extraction_conv_gas_ej() + real_extraction_unconv_gas_ej()


def pes_nat_gas_row():
    """
    Real Name: PES Nat Gas RoW
    Original Eqn: imports AUT conv gas from RoW EJ+imports AUT unconv gas from RoW EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return imports_aut_conv_gas_from_row_ej() + imports_aut_unconv_gas_from_row_ej()


def pes_total_nat_gas():
    """
    Real Name: PES total Nat Gas
    Original Eqn: PES Nat Gas AUT+PES Nat Gas RoW
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nat_gas_aut() + pes_nat_gas_row()


def share_biogas_total_pes_gases_aut():
    """
    Real Name: share Biogas total PES Gases AUT
    Original Eqn: ZIDZ(PES biogas for TFC, Total PES Gases )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(pes_biogas_for_tfc(), total_pes_gases())


def share_unconv_tot_gas():
    """
    Real Name: share unconv tot gas
    Original Eqn: ZIDZ( (imports AUT unconv gas from RoW EJ+real extraction unconv gas EJ ), PES total Nat Gas )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(
        (imports_aut_unconv_gas_from_row_ej() + real_extraction_unconv_gas_ej()),
        pes_total_nat_gas(),
    )


def total_biogas():
    """
    Real Name: TOTAL Biogas
    Original Eqn: PES biogas for TFC
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_biogas_for_tfc()


def total_gas_ej():
    """
    Real Name: Total GAS EJ
    Original Eqn: Other gases required+PE demand gas Elec plants EJ+PED gas for CHP plants EJ+"PED gas Heat-nc" +PED gases for Heat plants EJ+"PED nat. gas for GTL EJ" +Required FED by gas
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: Gas AUT+Gas RoW+TOTAL Biogas
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return gas_aut() + gas_row() + total_biogas()


def total_pes_gases():
    """
    Real Name: Total PES Gases
    Original Eqn: PES biogas for TFC+PES total Nat Gas
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_biogas_for_tfc() + pes_total_nat_gas()
