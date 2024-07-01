"""
Module climate.other_ghg_cycles
Translated using PySD version 3.14.0
"""

@component.add(
    name="CF4_molar_mass", units="g/mole", comp_type="Constant", comp_subtype="Normal"
)
def cf4_molar_mass():
    """
    CF4 grams per mole.
    """
    return 88


@component.add(
    name="CH4_atm_conc",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atm": 1, "ppb_ch4_per_mt_ch4": 1},
)
def ch4_atm_conc():
    return ch4_in_atm() * ppb_ch4_per_mt_ch4()


@component.add(
    name="CH4_Emissions_from_Permafrost_and_Clathrate",
    units="MtCH4/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_methane_emissions_to_permafrost_and_clathrate": 1,
        "reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature": 1,
        "temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate": 1,
        "temperature_change": 1,
    },
)
def ch4_emissions_from_permafrost_and_clathrate():
    """
    Methane emissions from melting permafrost and clathrate outgassing are assumed to be nonlinear. Emissions are assumed to be zero if warming over preindustrial levels is less than a threshold and linear in temperature above the threshold. The default sensitivity is zero, but the strength of the effect and threshold can be set by the user.
    """
    return (
        sensitivity_of_methane_emissions_to_permafrost_and_clathrate()
        * reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature()
        * np.maximum(
            0,
            temperature_change()
            - temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate(),
        )
    )


@component.add(
    name="CH4_Fractional_Uptake",
    units="1/years",
    limits=(5.0, 15.0, 0.1),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_ch4_time_constant": 1,
        "preindustrial_ch4": 1,
        "tropospheric_ch4_path_share": 2,
        "stratospheric_ch4_path_share": 2,
        "ch4_in_atm": 1,
    },
)
def ch4_fractional_uptake():
    """
    dCH4/dt = E – k1*CH4*OH – k2*CH4 E = emissions. The k1 path is dominant (k2 reflects soil processes and other minor sinks) dOH/dt = F – k3*CH4*OH – k4*OH F = formation. In this case the methane reaction is the minor path (15-20% of loss) so OH in equilibrium is OHeq = F/(k3*CH4+k4) substituting dCH4/dt = E – k1*CH4* F/(k3*CH4+k4) – k2*CH4 thus the total fractional uptake is k1*F/(k3*CH4+k4)+k2 which is robust at 0 Formulated from Meinshausen et al., 2011
    """
    return (
        1
        / reference_ch4_time_constant()
        * (
            tropospheric_ch4_path_share()
            / (
                stratospheric_ch4_path_share() * (ch4_in_atm() / preindustrial_ch4())
                + 1
                - stratospheric_ch4_path_share()
            )
            + (1 - tropospheric_ch4_path_share())
        )
    )


@component.add(
    name="CH4_in_Atm",
    units="MtCH4",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ch4_in_atm": 1},
    other_deps={
        "_integ_ch4_in_atm": {
            "initial": {"initial_ch4": 1},
            "step": {
                "ch4_emissions_from_permafrost_and_clathrate": 1,
                "global_ch4_emissions": 1,
                "ch4_uptake": 1,
            },
        }
    },
)
def ch4_in_atm():
    return _integ_ch4_in_atm()


_integ_ch4_in_atm = Integ(
    lambda: ch4_emissions_from_permafrost_and_clathrate()
    + global_ch4_emissions()
    - ch4_uptake(),
    lambda: initial_ch4(),
    "_integ_ch4_in_atm",
)


@component.add(
    name="CH4_molar_mass",
    units="gCH4/mole",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ch4_molar_mass():
    """
    CH4 grams per mole
    """
    return 16


@component.add(
    name="CH4_Uptake",
    units="(MtCH4)/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atm": 1, "ch4_fractional_uptake": 1},
)
def ch4_uptake():
    return ch4_in_atm() * ch4_fractional_uptake()


@component.add(
    name="Choose_RCP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_rcp"},
)
def choose_rcp():
    """
    Choose RCP (Representative Concentration Pathway) 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "select_RCP",
    {},
    _root,
    {},
    "_ext_constant_choose_rcp",
)


@component.add(
    name="Flux_C_from_permafrost_release",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_methane_emissions_to_permafrost_and_clathrate": 1,
        "reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature": 1,
        "temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate": 1,
        "temperature_change": 1,
    },
)
def flux_c_from_permafrost_release():
    return (
        sensitivity_of_methane_emissions_to_permafrost_and_clathrate()
        * reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature()
        * np.maximum(
            0,
            temperature_change()
            - temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate(),
        )
    )


@component.add(
    name="g_per_t", units="g/t", comp_type="Constant", comp_subtype="Unchangeable"
)
def g_per_t():
    return 1000000.0


@component.add(
    name="gCH4_per_tCH4", units="gCH4/tCH4", comp_type="Constant", comp_subtype="Normal"
)
def gch4_per_tch4():
    return 1000000.0


@component.add(
    name="global_CH4_anthro_emissions",
    units="MtCH4/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_emissions_mtch4": 1,
        "global_ch4_anthro_emissions_rcp": 4,
        "choose_rcp": 3,
    },
)
def global_ch4_anthro_emissions():
    """
    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) except Power Plants, Energy Conversion, Extraction, and Distribution. Corrected with endogenous data "Total CH4 emissions fossil fuels" Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return total_ch4_emissions_mtch4() + if_then_else(
        choose_rcp() == 1,
        lambda: float(global_ch4_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(global_ch4_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(global_ch4_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(global_ch4_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="global_CH4_anthro_emissions_RCP",
    units="MtCH4/year",
    subscripts=["RCP_Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_global_ch4_anthro_emissions_rcp",
        "__data__": "_ext_data_global_ch4_anthro_emissions_rcp",
        "time": 1,
    },
)
def global_ch4_anthro_emissions_rcp():
    """
    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_ch4_anthro_emissions_rcp(time())


_ext_data_global_ch4_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "CH4_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    _root,
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    "_ext_data_global_ch4_anthro_emissions_rcp",
)


@component.add(
    name="global_CH4_emissions",
    units="MtCH4/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"global_ch4_anthro_emissions": 1, "natural_ch4_emissions": 1},
)
def global_ch4_emissions():
    return global_ch4_anthro_emissions() + natural_ch4_emissions()


@component.add(
    name="global_HFC_emissions",
    units="t/year",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "global_hfc_emissions_rcp": 4},
)
def global_hfc_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: global_hfc_emissions_rcp().loc["RCP26", :].reset_coords(drop=True),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: global_hfc_emissions_rcp().loc["RCP45", :].reset_coords(drop=True),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: global_hfc_emissions_rcp()
                .loc["RCP60", :]
                .reset_coords(drop=True),
                lambda: global_hfc_emissions_rcp()
                .loc["RCP85", :]
                .reset_coords(drop=True),
            ),
        ),
    )


@component.add(
    name="global_HFC_emissions_RCP",
    units="t/year",
    subscripts=["RCP_Scenario", "HFC_type"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_global_hfc_emissions_rcp",
        "__data__": "_ext_data_global_hfc_emissions_rcp",
        "time": 1,
    },
)
def global_hfc_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_hfc_emissions_rcp(time())


_ext_data_global_hfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC134a_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC134a"]},
    _root,
    {
        "RCP_Scenario": _subscript_dict["RCP_Scenario"],
        "HFC_type": _subscript_dict["HFC_type"],
    },
    "_ext_data_global_hfc_emissions_rcp",
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC23_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC23"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC32_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC32"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC125_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC125"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC143a_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC143a"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC152a_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC152a"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC227ea_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC227ea"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC245ca_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC245ca"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC4310mee_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"], "HFC_type": ["HFC4310mee"]},
)


@component.add(
    name="global_N2O_anthro_emissions",
    units="MtN/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "global_n2o_anthro_emissions_rcp": 4},
)
def global_n2o_anthro_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(global_n2o_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(global_n2o_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(global_n2o_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(global_n2o_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="global_N2O_anthro_emissions_RCP",
    units="MtN/year",
    subscripts=["RCP_Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_global_n2o_anthro_emissions_rcp",
        "__data__": "_ext_data_global_n2o_anthro_emissions_rcp",
        "time": 1,
    },
)
def global_n2o_anthro_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_n2o_anthro_emissions_rcp(time())


_ext_data_global_n2o_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "N2O_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    _root,
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    "_ext_data_global_n2o_anthro_emissions_rcp",
)


@component.add(
    name="global_N2O_emissions",
    units="MtN/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"global_n2o_anthro_emissions": 1, "natural_n2o_emissions": 1},
)
def global_n2o_emissions():
    return global_n2o_anthro_emissions() + natural_n2o_emissions()


@component.add(
    name="global_PFC_emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "global_pfc_emissions_rcp": 4},
)
def global_pfc_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(global_pfc_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(global_pfc_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(global_pfc_emissions_rcp().loc["RCP60"]),
                lambda: float(global_pfc_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="global_PFC_emissions_RCP",
    units="t/year",
    subscripts=["RCP_Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_global_pfc_emissions_rcp",
        "__data__": "_ext_data_global_pfc_emissions_rcp",
        "time": 1,
    },
)
def global_pfc_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_pfc_emissions_rcp(time())


_ext_data_global_pfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "PFCs_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    _root,
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    "_ext_data_global_pfc_emissions_rcp",
)


@component.add(
    name="global_SF6_emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "global_sf6_emissions_rcp": 4},
)
def global_sf6_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(global_sf6_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(global_sf6_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(global_sf6_emissions_rcp().loc["RCP60"]),
                lambda: float(global_sf6_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="global_SF6_emissions_RCP",
    units="t/year",
    subscripts=["RCP_Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_global_sf6_emissions_rcp",
        "__data__": "_ext_data_global_sf6_emissions_rcp",
        "time": 1,
    },
)
def global_sf6_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_sf6_emissions_rcp(time())


_ext_data_global_sf6_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "SF6_emissions",
    "interpolate",
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    _root,
    {"RCP_Scenario": _subscript_dict["RCP_Scenario"]},
    "_ext_data_global_sf6_emissions_rcp",
)


@component.add(
    name="global_total_PFC_emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"global_pfc_emissions": 1, "natural_pfc_emissions": 1},
)
def global_total_pfc_emissions():
    return global_pfc_emissions() + natural_pfc_emissions()


@component.add(
    name="HFC_atm_conc",
    units="ppt",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfc_in_atm": 1, "ppt_hfc_per_tons_hfc": 1},
)
def hfc_atm_conc():
    return hfc_in_atm() * ppt_hfc_per_tons_hfc()


@component.add(
    name="HFC_in_Atm",
    units="t",
    limits=(2.5924e-43, np.nan),
    subscripts=["HFC_type"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hfc_in_atm": 1},
    other_deps={
        "_integ_hfc_in_atm": {
            "initial": {"initial_hfc": 1},
            "step": {"global_hfc_emissions": 1, "hfc_uptake": 1},
        }
    },
)
def hfc_in_atm():
    return _integ_hfc_in_atm()


_integ_hfc_in_atm = Integ(
    lambda: global_hfc_emissions() - hfc_uptake(),
    lambda: initial_hfc(),
    "_integ_hfc_in_atm",
)


@component.add(
    name="HFC_molar_mass",
    units="g/mole",
    subscripts=["HFC_type"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def hfc_molar_mass():
    """
    HFCs grams per mole. http://www.qc.ec.gc.ca/dpe/publication/enjeux_ges/hfc134a_a.html
    """
    return xr.DataArray(
        [102.0, 70.0, 52.0, 120.0, 84.0, 66.0, 170.0, 134.0, 252.0],
        {"HFC_type": _subscript_dict["HFC_type"]},
        ["HFC_type"],
    )


@component.add(
    name="HFC_radiative_efficiency",
    units="W/(ppb*m*m)",
    subscripts=["HFC_type"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_hfc_radiative_efficiency"},
)
def hfc_radiative_efficiency():
    """
    From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_hfc_radiative_efficiency()


_ext_constant_hfc_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "HFC_radiative_efficiency*",
    {"HFC_type": _subscript_dict["HFC_type"]},
    _root,
    {"HFC_type": _subscript_dict["HFC_type"]},
    "_ext_constant_hfc_radiative_efficiency",
)


@component.add(
    name="HFC_RF",
    units="W/(m*m)",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hfc_atm_conc": 1,
        "preindustrial_hfc_conc": 1,
        "hfc_radiative_efficiency": 1,
        "ppt_per_ppb": 1,
    },
)
def hfc_rf():
    return (
        (hfc_atm_conc() - preindustrial_hfc_conc())
        * hfc_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="HFC_uptake",
    units="t/year",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hfc_in_atm": 1, "time_const_for_hfc": 1},
)
def hfc_uptake():
    return hfc_in_atm() / time_const_for_hfc()


@component.add(
    name="init_PFC_in_atm",
    units="t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_pfc_in_atm_con": 1, "ppt_pfc_per_tons_pfc": 1},
)
def init_pfc_in_atm():
    return init_pfc_in_atm_con() / ppt_pfc_per_tons_pfc()


@component.add(
    name="init_PFC_in_atm_con",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_init_pfc_in_atm_con"},
)
def init_pfc_in_atm_con():
    """
    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_init_pfc_in_atm_con()


_ext_constant_init_pfc_in_atm_con = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_PFC_in_atm_con",
    {},
    _root,
    {},
    "_ext_constant_init_pfc_in_atm_con",
)


@component.add(
    name="inital_HFC_con",
    units="ppt",
    subscripts=["HFC_type"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_inital_hfc_con"},
)
def inital_hfc_con():
    return _ext_constant_inital_hfc_con()


_ext_constant_inital_hfc_con = ExtConstant(
    "../climate.xlsx",
    "World",
    "inital_HFC_con*",
    {"HFC_type": _subscript_dict["HFC_type"]},
    _root,
    {"HFC_type": _subscript_dict["HFC_type"]},
    "_ext_constant_inital_hfc_con",
)


@component.add(
    name="initial_CH4",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_ch4_conc": 1, "ppb_ch4_per_mt_ch4": 1},
)
def initial_ch4():
    return initial_ch4_conc() / ppb_ch4_per_mt_ch4()


@component.add(
    name="initial_CH4_conc",
    units="ppb",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_ch4_conc"},
)
def initial_ch4_conc():
    """
    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_ch4_conc()


_ext_constant_initial_ch4_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_CH4_conc",
    {},
    _root,
    {},
    "_ext_constant_initial_ch4_conc",
)


