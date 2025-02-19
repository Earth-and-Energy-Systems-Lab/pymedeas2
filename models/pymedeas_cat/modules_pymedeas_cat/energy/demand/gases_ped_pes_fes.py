"""
Module gases_ped_pes_fes
Translated using PySD version 3.2.0
"""


@component.add(
    name="abundance gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 3, "pes_gases": 2},
)
def abundance_gases():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_gases() < pes_gases(),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


@component.add(
    name="adapt max share imports nat gas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_share_net_imports_nat_gas_until_2016": 3,
        "max_share_imports_nat_gas": 2,
    },
)
def adapt_max_share_imports_nat_gas():
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


@component.add(
    name="check gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "pes_gases": 2},
)
def check_gases():
    """
    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


@component.add(
    name='"constrain gas exogenous growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"check_gases": 2},
)
def constrain_gas_exogenous_growth():
    """
    If negative, there is oversupply of gas. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


@component.add(
    name="FES total biogas",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_biogas_in_pes": 1, "real_fe_consumption_gases_ej": 1},
)
def fes_total_biogas():
    return share_biogas_in_pes() * real_fe_consumption_gases_ej()


@component.add(
    name='"Historic conv nat. gas domestic AUT extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej",
        "__data__": "_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej",
        "time": 1,
    },
)
def historic_conv_nat_gas_domestic_aut_extracted_ej():
    return _ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_nat_gas_domestic_aut_extracted_ej",
)


@component.add(
    name='"Historic net imports nat. gas AUT"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_conv_nat_gas_domestic_aut_extracted_ej": 1,
        "historic_unconv_nat_gas_domestic_aut_extracted_ej": 1,
    },
)
def historic_net_imports_nat_gas_aut():
    return (
        ped_nat_gas_ej()
        - historic_conv_nat_gas_domestic_aut_extracted_ej()
        - historic_unconv_nat_gas_domestic_aut_extracted_ej()
    )


@component.add(
    name='"Historic share conv. nat gas domestic AUT extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_nat_gas_domestic_aut_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_conv_nat_gas_domestic_aut_extraction():
    return zidz(historic_conv_nat_gas_domestic_aut_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic share conv. nat gas domestic AUT extraction\\" until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016": {
            "initial": {"historic_share_conv_nat_gas_domestic_aut_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_conv_nat_gas_domestic_aut_extraction": 1,
            },
        }
    },
)
def historic_share_conv_nat_gas_domestic_aut_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
    )


_sampleiftrue_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_aut_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_aut_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_aut_extraction_until_2016",
    )
)


@component.add(
    name='"Historic share net imports nat. gas until 2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_historic_share_net_imports_nat_gas_until_2016": 1},
    other_deps={
        "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016": {
            "initial": {
                "historic_net_imports_nat_gas_aut": 1,
                "extraction_nat_gas_ej_world": 1,
            },
            "step": {
                "time": 1,
                "extraction_nat_gas_ej_world": 1,
                "historic_net_imports_nat_gas_aut": 1,
            },
        }
    },
)
def historic_share_net_imports_nat_gas_until_2016():
    return _sampleiftrue_historic_share_net_imports_nat_gas_until_2016()


_sampleiftrue_historic_share_net_imports_nat_gas_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_nat_gas_aut(), extraction_nat_gas_ej_world()),
    lambda: zidz(historic_net_imports_nat_gas_aut(), extraction_nat_gas_ej_world()),
    "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016",
)


@component.add(
    name='"Historic share unconv. nat. gas domestric AUT extraction until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016": {
            "initial": {"historic_share_unconv_nat_gas_domestric_aut_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_unconv_nat_gas_domestric_aut_extraction": 1,
            },
        }
    },
)
def historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016()
    )


_sampleiftrue_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_unconv_nat_gas_domestric_aut_extraction(),
    lambda: historic_share_unconv_nat_gas_domestric_aut_extraction(),
    "_sampleiftrue_historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016",
)


@component.add(
    name='"Historic share unconv. nat. gas domestric AUT extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_unconv_nat_gas_domestic_aut_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_unconv_nat_gas_domestric_aut_extraction():
    return zidz(historic_unconv_nat_gas_domestic_aut_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic unconv nat. gas domestic AUT extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej",
        "__data__": "_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_nat_gas_domestic_aut_extracted_ej():
    return _ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_nat_gas_domestic_aut_extracted_ej",
)


@component.add(
    name="imports AUT conv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_aut_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_aut_conv_gas_from_row_ej():
    return (
        imports_aut_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name='"imports AUT nat. gas from RoW EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ped_aut_nat_gas_from_row": 5,
        "extraction_nat_gas_ej_world": 2,
        "limit_nat_gas_imports_from_row": 3,
        "adapt_max_share_imports_nat_gas": 1,
        "historic_share_net_imports_nat_gas_until_2016": 1,
    },
)
def imports_aut_nat_gas_from_row_ej():
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


@component.add(
    name="imports AUT unconv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_aut_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_aut_unconv_gas_from_row_ej():
    return imports_aut_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name="limit nat gas imports from RoW",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_limit_nat_gas_imports_from_row"},
)
def limit_nat_gas_imports_from_row():
    """
    1: Unlimited coal imports share from RoW (constrained by total global production) 2: Limited imports coal of UE from RoW (at 2016 share of EU imports vs global production) 3: Limited imports coal of UE from Row (user defined)
    """
    return _ext_constant_limit_nat_gas_imports_from_row()


_ext_constant_limit_nat_gas_imports_from_row = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "limit_nat_gas_imports_from_RoW",
    {},
    _root,
    {},
    "_ext_constant_limit_nat_gas_imports_from_row",
)


