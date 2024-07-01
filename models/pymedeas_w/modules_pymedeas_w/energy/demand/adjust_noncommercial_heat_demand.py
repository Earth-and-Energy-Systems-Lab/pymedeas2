"""
Module energy.demand.adjust_noncommercial_heat_demand
Translated using PySD version 3.14.0
"""

@component.add(
    name='"FED_by_fuel_for_heat-nc"',
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_oil_for_heatnc": 1,
        "fed_nat_gas_for_heatnc": 1,
        "fed_coal_for_heatnc": 1,
        "fed_solid_bioe_for_heatnc": 1,
    },
)
def fed_by_fuel_for_heatnc():
    """
    Final energy demand (excluding distribution and generation losses) of non-commercial heat by final fuel.
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = fed_oil_for_heatnc()
    value.loc[["gases"]] = fed_nat_gas_for_heatnc()
    value.loc[["solids"]] = fed_coal_for_heatnc() + fed_solid_bioe_for_heatnc()
    return value


@component.add(
    name='"FED_coal_for_heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel_before_heat_correction": 1,
        "share_feh_over_fed_solid_bioe": 1,
        "share_feh_over_fed_by_final_fuel": 1,
        "efficiency_coal_for_heat_plants": 1,
        "share_heat_distribution_losses": 1,
    },
)
def fed_coal_for_heatnc():
    """
    Final energy demand (excluding distribution and generation losses) of non-commercial heat from coal.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["solids"])
        * (
            float(share_feh_over_fed_by_final_fuel().loc["solids"])
            - share_feh_over_fed_solid_bioe()
        )
        * efficiency_coal_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


@component.add(
    name='"FED_nat._gas_for_heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel_before_heat_correction": 1,
        "share_feh_over_fed_by_final_fuel": 1,
        "efficiency_gases_for_heat_plants": 1,
        "share_heat_distribution_losses": 1,
    },
)
def fed_nat_gas_for_heatnc():
    """
    Final energy demand (excluding distribution and generation losses) of non-commercial heat from natural gas.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["gases"])
        * float(share_feh_over_fed_by_final_fuel().loc["gases"])
        * efficiency_gases_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


@component.add(
    name='"FED_NRE_for_heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_coal_for_heatnc": 1,
        "fed_nat_gas_for_heatnc": 1,
        "fed_oil_for_heatnc": 1,
    },
)
def fed_nre_for_heatnc():
    return fed_coal_for_heatnc() + fed_nat_gas_for_heatnc() + fed_oil_for_heatnc()


@component.add(
    name='"FED_oil_for_heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel_before_heat_correction": 1,
        "share_feh_over_fed_by_final_fuel": 1,
        "efficiency_liquids_for_heat_plants": 1,
        "share_heat_distribution_losses": 1,
    },
)
def fed_oil_for_heatnc():
    """
    Final energy demand (excluding distribution and generation losses) of non-commercial heat from oil.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["liquids"])
        * float(share_feh_over_fed_by_final_fuel().loc["liquids"])
        * efficiency_liquids_for_heat_plants()
        / (1 + share_heat_distribution_losses())
    )


@component.add(
    name='"FED_solid_bioE_for_heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel_before_heat_correction": 1,
        "share_feh_over_fed_solid_bioe": 1,
        "efficiency_conversion_bioe_plants_to_heat": 1,
        "share_heat_distribution_losses": 1,
    },
)
def fed_solid_bioe_for_heatnc():
    """
    Final energy demand (excluding distribution and generation losses) of non-commercial heat from solid bioenergy.
    """
    return (
        float(required_fed_by_fuel_before_heat_correction().loc["solids"])
        * share_feh_over_fed_solid_bioe()
        * efficiency_conversion_bioe_plants_to_heat()
        / (1 + share_heat_distribution_losses())
    )


