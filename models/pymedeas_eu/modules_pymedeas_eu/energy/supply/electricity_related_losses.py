"""
Module energy.supply.electricity_related_losses
Translated using PySD version 3.14.1
"""

@component.add(
    name="Elec gen related losses EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_losses_nre_elec_generation": 1, "pe_losses_res_for_elec": 1},
)
def elec_gen_related_losses_ej():
    """
    Electricity generation losses (EJ).
    """
    return pe_losses_nre_elec_generation() + pe_losses_res_for_elec()


@component.add(
    name="Gen losses vs PE for elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "elec_gen_related_losses_ej": 1,
        "total_pe_for_electricity_consumption_ej": 1,
    },
)
def gen_losses_vs_pe_for_elec():
    """
    Generation losses as a share of the total PE for electricity.
    """
    return elec_gen_related_losses_ej() / total_pe_for_electricity_consumption_ej()


@component.add(
    name="PE losses biogas for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_elec": 1, "fes_elec_from_biogas": 1},
)
def pe_losses_biogas_for_elec():
    return pes_tot_biogas_for_elec() - fes_elec_from_biogas()


@component.add(
    name="PE losses FF for elec",
    units="EJ/year",
    subscripts=["matter final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gen_losses_demand_for_chp_plants": 1,
        "share_efficiency_ff_for_elec_in_chp_plants": 1,
        "gen_losses_demand_for_elec_plants_ej": 1,
    },
)
def pe_losses_ff_for_elec():
    return (
        gen_losses_demand_for_chp_plants()
        * share_efficiency_ff_for_elec_in_chp_plants()
        + gen_losses_demand_for_elec_plants_ej()
    )


@component.add(
    name="PE losses NRE elec generation",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_losses_ff_for_elec": 1, "pe_losses_uranium_for_elec_ej": 1},
)
def pe_losses_nre_elec_generation():
    """
    Losses for electricity generation from non-renewable energy resources.
    """
    return (
        sum(
            pe_losses_ff_for_elec().rename(
                {"matter final sources": "matter final sources!"}
            ),
            dim=["matter final sources!"],
        )
        + pe_losses_uranium_for_elec_ej()
    )


@component.add(
    name="PE losses RES for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_losses_bioe_for_elec_ej": 1,
        "pe_losses_biogas_for_elec": 1,
        "pe_losses_waste_for_elec": 1,
    },
)
def pe_losses_res_for_elec():
    return (
        pe_losses_bioe_for_elec_ej()
        + pe_losses_biogas_for_elec()
        + pe_losses_waste_for_elec()
    )


@component.add(
    name="PE losses uranium for Elec EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium": 1,
        "extraction_uranium_row": 1,
        "efficiency_uranium_for_electricity": 1,
    },
)
def pe_losses_uranium_for_elec_ej():
    """
    (Primary) Energy losses in the generation of electricity in nuclear power centrals.
    """
    return (extraction_uranium() + extraction_uranium_row()) * (
        1 - efficiency_uranium_for_electricity()
    )


@component.add(
    name="PE losses waste for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_waste_for_elec": 1, "fes_elec_from_waste_ej": 1},
)
def pe_losses_waste_for_elec():
    return pes_tot_waste_for_elec() - fes_elec_from_waste_ej()


@component.add(
    name="real PED intensity of Electricity",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_ej": 1,
        "elec_gen_related_losses_ej": 1,
        "nvs_1_year": 1,
        "gdp_eu": 1,
    },
)
def real_ped_intensity_of_electricity():
    """
    Primary energy demand intensity of the electricity sector. Note that the parameter "'a' I-ELEC projection" refers to final energy while here we refer to primary energy. The "real PED intensity of electricity" may thus decrease with the penetration of RES in the electricity generation (see "share RES vs NRE electricity generation").
    """
    return zidz(
        (total_fe_elec_demand_ej() + elec_gen_related_losses_ej()) * nvs_1_year(),
        gdp_eu(),
    )


@component.add(
    name="Total electrical losses EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "elec_gen_related_losses_ej": 1,
        "electrical_distribution_losses_ej": 1,
    },
)
def total_electrical_losses_ej():
    """
    Total losses from electricity generation (generation + distribution).
    """
    return elec_gen_related_losses_ej() + electrical_distribution_losses_ej()


@component.add(
    name="Total PE for electricity consumption EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_ej": 1, "elec_gen_related_losses_ej": 1},
)
def total_pe_for_electricity_consumption_ej():
    """
    Total primary energy for electricity consumption (EJ).
    """
    return total_fe_elec_demand_ej() + elec_gen_related_losses_ej()
