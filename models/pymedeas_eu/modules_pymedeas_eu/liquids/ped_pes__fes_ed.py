"""
Module ped_pes__fes_ed
Translated using PySD version 2.1.0
"""


def abundance_liquids():
    """
    Real Name: abundance liquids
    Original Eqn: IF THEN ELSE(PED liquids EJ<PES Liquids EJ, 1, 1- ZIDZ( PED liquids EJ -PES Liquids EJ , PED liquids EJ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        ped_liquids_ej() < pes_liquids_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids_ej() - pes_liquids_ej(), ped_liquids_ej()),
    )


def adapt_max_share_imports_oil():
    """
    Real Name: adapt max share imports oil
    Original Eqn: IF THEN ELSE(Time<2016,Historic share net imports oil until 2016,IF THEN ELSE(Time<2021,Historic share net imports oil until 2016+(max share imports oil-Historic share net imports oil until 2016)*((Time-2016)/(2021-2016)),max share imports oil))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2016,
        lambda: historic_share_net_imports_oil_until_2016(),
        lambda: if_then_else(
            time() < 2021,
            lambda: historic_share_net_imports_oil_until_2016()
            + (max_share_imports_oil() - historic_share_net_imports_oil_until_2016())
            * ((time() - 2016) / (2021 - 2016)),
            lambda: max_share_imports_oil(),
        ),
    )


def check_liquids():
    """
    Real Name: check liquids
    Original Eqn: ZIDZ( (PED liquids EJ-PES Liquids EJ), PES Liquids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0,
        demand<supply (oversupply). Variable to avoid energy oversupply caused by
        exogenously driven policies.
    """
    return zidz((ped_liquids_ej() - pes_liquids_ej()), pes_liquids_ej())


def constrain_liquids_exogenous_growth():
    """
    Real Name: "constrain liquids exogenous growth?"
    Original Eqn: IF THEN ELSE(check liquids>0,1,check liquids)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    If negative, there is oversupply of liquids. This variable is used to
        constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > 0, lambda: 1, lambda: check_liquids())


def fes_total_biofuels():
    """
    Real Name: FES total biofuels
    Original Eqn: Share biofuel in PES*real FE consumption liquids EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return share_biofuel_in_pes() * real_fe_consumption_liquids_ej()


def historic_conv_oil_domestic_eu_extracted_ej():
    """
    Real Name: Historic conv oil domestic EU extracted EJ
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_domestic_conventional_oil_extraction')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None


    """
    return _ext_data_historic_conv_oil_domestic_eu_extracted_ej(time())


def historic_net_imports_oil_eu():
    """
    Real Name: Historic net imports oil EU
    Original Eqn: PED liquids EJ-Historic conv oil domestic EU extracted EJ-Historic unconv oil domestic EU extracted EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_liquids_ej()
        - historic_conv_oil_domestic_eu_extracted_ej()
        - historic_unconv_oil_domestic_eu_extracted_ej()
    )


def historic_share_conv_oil_domestic_eu_extraction():
    """
    Real Name: "Historic share conv. oil domestic EU extraction"
    Original Eqn: ZIDZ(Historic conv oil domestic EU extracted EJ,PED liquids EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(historic_conv_oil_domestic_eu_extracted_ej(), ped_liquids_ej())


def historic_share_conv_oil_domestic_eu_extraction_until_2016():
    """
    Real Name: "Historic share conv. oil domestic EU extraction\" until 2016"
    Original Eqn: SAMPLE IF TRUE(Time<2016,"Historic share conv. oil domestic EU extraction", "Historic share conv. oil domestic EU extraction")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _sample_if_true_historic_share_conv_oil_domestic_eu_extraction_until_2016()


def historic_share_net_imports_oil_until_2016():
    """
    Real Name: Historic share net imports oil until 2016
    Original Eqn: SAMPLE IF TRUE(Time<2016, ZIDZ(Historic net imports oil EU, Extraction oil EJ World), ZIDZ(Historic net imports oil EU, Extraction oil EJ World))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _sample_if_true_historic_share_net_imports_oil_until_2016()


def historic_share_unconv_oil_domestric_eu_extraction_until_2016():
    """
    Real Name: "Historic share unconv. oil domestric EU extraction until 2016"
    Original Eqn: SAMPLE IF TRUE(Time<2016, "Historic share unconv. oil domestric EU extraction", "Historic share unconv. oil domestric EU extraction")
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        _sample_if_true_historic_share_unconv_oil_domestric_eu_extraction_until_2016()
    )


def historic_share_unconv_oil_domestric_eu_extraction():
    """
    Real Name: "Historic share unconv. oil domestric EU extraction"
    Original Eqn: ZIDZ(Historic unconv oil domestic EU extracted EJ,PED liquids EJ)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(historic_unconv_oil_domestic_eu_extracted_ej(), ped_liquids_ej())


def historic_unconv_oil_domestic_eu_extracted_ej():
    """
    Real Name: Historic unconv oil domestic EU extracted EJ
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_domestic_unconventional_oil_extraction')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None


    """
    return _ext_data_historic_unconv_oil_domestic_eu_extracted_ej(time())


def imports_eu_conv_oil_from_row_ej():
    """
    Real Name: imports EU conv oil from RoW EJ
    Original Eqn: imports EU total oil from RoW EJ*share conv vs total oil extraction World
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        imports_eu_total_oil_from_row_ej() * share_conv_vs_total_oil_extraction_world()
    )


def imports_eu_total_oil_from_row_ej():
    """
    Real Name: imports EU total oil from RoW EJ
    Original Eqn: IF THEN ELSE(Time<2016, PED EU total oil from RoW, IF THEN ELSE(limit oil imports from RoW=1, PED EU total oil from RoW, IF THEN ELSE (limit oil imports from RoW=2, MIN(PED EU total oil from RoW,Historic share net imports oil until 2016 *Extraction oil EJ World), IF THEN ELSE(limit oil imports from RoW=3, MIN(PED EU total oil from RoW,adapt max share imports oil*Extraction oil EJ World ), PED EU total oil from RoW))))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2016,
        lambda: ped_eu_total_oil_from_row(),
        lambda: if_then_else(
            limit_oil_imports_from_row() == 1,
            lambda: ped_eu_total_oil_from_row(),
            lambda: if_then_else(
                limit_oil_imports_from_row() == 2,
                lambda: np.minimum(
                    ped_eu_total_oil_from_row(),
                    historic_share_net_imports_oil_until_2016()
                    * extraction_oil_ej_world(),
                ),
                lambda: if_then_else(
                    limit_oil_imports_from_row() == 3,
                    lambda: np.minimum(
                        ped_eu_total_oil_from_row(),
                        adapt_max_share_imports_oil() * extraction_oil_ej_world(),
                    ),
                    lambda: ped_eu_total_oil_from_row(),
                ),
            ),
        ),
    )


