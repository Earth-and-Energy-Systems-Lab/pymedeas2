"""
Module radiative_forcing
Translated using PySD version 2.2.1
"""


def adjusted_other_forcings():
    """
    Real Name: Adjusted other forcings
    Original Eqn: other forcings+IF THEN ELSE(Time>last historical RF year, mineral aerosols and land RF, 0)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    RCP does not include solar and albedo in their other forcings; the adjusted values
        add the values for these from MAGICC. It is the adjusted other forcings
        that are included in the total radiative forcing.        +IF THEN ELSE(Time>=last historical RF year, mineral aerosols and land RF,
        0)
    """
    return other_forcings() + if_then_else(
        time() > last_historical_rf_year(),
        lambda: mineral_aerosols_and_land_rf(),
        lambda: 0,
    )


def adjustment_for_ch4_and_n2oref():
    """
    Real Name: Adjustment for CH4 and N2Oref
    Original Eqn: CH4 N2O interaction coef 1 * LN( 1 +CH4 N2O interaction coef 2 *(CH4 atm conc*N2O reference conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 1 +CH4 N2O interaction coef 3 *CH4 atm conc*CH4 N2O unit adj *(CH4 atm conc*N2O reference conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 2)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1
        Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.        Adjusts total RF from CH4 and N2O to be less than the sum of RF from each
        individually to account for interactions between both gases.
    """
    return ch4_n2o_interaction_coef_1() * np.log(
        1
        + ch4_n2o_interaction_coef_2()
        * (
            ch4_atm_conc()
            * n2o_reference_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_1()
        + ch4_n2o_interaction_coef_3()
        * ch4_atm_conc()
        * ch4_n2o_unit_adj()
        * (
            ch4_atm_conc()
            * n2o_reference_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_2()
    )


def adjustment_for_ch4ref_and_n2o():
    """
    Real Name: Adjustment for CH4ref and N2O
    Original Eqn: CH4 N2O interaction coef 1 * LN( 1 +CH4 N2O interaction coef 2 *(CH4 reference conc*N2O atm conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 1 +CH4 N2O interaction coef 3 *CH4 reference conc*CH4 N2O unit adj *(CH4 reference conc*N2O atm conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 2)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1
        Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.        Adjusts total RF from CH4 and N2O to be less than the sum of RF from each
        individually to account for interactions between both gases.
    """
    return ch4_n2o_interaction_coef_1() * np.log(
        1
        + ch4_n2o_interaction_coef_2()
        * (
            ch4_reference_conc()
            * n2o_atm_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_1()
        + ch4_n2o_interaction_coef_3()
        * ch4_reference_conc()
        * ch4_n2o_unit_adj()
        * (
            ch4_reference_conc()
            * n2o_atm_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_2()
    )


def adjustment_for_ch4ref_and_n2oref():
    """
    Real Name: Adjustment for CH4ref and N2Oref
    Original Eqn: CH4 N2O interaction coef 1 * LN( 1 +CH4 N2O interaction coef 2 *(CH4 reference conc*N2O reference conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 1 +CH4 N2O interaction coef 3 *CH4 reference conc*CH4 N2O unit adj *(CH4 reference conc*N2O reference conc *CH4 N2O unit adj*CH4 N2O unit adj)^CH4 N2O interaction exp 2)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1
        Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.        Adjusts total RF from CH4 and N2O to be less than the sum of RF from each
        individually to account for interactions between both gases.
    """
    return ch4_n2o_interaction_coef_1() * np.log(
        1
        + ch4_n2o_interaction_coef_2()
        * (
            ch4_reference_conc()
            * n2o_reference_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_1()
        + ch4_n2o_interaction_coef_3()
        * ch4_reference_conc()
        * ch4_n2o_unit_adj()
        * (
            ch4_reference_conc()
            * n2o_reference_conc()
            * ch4_n2o_unit_adj()
            * ch4_n2o_unit_adj()
        )
        ** ch4_n2o_interaction_exp_2()
    )


def ch4_and_n2o_radiative_forcing():
    """
    Real Name: CH4 and N2O Radiative Forcing
    Original Eqn: CH4 Radiative Forcing + N2O Radiative Forcing
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1
        Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.        Adjusts total RF from CH4 and N2O to be less than the sum of RF from each
        individually to account for interactions between both gases.
    """
    return ch4_radiative_forcing() + n2o_radiative_forcing()


def ch4_n2o_interaction_coef_1():
    """
    Real Name: CH4 N2O interaction coef 1
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_interaction_coef_1')
    Units: W/m2
    Limits: (None, None)
    Type: constant
    Subs: None

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and
        Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF
        formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_1()


def ch4_n2o_interaction_coef_2():
    """
    Real Name: CH4 N2O interaction coef 2
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_interaction_coef_2')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and
        Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF
        formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_2()


def ch4_n2o_interaction_coef_3():
    """
    Real Name: CH4 N2O interaction coef 3
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_interaction_coef_3')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and
        Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF
        formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_3()


def ch4_n2o_interaction_exp_1():
    """
    Real Name: CH4 N2O interaction exp 1
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_interaction_exp_1')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    First exponent of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and
        Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF
        formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_exp_1()


def ch4_n2o_interaction_exp_2():
    """
    Real Name: CH4 N2O interaction exp 2
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_interaction_exp_2')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Second exponent of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic
        and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3:
        RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_exp_2()


def ch4_n2o_unit_adj():
    """
    Real Name: CH4 N2O unit adj
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_N2O_unit_adj')
    Units: 1/ppb
    Limits: (None, None)
    Type: constant
    Subs: None

    Normalizes units to avoid dimensioned variable in exponent
    """
    return _ext_constant_ch4_n2o_unit_adj()


def ch4_radiative_efficiency_coef():
    """
    Real Name: CH4 radiative efficiency coef
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_radiative_efficiency_coef')
    Units: W/m2
    Limits: (None, None)
    Type: constant
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table
        8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_radiative_efficiency_coef()


def ch4_radiative_forcing():
    """
    Real Name: CH4 Radiative Forcing
    Original Eqn: CH4 radiative efficiency coef*(SQRT(CH4 atm conc*CH4 N2O unit adj) -SQRT(CH4 reference conc*CH4 N2O unit adj)) -(Adjustment for CH4 and N2Oref-Adjustment for CH4ref and N2Oref)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table
        8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return ch4_radiative_efficiency_coef() * (
        np.sqrt(ch4_atm_conc() * ch4_n2o_unit_adj())
        - np.sqrt(ch4_reference_conc() * ch4_n2o_unit_adj())
    ) - (adjustment_for_ch4_and_n2oref() - adjustment_for_ch4ref_and_n2oref())


def ch4_reference_conc():
    """
    Real Name: CH4 reference conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'CH4_reference_conc')
    Units: ppb
    Limits: (None, None)
    Type: constant
    Subs: None

    WG1AR5_Chapter08_FINAL.pdf.
        https://www.ipcc.ch/pdf/assessment-report/ar5/wg1/WG1AR5_Chapter08_FINAL.pd
        f        722 ± 25 ppb
    """
    return _ext_constant_ch4_reference_conc()


def co2_radiative_forcing():
    """
    Real Name: CO2 radiative forcing
    Original Eqn: reference CO2 radiative forcing*LN(C in Atmosphere/preindustrial C)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Radiative forcing from accumulation of CO2.
    """
    return reference_co2_radiative_forcing() * np.log(
        c_in_atmosphere() / preindustrial_c()
    )


def effective_radiative_forcing():
    """
    Real Name: Effective Radiative Forcing
    Original Eqn: SAMPLE IF TRUE( Time<=time to commit RF,Total Radiative Forcing,Total Radiative Forcing)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Total Radiative Forcing from All GHGs
    """
    return _sample_if_true_effective_radiative_forcing()


def halocarbon_rf():
    """
    Real Name: Halocarbon RF
    Original Eqn: RF from F gases+MP RF total
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    RF from PFCs, SF6, HFCs, and MP gases.
    """
    return rf_from_f_gases() + mp_rf_total()


def hfc_rf_total():
    """
    Real Name: HFC RF total
    Original Eqn: SUM(HFC RF[HFC type!])
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    The sum of the RFs of the individual HFC types.
    """
    return sum(hfc_rf(), dim=("HFC type",))


def last_historical_rf_year():
    """
    Real Name: last historical RF year
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'last_historical_RF_year')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    2010
    """
    return _ext_constant_last_historical_rf_year()


def mineral_aerosols_and_land_rf():
    """
    Real Name: mineral aerosols and land RF
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'mineral_aerosols_and_land_RF')
    Units: W/m2
    Limits: (-1.0, 1.0, 0.01)
    Type: constant
    Subs: None

    Qaermn (minerals), Qland.  Updated to reflect AR5. (-0.3)
    """
    return _ext_constant_mineral_aerosols_and_land_rf()


def mp_rf_total():
    """
    Real Name: MP RF total
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'MP_RF_total_time', 'MP_RF_total')
    Units: W/m2
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Radiative forcing due to Montreal Protocol gases, based on the concentration of each
        gas multiplied by its radiative forcing coefficient.        CROADS. JS Daniel, GJM Velders et al. (2007) Scientific Assessment of
        Ozone Depletion: 2006.  Chapter 8.  Halocarbon Scenarios, Ozone Depletion
        Potentials, and Global Warming Potentials. Table 8-5. Mixing ratios (ppt)
        of the ODSs considered in scenario A1.
    """
    return _ext_data_mp_rf_total(time())


def n2o_radiative_efficiency_coeff():
    """
    Real Name: N2O radiative efficiency coeff
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'N2O_radiative_efficiency_coeff')
    Units: W/m2
    Limits: (None, None)
    Type: constant
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table
        8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_n2o_radiative_efficiency_coeff()


