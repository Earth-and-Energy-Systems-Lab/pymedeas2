"""
Module energy.supply.heat_related_losses
Translated using PySD version 3.14.0
"""

@component.add(
    name="Heat gen related losses EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_losses_nre_heat": 1, "pe_losses_res_for_heat": 1},
)
def heat_gen_related_losses_ej():
    return pe_losses_nre_heat() + pe_losses_res_for_heat()


@component.add(
    name="PE losses biogas for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_heatcom": 1, "fes_heatcom_from_biogas_ej": 1},
)
def pe_losses_biogas_for_heat():
    return pes_tot_biogas_for_heatcom() - fes_heatcom_from_biogas_ej()


@component.add(
    name="PE losses FF for Heat",
    units="EJ/year",
    subscripts=[np.str_("matter final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gen_losses_demand_for_chp_plants": 1,
        "share_efficiency_ff_for_elec_in_chp_plants": 1,
        "gen_losses_demand_for_ff_heat_plants": 1,
    },
)
def pe_losses_ff_for_heat():
    return (
        gen_losses_demand_for_chp_plants()
        * (1 - share_efficiency_ff_for_elec_in_chp_plants())
        + gen_losses_demand_for_ff_heat_plants()
    )


@component.add(
    name="PE losses NRE heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_losses_ff_for_heat": 1, "pe_losses_uranium_for_heat": 1},
)
def pe_losses_nre_heat():
    """
    Primary energy losses of non-renewable heat generation
    """
    return (
        sum(
            pe_losses_ff_for_heat().rename(
                {np.str_("matter final sources"): "matter final sources!"}
            ),
            dim=["matter final sources!"],
        )
        + pe_losses_uranium_for_heat()
    )


@component.add(
    name="PE losses RES for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_losses_biogas_for_heat": 1, "pe_losses_waste_for_heat": 1},
)
def pe_losses_res_for_heat():
    return pe_losses_biogas_for_heat() + pe_losses_waste_for_heat()


@component.add(
    name="PE losses uranium for Heat",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pe_losses_uranium_for_heat():
    """
    MUST BE CALCULATED!
    """
    return 0


@component.add(
    name="PE losses waste for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_waste_for_heatcom": 1, "fes_heatcom_from_waste": 1},
)
def pe_losses_waste_for_heat():
    return pes_tot_waste_for_heatcom() - fes_heatcom_from_waste()
