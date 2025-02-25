"""
Module climate.total_ch4_emissions
Translated using PySD version 3.14.0
"""

@component.add(
    name="CH4_emissions_BioE_and_Waste",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_biofuels": 1,
        "ch4_emissions_biogas": 1,
        "ch4_emissions_biomass": 1,
        "ch4_emissions_solid_bioe": 1,
        "ch4_emissions_waste": 1,
    },
)
def ch4_emissions_bioe_and_waste():
    return (
        ch4_emissions_biofuels()
        + ch4_emissions_biogas()
        + ch4_emissions_biomass()
        + ch4_emissions_solid_bioe()
        + ch4_emissions_waste()
    )


@component.add(
    name="CH4_emissions_biofuels",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"mtch4_per_ej_biofuels": 1, "oil_liquids_saved_by_biofuels_ej": 1},
)
def ch4_emissions_biofuels():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["liquids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["liquids"]] = (
        mtch4_per_ej_biofuels() * oil_liquids_saved_by_biofuels_ej()
    )
    return value


@component.add(
    name="CH4_emissions_biogas",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_biogas": 3,
        "pes_tot_biogas_for_elec": 1,
        "pes_tot_biogas_for_heatcom": 1,
        "pes_biogas_for_tfc": 1,
    },
)
def ch4_emissions_biogas():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = mtch4_per_ej_biogas() * pes_tot_biogas_for_elec()
    value.loc[["heat"]] = mtch4_per_ej_biogas() * pes_tot_biogas_for_heatcom()
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = mtch4_per_ej_biogas() * pes_biogas_for_tfc()
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CH4_emissions_biomass",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_traditional_biomass": 1,
        "pe_traditional_biomass_consum_ej": 1,
    },
)
def ch4_emissions_biomass():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["solids"]] = (
        mtch4_per_ej_traditional_biomass() * pe_traditional_biomass_consum_ej()
    )
    return value


@component.add(
    name="CH4_emissions_coal",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_coal": 3,
        "pec_coal": 4,
        "share_coal_for_elec_emissions_relevant": 2,
        "mtch4_per_ej_ctl": 1,
        "share_coal_for_ctl_emissions_relevant": 1,
        "share_coal_for_fc_emissions_relevant": 1,
    },
)
def ch4_emissions_coal():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = (
        mtch4_per_ej_coal() * pec_coal() * share_coal_for_elec_emissions_relevant()
    )
    value.loc[["heat"]] = (
        mtch4_per_ej_coal() * pec_coal() * share_coal_for_elec_emissions_relevant()
    )
    value.loc[["liquids"]] = (
        mtch4_per_ej_ctl() * pec_coal() * share_coal_for_ctl_emissions_relevant()
    )
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = (
        mtch4_per_ej_coal() * pec_coal() * share_coal_for_fc_emissions_relevant()
    )
    return value


@component.add(
    name="CH4_emissions_fossil_fuels",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_oil": 1,
        "ch4_emissions_gas": 1,
        "ch4_emissions_coal": 1,
        "ch4_emissions_peat": 1,
    },
)
def ch4_emissions_fossil_fuels():
    return (
        ch4_emissions_oil()
        + ch4_emissions_gas()
        + ch4_emissions_coal()
        + ch4_emissions_peat()
    )


