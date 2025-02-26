"""
Module energy.demand.heat_demand
Translated using PySD version 3.14.2
"""

@component.add(
    name='"FED_Heat-com_after_priorities"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_heatcom_ej": 1,
        "fes_heatcom_from_waste": 1,
        "fes_heatcom_from_biogas_ej": 1,
    },
)
def fed_heatcom_after_priorities():
    """
    Total commercial heat demand including distribution losses after technologies with priority in the mix (waste and biogas).
    """
    return float(
        np.maximum(
            0,
            total_fed_heatcom_ej()
            - fes_heatcom_from_waste()
            - fes_heatcom_from_biogas_ej(),
        )
    )


@component.add(
    name='"FED_Heat-com_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def fed_heatcom_ej():
    """
    Final energy demand heat commercial.
    """
    return float(required_fed_by_fuel_before_heat_correction().loc["heat"])


@component.add(
    name='"FED_Heat-com_NRE"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_after_priorities": 1,
        "total_fe_real_supply_res_for_heatcom": 1,
    },
)
def fed_heatcom_nre():
    """
    Demand of non renewable energy to produce commercial Heat (final energy). We give priority to RES.
    """
    return float(
        np.maximum(
            fed_heatcom_after_priorities() - total_fe_real_supply_res_for_heatcom(), 0
        )
    )


@component.add(
    name='"FED_Heat-com_plants_fossil_fuels_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_nre": 1,
        "fes_heatcom_fossil_fuels_chp_plants": 1,
        "fes_heatcom_nuclear_chp_plants": 1,
    },
)
def fed_heatcom_plants_fossil_fuels_ej():
    """
    Demand of fossil fuels for commercial heat plants. Fossil fuels CHP plants have priority due a better efficiency.
    """
    return float(
        np.maximum(
            fed_heatcom_nre()
            - fes_heatcom_fossil_fuels_chp_plants()
            - fes_heatcom_nuclear_chp_plants(),
            0,
        )
    )


@component.add(
    name='"FED_Heat-nc_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel": 1,
        "required_fed_by_fuel_before_heat_correction": 1,
    },
)
def fed_heatnc_ej():
    """
    Final energy (non-commercial) heat demand.
    """
    return float(required_fed_by_fuel().loc["heat"]) - float(
        required_fed_by_fuel_before_heat_correction().loc["heat"]
    )


@component.add(
    name='"Heat-com_distribution_losses"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatcom_ej": 1, "share_heat_distribution_losses": 1},
)
def heatcom_distribution_losses():
    """
    Distribution losses associated to heat commercial.
    """
    return fed_heatcom_ej() * share_heat_distribution_losses()


@component.add(
    name='"Heat-nc_distribution_losses"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "fed_heatnc_ej": 1},
)
def heatnc_distribution_losses():
    """
    Distribution losses associated to non-commercial heat.
    """
    return total_fed_heatnc_ej() - fed_heatnc_ej()


@component.add(
    name='"PED_FF_Heat-nc"',
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fed_nre_heatnc": 3,
        "share_fed_coal_vs_nre_heatnc": 1,
        "efficiency_coal_for_heat_plants": 1,
        "efficiency_gases_for_heat_plants": 1,
        "share_fed_gas_vs_nre_heatnc": 1,
        "share_fed_liquids_vs_nre_heatnc": 1,
        "efficiency_liquids_for_heat_plants": 1,
    },
)
def ped_ff_heatnc():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = (
        total_fed_nre_heatnc()
        * share_fed_coal_vs_nre_heatnc()
        / efficiency_coal_for_heat_plants()
    )
    value.loc[["gases"]] = (
        total_fed_nre_heatnc()
        * share_fed_gas_vs_nre_heatnc()
        / efficiency_gases_for_heat_plants()
    )
    value.loc[["liquids"]] = (
        total_fed_nre_heatnc()
        * share_fed_liquids_vs_nre_heatnc()
        / efficiency_liquids_for_heat_plants()
    )
    return value


@component.add(
    name='"Share_FED_heat-com_vs_total_heat"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatcom_ej": 2, "total_fed_heat": 1},
)
def share_fed_heatcom_vs_total_heat():
    """
    Share of commercial heat in relation to total final energy use for heat.
    """
    return total_fed_heatcom_ej() / (total_fed_heat() + total_fed_heatcom_ej())


@component.add(
    name="Share_heat_distribution_losses",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_heat_distribution_losses"},
)
def share_heat_distribution_losses():
    """
    Current share of heat transmission and distribution losses in relation to heat consumption. We define these losses at around 6.5% following historical data of IEA database.
    """
    return _ext_constant_share_heat_distribution_losses()


_ext_constant_share_heat_distribution_losses = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "share_heat_distribution_losses",
    {},
    _root,
    {},
    "_ext_constant_share_heat_distribution_losses",
)


@component.add(
    name='"Total_FE_real_supply_RES_for_heat-com"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatcom_ej": 1},
)
def total_fe_real_supply_res_for_heatcom():
    """
    Total final energy supply delivered by RES for commercial heat.
    """
    return sum(
        fe_real_generation_res_heatcom_ej().rename({"RES_heat": "RES_heat!"}),
        dim=["RES_heat!"],
    )


@component.add(
    name='"Total_FE_real_supply_RES_for_heat-nc_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatnc": 1},
)
def total_fe_real_supply_res_for_heatnc_ej():
    """
    Total final energy supply delivered by RES for non-commercial heat.
    """
    return sum(
        fe_real_generation_res_heatnc().rename({"RES_heat": "RES_heat!"}),
        dim=["RES_heat!"],
    )


@component.add(
    name="Total_FED_Heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatcom_ej": 1, "total_fed_heatnc_ej": 1},
)
def total_fed_heat():
    """
    Total final energy demand (including distribution losses) of heat.
    """
    return total_fed_heatcom_ej() + total_fed_heatnc_ej()


@component.add(
    name='"Total_FED_Heat-com_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatcom_ej": 1, "share_heat_distribution_losses": 1},
)
def total_fed_heatcom_ej():
    """
    Total commercial heat demand including distribution losses.
    """
    return fed_heatcom_ej() * (1 + share_heat_distribution_losses())


@component.add(
    name='"Total_FED_Heat-nc_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fed_heatnc_ej": 1, "share_heat_distribution_losses": 1},
)
def total_fed_heatnc_ej():
    """
    Total non-commercial heat demand including distribution losses (and climate change impacts).
    """
    return fed_heatnc_ej() * (1 + share_heat_distribution_losses())


@component.add(
    name='"Total_FED_NRE_Heat-nc"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "total_fe_real_supply_res_for_heatnc_ej": 1},
)
def total_fed_nre_heatnc():
    """
    Final energy demand heat non-commercial to be covered by NRE (including distribution losses and climate change impacts).
    """
    return float(
        np.maximum(0, total_fed_heatnc_ej() - total_fe_real_supply_res_for_heatnc_ej())
    )
