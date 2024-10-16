"""
Module energysupplylosses_in_transformation_and_distri
Translated using PySD version 3.14.0
"""

@component.add(
    name="Energy distr losses FF EJ",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_fossil_fuel_extraction_delayed": 3,
        "historic_share_of_losses_vs_extraction": 3,
    },
)
def energy_distr_losses_ff_ej():
    """
    Energy distribution losses of fossil fuels.
    """
    value = xr.DataArray(
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["liquids"]] = float(
        pes_fossil_fuel_extraction_delayed().loc["liquids"]
    ) * float(historic_share_of_losses_vs_extraction().loc["liquids"])
    value.loc[["solids"]] = float(
        pes_fossil_fuel_extraction_delayed().loc["solids"]
    ) * float(historic_share_of_losses_vs_extraction().loc["solids"])
    value.loc[["gases"]] = float(
        pes_fossil_fuel_extraction_delayed().loc["gases"]
    ) * float(historic_share_of_losses_vs_extraction().loc["gases"])
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    return value


@component.add(
    name="Historic share of losses vs extraction",
    units="Dmnl",
    subscripts=["matter final sources"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_of_losses_vs_extraction",
        "__data__": "_ext_data_historic_share_of_losses_vs_extraction",
        "time": 1,
    },
)
def historic_share_of_losses_vs_extraction():
    """
    Historic share losses of each fossil fuel vs annual extraction. (Own elaboration from IEA balances)
    """
    return _ext_data_historic_share_of_losses_vs_extraction(time())


_ext_data_historic_share_of_losses_vs_extraction = ExtData(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_liquids",
    None,
    {"matter final sources": ["liquids"]},
    _root,
    {"matter final sources": _subscript_dict["matter final sources"]},
    "_ext_data_historic_share_of_losses_vs_extraction",
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_solids",
    None,
    {"matter final sources": ["solids"]},
)

_ext_data_historic_share_of_losses_vs_extraction.add(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_share_losses_over_total_extraction_gases",
    None,
    {"matter final sources": ["gases"]},
)


@component.add(
    name="Historic share of transformation losses vs extraction",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_of_transformation_losses_vs_extraction",
        "__data__": "_ext_data_historic_share_of_transformation_losses_vs_extraction",
        "time": 1,
    },
)
def historic_share_of_transformation_losses_vs_extraction():
    """
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
    {"final sources": _subscript_dict["final sources"]},
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


@component.add(
    name="PES fossil fuel extraction",
    units="EJ/year",
    subscripts=["matter final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_oil_ej": 1, "extraction_coal_ej": 1, "pes_nat_gas": 1},
)
def pes_fossil_fuel_extraction():
    """
    Annual extraction of fossil fuels
    """
    value = xr.DataArray(
        np.nan,
        {"matter final sources": _subscript_dict["matter final sources"]},
        ["matter final sources"],
    )
    value.loc[["liquids"]] = pes_oil_ej()
    value.loc[["solids"]] = extraction_coal_ej()
    value.loc[["gases"]] = pes_nat_gas()
    return value


@component.add(
    name="PES fossil fuel extraction delayed",
    units="EJ/year",
    subscripts=["matter final sources"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={
        "_delayfixed_pes_fossil_fuel_extraction_delayed": 1,
        "_delayfixed_pes_fossil_fuel_extraction_delayed_1": 1,
        "_delayfixed_pes_fossil_fuel_extraction_delayed_2": 1,
    },
    other_deps={
        "_delayfixed_pes_fossil_fuel_extraction_delayed": {
            "initial": {"time_step": 1},
            "step": {"pes_fossil_fuel_extraction": 1},
        },
        "_delayfixed_pes_fossil_fuel_extraction_delayed_1": {
            "initial": {"time_step": 1},
            "step": {"pes_fossil_fuel_extraction": 1},
        },
        "_delayfixed_pes_fossil_fuel_extraction_delayed_2": {
            "initial": {"time_step": 1},
            "step": {"pes_fossil_fuel_extraction": 1},
        },
    },
)
def pes_fossil_fuel_extraction_delayed():
    """
    Annual extraction of fossil fuels delayed
    """
    value = xr.DataArray(
        np.nan,
        {"matter final sources": _subscript_dict["matter final sources"]},
        ["matter final sources"],
    )
    value.loc[["liquids"]] = _delayfixed_pes_fossil_fuel_extraction_delayed().values
    value.loc[["solids"]] = _delayfixed_pes_fossil_fuel_extraction_delayed_1().values
    value.loc[["gases"]] = _delayfixed_pes_fossil_fuel_extraction_delayed_2().values
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


@component.add(
    name='"pipeline transport constant 2.6 EJ in 2014"',
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pipeline_transport_constant_26_ej_in_2014():
    """
    Pipeline transport in 2014 (Ref: IEA balances).
    """
    return 2.6


@component.add(
    name="Ratio gain gas vs lose solids in tranf processes",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
        "__data__": "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
        "time": 1,
    },
)
def ratio_gain_gas_vs_lose_solids_in_tranf_processes():
    """
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
    {},
    "_ext_data_ratio_gain_gas_vs_lose_solids_in_tranf_processes",
)


@component.add(
    name="Total distribution losses",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electrical_distribution_losses_ej": 1,
        "heatcom_distribution_losses": 1,
        "heatnc_distribution_losses": 1,
        "pipeline_transport_constant_26_ej_in_2014": 1,
        "energy_distr_losses_ff_ej": 1,
    },
)
def total_distribution_losses():
    """
    Total energy distribution losses.
    """
    return (
        electrical_distribution_losses_ej()
        + heatcom_distribution_losses()
        + heatnc_distribution_losses()
        + pipeline_transport_constant_26_ej_in_2014()
        + sum(
            energy_distr_losses_ff_ej().rename(
                {np.str_("final sources"): "final sources!"}
            ),
            dim=["final sources!"],
        )
    )


@component.add(
    name="Transformation FF losses EJ",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_fossil_fuel_extraction_delayed": 3,
        "historic_share_of_transformation_losses_vs_extraction": 3,
        "ratio_gain_gas_vs_lose_solids_in_tranf_processes": 1,
    },
)
def transformation_ff_losses_ej():
    """
    Losses in transformation processes of each fossil fuel
    """
    value = xr.DataArray(
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["liquids"]] = float(
        pes_fossil_fuel_extraction_delayed().loc["liquids"]
    ) * float(historic_share_of_transformation_losses_vs_extraction().loc["liquids"])
    value.loc[["solids"]] = float(
        pes_fossil_fuel_extraction_delayed().loc["solids"]
    ) * float(historic_share_of_transformation_losses_vs_extraction().loc["solids"])
    value.loc[["electricity"]] = 0
    value.loc[["gases"]] = (
        float(pes_fossil_fuel_extraction_delayed().loc["solids"])
        * float(historic_share_of_transformation_losses_vs_extraction().loc["solids"])
        * ratio_gain_gas_vs_lose_solids_in_tranf_processes()
    )
    value.loc[["heat"]] = 0
    return value