@component.add(
    name="CH4_emissions_gas",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_gas": 3,
        "pec_nat_gas": 4,
        "share_nat_gas_for_elec_emissions_relevant": 1,
        "share_nat_gas_for_heat_emissions_relevant": 1,
        "mtch4_per_ej_gtl": 1,
        "share_nat_gas_for_gtl_emissions_relevant": 1,
        "share_nat_gas_for_fc_emissions_relevant": 1,
    },
)
def ch4_emissions_gas():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = (
        mtch4_per_ej_gas() * pec_nat_gas() * share_nat_gas_for_elec_emissions_relevant()
    )
    value.loc[["heat"]] = (
        mtch4_per_ej_gas() * pec_nat_gas() * share_nat_gas_for_heat_emissions_relevant()
    )
    value.loc[["liquids"]] = (
        mtch4_per_ej_gtl() * pec_nat_gas() * share_nat_gas_for_gtl_emissions_relevant()
    )
    value.loc[["gases"]] = (
        mtch4_per_ej_gas() * pec_nat_gas() * share_nat_gas_for_fc_emissions_relevant()
    )
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CH4_emissions_oil",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_oil": 3,
        "pec_total_oil": 3,
        "share_oil_for_elec_emissions_relevant": 1,
        "share_oil_for_heat_emissions_relevant": 2,
    },
)
def ch4_emissions_oil():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = (
        mtch4_per_ej_oil() * pec_total_oil() * share_oil_for_elec_emissions_relevant()
    )
    value.loc[["heat"]] = (
        mtch4_per_ej_oil() * pec_total_oil() * share_oil_for_heat_emissions_relevant()
    )
    value.loc[["liquids"]] = (
        mtch4_per_ej_oil() * pec_total_oil() * share_oil_for_heat_emissions_relevant()
    )
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CH4_emissions_peat",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_peat": 1, "mtch4_per_ej_peat": 1},
)
def ch4_emissions_peat():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["solids"]] = pes_peat() * mtch4_per_ej_peat()
    return value


@component.add(
    name="CH4_emissions_per_fuel",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_emissions_fossil_fuels": 1, "ch4_emissions_bioe_and_waste": 1},
)
def ch4_emissions_per_fuel():
    return ch4_emissions_fossil_fuels() + ch4_emissions_bioe_and_waste()


@component.add(
    name="CH4_emissions_solid_bioE",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_solid_bioe": 3,
        "pe_real_generation_res_elec": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
        "modern_bioe_in_households": 1,
    },
)
def ch4_emissions_solid_bioe():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = mtch4_per_ej_solid_bioe() * float(
        pe_real_generation_res_elec().loc["solid_bioE_elec"]
    )
    value.loc[["heat"]] = mtch4_per_ej_solid_bioe() * (
        float(pes_res_for_heatcom_by_techn().loc["solid_bioE_heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid_bioE_heat"])
    )
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = mtch4_per_ej_solid_bioe() * modern_bioe_in_households()
    return value


@component.add(
    name="CH4_emissions_waste",
    units="MtCH4/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "mtch4_per_ej_waste": 3,
        "pes_tot_waste_for_elec": 1,
        "pes_tot_waste_for_heatcom": 1,
        "pes_waste_for_tfc": 1,
    },
)
def ch4_emissions_waste():
    value = xr.DataArray(
        np.nan,
        {"final_sources": _subscript_dict["final_sources"]},
        [np.str_("final_sources")],
    )
    value.loc[["electricity"]] = mtch4_per_ej_waste() * pes_tot_waste_for_elec()
    value.loc[["heat"]] = mtch4_per_ej_waste() * pes_tot_waste_for_heatcom()
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = mtch4_per_ej_waste() * pes_waste_for_tfc()
    return value


@component.add(
    name="MtCH4_per_EJ_biofuels",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_biofuels"},
)
def mtch4_per_ej_biofuels():
    return _ext_constant_mtch4_per_ej_biofuels()


_ext_constant_mtch4_per_ej_biofuels = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_biofuels",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_biofuels",
)


@component.add(
    name="MtCH4_per_EJ_biogas",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_biogas"},
)
def mtch4_per_ej_biogas():
    return _ext_constant_mtch4_per_ej_biogas()


_ext_constant_mtch4_per_ej_biogas = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_waste",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_biogas",
)


@component.add(
    name="MtCH4_per_EJ_coal",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_coal"},
)
def mtch4_per_ej_coal():
    return _ext_constant_mtch4_per_ej_coal()


_ext_constant_mtch4_per_ej_coal = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_coal",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_coal",
)


@component.add(
    name="MtCH4_per_EJ_conv_gas",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_conv_gas"},
)
def mtch4_per_ej_conv_gas():
    return _ext_constant_mtch4_per_ej_conv_gas()


_ext_constant_mtch4_per_ej_conv_gas = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_conv_gas",
)


@component.add(
    name="MtCH4_per_EJ_conv_oil",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_conv_oil"},
)
def mtch4_per_ej_conv_oil():
    return _ext_constant_mtch4_per_ej_conv_oil()


_ext_constant_mtch4_per_ej_conv_oil = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_conv_oil",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_conv_oil",
)


