"""
Module energy.supply.chp_plants
Translated using PySD version 3.14.1
"""

@component.add(
    name="a reg share oil", units="1/year", comp_type="Constant", comp_subtype="Normal"
)
def a_reg_share_oil():
    return -0.002985


@component.add(
    name="efficiency Elec coal CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_elec_coal_chp_plants",
        "__data__": "_ext_data_efficiency_elec_coal_chp_plants",
        "time": 1,
    },
)
def efficiency_elec_coal_chp_plants():
    """
    Efficiency of elec in coal CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_coal_chp_plants(time())


_ext_data_efficiency_elec_coal_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_electricity_coal_chp_plants",
    None,
    {},
    _root,
    {},
    "_ext_data_efficiency_elec_coal_chp_plants",
)


@component.add(
    name="efficiency Elec gas CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_elec_gas_chp_plants",
        "__data__": "_ext_data_efficiency_elec_gas_chp_plants",
        "time": 1,
    },
)
def efficiency_elec_gas_chp_plants():
    """
    Efficiency of elec in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_gas_chp_plants(time())


_ext_data_efficiency_elec_gas_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_electricity_gas_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_elec_gas_chp_plants",
)


@component.add(
    name="efficiency Elec oil CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_elec_oil_chp_plants",
        "__data__": "_ext_data_efficiency_elec_oil_chp_plants",
        "time": 1,
    },
)
def efficiency_elec_oil_chp_plants():
    """
    Efficiency of liquids in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_elec_oil_chp_plants(time())


_ext_data_efficiency_elec_oil_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_electricity_liquids_chp_plants",
    None,
    {},
    _root,
    {},
    "_ext_data_efficiency_elec_oil_chp_plants",
)


@component.add(
    name="efficiency Heat coal CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_heat_coal_chp_plants",
        "__data__": "_ext_data_efficiency_heat_coal_chp_plants",
        "time": 1,
    },
)
def efficiency_heat_coal_chp_plants():
    """
    Efficiency of heat in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_coal_chp_plants(time())


_ext_data_efficiency_heat_coal_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_heat_coal_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_heat_coal_chp_plants",
)


@component.add(
    name="efficiency Heat gas CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_heat_gas_chp_plants",
        "__data__": "_ext_data_efficiency_heat_gas_chp_plants",
        "time": 1,
    },
)
def efficiency_heat_gas_chp_plants():
    """
    Efficiency of heat in gas CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_gas_chp_plants(time())


_ext_data_efficiency_heat_gas_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_heat_gas_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_heat_gas_chp_plants",
)


@component.add(
    name="efficiency Heat oil CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_heat_oil_chp_plants",
        "__data__": "_ext_data_efficiency_heat_oil_chp_plants",
        "time": 1,
    },
)
def efficiency_heat_oil_chp_plants():
    """
    Efficiency of heat in oil CHP plants. We assume constant last data IEA.
    """
    return _ext_data_efficiency_heat_oil_chp_plants(time())


_ext_data_efficiency_heat_oil_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_efficiency_heat_liquids_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_heat_oil_chp_plants",
)


@component.add(
    name="FED heat coal CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_fossil_fuels_chp_plants_ej": 1, "share_chp_plants_coal": 1},
)
def fed_heat_coal_chp_plants_ej():
    """
    Final energy demand of coal to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * share_chp_plants_coal()


@component.add(
    name="FED heat fossil fuels CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_by_nre_chp_plants_ej": 1,
        "fes_heatcom_nuclear_chp_plants_ej": 1,
    },
)
def fed_heat_fossil_fuels_chp_plants_ej():
    """
    Final energy demand of fossil fuels in CHP plants.
    """
    return np.maximum(
        fed_heatcom_by_nre_chp_plants_ej() - fes_heatcom_nuclear_chp_plants_ej(), 0
    )


