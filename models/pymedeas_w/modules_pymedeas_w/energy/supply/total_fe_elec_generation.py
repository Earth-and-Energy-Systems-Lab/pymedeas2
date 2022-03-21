"""
Module total_fe_elec_generation
Translated using PySD version 2.2.3
"""


def abundance_electricity():
    """
    Real Name: Abundance electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        total_fe_elec_generation_twh() > total_fe_elec_demand_twh(),
        lambda: 1,
        lambda: 1
        - zidz(
            total_fe_elec_demand_twh() - total_fe_elec_generation_twh(),
            total_fe_elec_demand_twh(),
        ),
    )


def annual_growth_rate_electricity_generation_res_elec_tot():
    """
    Real Name: Annual growth rate electricity generation RES elec tot
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy electricity generation from coal (TWh).
    """
    return (
        extraction_coal_ej()
        * efficiency_coal_for_electricity()
        * share_coal_dem_for_elec()
        / ej_per_twh()
    )


def fe_elec_generation_from_conv_gas_twh():
    """
    Real Name: FE Elec generation from conv gas TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy electricity generation from conventional gas (TWh).
    """
    return (
        real_extraction_conv_gas_ej()
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


def fe_elec_generation_from_fossil_fuels_twh():
    """
    Real Name: FE Elec generation from fossil fuels TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation from non-renewable resources (fossil fuels and uranium).
    """
    return fe_elec_generation_from_fossil_fuels_twh() + fe_nuclear_elec_generation_twh()


def fe_elec_generation_from_total_oil_twh():
    """
    Real Name: FE Elec generation from total oil TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation (final energy) from total oil.
    """
    return (
        pes_oil_ej()
        * share_oil_dem_for_elec()
        * efficiency_liquids_for_electricity()
        / ej_per_twh()
    )


def fe_elec_generation_from_unconv_gas_twh():
    """
    Real Name: FE Elec generation from unconv gas TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy electricity generation from unconventional gas (TWh).
    """
    return (
        real_extraction_unconv_gas_ej()
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


def fe_nuclear_elec_generation_twh():
    """
    Real Name: FE nuclear Elec generation TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy electricity generation from uranium (TWh).
    """
    return extraction_uranium_ej() * efficiency_uranium_for_electricity() / ej_per_twh()


def fe_tot_generation_all_res_elec_twh_delayed_1yr():
    """
    Real Name: FE tot generation all RES elec TWh delayed 1yr
    Original Eqn:
    Units: Tdollars/year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Electricity generation from all RES technologies. delayed 1 year.
    """
    return _delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr()


_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr = DelayFixed(
    lambda: fe_tot_generation_all_res_elec_twh(),
    lambda: 1,
    lambda: 2463,
    time_step,
    "_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr",
)


def fes_elec_from_biow():
    """
    Real Name: FES elec from BioW
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity generation of total bioenergy and waste (to compare with more common statistics).
    """
    return (
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        + fes_elec_from_biogas_twh()
        + fes_elec_from_waste_twh()
    )


def share_res_electricity_generation():
    """
    Real Name: share RES electricity generation
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of RES in the electricity generation.
    """
    return fe_tot_generation_all_res_elec_twh() / total_fe_elec_generation_twh()


def total_fe_elec_consumption_twh():
    """
    Real Name: Total FE Elec consumption TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses.
    """
    return total_fe_elec_generation_twh() / (1 + share_transmdistr_elec_losses())


def total_fe_elec_generation_twh():
    """
    Real Name: Total FE Elec generation TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy electricity generation (fossil fuels, nuclear, waste & renewables) (TWh).
    """
    return (
        fe_elec_generation_from_nre_twh()
        + fe_tot_generation_all_res_elec_twh()
        + fes_elec_from_waste_twh()
    )


def year_scarcity_elec():
    """
    Real Name: Year scarcity Elec
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_electricity() > 0.95, lambda: 0, lambda: time())
