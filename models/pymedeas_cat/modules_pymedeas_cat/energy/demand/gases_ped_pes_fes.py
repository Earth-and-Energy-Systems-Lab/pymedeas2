"""
Module gases_ped_pes_fes
Translated using PySD version 2.2.0
"""


def abundance_gases():
    """
    Real Name: abundance gases
    Original Eqn: IF THEN ELSE(PED gases<(PES gases), 1, 1-ZIDZ( PED gases -PES gases, PED gases ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        ped_gases() < (pes_gases()),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


def adapt_max_share_imports_nat_gas():
    """
    Real Name: adapt max share imports nat gas
    Original Eqn: IF THEN ELSE(Time<2016,"Historic share net imports nat. gas until 2016",IF THEN ELSE(Time<2021,"Historic share net imports nat. gas until 2016"+(max share imports nat gas-"Historic share net imports nat. gas until 2016")*((Time-2016)/(2021-2016)),max share imports nat gas))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2016,
        lambda: historic_share_net_imports_nat_gas_until_2016(),
        lambda: if_then_else(
            time() < 2021,
            lambda: historic_share_net_imports_nat_gas_until_2016()
            + (
                max_share_imports_nat_gas()
                - historic_share_net_imports_nat_gas_until_2016()
            )
            * ((time() - 2016) / (2021 - 2016)),
            lambda: max_share_imports_nat_gas(),
        ),
    )


def check_gases():
    """
    Real Name: check gases
    Original Eqn: ZIDZ( PED gases-PES gases, PES gases)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


def constrain_gas_exogenous_growth():
    """
    Real Name: "constrain gas exogenous growth?"
    Original Eqn: IF THEN ELSE(check gases>-0.01,1,check gases)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If negative, there is oversupply of gas. This variable is used to
        constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


def fes_total_biogas():
    """
    Real Name: FES total biogas
    Original Eqn: Share biogas in PES*real FE consumption gases EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return share_biogas_in_pes() * real_fe_consumption_gases_ej()


def historic_conv_nat_gas_domestic_aut_extracted_ej():
    """
    Real Name: "Historic conv nat. gas domestic AUT extracted EJ"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_domestic_natural_gas_extraction')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None


    """
    return _ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej(time())


def historic_net_imports_nat_gas_aut():
    """
    Real Name: "Historic net imports nat. gas AUT"
    Original Eqn: "PED nat. gas EJ"-"Historic conv nat. gas domestic AUT extracted EJ"-"Historic unconv nat. gas domestic AUT extracted EJ"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_nat_gas_ej()
        - historic_conv_nat_gas_domestic_aut_extracted_ej()
        - historic_unconv_nat_gas_domestic_aut_extracted_ej()
    )


def historic_share_conv_nat_gas_domestic_aut_extraction():
    """
    Real Name: "Historic share conv. nat gas domestic AUT extraction"
    Original Eqn: ZIDZ("Historic conv nat. gas domestic AUT extracted EJ","PED nat. gas EJ")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(historic_conv_nat_gas_domestic_aut_extracted_ej(), ped_nat_gas_ej())


def historic_share_conv_nat_gas_domestic_aut_extraction_until_2016():
    """
    Real Name: "Historic share conv. nat gas domestic AUT extraction\" until 2016"
    Original Eqn: SAMPLE IF TRUE(Time<2016, "Historic share conv. nat gas domestic AUT extraction", "Historic share conv. nat gas domestic AUT extraction")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        _sample_if_true_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
    )


def historic_share_net_imports_nat_gas_until_2016():
    """
    Real Name: "Historic share net imports nat. gas until 2016"
    Original Eqn: SAMPLE IF TRUE(Time<2016, ZIDZ("Historic net imports nat. gas AUT", "extraction nat. gas EJ World"), ZIDZ("Historic net imports nat. gas AUT", "extraction nat. gas EJ World"))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _sample_if_true_historic_share_net_imports_nat_gas_until_2016()


def historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016():
    """
    Real Name: "Historic share unconv. nat. gas domestric AUT extraction until 2016"
    Original Eqn: SAMPLE IF TRUE(Time<2016, "Historic share unconv. nat. gas domestric AUT extraction", "Historic share unconv. nat. gas domestric AUT extraction")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        _sample_if_true_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016()
    )