@component.add(
    name="FED heat gas CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_fossil_fuels_chp_plants_ej": 1, "share_chp_plants_gas": 1},
)
def fed_heat_gas_chp_plants_ej():
    """
    Final energy demand of gas to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * share_chp_plants_gas()


@component.add(
    name="FED heat liquids CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_fossil_fuels_chp_plants_ej": 1, "share_chp_plants_oil": 1},
)
def fed_heat_liquids_chp_plants_ej():
    """
    Final energy demand of oil to produce heat in CHP plants.
    """
    return fed_heat_fossil_fuels_chp_plants_ej() * share_chp_plants_oil()


@component.add(
    name='"FED heat-com by NRE CHP plants EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation": 1,
        "fed_heatcom_nre_ej": 1,
    },
)
def fed_heatcom_by_nre_chp_plants_ej():
    """
    Final energy demand of commercial heat in CHP plants without RES.
    """
    return (
        share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation()
        * fed_heatcom_nre_ej()
    )


@component.add(
    name="FES Elec fossil fuel CHP plants EJ",
    units="EJ/year",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fe_gen_elec_fossil_fuel_chp_plants_ej": 1},
)
def fes_elec_fossil_fuel_chp_plants_ej():
    """
    Final Energy supply of electricity from fossil fuels in CHP plants. We assign priority to it due to its better efficiency.
    """
    return potential_fe_gen_elec_fossil_fuel_chp_plants_ej()


@component.add(
    name='"FES heat-com fossil fuels CHP plants EJ"',
    units="EJ/year",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heat_fossil_fuels_chp_plants_ej": 3,
        "share_chp_plants_coal": 2,
        "scarcity_final_fuels_delayed": 3,
        "share_chp_plants_oil": 2,
    },
)
def fes_heatcom_fossil_fuels_chp_plants_ej():
    """
    Final Energy supply of heat from fossil fuels in CHP plants. We assign priority to it due to its better efficiency.
    """
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["coal"]] = (
        fed_heat_fossil_fuels_chp_plants_ej()
        * share_chp_plants_coal()
        * (1 - float(scarcity_final_fuels_delayed().loc["solids"]))
    )
    value.loc[["natural gas"]] = (
        fed_heat_fossil_fuels_chp_plants_ej()
        * (1 - share_chp_plants_oil() - share_chp_plants_coal())
        * (1 - float(scarcity_final_fuels_delayed().loc["gases"]))
    )
    value.loc[["oil"]] = (
        fed_heat_fossil_fuels_chp_plants_ej()
        * share_chp_plants_oil()
        * (1 - float(scarcity_final_fuels_delayed().loc["liquids"]))
    )
    return value


@component.add(
    name='"FES Heat-com nuclear CHP plants EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fes_heatcom_nuclear_chp_plants_ej": 1,
        "fed_heatcom_nre_ej": 1,
    },
)
def fes_heatcom_nuclear_chp_plants_ej():
    """
    Commercial heat produced in cogeration nuclear plants.
    """
    return np.minimum(
        potential_fes_heatcom_nuclear_chp_plants_ej(), fed_heatcom_nre_ej()
    )


@component.add(
    name="Gen losses demand for CHP plants EJ",
    units="EJ/year",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gas_for_chp_plants_ej": 1,
        "efficiency_elec_gas_chp_plants": 1,
        "efficiency_heat_gas_chp_plants": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "efficiency_elec_oil_chp_plants": 1,
        "efficiency_heat_oil_chp_plants": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "efficiency_heat_coal_chp_plants": 1,
        "efficiency_elec_coal_chp_plants": 1,
    },
)
def gen_losses_demand_for_chp_plants_ej():
    """
    Total generation losses associated to CHP plants.
    """
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["natural gas"]] = ped_gas_for_chp_plants_ej() * (
        1 - efficiency_elec_gas_chp_plants() - efficiency_heat_gas_chp_plants()
    )
    value.loc[["oil"]] = ped_oil_for_chp_plants_ej() * (
        1 - efficiency_elec_oil_chp_plants() - efficiency_heat_oil_chp_plants()
    )
    value.loc[["coal"]] = ped_coal_for_chp_plants_ej() * (
        1 - efficiency_heat_coal_chp_plants() - efficiency_elec_coal_chp_plants()
    )
    return value


@component.add(
    name="historic share CHP plants coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_share_chp_plants_gas": 1, "historic_share_chp_plants_oil": 1},
)
def historic_share_chp_plants_coal():
    return 1 - historic_share_chp_plants_gas() - historic_share_chp_plants_oil()


@component.add(
    name="historic share CHP plants gas",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_chp_plants_gas",
        "__data__": "_ext_data_historic_share_chp_plants_gas",
        "time": 1,
    },
)
def historic_share_chp_plants_gas():
    """
    Historic share of natural gas for electricity in relation to the total fossil fuels for CHP plants
    """
    return _ext_data_historic_share_chp_plants_gas(time())


_ext_data_historic_share_chp_plants_gas = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_chp_plants_gas",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_share_chp_plants_gas",
)


@component.add(
    name="historic share CHP plants oil",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_chp_plants_oil",
        "__data__": "_ext_data_historic_share_chp_plants_oil",
        "time": 1,
    },
)
def historic_share_chp_plants_oil():
    """
    historic share CHP plants oil
    """
    return _ext_data_historic_share_chp_plants_oil(time())


_ext_data_historic_share_chp_plants_oil = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_chp_plants_oil",
    None,
    {},
    _root,
    {},
    "_ext_data_historic_share_chp_plants_oil",
)


@component.add(
    name="PED coal for CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_coal_chp_plants_ej": 1, "efficiency_heat_coal_chp_plants": 1},
)
def ped_coal_for_chp_plants_ej():
    """
    Primary energy demand of coal (EJ) for CHP plants.
    """
    return zidz(fed_heat_coal_chp_plants_ej(), efficiency_heat_coal_chp_plants())


@component.add(
    name="PED gas for CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heat_gas_chp_plants_ej": 1, "efficiency_heat_gas_chp_plants": 1},
)
def ped_gas_for_chp_plants_ej():
    """
    Primary energy demand of gas (EJ) for CHP plants.
    """
    return fed_heat_gas_chp_plants_ej() / efficiency_heat_gas_chp_plants()


@component.add(
    name="PED oil for CHP plants EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heat_liquids_chp_plants_ej": 1,
        "efficiency_heat_oil_chp_plants": 1,
    },
)
def ped_oil_for_chp_plants_ej():
    """
    Primary energy demand of oil (EJ) for CHP plants.COMMENT: FACTOR 10 TO REVIEW
    """
    return fed_heat_liquids_chp_plants_ej() / efficiency_heat_oil_chp_plants()


@component.add(
    name="Potential FE gen Elec fossil fuel CHP plants EJ",
    units="EJ/year",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_chp_plants_ej": 1,
        "efficiency_elec_coal_chp_plants": 1,
        "efficiency_elec_gas_chp_plants": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "efficiency_elec_oil_chp_plants": 1,
    },
)
def potential_fe_gen_elec_fossil_fuel_chp_plants_ej():
    """
    Potential electricity generation from CHP plants burning fossil fuels.
    """
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["coal"]] = (
        ped_coal_for_chp_plants_ej() * efficiency_elec_coal_chp_plants()
    )
    value.loc[["natural gas"]] = (
        ped_gas_for_chp_plants_ej() * efficiency_elec_gas_chp_plants()
    )
    value.loc[["oil"]] = ped_oil_for_chp_plants_ej() * efficiency_elec_oil_chp_plants()
    return value


@component.add(
    name='"Potential FES Heat-com nuclear CHP plants EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_nuclear_elec_generation_twh": 1,
        "share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation": 1,
        "ej_per_twh": 1,
    },
)
def potential_fes_heatcom_nuclear_chp_plants_ej():
    """
    Potential commercial heat to be produced in cogeration nuclear plants.
    """
    return (
        fe_nuclear_elec_generation_twh()
        * share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation()
        * ej_per_twh()
    )


@component.add(
    name="scarcity final fuels delayed",
    units="Dmnl",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_scarcity_final_fuels_delayed": 1},
    other_deps={
        "_delayfixed_scarcity_final_fuels_delayed": {
            "initial": {"time_step": 1},
            "step": {"scarcity_final_fuels": 1},
        }
    },
)
def scarcity_final_fuels_delayed():
    return _delayfixed_scarcity_final_fuels_delayed()


_delayfixed_scarcity_final_fuels_delayed = DelayFixed(
    lambda: scarcity_final_fuels(),
    lambda: time_step(),
    lambda: xr.DataArray(
        0, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    ),
    time_step,
    "_delayfixed_scarcity_final_fuels_delayed",
)


@component.add(
    name="share CHP plants coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_share_chp_plants_coal": 1,
        "share_chp_plants_oil": 1,
        "share_chp_plants_gas": 1,
    },
)
def share_chp_plants_coal():
    """
    Coal is assumed to cover the rest of the CHP plants demand after RES, nuclear, oil and gas.It is supposed that the share of coal is not going to grow in the future.
    """
    return np.minimum(
        historic_share_chp_plants_coal(),
        1 - share_chp_plants_gas() - share_chp_plants_oil(),
    )


@component.add(
    name="share CHP plants gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_share_chp_plants_coal": 1, "share_chp_plants_oil": 1},
)
def share_chp_plants_gas():
    return 1 - historic_share_chp_plants_coal() - share_chp_plants_oil()


@component.add(
    name="share CHP plants oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_share_chp_plants_gas": 1,
        "a_reg_share_oil": 1,
        "historic_share_chp_plants_oil": 1,
    },
)
def share_chp_plants_oil():
    """
    Oil share of heat demand. Since this share has been falling globally since the first oil shock, and given the difficulties to substitute oil in other sectors (e.g. Transportation) and that there are many more resources that can supply heat, we assume an exogenous linear decreasing trend for the oil share of heat demand to reach 0% around 2025.
    """
    return np.maximum(
        if_then_else(
            time() > 2014,
            lambda: np.minimum(
                1 - historic_share_chp_plants_gas(),
                a_reg_share_oil() * time() + 6.04554,
            ),
            lambda: historic_share_chp_plants_oil(),
        ),
        0,
    )


@component.add(
    name="share efficiency FF for elec in CHP plants",
    units="Dmnl",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_elec_oil_chp_plants": 2,
        "efficiency_heat_oil_chp_plants": 1,
        "efficiency_heat_coal_chp_plants": 1,
        "efficiency_elec_coal_chp_plants": 2,
        "efficiency_elec_gas_chp_plants": 2,
        "efficiency_heat_gas_chp_plants": 1,
    },
)
def share_efficiency_ff_for_elec_in_chp_plants():
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["oil"]] = zidz(
        efficiency_elec_oil_chp_plants(),
        efficiency_elec_oil_chp_plants() + efficiency_heat_oil_chp_plants(),
    )
    value.loc[["coal"]] = zidz(
        efficiency_elec_coal_chp_plants(),
        efficiency_elec_coal_chp_plants() + efficiency_heat_coal_chp_plants(),
    )
    value.loc[["natural gas"]] = zidz(
        efficiency_elec_gas_chp_plants(),
        efficiency_elec_gas_chp_plants() + efficiency_heat_gas_chp_plants(),
    )
    return value


@component.add(
    name="share Elec gen in CHP",
    units="Dmnl",
    subscripts=["fossil fuels"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fe_gen_elec_fossil_fuel_chp_plants_ej": 6,
        "fed_heat_gas_chp_plants_ej": 1,
        "fed_heat_coal_chp_plants_ej": 1,
        "fed_heat_liquids_chp_plants_ej": 1,
    },
)
def share_elec_gen_in_chp():
    value = xr.DataArray(
        np.nan, {"fossil fuels": _subscript_dict["fossil fuels"]}, ["fossil fuels"]
    )
    value.loc[["natural gas"]] = zidz(
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["natural gas"]),
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["natural gas"])
        + fed_heat_gas_chp_plants_ej(),
    )
    value.loc[["coal"]] = zidz(
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["coal"]),
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["coal"])
        + fed_heat_coal_chp_plants_ej(),
    )
    value.loc[["oil"]] = zidz(
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["oil"]),
        float(potential_fe_gen_elec_fossil_fuel_chp_plants_ej().loc["oil"])
        + fed_heat_liquids_chp_plants_ej(),
    )
    return value


@component.add(
    name='"Share heat-com CHP plants NRE vs NRE tot heat-com generation"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation",
        "__data__": "_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation",
        "time": 1,
    },
)
def share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation():
    """
    Share of commercial heat produced in CHP plants from non-renewable energies vs. total commercial heat generation from NRE.
    """
    return _ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation(time())


_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_share_commercial_heat_in_chp_on_total_commercial_heat_generation",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_heatcom_chp_plants_nre_vs_nre_tot_heatcom_generation",
)


@component.add(
    name="share of heat production in CHP plants vs total nucelar elec generation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation"
    },
)
def share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation():
    """
    Share of heat production in CHP plants vs total nucelar elec generation.
    """
    return (
        _ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation()
    )


_ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "share_heat_output_vs_electricity_in_nuclear",
    {},
    _root,
    {},
    "_ext_constant_share_of_heat_production_in_chp_plants_vs_total_nucelar_elec_generation",
)