@component.add(
    name="MtCH4_per_EJ_CTL",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_ctl"},
)
def mtch4_per_ej_ctl():
    return _ext_constant_mtch4_per_ej_ctl()


_ext_constant_mtch4_per_ej_ctl = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_ctl",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_ctl",
)


@component.add(
    name="MtCH4_per_EJ_gas",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_conv_vs_total_gas_extraction": 2,
        "mtch4_per_ej_conv_gas": 1,
        "mtch4_per_ej_unconv_gas": 1,
    },
)
def mtch4_per_ej_gas():
    return (
        share_conv_vs_total_gas_extraction() * mtch4_per_ej_conv_gas()
        + (1 - share_conv_vs_total_gas_extraction()) * mtch4_per_ej_unconv_gas()
    )


@component.add(
    name="MtCH4_per_EJ_GTL",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_gtl"},
)
def mtch4_per_ej_gtl():
    return _ext_constant_mtch4_per_ej_gtl()


_ext_constant_mtch4_per_ej_gtl = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_gtl",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_gtl",
)


@component.add(
    name="MtCH4_per_EJ_oil",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_conv_vs_total_oil_extraction": 2,
        "mtch4_per_ej_conv_oil": 1,
        "mtch4_per_ej_shale_oil": 1,
        "mtch4_per_ej_unconv_oil": 2,
        "adapt_emissions_shale_oil": 1,
    },
)
def mtch4_per_ej_oil():
    return share_conv_vs_total_oil_extraction() * mtch4_per_ej_conv_oil() + (
        1 - share_conv_vs_total_oil_extraction()
    ) * (
        mtch4_per_ej_unconv_oil()
        + (mtch4_per_ej_shale_oil() - mtch4_per_ej_unconv_oil())
        * adapt_emissions_shale_oil()
    )


@component.add(
    name="MtCH4_per_EJ_peat",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_peat"},
)
def mtch4_per_ej_peat():
    return _ext_constant_mtch4_per_ej_peat()


_ext_constant_mtch4_per_ej_peat = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_peat",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_peat",
)


@component.add(
    name="MtCH4_per_EJ_shale_oil",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_shale_oil"},
)
def mtch4_per_ej_shale_oil():
    return _ext_constant_mtch4_per_ej_shale_oil()


_ext_constant_mtch4_per_ej_shale_oil = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_shale_oil",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_shale_oil",
)


@component.add(
    name="MtCH4_per_EJ_solid_BioE",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_solid_bioe"},
)
def mtch4_per_ej_solid_bioe():
    return _ext_constant_mtch4_per_ej_solid_bioe()


_ext_constant_mtch4_per_ej_solid_bioe = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_solid_bioe",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_solid_bioe",
)


@component.add(
    name="MtCH4_per_EJ_traditional_biomass",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_traditional_biomass"},
)
def mtch4_per_ej_traditional_biomass():
    return _ext_constant_mtch4_per_ej_traditional_biomass()


_ext_constant_mtch4_per_ej_traditional_biomass = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_traditional_biomass",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_traditional_biomass",
)


@component.add(
    name="MtCH4_per_EJ_unconv_gas",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_unconv_gas"},
)
def mtch4_per_ej_unconv_gas():
    return _ext_constant_mtch4_per_ej_unconv_gas()


_ext_constant_mtch4_per_ej_unconv_gas = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_unconv_gas",
)


@component.add(
    name="MtCH4_per_EJ_unconv_oil",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_unconv_oil"},
)
def mtch4_per_ej_unconv_oil():
    return _ext_constant_mtch4_per_ej_unconv_oil()


_ext_constant_mtch4_per_ej_unconv_oil = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_unconv_oil",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_unconv_oil",
)


@component.add(
    name="MtCH4_per_EJ_waste",
    units="MtCH4/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_mtch4_per_ej_waste"},
)
def mtch4_per_ej_waste():
    return _ext_constant_mtch4_per_ej_waste()


_ext_constant_mtch4_per_ej_waste = ExtConstant(
    "../climate.xlsx",
    "Global",
    "ch4_waste",
    {},
    _root,
    {},
    "_ext_constant_mtch4_per_ej_waste",
)