def historic_share_unconv_nat_gas_domestric_aut_extraction():
    """
    Real Name: "Historic share unconv. nat. gas domestric AUT extraction"
    Original Eqn: ZIDZ("Historic unconv nat. gas domestic AUT extracted EJ","PED nat. gas EJ" )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(historic_unconv_nat_gas_domestic_aut_extracted_ej(), ped_nat_gas_ej())


def historic_unconv_nat_gas_domestic_aut_extracted_ej():
    """
    Real Name: "Historic unconv nat. gas domestic AUT extracted EJ"
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_domestic_unconventional_natural_gas_extraction')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None


    """
    return _ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej(time())


def imports_aut_conv_gas_from_row_ej():
    """
    Real Name: imports AUT conv gas from RoW EJ
    Original Eqn: "imports AUT nat. gas from RoW EJ"*share conv vs total gas extraction World
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        imports_aut_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()
    )


def imports_aut_nat_gas_from_row_ej():
    """
    Real Name: "imports AUT nat. gas from RoW EJ"
    Original Eqn: IF THEN ELSE(Time<2016, "PED AUT nat. gas from RoW", IF THEN ELSE(limit nat gas imports from RoW=1, "PED AUT nat. gas from RoW", IF THEN ELSE (limit nat gas imports from RoW=2, MIN("PED AUT nat. gas from RoW","Historic share net imports nat. gas until 2016" *"extraction nat. gas EJ World"), IF THEN ELSE(limit nat gas imports from RoW=3, MIN("PED AUT nat. gas from RoW",adapt max share imports nat gas*"extraction nat. gas EJ World"), "PED AUT nat. gas from RoW"))))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2016,
        lambda: ped_aut_nat_gas_from_row(),
        lambda: if_then_else(
            limit_nat_gas_imports_from_row() == 1,
            lambda: ped_aut_nat_gas_from_row(),
            lambda: if_then_else(
                limit_nat_gas_imports_from_row() == 2,
                lambda: np.minimum(
                    ped_aut_nat_gas_from_row(),
                    historic_share_net_imports_nat_gas_until_2016()
                    * extraction_nat_gas_ej_world(),
                ),
                lambda: if_then_else(
                    limit_nat_gas_imports_from_row() == 3,
                    lambda: np.minimum(
                        ped_aut_nat_gas_from_row(),
                        adapt_max_share_imports_nat_gas()
                        * extraction_nat_gas_ej_world(),
                    ),
                    lambda: ped_aut_nat_gas_from_row(),
                ),
            ),
        ),
    )


def imports_aut_unconv_gas_from_row_ej():
    """
    Real Name: imports AUT unconv gas from RoW EJ
    Original Eqn: "imports AUT nat. gas from RoW EJ"*(1-share conv vs total gas extraction World)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return imports_aut_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


def limit_nat_gas_imports_from_row():
    """
    Real Name: limit nat gas imports from RoW
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'limit_nat_gas_imports_from_RoW')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1: Unlimited coal imports share from RoW (constrained by total global production)        2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global
        production)        3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_nat_gas_imports_from_row()


def max_share_imports_nat_gas():
    """
    Real Name: max share imports nat gas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'max_share_imports_nat_gas')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_max_share_imports_nat_gas()


def other_gases_required():
    """
    Real Name: Other gases required
    Original Eqn: +Transformation FF losses EJ[gases]+Energy distr losses FF EJ[gases]+"Non-energy use demand by final fuel EJ"[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
    )


def pec_nat_gas():
    """
    Real Name: "PEC nat. gas"
    Original Eqn: "PES nat. gas AUT"+"imports AUT nat. gas from RoW EJ"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej()


def ped_aut_nat_gas_from_row():
    """
    Real Name: "PED AUT nat. gas from RoW"
    Original Eqn: MAX(0, "PED nat. gas EJ"-"PES nat. gas AUT")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_aut_1())


def ped_domestic_aut_conv_nat_gas_ej():
    """
    Real Name: "PED domestic AUT conv. nat. gas EJ"
    Original Eqn: "PED nat. gas EJ"*"Historic share conv. nat gas domestic AUT extraction\" until 2016"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_nat_gas_ej()
        * historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
    )


