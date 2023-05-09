"""
Module energy.demand.gases_ped_pes_fes
Translated using PySD version 3.10.0
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
    name="Energy losses from gases",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_distr_losses_ff_ej": 1, "transformation_ff_losses_ej": 1},
)
def energy_losses_from_gases():
    """
    Gases-related distribution and transformation losses.
    """
    return float(energy_distr_losses_ff_ej().loc["gases"]) + float(
        transformation_ff_losses_ej().loc["gases"]
    )


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
    name='"Historic conv nat. gas domestic CAT extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_conv_nat_gas_domestic_cat_extracted_ej():
    return _ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
)


@component.add(
    name='"Historic net imports nat. gas CAT "',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_conv_nat_gas_domestic_cat_extracted_ej": 1,
        "historic_unconv_nat_gas_domestic_cat_extracted_ej": 1,
    },
)
def historic_net_imports_nat_gas_cat_():
    return (
        ped_nat_gas_ej()
        - historic_conv_nat_gas_domestic_cat_extracted_ej()
        - historic_unconv_nat_gas_domestic_cat_extracted_ej()
    )


@component.add(
    name='"Historic share conv. nat gas domestic CAT extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_nat_gas_domestic_cat_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_conv_nat_gas_domestic_cat_extraction():
    return zidz(historic_conv_nat_gas_domestic_cat_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic share conv. nat gas domestic CAT extraction\\" until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": {
            "initial": {"historic_share_conv_nat_gas_domestic_cat_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_conv_nat_gas_domestic_cat_extraction": 1,
            },
        }
    },
)
def historic_share_conv_nat_gas_domestic_cat_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016()
    )


_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_cat_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_cat_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016",
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
                "historic_net_imports_nat_gas_cat_": 1,
                "extraction_nat_gas_ej_world": 1,
            },
            "step": {
                "time": 1,
                "historic_net_imports_nat_gas_cat_": 1,
                "extraction_nat_gas_ej_world": 1,
            },
        }
    },
)
def historic_share_net_imports_nat_gas_until_2016():
    return _sampleiftrue_historic_share_net_imports_nat_gas_until_2016()


_sampleiftrue_historic_share_net_imports_nat_gas_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_nat_gas_cat_(), extraction_nat_gas_ej_world()),
    lambda: zidz(historic_net_imports_nat_gas_cat_(), extraction_nat_gas_ej_world()),
    "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016",
)


@component.add(
    name='"Historic share unconv. nat. gas domestric CAT extraction"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_unconv_nat_gas_domestic_cat_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_unconv_nat_gas_domestric_cat_extraction():
    return zidz(historic_unconv_nat_gas_domestic_cat_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic share unconv. nat. gas domestric CAT extraction until 2016"',
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016": {
            "initial": {"historic_share_unconv_nat_gas_domestric_cat_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_unconv_nat_gas_domestric_cat_extraction": 1,
            },
        }
    },
)
def historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016()
    )


_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_unconv_nat_gas_domestric_cat_extraction(),
    lambda: historic_share_unconv_nat_gas_domestric_cat_extraction(),
    "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016",
)


@component.add(
    name='"Historic unconv nat. gas domestic CAT extracted EJ"',
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_nat_gas_domestic_cat_extracted_ej():
    return _ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
)


@component.add(
    name="imports CAT conv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_cat_conv_gas_from_row_ej():
    return (
        imports_cat_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name='"imports CAT nat. gas from RoW EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_gas_flux_cat": 1},
)
def imports_cat_nat_gas_from_row_ej():
    return net_gas_flux_cat()


@component.add(
    name="imports CAT unconv gas from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_cat_unconv_gas_from_row_ej():
    return imports_cat_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name="PEC biogas for conversion",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_chp": 1,
        "pes_biogas_for_elec_plants": 1,
        "pes_biogas_for_heatcom_plants": 1,
    },
)
def pec_biogas_for_conversion():
    """
    Primary energy consumption of biogas to transform it into heat and electricity. Biogas is considered a substitute of fossil gas, therefore introduced as an alternative supply through policies.
    """
    return (
        pes_biogas_for_chp()
        + pes_biogas_for_elec_plants()
        + pes_biogas_for_heatcom_plants()
    )


@component.add(
    name='"PEC nat. gas"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_cat_": 1, "imports_cat_nat_gas_from_row_ej": 1},
)
def pec_nat_gas():
    return pes_nat_gas_cat_() + imports_cat_nat_gas_from_row_ej()


@component.add(
    name="PEC nat gas for conversion",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_nat_gas": 1, "share_nat_gas_for_conversion": 1},
)
def pec_nat_gas_for_conversion():
    return pec_nat_gas() * share_nat_gas_for_conversion()


@component.add(
    name='"PED CAT nat. gas from RoW"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "pes_nat_gas_cat_": 1},
)
def ped_cat_nat_gas_from_row():
    return np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_cat_())


@component.add(
    name='"PED domestic CAT conv. nat. gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": 1,
    },
)
def ped_domestic_cat_conv_nat_gas_ej():
    return (
        ped_nat_gas_ej()
        * historic_share_conv_nat_gas_domestic_cat_extraction_until_2016()
    )


@component.add(
    name='"PED domestic CAT total nat.gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "imports_cat_nat_gas_from_row_ej": 1},
)
def ped_domestic_cat_total_natgas_ej():
    """
    "PED nat. gas EJ"*("Historic share conv. nat gas domestic CAT extraction
    " until 2016"+"Historic share unconv. nat. gas domestric CAT extraction until 2016" )
    """
    return np.maximum(0, ped_nat_gas_ej() - imports_cat_nat_gas_from_row_ej())


@component.add(
    name="PED gases",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gases": 1,
        "ped_nat_gas_for_conversion": 1,
        "pec_biogas_for_conversion": 1,
        "energy_losses_from_gases": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def ped_gases():
    """
    Primary energy demand total gases.
    """
    return np.maximum(
        0,
        required_fed_by_gases()
        + ped_nat_gas_for_conversion()
        + pec_biogas_for_conversion()
        + energy_losses_from_gases()
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]),
    )


@component.add(
    name='"PED nat. gas EJ"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_for_conversion": 1, "pes_biogas": 1, "ped_gases": 1},
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return np.maximum(
        ped_nat_gas_for_conversion(), np.maximum(0, ped_gases() - pes_biogas())
    )


@component.add(
    name='"PED nat. gas for conversion"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gas_elec_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "ped_nat_gas_for_gtl_ej": 1,
    },
)
def ped_nat_gas_for_conversion():
    """
    Primary energy demand of natural gas for conversion into heat and electricity.
    """
    return (
        ped_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + ped_gases_for_heat_plants_ej()
        + ped_nat_gas_for_gtl_ej()
    )


@component.add(
    name="PES gases",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_nat_gas": 1, "pes_biogas": 1},
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return pec_nat_gas() + pes_biogas()


@component.add(
    name="real FE consumption gases EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gases": 1,
        "share_gases_for_final_energy": 1,
        "energy_losses_from_gases": 1,
        "pes_gases": 1,
    },
)
def real_fe_consumption_gases_ej():
    """
    Real final energy consumption by gases after accounting for energy availability.
    """
    return np.minimum(
        required_fed_by_gases(),
        (pes_gases() - energy_losses_from_gases()) * share_gases_for_final_energy(),
    )


@component.add(
    name="Required FED by gases",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_gases():
    """
    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


