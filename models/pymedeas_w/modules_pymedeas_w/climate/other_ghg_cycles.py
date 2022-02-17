"""
Module other_ghg_cycles
Translated using PySD version 2.2.1
"""


def cf4_molar_mass():
    """
    Real Name: CF4 molar mass
    Original Eqn: 88
    Units: g/mole
    Limits: (None, None)
    Type: constant
    Subs: None

    CF4 grams per mole.
    """
    return 88


def ch4_atm_conc():
    """
    Real Name: CH4 atm conc
    Original Eqn: CH4 in Atm*ppb CH4 per Mt CH4
    Units: ppb
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ch4_in_atm() * ppb_ch4_per_mt_ch4()


def ch4_emissions_from_permafrost_and_clathrate():
    """
    Real Name: CH4 Emissions from Permafrost and Clathrate
    Original Eqn: sensitivity of methane emissions to permafrost and clathrate*reference sensitivity of CH4 from permafrost and clathrate to temperature *MAX(0,Temperature change-temperature threshold for methane emissions from permafrost and clathrate )
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None

    Methane emissions from melting permafrost and clathrate outgassing are
        assumed to be nonlinear. Emissions are assumed to be zero if warming over
        preindustrial levels is less than a threshold and linear in temperature
        above the threshold. The default sensitivity is zero, but the strength of
        the effect and threshold can be set by the user.
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


def ch4_fractional_uptake():
    """
    Real Name: CH4 Fractional Uptake
    Original Eqn: 1/reference CH4 time constant*( Tropospheric CH4 path share/(Stratospheric CH4 path share*(CH4 in Atm/preindustrial CH4 ) + 1-Stratospheric CH4 path share) +(1-Tropospheric CH4 path share) )
    Units: 1/years
    Limits: (5.0, 15.0, 0.1)
    Type: component
    Subs: None

    dCH4/dt = E – k1*CH4*OH – k2*CH4        E = emissions. The k1 path is dominant (k2 reflects soil processes and other minor
        sinks)        dOH/dt = F – k3*CH4*OH – k4*OH        F = formation. In this case the methane reaction is the minor path (15-20% of loss)
        so OH in equilibrium is        OHeq = F/(k3*CH4+k4)        substituting        dCH4/dt = E – k1*CH4* F/(k3*CH4+k4) – k2*CH4        thus the total fractional uptake is        k1*F/(k3*CH4+k4)+k2        which is robust at 0        Formulated from Meinshausen et al., 2011
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


def ch4_in_atm():
    """
    Real Name: CH4 in Atm
    Original Eqn: INTEG ( CH4 Emissions from Permafrost and Clathrate+global CH4 emissions-CH4 Uptake, initial CH4)
    Units: Mt
    Limits: (3.01279e-43, None)
    Type: component
    Subs: None


    """
    return _integ_ch4_in_atm()


def ch4_molar_mass():
    """
    Real Name: CH4 molar mass
    Original Eqn: 16
    Units: g/mole
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 grams per mole
    """
    return 16


def ch4_uptake():
    """
    Real Name: CH4 Uptake
    Original Eqn: CH4 in Atm*CH4 Fractional Uptake
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ch4_in_atm() * ch4_fractional_uptake()


def choose_rcp():
    """
    Real Name: Choose RCP
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'select_RCP')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Choose RCP (Representative Concentration Pathway)        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


def flux_c_from_permafrost_release():
    """
    Real Name: Flux C from permafrost release
    Original Eqn: sensitivity of methane emissions to permafrost and clathrate*reference sensitivity of C from permafrost and clathrate to temperature *MAX(0,Temperature change-temperature threshold for methane emissions from permafrost and clathrate )
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        sensitivity_of_methane_emissions_to_permafrost_and_clathrate()
        * reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature()
        * np.maximum(
            0,
            temperature_change()
            - temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate(),
        )
    )


def g_per_t():
    """
    Real Name: g per t
    Original Eqn: 1e+06
    Units: g/t
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1e06


def global_ch4_anthro_emissions():
    """
    Real Name: global CH4 anthro emissions
    Original Eqn: Total CH4 emissions fossil fuels+IF THEN ELSE(Choose RCP=1, global CH4 anthro emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, global CH4 anthro emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, global CH4 anthro emissions RCP[RCP60], global CH4 anthro emissions RCP[RCP85])))
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None

    "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
        except  Power Plants, Energy Conversion, Extraction, and Distribution.
        Corrected with endogenous data "Total CH4 emissions fossil fuels"        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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


