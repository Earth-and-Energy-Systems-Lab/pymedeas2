"""
Module losses_in_transformation_and_distri
Translated using PySD version 3.0.0
"""


@component.add(
    name='"FEC gases+liquids"', units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fec_gasesliquids():
    return float(real_fe_consumption_by_fuel().loc["gases"]) + float(
        real_fe_consumption_by_fuel().loc["liquids"]
    )


@component.add(
    name="Energy distr losses FF EJ",
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
)
def energy_distr_losses_ff_ej():
    """
    Energy distribution losses of fossil fuels.
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = float(
        pes_fossil_fuel_extraction_delayed().loc["liquids"]
    ) * float(historic_share_of_losses_vs_extraction().loc["liquids"])
    value.loc[{"final sources": ["solids"]}] = float(
        pes_fossil_fuel_extraction_delayed().loc["solids"]
    ) * float(historic_share_of_losses_vs_extraction().loc["solids"])
    value.loc[{"final sources": ["gases"]}] = float(
        pes_fossil_fuel_extraction_delayed().loc["gases"]
    ) * float(historic_share_of_losses_vs_extraction().loc["gases"])
    value.loc[{"final sources": ["electricity"]}] = 0
    value.loc[{"final sources": ["heat"]}] = 0
    return value


@component.add(
    name="Historic pipeline transport",
    units="EJ",
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_pipeline_transport(x, final_subs=None):
    """
    Historic pipeline transport
    """
    return _ext_lookup_historic_pipeline_transport(x, final_subs)


_ext_lookup_historic_pipeline_transport = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_pipeline_transport",
    {},
    _root,
    {},
    "_ext_lookup_historic_pipeline_transport",
)


@component.add(
    name="Historic share of losses vs extraction",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Data",
    comp_subtype="External",
)
def historic_share_of_losses_vs_extraction():
    """
    Historic share losses of each fossil fuel vs annual extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_losses_vs_extraction(time())


_ext_data_historic_share_of_losses_vs_extraction = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    {"final sources": ["liquids", "solids", "gases"]},
    "_ext_data_historic_share_of_losses_vs_extraction",
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_gases",
    None,
    {"final sources": ["gases"]},
)


@component.add(
    name="Historic share of transformation losses vs extraction",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Data",
    comp_subtype="External",
)
def historic_share_of_transformation_losses_vs_extraction():
    """
    Historic share transformation losses of each fossil fuel vs annual extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_transformation_losses_vs_extraction(time())


_ext_data_historic_share_of_transformation_losses_vs_extraction = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    {"final sources": ["liquids", "solids"]},
    "_ext_data_historic_share_of_transformation_losses_vs_extraction",
)

_ext_data_historic_share_of_transformation_losses_vs_extraction.add(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)


@component.add(
    name="Historic share pipeline transport",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_share_pipeline_transport():
    """
    Historic share of energy for pipeline transport vs TFEC of liquids and gases.
    """
    return if_then_else(
        time() < 2016,
        lambda: zidz(historic_pipeline_transport(time()), fec_gasesliquids()),
        lambda: 0,
    )


@component.add(
    name="PES fossil fuel extraction",
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_fossil_fuel_extraction():
    """
    Annual extraction of fossil fuels
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = (
        pes_total_oil_ej_eu() + imports_eu_total_oil_from_row_ej()
    )
    value.loc[{"final sources": ["solids"]}] = (
        extraction_coal_ej_eu() + imports_eu_coal_from_row_ej()
    )
    value.loc[{"final sources": ["gases"]}] = (
        pes_nat_gas_eu() + imports_eu_nat_gas_from_row_ej()
    )
    return value


