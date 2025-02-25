"""
Module economy.total_outputs_from_demand
Translated using PySD version 3.14.0
"""

@component.add(
    name='"activate ELF by scen?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_elf_by_scen"},
)
def activate_elf_by_scen():
    """
    Active/deactivate the energy loss function by scenario: 1: activate 0: not active
    """
    return _ext_constant_activate_elf_by_scen()


_ext_constant_activate_elf_by_scen = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "activate_ELF",
    {},
    _root,
    {},
    "_ext_constant_activate_elf_by_scen",
)


@component.add(
    name='"Activate energy scarcity feedback?"',
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
    name="Annual GDP growth rate EU",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu": 1, "gdp_delayed_1yr": 1, "nvs_1_year": 1},
)
def annual_gdp_growth_rate_eu():
    """
    Annual GDP growth rate.
    """
    return -1 + zidz(gdp_eu(), gdp_delayed_1yr()) / nvs_1_year()


@component.add(
    name="CC impacts feedback shortage coeff",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_e_losses_cc_world": 1},
)
def cc_impacts_feedback_shortage_coeff():
    """
    This coefficient adapts the real final energy by fuel to be used by economic sectors taking into account climate change impacts.
    """
    return 1 - share_e_losses_cc_world()


@component.add(
    name="dollars to Tdollars",
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
    name="Domestic demand by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1},
)
def domestic_demand_by_sector():
    """
    EU28 total final demand by sector
    """
    return demand_by_sector_fd_adjusted()


@component.add(
    name="Energy scarcity feedback shortage coeff EU",
    units="Dmnl",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_energy_scarcity_feedback": 1,
        "real_fe_consumption_by_fuel_before_heat_correction": 1,
        "required_fed_by_fuel_before_heat_correction": 1,
    },
)
def energy_scarcity_feedback_shortage_coeff_eu():
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
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@component.add(
    name="Final energy intensity by sector and fuel EU",
    units="EJ/Tdollars",
    subscripts=[np.str_("final sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_by_sector_and_fuel": 1},
)
def final_energy_intensity_by_sector_and_fuel_eu():
    """
    Evolution of final energy intensity by sector and fuel.
    """
    return evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final sources", "sectors"
    )


@component.add(
    name="GDP by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_by_sector_eu": 1,
        "ic_exports_eu": 1,
        "ic_imports_eu": 1,
    },
)
def gdp_by_sector():
    """
    EU 28 Gross Domestic Product by sector
    """
    return real_final_demand_by_sector_eu() + ic_exports_eu() - ic_imports_eu()