@component.add(
    name="Initial_HFC",
    units="t",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"inital_hfc_con": 1, "ppt_hfc_per_tons_hfc": 1},
)
def initial_hfc():
    return inital_hfc_con() / ppt_hfc_per_tons_hfc()


@component.add(
    name="initial_N2O",
    units="MtN",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_n2o_conc": 1, "ppb_n2o_per_mtonn": 1},
)
def initial_n2o():
    return initial_n2o_conc() / ppb_n2o_per_mtonn()


@component.add(
    name="initial_N2O_conc",
    units="ppb",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_n2o_conc"},
)
def initial_n2o_conc():
    """
    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_n2o_conc()


_ext_constant_initial_n2o_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_N2O_conc",
    {},
    _root,
    {},
    "_ext_constant_initial_n2o_conc",
)


@component.add(
    name="initial_SF6",
    units="t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_sf6_conc": 1, "ppt_sf6_per_tons_sf6": 1},
)
def initial_sf6():
    return initial_sf6_conc() / ppt_sf6_per_tons_sf6()


@component.add(
    name="initial_SF6_conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_sf6_conc"},
)
def initial_sf6_conc():
    """
    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_sf6_conc()


_ext_constant_initial_sf6_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_SF6_conc",
    {},
    _root,
    {},
    "_ext_constant_initial_sf6_conc",
)


