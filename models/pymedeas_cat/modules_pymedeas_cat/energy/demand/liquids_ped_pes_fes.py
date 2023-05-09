"""
Module energy.demand.liquids_ped_pes_fes
Translated using PySD version 3.10.0
"""


@component.add(
    name="abundance liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 3, "pes_liquids": 2},
)
def abundance_liquids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_liquids() < pes_liquids(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids() - pes_liquids(), ped_liquids()),
    )


@component.add(
    name="check liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "pes_liquids": 2},
)
def check_liquids():
    """
    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0, demand<supply (oversupply). Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_liquids() - pes_liquids(), pes_liquids())


@component.add(
    name='"constrain liquids exogenous growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"check_liquids": 2},
)
def constrain_liquids_exogenous_growth():
    """
    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > 0, lambda: 1, lambda: check_liquids())


@component.add(
    name="Energy losses from liquids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_distr_losses_ff_ej": 1, "transformation_ff_losses_ej": 1},
)
def energy_losses_from_liquids():
    """
    Liquids-related distribution and transformation losses.
    """
    return float(energy_distr_losses_ff_ej().loc["liquids"]) + float(
        transformation_ff_losses_ej().loc["liquids"]
    )


@component.add(
    name="Historic conv oil domestic CAT extracted EJ",
    units="EJ/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_conv_oil_domestic_cat_extracted_ej():
    return _ext_data_historic_conv_oil_domestic_cat_extracted_ej(time())


_ext_data_historic_conv_oil_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_conventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
)


@component.add(
    name="Historic net imports oil CAT",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_liquids": 1,
        "historic_conv_oil_domestic_cat_extracted_ej": 1,
        "historic_unconv_oil_domestic_cat_extracted_ej": 1,
    },
)
def historic_net_imports_oil_cat():
    return (
        ped_liquids()
        - historic_conv_oil_domestic_cat_extracted_ej()
        - historic_unconv_oil_domestic_cat_extracted_ej()
    )


@component.add(
    name='"Historic share conv. oil domestic CAT extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_conv_oil_domestic_cat_extracted_ej": 1, "ped_liquids": 1},
)
def historic_share_conv_oil_domestic_cat_extraction():
    return zidz(historic_conv_oil_domestic_cat_extracted_ej(), ped_liquids())


@component.add(
    name='"Historic share conv. oil domestic CAT extraction\\" until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016": {
            "initial": {"historic_share_conv_oil_domestic_cat_extraction": 1},
            "step": {"time": 1, "historic_share_conv_oil_domestic_cat_extraction": 1},
        }
    },
)
def historic_share_conv_oil_domestic_cat_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016()


_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_conv_oil_domestic_cat_extraction(),
    lambda: historic_share_conv_oil_domestic_cat_extraction(),
    "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016",
)


@component.add(
    name="Historic unconv oil domestic CAT extracted EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_oil_domestic_cat_extracted_ej():
    return _ext_data_historic_unconv_oil_domestic_cat_extracted_ej(time())


_ext_data_historic_unconv_oil_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
)


@component.add(
    name="imports CAT conv oil from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_cat_conv_oil_from_row_ej():
    return (
        imports_cat_total_oil_from_row_ej() * share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name="imports CAT total oil from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_oil_flux_cat": 1},
)
def imports_cat_total_oil_from_row_ej():
    return net_oil_flux_cat()


@component.add(
    name="imports CAT unconv oil from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_cat_unconv_oil_from_row_ej():
    return imports_cat_total_oil_from_row_ej() * (
        1 - share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name='"Non-energy use consumption"',
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_liquids_for_nonenergy_uses": 1,
        "energy_losses_from_liquids": 1,
        "pes_liquids": 1,
        "share_solids_for_nonenergy_uses": 1,
        "energy_losses_from_solids": 1,
        "pes_solids": 1,
        "energy_losses_from_gases": 1,
        "pes_gases": 1,
        "share_gases_for_nonenergy_uses": 1,
    },
)
def nonenergy_use_consumption():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["liquids"]] = share_liquids_for_nonenergy_uses() * (
        pes_liquids() - energy_losses_from_liquids()
    )
    value.loc[["solids"]] = share_solids_for_nonenergy_uses() * (
        pes_solids() - energy_losses_from_solids()
    )
    value.loc[["gases"]] = share_gases_for_nonenergy_uses() * (
        pes_gases() - energy_losses_from_gases()
    )
    return value


