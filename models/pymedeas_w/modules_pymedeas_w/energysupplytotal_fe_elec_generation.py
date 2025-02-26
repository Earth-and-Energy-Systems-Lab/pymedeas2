"""
Module energysupplytotal_fe_elec_generation
Translated using PySD version 3.14.0
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
    name="abundance NRE elec",
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
    name="FE Elec generation from fossil fuels",
    units="EJ/year",
    subscripts=["matter final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fe_gen_elec_fossil_fuel_chp_plants_ej": 3,
        "pes_oil_ej": 1,
        "share_oil_dem_for_elec": 1,
        "efficiency_liquids_for_electricity": 1,
        "share_coal_dem_for_elec": 1,
        "extraction_coal_ej": 1,
        "efficiency_coal_for_electricity": 1,
        "pes_nat_gas": 1,
        "efficiency_gas_for_electricity": 1,
        "share_nat_gas_dem_for_elec": 1,
    },
)
def fe_elec_generation_from_fossil_fuels():
    value = xr.DataArray(
        np.nan,
        {"matter final sources": _subscript_dict["matter final sources"]},
        ["matter final sources"],
    )
    value.loc[["liquids"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["liquids"])
        + share_oil_dem_for_elec() * pes_oil_ej() * efficiency_liquids_for_electricity()
    )
    value.loc[["solids"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["solids"])
        + share_coal_dem_for_elec()
        * extraction_coal_ej()
        * efficiency_coal_for_electricity()
    )
    value.loc[["gases"]] = (
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["gases"])
        + share_nat_gas_dem_for_elec()
        * pes_nat_gas()
        * efficiency_gas_for_electricity()
    )
    return value


@component.add(
    name="FE Elec generation from fossil fuels TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_elec_generation_from_fossil_fuels": 1, "ej_per_twh": 1},
)
def fe_elec_generation_from_fossil_fuels_twh():
    """
    Final energy electricity generation from fossil fuels (TWh).
    """
    return (
        sum(
            fe_elec_generation_from_fossil_fuels().rename(
                {"matter final sources": "matter final sources!"}
            ),
            dim=["matter final sources!"],
        )
        / ej_per_twh()
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
    lambda: 2463,
    time_step,
    "_delayfixed_fe_tot_generation_all_res_elec_twh_delayed_1yr",
)


@component.add(
    name="FES elec from BioW",
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
        float(real_generation_res_elec_twh().loc["solid bioE elec"])
        + fes_elec_from_biogas_twh()
        + fes_elec_from_waste()
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
    depends_on={
        "total_fe_elec_generation_twh": 1,
        "policy_share_trans_and_dist_losses": 1,
        "time": 1,
    },
)
def total_fe_elec_consumption_twh():
    """
    Total final energy electricity consumption (fossil fuels, nuclear, waste & renewables) (TWh) excluding distribution losses.
    """
    return total_fe_elec_generation_twh() / (
        1 + policy_share_trans_and_dist_losses(time())
    )


@component.add(
    name="Total FE Elec generation TWh",
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