@component.add(
    name='"ratio_FED_for_heat-nc_vs_FED_for_heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_by_fuel_for_heatnc": 1,
        "required_fed_by_fuel_before_heat_correction": 1,
    },
)
def ratio_fed_for_heatnc_vs_fed_for_heatcom():
    """
    Ratio FED for non-commercial heat vs FED for commercial heat (before climate change impacts).
    """
    return sum(
        fed_by_fuel_for_heatnc().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    ) * zidz(1, float(required_fed_by_fuel_before_heat_correction().loc["heat"]))


@component.add(
    name='"share_FED_coal_vs_NRE_heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_coal_for_heatnc": 1, "fed_nre_for_heatnc": 1},
)
def share_fed_coal_vs_nre_heatnc():
    """
    Share coal vs non-renewable energy sources for non-commercial heat generation.
    """
    return zidz(fed_coal_for_heatnc(), fed_nre_for_heatnc())


@component.add(
    name='"share_FED_gas_vs_NRE_heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_nat_gas_for_heatnc": 1, "fed_nre_for_heatnc": 1},
)
def share_fed_gas_vs_nre_heatnc():
    """
    Share gas vs non-renewable energy sources for non-commercial heat generation.
    """
    return zidz(fed_nat_gas_for_heatnc(), fed_nre_for_heatnc())


@component.add(
    name='"share_FED_liquids_vs_NRE_heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_oil_for_heatnc": 1, "fed_nre_for_heatnc": 1},
)
def share_fed_liquids_vs_nre_heatnc():
    """
    Share liquids vs non-renewable energy sources for non-commercial heat generation.
    """
    return zidz(fed_oil_for_heatnc(), fed_nre_for_heatnc())


@component.add(
    name="share_FEH_over_FED_by_final_fuel",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_feh_over_fed_oil": 1,
        "share_feh_over_fed_nat_gas": 1,
        "share_feh_over_fed_solid_bioe": 1,
        "share_feh_over_fed_coal": 1,
    },
)
def share_feh_over_fed_by_final_fuel():
    """
    Share FEH over FED by final fuel.
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = share_feh_over_fed_oil()
    value.loc[["gases"]] = share_feh_over_fed_nat_gas()
    value.loc[["solids"]] = share_feh_over_fed_coal() + share_feh_over_fed_solid_bioe()
    return value


@component.add(
    name="share_FEH_over_FED_coal",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_feh_over_fed_coal"},
)
def share_feh_over_fed_coal():
    """
    Estimated share of FEH over FED for coal solids (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_coal()


_ext_constant_share_feh_over_fed_coal = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_feh_over_fed_coal",
    {},
    _root,
    {},
    "_ext_constant_share_feh_over_fed_coal",
)


@component.add(
    name='"share_FEH_over_FED_nat._gas"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_feh_over_fed_nat_gas"},
)
def share_feh_over_fed_nat_gas():
    """
    Estimated share of FEH over FED for gases (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_nat_gas()


_ext_constant_share_feh_over_fed_nat_gas = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_feh_over_fed_nat_gas",
    {},
    _root,
    {},
    "_ext_constant_share_feh_over_fed_nat_gas",
)


@component.add(
    name="share_FEH_over_FED_oil",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_feh_over_fed_oil"},
)
def share_feh_over_fed_oil():
    """
    Estimated share of FEH over FED for liquids (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_oil()


_ext_constant_share_feh_over_fed_oil = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_feh_over_fed_oil",
    {},
    _root,
    {},
    "_ext_constant_share_feh_over_fed_oil",
)


@component.add(
    name="share_FEH_over_FED_solid_bioE",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_feh_over_fed_solid_bioe"},
)
def share_feh_over_fed_solid_bioe():
    """
    Estimated share of FEH over FED for solid bioenergy for the year 2011 (IEA, 2014 and own calculations).
    """
    return _ext_constant_share_feh_over_fed_solid_bioe()


_ext_constant_share_feh_over_fed_solid_bioe = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_feh_over_fed_solids_bioe",
    {},
    _root,
    {},
    "_ext_constant_share_feh_over_fed_solid_bioe",
)
