"""
Module transformation_and_distribution
Translated using PySD version 2.2.0
"""


@subs(["final sources"], _subscript_dict)
def energy_distr_losses_ff_ej():
    """
    Real Name: Energy distr losses FF EJ
    Original Eqn:
      PES fossil fuel extraction delayed[liquids]*Historic share of losses vs extraction[liquids]
      PES fossil fuel extraction delayed[solids]*Historic share of losses vs extraction[solids]
      PES fossil fuel extraction delayed[gases]*Historic share of losses vs extraction[gases]
      0
      0
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Energy distribution losses of fossil fuels.
    """
    return xrmerge(
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["liquids"])
            * float(historic_share_of_losses_vs_extraction().loc["liquids"]),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["solids"])
            * float(historic_share_of_losses_vs_extraction().loc["solids"]),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["gases"])
            * float(historic_share_of_losses_vs_extraction().loc["gases"]),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        xr.DataArray(0, {"final sources": ["electricity"]}, ["final sources"]),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
    )


@subs(["final sources"], _subscript_dict)
def historic_share_of_losses_vs_extraction():
    """
    Real Name: Historic share of losses vs extraction
    Original Eqn:
      GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_share_losses_over_total_extraction_liquids')
      GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_share_losses_over_total_extraction_solids')
      GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_share_losses_over_total_extraction_gases')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['final sources']

    Historic share losses of each fossil fuel vs annual extraction. (Own
        elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_losses_vs_extraction(time())


@subs(["final sources"], _subscript_dict)
def historic_share_of_transformation_losses_vs_extraction():
    """
    Real Name: Historic share of transformation losses vs extraction
    Original Eqn:
      GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_share_of_transformation_losses_over_total_extraction_liquids')
      GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'historic_share_of_transformation_losses_over_total_extraction_solids')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['final sources']

    Historic share transformation losses of each fossil fuel vs annual
        extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_transformation_losses_vs_extraction(time())


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction():
    """
    Real Name: PES fossil fuel extraction
    Original Eqn:
      PES oil EJ
      extraction coal EJ
      PES nat gas
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Annual extraction of fossil fuels
    """
    return xrmerge(
        rearrange(pes_oil_ej(), ["final sources"], {"final sources": ["liquids"]}),
        rearrange(
            extraction_coal_ej(), ["final sources"], {"final sources": ["solids"]}
        ),
        rearrange(pes_nat_gas(), ["final sources"], {"final sources": ["gases"]}),
    )


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction_delayed():
    """
    Real Name: PES fossil fuel extraction delayed
    Original Eqn:
      DELAY FIXED ( PES fossil fuel extraction[liquids], TIME STEP, 139)
      DELAY FIXED ( PES fossil fuel extraction[solids], TIME STEP, 101)
      DELAY FIXED ( PES fossil fuel extraction[gases], TIME STEP, 79)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Annual extraction of fossil fuels delayed
    """
    return xrmerge(
        rearrange(
            _delayfixed_pes_fossil_fuel_extraction_delayed(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            _delayfixed_pes_fossil_fuel_extraction_delayed(),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        rearrange(
            _delayfixed_pes_fossil_fuel_extraction_delayed(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
    )


def pipeline_transport_constant_26_ej_in_2014():
    """
    Real Name: "pipeline transport constant 2.6 EJ in 2014"
    Original Eqn: 2.6
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Pipeline transport in 2014 (Ref: IEA balances).
    """
    return 2.6


def ratio_gain_gas_vs_lose_solids_in_tranf_processes():
    """
    Real Name: Ratio gain gas vs lose solids in tranf processes
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'World', 'time_historic_data', 'ratio_gain_gas_vs_losses_solids_in_tranformation_processes')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Gas gain in transformation processes of coal(Coke oven, Blust furnace,...)
        (Own elaboration from IEA balances)
    """
    return _ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes(time())


def total_distribution_losses():
    """
    Real Name: Total distribution losses
    Original Eqn: Electrical distribution losses EJ+"Heat-com distribution losses" +"Heat-nc distribution losses" +"pipeline transport constant 2.6 EJ in 2014"+SUM(Energy distr losses FF EJ[ final sources!])
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total energy distribution losses.
    """
    return (
        electrical_distribution_losses_ej()
        + heatcom_distribution_losses()
        + heatnc_distribution_losses()
        + pipeline_transport_constant_26_ej_in_2014()
        + sum(energy_distr_losses_ff_ej(), dim=("final sources",))
    )


@subs(["final sources"], _subscript_dict)
def transformation_ff_losses_ej():
    """
    Real Name: Transformation FF losses EJ
    Original Eqn:
      PES fossil fuel extraction delayed[liquids]*Historic share of transformation losses vs extraction[liquids]
      PES fossil fuel extraction delayed[solids]*Historic share of transformation losses vs extraction[solids]
      0
      PES fossil fuel extraction delayed[solids]*Historic share of transformation losses vs extraction[solids]*Ratio gain gas vs lose solids in tranf processes
      0
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Losses in transformation processes of each fossil fuel
    """
    return xrmerge(
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["liquids"])
            * float(
                historic_share_of_transformation_losses_vs_extraction().loc["liquids"]
            ),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["solids"])
            * float(
                historic_share_of_transformation_losses_vs_extraction().loc["solids"]
            ),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        xr.DataArray(0, {"final sources": ["electricity"]}, ["final sources"]),
        rearrange(
            float(pes_fossil_fuel_extraction_delayed().loc["solids"])
            * float(
                historic_share_of_transformation_losses_vs_extraction().loc["solids"]
            )
            * ratio_gain_gas_vs_lose_solids_in_tranf_processes(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
    )


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


_delayfixed_pes_fossil_fuel_extraction_delayed = DelayFixed(
    lambda: float(pes_fossil_fuel_extraction().loc["liquids"]),
    lambda: time_step(),
    lambda: 139,
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed",
)


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