@subs(["RCP Scenario"], _subscript_dict)
def global_ch4_anthro_emissions_rcp():
    """
    Real Name: global CH4 anthro emissions RCP
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'CH4_emissions')
    Units: Mt/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_ch4_anthro_emissions_rcp(time())


def global_ch4_emissions():
    """
    Real Name: global CH4 emissions
    Original Eqn: global CH4 anthro emissions + natural CH4 emissions
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return global_ch4_anthro_emissions() + natural_ch4_emissions()


@subs(["HFC type"], _subscript_dict)
def global_hfc_emissions():
    """
    Real Name: global HFC emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, global HFC emissions RCP[RCP26, HFC type], IF THEN ELSE(Choose RCP=2, global HFC emissions RCP[RCP45, HFC type], IF THEN ELSE(Choose RCP=3, global HFC emissions RCP[RCP60, HFC type], global HFC emissions RCP[RCP85, HFC type])))
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: rearrange(
            global_hfc_emissions_rcp().loc["RCP26", :].reset_coords(drop=True),
            ["HFC type"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: rearrange(
                global_hfc_emissions_rcp().loc["RCP45", :].reset_coords(drop=True),
                ["HFC type"],
                _subscript_dict,
            ),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: rearrange(
                    global_hfc_emissions_rcp().loc["RCP60", :].reset_coords(drop=True),
                    ["HFC type"],
                    _subscript_dict,
                ),
                lambda: rearrange(
                    global_hfc_emissions_rcp().loc["RCP85", :].reset_coords(drop=True),
                    ["HFC type"],
                    _subscript_dict,
                ),
            ),
        ),
    )


@subs(["RCP Scenario", "HFC type"], _subscript_dict)
def global_hfc_emissions_rcp():
    """
    Real Name: global HFC emissions RCP
    Original Eqn:
      GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'HFC134a_emissions')
        .
        .
        .
      GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'HFC4310mee_emissions')
    Units: t/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario', 'HFC type']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_hfc_emissions_rcp(time())


def global_n2o_anthro_emissions():
    """
    Real Name: global N2O anthro emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, global N2O anthro emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, global N2O anthro emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, global N2O anthro emissions RCP[RCP60], global N2O anthro emissions RCP[RCP85])))
    Units: Mt N/year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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


@subs(["RCP Scenario"], _subscript_dict)
def global_n2o_anthro_emissions_rcp():
    """
    Real Name: global N2O anthro emissions RCP
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'N2O_emissions')
    Units: Mt N/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_n2o_anthro_emissions_rcp(time())


def global_n2o_emissions():
    """
    Real Name: global N2O emissions
    Original Eqn: global N2O anthro emissions+natural N2O emissions
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return global_n2o_anthro_emissions() + natural_n2o_emissions()


def global_pfc_emissions():
    """
    Real Name: global PFC emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, global PFC emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, global PFC emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3,global PFC emissions RCP[RCP60], global PFC emissions RCP[RCP85])))
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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


