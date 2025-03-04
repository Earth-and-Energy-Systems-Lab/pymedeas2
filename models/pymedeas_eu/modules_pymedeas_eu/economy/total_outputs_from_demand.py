"""
Module economy.total_outputs_from_demand
Translated using PySD version 3.14.2
"""

@component.add(
    name='"activate_ELF_by_scen?"',
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
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "activate_ELF",
    {},
    _root,
    {},
    "_ext_constant_activate_elf_by_scen",
)


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
    name="Annual_GDP_growth_rate_EU",
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
    name="CC_impacts_feedback_shortage_coeff",
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
    name="Domestic_demand_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
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
    name="Energy_scarcity_feedback_shortage_coeff_EU",
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
            1, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )


@component.add(
    name="Final_energy_intensity_by_sector_and_fuel_EU",
    units="EJ/Tdollars",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_by_sector_and_fuel": 1},
)
def final_energy_intensity_by_sector_and_fuel_eu():
    """
    Evolution of final energy intensity by sector and fuel.
    """
    return evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final_sources", "sectors"
    )


@component.add(
    name="GDP_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
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
    name="GDP_delayed_1yr",
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
    name="GDP_EU",
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
        sum(gdp_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"])
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
    name="M$_to_T$", units="T$/M$", comp_type="Constant", comp_subtype="Normal"
)
def m_to_t():
    return 1e-06


@component.add(
    name="Real_demand",
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
        real_final_demand_by_sector_eu().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Real_demand_by_sector_delayed_EU",
    units="M$",
    subscripts=["sectors"],
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
    name="Real_demand_delayed_1yr",
    units="T$",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_real_demand_delayed_1yr": 1},
    other_deps={
        "_delayfixed_real_demand_delayed_1yr": {
            "initial": {},
            "step": {"real_demand_tdollars": 1},
        }
    },
)
def real_demand_delayed_1yr():
    """
    SMOOTH N(Real demand Tdollars, 1, 8.6, 12)
    """
    return _delayfixed_real_demand_delayed_1yr()


_delayfixed_real_demand_delayed_1yr = DelayFixed(
    lambda: real_demand_tdollars(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_real_demand_delayed_1yr",
)


@component.add(
    name="Real_demand_Tdollars",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand": 1, "m_to_t": 1},
)
def real_demand_tdollars():
    return real_demand() * m_to_t()


@component.add(
    name="Real_domestic_demand_by_sector_EU",
    units="Mdollars",
    subscripts=["sectors"],
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
            ia_matrix_domestic().rename({"sectors1": "sectors1!"})
            * real_total_output_by_sector_eu().rename({"sectors": "sectors1!"}),
            dim=["sectors1!"],
        ),
    )


@component.add(
    name="real_FE_consumption_by_fuel",
    units="EJ/year",
    subscripts=["final_sources"],
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
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = total_fe_elec_consumption_ej()
    value.loc[["heat"]] = total_fe_heat_consumption()
    value.loc[["liquids"]] = float(real_fe_consumption_fs().loc["liquids"])
    value.loc[["solids"]] = float(real_fe_consumption_fs().loc["solids"])
    value.loc[["gases"]] = float(real_fe_consumption_fs().loc["gases"])
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
    name="Real_FEC_before_heat_dem_corr",
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
def real_fec_before_heat_dem_corr():
    """
    Real energy consumption by final fuel before heat demand correction.
    """
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
    name="Real_final_demand_by_sector_EU",
    units="Mdollars",
    subscripts=["sectors"],
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
    name="Real_final_energy_by_sector_and_fuel_EU",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
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
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac_final_sources"], :] = False
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
                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                * ej_per_twh()
                - dac_energy_consumption_by_sector_and_fuel()
                .loc["electricity", _subscript_dict["sectors"]]
                .reset_coords(drop=True)
                .rename({"SECTORS_and_HOUSEHOLDS": "sectors"})
                * ej_per_twh()
            )
            * float(energy_scarcity_feedback_shortage_coeff_eu().loc["electricity"])
        )
        .expand_dims({"final_sources": ["electricity"]}, 0)
        .values
    )
    value.loc[["heat"], :] = (
        (
            required_final_energy_by_sector_and_fuel_eu()
            .loc["heat", :]
            .reset_coords(drop=True)
            * float(energy_scarcity_feedback_shortage_coeff_eu().loc["heat"])
        )
        .expand_dims({"final_sources": ["heat"]}, 0)
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
    Real total final energy consumption (not including non-energy uses).
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
    name="Real_TFEC_before_heat_dem_corr",
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
        real_fec_before_heat_dem_corr().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="Real_total_output",
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
        real_total_output_by_sector_eu().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Real_total_output_by_fuel_and_sector",
    units="Mdollars",
    subscripts=["final_sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel_eu": 1,
        "nvs_1_year": 1,
        "final_energy_intensity_by_sector_and_fuel_eu": 1,
        "m_to_t": 2,
        "total_output_required_by_sector": 1,
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
                {"final_sources": _subscript_dict["final_sources"]}, 0
            ),
        )
        / m_to_t()
    )


@component.add(
    name="Real_total_output_by_sector_EU",
    units="Mdollars",
    subscripts=["sectors"],
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
        "required_final_energy_by_sector_and_fuel_eu": 1,
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
        required_final_energy_by_sector_and_fuel_eu().rename(
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
    depends_on={"required_final_energy_by_sector_and_fuel_eu": 1},
)
def required_fed_sectors_by_fuel():
    return sum(
        required_final_energy_by_sector_and_fuel_eu().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Required_final_energy_by_sector_and_fuel_EU",
    units="EJ/year",
    subscripts=["final_sources", "sectors"],
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
            "final_sources": _subscript_dict["final_sources"],
            "sectors": _subscript_dict["sectors"],
        },
        ["final_sources", "sectors"],
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[_subscript_dict["dac_final_sources"], :] = False
    value.values[except_subs.values] = (
        (
            total_output_required_by_sector()
            * final_energy_intensity_by_sector_and_fuel_eu().transpose(
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
            total_output_required_by_sector()
            * final_energy_intensity_by_sector_and_fuel_eu()
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
        .expand_dims({"final_sources": ["electricity"]}, 0)
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
        .expand_dims({"final_sources": ["heat"]}, 0)
        .values
    )
    return value


@component.add(
    name="share_E_losses_CC_world",
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
    name="share_electricity_TFEC",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1, "real_tfec_before_heat_corr": 1},
)
def share_electricity_tfec():
    """
    Share of electricity in total final energy consumption
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
    name='"Shortage_coef_without_MIN_without_E-losses"',
    units="Dmnl",
    subscripts=["final_sources"],
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
    name="TFEI_sectors",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_energy_intensity_by_sector_and_fuel_eu": 1},
)
def tfei_sectors():
    return sum(
        final_energy_intensity_by_sector_and_fuel_eu().rename(
            {"final_sources": "final_sources!", "sectors": "sectors!"}
        ),
        dim=["final_sources!", "sectors!"],
    )


@component.add(
    name="Total_domestic_output_required_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_domestic": 1, "domestic_demand_by_sector": 1},
)
def total_domestic_output_required_by_sector():
    """
    Required total EU28 output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix_domestic().rename({"sectors1": "sectors1!"})
        * domestic_demand_by_sector().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
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
    name="Total_output_required_by_sector",
    units="Mdollars",
    subscripts=["sectors"],
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
