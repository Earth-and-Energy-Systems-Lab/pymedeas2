"""
Module total_fe_elec_generation
Translated using PySD version 2.2.0
"""


def abundance_electricity():
    """
    Real Name: Abundance electricity
    Original Eqn: IF THEN ELSE(Total FE Elec generation TWh AUT>Total FE Elec demand TWh , 1, 1-ZIDZ( Total FE Elec demand TWh-Total FE Elec generation TWh AUT , Total FE Elec demand TWh ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        total_fe_elec_generation_twh_aut() > total_fe_elec_demand_twh(),
        lambda: 1,
        lambda: 1
        - zidz(
            total_fe_elec_demand_twh() - total_fe_elec_generation_twh_aut(),
            total_fe_elec_demand_twh(),
        ),
    )


def annual_growth_rate_electricity_generation_res_elec_tot():
    """
    Real Name: Annual growth rate electricity generation RES elec tot
    Original Eqn: -1+FE tot generation all RES elec TWh/FE tot generation all RES elec TWh delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual growth rate of electricity generation from RES.
    """
    return (
        -1
        + fe_tot_generation_all_res_elec_twh()
        / fe_tot_generation_all_res_elec_twh_delayed_1yr()
    )


def fe_elec_generation_from_coal_twh():
    """
    Real Name: FE Elec generation from coal TWh
    Original Eqn: (extraction coal EJ AUT+imports AUT coal from RoW EJ)*efficiency coal for electricity*share coal dem for Elec /EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy electricity generation from coal (TWh).
    """
    return (
        (extraction_coal_ej_aut() + imports_aut_coal_from_row_ej())
        * efficiency_coal_for_electricity()
        * share_coal_dem_for_elec()
        / ej_per_twh()
    )


def fe_elec_generation_from_conv_gas_twh():
    """
    Real Name: FE Elec generation from conv gas TWh
    Original Eqn: (real extraction conv gas EJ+imports AUT conv gas from RoW EJ)*"share nat. gas dem for Elec" *efficiency gas for electricity /EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy electricity generation from conventional gas (TWh).
    """
    return (
        (real_extraction_conv_gas_ej() + imports_aut_conv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


def fe_elec_generation_from_fossil_fuels_twh():
    """
    Real Name: FE Elec generation from fossil fuels TWh
    Original Eqn: FE Elec generation from coal TWh+FE Elec generation from conv gas TWh +FE Elec generation from unconv gas TWh +FE Elec generation from total oil TWh+FES Elec fossil fuel CHP plants TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy electricity generation from fossil fuels (TWh).
    """
    return (
        fe_elec_generation_from_coal_twh()
        + fe_elec_generation_from_conv_gas_twh()
        + fe_elec_generation_from_unconv_gas_twh()
        + fe_elec_generation_from_total_oil_twh()
        + fes_elec_fossil_fuel_chp_plants_twh()
    )


def fe_elec_generation_from_nre_twh():
    """
    Real Name: FE Elec generation from NRE TWh
    Original Eqn: FE Elec generation from fossil fuels TWh+FE nuclear Elec generation TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation from non-renewable resources (fossil fuels and
        uranium).
    """
    return fe_elec_generation_from_fossil_fuels_twh() + fe_nuclear_elec_generation_twh()


def fe_elec_generation_from_total_oil_twh():
    """
    Real Name: FE Elec generation from total oil TWh
    Original Eqn: (PES total oil EJ AUT+imports AUT total oil from RoW EJ)*share oil dem for Elec*efficiency liquids for electricity /EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation (final energy) from total oil.
    """
    return (
        (pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej())
        * share_oil_dem_for_elec()
        * efficiency_liquids_for_electricity()
        / ej_per_twh()
    )


def fe_elec_generation_from_unconv_gas_twh():
    """
    Real Name: FE Elec generation from unconv gas TWh
    Original Eqn: (real extraction unconv gas EJ+imports AUT unconv gas from RoW EJ )*"share nat. gas dem for Elec" *efficiency gas for electricity/EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy electricity generation from unconventional gas (TWh).
    """
    return (
        (real_extraction_unconv_gas_ej() + imports_aut_unconv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


def fe_nuclear_elec_generation_twh():
    """
    Real Name: FE nuclear Elec generation TWh
    Original Eqn: (extraction uranium EJ AUT+extraction uranium RoW)*efficiency uranium for electricity/EJ per TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy electricity generation from uranium (TWh).
    """
    return (
        (extraction_uranium_ej_aut() + extraction_uranium_row())
        * efficiency_uranium_for_electricity()
        / ej_per_twh()
    )


def fe_tot_generation_all_res_elec_twh_delayed_1yr():
    """
    Real Name: FE tot generation all RES elec TWh delayed 1yr
    Original Eqn: DELAY FIXED ( FE tot generation all RES elec TWh, 1, 36)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation from all RES technologies. delayed 1 year.
    """
    return _delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr()


def fes_elec_from_biow():
    """
    Real Name: FES elec from BioW
    Original Eqn: real generation RES elec TWh[solid bioE elec]+FES elec from biogas TWh +FES elec from waste TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation of total bioenergy and waste (to compare with more
        common statistics).
    """
    return (
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        + fes_elec_from_biogas_twh()
        + fes_elec_from_waste_twh()
    )


def share_res_electricity_generation():
    """
    Real Name: share RES electricity generation
    Original Eqn: FE tot generation all RES elec TWh/Total FE Elec generation TWh AUT
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of RES in the electricity generation.
    """
    return fe_tot_generation_all_res_elec_twh() / total_fe_elec_generation_twh_aut()


def total_fe_elec_consumption_ej():
    """
    Real Name: Total FE Elec consumption EJ
    Original Eqn: Total FE Elec consumption TWh*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy electricity consumption (fossil fuels, nuclear, waste &
        renewables) (TWh) excluding distribution losses and the energy losses due
        to impacts of Climate Change.
    """
    return total_fe_elec_consumption_twh() * ej_per_twh()


def total_fe_elec_consumption_twh():
    """
    Real Name: Total FE Elec consumption TWh
    Original Eqn: (Total FE Elec generation TWh AUT+"imports/exports electricity" )/(1+"share transm&distr elec losses")
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy electricity consumption (fossil fuels, nuclear, waste &
        renewables) (TWh) excluding distribution losses.
    """
    return (total_fe_elec_generation_twh_aut() + importsexports_electricity()) / (
        1 + share_transmdistr_elec_losses()
    )


def total_fe_elec_generation_twh_aut():
    """
    Real Name: Total FE Elec generation TWh AUT
    Original Eqn: FE Elec generation from NRE TWh+FE tot generation all RES elec TWh +FES elec from waste TWh
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy electricity generation (fossil fuels, nuclear, waste &
        renewables) (TWh).
    """
    return (
        fe_elec_generation_from_nre_twh()
        + fe_tot_generation_all_res_elec_twh()
        + fes_elec_from_waste_twh()
    )


def year_scarcity_elec():
    """
    Real Name: Year scarcity Elec
    Original Eqn: IF THEN ELSE(Abundance electricity>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_electricity() > 0.95, lambda: 0, lambda: time())


_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr = DelayFixed(
    lambda: fe_tot_generation_all_res_elec_twh(),
    lambda: 1,
    lambda: 36,
    time_step,
    "_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr",
)