@component.add(
    name="GDP delayed 1yr",
    units="Tdollars",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_gdp_delayed_1yr": 1},
    other_deps={"_delayfixed_gdp_delayed_1yr": {"initial": {}, "step": {"gdp_eu": 1}}},
)
def gdp_delayed_1yr():
    """
    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp_eu(), lambda: 1, lambda: 8.6, time_step, "_delayfixed_gdp_delayed_1yr"
)


@component.add(
    name="GDP EU",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_by_sector": 1, "m_to_t": 1},
)
def gdp_eu():
    """
    Global GDP in T1995T$.
    """
    return (
        sum(gdp_by_sector().rename({np.str_("sectors"): "sectors!"}), dim=["sectors!"])
        * m_to_t()
    )


@component.add(
    name="GDPpc",
    units="$/people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu": 1, "dollars_to_tdollars": 1, "population": 1},
)
def gdppc():
    """
    GDP per capita (1995T$ per capita).
    """
    return gdp_eu() * dollars_to_tdollars() / population()


@component.add(
    name="M$ to T$", units="T$/M$", comp_type="Constant", comp_subtype="Normal"
)
def m_to_t():
    return 1e-06


@component.add(
    name="Real demand",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_demand_by_sector_eu": 1},
)
def real_demand():
    """
    Total demand
    """
    return sum(
        real_final_demand_by_sector_eu().rename({np.str_("sectors"): "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Real demand by sector delayed EU",
    units="M$",
    subscripts=[np.str_("sectors")],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_demand_by_sector_delayed_eu": 1},
    other_deps={
        "_delayfixed_real_demand_by_sector_delayed_eu": {
            "initial": {},
            "step": {"real_final_demand_by_sector_eu": 1},
        }
    },
)
def real_demand_by_sector_delayed_eu():
    return _delayfixed_real_demand_by_sector_delayed_eu()


_delayfixed_real_demand_by_sector_delayed_eu = DelayFixed(
    lambda: real_final_demand_by_sector_eu(),
    lambda: 1,
    lambda: xr.DataArray(10, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    time_step,
    "_delayfixed_real_demand_by_sector_delayed_eu",
)


@component.add(
    name="Real demand delayed 1yr",
    units="T$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_real_demand_delayed_1yr": 1},
    other_deps={
        "_smooth_real_demand_delayed_1yr": {
            "initial": {},
            "step": {"real_demand_tdollars": 1},
        }
    },
)
def real_demand_delayed_1yr():
    return _smooth_real_demand_delayed_1yr()


_smooth_real_demand_delayed_1yr = Smooth(
    lambda: real_demand_tdollars(),
    lambda: 1,
    lambda: 8.6,
    lambda: 12,
    "_smooth_real_demand_delayed_1yr",
)


@component.add(
    name="Real demand Tdollars",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand": 1, "m_to_t": 1},
)
def real_demand_tdollars():
    return real_demand() * m_to_t()


@component.add(
    name="Real domestic demand by sector EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_domestic": 1, "real_total_output_by_sector_eu": 1},
)
def real_domestic_demand_by_sector_eu():
    """
    Total real domestic (without exports) final demand of EU28 products (after energy-economy feedback).
    """
    return np.maximum(
        0,
        sum(
            ia_matrix_domestic().rename({np.str_("sectors1"): "sectors1!"})
            * real_total_output_by_sector_eu().rename(
                {np.str_("sectors"): "sectors1!"}
            ),
            dim=["sectors1!"],
        ),
    )


@component.add(
    name="real FE consumption by fuel",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_consumption_ej": 1,
        "total_fe_heat_consumption": 1,
        "real_fe_consumption_fs": 3,
    },
)
def real_fe_consumption_by_fuel():
    """
    Real final energy consumption by fuel after accounting for energy availability. test2+0*Total FE Elec consumption EJ
    """
    value = xr.DataArray(
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["electricity"]] = total_fe_elec_consumption_ej()
    value.loc[["heat"]] = total_fe_heat_consumption()
    value.loc[["liquids"]] = float(real_fe_consumption_fs().loc["liquids"])
    value.loc[["solids"]] = float(real_fe_consumption_fs().loc["solids"])
    value.loc[["gases"]] = float(real_fe_consumption_fs().loc["gases"])
    return value


@component.add(
    name="real FE consumption by fuel before heat correction",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
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
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
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
    name="Real FEC before heat dem corr",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_fe_consumption_by_fuel": 5,
        "ratio_fed_for_heatnc_vs_fed_for_heatcom": 1,
        "share_feh_over_fed_by_final_fuel": 1,
        "hist_share_feh_over_fed_by_final_fuel": 2,
    },
)
def real_fec_before_heat_dem_corr():
    """
    Real energy consumption by final fuel before heat demand correction.
    """
    value = xr.DataArray(
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
    )
    value.loc[["electricity"]] = float(real_fe_consumption_by_fuel().loc["electricity"])
    value.loc[["heat"]] = float(real_fe_consumption_by_fuel().loc["heat"]) / (
        1 + ratio_fed_for_heatnc_vs_fed_for_heatcom()
    )
    value.loc[["liquids"]] = float(real_fe_consumption_by_fuel().loc["liquids"]) / (
        1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"])
    )
    value.loc[["gases"]] = float(real_fe_consumption_by_fuel().loc["gases"]) / (
        1 - float(hist_share_feh_over_fed_by_final_fuel().loc["gases"])
    )
    value.loc[["solids"]] = float(real_fe_consumption_by_fuel().loc["solids"]) / (
        1 - float(hist_share_feh_over_fed_by_final_fuel().loc["solids"])
    )
    return value


@component.add(
    name="Real final demand by sector EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_domestic_demand_by_sector_eu": 1,
        "real_final_demand_of_exports": 1,
    },
)
def real_final_demand_by_sector_eu():
    """
    Sectoral final demand of EU28 products (domestic and foreign).
    """
    return np.maximum(
        0, real_domestic_demand_by_sector_eu() + real_final_demand_of_exports()
    )


@component.add(
    name="Real final energy by sector and fuel EU",
    units="EJ/year",
    subscripts=[np.str_("final sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel_eu": 3,
        "energy_scarcity_feedback_shortage_coeff_eu": 3,
        "cc_impacts_feedback_shortage_coeff": 1,
        "dac_energy_consumption_by_sector_and_fuel": 1,
        "ccs_energy_consumption_sector": 1,
        "ej_per_twh": 2,
    },
)
def real_final_energy_by_sector_and_fuel_eu():
    """
    Real final energy to be used by economic sectors and fuel after accounting for energy scarcity and CC impacts. (Required final energy by sector and fuel EU[heat,sectors]-DAC energy consumption by sector and fuel[heat,sectors]*EJ per TWh)*Energy scarcity feedback shortage coeff EU[heat]
    """
    value = xr.DataArray(
        np.nan,
        {
            "final sources": _subscript_dict["final sources"],
            "sectors": _subscript_dict["sectors"],
        },
        [np.str_("final sources"), np.str_("sectors")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac final sources"], :] = False
    value.values[except_subs.values] = (
        required_final_energy_by_sector_and_fuel_eu()
        * energy_scarcity_feedback_shortage_coeff_eu()
        * cc_impacts_feedback_shortage_coeff()
    ).values[except_subs.values]
    value.loc[["electricity"], :] = (
        (
            (
                required_final_energy_by_sector_and_fuel_eu()
                .loc["electricity", :]
                .reset_coords(drop=True)
                - ccs_energy_consumption_sector()
                .loc[_subscript_dict["sectors"]]
                .rename({np.str_("SECTORS and HOUSEHOLDS"): "sectors"})
                * ej_per_twh()
                - dac_energy_consumption_by_sector_and_fuel()
                .loc["electricity", _subscript_dict["sectors"]]
                .reset_coords(drop=True)
                .rename({np.str_("SECTORS and HOUSEHOLDS"): "sectors"})
                * ej_per_twh()
            )
            * float(energy_scarcity_feedback_shortage_coeff_eu().loc["electricity"])
        )
        .expand_dims({"final sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = (
        (
            required_final_energy_by_sector_and_fuel_eu()
            .loc["heat", :]
            .reset_coords(drop=True)
            * float(energy_scarcity_feedback_shortage_coeff_eu().loc["heat"])
        )
        .expand_dims({"final sources": ["heat"]}, 0)
        .values
    )
    return value


@component.add(
    name="Real TFEC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1},
)
def real_tfec():
    """
    Real total final energy consumption (not including non-energy uses).
    """
    return sum(
        real_fe_consumption_by_fuel().rename(
            {np.str_("final sources"): "final sources!"}
        ),
        dim=["final sources!"],
    )


@component.add(
    name="Real TFEC before heat dem corr",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fec_before_heat_dem_corr": 1},
)
def real_tfec_before_heat_dem_corr():
    """
    Real total final energy consumption (not including non-energy uses) before heat demand correction
    """
    return sum(
        real_fec_before_heat_dem_corr().rename(
            {np.str_("final sources"): "final sources!"}
        ),
        dim=["final sources!"],
    )


@component.add(
    name="Real total output",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_sector_eu": 1},
)
def real_total_output():
    """
    Total output (1995$).
    """
    return sum(
        real_total_output_by_sector_eu().rename({np.str_("sectors"): "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Real total output by fuel and sector",
    units="Mdollars",
    subscripts=[np.str_("final sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel_eu": 1,
        "nvs_1_year": 1,
        "final_energy_intensity_by_sector_and_fuel_eu": 1,
        "total_output_required_by_sector": 1,
        "m_to_t": 2,
    },
)
def real_total_output_by_fuel_and_sector():
    """
    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel_eu() * nvs_1_year(),
            final_energy_intensity_by_sector_and_fuel_eu(),
            (total_output_required_by_sector() * m_to_t()).expand_dims(
                {"final sources": _subscript_dict["final sources"]}, 0
            ),
        )
        / m_to_t()
    )