@subs(["RCP Scenario"], _subscript_dict)
def global_pfc_emissions_rcp():
    """
    Real Name: global PFC emissions RCP
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'PFCs_emissions')
    Units: t/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_pfc_emissions_rcp(time())


def global_sf6_emissions():
    """
    Real Name: global SF6 emissions
    Original Eqn: IF THEN ELSE(Choose RCP=1, global SF6 emissions RCP[RCP26], IF THEN ELSE(Choose RCP=2, global SF6 emissions RCP[RCP45], IF THEN ELSE(Choose RCP=3, global SF6 emissions RCP[RCP60], global SF6 emissions RCP[RCP85])))
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None

    Historic data + projections "Representative Concentration Pathways" (RCPs, see
        http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
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


@subs(["RCP Scenario"], _subscript_dict)
def global_sf6_emissions_rcp():
    """
    Real Name: global SF6 emissions RCP
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'year_emissions', 'SF6_emissions')
    Units: t/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    Historic data + projections "Representative Concentration Pathways" (RCPs,
        see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_global_sf6_emissions_rcp(time())


def global_total_pfc_emissions():
    """
    Real Name: global total PFC emissions
    Original Eqn: global PFC emissions+natural PFC emissions
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return global_pfc_emissions() + natural_pfc_emissions()


@subs(["HFC type"], _subscript_dict)
def hfc_atm_conc():
    """
    Real Name: HFC atm conc
    Original Eqn: HFC in Atm[HFC type]*ppt HFC per Tons HFC[HFC type]
    Units: ppt
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']


    """
    return hfc_in_atm() * ppt_hfc_per_tons_hfc()


@subs(["HFC type"], _subscript_dict)
def hfc_in_atm():
    """
    Real Name: HFC in Atm
    Original Eqn: INTEG ( global HFC emissions[HFC type]-HFC uptake[HFC type], Initial HFC[HFC type])
    Units: t
    Limits: (2.5924e-43, None)
    Type: component
    Subs: ['HFC type']


    """
    return _integ_hfc_in_atm()


@subs(["HFC type"], _subscript_dict)
def hfc_molar_mass():
    """
    Real Name: HFC molar mass
    Original Eqn: 102,70,52,120,84,66,170,134,252
    Units: g/mole
    Limits: (None, None)
    Type: constant
    Subs: ['HFC type']

    HFCs grams per mole.
        http://www.qc.ec.gc.ca/dpe/publication/enjeux_ges/hfc134a_a.html
    """
    return xr.DataArray(
        [102.0, 70.0, 52.0, 120.0, 84.0, 66.0, 170.0, 134.0, 252.0],
        {"HFC type": _subscript_dict["HFC type"]},
        ["HFC type"],
    )


@subs(["HFC type"], _subscript_dict)
def hfc_radiative_efficiency():
    """
    Real Name: HFC radiative efficiency
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'HFC_radiative_efficiency*')
    Units: W/(ppb*m2)
    Limits: (None, None)
    Type: constant
    Subs: ['HFC type']

    From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_hfc_radiative_efficiency()


@subs(["HFC type"], _subscript_dict)
def hfc_rf():
    """
    Real Name: HFC RF
    Original Eqn: (HFC atm conc[HFC type]-preindustrial HFC conc)*HFC radiative efficiency[HFC type]/ppt per ppb
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']


    """
    return (
        (hfc_atm_conc() - preindustrial_hfc_conc())
        * hfc_radiative_efficiency()
        / ppt_per_ppb()
    )


@subs(["HFC type"], _subscript_dict)
def hfc_uptake():
    """
    Real Name: HFC uptake
    Original Eqn: HFC in Atm[HFC type]/Time Const for HFC[HFC type]
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']


    """
    return hfc_in_atm() / time_const_for_hfc()


def init_pfc_in_atm():
    """
    Real Name: init PFC in atm
    Original Eqn: init PFC in atm con/ppt PFC per Tons PFC
    Units: t
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return init_pfc_in_atm_con() / ppt_pfc_per_tons_pfc()


def init_pfc_in_atm_con():
    """
    Real Name: init PFC in atm con
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'init_PFC_in_atm_con')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: None

    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_init_pfc_in_atm_con()


@subs(["HFC type"], _subscript_dict)
def inital_hfc_con():
    """
    Real Name: inital HFC con
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'inital_HFC_con*')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: ['HFC type']


    """
    return _ext_constant_inital_hfc_con()


def initial_ch4():
    """
    Real Name: initial CH4
    Original Eqn: initial CH4 conc/ppb CH4 per Mt CH4
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_ch4_conc() / ppb_ch4_per_mt_ch4()


def initial_ch4_conc():
    """
    Real Name: initial CH4 conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'initial_CH4_conc')
    Units: ppb
    Limits: (None, None)
    Type: constant
    Subs: None

    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_ch4_conc()


@subs(["HFC type"], _subscript_dict)
def initial_hfc():
    """
    Real Name: Initial HFC
    Original Eqn: inital HFC con[HFC type]/ppt HFC per Tons HFC[HFC type]
    Units: t
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']


    """
    return inital_hfc_con() / ppt_hfc_per_tons_hfc()


def initial_n2o():
    """
    Real Name: initial N2O
    Original Eqn: initial N2O conc/ppb N2O per MTonN
    Units: Mt N
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_n2o_conc() / ppb_n2o_per_mtonn()