@component.add(
    name="N2O_atm_conc",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atm": 1, "ppb_n2o_per_mtonn": 1},
)
def n2o_atm_conc():
    return n2o_in_atm() * ppb_n2o_per_mtonn()


@component.add(
    name="N2O_in_Atm",
    units="MtN",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_n2o_in_atm": 1},
    other_deps={
        "_integ_n2o_in_atm": {
            "initial": {"initial_n2o": 1},
            "step": {"global_n2o_emissions": 1, "n2o_uptake": 1},
        }
    },
)
def n2o_in_atm():
    return _integ_n2o_in_atm()


_integ_n2o_in_atm = Integ(
    lambda: global_n2o_emissions() - n2o_uptake(),
    lambda: initial_n2o(),
    "_integ_n2o_in_atm",
)


@component.add(
    name="N2O_Uptake",
    units="MtN/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atm": 1, "time_const_for_n2o": 1},
)
def n2o_uptake():
    return n2o_in_atm() / time_const_for_n2o()


@component.add(
    name='"N2O-N_molar_mass"',
    units="g/mole",
    comp_type="Constant",
    comp_subtype="Unchangeable",
)
def n2on_molar_mass():
    """
    NO2-N grams per mole.
    """
    return 28


@component.add(
    name="natural_N2O_emissions",
    units="MtN/year",
    limits=(0.0, 20.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_natural_n2o_emissions"},
)
def natural_n2o_emissions():
    """
    AR5 WG1 Chapter 6 Table 6.9
    """
    return _ext_constant_natural_n2o_emissions()


_ext_constant_natural_n2o_emissions = ExtConstant(
    "../climate.xlsx",
    "World",
    "natural_N2O_emissions",
    {},
    _root,
    {},
    "_ext_constant_natural_n2o_emissions",
)


@component.add(
    name="natural_PFC_emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"preindustrial_pfc": 1, "time_const_for_pfc": 1},
)
def natural_pfc_emissions():
    return preindustrial_pfc() / time_const_for_pfc()


@component.add(
    name="PFC_atm_conc",
    units="ppt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pfc_in_atm": 1, "ppt_pfc_per_tons_pfc": 1},
)
def pfc_atm_conc():
    return pfc_in_atm() * ppt_pfc_per_tons_pfc()


