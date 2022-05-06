"""
Module solids_ped_pes_fes
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="abundance solids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids": 2, "ped_solids": 3},
)
def abundance_solids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pes_solids() > ped_solids(),
        lambda: 1,
        lambda: 1 - zidz(ped_solids() - pes_solids(), ped_solids()),
    )


@component.add(
    name="adapt max share imports coal",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_share_net_imports_coal_aut_until_2016": 3,
        "max_share_imports_coal": 2,
    },
)
def adapt_max_share_imports_coal():
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


@component.add(
    name="extraction coal EJ RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej_world": 1, "extraction_coal_aut": 1},
)
def extraction_coal_ej_row():
    return extraction_coal_ej_world() - extraction_coal_aut()


@component.add(
    name="check domestic AUT extracted",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_aut": 1, "historic_coal_domestic_aut_extracted_ej": 1},
)
def check_domestic_aut_extracted():
    return -1 + zidz(extraction_coal_aut(), historic_coal_domestic_aut_extracted_ej())


@component.add(
    name="Historic coal domestic AUT extracted EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_coal_domestic_aut_extracted_ej",
        "__data__": "_ext_data_historic_coal_domestic_aut_extracted_ej",
        "time": 1,
    },
)
def historic_coal_domestic_aut_extracted_ej():
    return _ext_data_historic_coal_domestic_aut_extracted_ej(time())


_ext_data_historic_coal_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_coal_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_coal_domestic_aut_extracted_ej",
)


@component.add(
    name="Historic net imports coal AUT",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "historic_coal_domestic_aut_extracted_ej": 1},
)
def historic_net_imports_coal_aut():
    return ped_coal_ej() - historic_coal_domestic_aut_extracted_ej()


@component.add(
    name="Historic PES peat EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_pes_peat_ej",
        "__data__": "_ext_data_historic_pes_peat_ej",
        "time": 1,
    },
)
def historic_pes_peat_ej():
    """
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
    {},
    "_ext_data_historic_pes_peat_ej",
)


@component.add(
    name="Historic share coal domestic AUT extraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_coal_domestic_aut_extracted_ej": 1, "ped_coal_ej": 1},
)
def historic_share_coal_domestic_aut_extraction():
    return zidz(historic_coal_domestic_aut_extracted_ej(), ped_coal_ej())


@component.add(
    name="Historic share coal domestic AUT extraction until 2016",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016": {
            "initial": {"historic_share_coal_domestic_aut_extraction": 1},
            "step": {"time": 1, "historic_share_coal_domestic_aut_extraction": 1},
        }
    },
)
def historic_share_coal_domestic_aut_extraction_until_2016():
    return _sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016()


_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_coal_domestic_aut_extraction(),
    lambda: historic_share_coal_domestic_aut_extraction(),
    "_sampleiftrue_historic_share_coal_domestic_aut_extraction_until_2016",
)


@component.add(
    name="Historic share net imports coal AUT until 2016",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_historic_share_net_imports_coal_aut_until_2016": 1},
    other_deps={
        "_sampleiftrue_historic_share_net_imports_coal_aut_until_2016": {
            "initial": {
                "historic_net_imports_coal_aut": 1,
                "extraction_coal_ej_world": 1,
            },
            "step": {
                "time": 1,
                "extraction_coal_ej_world": 1,
                "historic_net_imports_coal_aut": 1,
            },
        }
    },
)
def historic_share_net_imports_coal_aut_until_2016():
    return _sampleiftrue_historic_share_net_imports_coal_aut_until_2016()


_sampleiftrue_historic_share_net_imports_coal_aut_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_coal_aut(), extraction_coal_ej_world()),
    lambda: zidz(historic_net_imports_coal_aut(), extraction_coal_ej_world()),
    "_sampleiftrue_historic_share_net_imports_coal_aut_until_2016",
)


@component.add(
    name="imports AUT coal from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ped_aut_coal_from_row": 5,
        "extraction_coal_ej_world": 2,
        "limit_coal_imports_from_row": 3,
        "adapt_max_share_imports_coal": 1,
        "historic_share_net_imports_coal_aut_until_2016": 1,
    },
)
def imports_aut_coal_from_row_ej():
    """
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


@component.add(
    name="limit coal imports from RoW",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_limit_coal_imports_from_row"},
)
def limit_coal_imports_from_row():
    """
    1: Unlimited coal imports share from RoW (constrained by total global production) 2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global production) 3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_coal_imports_from_row()