def n2o_radiative_forcing():
    """
    Real Name: N2O Radiative Forcing
    Original Eqn: N2O radiative efficiency coeff*(SQRT(N2O atm conc*CH4 N2O unit adj) -SQRT(N2O reference conc*CH4 N2O unit adj)) -(Adjustment for CH4ref and N2O-Adjustment for CH4ref and N2Oref)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table
        8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return n2o_radiative_efficiency_coeff() * (
        np.sqrt(n2o_atm_conc() * ch4_n2o_unit_adj())
        - np.sqrt(n2o_reference_conc() * ch4_n2o_unit_adj())
    ) - (adjustment_for_ch4ref_and_n2o() - adjustment_for_ch4ref_and_n2oref())


def n2o_reference_conc():
    """
    Real Name: N2O reference conc
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'N2O_reference_conc')
    Units: ppb
    Limits: (None, None)
    Type: constant
    Subs: None

    WG1AR5_Chapter08_FINAL.pdf.
        https://www.ipcc.ch/pdf/assessment-report/ar5/wg1/WG1AR5_Chapter08_FINAL.pd
        f
    """
    return _ext_constant_n2o_reference_conc()


def other_forcings():
    """
    Real Name: other forcings
    Original Eqn: IF THEN ELSE(Time<=last historical RF year, other forcings history, other forcings RCP)
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Forcings for all components except well-mixed GHGs.        Switch over from historical data to projections in 1995 (GISS) and bridge
        to RCPs starting in 2010.
    """
    return if_then_else(
        time() <= last_historical_rf_year(),
        lambda: other_forcings_history(),
        lambda: other_forcings_rcp(),
    )


def other_forcings_history():
    """
    Real Name: other forcings history
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'other_forcings_history_time', 'other_forcings_history')
    Units: W/m2
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    GISS other forcings 1850-2010.
    """
    return _ext_data_other_forcings_history(time())


def other_forcings_rcp():
    """
    Real Name: other forcings RCP
    Original Eqn: IF THEN ELSE(Choose RCP=1, other forcings RCP Scenario[RCP26], IF THEN ELSE(Choose RCP=2, other forcings RCP Scenario[RCP45], IF THEN ELSE(Choose RCP=3, other forcings RCP Scenario[RCP60], other forcings RCP Scenario[RCP85])))
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Projections "Representative Concentration Pathways" (RCPs)        Choose RCP:        1. RCP 2.6        2. RCP 4.5        3. RCP 6.0        4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(other_forcings_rcp_scenario().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(other_forcings_rcp_scenario().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(other_forcings_rcp_scenario().loc["RCP60"]),
                lambda: float(other_forcings_rcp_scenario().loc["RCP85"]),
            ),
        ),
    )