@component.add(
    name="PFC_in_Atm",
    units="t",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pfc_in_atm": 1},
    other_deps={
        "_integ_pfc_in_atm": {
            "initial": {"init_pfc_in_atm": 1},
            "step": {"global_total_pfc_emissions": 1, "pfc_uptake": 1},
        }
    },
)
def pfc_in_atm():
    return _integ_pfc_in_atm()


_integ_pfc_in_atm = Integ(
    lambda: global_total_pfc_emissions() - pfc_uptake(),
    lambda: init_pfc_in_atm(),
    "_integ_pfc_in_atm",
)


@component.add(
    name="PFC_radiative_efficiency",
    units="W/(ppb*m*m)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pfc_radiative_efficiency"},
)
def pfc_radiative_efficiency():
    """
    Radiative efficiency of CF4. From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_pfc_radiative_efficiency()


_ext_constant_pfc_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "PFC_radiative_efficiency",
    {},
    _root,
    {},
    "_ext_constant_pfc_radiative_efficiency",
)


@component.add(
    name="PFC_RF",
    units="W/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pfc_atm_conc": 1,
        "preindustrial_pfc_conc": 1,
        "pfc_radiative_efficiency": 1,
        "ppt_per_ppb": 1,
    },
)
def pfc_rf():
    return (
        (pfc_atm_conc() - preindustrial_pfc_conc())
        * pfc_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="PFC_uptake",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pfc_in_atm": 1, "time_const_for_pfc": 1},
)
def pfc_uptake():
    return pfc_in_atm() / time_const_for_pfc()


@component.add(
    name="ppb_CH4_per_Mt_CH4",
    units="ppb/MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppt_per_mol": 1,
        "ch4_molar_mass": 1,
        "gch4_per_tch4": 1,
        "tch4_per_mtch4": 1,
        "ppt_per_ppb": 1,
    },
)
def ppb_ch4_per_mt_ch4():
    return (
        ppt_per_mol()
        / ch4_molar_mass()
        * gch4_per_tch4()
        * tch4_per_mtch4()
        / ppt_per_ppb()
    )


@component.add(
    name="ppb_N2O_per_MTonN",
    units="ppb/MtN",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppt_per_mol": 1,
        "n2on_molar_mass": 1,
        "g_per_t": 1,
        "t_per_mt": 1,
        "ppt_per_ppb": 1,
    },
)
def ppb_n2o_per_mtonn():
    return ppt_per_mol() / n2on_molar_mass() * g_per_t() * t_per_mt() / ppt_per_ppb()


@component.add(
    name="ppt_HFC_per_Tons_HFC",
    units="ppt/t",
    subscripts=["HFC_type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ppt_per_mol": 1, "hfc_molar_mass": 1, "g_per_t": 1},
)
def ppt_hfc_per_tons_hfc():
    return ppt_per_mol() / hfc_molar_mass() * g_per_t()


@component.add(
    name="ppt_per_mol",
    units="ppt/mole",
    comp_type="Constant",
    comp_subtype="Unchangeable",
)
def ppt_per_mol():
    return 5.68e-09


@component.add(
    name="ppt_per_ppb",
    units="ppt/ppb",
    comp_type="Constant",
    comp_subtype="Unchangeable",
)
def ppt_per_ppb():
    return 1000


@component.add(
    name="ppt_PFC_per_Tons_PFC",
    units="ppt/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ppt_per_mol": 1, "cf4_molar_mass": 1, "g_per_t": 1},
)
def ppt_pfc_per_tons_pfc():
    """
    CF4 ppt per tne
    """
    return ppt_per_mol() / cf4_molar_mass() * g_per_t()


@component.add(
    name="ppt_SF6_per_Tons_SF6",
    units="ppt/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ppt_per_mol": 1, "sf6_molar_mass": 1, "g_per_t": 1},
)
def ppt_sf6_per_tons_sf6():
    return ppt_per_mol() / sf6_molar_mass() * g_per_t()


@component.add(
    name="preindustrial_CH4",
    units="MtCH4",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_ch4"},
)
def preindustrial_ch4():
    """
    Law Dome ice core
    """
    return _ext_constant_preindustrial_ch4()


_ext_constant_preindustrial_ch4 = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_CH4",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_ch4",
)


@component.add(
    name="preindustrial_HFC_conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_hfc_conc"},
)
def preindustrial_hfc_conc():
    return _ext_constant_preindustrial_hfc_conc()


_ext_constant_preindustrial_hfc_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_HFC_conc",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_hfc_conc",
)


@component.add(
    name="preindustrial_PFC",
    units="t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"preindustrial_pfc_conc": 1, "ppt_pfc_per_tons_pfc": 1},
)
def preindustrial_pfc():
    return preindustrial_pfc_conc() / ppt_pfc_per_tons_pfc()


@component.add(
    name="preindustrial_PFC_conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_pfc_conc"},
)
def preindustrial_pfc_conc():
    return _ext_constant_preindustrial_pfc_conc()


_ext_constant_preindustrial_pfc_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_PFC_conc",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_pfc_conc",
)


@component.add(
    name="preindustrial_SF6_conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_preindustrial_sf6_conc"},
)
def preindustrial_sf6_conc():
    return _ext_constant_preindustrial_sf6_conc()


_ext_constant_preindustrial_sf6_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_SF6_conc",
    {},
    _root,
    {},
    "_ext_constant_preindustrial_sf6_conc",
)


@component.add(
    name="reference_CH4_time_constant",
    units="year",
    limits=(8.0, 10.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_reference_ch4_time_constant"},
)
def reference_ch4_time_constant():
    """
    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_reference_ch4_time_constant()


