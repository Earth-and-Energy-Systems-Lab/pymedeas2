"""
Module solids_ped_pes_fes
Translated using PySD version 2.2.1
"""


def abundance_solids():
    """
    Real Name: abundance solids
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pes_solids() > ped_solids(),
        lambda: 1,
        lambda: 1 - zidz(ped_solids() - pes_solids(), ped_solids()),
    )


def adapt_max_share_imports_coal():
    """
    Real Name: adapt max share imports coal
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2016,
        lambda: historic_share_net_imports_coal_aut_until_2016(),
        lambda: if_then_else(
            time() < 2021,
            lambda: historic_share_net_imports_coal_aut_until_2016()
            + (
                max_share_imports_coal()
                - historic_share_net_imports_coal_aut_until_2016()
            )
            * ((time() - 2016) / (2021 - 2016)),
            lambda: max_share_imports_coal(),
        ),
    )


def check_domestic_aut_extracted():
    """
    Real Name: check domestic AUT extracted
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return -1 + zidz(
        extraction_coal_ej_aut(), historic_coal_domestic_aut_extracted_ej()
    )


def extraction_coal_ej_row():
    """
    Real Name: extraction coal EJ RoW
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return extraction_coal_ej_world() - extraction_coal_ej_aut()


def historic_coal_domestic_aut_extracted_ej():
    """
    Real Name: Historic coal domestic AUT extracted EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []


    """
    return _ext_data_historic_coal_domestic_aut_extracted_ej(time())


_ext_data_historic_coal_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_coal_extraction",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_coal_domestic_aut_extracted_ej",
)


def historic_net_imports_coal_aut():
    """
    Real Name: Historic net imports coal AUT
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return ped_coal_ej() - historic_coal_domestic_aut_extracted_ej()


def historic_pes_peat_ej():
    """
    Real Name: Historic PES peat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []

    Historic primary energy supply of peat.
    """
    return _ext_data_historic_pes_peat_ej(time())


_ext_data_historic_pes_peat_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_primary_energy_supply_peat",
    "interpolate",
    {},
    _root,
    "_ext_data_historic_pes_peat_ej",
)


def historic_share_coal_domestic_aut_extraction():
    """
    Real Name: Historic share coal domestic AUT extraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(historic_coal_domestic_aut_extracted_ej(), ped_coal_ej())


def historic_share_coal_domestic_aut_extraction_until_2016():
    """
    Real Name: Historic share coal domestic AUT extraction until 2016
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016()


_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_coal_domestic_aut_extraction(),
    lambda: historic_share_coal_domestic_aut_extraction(),
    "_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016",
)


def historic_share_net_imports_coal_aut_until_2016():
    """
    Real Name: Historic share net imports coal AUT until 2016
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_historic_share_net_imports_coal_aut_until_2016()


_sampleiftrue_historic_share_net_imports_coal_aut_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_coal_aut(), extraction_coal_ej_world()),
    lambda: zidz(historic_net_imports_coal_aut(), extraction_coal_ej_world()),
    "_sampleiftrue_historic_share_net_imports_coal_aut_until_2016",
)


def imports_aut_coal_from_row_ej():
    """
    Real Name: imports AUT coal from RoW EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    IF THEN ELSE(Time<2016, Historic share net imports coal EU until 2016*extraction coal EJ World, IF THEN ELSE(limit coal imports from RoW=0, PED EU coal from RoW, IF THEN ELSE (limit coal imports from RoW=1, MIN(PED EU coal from RoW, Historic share net imports coal EU until 2016*extraction coal EJ World), PED EU coal from RoW))) IF THEN ELSE(Time<2016, PED EU coal from RoW, IF THEN ELSE(limit coal imports from RoW=0, PED EU coal from RoW, IF THEN ELSE (limit coal imports from RoW=1, MIN(PED EU coal from RoW, Historic share net imports coal EU until 2016*extraction coal EJ World), PED EU coal from RoW)))
    """
    return if_then_else(
        time() < 2016,
        lambda: ped_aut_coal_from_row(),
        lambda: if_then_else(
            limit_coal_imports_from_row() == 1,
            lambda: ped_aut_coal_from_row(),
            lambda: if_then_else(
                limit_coal_imports_from_row() == 2,
                lambda: np.minimum(
                    ped_aut_coal_from_row(),
                    historic_share_net_imports_coal_aut_until_2016()
                    * extraction_coal_ej_world(),
                ),
                lambda: if_then_else(
                    limit_coal_imports_from_row() == 3,
                    lambda: np.minimum(
                        ped_aut_coal_from_row(),
                        adapt_max_share_imports_coal() * extraction_coal_ej_world(),
                    ),
                    lambda: ped_aut_coal_from_row(),
                ),
            ),
        ),
    )


