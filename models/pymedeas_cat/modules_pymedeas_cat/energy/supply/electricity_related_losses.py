"""
Module electricity_related_losses
Translated using PySD version 2.2.0
"""


def elec_gen_related_losses_ej():
    """
    Real Name: Elec gen related losses EJ
    Original Eqn: PE losses NRE elec generation+PE losses RES for elec
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation losses (EJ).
    """
    return pe_losses_nre_elec_generation() + pe_losses_res_for_elec()


def gen_losses_vs_pe_for_elec():
    """
    Real Name: Gen losses vs PE for elec
    Original Eqn: Elec gen related losses EJ/Total PE for electricity consumption EJ
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Generation losses as a share of the total PE for electricity.
    """
    return elec_gen_related_losses_ej() / total_pe_for_electricity_consumption_ej()


def pe_losses_biogas_for_elec():
    """
    Real Name: PE losses biogas for elec
    Original Eqn: PES tot biogas for elec-FES elec from biogas EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_tot_biogas_for_elec() - fes_elec_from_biogas_ej()


def pe_losses_coal_for_elec_ej():
    """
    Real Name: PE losses coal for Elec EJ
    Original Eqn: (extraction coal EJ AUT+imports AUT coal from RoW EJ)*share coal dem for Elec*(1-efficiency coal for electricity )
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    (Primary) Energy losses in the generation of electricity in coal power
        centrals.
    """
    return (
        (extraction_coal_ej_aut() + imports_aut_coal_from_row_ej())
        * share_coal_dem_for_elec()
        * (1 - efficiency_coal_for_electricity())
    )


def pe_losses_conv_gas_for_elec_ej():
    """
    Real Name: PE losses conv gas for Elec EJ
    Original Eqn: (real extraction conv gas EJ+imports AUT conv gas from RoW EJ)*"share nat. gas dem for Elec" *(1-efficiency gas for electricity)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    (Primary) Energy losses in the generation of electricity in gas power
        centrals.
    """
    return (
        (real_extraction_conv_gas_ej() + imports_aut_conv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * (1 - efficiency_gas_for_electricity())
    )


def pe_losses_nre_elec_generation():
    """
    Real Name: PE losses NRE elec generation
    Original Eqn: PE losses coal for Elec EJ+PE losses conv gas for Elec EJ+PE losses oil for Elec EJ+PE losses uncon gas for Elec EJ+PE losses uranium for Elec EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: (PES total oil EJ AUT+imports AUT total oil from RoW EJ)*share oil dem for Elec*(1-efficiency liquids for electricity )
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy losses related with oil for electricity generation.
    """
    return (
        (pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej())
        * share_oil_dem_for_elec()
        * (1 - efficiency_liquids_for_electricity())
    )


def pe_losses_res_for_elec():
    """
    Real Name: PE losses RES for elec
    Original Eqn: PE losses BioE for Elec EJ+PE losses biogas for elec+PE losses waste for elec
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_losses_bioe_for_elec_ej()
        + pe_losses_biogas_for_elec()
        + pe_losses_waste_for_elec()
    )


def pe_losses_uncon_gas_for_elec_ej():
    """
    Real Name: PE losses uncon gas for Elec EJ
    Original Eqn: (real extraction unconv gas EJ+imports AUT unconv gas from RoW EJ )*"share nat. gas dem for Elec" *(1-efficiency gas for electricity)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    (Primary) Energy losses in the generation of electricity in gas power
        centrals.
    """
    return (
        (real_extraction_unconv_gas_ej() + imports_aut_unconv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * (1 - efficiency_gas_for_electricity())
    )


def pe_losses_uranium_for_elec_ej():
    """
    Real Name: PE losses uranium for Elec EJ
    Original Eqn: (extraction uranium EJ AUT+extraction uranium RoW)*(1-efficiency uranium for electricity)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    (Primary) Energy losses in the generation of electricity in nuclear power
        centrals.
    """
    return (extraction_uranium_ej_aut() + extraction_uranium_row()) * (
        1 - efficiency_uranium_for_electricity()
    )


def pe_losses_waste_for_elec():
    """
    Real Name: PE losses waste for elec
    Original Eqn: PES tot waste for elec-FES elec from waste EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_tot_waste_for_elec() - fes_elec_from_waste_ej()


def real_ped_intensity_of_electricity():
    """
    Real Name: real PED intensity of Electricity
    Original Eqn: ZIDZ( (Total FE Elec demand EJ+Elec gen related losses EJ), GDP AUT)
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand intensity of the electricity sector. Note that the
        parameter "'a' I-ELEC projection" refers to final energy while here we
        refer to primary energy. The "real PED intensity of electricity" may thus
        decrease with the penetration of RES in the electricity generation (see
        "share RES vs NRE electricity generation").
    """
    return zidz((total_fe_elec_demand_ej() + elec_gen_related_losses_ej()), gdp_aut())


def total_electrical_losses_ej():
    """
    Real Name: Total electrical losses EJ
    Original Eqn: Elec gen related losses EJ+Electrical distribution losses EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total losses from electricity generation (generation + distribution).
    """
    return elec_gen_related_losses_ej() + electrical_distribution_losses_ej()


def total_pe_for_electricity_consumption_ej():
    """
    Real Name: Total PE for electricity consumption EJ
    Original Eqn: Total FE Elec demand EJ+Elec gen related losses EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy for electricity consumption (EJ).
    """
    return total_fe_elec_demand_ej() + elec_gen_related_losses_ej()
