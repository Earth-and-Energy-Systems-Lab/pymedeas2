"""
Module total_fe_heat_generation_eh
Translated using PySD version 2.1.0
"""


def abundance_heat():
    """
    Real Name: Abundance heat
    Original Eqn: IF THEN ELSE(Total FE Heat generation EJ>Total FED Heat EJ, 1,1-ZIDZ( Total FED Heat EJ-Total FE Heat generation EJ, Total FED Heat EJ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        total_fe_heat_generation_ej() > total_fed_heat_ej(),
        lambda: 1,
        lambda: 1
        - zidz(
            total_fed_heat_ej() - total_fe_heat_generation_ej(), total_fed_heat_ej()
        ),
    )


def annual_growth_rate_res_for_heat():
    """
    Real Name: Annual growth rate RES for heat
    Original Eqn: -1+FES RES for heat EJ/FES RES for heat delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual growth rate of heat generation from RES.
    """
    return -1 + fes_res_for_heat_ej() / fes_res_for_heat_delayed_1yr()


def fes_heat_from_biow():
    """
    Real Name: FES heat from BioW
    Original Eqn: "FE real supply RES for heat-com tot EJ"+"FE real supply RES for heat-nc tot EJ"+"FES heat-com from biogas EJ"+"FES heat-com from waste EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat generation of total bioenergy and waste (to compare with more common
        statistics).
    """
    return (
        fe_real_supply_res_for_heatcom_tot_ej()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
        + fes_heatcom_from_waste_ej()
    )


def fes_heat_from_coal():
    """
    Real Name: FES Heat from coal
    Original Eqn: ("PES coal for Heat-com plants"+"PES coal for Heat-nc plants")*efficiency coal for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from Heat plants that burn coal (both commercial and non-commercial).
    """
    return (
        pes_coal_for_heatcom_plants() + pes_coal_for_heatnc_plants()
    ) * efficiency_coal_for_heat_plants()


def fes_heat_from_nat_gas():
    """
    Real Name: "FES Heat from nat. gas"
    Original Eqn: ("PES nat. gas for Heat-com plants"+"PES nat. gas for Heat-nc plants" )*efficiency gases for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from Heat plants that burn fossil natural gas (both commercial and
        non-commercial).
    """
    return (
        pes_nat_gas_for_heatcom_plants() + pes_nat_gas_for_heatnc_plants()
    ) * efficiency_gases_for_heat_plants()


def fes_heat_from_oil():
    """
    Real Name: FES Heat from oil
    Original Eqn: ("PES oil for Heat-com plants"+"PES oil for Heat-nc plants")*efficiency liquids for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from Heat plants that burn oil (both commercial and non-commercial).
    """
    return (
        pes_oil_for_heatcom_plants() + pes_oil_for_heatnc_plants()
    ) * efficiency_liquids_for_heat_plants()


def fes_nre_for_heat():
    """
    Real Name: FES NRE for heat
    Original Eqn: "FES heat-com fossil fuels CHP plants EJ"+FES Heat from coal+"FES Heat from nat. gas"+ FES Heat from oil+"FES Heat-com nuclear CHP plants EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from non-renewable energy resources.
    """
    return (
        fes_heatcom_fossil_fuels_chp_plants_ej()
        + fes_heat_from_coal()
        + fes_heat_from_nat_gas()
        + fes_heat_from_oil()
        + fes_heatcom_nuclear_chp_plants_ej()
    )


def fes_res_for_heat_delayed_1yr():
    """
    Real Name: FES RES for heat delayed 1yr
    Original Eqn: DELAY FIXED ( FES RES for heat EJ, 1, 0.04)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from renewable energy sources delayed 1 year.
    """
    return _delayfixed_fes_res_for_heat_delayed_1yr()


def fes_res_for_heat_ej():
    """
    Real Name: FES RES for heat EJ
    Original Eqn: "FE real supply RES for heat-com tot EJ"+"FE real supply RES for heat-nc tot EJ"+"FES heat-com from biogas EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Heat from renewable energy sources.
    """
    return (
        fe_real_supply_res_for_heatcom_tot_ej()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
    )


def pes_coal_for_heatcom_plants():
    """
    Real Name: "PES coal for Heat-com plants"
    Original Eqn: (extraction coal EJ AUT+imports AUT coal from RoW EJ)*"share coal dem for Heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of coal for commercial Heat plants.
    """
    return (
        extraction_coal_ej_aut() + imports_aut_coal_from_row_ej()
    ) * share_coal_dem_for_heatcom()


def pes_coal_for_heatnc_plants():
    """
    Real Name: "PES coal for Heat-nc plants"
    Original Eqn: (extraction coal EJ AUT+imports AUT coal from RoW EJ)*"share coal dem for Heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of coal for non-commercial Heat plants.
    """
    return (
        extraction_coal_ej_aut() + imports_aut_coal_from_row_ej()
    ) * share_coal_dem_for_heatnc()


def pes_nat_gas_for_heatcom_plants():
    """
    Real Name: "PES nat. gas for Heat-com plants"
    Original Eqn: ("PES nat. gas AUT"+"imports AUT nat. gas from RoW EJ")*"share nat. gas dem for Heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of fossil natural gas for commercial Heat plants.
    """
    return (
        pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej()
    ) * share_nat_gas_dem_for_heatcom()


def pes_nat_gas_for_heatnc_plants():
    """
    Real Name: "PES nat. gas for Heat-nc plants"
    Original Eqn: (PES gases-"PED nat. gas for GTL EJ")*"share gases dem for Heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of natural gas for non-commercial Heat plants.
    """
    return (pes_gases() - ped_nat_gas_for_gtl_ej()) * share_gases_dem_for_heatnc()


def pes_oil_for_heatcom_plants():
    """
    Real Name: "PES oil for Heat-com plants"
    Original Eqn: (PES total oil EJ AUT+imports AUT total oil from RoW EJ)*"share oil dem for Heat-com"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of oil for commercial Heat plants.
    """
    return (
        pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej()
    ) * share_oil_dem_for_heatcom()


def pes_oil_for_heatnc_plants():
    """
    Real Name: "PES oil for Heat-nc plants"
    Original Eqn: (PES Liquids EJ)*"share liquids dem for Heat-nc"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of natural oil for non-commercial Heat plants.
    """
    return (pes_liquids_ej()) * share_liquids_dem_for_heatnc()


def share_res_heat_generation():
    """
    Real Name: share RES heat generation
    Original Eqn: FES RES for heat EJ/Total FE Heat generation EJ
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of RES in the total heat generation.
    """
    return fes_res_for_heat_ej() / total_fe_heat_generation_ej()


def total_fe_heat_consumption_ej():
    """
    Real Name: Total FE Heat consumption EJ
    Original Eqn: Total FE Heat generation EJ/(1+Share heat distribution losses)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final heat consumption (fossil fuels, nuclear, waste & renewables)
        (EJ).
    """
    return total_fe_heat_generation_ej() / (1 + share_heat_distribution_losses())


def total_fe_heat_generation_ej():
    """
    Real Name: Total FE Heat generation EJ
    Original Eqn: FES RES for heat EJ+"FES heat-com from waste EJ"+FES NRE for heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final heat generation (fossil fuels, nuclear, waste & renewables)
        (EJ).
    """
    return fes_res_for_heat_ej() + fes_heatcom_from_waste_ej() + fes_nre_for_heat()


def year_scarcity_heat():
    """
    Real Name: Year scarcity Heat
    Original Eqn: IF THEN ELSE(Abundance heat>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_heat() > 0.95, lambda: 0, lambda: time())


_delayfixed_fes_res_for_heat_delayed_1yr = DelayFixed(
    lambda: fes_res_for_heat_ej(),
    lambda: 1,
    lambda: 0.04,
    time_step,
    "_delayfixed_fes_res_for_heat_delayed_1yr",
)
