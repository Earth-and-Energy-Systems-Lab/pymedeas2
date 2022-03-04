"""
Module losses_in_transformation_and_distri
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def energy_distr_losses_ff_ej():
    """
    Real Name: Energy distr losses FF EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary, Constant
    Subs: ['final sources']

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


def fec_gasesliquids():
    """
    Real Name: "FEC gases+liquids"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return float(real_fe_consumption_by_fuel().loc["gases"]) + float(
        real_fe_consumption_by_fuel().loc["liquids"]
    )


def historic_pipeline_transport(x):
    """
    Real Name: Historic pipeline transport
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic pipeline transport
    """
    return _ext_lookup_historic_pipeline_transport(x)


_ext_lookup_historic_pipeline_transport = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_pipeline_transport",
    {},
    _root,
    "_ext_lookup_historic_pipeline_transport",
)


@subs(["final sources"], _subscript_dict)
def historic_share_of_losses_vs_extraction():
    """
    Real Name: Historic share of losses vs extraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: ['final sources']

    Historic share losses of each fossil fuel vs annual extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_losses_vs_extraction(time())


_ext_data_historic_share_of_losses_vs_extraction = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    "_ext_data_historic_share_of_losses_vs_extraction",
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_gases",
    None,
    {"final sources": ["gases"]},
)


@subs(["final sources"], _subscript_dict)
def historic_share_of_transformation_losses_vs_extraction():
    """
    Real Name: Historic share of transformation losses vs extraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: ['final sources']

    Historic share transformation losses of each fossil fuel vs annual extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_transformation_losses_vs_extraction(time())


_ext_data_historic_share_of_transformation_losses_vs_extraction = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    "_ext_data_historic_share_of_transformation_losses_vs_extraction",
)

_ext_data_historic_share_of_transformation_losses_vs_extraction.add(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)


def historic_share_pipeline_transport():
    """
    Real Name: Historic share pipeline transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic share of energy for pipeline transport vs TFEC of liquids and gases.
    """
    return if_then_else(
        time() < 2016,
        lambda: zidz(historic_pipeline_transport(time()), fec_gasesliquids()),
        lambda: 0,
    )


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction():
    """
    Real Name: PES fossil fuel extraction
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Annual extraction of fossil fuels
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = (
        pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej()
    )
    value.loc[{"final sources": ["solids"]}] = (
        extraction_coal_ej_aut() + imports_aut_coal_from_row_ej()
    )
    value.loc[{"final sources": ["gases"]}] = (
        pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej()
    )
    return value


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction_delayed():
    """
    Real Name: PES fossil fuel extraction delayed
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']

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
    lambda: xr.DataArray(0.5, {"final sources": ["liquids"]}, ["final sources"]),
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
    lambda: xr.DataArray(0.12, {"final sources": ["solids"]}, ["final sources"]),
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
    lambda: xr.DataArray(0.3, {"final sources": ["gases"]}, ["final sources"]),
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed_2",
)


def pipeline_transport():
    """
    Real Name: Pipeline transport
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Pipeline transport. IEA definition: Pipeline transport includes energy used in the support and operation of pipelines transporting gases, liquids, slurries and other commodities, including the energy used for pump stations and maintenance of the pipeline.
    """
    return share_pipeline_transport_fecgl_in_2015() * fec_gasesliquids()


def ratio_gain_gas_vs_lose_solids_in_tranf_processes():
    """
    Real Name: Ratio gain gas vs lose solids in tranf processes
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []

    Gas gain in transformation processes of coal(Coke oven, Blust furnace,...) (Own elaboration from IEA balances)
    """
    return _ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes(time())


_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "ratio_gain_gas_vs_losses_solids_in_tranformation_processes",
    None,
    {},
    _root,
    "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
)


def share_pipeline_transport_fecgl_in_2015():
    """
    Real Name: "Share pipeline transport FECg+l in 2015"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Share of energy dedicated for pipeline transport vs final energy consumption of gases and liquids.
    """
    return _sampleiftrue_share_pipeline_transport_fecgl_in_2015()


_sampleiftrue_share_pipeline_transport_fecgl_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_pipeline_transport(),
    lambda: historic_share_pipeline_transport(),
    "_sampleiftrue_share_pipeline_transport_fecgl_in_2015",
)


def total_distribution_losses():
    """
    Real Name: Total distribution losses
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


@subs(["final sources"], _subscript_dict)
def transformation_ff_losses_ej():
    """
    Real Name: Transformation FF losses EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary, Constant
    Subs: ['final sources']

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