@component.add(
    name="Real total output by sector EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_fuel_and_sector": 5},
)
def real_total_output_by_sector_eu():
    """
    Real total output by sector (35 WIOD sectors). US$1995. We assume the most limiting resources.
    """
    return np.minimum(
        real_total_output_by_fuel_and_sector()
        .loc["electricity", :]
        .reset_coords(drop=True),
        np.minimum(
            real_total_output_by_fuel_and_sector()
            .loc["heat", :]
            .reset_coords(drop=True),
            np.minimum(
                real_total_output_by_fuel_and_sector()
                .loc["liquids", :]
                .reset_coords(drop=True),
                np.minimum(
                    real_total_output_by_fuel_and_sector()
                    .loc["gases", :]
                    .reset_coords(drop=True),
                    real_total_output_by_fuel_and_sector()
                    .loc["solids", :]
                    .reset_coords(drop=True),
                ),
            ),
        ),
    )


@component.add(
    name="Required FED by fuel",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
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
        np.nan,
        {"final sources": _subscript_dict["final sources"]},
        [np.str_("final sources")],
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
    name="Required FED by fuel before heat correction",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
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
    name="required FED by sector",
    units="EJ/year",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel_eu": 1,
        "households_final_energy_demand": 1,
    },
)
def required_fed_by_sector():
    value = xr.DataArray(
        np.nan,
        {"SECTORS and HOUSEHOLDS": _subscript_dict["SECTORS and HOUSEHOLDS"]},
        [np.str_("SECTORS and HOUSEHOLDS")],
    )
    value.loc[_subscript_dict["sectors"]] = sum(
        required_final_energy_by_sector_and_fuel_eu().rename(
            {np.str_("final sources"): "final sources!"}
        ),
        dim=["final sources!"],
    ).values
    value.loc[["Households"]] = sum(
        households_final_energy_demand().rename(
            {np.str_("final sources"): "final sources!"}
        ),
        dim=["final sources!"],
    )
    return value


