"""
Module energy.supply.total_fe_elec_generation
Translated using PySD version 3.9.1
"""


@component.add(
    name="Abundance electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_generation_twh": 2, "total_fe_elec_demand_twh": 3},
)
def abundance_electricity():
    """
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


@component.add(
    name="Annual growth rate electricity generation RES elec tot",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_tot_generation_all_res_elec_twh": 1,
        "fe_tot_generation_all_res_elec_twh_delayed_1yr": 1,
    },
)
def annual_growth_rate_electricity_generation_res_elec_tot():
    """
    Annual growth rate of electricity generation from RES.
    """
    return (
        -1
        + fe_tot_generation_all_res_elec_twh()
        / fe_tot_generation_all_res_elec_twh_delayed_1yr()
    )


@component.add(
    name="FE Elec generation from coal TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_ej": 1,
        "efficiency_coal_for_electricity": 1,
        "share_coal_dem_for_elec": 1,
        "ej_per_twh": 1,
    },
)
def fe_elec_generation_from_coal_twh():
    """
    Final energy electricity generation from coal (TWh).
    """
    return (
        extraction_coal_ej()
        * efficiency_coal_for_electricity()
        * share_coal_dem_for_elec()
        / ej_per_twh()
    )


@component.add(
    name="FE Elec generation from conv gas TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_conv_gas_ej": 1,
        "share_nat_gas_dem_for_elec": 1,
        "efficiency_gas_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def fe_elec_generation_from_conv_gas_twh():
    """
    Final energy electricity generation from conventional gas (TWh).
    """
    return (
        real_extraction_conv_gas_ej()
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


@component.add(
    name="FE Elec generation from fossil fuels TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_coal_twh": 1,
        "fe_elec_generation_from_conv_gas_twh": 1,
        "fe_elec_generation_from_unconv_gas_twh": 1,
        "fe_elec_generation_from_total_oil_twh": 1,
        "fes_elec_fossil_fuel_chp_plants_twh": 1,
    },
)
def fe_elec_generation_from_fossil_fuels_twh():
    """
    Final energy electricity generation from fossil fuels (TWh).
    """
    return (
        fe_elec_generation_from_coal_twh()
        + fe_elec_generation_from_conv_gas_twh()
        + fe_elec_generation_from_unconv_gas_twh()
        + fe_elec_generation_from_total_oil_twh()
        + fes_elec_fossil_fuel_chp_plants_twh()
    )


@component.add(
    name="FE Elec generation from NRE TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_fossil_fuels_twh": 1,
        "fe_nuclear_elec_generation_twh": 1,
    },
)
def fe_elec_generation_from_nre_twh():
    """
    Electricity generation from non-renewable resources (fossil fuels and uranium).
    """
    return fe_elec_generation_from_fossil_fuels_twh() + fe_nuclear_elec_generation_twh()


@component.add(
    name="FE Elec generation from total oil TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_oil_ej": 1,
        "share_oil_dem_for_elec": 1,
        "efficiency_liquids_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def fe_elec_generation_from_total_oil_twh():
    """
    Electricity generation (final energy) from total oil.
    """
    return (
        pes_oil_ej()
        * share_oil_dem_for_elec()
        * efficiency_liquids_for_electricity()
        / ej_per_twh()
    )


@component.add(
    name="FE Elec generation from unconv gas TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_unconv_gas_ej": 1,
        "share_nat_gas_dem_for_elec": 1,
        "efficiency_gas_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def fe_elec_generation_from_unconv_gas_twh():
    """
    Final energy electricity generation from unconventional gas (TWh).
    """
    return (
        real_extraction_unconv_gas_ej()
        * share_nat_gas_dem_for_elec()
        * efficiency_gas_for_electricity()
        / ej_per_twh()
    )


@component.add(
    name="FE nuclear Elec generation TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium_ej": 1,
        "efficiency_uranium_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def fe_nuclear_elec_generation_twh():
    """
    Final energy electricity generation from uranium (TWh).
    """
    return extraction_uranium_ej() * efficiency_uranium_for_electricity() / ej_per_twh()


@component.add(
    name="FE tot generation all RES elec TWh delayed 1yr",
    units="Tdollars/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr": 1},
    other_deps={
        "_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr": {
            "initial": {},
            "step": {"fe_tot_generation_all_res_elec_twh": 1},
        }
    },
)
def fe_tot_generation_all_res_elec_twh_delayed_1yr():
    """
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


@component.add(
    name="FES elec from BioW",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_generation_res_elec_twh": 1,
        "fes_elec_from_biogas_twh": 1,
        "fes_elec_from_waste_twh": 1,
    },
)
def fes_elec_from_biow():
    """
    Electricity generation of total bioenergy and waste (to compare with more common statistics).
    """
    return (
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        + fes_elec_from_biogas_twh()
        + fes_elec_from_waste_twh()
    )


@component.add(
    name="share RES electricity generation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_tot_generation_all_res_elec_twh": 1,
        "total_fe_elec_generation_twh": 1,
    },
)
def share_res_electricity_generation():
    """
    Share of RES in the electricity generation.
    """
    return fe_tot_generation_all_res_elec_twh() / total_fe_elec_generation_twh()


@component.add(
    name="Total FE Elec consumption TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_generation_twh": 1, "share_transmdistr_elec_losses": 1},
)
def total_fe_elec_consumption_twh():
    """
    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses.
    """
    return total_fe_elec_generation_twh() / (1 + share_transmdistr_elec_losses())


@component.add(
    name="Total FE Elec generation TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_nre_twh": 1,
        "fe_tot_generation_all_res_elec_twh": 1,
        "fes_elec_from_waste_twh": 1,
    },
)
def total_fe_elec_generation_twh():
    """
    Total final energy electricity generation (fossil fuels, nuclear, waste & renewables) (TWh).
    """
    return (
        fe_elec_generation_from_nre_twh()
        + fe_tot_generation_all_res_elec_twh()
        + fes_elec_from_waste_twh()
    )


@component.add(
    name="Year scarcity Elec",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_electricity": 1, "time": 1},
)
def year_scarcity_elec():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_electricity() > 0.95, lambda: 0, lambda: time())