_ext_constant_limit_coal_imports_from_row = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "limit_coal_imports_from_RoW",
    {},
    _root,
    {},
    "_ext_constant_limit_coal_imports_from_row",
)


@component.add(
    name="max share imports coal",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_share_imports_coal"},
)
def max_share_imports_coal():
    return _ext_constant_max_share_imports_coal()


_ext_constant_max_share_imports_coal = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "max_share_imports_coal",
    {},
    _root,
    {},
    "_ext_constant_max_share_imports_coal",
)


@component.add(
    name="Other solids required",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def other_solids_required():
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff_ej().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


@component.add(
    name="PEC coal",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_aut": 1, "imports_aut_coal_from_row_ej": 1},
)
def pec_coal():
    return extraction_coal_aut() + imports_aut_coal_from_row_ej()


@component.add(
    name="PED AUT coal from RoW",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "extraction_coal_aut": 1},
)
def ped_aut_coal_from_row():
    return np.maximum(0, ped_coal_ej() - extraction_coal_aut())


@component.add(
    name="PED coal EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_solids": 1,
        "pes_waste_for_tfc": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pes_peat_ej": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def ped_coal_ej():
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


@component.add(
    name="PED domestic AUT coal EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_ej": 1,
        "historic_share_coal_domestic_aut_extraction_until_2016": 1,
    },
)
def ped_domestic_aut_coal_ej():
    return ped_coal_ej() * historic_share_coal_domestic_aut_extraction_until_2016()


@component.add(
    name="PED solids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_solids": 1,
        "ped_coal_for_ctl_ej": 1,
        "pe_demand_coal_elec_plants_ej": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "other_solids_required": 1,
    },
)
def ped_solids():
    """
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


@component.add(
    name="PED2",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_solids": 1, "transformation_ff_losses_ej": 1},
)
def ped2():
    return ped_solids() - float(transformation_ff_losses_ej().loc["solids"])


@component.add(
    name="PES peat EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_pes_peat_ej": 1},
)
def pes_peat_ej():
    return historic_pes_peat_ej()


@component.add(
    name="PES solids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_coal": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_peat_ej": 1,
        "pes_waste_for_tfc": 1,
        "losses_in_charcoal_plants_ej": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def pes_solids():
    """
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


@component.add(
    name="real FE consumption solids EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_aut": 1,
        "imports_aut_coal_from_row_ej": 1,
        "pes_waste_for_tfc": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pes_peat_ej": 1,
        "modern_solids_bioe_demand_households": 1,
        "ped_coal_for_ctl_ej": 1,
        "other_solids_required": 1,
        "share_solids_for_final_energy": 1,
    },
)
def real_fe_consumption_solids_ej():
    """
    Real final energy consumption by solids after accounting for energy availability.
    """
    return (
        extraction_coal_aut()
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


@component.add(
    name="Required FED solids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_solids():
    """
    Required final energy demand solids.
    """
    return float(required_fed_by_fuel().loc["solids"])


@component.add(
    name="share coal dem for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "pe_demand_coal_elec_plants_ej": 1},
)
def share_coal_dem_for_elec():
    """
    Share of coal demand to cover electricity consumption in Elec plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: pe_demand_coal_elec_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share coal dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "ped_coal_for_heat_plants_ej": 1},
)
def share_coal_dem_for_heatcom():
    """
    Share of coal demand to cover commercial heat consumption in Heat plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: ped_coal_for_heat_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share coal dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_heatnc": 1, "ped_coal_ej": 1},
)
def share_coal_dem_for_heatnc():
    """
    Share of coal demand to cover non-commercial heat consumption in Heat plants.
    """
    return zidz(ped_coal_heatnc(), ped_coal_ej())


@component.add(
    name="share imports AUT coal from RoW vs extraction World",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_aut_coal_from_row_ej": 1, "extraction_coal_ej_world": 1},
)
def share_imports_aut_coal_from_row_vs_extraction_world():
    """
    Share of EU coal imports vs global coal extraction.
    """
    return zidz(imports_aut_coal_from_row_ej(), extraction_coal_ej_world())


@component.add(
    name="share solids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_solids": 1,
        "other_solids_required": 1,
        "ped_coal_for_ctl_ej": 1,
        "ped_solids": 1,
    },
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_solids(),
        ped_solids() - ped_coal_for_ctl_ej() - other_solids_required(),
    )
