"""
Module losses_in_transformation_and_distri
Translated using PySD version 2.2.3
"""


@subs(["final sources"], _subscript_dict)
def energy_distr_losses_ff_ej():
    """
    Real Name: Energy distr losses FF EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Constant, Auxiliary
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
    "World",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    "_ext_data_historic_share_of_losses_vs_extraction",
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "World",
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
    "World",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_liquids",
    None,
    {"final sources": ["liquids"]},
    _root,
    "_ext_data_historic_share_of_transformation_losses_vs_extraction",
)

_ext_data_historic_share_of_transformation_losses_vs_extraction.add(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_of_transformation_losses_over_total_extraction_solids",
    None,
    {"final sources": ["solids"]},
)


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction():
    """
    Real Name: PES fossil fuel extraction
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Annual extraction of fossil fuels
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = pes_oil_ej()
    value.loc[{"final sources": ["solids"]}] = extraction_coal_ej()
    value.loc[{"final sources": ["gases"]}] = pes_nat_gas()
    return value


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction_delayed():
    """
    Real Name: PES fossil fuel extraction delayed
    Original Eqn:
    Units: EJ/year
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
    lambda: xr.DataArray(139, {"final sources": ["liquids"]}, ["final sources"]),
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
    lambda: xr.DataArray(101, {"final sources": ["solids"]}, ["final sources"]),
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
    lambda: xr.DataArray(79, {"final sources": ["gases"]}, ["final sources"]),
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed_2",
)


def pipeline_transport_constant_26_ej_in_2014():
    """
    Real Name: "pipeline transport constant 2.6 EJ in 2014"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Pipeline transport in 2014 (Ref: IEA balances).
    """
    return 2.6


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
    "World",
    "time_historic_data",
    "ratio_gain_gas_vs_losses_solids_in_tranformation_processes",
    None,
    {},
    _root,
    "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
)


def total_distribution_losses():
    """
    Real Name: Total distribution losses
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total energy distribution losses.
    """
    return (
        electrical_distribution_losses_ej()
        + heatcom_distribution_losses()
        + heatnc_distribution_losses()
        + pipeline_transport_constant_26_ej_in_2014()
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
    Units:
    Limits: (None, None)
    Type: Constant, Auxiliary
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