@component.add(
    name="Share biogas in PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas": 1, "pes_gases": 1},
)
def share_biogas_in_pes():
    return zidz(pes_biogas(), pes_gases())


@component.add(
    name='"share FED vs non-energy"',
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_gases": 2, "nonenergy_use_demand_by_final_fuel_ej": 1},
)
def share_fed_vs_nonenergy():
    return zidz(
        required_fed_by_gases(),
        float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])
        + required_fed_by_gases(),
    )


@component.add(
    name="share gases for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gases": 1,
        "energy_losses_from_gases": 1,
        "ped_gases": 1,
    },
)
def share_gases_for_final_energy():
    """
    Share of final energy vs primary energy for gases.
    """
    return zidz(required_fed_by_gases(), ped_gases() - energy_losses_from_gases())


@component.add(
    name='"share gases for non-energy uses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "energy_losses_from_gases": 1,
        "ped_gases": 1,
    },
)
def share_gases_for_nonenergy_uses():
    return zidz(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]),
        ped_gases() - energy_losses_from_gases(),
    )


@component.add(
    name="share nat gas for conversion",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_for_conversion": 1, "ped_nat_gas_ej": 1},
)
def share_nat_gas_for_conversion():
    return zidz(ped_nat_gas_for_conversion(), ped_nat_gas_ej())
