"""
Module other_ghg_cycles
Translated using PySD version 3.0.0
"""


@component.add(
    name="CF4 molar mass", units="g/mole", comp_type="Constant", comp_subtype="Normal"
)
def cf4_molar_mass():
    """
    CF4 grams per mole.
    """
    return 88


@component.add(
    name="CH4 atm conc", units="ppb", comp_type="Auxiliary", comp_subtype="Normal"
)
def ch4_atm_conc():
    return ch4_in_atm() * ppb_ch4_per_mt_ch4()


@component.add(
    name="CH4 Emissions from Permafrost and Clathrate",
    units="Mt/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="CH4 Fractional Uptake",
    units="1/years",
    limits=(5.0, 15.0, 0.1),
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="CH4 in Atm",
    units="Mt",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
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
    name="CH4 molar mass", units="g/mole", comp_type="Constant", comp_subtype="Normal"
)
def ch4_molar_mass():
    """
    CH4 grams per mole
    """
    return 16


@component.add(
    name="CH4 Uptake", units="Mt/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def ch4_uptake():
    return ch4_in_atm() * ch4_fractional_uptake()


@component.add(
    name="Choose RCP", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def choose_rcp():
    """
    Choose RCP (Representative Concentration Pathway) 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "select_RCP",
    {},
    _root,
    {},
    "_ext_constant_choose_rcp",
)


@component.add(
    name="Flux C from permafrost release",
    units="GtC/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="g per t", units="g/t", comp_type="Constant", comp_subtype="Unchangeable"
)
def g_per_t():
    return 1000000.0


@component.add(
    name="global CH4 anthro emissions",
    units="Mt/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def global_ch4_anthro_emissions():
    """
    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) except Power Plants, Energy Conversion, Extraction, and Distribution. Corrected with endogenous data "Total CH4 emissions fossil fuels" Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return total_ch4_emissions_fossil_fuels() + if_then_else(
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
    name="global CH4 anthro emissions RCP",
    units="Mt/year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_global_ch4_anthro_emissions_rcp",
)


@component.add(
    name="global CH4 emissions",
    units="Mt/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def global_ch4_emissions():
    return global_ch4_anthro_emissions() + natural_ch4_emissions()


@component.add(
    name="global HFC emissions",
    units="t/year",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="global HFC emissions RCP",
    units="t/year",
    subscripts=["RCP Scenario", "HFC type"],
    comp_type="Data",
    comp_subtype="External",
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC134a"]},
    _root,
    {
        "RCP Scenario": _subscript_dict["RCP Scenario"],
        "HFC type": _subscript_dict["HFC type"],
    },
    "_ext_data_global_hfc_emissions_rcp",
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC23_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC23"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC32_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC32"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC125_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC125"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC143a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC143a"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC152a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC152a"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC227ea_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC227ea"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC245ca_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC245ca"]},
)

_ext_data_global_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC4310mee_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC4310mee"]},
)


@component.add(
    name="global N2O anthro emissions",
    units="Mt N/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="global N2O anthro emissions RCP",
    units="Mt N/year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_global_n2o_anthro_emissions_rcp",
)


@component.add(
    name="global N2O emissions",
    units="Mt/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def global_n2o_emissions():
    return global_n2o_anthro_emissions() + natural_n2o_emissions()


@component.add(
    name="global PFC emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="global PFC emissions RCP",
    units="t/year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_global_pfc_emissions_rcp",
)


@component.add(
    name="global SF6 emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="global SF6 emissions RCP",
    units="t/year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
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
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_global_sf6_emissions_rcp",
)


@component.add(
    name="global total PFC emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def global_total_pfc_emissions():
    return global_pfc_emissions() + natural_pfc_emissions()


@component.add(
    name="HFC atm conc",
    units="ppt",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def hfc_atm_conc():
    return hfc_in_atm() * ppt_hfc_per_tons_hfc()


@component.add(
    name="HFC in Atm",
    units="t",
    limits=(2.5924e-43, np.nan),
    subscripts=["HFC type"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def hfc_in_atm():
    return _integ_hfc_in_atm()


_integ_hfc_in_atm = Integ(
    lambda: global_hfc_emissions() - hfc_uptake(),
    lambda: initial_hfc(),
    "_integ_hfc_in_atm",
)


@component.add(
    name="HFC molar mass",
    units="g/mole",
    subscripts=["HFC type"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def hfc_molar_mass():
    """
    HFCs grams per mole. http://www.qc.ec.gc.ca/dpe/publication/enjeux_ges/hfc134a_a.html
    """
    return xr.DataArray(
        [102.0, 70.0, 52.0, 120.0, 84.0, 66.0, 170.0, 134.0, 252.0],
        {"HFC type": _subscript_dict["HFC type"]},
        ["HFC type"],
    )


@component.add(
    name="HFC radiative efficiency",
    units="W/(ppb*m2)",
    subscripts=["HFC type"],
    comp_type="Constant",
    comp_subtype="External",
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
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    {"HFC type": _subscript_dict["HFC type"]},
    "_ext_constant_hfc_radiative_efficiency",
)


@component.add(
    name="HFC RF",
    units="W/m2",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def hfc_rf():
    return (
        (hfc_atm_conc() - preindustrial_hfc_conc())
        * hfc_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="HFC uptake",
    units="t/year",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def hfc_uptake():
    return hfc_in_atm() / time_const_for_hfc()


@component.add(
    name="init PFC in atm", units="t", comp_type="Auxiliary", comp_subtype="Normal"
)
def init_pfc_in_atm():
    return init_pfc_in_atm_con() / ppt_pfc_per_tons_pfc()


@component.add(
    name="init PFC in atm con",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
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
    name="inital HFC con",
    units="ppt",
    subscripts=["HFC type"],
    comp_type="Constant",
    comp_subtype="External",
)
def inital_hfc_con():
    return _ext_constant_inital_hfc_con()


_ext_constant_inital_hfc_con = ExtConstant(
    "../climate.xlsx",
    "World",
    "inital_HFC_con*",
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    {"HFC type": _subscript_dict["HFC type"]},
    "_ext_constant_inital_hfc_con",
)


@component.add(
    name="initial CH4", units="Mt", comp_type="Auxiliary", comp_subtype="Normal"
)
def initial_ch4():
    return initial_ch4_conc() / ppb_ch4_per_mt_ch4()


@component.add(
    name="initial CH4 conc", units="ppb", comp_type="Constant", comp_subtype="External"
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
    name="Initial HFC",
    units="t",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_hfc():
    return inital_hfc_con() / ppt_hfc_per_tons_hfc()


@component.add(
    name="initial N2O", units="Mt N", comp_type="Auxiliary", comp_subtype="Normal"
)
def initial_n2o():
    return initial_n2o_conc() / ppb_n2o_per_mtonn()


@component.add(
    name="initial N2O conc", units="ppb", comp_type="Constant", comp_subtype="External"
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
    name="initial SF6", units="t", comp_type="Auxiliary", comp_subtype="Normal"
)
def initial_sf6():
    return initial_sf6_conc() / ppt_sf6_per_tons_sf6()


@component.add(
    name="initial SF6 conc", units="ppt", comp_type="Constant", comp_subtype="External"
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
    name="N2O atm conc", units="ppb", comp_type="Auxiliary", comp_subtype="Normal"
)
def n2o_atm_conc():
    return n2o_in_atm() * ppb_n2o_per_mtonn()


@component.add(
    name="N2O in Atm",
    units="Mt N",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
)
def n2o_in_atm():
    return _integ_n2o_in_atm()


_integ_n2o_in_atm = Integ(
    lambda: global_n2o_emissions() - n2o_uptake(),
    lambda: initial_n2o(),
    "_integ_n2o_in_atm",
)


@component.add(
    name="N2O Uptake", units="Mt/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def n2o_uptake():
    return n2o_in_atm() / time_const_for_n2o()


@component.add(
    name='"N2O-N molar mass"',
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
    name="natural N2O emissions",
    units="MtN/year",
    limits=(0.0, 20.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
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
    name="natural PFC emissions",
    units="t/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def natural_pfc_emissions():
    return preindustrial_pfc() / time_const_for_pfc()


@component.add(
    name="PFC atm conc", units="ppt", comp_type="Auxiliary", comp_subtype="Normal"
)
def pfc_atm_conc():
    return pfc_in_atm() * ppt_pfc_per_tons_pfc()


@component.add(
    name="PFC in Atm",
    units="t",
    limits=(3.01279e-43, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
)
def pfc_in_atm():
    return _integ_pfc_in_atm()


_integ_pfc_in_atm = Integ(
    lambda: global_total_pfc_emissions() - pfc_uptake(),
    lambda: init_pfc_in_atm(),
    "_integ_pfc_in_atm",
)


@component.add(
    name="PFC radiative efficiency",
    units="W/(ppb*m2)",
    comp_type="Constant",
    comp_subtype="External",
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
    name="PFC RF", units="W/m2", comp_type="Auxiliary", comp_subtype="Normal"
)
def pfc_rf():
    return (
        (pfc_atm_conc() - preindustrial_pfc_conc())
        * pfc_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="PFC uptake", units="t/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def pfc_uptake():
    return pfc_in_atm() / time_const_for_pfc()


@component.add(
    name="ppb CH4 per Mt CH4",
    units="ppb/Mt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ppb_ch4_per_mt_ch4():
    return ppt_per_mol() / ch4_molar_mass() * g_per_t() * t_per_mt() / ppt_per_ppb()


@component.add(
    name="ppb N2O per MTonN",
    units="ppb/Mt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ppb_n2o_per_mtonn():
    return ppt_per_mol() / n2on_molar_mass() * g_per_t() * t_per_mt() / ppt_per_ppb()


@component.add(
    name="ppt HFC per Tons HFC",
    units="ppt/t",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ppt_hfc_per_tons_hfc():
    return ppt_per_mol() / hfc_molar_mass() * g_per_t()


@component.add(
    name="ppt per mol",
    units="ppt/mole",
    comp_type="Constant",
    comp_subtype="Unchangeable",
)
def ppt_per_mol():
    return 5.68e-09


@component.add(
    name="ppt per ppb",
    units="ppt/ppb",
    comp_type="Constant",
    comp_subtype="Unchangeable",
)
def ppt_per_ppb():
    return 1000


@component.add(
    name="ppt PFC per Tons PFC",
    units="ppt/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ppt_pfc_per_tons_pfc():
    """
    CF4 ppt per tne
    """
    return ppt_per_mol() / cf4_molar_mass() * g_per_t()


@component.add(
    name="ppt SF6 per Tons SF6",
    units="ppt/t",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ppt_sf6_per_tons_sf6():
    return ppt_per_mol() / sf6_molar_mass() * g_per_t()


@component.add(
    name="preindustrial CH4", units="Mt", comp_type="Constant", comp_subtype="External"
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
    name="preindustrial HFC conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
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
    name="preindustrial PFC", units="t", comp_type="Auxiliary", comp_subtype="Normal"
)
def preindustrial_pfc():
    return preindustrial_pfc_conc() / ppt_pfc_per_tons_pfc()


@component.add(
    name="preindustrial PFC conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
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
    name="preindustrial SF6 conc",
    units="ppt",
    comp_type="Constant",
    comp_subtype="External",
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
    name="reference CH4 time constant",
    units="year",
    limits=(8.0, 10.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
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
    name="reference sensitivity of C from permafrost and clathrate to temperature",
    units="GtC/year/ºC",
    comp_type="Constant",
    comp_subtype="External",
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
    name="reference sensitivity of CH4 from permafrost and clathrate to temperature",
    units="Mt/year/ºC",
    comp_type="Constant",
    comp_subtype="External",
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
    name="sensitivity of methane emissions to permafrost and clathrate",
    units="Dmnl",
    limits=(0.0, 1.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
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
)
def sf6():
    return _integ_sf6()


_integ_sf6 = Integ(
    lambda: global_sf6_emissions() - sf6_uptake(), lambda: initial_sf6(), "_integ_sf6"
)


@component.add(
    name="SF6 atm conc", units="ppt", comp_type="Auxiliary", comp_subtype="Normal"
)
def sf6_atm_conc():
    return sf6() * ppt_sf6_per_tons_sf6()


@component.add(
    name="SF6 molar mass", units="g/mole", comp_type="Constant", comp_subtype="Normal"
)
def sf6_molar_mass():
    """
    SF6 grams per mole
    """
    return 146


@component.add(
    name="SF6 radiative efficiency",
    units="W/(ppb*m2)",
    comp_type="Constant",
    comp_subtype="External",
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
    name="SF6 RF", units="W/m2", comp_type="Auxiliary", comp_subtype="Normal"
)
def sf6_rf():
    return (
        (sf6_atm_conc() - preindustrial_sf6_conc())
        * sf6_radiative_efficiency()
        / ppt_per_ppb()
    )


@component.add(
    name="SF6 uptake", units="t/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def sf6_uptake():
    return sf6() / time_const_for_sf6()


@component.add(
    name="Stratospheric CH4 path share",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="External",
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
    name="t per Mt", units="t/Mt", comp_type="Constant", comp_subtype="Normal"
)
def t_per_mt():
    return 1000000.0


@component.add(
    name="temperature threshold for methane emissions from permafrost and clathrate",
    units="DegreesC",
    limits=(0.0, 4.0, 0.1),
    comp_type="Constant",
    comp_subtype="External",
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
    name="Time Const for CH4",
    units="years",
    limits=(5.0, 15.0, 0.1),
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def time_const_for_ch4():
    return 1 / ch4_fractional_uptake()


@component.add(
    name="Time Const for HFC",
    units="years",
    subscripts=["HFC type"],
    comp_type="Constant",
    comp_subtype="External",
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
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    {"HFC type": _subscript_dict["HFC type"]},
    "_ext_constant_time_const_for_hfc",
)


@component.add(
    name="Time Const for N2O",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Time Const for PFC",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Time Const for SF6",
    units="years",
    comp_type="Constant",
    comp_subtype="External",
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
    name="Total C from permafrost",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def total_c_from_permafrost():
    """
    In terms of total C mass (of both CO2 and CH4) released from permafrost melting, experts estimated that 15-33 Pg C (n=27) could be released by 2040, reaching 120-195 Pg C by 2100, and 276-414 Pg C by 2300 under the high warming scenario (Fig. 1c). 1 PgC = 1GtC.
    """
    return _integ_total_c_from_permafrost()


_integ_total_c_from_permafrost = Integ(
    lambda: flux_c_from_permafrost_release()
    + ch4_emissions_from_permafrost_and_clathrate() / ch4_per_c() / mt_per_gt(),
    lambda: 0,
    "_integ_total_c_from_permafrost",
)


@component.add(
    name="Total CH4 released", units="GtC", comp_type="Stateful", comp_subtype="Integ"
)
def total_ch4_released():
    """
    Of C emissions released from melting of permafrost, only about 2.3 % was expected to be in the form of CH4, corresponding to 0.26-0.85 Pg CH4-C by 2040, 2.03-6.21 Pg CH4-C by 2100 and 4.61-14.24 Pg CH4-C by 2300 (Fig. 1d).
    """
    return _integ_total_ch4_released()


_integ_total_ch4_released = Integ(
    lambda: ch4_emissions_from_permafrost_and_clathrate() / ch4_per_c() / mt_per_gt(),
    lambda: 0,
    "_integ_total_ch4_released",
)


@component.add(
    name="Tropospheric CH4 path share",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="External",
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
