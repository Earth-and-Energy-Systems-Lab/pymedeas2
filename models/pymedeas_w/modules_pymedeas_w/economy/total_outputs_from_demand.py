"""
Module economy.total_outputs_from_demand
Translated using PySD version 3.14.2
"""

@component.add(
    name='"Activate_energy_scarcity_feedback?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def activate_energy_scarcity_feedback():
    """
    0- NOT activated 1- ACTIVATED
    """
    return 1


@component.add(
    name="Annual_GDP_growth_rate",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp": 1, "gdp_delayed_1yr": 1, "nvs_1_year": 1},
)
def annual_gdp_growth_rate():
    """
    Annual GDP growth rate.
    """
    return -1 + zidz(gdp(), gdp_delayed_1yr()) / nvs_1_year()


@component.add(
    name="CC_impacts_feedback_shortage_coeff",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_e_losses_cc": 1},
)
def cc_impacts_feedback_shortage_coeff():
    """
    This coefficient adapts the real final energy by fuel to be used by economic sectors taking into account climate change impacts.
    """
    return 1 + share_e_losses_cc()


@component.add(
    name="Demand_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1},
)
def demand_by_sector():
    return demand_by_sector_fd_adjusted()


@component.add(
    name="dollars_to_Tdollars",
    units="$/T$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dollars_to_tdollars():
    """
    Conversion from dollars to Tdollars (1 T$ = 1e12 $).
    """
    return 1000000000000.0


@component.add(
    name="Energy_scarcity_feedback_shortage_coeff",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_energy_scarcity_feedback": 1,
        "real_fe_consumption_by_fuel_before_heat_correction": 1,
        "required_fed_by_fuel_before_heat_correction": 1,
    },
)
def energy_scarcity_feedback_shortage_coeff():
    """
    MIN(1, real FE consumption by fuel before heat correction[final sources]/Required FED by fuel before heat correction [final sources]) This coefficient adapts the real final energy by fuel to be used by economic sectors taking into account energy availability.
    """
    return if_then_else(
        activate_energy_scarcity_feedback() == 1,
        lambda: np.minimum(
            1,
            zidz(
                real_fe_consumption_by_fuel_before_heat_correction(),
                required_fed_by_fuel_before_heat_correction(),
            ),
        ),
        lambda: xr.DataArray(
            1, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )


@component.add(
    name="Final_energy_intensity_by_sector_and_fuel",
    units="EJ/Tdollars",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_by_sector_and_fuel": 1},
)
def final_energy_intensity_by_sector_and_fuel():
    """
    Evolution of final energy intensity by sector and fuel. (1+("Activate EROI tot FC feedback through intensities?"*EROI FC tot from 2015*1-1)): to test method of EROI feedback through the variation of energy intensities. "EROI FC tot from 2015*1", ese "*1" si aumento el factor a por ejemplo 2 entonces se ve el efecto de que se reduce el GDP progresivamente.
    """
    return evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final_sources", "sectors"
    )


@component.add(
    name="GDP",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand": 1, "m_to_t": 1},
)
def gdp():
    """
    Global GDP in T1995T$.
    """
    return real_demand() * m_to_t()


@component.add(
    name="GDP_delayed_1yr",
    units="Tdollars",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_gdp_delayed_1yr": 1},
    other_deps={"_delayfixed_gdp_delayed_1yr": {"initial": {}, "step": {"gdp": 1}}},
)
def gdp_delayed_1yr():
    """
    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp(), lambda: 1, lambda: 29.16, time_step, "_delayfixed_gdp_delayed_1yr"
)


@component.add(
    name="GDPpc",
    units="$/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp": 1, "dollars_to_tdollars": 1, "population": 1},
)
def gdppc():
    """
    GDP per capita (1995T$ per capita).
    """
    return gdp() * dollars_to_tdollars() / population()


@component.add(
    name="M$_to_T$", units="T$/M$", comp_type="Constant", comp_subtype="Normal"
)
def m_to_t():
    return 1e-06


@component.add(
    name="Real_demand",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_by_sector": 1},
)
def real_demand():
    """
    Total demand
    """
    return sum(
        real_demand_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="Real_demand_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1, "real_total_output_by_sector": 1},
)
def real_demand_by_sector():
    """
    Real demand by sector (35 WIOD sectors). US$1995
    """
    return np.maximum(
        0,
        sum(
            ia_matrix().rename({"sectors1": "sectors1!"})
            * real_total_output_by_sector().rename({"sectors": "sectors1!"}),
            dim=["sectors1!"],
        ),
    )


@component.add(
    name="Real_demand_by_sector_delayed",
    units="M$",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_demand_by_sector_delayed": 1},
    other_deps={
        "_delayfixed_real_demand_by_sector_delayed": {
            "initial": {},
            "step": {"real_demand_by_sector": 1},
        }
    },
)
def real_demand_by_sector_delayed():
    return _delayfixed_real_demand_by_sector_delayed()


_delayfixed_real_demand_by_sector_delayed = DelayFixed(
    lambda: real_demand_by_sector(),
    lambda: 1,
    lambda: xr.DataArray(10, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    time_step,
    "_delayfixed_real_demand_by_sector_delayed",
)


@component.add(
    name="real_FE_consumption_by_fuel",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_consumption_twh": 1,
        "ej_per_twh": 1,
        "share_heat_distribution_losses": 1,
        "total_fe_heat_generation": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "share_gases_for_final_energy": 1,
        "other_gases_required": 1,
        "pes_gases": 1,
        "other_liquids_required_ej": 1,
        "share_liquids_for_final_energy": 1,
        "pes_liquids": 1,
        "pe_traditional_biomass_ej_delayed": 1,
        "other_solids_required": 1,
        "solid_bioe_supply": 1,
        "pes_waste_for_tfc": 1,
        "extraction_coal_ej": 1,
        "share_solids_for_final_energy": 1,
        "ped_coal_for_ctl_ej": 1,
        "pes_peat": 1,
        "losses_in_charcoal_plants_historic": 1,
    },
)
def real_fe_consumption_by_fuel():
    """
    Real final energy consumption by fuel after accounting for energy availability.
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = total_fe_elec_consumption_twh() * ej_per_twh()
    value.loc[["heat"]] = total_fe_heat_generation() / (
        1 + share_heat_distribution_losses()
    )
    value.loc[["gases"]] = (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()
    value.loc[["liquids"]] = float(
        np.maximum(
            (pes_liquids() - other_liquids_required_ej())
            * share_liquids_for_final_energy(),
            0,
        )
    )
    value.loc[["solids"]] = (
        extraction_coal_ej()
        + (pe_traditional_biomass_ej_delayed() + pes_peat() + solid_bioe_supply())
        - losses_in_charcoal_plants_historic()
        - ped_coal_for_ctl_ej()
        - other_solids_required()
    ) * share_solids_for_final_energy() + pes_waste_for_tfc()
    return value


@component.add(
    name="real_FE_consumption_by_fuel_before_heat_correction",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_fe_consumption_by_fuel": 5,
        "ratio_fed_for_heatnc_vs_fed_for_heatcom": 1,
        "share_feh_over_fed_by_final_fuel": 3,
    },
)
def real_fe_consumption_by_fuel_before_heat_correction():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = float(real_fe_consumption_by_fuel().loc["electricity"])
    value.loc[["heat"]] = float(real_fe_consumption_by_fuel().loc["heat"]) / (
        1 + ratio_fed_for_heatnc_vs_fed_for_heatcom()
    )
    value.loc[["liquids"]] = float(real_fe_consumption_by_fuel().loc["liquids"]) / (
        1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"])
    )
    value.loc[["gases"]] = float(real_fe_consumption_by_fuel().loc["gases"]) / (
        1 - float(share_feh_over_fed_by_final_fuel().loc["gases"])
    )
    value.loc[["solids"]] = float(real_fe_consumption_by_fuel().loc["solids"]) / (
        1 - float(share_feh_over_fed_by_final_fuel().loc["solids"])
    )
    return value


@component.add(
    name="Real_final_energy_by_sector_and_fuel",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel": 3,
        "energy_scarcity_feedback_shortage_coeff": 3,
        "ej_per_twh": 3,
        "ccs_energy_consumption_sector": 1,
        "dac_energy_consumption_by_sector_and_fuel": 2,
    },
)
def real_final_energy_by_sector_and_fuel():
    """
    Real final energy to be used by economic sectors and fuel after accounting for energy scarcity and CC impacts.
    """
    value = xr.DataArray(
        np.nan,
        {
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac_final_sources"], :] = False
    value.values[except_subs.values] = (
        required_final_energy_by_sector_and_fuel()
        * energy_scarcity_feedback_shortage_coeff()
    ).values[except_subs.values]
    value.loc[["electricity"], :] = (
        (
            required_final_energy_by_sector_and_fuel()
            .loc["electricity", :]
            .reset_coords(drop=True)
            * float(energy_scarcity_feedback_shortage_coeff().loc["electricity"])
            - ccs_energy_consumption_sector()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
            - dac_energy_consumption_by_sector_and_fuel()
            .loc["electricity", _subscript_dict["sectors"]]
            .reset_coords(drop=True)
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
        )
        .expand_dims({"dac_final_sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = (
        (
            required_final_energy_by_sector_and_fuel()
            .loc["heat", :]
            .reset_coords(drop=True)
            * float(energy_scarcity_feedback_shortage_coeff().loc["heat"])
            - dac_energy_consumption_by_sector_and_fuel()
            .loc["heat", _subscript_dict["sectors"]]
            .reset_coords(drop=True)
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
        )
        .expand_dims({"dac_final_sources": ["heat"]}, 0)
        .values
    )
    return value


@component.add(
    name="Real_TFEC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1},
)
def real_tfec():
    """
    Real total final energy consumption.
    """
    return sum(
        real_fe_consumption_by_fuel().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="real_TFEC_before_heat_corr",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel_before_heat_correction": 1},
)
def real_tfec_before_heat_corr():
    return sum(
        real_fe_consumption_by_fuel_before_heat_correction().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name="Real_total_output",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_sector": 1},
)
def real_total_output():
    """
    Total output (1995$).
    """
    return sum(
        real_total_output_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="Real_total_output_by_fuel_and_sector",
    units="Mdollars",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel": 1,
        "nvs_1_year": 1,
        "final_energy_intensity_by_sector_and_fuel": 1,
        "required_total_output_by_sector": 1,
        "m_to_t": 2,
    },
)
def real_total_output_by_fuel_and_sector():
    """
    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel() * nvs_1_year(),
            final_energy_intensity_by_sector_and_fuel(),
            (required_total_output_by_sector() * m_to_t()).expand_dims(
                {"final_sources": _subscript_dict["final_sources"]}, 0
            ),
        )
        / m_to_t()
    )


@component.add(
    name="Real_total_output_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_fuel_and_sector": 1},
)
def real_total_output_by_sector():
    """
    Real total output by sector (14 WIOD sectors). US$1995. We assume the most limiting resources.
    """
    return sum(
        real_total_output_by_fuel_and_sector().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    ) / len(
        xr.DataArray(
            np.arange(1, len(_subscript_dict["final_sources"]) + 1),
            {"final_sources": _subscript_dict["final_sources"]},
            ["final_sources"],
        )
    )


@component.add(
    name="Required_FED_by_fuel",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel_before_heat_correction": 5,
        "ratio_fed_for_heatnc_vs_fed_for_heatcom": 1,
        "share_feh_over_fed_by_final_fuel": 3,
    },
)
def required_fed_by_fuel():
    """
    Required final energy demand by fuel after heat demand correction.
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = float(
        required_fed_by_fuel_before_heat_correction().loc["electricity"]
    )
    value.loc[["heat"]] = float(
        required_fed_by_fuel_before_heat_correction().loc["heat"]
    ) * (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom())
    value.loc[["liquids"]] = float(
        required_fed_by_fuel_before_heat_correction().loc["liquids"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"]))
    value.loc[["gases"]] = float(
        required_fed_by_fuel_before_heat_correction().loc["gases"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"]))
    value.loc[["solids"]] = float(
        required_fed_by_fuel_before_heat_correction().loc["solids"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"]))
    return value


@component.add(
    name="Required_FED_by_fuel_before_heat_correction",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_sectors_by_fuel": 1, "households_final_energy_demand": 1},
)
def required_fed_by_fuel_before_heat_correction():
    """
    Required final energy demand by fuel before heat demand correction. The final energy demand is modified with the feedback from the change of the EROEI.
    """
    return required_fed_sectors_by_fuel() + households_final_energy_demand()


@component.add(
    name="required_FED_by_sector",
    units="EJ/year",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel": 1,
        "households_final_energy_demand": 1,
    },
)
def required_fed_by_sector():
    value = xr.DataArray(
        np.nan,
        {"SECTORS_and_HOUSEHOLDS": _subscript_dict["SECTORS_and_HOUSEHOLDS"]},
        ["SECTORS_and_HOUSEHOLDS"],
    )
    value.loc[_subscript_dict["sectors"]] = sum(
        required_final_energy_by_sector_and_fuel().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    ).values
    value.loc[["Households"]] = sum(
        households_final_energy_demand().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )
    return value


@component.add(
    name="required_FED_sectors_by_fuel",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel": 1,
        "cc_impacts_feedback_shortage_coeff": 1,
    },
)
def required_fed_sectors_by_fuel():
    return (
        sum(
            required_final_energy_by_sector_and_fuel().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        * cc_impacts_feedback_shortage_coeff()
    )


@component.add(
    name="Required_final_energy_by_sector_and_fuel",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_total_output_by_sector": 3,
        "final_energy_intensity_by_sector_and_fuel": 3,
        "m_to_t": 3,
        "nvs_1_year": 3,
        "ej_per_twh": 3,
        "ccs_energy_demand_sect": 1,
        "dac_energy_demand_per_sector_and_fuel": 2,
    },
)
def required_final_energy_by_sector_and_fuel():
    """
    Required final energy by sector and fuel (35 WIOD sectors & 5 final sources). Adding the energy demand for CCS technologies
    """
    value = xr.DataArray(
        np.nan,
        {
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac_final_sources"], :] = False
    value.values[except_subs.values] = (
        (
            required_total_output_by_sector()
            * final_energy_intensity_by_sector_and_fuel().transpose(
                "sectors", "final_sources"
            )
            * m_to_t()
            / nvs_1_year()
        )
        .transpose("final_sources", "sectors")
        .values[except_subs.values]
    )
    value.loc[["electricity"], :] = (
        (
            required_total_output_by_sector()
            * final_energy_intensity_by_sector_and_fuel()
            .loc["electricity", :]
            .reset_coords(drop=True)
            * m_to_t()
            / nvs_1_year()
            + ccs_energy_demand_sect()
            .loc[_subscript_dict["sectors"]]
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
            + dac_energy_demand_per_sector_and_fuel()
            .loc["electricity", _subscript_dict["sectors"]]
            .reset_coords(drop=True)
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
        )
        .expand_dims({"dac_final_sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = (
        (
            required_total_output_by_sector()
            * final_energy_intensity_by_sector_and_fuel()
            .loc["heat", :]
            .reset_coords(drop=True)
            * m_to_t()
            / nvs_1_year()
            + dac_energy_demand_per_sector_and_fuel()
            .loc["heat", _subscript_dict["sectors"]]
            .reset_coords(drop=True)
            .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
            * ej_per_twh()
        )
        .expand_dims({"dac_final_sources": ["heat"]}, 0)
        .values
    )
    return value


@component.add(
    name="Required_total_output_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1, "demand_by_sector": 1},
)
def required_total_output_by_sector():
    """
    Required total output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix().rename({"sectors1": "sectors1!"})
        * demand_by_sector().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="share_electricity_TFEC",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1, "real_tfec_before_heat_corr": 1},
)
def share_electricity_tfec():
    """
    Share of electricity in TFEC
    """
    return (
        float(real_fe_consumption_by_fuel().loc["electricity"])
        / real_tfec_before_heat_corr()
    )


@component.add(
    name="share_FED_by_sector",
    units="1",
    subscripts=["SECTORS_and_HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_sector": 2},
)
def share_fed_by_sector():
    return required_fed_by_sector() / sum(
        required_fed_by_sector().rename(
            {"SECTORS_and_HOUSEHOLDS": "SECTORS_and_HOUSEHOLDS!"}
        ),
        dim=["SECTORS_and_HOUSEHOLDS!"],
    )


@component.add(
    name="TFEI_sectors",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_energy_intensity_by_sector_and_fuel": 1},
)
def tfei_sectors():
    """
    Total final energy intensity of the 35 WIOD sectors.
    """
    return sum(
        final_energy_intensity_by_sector_and_fuel().rename(
            {"final_sources": "final_sources!", "sectors": "sectors!"}
        ),
        dim=["final_sources!", "sectors!"],
    )


@component.add(
    name="Total_FED",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def total_fed():
    return sum(
        required_fed_by_fuel().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="total_FED_before_heat_corr",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def total_fed_before_heat_corr():
    return sum(
        required_fed_by_fuel_before_heat_correction().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )
