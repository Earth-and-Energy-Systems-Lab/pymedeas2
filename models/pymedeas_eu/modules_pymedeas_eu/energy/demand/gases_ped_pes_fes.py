"""
Module gases_ped_pes_fes
Translated using PySD version 2.2.1
"""


def abundance_gases():
    """
    Real Name: abundance gases
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_gases() < pes_gases(),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


def adapt_max_share_imports_nat_gas():
    """
    Real Name: adapt max share imports nat gas
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


def constrain_gas_exogenous_growth():
    """
    Real Name: "constrain gas exogenous growth?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If negative, there is oversupply of gas. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


def fes_total_biogas():
    """
    Real Name: FES total biogas
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return share_biogas_in_pes() * real_fe_consumption_gases_ej()


def historic_conv_nat_gas_domestic_eu_extracted_ej():
    """
    Real Name: "Historic conv nat. gas domestic EU extracted EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
)


def historic_net_imports_nat_gas_eu():
    """
    Real Name: "Historic net imports nat. gas EU"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        ped_nat_gas_ej()
        - historic_conv_nat_gas_domestic_eu_extracted_ej()
        - historic_unconv_nat_gas_domestic_eu_extracted_ej()
    )


def historic_share_conv_nat_gas_domestic_eu_extraction_until_2016():
    """
    Real Name: "Historic share conv. nat gas domestic EU extraction until 2016"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()


_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016",
    )
)


def historic_share_conv_nat_gas_domestic_eu_extraction():
    """
    Real Name: "Historic share conv. nat gas domestic EU extraction"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(historic_conv_nat_gas_domestic_eu_extracted_ej(), ped_nat_gas_ej())


def historic_share_net_imports_nat_gas_until_2016():
    """
    Real Name: "Historic share net imports nat. gas until 2016"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_historic_share_net_imports_nat_gas_until_2016()


_sampleiftrue_historic_share_net_imports_nat_gas_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_nat_gas_eu(), extraction_nat_gas_ej_world()),
    lambda: zidz(historic_net_imports_nat_gas_eu(), extraction_nat_gas_ej_world()),
    "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016",
)


def historic_share_unconv_nat_gas_domestric_eu_extraction_until_2016():
    """
    Real Name: "Historic share unconv. nat. gas domestric EU extraction until 2016"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2016,
        lambda: historic_share_unconv_nat_gas_domestric_eu_extraction(),
        lambda: historic_share_unconv_nat_gas_domestric_eu_extraction(),
    )


def historic_share_unconv_nat_gas_domestric_eu_extraction():
    """
    Real Name: "Historic share unconv. nat. gas domestric EU extraction"
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(historic_unconv_nat_gas_domestic_eu_extracted_ej(), ped_nat_gas_ej())


def historic_unconv_nat_gas_domestic_eu_extracted_ej():
    """
    Real Name: "Historic unconv nat. gas domestic EU extracted EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
)


def imports_eu_conv_gas_from_row_ej():
    """
    Real Name: imports EU conv gas from RoW EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return imports_eu_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()


def imports_eu_nat_gas_from_row_ej():
    """
    Real Name: "imports EU nat. gas from RoW EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2016,
        lambda: ped_eu_nat_gas_from_row(),
        lambda: if_then_else(
            limit_nat_gas_imports_from_row() == 1,
            lambda: ped_eu_nat_gas_from_row(),
            lambda: if_then_else(
                limit_nat_gas_imports_from_row() == 2,
                lambda: np.minimum(
                    ped_eu_nat_gas_from_row(),
                    historic_share_net_imports_nat_gas_until_2016()
                    * extraction_nat_gas_ej_world(),
                ),
                lambda: if_then_else(
                    limit_nat_gas_imports_from_row() == 3,
                    lambda: np.minimum(
                        ped_eu_nat_gas_from_row(),
                        adapt_max_share_imports_nat_gas()
                        * extraction_nat_gas_ej_world(),
                    ),
                    lambda: ped_eu_nat_gas_from_row(),
                ),
            ),
        ),
    )


def imports_eu_unconv_gas_from_row_ej():
    """
    Real Name: imports EU unconv gas from RoW EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return imports_eu_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


def limit_nat_gas_imports_from_row():
    """
    Real Name: limit nat gas imports from RoW
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    1: Unlimited coal imports share from RoW (constrained by total global production) 2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global production) 3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_nat_gas_imports_from_row()


_ext_constant_limit_nat_gas_imports_from_row = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "limit_nat_gas_imports_from_RoW",
    {},
    _root,
    "_ext_constant_limit_nat_gas_imports_from_row",
)


def max_share_imports_nat_gas():
    """
    Real Name: max share imports nat gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_max_share_imports_nat_gas()


_ext_constant_max_share_imports_nat_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "max_share_imports_nat_gas",
    {},
    _root,
    "_ext_constant_max_share_imports_nat_gas",
)


def other_gases_required():
    """
    Real Name: Other gases required
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
    )


def pec_nat_gas():
    """
    Real Name: "PEC nat. gas"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_nat_gas_eu() + imports_eu_nat_gas_from_row_ej()


def ped_domestic_eu_conv_nat_gas_ej():
    """
    Real Name: "PED domestic EU conv. nat. gas EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        ped_nat_gas_ej()
        * historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()
    )


def ped_domestic_eu_total_natgas_ej():
    """
    Real Name: "PED domestic EU total nat.gas EJ"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return ped_nat_gas_ej() * (
        historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()
        + historic_share_unconv_nat_gas_domestric_eu_extraction_until_2016()
    )


def ped_eu_nat_gas_from_row():
    """
    Real Name: "PED EU nat. gas from RoW"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_eu())


def ped_gases():
    """
    Real Name: PED gases
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


def pes_gases():
    """
    Real Name: PES gases
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply gas.
    """
    return pec_nat_gas() + pes_biogas_for_tfc()


def real_fe_consumption_gases_ej():
    """
    Real Name: real FE consumption gases EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real final energy consumption by gases after accounting for energy availability.
    """
    return (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()


def required_fed_by_gas():
    """
    Real Name: Required FED by gas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


def share_biogas_in_pes():
    """
    Real Name: Share biogas in PES
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(pes_biogas_for_tfc(), pes_gases())


def share_gases_dem_for_heatnc():
    """
    Real Name: "share gases dem for Heat-nc"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of natural gas demand for non-commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), pes_gases() - ped_nat_gas_for_gtl_ej())


def share_gases_for_final_energy():
    """
    Real Name: share gases for final energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gas(),
        ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required(),
    )


def share_imports_eu_nat_gas_from_row_vs_extraction_world():
    """
    Real Name: "share imports EU nat. gas from RoW vs extraction World"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of EU natural gas imports vs global natural gas extraction.
    """
    return zidz(imports_eu_nat_gas_from_row_ej(), extraction_nat_gas_ej_world())


def share_nat_gas_dem_for_elec():
    """
    Real Name: "share nat. gas dem for Elec"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of natural gas demand for commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


def year_scarcity_gases():
    """
    Real Name: Year scarcity gases
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
