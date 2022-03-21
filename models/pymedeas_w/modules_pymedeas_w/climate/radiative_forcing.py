"""
Module radiative_forcing
Translated using PySD version 2.2.3
"""


def adjusted_other_forcings():
    """
    Real Name: Adjusted other forcings
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    RCP does not include solar and albedo in their other forcings; the adjusted values add the values for these from MAGICC. It is the adjusted other forcings that are included in the total radiative forcing. +IF THEN ELSE(Time>=last historical RF year, mineral aerosols and land RF, 0)
    """
    return other_forcings() + if_then_else(
        time() > last_historical_rf_year(),
        lambda: mineral_aerosols_and_land_rf(),
        lambda: 0,
    )


def adjustment_for_ch4_and_n2oref():
    """
    Real Name: Adjustment for CH4 and N2Oref
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O. Adjusts total RF from CH4 and N2O to be less than the sum of RF from each individually to account for interactions between both gases.
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
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O. Adjusts total RF from CH4 and N2O to be less than the sum of RF from each individually to account for interactions between both gases.
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
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O. Adjusts total RF from CH4 and N2O to be less than the sum of RF from each individually to account for interactions between both gases.
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
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O. Adjusts total RF from CH4 and N2O to be less than the sum of RF from each individually to account for interactions between both gases.
    """
    return ch4_radiative_forcing() + n2o_radiative_forcing()


def ch4_n2o_interaction_coef_1():
    """
    Real Name: CH4 N2O interaction coef 1
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_1()


_ext_constant_ch4_n2o_interaction_coef_1 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_1",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_1",
)


def ch4_n2o_interaction_coef_2():
    """
    Real Name: CH4 N2O interaction coef 2
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_2()


_ext_constant_ch4_n2o_interaction_coef_2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_2",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_2",
)


def ch4_n2o_interaction_coef_3():
    """
    Real Name: CH4 N2O interaction coef 3
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Coefficient of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_coef_3()


_ext_constant_ch4_n2o_interaction_coef_3 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_coef_3",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_coef_3",
)


def ch4_n2o_interaction_exp_1():
    """
    Real Name: CH4 N2O interaction exp 1
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    First exponent of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_exp_1()


_ext_constant_ch4_n2o_interaction_exp_1 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_exp_1",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_exp_1",
)


def ch4_n2o_interaction_exp_2():
    """
    Real Name: CH4 N2O interaction exp 2
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Second exponent of CH4 N2O interaction. AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_n2o_interaction_exp_2()


_ext_constant_ch4_n2o_interaction_exp_2 = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_interaction_exp_2",
    {},
    _root,
    "_ext_constant_ch4_n2o_interaction_exp_2",
)


def ch4_n2o_unit_adj():
    """
    Real Name: CH4 N2O unit adj
    Original Eqn:
    Units: 1/ppb
    Limits: (None, None)
    Type: Constant
    Subs: []

    Normalizes units to avoid dimensioned variable in exponent
    """
    return _ext_constant_ch4_n2o_unit_adj()


_ext_constant_ch4_n2o_unit_adj = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_N2O_unit_adj",
    {},
    _root,
    "_ext_constant_ch4_n2o_unit_adj",
)


def ch4_radiative_efficiency_coef():
    """
    Real Name: CH4 radiative efficiency coef
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_ch4_radiative_efficiency_coef()


_ext_constant_ch4_radiative_efficiency_coef = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_radiative_efficiency_coef",
    {},
    _root,
    "_ext_constant_ch4_radiative_efficiency_coef",
)


def ch4_radiative_forcing():
    """
    Real Name: CH4 Radiative Forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return ch4_radiative_efficiency_coef() * (
        np.sqrt(ch4_atm_conc() * ch4_n2o_unit_adj())
        - np.sqrt(ch4_reference_conc() * ch4_n2o_unit_adj())
    ) - (adjustment_for_ch4_and_n2oref() - adjustment_for_ch4ref_and_n2oref())


def ch4_reference_conc():
    """
    Real Name: CH4 reference conc
    Original Eqn:
    Units: ppb
    Limits: (None, None)
    Type: Constant
    Subs: []

    WG1AR5_Chapter08_FINAL.pdf. https://www.ipcc.ch/pdf/assessment-report/ar5/wg1/WG1AR5_Chapter08_FINAL.pd f 722 ± 25 ppb
    """
    return _ext_constant_ch4_reference_conc()


_ext_constant_ch4_reference_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "CH4_reference_conc",
    {},
    _root,
    "_ext_constant_ch4_reference_conc",
)


def co2_radiative_forcing():
    """
    Real Name: CO2 radiative forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Radiative forcing from accumulation of CO2.
    """
    return reference_co2_radiative_forcing() * np.log(
        c_in_atmosphere() / preindustrial_c()
    )


def effective_radiative_forcing():
    """
    Real Name: Effective Radiative Forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total Radiative Forcing from All GHGs
    """
    return _sampleiftrue_effective_radiative_forcing()


_sampleiftrue_effective_radiative_forcing = SampleIfTrue(
    lambda: time() <= time_to_commit_rf(),
    lambda: total_radiative_forcing(),
    lambda: total_radiative_forcing(),
    "_sampleiftrue_effective_radiative_forcing",
)


def halocarbon_rf():
    """
    Real Name: Halocarbon RF
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    RF from PFCs, SF6, HFCs, and MP gases.
    """
    return rf_from_f_gases() + mp_rf_total()


def hfc_rf_total():
    """
    Real Name: HFC RF total
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The sum of the RFs of the individual HFC types.
    """
    return sum(hfc_rf().rename({"HFC type": "HFC type!"}), dim=["HFC type!"])


def last_historical_rf_year():
    """
    Real Name: last historical RF year
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    2010
    """
    return _ext_constant_last_historical_rf_year()


_ext_constant_last_historical_rf_year = ExtConstant(
    "../climate.xlsx",
    "World",
    "last_historical_RF_year",
    {},
    _root,
    "_ext_constant_last_historical_rf_year",
)


def mineral_aerosols_and_land_rf():
    """
    Real Name: mineral aerosols and land RF
    Original Eqn:
    Units: W/m2
    Limits: (-1.0, 1.0, 0.01)
    Type: Constant
    Subs: []

    Qaermn (minerals), Qland. Updated to reflect AR5. (-0.3)
    """
    return _ext_constant_mineral_aerosols_and_land_rf()


_ext_constant_mineral_aerosols_and_land_rf = ExtConstant(
    "../climate.xlsx",
    "World",
    "mineral_aerosols_and_land_RF",
    {},
    _root,
    "_ext_constant_mineral_aerosols_and_land_rf",
)


def mp_rf_total():
    """
    Real Name: MP RF total
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Data
    Subs: []

    Radiative forcing due to Montreal Protocol gases, based on the concentration of each gas multiplied by its radiative forcing coefficient. CROADS. JS Daniel, GJM Velders et al. (2007) Scientific Assessment of Ozone Depletion: 2006. Chapter 8. Halocarbon Scenarios, Ozone Depletion Potentials, and Global Warming Potentials. Table 8-5. Mixing ratios (ppt) of the ODSs considered in scenario A1.
    """
    return _ext_data_mp_rf_total(time())


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


def n2o_radiative_efficiency_coeff():
    """
    Real Name: N2O radiative efficiency coeff
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Constant
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return _ext_constant_n2o_radiative_efficiency_coeff()