def limit_coal_imports_from_row():
    """
    Real Name: limit coal imports from RoW
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    1: Unlimited coal imports share from RoW (constrained by total global production) 2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global production) 3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_coal_imports_from_row()


_ext_constant_limit_coal_imports_from_row = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "limit_coal_imports_from_RoW",
    {},
    _root,
    "_ext_constant_limit_coal_imports_from_row",
)


def max_share_imports_coal():
    """
    Real Name: max share imports coal
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_max_share_imports_coal()


_ext_constant_max_share_imports_coal = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "max_share_imports_coal",
    {},
    _root,
    "_ext_constant_max_share_imports_coal",
)


def other_solids_required():
    """
    Real Name: Other solids required
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff_ej().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


def pec_coal():
    """
    Real Name: PEC coal
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return extraction_coal_ej_aut() + imports_aut_coal_from_row_ej()


def ped_aut_coal_from_row():
    """
    Real Name: PED AUT coal from RoW
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return np.maximum(0, ped_coal_ej() - extraction_coal_ej_aut())


def ped_coal_ej():
    """
    Real Name: PED coal EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return np.maximum(
        0,
        ped_solids()
        - (
            pe_traditional_biomass_ej_delayed_1yr()
            + modern_solids_bioe_demand_households()
            + pes_peat_ej()
            + pes_waste_for_tfc()
            + losses_in_charcoal_plants_ej()
        ),
    )


def ped_domestic_aut_coal_ej():
    """
    Real Name: PED domestic AUT coal EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return ped_coal_ej() * historic_share_coal_domestic_aut_extraction_until_2016()


def ped_solids():
    """
    Real Name: PED solids
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of solids.
    """
    return np.maximum(
        0,
        required_fed_solids()
        + ped_coal_for_ctl_ej()
        + pe_demand_coal_elec_plants_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required(),
    )


def ped2():
    """
    Real Name: PED2
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return ped_solids() - float(transformation_ff_losses_ej().loc["solids"])


def pes_peat_ej():
    """
    Real Name: PES peat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return historic_pes_peat_ej()


def pes_solids():
    """
    Real Name: PES solids
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply solids.
    """
    return (
        pec_coal()
        + pe_traditional_biomass_ej_delayed_1yr()
        + pes_peat_ej()
        + pes_waste_for_tfc()
        + losses_in_charcoal_plants_ej()
        + modern_solids_bioe_demand_households()
    )


def real_fe_consumption_solids_ej():
    """
    Real Name: real FE consumption solids EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real final energy consumption by solids after accounting for energy availability.
    """
    return (
        extraction_coal_ej_aut()
        + imports_aut_coal_from_row_ej()
        + (
            modern_solids_bioe_demand_households()
            + pe_traditional_biomass_ej_delayed_1yr()
            + pes_waste_for_tfc()
            + pes_peat_ej()
            + losses_in_charcoal_plants_ej()
        )
        - ped_coal_for_ctl_ej()
        - other_solids_required()
    ) * share_solids_for_final_energy()


def required_fed_solids():
    """
    Real Name: Required FED solids
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required final energy demand solids.
    """
    return float(required_fed_by_fuel().loc["solids"])


def share_coal_dem_for_elec():
    """
    Real Name: share coal dem for Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of coal demand to cover electricity consumption in Elec plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: pe_demand_coal_elec_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


def share_coal_dem_for_heatcom():
    """
    Real Name: "share coal dem for Heat-com"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of coal demand to cover commercial heat consumption in Heat plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: ped_coal_for_heat_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


def share_coal_dem_for_heatnc():
    """
    Real Name: "share coal dem for Heat-nc"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of coal demand to cover non-commercial heat consumption in Heat plants.
    """
    return zidz(ped_coal_heatnc(), ped_coal_ej())


def share_imports_aut_coal_from_row_vs_extraction_world():
    """
    Real Name: share imports AUT coal from RoW vs extraction World
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of EU coal imports vs global coal extraction.
    """
    return zidz(imports_aut_coal_from_row_ej(), extraction_coal_ej_world())


def share_solids_for_final_energy():
    """
    Real Name: share solids for final energy
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_solids(),
        ped_solids() - ped_coal_for_ctl_ej() - other_solids_required(),
    )