@subs(["RCP Scenario"], _subscript_dict)
def other_forcings_rcp_scenario():
    """
    Real Name: other forcings RCP Scenario
    Original Eqn: GET DIRECT DATA('../climate.xlsx', 'World', 'other_forcings_RCP_time', 'other_forcings_RCP')
    Units: W/m2
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['RCP Scenario']

    RCPs starting in 2010.
    """
    return _ext_data_other_forcings_rcp_scenario(time())


def other_ghg_rad_forcing_non_co2():
    """
    Real Name: "Other GHG Rad Forcing (non CO2)"
    Original Eqn: Total Radiative Forcing-CO2 radiative forcing
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_radiative_forcing() - co2_radiative_forcing()


def rf_from_f_gases():
    """
    Real Name: RF from F gases
    Original Eqn: PFC RF+SF6 RF+HFC RF total
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None

    Radiative forcing due to fluorinated gases, based on the concentration of
        each gas multiplied by its radiative forcing coefficient.  The RF of HFCs
        is the sum of the RFs of the individual HFC types:
    """
    return pfc_rf() + sf6_rf() + hfc_rf_total()


def time_to_commit_rf():
    """
    Real Name: time to commit RF
    Original Eqn: GET DIRECT CONSTANTS('../climate.xlsx', 'World', 'time_to_commit_RF')
    Units: year
    Limits: (1900.0, 2200.0)
    Type: constant
    Subs: None

    Time after which forcing is frozen for a test of committed warming.
    """
    return _ext_constant_time_to_commit_rf()


def total_radiative_forcing():
    """
    Real Name: Total Radiative Forcing
    Original Eqn: "Well-Mixed GHG Forcing"+Adjusted other forcings
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return wellmixed_ghg_forcing() + adjusted_other_forcings()