@component.add(
    name="max share imports nat gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_share_imports_nat_gas"},
)
def max_share_imports_nat_gas():
    return _ext_constant_max_share_imports_nat_gas()


_ext_constant_max_share_imports_nat_gas = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "max_share_imports_nat_gas",
    {},
    _root,
    {},
    "_ext_constant_max_share_imports_nat_gas",
)


@component.add(
    name="Other gases required",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 2,
        "energy_distr_losses_ff_ej": 2,
        "nonenergy_use_demand_by_final_fuel_ej": 2,
    },
)
def other_gases_required():
    return if_then_else(
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        < 0,
        lambda: 0,
        lambda: float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff_ej().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]),
    )


@component.add(
    name='"PEC nat. gas"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_aut_1": 1, "imports_aut_nat_gas_from_row_ej": 1},
)
def pec_nat_gas():
    return pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej()


@component.add(
    name='"PED AUT nat. gas from RoW"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "pes_nat_gas_aut_1": 1},
)
def ped_aut_nat_gas_from_row():
    return np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_aut_1())


@component.add(
    name='"PED domestic AUT conv. nat. gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_share_conv_nat_gas_domestic_aut_extraction_until_2016": 1,
    },
)
def ped_domestic_aut_conv_nat_gas_ej():
    return (
        ped_nat_gas_ej()
        * historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
    )


@component.add(
    name='"PED domestic AUT total nat.gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_share_conv_nat_gas_domestic_aut_extraction_until_2016": 1,
        "historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016": 1,
    },
)
def ped_domestic_aut_total_natgas_ej():
    return ped_nat_gas_ej() * (
        historic_share_conv_nat_gas_domestic_aut_extraction_until_2016()
        + historic_share_unconv_nat_gas_domestric_aut_extraction_until_2016()
    )


@component.add(
    name="PED gases",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "pe_demand_gas_elec_plants_ej": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "other_gases_required": 1,
    },
)
def ped_gases():
    """
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


@component.add(
    name='"PED nat. gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "pes_biogas_for_tfc": 1},
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(0, ped_gases() - pes_biogas_for_tfc())


@component.add(
    name="PES gases",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_nat_gas": 1, "pes_biogas_for_tfc": 1},
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return pec_nat_gas() + pes_biogas_for_tfc()


@component.add(
    name="real FE consumption gases EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_gases": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "other_gases_required": 1,
        "share_gases_for_final_energy": 1,
    },
)
def real_fe_consumption_gases_ej():
    """
    Real final energy consumption by gases after accounting for energy availability.
    """
    return (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()


@component.add(
    name="Required FED by gas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_gas():
    """
    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


@component.add(
    name="Share biogas in PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_tfc": 1, "pes_gases": 1},
)
def share_biogas_in_pes():
    return zidz(pes_biogas_for_tfc(), pes_gases())


@component.add(
    name='"share gases dem for Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gas_heatnc": 1, "ped_nat_gas_for_gtl_ej": 1, "pes_gases": 1},
)
def share_gases_dem_for_heatnc():
    """
    Share of natural gas demand for non-commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), pes_gases() - ped_nat_gas_for_gtl_ej())


@component.add(
    name="share gases for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "other_gases_required": 1,
        "ped_gases": 1,
    },
)
def share_gases_for_final_energy():
    """
    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gas(),
        ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required(),
    )


@component.add(
    name='"share imports AUT nat. gas from RoW vs extraction World"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_aut_nat_gas_from_row_ej": 1, "extraction_nat_gas_ej_world": 1},
)
def share_imports_aut_nat_gas_from_row_vs_extraction_world():
    """
    Share of EU natural gas imports vs global natural gas extraction.
    """
    return zidz(imports_aut_nat_gas_from_row_ej(), extraction_nat_gas_ej_world())


@component.add(
    name='"share nat. gas dem for Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 2, "pe_demand_gas_elec_plants_ej": 1},
)
def share_nat_gas_dem_for_elec():
    """
    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: pe_demand_gas_elec_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name='"share nat. gas dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 2, "ped_gases_for_heat_plants_ej": 1},
)
def share_nat_gas_dem_for_heatcom():
    """
    Share of natural gas demand for commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name="Year scarcity gases",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 1, "time": 1},
)
def year_scarcity_gases():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