_ext_constant_reference_ch4_time_constant = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_CH4_time_constant",
    {},
    _root,
    {},
    "_ext_constant_reference_ch4_time_constant",
)


@component.add(
    name="reference_sensitivity_of_C_from_permafrost_and_clathrate_to_temperature",
    units="GtC/year/ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature"
    },
)
def reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature():
    return (
        _ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature()
    )


_ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_sensitivity_of_C_from_permafrost_and_clathrate_to_temperature",
    {},
    _root,
    {},
    "_ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature",
)


@component.add(
    name="reference_sensitivity_of_CH4_from_permafrost_and_clathrate_to_temperature",
    units="MtCH4/year/ºC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature"
    },
)
def reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature():
    """
    The reference emissions of methane from melting permafrost and outgassing from clathrates per degree C of warming above the threshold.
    """
    return (
        _ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature()
    )


_ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_sensitivity_of_CH4_from_permafrost_and_clathrate_to_temperature",
    {},
    _root,
    {},
    "_ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature",
)


@component.add(
    name="sensitivity_of_methane_emissions_to_permafrost_and_clathrate",
    units="Dmnl",
    limits=(0.0, 1.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate"
    },
)
def sensitivity_of_methane_emissions_to_permafrost_and_clathrate():
    """
    0 = no feedback 1 = base feedback
    """
    return _ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate()


_ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate = (
    ExtConstant(
        "../climate.xlsx",
        "World",
        "sensitivity_of_methane_emissions_to_permafrost_and_clathrate",
        {},
        _root,
        {},
        "_ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate",
    )
)


@component.add(
    name="SF6",
    units="t",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_sf6": 1},
    other_deps={
        "_integ_sf6": {
            "initial": {"initial_sf6": 1},
            "step": {"global_sf6_emissions": 1, "sf6_uptake": 1},
        }
    },
)
def sf6():
    return _integ_sf6()


_integ_sf6 = Integ(
    lambda: global_sf6_emissions() - sf6_uptake(), lambda: initial_sf6(), "_integ_sf6"
)


@component.add(
    name="SF6_atm_conc",
    units="ppt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sf6": 1, "ppt_sf6_per_tons_sf6": 1},
)
def sf6_atm_conc():
    return sf6() * ppt_sf6_per_tons_sf6()


@component.add(
    name="SF6_molar_mass", units="g/mole", comp_type="Constant", comp_subtype="Normal"
)
def sf6_molar_mass():
    """
    SF6 grams per mole
    """
    return 146


@component.add(
    name="SF6_radiative_efficiency",
    units="W/(ppb*m*m)",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_sf6_radiative_efficiency"},
)
def sf6_radiative_efficiency():
    """
    From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_sf6_radiative_efficiency()


_ext_constant_sf6_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "SF6_radiative_efficiency",
    {},
    _root,
    {},
    "_ext_constant_sf6_radiative_efficiency",
)


@component.add(
    name="SF6_RF",
    units="W/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sf6_atm_conc": 1,
        "preindustrial_sf6_conc": 1,
        "sf6_radiative_efficiency": 1,
        "ppt_per_ppb": 1,
    },
)
def sf6_rf():
    return (
        (sf6_atm_conc() - preindustrial_sf6_conc())
        * sf6_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="SF6_uptake",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sf6": 1, "time_const_for_sf6": 1},
)
def sf6_uptake():
    return sf6() / time_const_for_sf6()


@component.add(
    name="Stratospheric_CH4_path_share",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_stratospheric_ch4_path_share"},
)
def stratospheric_ch4_path_share():
    """
    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_stratospheric_ch4_path_share()


_ext_constant_stratospheric_ch4_path_share = ExtConstant(
    "../climate.xlsx",
    "World",
    "stratospheric_CH4_path_share",
    {},
    _root,
    {},
    "_ext_constant_stratospheric_ch4_path_share",
)


@component.add(
    name="t_per_Mt", units="t/MtN", comp_type="Constant", comp_subtype="Normal"
)
def t_per_mt():
    return 1000000.0


