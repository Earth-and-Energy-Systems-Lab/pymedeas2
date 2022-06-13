"""
Module total_outputs_from_demand
Translated using PySD version 3.2.0
"""


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
    name="Annual GDP growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp": 1, "gdp_delayed_1yr": 1},
)
def annual_gdp_growth_rate():
    """
    Annual GDP growth rate.
    """
    return -1 + zidz(gdp(), gdp_delayed_1yr())


@component.add(
    name="CC impacts feedback shortage coeff",
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
    name="Demand by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1},
)
def demand_by_sector():
    return demand_by_sector_fd_adjusted()


@component.add(
    name="dollars to Tdollars",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dollars_to_tdollars():
    """
    Conversion from dollars to Tdollars (1 T$ = 1e12 $).
    """
    return 1000000000000.0


@component.add(
    name="Energy scarcity feedback shortage coeff",
    units="Dmnl",
    subscripts=["final sources"],
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
            1, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
        ),
    )


@component.add(
    name="Final energy intensity by sector and fuel",
    units="EJ/Tdollars",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_by_sector_and_fuel": 1},
)
def final_energy_intensity_by_sector_and_fuel():
    """
    Evolution of final energy intensity by sector and fuel. (1+("Activate EROI tot FC feedback through intensities?"*EROI FC tot from 2015*1-1)): to test method of EROI feedback through the variation of energy intensities. "EROI FC tot from 2015*1", ese "*1" si aumento el factor a por ejemplo 2 entonces se ve el efecto de que se reduce el GDP progresivamente.
    """
    return evol_final_energy_intensity_by_sector_and_fuel().transpose(
        "final sources", "sectors"
    )


@component.add(
    name="GDP",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand": 1},
)
def gdp():
    """
    Global GDP in T1995T$.
    """
    return real_demand() / 1000000.0


@component.add(
    name="GDP delayed 1yr",
    units="Tdollars/year",
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
    name="Real demand",
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
    name="Real demand by sector",
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
    name="Real demand by sector delayed",
    units="$",
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
    name="real FE consumption by fuel",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_consumption_twh": 1,
        "ej_per_twh": 1,
        "share_heat_distribution_losses": 1,
        "total_fe_heat_generation_ej": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "share_gases_for_final_energy": 1,
        "other_gases_required": 1,
        "pes_gases": 1,
        "other_liquids_required_ej": 1,
        "share_liquids_for_final_energy": 1,
        "pes_liquids_ej": 1,
        "ped_coal_for_ctl_ej": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pes_peat_ej": 1,
        "pes_waste_for_tfc": 1,
        "other_solids_required": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "share_solids_for_final_energy": 1,
        "extraction_coal_ej": 1,
    },
)
def real_fe_consumption_by_fuel():
    """
    Real final energy consumption by fuel after accounting for energy availability.
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["electricity"]] = total_fe_elec_consumption_twh() * ej_per_twh()
    value.loc[["heat"]] = total_fe_heat_generation_ej() / (
        1 + share_heat_distribution_losses()
    )
    value.loc[["gases"]] = (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()
    value.loc[["liquids"]] = (
        pes_liquids_ej() - other_liquids_required_ej()
    ) * share_liquids_for_final_energy()
    value.loc[["solids"]] = (
        extraction_coal_ej()
        + (
            pe_traditional_biomass_ej_delayed_1yr()
            + pes_waste_for_tfc()
            + pes_peat_ej()
            + losses_in_charcoal_plants_ej()
        )
        - ped_coal_for_ctl_ej()
        - other_solids_required()
    ) * share_solids_for_final_energy()
    return value


@component.add(
    name="real FE consumption by fuel before heat correction",
    units="EJ",
    subscripts=["final sources"],
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
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
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
    name="Real final energy by sector and fuel",
    units="EJ",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel": 1,
        "energy_scarcity_feedback_shortage_coeff": 1,
    },
)
def real_final_energy_by_sector_and_fuel():
    """
    Real final energy to be used by economic sectors and fuel after accounting for energy scarcity and CC impacts.
    """
    return (
        required_final_energy_by_sector_and_fuel()
        * energy_scarcity_feedback_shortage_coeff()
    )


@component.add(
    name="Real TFEC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_fe_consumption_by_fuel": 1},
)
def real_tfec():
    """
    Real total final energy consumption.
    """
    return sum(
        real_fe_consumption_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Real total output",
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
    name="Real total output by fuel and sector",
    units="Mdollars",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel": 1,
        "final_energy_intensity_by_sector_and_fuel": 1,
        "required_total_output_by_sector": 1,
    },
)
def real_total_output_by_fuel_and_sector():
    """
    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel(),
            final_energy_intensity_by_sector_and_fuel(),
            (required_total_output_by_sector() / 1000000.0).expand_dims(
                {"final sources": _subscript_dict["final sources"]}, 0
            ),
        )
        * 1000000.0
    )


@component.add(
    name="Real total output by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_fuel_and_sector": 1},
)
def real_total_output_by_sector():
    """
    Real total output by sector (35 WIOD sectors). US$1995. We assume the most limiting resources.
    """
    return vmin(
        real_total_output_by_fuel_and_sector().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@component.add(
    name="Required FED by fuel",
    units="EJ",
    subscripts=["final sources"],
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
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
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
    units="EJ",
    subscripts=["final sources"],
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
    name="required FED sectors by fuel",
    units="EJ",
    subscripts=["final sources"],
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
    name="Required final energy by sector and fuel",
    units="EJ",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_total_output_by_sector": 1,
        "final_energy_intensity_by_sector_and_fuel": 1,
    },
)
def required_final_energy_by_sector_and_fuel():
    """
    Required final energy by sector and fuel (35 WIOD sectors & 5 final sources).
    """
    return (
        required_total_output_by_sector()
        * final_energy_intensity_by_sector_and_fuel().transpose(
            "sectors", "final sources"
        )
        / 1000000.0
    ).transpose("final sources", "sectors")


@component.add(
    name="Required total output by sector",
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
    name="TFEI sectors",
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
            {"final sources": "final sources!", "sectors": "sectors!"}
        ),
        dim=["final sources!", "sectors!"],
    )
