"""
Module energy.supply.energy_indicators
Translated using PySD version 3.14.0
"""

@component.add(
    name="Average elec consumption per capita",
    units="kWh/(year*people)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_consumption_twh": 1, "kwh_per_twh": 1, "population": 1},
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
    depends_on={"tpes_ej": 1, "gj_per_ej": 1, "population": 1},
)
def average_tpes_per_capita():
    """
    Average Total Primary Energy Supply per capita (GJ per capita).
    """
    return tpes_ej() * gj_per_ej() / population()


@component.add(
    name='"Average TPESpc (without trad biomass)"',
    units="GJ/(year*people)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tpes_without_trad_biomass": 1,
        "gj_per_ej": 1,
        "pop_not_dependent_on_trad_biomass": 1,
    },
)
def average_tpespc_without_trad_biomass():
    """
    Average per capita TPES without accounting for the energy supplied by traditional biomass. The population considered for estimating the average is not the global population, but the share of the population not relying on traditional biomass for covering their energy uses.
    """
    return (
        tpes_without_trad_biomass() * gj_per_ej() / pop_not_dependent_on_trad_biomass()
    )


@component.add(
    name="GJ per EJ", units="GJ/EJ", comp_type="Constant", comp_subtype="Normal"
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
    name="Net TFEC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tfec": 1, "feist_system": 1},
)
def net_tfec():
    """
    Net total final energy consumption (final energy minus energy invested to produce energy).
    """
    return real_tfec() - feist_system()


@component.add(
    name="Net TFEC per capita",
    units="GJ/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_tfec": 1, "gj_per_ej": 1, "population": 1},
)
def net_tfec_per_capita():
    """
    Net total final energy consumption per capita.
    """
    return zidz(net_tfec() * gj_per_ej(), population())


@component.add(
    name="Physical energy intensity TPES vs final",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_total_final_energy_vs_tpes": 1},
)
def physical_energy_intensity_tpes_vs_final():
    """
    Physical energy intensity
    """
    return 1 / share_total_final_energy_vs_tpes()


@component.add(
    name="Physical energy intensity TPES vs net",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_total_net_energy_vs_tpes": 1},
)
def physical_energy_intensity_tpes_vs_net():
    """
    Physical energy intensity
    """
    return 1 / share_total_net_energy_vs_tpes()


@component.add(
    name="Pop not dependent on trad biomass",
    units="people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "population_dependent_on_trad_biomass": 1},
)
def pop_not_dependent_on_trad_biomass():
    """
    Global population not dependent on traditional biomass.
    """
    return population() - population_dependent_on_trad_biomass()


@component.add(
    name="share total net energy vs TPES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "net_tfec": 1,
        "tpes_ej": 1,
        "total_real_nonenergy_use_consumption_ej": 1,
    },
)
def share_total_net_energy_vs_tpes():
    """
    Share of total net energy vs total primary energy supply (without accounting for non-energy uses).
    """
    return zidz(net_tfec(), tpes_ej() - total_real_nonenergy_use_consumption_ej())


@component.add(
    name="TFEC from RES per capita",
    units="GJ/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tfec_res_ej": 1, "gj_per_ej": 1, "population": 1},
)
def tfec_from_res_per_capita():
    return zidz(tfec_res_ej() * gj_per_ej(), population())


@component.add(
    name="TFEC per capita",
    units="GJ/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tfec": 1, "gj_per_ej": 1, "population": 1},
)
def tfec_per_capita():
    return zidz(real_tfec() * gj_per_ej(), population())


@component.add(
    name="TFEC per capita before heat dem corr",
    units="GJ/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tfec_before_heat_dem_corr": 1, "gj_per_ej": 1, "population": 1},
)
def tfec_per_capita_before_heat_dem_corr():
    return zidz(real_tfec_before_heat_dem_corr() * gj_per_ej(), population())


@component.add(
    name="TFEC RES EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_tot_generation_all_res_elec_ej": 1,
        "fes_res_for_heat": 1,
        "pe_traditional_biomass_consum_ej": 1,
        "fes_total_biofuels_production_ej": 1,
        "pes_biogas_for_tfc": 1,
    },
)
def tfec_res_ej():
    """
    Total final energy consumption from RES.
    """
    return (
        fe_tot_generation_all_res_elec_ej()
        + fes_res_for_heat()
        + pe_traditional_biomass_consum_ej()
        + fes_total_biofuels_production_ej()
        + pes_biogas_for_tfc()
    )


@component.add(
    name='"TPES (without trad biomass)"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tpes_ej": 1, "pe_traditional_biomass_ej_delayed_1yr": 1},
)
def tpes_without_trad_biomass():
    """
    TPES without accounting for traditional biomass.
    """
    return tpes_ej() - pe_traditional_biomass_ej_delayed_1yr()