@component.add(
    name="PES fossil fuel extraction delayed",
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pes_fossil_fuel_extraction_delayed():
    """
    Annual extraction of fossil fuels delayed
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[
        {"final sources": ["liquids"]}
    ] = _delayfixed_pes_fossil_fuel_extraction_delayed().values
    value.loc[
        {"final sources": ["solids"]}
    ] = _delayfixed_pes_fossil_fuel_extraction_delayed_1().values
    value.loc[
        {"final sources": ["gases"]}
    ] = _delayfixed_pes_fossil_fuel_extraction_delayed_2().values
    return value


_delayfixed_pes_fossil_fuel_extraction_delayed = DelayFixed(
    lambda: xr.DataArray(
        float(pes_fossil_fuel_extraction().loc["liquids"]),
        {"final sources": ["liquids"]},
        ["final sources"],
    ),
    lambda: time_step(),
    lambda: xr.DataArray(25.9, {"final sources": ["liquids"]}, ["final sources"]),
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed",
)

_delayfixed_pes_fossil_fuel_extraction_delayed_1 = DelayFixed(
    lambda: xr.DataArray(
        float(pes_fossil_fuel_extraction().loc["solids"]),
        {"final sources": ["solids"]},
        ["final sources"],
    ),
    lambda: time_step(),
    lambda: xr.DataArray(15.05, {"final sources": ["solids"]}, ["final sources"]),
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed_1",
)

_delayfixed_pes_fossil_fuel_extraction_delayed_2 = DelayFixed(
    lambda: xr.DataArray(
        float(pes_fossil_fuel_extraction().loc["gases"]),
        {"final sources": ["gases"]},
        ["final sources"],
    ),
    lambda: time_step(),
    lambda: xr.DataArray(12.2, {"final sources": ["gases"]}, ["final sources"]),
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed_2",
)


@component.add(
    name="Pipeline transport", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pipeline_transport():
    """
    Pipeline transport. IEA definition: Pipeline transport includes energy used in the support and operation of pipelines transporting gases, liquids, slurries and other commodities, including the energy used for pump stations and maintenance of the pipeline.
    """
    return share_pipeline_transport_fecgl_in_2015() * fec_gasesliquids()


@component.add(
    name="Ratio gain gas vs lose solids in tranf processes",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
)
def ratio_gain_gas_vs_lose_solids_in_tranf_processes():
    """
    Gas gain in transformation processes of coal(Coke oven, Blust furnace,...) (Own elaboration from IEA balances)
    """
    return _ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes(time())


_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "ratio_gain_gas_vs_losses_solids_in_tranformation_processes",
    None,
    {},
    _root,
    {},
    "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
)


@component.add(
    name='"Share pipeline transport FECg+l in 2015"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
)
def share_pipeline_transport_fecgl_in_2015():
    """
    Share of energy dedicated for pipeline transport vs final energy consumption of gases and liquids.
    """
    return _sampleiftrue_share_pipeline_transport_fecgl_in_2015()


_sampleiftrue_share_pipeline_transport_fecgl_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_pipeline_transport(),
    lambda: historic_share_pipeline_transport(),
    "_sampleiftrue_share_pipeline_transport_fecgl_in_2015",
)


@component.add(
    name="Total distribution losses",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_distribution_losses():
    """
    Total energy distribution losses.
    """
    return (
        electrical_distribution_losses_ej()
        + heatcom_distribution_losses()
        + heatnc_distribution_losses()
        + pipeline_transport()
        + sum(
            energy_distr_losses_ff_ej().rename({"final sources": "final sources!"}),
            dim=["final sources!"],
        )
    )


@component.add(
    name="Transformation FF losses EJ",
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
)
def transformation_ff_losses_ej():
    """
    Losses in transformation processes of each fossil fuel
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = float(
        pes_fossil_fuel_extraction_delayed().loc["liquids"]
    ) * float(historic_share_of_transformation_losses_vs_extraction().loc["liquids"])
    value.loc[{"final sources": ["solids"]}] = float(
        pes_fossil_fuel_extraction_delayed().loc["solids"]
    ) * float(historic_share_of_transformation_losses_vs_extraction().loc["solids"])
    value.loc[{"final sources": ["electricity"]}] = 0
    value.loc[{"final sources": ["gases"]}] = (
        float(pes_fossil_fuel_extraction_delayed().loc["solids"])
        * float(historic_share_of_transformation_losses_vs_extraction().loc["solids"])
        * ratio_gain_gas_vs_lose_solids_in_tranf_processes()
    )
    value.loc[{"final sources": ["heat"]}] = 0
    return value