@component.add(
    name="required FED sectors by fuel",
    units="EJ/year",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_final_energy_by_sector_and_fuel_eu": 1},
)
def required_fed_sectors_by_fuel():
    return sum(
        required_final_energy_by_sector_and_fuel_eu().rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    )


@component.add(
    name="Required final energy by sector and fuel EU",
    units="EJ/year",
    subscripts=[np.str_("final sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_output_required_by_sector": 3,
        "final_energy_intensity_by_sector_and_fuel_eu": 3,
        "m_to_t": 3,
        "nvs_1_year": 3,
        "ccs_energy_demand_sect": 1,
        "dac_energy_demand_per_sector_and_fuel": 1,
        "ej_per_twh": 2,
    },
)
def required_final_energy_by_sector_and_fuel_eu():
    """
    Required final energy by sector and fuel (35 WIOD sectors & 5 final sources). Adding the energy demand for CCS technologies Total output required by sector[sectors]*Final energy intensity by sector and fuel EU[heat,sectors]*M$ to T$ /"1 year"+DAC energy demand per sector and fuel[heat,sectors]*EJ per TWh
    """
    value = xr.DataArray(
        np.nan,
        {
            "final sources": _subscript_dict["final sources"],
            "sectors": _subscript_dict["sectors"],
        },
        [np.str_("final sources"), np.str_("sectors")],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac final sources"], :] = False
    value.values[except_subs.values] = (
        (
            total_output_required_by_sector()
            * final_energy_intensity_by_sector_and_fuel_eu().transpose(
                "sectors", "final sources"
            )
            * m_to_t()
            / nvs_1_year()
        )
        .transpose("final sources", "sectors")
        .values[except_subs.values]
    )
    value.loc[["electricity"], :] = (
        (
            total_output_required_by_sector()
            * final_energy_intensity_by_sector_and_fuel_eu()
            .loc["electricity", :]
            .reset_coords(drop=True)
            * m_to_t()
            / nvs_1_year()
            + ccs_energy_demand_sect()
            .loc[_subscript_dict["sectors"]]
            .rename({np.str_("SECTORS and HOUSEHOLDS"): "sectors"})
            * ej_per_twh()
            + dac_energy_demand_per_sector_and_fuel()
            .loc["electricity", _subscript_dict["sectors"]]
            .reset_coords(drop=True)
            .rename({np.str_("SECTORS and HOUSEHOLDS"): "sectors"})
            * ej_per_twh()
        )
        .expand_dims({"final sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = (
        (
            total_output_required_by_sector()
            * final_energy_intensity_by_sector_and_fuel_eu()
            .loc["heat", :]
            .reset_coords(drop=True)
            * m_to_t()
            / nvs_1_year()
        )
        .expand_dims({"final sources": ["heat"]}, 0)
        .values
    )
    return value


@component.add(
    name="share E losses CC world",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"activate_elf_by_scen": 1, "share_e_losses_cc": 1},
)
def share_e_losses_cc_world():
    return if_then_else(
        activate_elf_by_scen() == 1, lambda: share_e_losses_cc(), lambda: 0
    )


@component.add(
    name="share electricity TFEC",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1, "real_tfec": 1},
)
def share_electricity_tfec():
    """
    Share of electricity in total final energy consumption
    """
    return float(real_fe_consumption_by_fuel().loc["electricity"]) / real_tfec()


@component.add(
    name="share FED by sector",
    units="1",
    subscripts=[np.str_("SECTORS and HOUSEHOLDS")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_sector": 2},
)
def share_fed_by_sector():
    return required_fed_by_sector() / sum(
        required_fed_by_sector().rename(
            {np.str_("SECTORS and HOUSEHOLDS"): "SECTORS and HOUSEHOLDS!"}
        ),
        dim=["SECTORS and HOUSEHOLDS!"],
    )


@component.add(
    name='"Shortage coef without MIN without E-losses"',
    units="Dmnl",
    subscripts=[np.str_("final sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_fe_consumption_by_fuel_before_heat_correction": 1,
        "required_fed_by_fuel_before_heat_correction": 1,
    },
)
def shortage_coef_without_min_without_elosses():
    """
    ***Variable to test the consistency of the modeling. IT CAN NEVER BE > 1! (that would mean consumption > demand.***
    """
    return (
        real_fe_consumption_by_fuel_before_heat_correction()
        / required_fed_by_fuel_before_heat_correction()
    )


@component.add(
    name="TFEI sectors",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_energy_intensity_by_sector_and_fuel_eu": 1},
)
def tfei_sectors():
    return sum(
        final_energy_intensity_by_sector_and_fuel_eu().rename(
            {np.str_("final sources"): "final sources!", np.str_("sectors"): "sectors!"}
        ),
        dim=["final sources!", "sectors!"],
    )


@component.add(
    name="Total domestic output required by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_domestic": 1, "domestic_demand_by_sector": 1},
)
def total_domestic_output_required_by_sector():
    """
    Required total EU28 output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix_domestic().rename({np.str_("sectors1"): "sectors1!"})
        * domestic_demand_by_sector().rename({np.str_("sectors"): "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Total FED",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def total_fed():
    return sum(
        required_fed_by_fuel().rename({np.str_("final sources"): "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Total output required by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_output_required_for_exports_by_sector": 1,
        "total_domestic_output_required_by_sector": 1,
    },
)
def total_output_required_by_sector():
    """
    Total output required to satisfy domestic and foreign final demand.
    """
    return (
        domestic_output_required_for_exports_by_sector()
        + total_domestic_output_required_by_sector()
    )