def initial_n2o_conc():
    """
    Real Name: initial N2O conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'initial_N2O_conc')
    Units: ppb
    Limits: (None, None)
    Type: constant
    Subs: None

    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_n2o_conc()


def initial_sf6():
    """
    Real Name: initial SF6
    Original Eqn: initial SF6 conc/ppt SF6 per Tons SF6
    Units: t
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_sf6_conc() / ppt_sf6_per_tons_sf6()


def initial_sf6_conc():
    """
    Real Name: initial SF6 conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'initial_SF6_conc')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: None

    Historical data. NASA. GISS. https://data.giss.nasa.gov/modelforce/ghgases/
    """
    return _ext_constant_initial_sf6_conc()


def n2o_atm_conc():
    """
    Real Name: N2O atm conc
    Original Eqn: N2O in Atm*ppb N2O per MTonN
    Units: ppb
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return n2o_in_atm() * ppb_n2o_per_mtonn()


def n2o_in_atm():
    """
    Real Name: N2O in Atm
    Original Eqn: INTEG ( global N2O emissions-N2O Uptake, initial N2O)
    Units: Mt N
    Limits: (3.01279e-43, None)
    Type: component
    Subs: None


    """
    return _integ_n2o_in_atm()


def n2o_uptake():
    """
    Real Name: N2O Uptake
    Original Eqn: N2O in Atm/Time Const for N2O
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return n2o_in_atm() / time_const_for_n2o()


def n2on_molar_mass():
    """
    Real Name: "N2O-N molar mass"
    Original Eqn: 28
    Units: g/mole
    Limits: (None, None)
    Type: constant
    Subs: None

    NO2-N grams per mole.
    """
    return 28


def natural_n2o_emissions():
    """
    Real Name: natural N2O emissions
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'natural_N2O_emissions')
    Units: MtN/year
    Limits: (0.0, 20.0, 0.1)
    Type: constant
    Subs: None

    AR5 WG1 Chapter 6 Table 6.9
    """
    return _ext_constant_natural_n2o_emissions()


def natural_pfc_emissions():
    """
    Real Name: natural PFC emissions
    Original Eqn: preindustrial PFC/Time Const for PFC
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return preindustrial_pfc() / time_const_for_pfc()


def pfc_atm_conc():
    """
    Real Name: PFC atm conc
    Original Eqn: PFC in Atm*ppt PFC per Tons PFC
    Units: ppt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pfc_in_atm() * ppt_pfc_per_tons_pfc()


def pfc_in_atm():
    """
    Real Name: PFC in Atm
    Original Eqn: INTEG ( global total PFC emissions-PFC uptake, init PFC in atm)
    Units: t
    Limits: (3.01279e-43, None)
    Type: component
    Subs: None


    """
    return _integ_pfc_in_atm()


def pfc_radiative_efficiency():
    """
    Real Name: PFC radiative efficiency
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'PFC_radiative_efficiency')
    Units: W/(ppb*m2)
    Limits: (None, None)
    Type: constant
    Subs: None

    Radiative efficiency of CF4.        From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_pfc_radiative_efficiency()


def pfc_rf():
    """
    Real Name: PFC RF
    Original Eqn: (PFC atm conc-preindustrial PFC conc)*PFC radiative efficiency/ppt per ppb
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (pfc_atm_conc() - preindustrial_pfc_conc())
        * pfc_radiative_efficiency()
        / ppt_per_ppb()
    )


def pfc_uptake():
    """
    Real Name: PFC uptake
    Original Eqn: PFC in Atm/Time Const for PFC
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pfc_in_atm() / time_const_for_pfc()


def ppb_ch4_per_mt_ch4():
    """
    Real Name: ppb CH4 per Mt CH4
    Original Eqn: ppt per mol/CH4 molar mass*g per t*t per Mt/ppt per ppb
    Units: ppb/Mt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ppt_per_mol() / ch4_molar_mass() * g_per_t() * t_per_mt() / ppt_per_ppb()


