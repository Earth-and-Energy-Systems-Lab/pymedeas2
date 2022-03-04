"""
Module electricity_related_losses
Translated using PySD version 2.2.1
"""


def elec_gen_related_losses_ej():
    """
    Real Name: Elec gen related losses EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation losses (EJ).
    """
    return pe_losses_nre_elec_generation() + pe_losses_res_for_elec()


def gen_losses_vs_pe_for_elec():
    """
    Real Name: Gen losses vs PE for elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Generation losses as a share of the total PE for electricity.
    """
    return elec_gen_related_losses_ej() / total_pe_for_electricity_consumption_ej()


def pe_losses_biogas_for_elec():
    """
    Real Name: PE losses biogas for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_tot_biogas_for_elec() - fes_elec_from_biogas_ej()


def pe_losses_coal_for_elec_ej():
    """
    Real Name: PE losses coal for Elec EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    (Primary) Energy losses in the generation of electricity in coal power centrals.
    """
    return (
        (extraction_coal_ej_eu() + imports_eu_coal_from_row_ej())
        * share_coal_dem_for_elec()
        * (1 - efficiency_coal_for_electricity())
    )


def pe_losses_conv_gas_for_elec_ej():
    """
    Real Name: PE losses conv gas for Elec EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    (Primary) Energy losses in the generation of electricity in gas power centrals.
    """
    return (
        (real_extraction_conv_gas_ej() + imports_eu_conv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * (1 - efficiency_gas_for_electricity())
    )


def pe_losses_nre_elec_generation():
    """
    Real Name: PE losses NRE elec generation
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Losses for electricity generation from non-renewable energy resources.
    """
    return (
        pe_losses_coal_for_elec_ej()
        + pe_losses_conv_gas_for_elec_ej()
        + pe_losses_oil_for_elec_ej()
        + pe_losses_uncon_gas_for_elec_ej()
        + pe_losses_uranium_for_elec_ej()
    )


def pe_losses_oil_for_elec_ej():
    """
    Real Name: PE losses oil for Elec EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy losses related with oil for electricity generation.
    """
    return (
        (pes_total_oil_ej_eu() + imports_eu_total_oil_from_row_ej())
        * share_oil_dem_for_elec()
        * (1 - efficiency_liquids_for_electricity())
    )


def pe_losses_res_for_elec():
    """
    Real Name: PE losses RES for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pe_losses_bioe_for_elec_ej()
        + pe_losses_biogas_for_elec()
        + pe_losses_waste_for_elec()
    )


def pe_losses_uncon_gas_for_elec_ej():
    """
    Real Name: PE losses uncon gas for Elec EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    (Primary) Energy losses in the generation of electricity in gas power centrals.
    """
    return (
        (real_extraction_unconv_gas_ej() + imports_eu_unconv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * (1 - efficiency_gas_for_electricity())
    )


def pe_losses_uranium_for_elec_ej():
    """
    Real Name: PE losses uranium for Elec EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    (Primary) Energy losses in the generation of electricity in nuclear power centrals.
    """
    return (extraction_uranium_ej_eu() + extraction_uranium_row()) * (
        1 - efficiency_uranium_for_electricity()
    )


def pe_losses_waste_for_elec():
    """
    Real Name: PE losses waste for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_tot_waste_for_elec() - fes_elec_from_waste_ej()


def real_ped_intensity_of_electricity():
    """
    Real Name: real PED intensity of Electricity
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand intensity of the electricity sector. Note that the parameter "'a' I-ELEC projection" refers to final energy while here we refer to primary energy. The "real PED intensity of electricity" may thus decrease with the penetration of RES in the electricity generation (see "share RES vs NRE electricity generation").
    """
    return zidz(total_fe_elec_demand_ej() + elec_gen_related_losses_ej(), gdp_eu())


def total_electrical_losses_ej():
    """
    Real Name: Total electrical losses EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total losses from electricity generation (generation + distribution).
    """
    return elec_gen_related_losses_ej() + electrical_distribution_losses_ej()


def total_pe_for_electricity_consumption_ej():
    """
    Real Name: Total PE for electricity consumption EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy for electricity consumption (EJ).
    """
    return total_fe_elec_demand_ej() + elec_gen_related_losses_ej()