@component.add(
    name="tCH4_per_MtCH4",
    units="tCH4/MtCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tch4_per_mtch4():
    return 1000000.0


@component.add(
    name="temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate",
    units="DegreesC",
    limits=(0.0, 4.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate"
    },
)
def temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate():
    """
    The threshold rise in global mean surface temperature above preindustrial levels that triggers the release of methane from permafrost and clathrates. Below this threshold, emissions from these sources are assumed to be zero. Above the threshold, emissions are assumed to rise linearly with temperature.
    """
    return (
        _ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate()
    )


_ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate = ExtConstant(
    "../climate.xlsx",
    "World",
    "temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate",
    {},
    _root,
    {},
    "_ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate",
)


@component.add(
    name="Time_Const_for_CH4",
    units="years",
    limits=(5.0, 15.0, 0.1),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_fractional_uptake": 1},
)
def time_const_for_ch4():
    return 1 / ch4_fractional_uptake()


@component.add(
    name="Time_Const_for_HFC",
    units="years",
    subscripts=["HFC_type"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_const_for_hfc"},
)
def time_const_for_hfc():
    """
    From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_time_const_for_hfc()


_ext_constant_time_const_for_hfc = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_HFC*",
    {"HFC_type": _subscript_dict["HFC_type"]},
    _root,
    {"HFC_type": _subscript_dict["HFC_type"]},
    "_ext_constant_time_const_for_hfc",
)


@component.add(
    name="Time_Const_for_N2O",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_const_for_n2o"},
)
def time_const_for_n2o():
    """
    Value of CH4 and N2O time constants reported in AR5 WG1 Chapter 8 Table 8.A.1 noted to be for calculation of GWP, not for cycle. Value of 117 years determined through optimization.
    """
    return _ext_constant_time_const_for_n2o()


_ext_constant_time_const_for_n2o = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_N2O",
    {},
    _root,
    {},
    "_ext_constant_time_const_for_n2o",
)


@component.add(
    name="Time_Const_for_PFC",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_const_for_pfc"},
)
def time_const_for_pfc():
    """
    based on CF4 From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_time_const_for_pfc()


_ext_constant_time_const_for_pfc = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_PFC",
    {},
    _root,
    {},
    "_ext_constant_time_const_for_pfc",
)


@component.add(
    name="Time_Const_for_SF6",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_const_for_sf6"},
)
def time_const_for_sf6():
    """
    From AR5 WG1 Chapter 8. Table 8.A.1. Lifetimes, Radiative Efficiencies and Metric Values
    """
    return _ext_constant_time_const_for_sf6()


_ext_constant_time_const_for_sf6 = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_SF6",
    {},
    _root,
    {},
    "_ext_constant_time_const_for_sf6",
)


@component.add(
    name="Total_C_from_permafrost",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_c_from_permafrost": 1},
    other_deps={
        "_integ_total_c_from_permafrost": {
            "initial": {},
            "step": {
                "flux_c_from_permafrost_release": 1,
                "gtch4_per_gtc": 1,
                "mtch4_per_gtch4": 1,
                "ch4_emissions_from_permafrost_and_clathrate": 1,
            },
        }
    },
)
def total_c_from_permafrost():
    """
    In terms of total C mass (of both CO2 and CH4) released from permafrost melting, experts estimated that 15-33 Pg C (n=27) could be released by 2040, reaching 120-195 Pg C by 2100, and 276-414 Pg C by 2300 under the high warming scenario (Fig. 1c). 1 PgC = 1GtC.
    """
    return _integ_total_c_from_permafrost()


_integ_total_c_from_permafrost = Integ(
    lambda: flux_c_from_permafrost_release()
    + ch4_emissions_from_permafrost_and_clathrate()
    / gtch4_per_gtc()
    / mtch4_per_gtch4(),
    lambda: 0,
    "_integ_total_c_from_permafrost",
)


@component.add(
    name="Total_CH4_released",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_ch4_released": 1},
    other_deps={
        "_integ_total_ch4_released": {
            "initial": {},
            "step": {
                "ch4_emissions_from_permafrost_and_clathrate": 1,
                "gtch4_per_gtc": 1,
                "mtch4_per_gtch4": 1,
            },
        }
    },
)
def total_ch4_released():
    """
    Of C emissions released from melting of permafrost, only about 2.3 % was expected to be in the form of CH4, corresponding to 0.26-0.85 Pg CH4-C by 2040, 2.03-6.21 Pg CH4-C by 2100 and 4.61-14.24 Pg CH4-C by 2300 (Fig. 1d).
    """
    return _integ_total_ch4_released()


_integ_total_ch4_released = Integ(
    lambda: ch4_emissions_from_permafrost_and_clathrate()
    / gtch4_per_gtc()
    / mtch4_per_gtch4(),
    lambda: 0,
    "_integ_total_ch4_released",
)


@component.add(
    name="Tropospheric_CH4_path_share",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_tropospheric_ch4_path_share"},
)
def tropospheric_ch4_path_share():
    """
    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_tropospheric_ch4_path_share()


_ext_constant_tropospheric_ch4_path_share = ExtConstant(
    "../climate.xlsx",
    "World",
    "tropospheric_CH4_path_share",
    {},
    _root,
    {},
    "_ext_constant_tropospheric_ch4_path_share",
)
