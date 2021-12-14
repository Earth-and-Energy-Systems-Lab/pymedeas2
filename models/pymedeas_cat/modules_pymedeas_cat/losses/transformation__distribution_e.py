"""
Module transformation__distribution_e
Translated using PySD version 2.1.0
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
    Units: EJ
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


def fec_gasesliquids():
    """
    Real Name: "FEC gases+liquids"
    Original Eqn: real FE consumption by fuel[gases]+real FE consumption by fuel[liquids]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(real_fe_consumption_by_fuel().loc["gases"]) + float(
        real_fe_consumption_by_fuel().loc["liquids"]
    )


def historic_pipeline_transport(x):
    """
    Real Name: Historic pipeline transport
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_pipeline_transport')
    Units: EJ
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic pipeline transport
    """
    return _ext_lookup_historic_pipeline_transport(x)


@subs(["final sources"], _subscript_dict)
def historic_share_of_losses_vs_extraction():
    """
    Real Name: Historic share of losses vs extraction
    Original Eqn:
      GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_losses_over_total_extraction_liquids')
      GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_losses_over_total_extraction_solids')
      GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_losses_over_total_extraction_gases')
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
      GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_of_transformation_losses_over_total_extraction_liquids')
      GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_share_of_transformation_losses_over_total_extraction_solids')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['final sources']

    Historic share transformation losses of each fossil fuel vs annual
        extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_transformation_losses_vs_extraction(time())


def historic_share_pipeline_transport():
    """
    Real Name: Historic share pipeline transport
    Original Eqn: IF THEN ELSE(Time<2016, ZIDZ(Historic pipeline transport(Time), "FEC gases+liquids" ), 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic share of energy for pipeline transport vs TFEC of liquids and
        gases.
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
      PES total oil EJ AUT+imports AUT total oil from RoW EJ
      extraction coal EJ AUT+imports AUT coal from RoW EJ
      "PES nat. gas AUT"+"imports AUT nat. gas from RoW EJ"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Annual extraction of fossil fuels
    """
    return xrmerge(
        rearrange(
            pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            extraction_coal_ej_aut() + imports_aut_coal_from_row_ej(),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        rearrange(
            pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def pes_fossil_fuel_extraction_delayed():
    """
    Real Name: PES fossil fuel extraction delayed
    Original Eqn:
      DELAY FIXED ( PES fossil fuel extraction[liquids], TIME STEP, 0.5)
      DELAY FIXED ( PES fossil fuel extraction[solids], TIME STEP, 0.12)
      DELAY FIXED ( PES fossil fuel extraction[gases], TIME STEP, 0.3)
    Units: EJ/Year
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


def pipeline_transport():
    """
    Real Name: Pipeline transport
    Original Eqn: "Share pipeline transport FECg+l in 2015"*"FEC gases+liquids"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Pipeline transport. IEA definition: Pipeline transport includes energy
        used in the support and operation of pipelines transporting gases,
        liquids, slurries and other commodities, including the energy used for
        pump stations and maintenance of the pipeline.
    """
    return share_pipeline_transport_fecgl_in_2015() * fec_gasesliquids()


def ratio_gain_gas_vs_lose_solids_in_tranf_processes():
    """
    Real Name: Ratio gain gas vs lose solids in tranf processes
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Austria', 'time_historic_data', 'ratio_gain_gas_vs_losses_solids_in_tranformation_processes')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Gas gain in transformation processes of coal(Coke oven, Blust furnace,...)
        (Own elaboration from IEA balances)
    """
    return _ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes(time())


def share_pipeline_transport_fecgl_in_2015():
    """
    Real Name: "Share pipeline transport FECg+l in 2015"
    Original Eqn: SAMPLE IF TRUE(Time<2015, Historic share pipeline transport, Historic share pipeline transport )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of energy dedicated for pipeline transport vs final energy
        consumption of gases and liquids.
    """
    return _sample_if_true_share_pipeline_transport_fecgl_in_2015()


def total_distribution_losses():
    """
    Real Name: Total distribution losses
    Original Eqn: Electrical distribution losses EJ+"Heat-com distribution losses" +"Heat-nc distribution losses" +Pipeline transport+SUM(Energy distr losses FF EJ[final sources!])
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total energy distribution losses.
    """
    return (
        electrical_distribution_losses_ej()
        + heatcom_distribution_losses()
        + heatnc_distribution_losses()
        + pipeline_transport()
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
    Units: EJ
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


_ext_lookup_historic_pipeline_transport = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_pipeline_transport",
    {},
    _root,
    "_ext_lookup_historic_pipeline_transport",
)


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


_delayfixed_pes_fossil_fuel_extraction_delayed = DelayFixed(
    lambda: float(pes_fossil_fuel_extraction().loc["liquids"]),
    lambda: time_step(),
    lambda: 0.5,
    time_step,
    "_delayfixed_pes_fossil_fuel_extraction_delayed",
)


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


_sample_if_true_share_pipeline_transport_fecgl_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_pipeline_transport(),
    lambda: historic_share_pipeline_transport(),
    "_sample_if_true_share_pipeline_transport_fecgl_in_2015",
)