def imports_eu_unconv_oil_from_row_ej():
    """
    Real Name: imports EU unconv oil from RoW EJ
    Original Eqn: imports EU total oil from RoW EJ*(1-share conv vs total oil extraction World)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return imports_eu_total_oil_from_row_ej() * (
        1 - share_conv_vs_total_oil_extraction_world()
    )


def limit_oil_imports_from_row():
    """
    Real Name: limit oil imports from RoW
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'limit_oil_imports_from_RoW')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1: Unlimited coal imports share from RoW (constrained by total global production)        2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global
        production)        3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_oil_imports_from_row()


def max_share_imports_oil():
    """
    Real Name: max share imports oil
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'max_share_imports_oil')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_max_share_imports_oil()


def other_liquids_required_ej():
    """
    Real Name: Other liquids required EJ
    Original Eqn: Energy distr losses FF EJ[liquids]+Transformation FF losses EJ[liquids]+"Non-energy use demand by final fuel EJ"[liquids]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(energy_distr_losses_ff_ej().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"])
    )


def other_liquids_supply_ej():
    """
    Real Name: Other liquids supply EJ
    Original Eqn: Oil refinery gains EJ+"FES CTL+GTL EJ"+FES total biofuels production EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_production_ej()
    )


def pec_total_oil():
    """
    Real Name: PEC total oil
    Original Eqn: PES total oil EJ EU+imports EU total oil from RoW EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_total_oil_ej_eu() + imports_eu_total_oil_from_row_ej()


def ped_domestic_eu_conv_oil_ej():
    """
    Real Name: "PED domestic EU conv. oil EJ"
    Original Eqn: PED total oil EJ*"Historic share conv. oil domestic EU extraction\" until 2016"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_total_oil_ej() * historic_share_conv_oil_domestic_eu_extraction_until_2016()
    )


def ped_domestic_eu_total_oil_ej():
    """
    Real Name: PED domestic EU total oil EJ
    Original Eqn: PED total oil EJ*("Historic share conv. oil domestic EU extraction\" until 2016"+"Historic share unconv. oil domestric EU extraction until 2016" )
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ped_total_oil_ej() * (
        historic_share_conv_oil_domestic_eu_extraction_until_2016()
        + historic_share_unconv_oil_domestric_eu_extraction_until_2016()
    )