@component.add(
    name="Other liquids supply EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_refinery_gains_ej": 1,
        "fes_ctlgtl_ej": 1,
        "fes_total_biofuels_ej": 1,
    },
)
def other_liquids_supply_ej():
    """
    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_ej()


@component.add(
    name="PEC oil for conversion",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "share_nre_liquids_for_conversion": 1},
)
def pec_oil_for_conversion():
    return pec_total_oil() * share_nre_liquids_for_conversion()


@component.add(
    name="PEC total oil",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_total_oil_ej_cat": 1, "imports_cat_total_oil_from_row_ej": 1},
)
def pec_total_oil():
    """
    There are loses related to oil refinery that reduces final energy consumtion
    """
    return pes_total_oil_ej_cat() + imports_cat_total_oil_from_row_ej()


@component.add(
    name="PED CAT total oil from RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "pes_total_oil_ej_cat": 1},
)
def ped_cat_total_oil_from_row():
    return np.maximum(0, ped_total_oil_ej() - pes_total_oil_ej_cat())


@component.add(
    name='"PED domestic CAT conv. oil EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_total_oil_ej": 1,
        "historic_share_conv_oil_domestic_cat_extraction_until_2016": 1,
    },
)
def ped_domestic_cat_conv_oil_ej():
    return (
        ped_total_oil_ej()
        * historic_share_conv_oil_domestic_cat_extraction_until_2016()
    )


@component.add(
    name="PED domestic CAT total oil EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "imports_cat_total_oil_from_row_ej": 1},
)
def ped_domestic_cat_total_oil_ej():
    """
    PED total oil EJ*("Historic share conv. oil domestic CAT extraction
    " until 2016"+"Historic share unconv. oil domestric CAT extraction until 2016" )
    """
    return np.maximum(0, ped_total_oil_ej() - imports_cat_total_oil_from_row_ej())


@component.add(
    name="PED liquids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 1,
        "energy_losses_from_liquids": 1,
        "ped_oil_for_conversion": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def ped_liquids():
    """
    Primary energy demand of total liquids.
    """
    return np.maximum(
        0,
        required_fed_by_liquids()
        + energy_losses_from_liquids()
        + ped_oil_for_conversion()
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]),
    )


@component.add(
    name="PED NRE Liquids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_conversion": 1,
        "ped_liquids": 1,
        "fes_total_biofuels_ej": 1,
    },
)
def ped_nre_liquids():
    """
    Primary energy demand of non-renewable energy for the production of liquids.
    """
    return np.maximum(
        ped_oil_for_conversion(), np.maximum(0, ped_liquids() - fes_total_biofuels_ej())
    )


@component.add(
    name="PED oil for conversion",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_liquids_heatnc": 1,
        "ped_oil_elec_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_oil_for_heat_plants_ej": 1,
    },
)
def ped_oil_for_conversion():
    """
    Primary energy demand of oil to transform it into heat and electricity.
    """
    return (
        ped_liquids_heatnc()
        + ped_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_oil_for_heat_plants_ej()
    )


@component.add(
    name="PED total oil EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_liquids": 1, "fes_ctlgtl_ej": 1, "oil_refinery_gains_ej": 1},
)
def ped_total_oil_ej():
    """
    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


@component.add(
    name="PES Liquids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "other_liquids_supply_ej": 1},
)
def pes_liquids():
    """
    Total primary supply of liquids.
    """
    return pec_total_oil() + other_liquids_supply_ej()


@component.add(
    name="real FE consumption liquids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 1,
        "energy_losses_from_liquids": 1,
        "share_liquids_for_final_energy": 1,
        "pes_liquids": 1,
    },
)
def real_fe_consumption_liquids_ej():
    """
    Real final energy consumption by liquids after accounting for energy availability.
    """
    return np.minimum(
        required_fed_by_liquids(),
        (pes_liquids() - energy_losses_from_liquids())
        * share_liquids_for_final_energy(),
    )


@component.add(
    name="Required FED by liquids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_liquids():
    """
    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


@component.add(
    name="Share biofuel in PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_ej": 1, "pes_liquids": 1},
)
def share_biofuel_in_pes():
    return zidz(fes_total_biofuels_ej(), pes_liquids())


@component.add(
    name='"share fed vs non-energy liquids"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 2,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def share_fed_vs_nonenergy_liquids():
    return zidz(
        required_fed_by_liquids(),
        float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
        + required_fed_by_liquids(),
    )


@component.add(
    name="share liquids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 1,
        "ped_liquids": 1,
        "energy_losses_from_liquids": 1,
    },
)
def share_liquids_for_final_energy():
    """
    Share of final energy vs primary energy for liquids.
    """
    return zidz(required_fed_by_liquids(), ped_liquids() - energy_losses_from_liquids())


@component.add(
    name='"share liquids for non-energy uses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_liquids": 1,
        "energy_losses_from_liquids": 1,
    },
)
def share_liquids_for_nonenergy_uses():
    return zidz(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]),
        ped_liquids() - energy_losses_from_liquids(),
    )


@component.add(
    name="share NRE liquids for conversion",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_oil_for_conversion": 1, "ped_nre_liquids": 1},
)
def share_nre_liquids_for_conversion():
    return zidz(ped_oil_for_conversion(), ped_nre_liquids())


@component.add(
    name='"Total demand liquids mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "mbd_per_ejyear": 1},
)
def total_demand_liquids_mbd():
    """
    Total demand of liquids.
    """
    return ped_liquids() * mbd_per_ejyear()