def ppb_n2o_per_mtonn():
    """
    Real Name: ppb N2O per MTonN
    Original Eqn: ppt per mol/"N2O-N molar mass"*g per t*t per Mt/ppt per ppb
    Units: ppb/Mt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ppt_per_mol() / n2on_molar_mass() * g_per_t() * t_per_mt() / ppt_per_ppb()


@subs(["HFC type"], _subscript_dict)
def ppt_hfc_per_tons_hfc():
    """
    Real Name: ppt HFC per Tons HFC
    Original Eqn: ppt per mol/HFC molar mass[HFC type]*g per t
    Units: ppt/t
    Limits: (None, None)
    Type: component
    Subs: ['HFC type']


    """
    return ppt_per_mol() / hfc_molar_mass() * g_per_t()


def ppt_per_mol():
    """
    Real Name: ppt per mol
    Original Eqn: 5.68e-09
    Units: ppt/mole
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 5.68e-09


def ppt_per_ppb():
    """
    Real Name: ppt per ppb
    Original Eqn: 1000
    Units: ppt/ppb
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1000


def ppt_pfc_per_tons_pfc():
    """
    Real Name: ppt PFC per Tons PFC
    Original Eqn: ppt per mol/CF4 molar mass*g per t
    Units: ppt/t
    Limits: (None, None)
    Type: component
    Subs: None

    CF4 ppt per tne
    """
    return ppt_per_mol() / cf4_molar_mass() * g_per_t()


def ppt_sf6_per_tons_sf6():
    """
    Real Name: ppt SF6 per Tons SF6
    Original Eqn: ppt per mol/SF6 molar mass*g per t
    Units: ppt/t
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ppt_per_mol() / sf6_molar_mass() * g_per_t()


def preindustrial_ch4():
    """
    Real Name: preindustrial CH4
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preindustrial_CH4')
    Units: Mt
    Limits: (None, None)
    Type: constant
    Subs: None

    Law Dome ice core
    """
    return _ext_constant_preindustrial_ch4()


def preindustrial_hfc_conc():
    """
    Real Name: preindustrial HFC conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preindustrial_HFC_conc')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_preindustrial_hfc_conc()


def preindustrial_pfc():
    """
    Real Name: preindustrial PFC
    Original Eqn: preindustrial PFC conc/ppt PFC per Tons PFC
    Units: t
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return preindustrial_pfc_conc() / ppt_pfc_per_tons_pfc()


def preindustrial_pfc_conc():
    """
    Real Name: preindustrial PFC conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preindustrial_PFC_conc')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_preindustrial_pfc_conc()


def preindustrial_sf6_conc():
    """
    Real Name: preindustrial SF6 conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'preindustrial_SF6_conc')
    Units: ppt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_preindustrial_sf6_conc()


def reference_ch4_time_constant():
    """
    Real Name: reference CH4 time constant
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'reference_CH4_time_constant')
    Units: year
    Limits: (8.0, 10.0, 0.1)
    Type: constant
    Subs: None

    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_reference_ch4_time_constant()


def reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature():
    """
    Real Name: reference sensitivity of C from permafrost and clathrate to temperature
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'reference_sensitivity_of_C_from_permafrost_and_clathrate_to_temperature')
    Units: GtC/year/ºC
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return (
        _ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature()
    )


def reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature():
    """
    Real Name: reference sensitivity of CH4 from permafrost and clathrate to temperature
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'reference_sensitivity_of_CH4_from_permafrost_and_clathrate_to_temperature')
    Units: Mt/year/ºC
    Limits: (None, None)
    Type: constant
    Subs: None

    The reference emissions of methane from melting permafrost and outgassing
        from clathrates per degree C of warming above the threshold.
    """
    return (
        _ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature()
    )


def sensitivity_of_methane_emissions_to_permafrost_and_clathrate():
    """
    Real Name: sensitivity of methane emissions to permafrost and clathrate
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'sensitivity_of_methane_emissions_to_permafrost_and_clathrate')
    Units: Dmnl
    Limits: (0.0, 1.0, 0.1)
    Type: constant
    Subs: None

    0 = no feedback        1 = base feedback
    """
    return _ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate()


def sf6():
    """
    Real Name: SF6
    Original Eqn: INTEG ( global SF6 emissions-SF6 uptake, initial SF6)
    Units: t
    Limits: (3.01279e-43, None)
    Type: component
    Subs: None


    """
    return _integ_sf6()