def ped_eu_total_oil_from_row():
    """
    Real Name: PED EU total oil from RoW
    Original Eqn: MAX(0, PED total oil EJ-PES total oil EJ EU)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.maximum(0, ped_total_oil_ej() - pes_total_oil_ej_eu())


def ped_liquids_ej():
    """
    Real Name: PED liquids EJ
    Original Eqn: MAX(0,Required FED by liquids EJ+Other liquids required EJ+PE demand oil Elec plants EJ+PED oil for Heat plants EJ+PED oil for CHP plants EJ +"PED liquids Heat-nc")
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of total liquids.
    """
    return np.maximum(
        0,
        required_fed_by_liquids_ej()
        + other_liquids_required_ej()
        + pe_demand_oil_elec_plants_ej()
        + ped_oil_for_heat_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_liquids_heatnc(),
    )


def ped_nre_liquids():
    """
    Real Name: PED NRE Liquids
    Original Eqn: MAX(0, PED liquids EJ-FES total biofuels production EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of non-renewable energy for the production of
        liquids.
    """
    return np.maximum(0, ped_liquids_ej() - fes_total_biofuels_production_ej())


def ped_total_oil_ej():
    """
    Real Name: PED total oil EJ
    Original Eqn: MAX(0,PED NRE Liquids-"FES CTL+GTL EJ"-Oil refinery gains EJ )
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


def pes_liquids_ej():
    """
    Real Name: PES Liquids EJ
    Original Eqn: PEC total oil+Other liquids supply EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary supply of liquids.
    """
    return pec_total_oil() + other_liquids_supply_ej()


def real_fe_consumption_liquids_ej():
    """
    Real Name: real FE consumption liquids EJ
    Original Eqn: (PES Liquids EJ-Other liquids required EJ)*share liquids for final energy
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Real final energy consumption by liquids after accounting for energy
        availability.
    """
    return (
        pes_liquids_ej() - other_liquids_required_ej()
    ) * share_liquids_for_final_energy()


def required_fed_by_liquids_ej():
    """
    Real Name: Required FED by liquids EJ
    Original Eqn: Required FED by fuel[liquids]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


def share_biofuel_in_pes():
    """
    Real Name: Share biofuel in PES
    Original Eqn: ZIDZ (FES total biofuels production EJ, PES Liquids EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(fes_total_biofuels_production_ej(), pes_liquids_ej())


def share_imports_eu_tot_oil_from_row_vs_extraction_world():
    """
    Real Name: share imports EU tot oil from RoW vs extraction World
    Original Eqn: ZIDZ(imports EU total oil from RoW EJ, Extraction oil EJ World )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of EU total oil imports vs global oil extraction.
    """
    return zidz(imports_eu_total_oil_from_row_ej(), extraction_oil_ej_world())


def share_liquids_dem_for_heatnc():
    """
    Real Name: "share liquids dem for Heat-nc"
    Original Eqn: ZIDZ("PED liquids Heat-nc", PES Liquids EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of liquids demand for non-commercial Heat plants in relation to the
        total demand of liquids.
    """
    return zidz(ped_liquids_heatnc(), pes_liquids_ej())


def share_liquids_for_final_energy():
    """
    Real Name: share liquids for final energy
    Original Eqn: ZIDZ( Required FED by liquids EJ, (PED liquids EJ-Other liquids required EJ) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of final energy vs primary energy for liquids.
    """
    return zidz(
        required_fed_by_liquids_ej(), (ped_liquids_ej() - other_liquids_required_ej())
    )


def share_oil_dem_for_elec():
    """
    Real Name: share oil dem for Elec
    Original Eqn: IF THEN ELSE(PED total oil EJ>0, PE demand oil Elec plants EJ/PED total oil EJ, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of oil demand to cover electricity consumption.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: pe_demand_oil_elec_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


def share_oil_dem_for_heatcom():
    """
    Real Name: "share oil dem for Heat-com"
    Original Eqn: IF THEN ELSE(PED total oil EJ>0, PED oil for Heat plants EJ/PED total oil EJ,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of oil demand for commercial Heat plants in relation to the total
        demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_for_heat_plants_ej() / ped_total_oil_ej(),
        lambda: 0,
    )


def total_demand_liquids_mbd():
    """
    Real Name: "Total demand liquids mb/d"
    Original Eqn: PED liquids EJ*"Mb/d per EJ/year"
    Units: Mb/d
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand of liquids.
    """
    return ped_liquids_ej() * mbd_per_ejyear()


def year_scarcity_liquids():
    """
    Real Name: Year scarcity liquids
    Original Eqn: IF THEN ELSE(abundance liquids>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())


_ext_data_historic_conv_oil_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_conventional_oil_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_conv_oil_domestic_eu_extracted_ej",
)


_sample_if_true_historic_share_conv_oil_domestic_eu_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_oil_domestic_eu_extraction(),
        lambda: historic_share_conv_oil_domestic_eu_extraction(),
        "_sample_if_true_historic_share_conv_oil_domestic_eu_extraction_until_2016",
    )
)


_sample_if_true_historic_share_net_imports_oil_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_oil_eu(), extraction_oil_ej_world()),
    lambda: zidz(historic_net_imports_oil_eu(), extraction_oil_ej_world()),
    "_sample_if_true_historic_share_net_imports_oil_until_2016",
)


_sample_if_true_historic_share_unconv_oil_domestric_eu_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_unconv_oil_domestric_eu_extraction(),
        lambda: historic_share_unconv_oil_domestric_eu_extraction(),
        "_sample_if_true_historic_share_unconv_oil_domestric_eu_extraction_until_2016",
    )
)


_ext_data_historic_unconv_oil_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_unconv_oil_domestic_eu_extracted_ej",
)


_ext_constant_limit_oil_imports_from_row = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "limit_oil_imports_from_RoW",
    {},
    _root,
    "_ext_constant_limit_oil_imports_from_row",
)


_ext_constant_max_share_imports_oil = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "max_share_imports_oil",
    {},
    _root,
    "_ext_constant_max_share_imports_oil",
)
