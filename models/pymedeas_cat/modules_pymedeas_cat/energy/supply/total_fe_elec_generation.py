"""
Module energy.supply.total_fe_elec_generation
Translated using PySD version 3.14.2
"""

@component.add(
    name="Abundance_electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_consumption_twh": 2, "fe_demand_elec_consum_twh": 3},
)
def abundance_electricity():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        total_fe_elec_consumption_twh() > fe_demand_elec_consum_twh(),
        lambda: 1,
        lambda: 1
        - zidz(
            fe_demand_elec_consum_twh() - total_fe_elec_consumption_twh(),
            fe_demand_elec_consum_twh(),
        ),
    )


@component.add(
    name="abundance_NRE_elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_elec_generation_from_nre_twh": 2, "demand_elec_nre_twh": 3},
)
def abundance_nre_elec():
    return if_then_else(
        fe_elec_generation_from_nre_twh() > demand_elec_nre_twh(),
        lambda: 1,
        lambda: 1
        - zidz(
            demand_elec_nre_twh() - fe_elec_generation_from_nre_twh(),
            demand_elec_nre_twh(),
        ),
    )


@component.add(
    name="Annual_growth_rate_electricity_generation_RES_elec_tot",
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
    name="FE_Elec_generation_FF_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_elec_generation_from_fossil_fuels": 1, "ej_per_twh": 1},
)
def fe_elec_generation_ff_twh():
    return (
        sum(
            fe_elec_generation_from_fossil_fuels().rename(
                {"fossil_fuels": "fossil_fuels!"}
            ),
            dim=["fossil_fuels!"],
        )
        / ej_per_twh()
    )


@component.add(
    name="FE_Elec_generation_from_fossil_fuels",
    units="EJ/year",
    subscripts=["fossil_fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_elec_fossil_fuel_chp_plants_ej": 3,
        "share_gas_elec_plants": 1,
        "pec_nat_gas": 1,
        "efficiency_gas_for_electricity": 1,
        "efficiency_coal_for_electricity": 1,
        "pec_coal": 1,
        "share_coal_elec_plants": 1,
        "share_oil_elec_plants": 1,
        "efficiency_liquids_for_electricity": 1,
        "pec_total_oil": 1,
    },
)
def fe_elec_generation_from_fossil_fuels():
    """
    Final energy electricity generation from fossil fuels (TWh).
    """
    value = xr.DataArray(
        np.nan, {"fossil_fuels": _subscript_dict["fossil_fuels"]}, ["fossil_fuels"]
    )
    value.loc[["natural_gas"]] = (
        float(fes_elec_fossil_fuel_chp_plants_ej().loc["natural_gas"])
        + share_gas_elec_plants() * pec_nat_gas() * efficiency_gas_for_electricity()
    )
    value.loc[["coal"]] = (
        float(fes_elec_fossil_fuel_chp_plants_ej().loc["coal"])
        + pec_coal() * share_coal_elec_plants() * efficiency_coal_for_electricity()
    )
    value.loc[["oil"]] = (
        float(fes_elec_fossil_fuel_chp_plants_ej().loc["oil"])
        + pec_total_oil()
        * share_oil_elec_plants()
        * efficiency_liquids_for_electricity()
    )
    return value


@component.add(
    name="FE_Elec_generation_from_NRE_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_fossil_fuels": 1,
        "ej_per_twh": 1,
        "fe_nuclear_elec_generation_twh": 1,
    },
)
def fe_elec_generation_from_nre_twh():
    """
    Electricity generation from non-renewable resources (fossil fuels and uranium).
    """
    return (
        sum(
            fe_elec_generation_from_fossil_fuels().rename(
                {"fossil_fuels": "fossil_fuels!"}
            ),
            dim=["fossil_fuels!"],
        )
        / ej_per_twh()
        + fe_nuclear_elec_generation_twh()
    )


@component.add(
    name="FE_nuclear_Elec_generation_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium_ej_cat": 1,
        "extraction_uranium_row": 1,
        "efficiency_uranium_for_electricity": 1,
        "ej_per_twh": 1,
    },
)
def fe_nuclear_elec_generation_twh():
    """
    Final energy electricity generation from uranium (TWh).
    """
    return (
        (extraction_uranium_ej_cat() + extraction_uranium_row())
        * efficiency_uranium_for_electricity()
        / ej_per_twh()
    )


@component.add(
    name="FE_tot_generation_all_RES_elec_TWh_delayed_1yr",
    units="TWh/year",
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
    lambda: 36,
    time_step,
    "_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr",
)


@component.add(
    name="FES_elec_from_BioW",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_generation_res_elec_twh": 1,
        "fes_elec_from_biogas_twh": 1,
        "fes_elec_from_waste": 1,
    },
)
def fes_elec_from_biow():
    """
    Electricity generation of total bioenergy and waste (to compare with more common statistics).
    """
    return (
        float(real_generation_res_elec_twh().loc["solid_bioE_elec"])
        + fes_elec_from_biogas_twh()
        + fes_elec_from_waste()
    )


@component.add(
    name="share_RES_electricity_generation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_tot_generation_all_res_elec_twh": 1,
        "total_fe_elec_generation_twh_cat": 1,
    },
)
def share_res_electricity_generation():
    """
    Share of RES in the electricity generation.
    """
    return fe_tot_generation_all_res_elec_twh() / total_fe_elec_generation_twh_cat()


@component.add(
    name="Total_FE_Elec_consumption_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_consumption_twh": 1, "ej_per_twh": 1},
)
def total_fe_elec_consumption_ej():
    """
    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses and the energy losses due to impacts of Climate Change.
    """
    return total_fe_elec_consumption_twh() * ej_per_twh()


@component.add(
    name="Total_FE_Elec_consumption_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_demand_elec_consum_twh": 1,
        "total_fe_elec_generation_twh_cat": 1,
        "ej_per_twh": 1,
        "total_electricity_demand_for_synthetic": 1,
        "elec_exports_share": 1,
        "share_transmdistr_elec_losses": 1,
    },
)
def total_fe_elec_consumption_twh():
    """
    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses.
    """
    return float(
        np.minimum(
            fe_demand_elec_consum_twh(),
            (
                total_fe_elec_generation_twh_cat()
                - total_electricity_demand_for_synthetic() / ej_per_twh()
            )
            / (1 + share_transmdistr_elec_losses() + elec_exports_share()),
        )
    )


@component.add(
    name="Total_FE_Elec_generation_TWh_CAT",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_nre_twh": 1,
        "fe_tot_generation_all_res_elec_twh": 1,
        "fes_elec_from_waste": 1,
    },
)
def total_fe_elec_generation_twh_cat():
    """
    Total final energy electricity generation (fossil fuels, nuclear, waste & renewables) (TWh).
    """
    return (
        fe_elec_generation_from_nre_twh()
        + fe_tot_generation_all_res_elec_twh()
        + fes_elec_from_waste()
    )


@component.add(
    name="Year_scarcity_Elec",
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