def sf6_atm_conc():
    """
    Real Name: SF6 atm conc
    Original Eqn: SF6*ppt SF6 per Tons SF6
    Units: ppt
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sf6() * ppt_sf6_per_tons_sf6()


def sf6_molar_mass():
    """
    Real Name: SF6 molar mass
    Original Eqn: 146
    Units: g/mole
    Limits: (None, None)
    Type: constant
    Subs: None

    SF6 grams per mole
    """
    return 146


def sf6_radiative_efficiency():
    """
    Real Name: SF6 radiative efficiency
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'SF6_radiative_efficiency')
    Units: W/(ppb*m2)
    Limits: (None, None)
    Type: constant
    Subs: None

    From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_sf6_radiative_efficiency()


def sf6_rf():
    """
    Real Name: SF6 RF
    Original Eqn: (SF6 atm conc-preindustrial SF6 conc)*SF6 radiative efficiency/ppt per ppb
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (sf6_atm_conc() - preindustrial_sf6_conc())
        * sf6_radiative_efficiency()
        / ppt_per_ppb()
    )


def sf6_uptake():
    """
    Real Name: SF6 uptake
    Original Eqn: SF6/Time Const for SF6
    Units: t/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sf6() / time_const_for_sf6()


def stratospheric_ch4_path_share():
    """
    Real Name: Stratospheric CH4 path share
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'stratospheric_CH4_path_share')
    Units: Dmnl
    Limits: (0.0, 1.0)
    Type: constant
    Subs: None

    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_stratospheric_ch4_path_share()


def t_per_mt():
    """
    Real Name: t per Mt
    Original Eqn: 1e+06
    Units: t/Mt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1e06


def temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate():
    """
    Real Name: temperature threshold for methane emissions from permafrost and clathrate
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate')
    Units: DegreesC
    Limits: (0.0, 4.0, 0.1)
    Type: constant
    Subs: None

    The threshold rise in global mean surface temperature above preindustrial
        levels that triggers the release of methane from permafrost and
        clathrates. Below this threshold, emissions from    these sources are assumed
        to be zero. Above the threshold, emissions are assumed to rise linearly
        with temperature.
    """
    return (
        _ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate()
    )


def time_const_for_ch4():
    """
    Real Name: Time Const for CH4
    Original Eqn: 1/CH4 Fractional Uptake
    Units: years
    Limits: (5.0, 15.0, 0.1)
    Type: component
    Subs: None


    """
    return 1 / ch4_fractional_uptake()


@subs(["HFC type"], _subscript_dict)
def time_const_for_hfc():
    """
    Real Name: Time Const for HFC
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'time_const_for_HFC*')
    Units: years
    Limits: (None, None)
    Type: constant
    Subs: ['HFC type']

    From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_time_const_for_hfc()


def time_const_for_n2o():
    """
    Real Name: Time Const for N2O
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'time_const_for_N2O')
    Units: years
    Limits: (None, None)
    Type: constant
    Subs: None

    Value of CH4 and N2O time constants reported in AR5 WG1 Chapter 8 Table
        8.A.1 noted to be for calculation of GWP, not for cycle. Value of 117
        years determined through optimization.
    """
    return _ext_constant_time_const_for_n2o()


def time_const_for_pfc():
    """
    Real Name: Time Const for PFC
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'time_const_for_PFC')
    Units: years
    Limits: (None, None)
    Type: constant
    Subs: None

    based on CF4        From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_time_const_for_pfc()


def time_const_for_sf6():
    """
    Real Name: Time Const for SF6
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'time_const_for_SF6')
    Units: years
    Limits: (None, None)
    Type: constant
    Subs: None

    From AR5 WG1 Chapter 8.  Table 8.A.1. Lifetimes, Radiative Efficiencies
        and Metric Values
    """
    return _ext_constant_time_const_for_sf6()


def total_c_from_permafrost():
    """
    Real Name: Total C from permafrost
    Original Eqn: INTEG ( Flux C from permafrost release+CH4 Emissions from Permafrost and Clathrate/CH4 per C/Mt per Gt, 0)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    In terms of total C mass (of both CO2 and CH4) released from permafrost
        melting, experts estimated that 15-33 Pg C (n=27) could be released by
        2040, reaching 120-195 Pg C by 2100, and 276-414 Pg C by 2300 under the
        high warming scenario (Fig. 1c). 1 PgC = 1GtC.
    """
    return _integ_total_c_from_permafrost()