_ext_constant_n2o_radiative_efficiency_coeff = ExtConstant(
    "../climate.xlsx",
    "World",
    "N2O_radiative_efficiency_coeff",
    {},
    _root,
    "_ext_constant_n2o_radiative_efficiency_coeff",
)


def n2o_radiative_forcing():
    """
    Real Name: N2O Radiative Forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    AR5 WG1 Chapter 8 Anthropogenic and Natural Radiative Forcing. Table 8.SM.1 Supplementary for Table 8.3: RF formulae for CO2, CH4 and N2O.
    """
    return n2o_radiative_efficiency_coeff() * (
        np.sqrt(n2o_atm_conc() * ch4_n2o_unit_adj())
        - np.sqrt(n2o_reference_conc() * ch4_n2o_unit_adj())
    ) - (adjustment_for_ch4ref_and_n2o() - adjustment_for_ch4ref_and_n2oref())


def n2o_reference_conc():
    """
    Real Name: N2O reference conc
    Original Eqn:
    Units: ppb
    Limits: (None, None)
    Type: Constant
    Subs: []

    WG1AR5_Chapter08_FINAL.pdf. https://www.ipcc.ch/pdf/assessment-report/ar5/wg1/WG1AR5_Chapter08_FINAL.pd f
    """
    return _ext_constant_n2o_reference_conc()


_ext_constant_n2o_reference_conc = ExtConstant(
    "../climate.xlsx",
    "World",
    "N2O_reference_conc",
    {},
    _root,
    "_ext_constant_n2o_reference_conc",
)


def other_forcings():
    """
    Real Name: other forcings
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Forcings for all components except well-mixed GHGs. Switch over from historical data to projections in 1995 (GISS) and bridge to RCPs starting in 2010.
    """
    return if_then_else(
        time() <= last_historical_rf_year(),
        lambda: other_forcings_history(),
        lambda: other_forcings_rcp(),
    )


def other_forcings_history():
    """
    Real Name: other forcings history
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Data
    Subs: []

    GISS other forcings 1850-2010.
    """
    return _ext_data_other_forcings_history(time())


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


def other_forcings_rcp():
    """
    Real Name: other forcings RCP
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Data
    Subs: []

    Projections "Representative Concentration Pathways" (RCPs) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
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
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Data
    Subs: ['RCP Scenario']

    RCPs starting in 2010.
    """
    return _ext_data_other_forcings_rcp_scenario(time())


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


def other_ghg_rad_forcing_non_co2():
    """
    Real Name: "Other GHG Rad Forcing (non CO2)"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return total_radiative_forcing() - co2_radiative_forcing()


def rf_from_f_gases():
    """
    Real Name: RF from F gases
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Radiative forcing due to fluorinated gases, based on the concentration of each gas multiplied by its radiative forcing coefficient. The RF of HFCs is the sum of the RFs of the individual HFC types:
    """
    return pfc_rf() + sf6_rf() + hfc_rf_total()


def time_to_commit_rf():
    """
    Real Name: time to commit RF
    Original Eqn:
    Units: year
    Limits: (1900.0, 2200.0)
    Type: Constant
    Subs: []

    Time after which forcing is frozen for a test of committed warming.
    """
    return _ext_constant_time_to_commit_rf()


_ext_constant_time_to_commit_rf = ExtConstant(
    "../climate.xlsx",
    "World",
    "time_to_commit_RF",
    {},
    _root,
    "_ext_constant_time_to_commit_rf",
)


def total_radiative_forcing():
    """
    Real Name: Total Radiative Forcing
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return wellmixed_ghg_forcing() + adjusted_other_forcings()


def wellmixed_ghg_forcing():
    """
    Real Name: "Well-Mixed GHG Forcing"
    Original Eqn:
    Units: W/m2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return co2_radiative_forcing() + ch4_and_n2o_radiative_forcing() + halocarbon_rf()