def wellmixed_ghg_forcing():
    """
    Real Name: "Well-Mixed GHG Forcing"
    Original Eqn: CO2 radiative forcing+CH4 and N2O Radiative Forcing+Halocarbon RF
    Units: W/m2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return co2_radiative_forcing() + ch4_and_n2o_radiative_forcing() + halocarbon_rf()


_ext_constant_ch4_n2o_interaction_coef_1 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_1",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_1",
)


_ext_constant_ch4_n2o_interaction_coef_2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_2",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_2",
)


_ext_constant_ch4_n2o_interaction_coef_3 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_3",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_3",
)


_ext_constant_ch4_n2o_interaction_exp_1 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_exp_1",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_exp_1",
)


_ext_constant_ch4_n2o_interaction_exp_2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_exp_2",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_exp_2",
)


_ext_constant_ch4_n2o_unit_adj = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_unit_adj",
    {},
    _root,
    "_ext_constant_ch4_n2o_unit_adj",
)


_ext_constant_ch4_radiative_efficiency_coef = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_radiative_efficiency_coef",
    {},
    _root,
    "_ext_constant_ch4_radiative_efficiency_coef",
)


_ext_constant_ch4_reference_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_reference_conc",
    {},
    _root,
    "_ext_constant_ch4_reference_conc",
)


_sample_if_true_effective_radiative_forcing = SampleIfTrue(
    lambda: time() <= time_to_commit_rf(),
    lambda: total_radiative_forcing(),
    lambda: total_radiative_forcing(),
    "_sample_if_true_effective_radiative_forcing",
)


_ext_constant_last_historical_rf_year = ExtConstant(
    "../climate.xlsx",
    "World",
    "last_historical_RF_year",
    {},
    _root,
    "_ext_constant_last_historical_rf_year",
)


_ext_constant_mineral_aerosols_and_land_rf = ExtConstant(
    "../climate.xlsx",
    "World",
    "mineral_aerosols_and_land_RF",
    {},
    _root,
    "_ext_constant_mineral_aerosols_and_land_rf",
)


_ext_data_mp_rf_total = ExtData(
    "../climate.xlsx",
    "World",
    "MP_RF_total_time",
    "MP_RF_total",
    "interpolate",
    {},
    _root,
    "_ext_data_mp_rf_total",
)


_ext_constant_n2o_radiative_efficiency_coeff = ExtConstant(
    "../climate.xlsx",
    "World",
    "N2O_radiative_efficiency_coeff",
    {},
    _root,
    "_ext_constant_n2o_radiative_efficiency_coeff",
)


_ext_constant_n2o_reference_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "N2O_reference_conc",
    {},
    _root,
    "_ext_constant_n2o_reference_conc",
)


_ext_data_other_forcings_history = ExtData(
    "../climate.xlsx",
    "World",
    "other_forcings_history_time",
    "other_forcings_history",
    "interpolate",
    {},
    _root,
    "_ext_data_other_forcings_history",
)


_ext_data_other_forcings_rcp_scenario = ExtData(
    "../climate.xlsx",
    "World",
    "other_forcings_RCP_time",
    "other_forcings_RCP",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    "_ext_data_other_forcings_rcp_scenario",
)


_ext_constant_time_to_commit_rf = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_to_commit_RF",
    {},
    _root,
    "_ext_constant_time_to_commit_rf",
)