def total_ch4_released():
    """
    Real Name: Total CH4 released
    Original Eqn: INTEG ( CH4 Emissions from Permafrost and Clathrate/CH4 per C/Mt per Gt, 0)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Of C emissions released from melting of permafrost, only about 2.3 % was
        expected to be in the form of CH4, corresponding to 0.26-0.85 Pg CH4-C by
        2040, 2.03-6.21 Pg CH4-C by 2100 and 4.61-14.24 Pg CH4-C by 2300 (Fig. 1d).
    """
    return _integ_total_ch4_released()


def tropospheric_ch4_path_share():
    """
    Real Name: Tropospheric CH4 path share
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'tropospheric_CH4_path_share')
    Units: Dmnl
    Limits: (0.0, 1.0)
    Type: constant
    Subs: None

    Calculated from AR5 WG1 Chapter 6
    """
    return _ext_constant_tropospheric_ch4_path_share()


_integ_ch4_in_atm = Integ(
    lambda: ch4_emissions_from_permafrost_and_clathrate()
    + global_ch4_emissions()
    - ch4_uptake(),
    lambda: initial_ch4(),
    "_integ_ch4_in_atm",
)


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "select_RCP",
    {},
    _root,
    "_ext_constant_choose_rcp",
)


_ext_data_global_ch4_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "CH4_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_global_ch4_anthro_emissions_rcp",
)


_ext_data_global_hfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "HFC134a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC134a"]},
    _root,
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


_ext_data_global_n2o_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "N2O_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_global_n2o_anthro_emissions_rcp",
)


_ext_data_global_pfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "PFCs_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_global_pfc_emissions_rcp",
)


_ext_data_global_sf6_emissions_rcp = ExtData(
    "../climate.xlsx",
    "World",
    "year_emissions",
    "SF6_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_global_sf6_emissions_rcp",
)


@subs(["HFC type"], _subscript_dict)
def _integ_init_hfc_in_atm():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for hfc_in_atm
    Limits: None
    Type: setup
    Subs: ['HFC type']

    Provides initial conditions for hfc_in_atm function
    """
    return initial_hfc()


@subs(["HFC type"], _subscript_dict)
def _integ_input_hfc_in_atm():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for hfc_in_atm
    Limits: None
    Type: component
    Subs: ['HFC type']

    Provides derivative for hfc_in_atm function
    """
    return global_hfc_emissions() - hfc_uptake()


_integ_hfc_in_atm = Integ(
    _integ_input_hfc_in_atm, _integ_init_hfc_in_atm, "_integ_hfc_in_atm"
)


_ext_constant_hfc_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "HFC_radiative_efficiency*",
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    "_ext_constant_hfc_radiative_efficiency",
)


_ext_constant_init_pfc_in_atm_con = ExtConstant(
    "../climate.xlsx",
    "World",
    "init_PFC_in_atm_con",
    {},
    _root,
    "_ext_constant_init_pfc_in_atm_con",
)


_ext_constant_inital_hfc_con = ExtConstant(
    "../climate.xlsx",
    "World",
    "inital_HFC_con*",
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    "_ext_constant_inital_hfc_con",
)


_ext_constant_initial_ch4_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_CH4_conc",
    {},
    _root,
    "_ext_constant_initial_ch4_conc",
)


_ext_constant_initial_n2o_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_N2O_conc",
    {},
    _root,
    "_ext_constant_initial_n2o_conc",
)


_ext_constant_initial_sf6_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "initial_SF6_conc",
    {},
    _root,
    "_ext_constant_initial_sf6_conc",
)


_integ_n2o_in_atm = Integ(
    lambda: global_n2o_emissions() - n2o_uptake(),
    lambda: initial_n2o(),
    "_integ_n2o_in_atm",
)


_ext_constant_natural_n2o_emissions = ExtConstant(
    "../climate.xlsx",
    "World",
    "natural_N2O_emissions",
    {},
    _root,
    "_ext_constant_natural_n2o_emissions",
)


_integ_pfc_in_atm = Integ(
    lambda: global_total_pfc_emissions() - pfc_uptake(),
    lambda: init_pfc_in_atm(),
    "_integ_pfc_in_atm",
)


_ext_constant_pfc_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "PFC_radiative_efficiency",
    {},
    _root,
    "_ext_constant_pfc_radiative_efficiency",
)


_ext_constant_preindustrial_ch4 = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_CH4",
    {},
    _root,
    "_ext_constant_preindustrial_ch4",
)


_ext_constant_preindustrial_hfc_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_HFC_conc",
    {},
    _root,
    "_ext_constant_preindustrial_hfc_conc",
)


_ext_constant_preindustrial_pfc_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_PFC_conc",
    {},
    _root,
    "_ext_constant_preindustrial_pfc_conc",
)


_ext_constant_preindustrial_sf6_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "preindustrial_SF6_conc",
    {},
    _root,
    "_ext_constant_preindustrial_sf6_conc",
)


_ext_constant_reference_ch4_time_constant = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_CH4_time_constant",
    {},
    _root,
    "_ext_constant_reference_ch4_time_constant",
)


_ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_sensitivity_of_C_from_permafrost_and_clathrate_to_temperature",
    {},
    _root,
    "_ext_constant_reference_sensitivity_of_c_from_permafrost_and_clathrate_to_temperature",
)


_ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature = ExtConstant(
    "../climate.xlsx",
    "World",
    "reference_sensitivity_of_CH4_from_permafrost_and_clathrate_to_temperature",
    {},
    _root,
    "_ext_constant_reference_sensitivity_of_ch4_from_permafrost_and_clathrate_to_temperature",
)


_ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate = (
    ExtConstant(
        "../climate.xlsx",
        "World",
        "sensitivity_of_methane_emissions_to_permafrost_and_clathrate",
        {},
        _root,
        "_ext_constant_sensitivity_of_methane_emissions_to_permafrost_and_clathrate",
    )
)


_integ_sf6 = Integ(
    lambda: global_sf6_emissions() - sf6_uptake(), lambda: initial_sf6(), "_integ_sf6"
)


_ext_constant_sf6_radiative_efficiency = ExtConstant(
    "../climate.xlsx",
    "World",
    "SF6_radiative_efficiency",
    {},
    _root,
    "_ext_constant_sf6_radiative_efficiency",
)


_ext_constant_stratospheric_ch4_path_share = ExtConstant(
    "../climate.xlsx",
    "World",
    "stratospheric_CH4_path_share",
    {},
    _root,
    "_ext_constant_stratospheric_ch4_path_share",
)


_ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate = ExtConstant(
    "../climate.xlsx",
    "World",
    "temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate",
    {},
    _root,
    "_ext_constant_temperature_threshold_for_methane_emissions_from_permafrost_and_clathrate",
)


_ext_constant_time_const_for_hfc = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_HFC*",
    {"HFC type": _subscript_dict["HFC type"]},
    _root,
    "_ext_constant_time_const_for_hfc",
)


_ext_constant_time_const_for_n2o = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_N2O",
    {},
    _root,
    "_ext_constant_time_const_for_n2o",
)


_ext_constant_time_const_for_pfc = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_PFC",
    {},
    _root,
    "_ext_constant_time_const_for_pfc",
)


_ext_constant_time_const_for_sf6 = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_const_for_SF6",
    {},
    _root,
    "_ext_constant_time_const_for_sf6",
)


_integ_total_c_from_permafrost = Integ(
    lambda: flux_c_from_permafrost_release()
    + ch4_emissions_from_permafrost_and_clathrate() / ch4_per_c() / mt_per_gt(),
    lambda: 0,
    "_integ_total_c_from_permafrost",
)


_integ_total_ch4_released = Integ(
    lambda: ch4_emissions_from_permafrost_and_clathrate() / ch4_per_c() / mt_per_gt(),
    lambda: 0,
    "_integ_total_ch4_released",
)


_ext_constant_tropospheric_ch4_path_share = ExtConstant(
    "../climate.xlsx",
    "World",
    "tropospheric_CH4_path_share",
    {},
    _root,
    "_ext_constant_tropospheric_ch4_path_share",
)