def ped_domestic_aut_total_natgas_ej():
    """
    Real Name: "PED domestic AUT total nat.gas EJ"
    Original Eqn: "PED nat. gas EJ"*("Historic share conv. nat gas domestic AUT extraction\" until 2016"+"Historic share unconv. nat. gas domestric AUT extraction until 2016" )
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ped_nat_gas_ej() * (
        historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
        + historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016()
    )


def ped_gases():
    """
    Real Name: PED gases
    Original Eqn: MAX(0, Required FED by gas+"PED nat. gas for GTL EJ"+PE demand gas Elec plants EJ+PED gases for Heat plants EJ +PED gas for CHP plants EJ+"PED gas Heat-nc"+Other gases required)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand total gases.
    """
    return np.maximum(
        0,
        required_fed_by_gas()
        + ped_nat_gas_for_gtl_ej()
        + pe_demand_gas_elec_plants_ej()
        + ped_gases_for_heat_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + other_gases_required(),
    )


def ped_nat_gas_ej():
    """
    Real Name: "PED nat. gas EJ"
    Original Eqn: MAX(0, PED gases-PES biogas for TFC)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


def pes_gases():
    """
    Real Name: PES gases
    Original Eqn: "PEC nat. gas"+PES biogas for TFC
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply gas.
    """
    return pec_nat_gas() + pes_biogas_for_tfc()


def real_fe_consumption_gases_ej():
    """
    Real Name: real FE consumption gases EJ
    Original Eqn: (PES gases-"PED nat. gas for GTL EJ"-Other gases required )*share gases for final energy
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Real final energy consumption by gases after accounting for energy
        availability.
    """
    return (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()


def required_fed_by_gas():
    """
    Real Name: Required FED by gas
    Original Eqn: Required FED by fuel[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


def share_biogas_in_pes():
    """
    Real Name: Share biogas in PES
    Original Eqn: ZIDZ (PES biogas for TFC, PES gases)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(pes_biogas_for_tfc(), pes_gases())


def share_gases_dem_for_heatnc():
    """
    Real Name: "share gases dem for Heat-nc"
    Original Eqn: ZIDZ("PED gas Heat-nc", (PES gases-"PED nat. gas for GTL EJ" ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand for non-commercial Heat plants in relation to
        the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), (pes_gases() - ped_nat_gas_for_gtl_ej()))


def share_gases_for_final_energy():
    """
    Real Name: share gases for final energy
    Original Eqn: ZIDZ( Required FED by gas, (PED gases-"PED nat. gas for GTL EJ"-Other gases required) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gas(),
        (ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()),
    )


def share_imports_aut_nat_gas_from_row_vs_extraction_world():
    """
    Real Name: "share imports AUT nat. gas from RoW vs extraction World"
    Original Eqn: ZIDZ("imports AUT nat. gas from RoW EJ", "extraction nat. gas EJ World" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of EU natural gas imports vs global natural gas extraction.
    """
    return zidz(imports_aut_nat_gas_from_row_ej(), extraction_nat_gas_ej_world())


def share_nat_gas_dem_for_elec():
    """
    Real Name: "share nat. gas dem for Elec"
    Original Eqn: IF THEN ELSE("PED nat. gas EJ">0, PE demand gas Elec plants EJ/"PED nat. gas EJ", 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: pe_demand_gas_elec_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


def share_nat_gas_dem_for_heatcom():
    """
    Real Name: "share nat. gas dem for Heat-com"
    Original Eqn: IF THEN ELSE("PED nat. gas EJ">0, PED gases for Heat plants EJ/"PED nat. gas EJ", 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of natural gas demand for commercial Heat plants in relation to the
        demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


def year_scarcity_gases():
    """
    Real Name: Year scarcity gases
    Original Eqn: IF THEN ELSE(abundance gases>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())


_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej",
)


_sample_if_true_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_conv_nat_gas_domestic_aut_extraction(),
    lambda: historic_share_conv_nat_gas_domestic_aut_extraction(),
    "_sample_if_true_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016",
)


_sample_if_true_historic_share_net_imports_nat_gas_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_nat_gas_aut(), extraction_nat_gas_ej_world()),
    lambda: zidz(historic_net_imports_nat_gas_aut(), extraction_nat_gas_ej_world()),
    "_sample_if_true_historic_share_net_imports_nat_gas_until_2016",
)


_sample_if_true_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_unconv_nat_gas_domestric_aut_extraction(),
    lambda: historic_share_unconv_nat_gas_domestric_aut_extraction(),
    "_sample_if_true_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016",
)


_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej",
)


_ext_constant_limit_nat_gas_imports_from_row = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "limit_nat_gas_imports_from_RoW",
    {},
    _root,
    "_ext_constant_limit_nat_gas_imports_from_row",
)


_ext_constant_max_share_imports_nat_gas = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "max_share_imports_nat_gas",
    {},
    _root,
    "_ext_constant_max_share_imports_nat_gas",
)
