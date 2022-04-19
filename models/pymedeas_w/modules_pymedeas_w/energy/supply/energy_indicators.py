"""
Module energy_indicators
Translated using PySD version 3.0.0
"""


@component.add(
    name="Average elec consumption per capita",
    units="kWh/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def average_elec_consumption_per_capita():
    """
    Electricity consumption per capita (kWh per capita).
    """
    return total_fe_elec_consumption_twh() * kwh_per_twh() / population()


@component.add(
    name="Average TPES per capita",
    units="GJ/(year*people)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def average_tpes_per_capita():
    """
    Average Total Primary Energy Supply per capita (GJ per capita).
    """
    return tpes_ej() * gj_per_ej() / population()


@component.add(
    name='"Average TPESpc (without trad biomass)"',
    units="GJ/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def average_tpespc_without_trad_biomass():
    """
    Average per capita TPES without accounting for the energy supplied by traditional biomass. The population considered for estimating the average is not the global population, but the share of the population not relying on traditional biomass for covering their energy uses.
    """
    return (
        tpes_without_trad_biomass() * gj_per_ej() / pop_not_dependent_on_trad_biomass()
    )


@component.add(
    name="GJ per EJ", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def gj_per_ej():
    """
    Conversion from GJ to EJ (1 EJ = 1e9 GJ).
    """
    return 1000000000.0


@component.add(
    name="kWh per TWh", units="kWh/TWh", comp_type="Constant", comp_subtype="Normal"
)
def kwh_per_twh():
    """
    Conversion between kWh and TWh (1 TWh=1e9 kWh).
    """
    return 1000000000.0


@component.add(
    name="Net TFEC per capita",
    units="GJ/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def net_tfec_per_capita():
    return zidz(real_tfec() * gj_per_ej(), population())


@component.add(
    name="Pop not dependent on trad biomass",
    units="people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pop_not_dependent_on_trad_biomass():
    """
    Global population not dependent on traditional biomass.
    """
    return population() - population_dependent_on_trad_biomass()


@component.add(
    name="TFEC from RES per capita",
    units="GJ/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def tfec_from_res_per_capita():
    return zidz(tfec_res_ej() * gj_per_ej(), population())


@component.add(
    name="TFEC per capita",
    units="GJ/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def tfec_per_capita():
    return zidz(real_tfec() * gj_per_ej(), population())


@component.add(
    name="TFEC RES EJ", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def tfec_res_ej():
    """
    Total final energy consumption from RES.
    """
    return (
        fe_tot_generation_all_res_elec_ej()
        + fes_res_for_heat_ej()
        + pe_traditional_biomass_consum_ej()
        + fes_total_biofuels()
        + fes_total_biogas()
    )


@component.add(
    name='"TPES (without trad biomass)"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def tpes_without_trad_biomass():
    """
    TPES without accounting for traditional biomass.
    """
    return tpes_ej() - pe_traditional_biomass_ej_delayed_1yr()
