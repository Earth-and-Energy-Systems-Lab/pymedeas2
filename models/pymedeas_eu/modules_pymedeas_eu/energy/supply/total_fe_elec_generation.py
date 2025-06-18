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
    name="FE_Elec_generation_from_fossil_fuels",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fe_gen_elec_fossil_fuel_chp_plants": 3,
        "efficiency_liquids_for_electricity": 1,
        "share_ff_for_electricity": 3,
        "pec_ff": 3,
        "efficiency_gas_for_electricity": 1,
        "efficiency_coal_for_electricity": 1,
    },
)
def fe_elec_generation_from_fossil_fuels():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["liquids"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants().loc["liquids"])
        + float(share_ff_for_electricity().loc["liquids"])
        * float(pec_ff().loc["liquids"])
        * efficiency_liquids_for_electricity()
    )
    value.loc[["gases"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants().loc["gases"])
        + float(share_ff_for_electricity().loc["gases"])
        * float(pec_ff().loc["gases"])
        * efficiency_gas_for_electricity()
    )
    value.loc[["solids"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants().loc["solids"])
        + float(share_ff_for_electricity().loc["solids"])
        * float(pec_ff().loc["solids"])
        * efficiency_coal_for_electricity()
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
                {"matter_final_sources": "matter_final_sources!"}
            ),
            dim=["matter_final_sources!"],
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
        "extraction_uranium": 1,
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
        (extraction_uranium() + extraction_uranium_row())
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
    lambda: 396.6,
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
        "total_fe_elec_generation_twh": 1,
    },
)
def share_res_electricity_generation():
    """
    Share of RES in the electricity generation.
    """
    return fe_tot_generation_all_res_elec_twh() / total_fe_elec_generation_twh()


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
        "total_fe_elec_generation_twh": 1,
        "total_electricity_demand_for_synthetic": 1,
        "ej_per_twh": 1,
        "elec_exports_share": 1,
        "share_trans_and_dist_losses": 1,
    },
)
def total_fe_elec_consumption_twh():
    """
    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses.
    """
    return (
        (
            total_fe_elec_generation_twh()
            - total_electricity_demand_for_synthetic() / ej_per_twh()
        )
        * (1 - elec_exports_share())
        / (1 + share_trans_and_dist_losses())
    )


@component.add(
    name="Total_FE_Elec_generation_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_elec_generation_from_nre_twh": 1,
        "fe_tot_generation_all_res_elec_twh": 1,
        "fes_elec_from_waste": 1,
    },
)
def total_fe_elec_generation_twh():
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
