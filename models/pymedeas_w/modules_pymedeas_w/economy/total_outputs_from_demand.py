"""
Module total_outputs_from_demand
Translated using PySD version 2.2.1
"""


def activate_energy_scarcity_feedback():
    """
    Real Name: "Activate energy scarcity feedback?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0- NOT activated 1- ACTIVATED
    """
    return 1


def annual_gdp_growth_rate():
    """
    Real Name: Annual GDP growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual GDP growth rate.
    """
    return -1 + zidz(gdp(), gdp_delayed_1yr())


def cc_impacts_feedback_shortage_coeff():
    """
    Real Name: CC impacts feedback shortage coeff
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    This coefficient adapts the real final energy by fuel to be used by economic sectors taking into account climate change impacts.
    """
    return 1 - share_e_losses_cc()


@subs(["sectors"], _subscript_dict)
def demand_by_sector():
    """
    Real Name: Demand by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return demand_by_sector_fd_adjusted()


def dollars_to_tdollars():
    """
    Real Name: dollars to Tdollars
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion from dollars to Tdollars (1 T$ = 1e12 $).
    """
    return 1000000000000.0


@subs(["final sources"], _subscript_dict)
def energy_scarcity_feedback_shortage_coeff():
    """
    Real Name: Energy scarcity feedback shortage coeff
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

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


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Final energy intensity by sector and fuel
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Evolution of final energy intensity by sector and fuel. (1+("Activate EROI tot FC feedback through intensities?"*EROI FC tot from 2015*1-1)): to test method of EROI feedback through the variation of energy intensities. "EROI FC tot from 2015*1", ese "*1" si aumento el factor a por ejemplo 2 entonces se ve el efecto de que se reduce el GDP progresivamente.
    """
    return (
        xr.DataArray(
            0,
            {
                "final sources": _subscript_dict["final sources"],
                "sectors": _subscript_dict["sectors"],
            },
            ["final sources", "sectors"],
        )
        + evol_final_energy_intensity_by_sector_and_fuel()
    )


def gdp():
    """
    Real Name: GDP
    Original Eqn:
    Units: T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global GDP in T1995T$.
    """
    return real_demand() / 1000000.0


def gdp_delayed_1yr():
    """
    Real Name: GDP delayed 1yr
    Original Eqn:
    Units: Tdollars/year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp(), lambda: 1, lambda: 29.16, time_step, "_delayfixed_gdp_delayed_1yr"
)


def gdppc():
    """
    Real Name: GDPpc
    Original Eqn:
    Units: $/people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    GDP per capita (1995T$ per capita).
    """
    return gdp() * dollars_to_tdollars() / population()


def real_demand():
    """
    Real Name: Real demand
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand
    """
    return sum(
        real_demand_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector():
    """
    Real Name: Real demand by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real demand by sector (35 WIOD sectors). US$1995
    """
    return np.maximum(
        0,
        sum(
            ia_matrix().rename({"sectors1": "sectors1!"})
            * (
                xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "sectors1!": _subscript_dict["sectors1"],
                    },
                    ["sectors", "sectors1!"],
                )
                + real_total_output_by_sector().rename({"sectors": "sectors1!"})
            ),
            dim=["sectors1!"],
        ),
    )


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_delayed():
    """
    Real Name: Real demand by sector delayed
    Original Eqn:
    Units: $
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors']


    """
    return _delayfixed_real_demand_by_sector_delayed()


_delayfixed_real_demand_by_sector_delayed = DelayFixed(
    lambda: real_demand_by_sector(),
    lambda: 1,
    lambda: xr.DataArray(10, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    time_step,
    "_delayfixed_real_demand_by_sector_delayed",
)


@subs(["final sources"], _subscript_dict)
def real_fe_consumption_by_fuel():
    """
    Real Name: real FE consumption by fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Real final energy consumption by fuel after accounting for energy availability.
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = (
        total_fe_elec_consumption_twh() * ej_per_twh()
    )
    value.loc[{"final sources": ["heat"]}] = total_fe_heat_generation_ej() / (
        1 + share_heat_distribution_losses()
    )
    value.loc[{"final sources": ["gases"]}] = (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()
    value.loc[{"final sources": ["liquids"]}] = (
        pes_liquids_ej() - other_liquids_required_ej()
    ) * share_liquids_for_final_energy()
    value.loc[{"final sources": ["solids"]}] = (
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


@subs(["final sources"], _subscript_dict)
def real_fe_consumption_by_fuel_before_heat_correction():
    """
    Real Name: real FE consumption by fuel before heat correction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']


    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = float(
        real_fe_consumption_by_fuel().loc["electricity"]
    )
    value.loc[{"final sources": ["heat"]}] = float(
        real_fe_consumption_by_fuel().loc["heat"]
    ) / (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom())
    value.loc[{"final sources": ["liquids"]}] = float(
        real_fe_consumption_by_fuel().loc["liquids"]
    ) / (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"]))
    value.loc[{"final sources": ["gases"]}] = float(
        real_fe_consumption_by_fuel().loc["gases"]
    ) / (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"]))
    value.loc[{"final sources": ["solids"]}] = float(
        real_fe_consumption_by_fuel().loc["solids"]
    ) / (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"]))
    return value


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel():
    """
    Real Name: Real final energy by sector and fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Real final energy to be used by economic sectors and fuel after accounting for energy scarcity and CC impacts.
    """
    return (
        required_final_energy_by_sector_and_fuel()
        * (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + energy_scarcity_feedback_shortage_coeff()
        )
        * cc_impacts_feedback_shortage_coeff()
    )


def real_tfec():
    """
    Real Name: Real TFEC
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real total final energy consumption.
    """
    return sum(
        real_fe_consumption_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


def real_total_output():
    """
    Real Name: Real total output
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total output (1995$).
    """
    return sum(
        real_total_output_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_total_output_by_fuel_and_sector():
    """
    Real Name: Real total output by fuel and sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel(),
            final_energy_intensity_by_sector_and_fuel(),
            (
                xr.DataArray(
                    0,
                    {
                        "final sources": _subscript_dict["final sources"],
                        "sectors": _subscript_dict["sectors"],
                    },
                    ["final sources", "sectors"],
                )
                + required_total_output_by_sector() / 1000000.0
            ),
        )
        * 1000000.0
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector():
    """
    Real Name: Real total output by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real total output by sector (35 WIOD sectors). US$1995. We assume the most limiting resources.
    """
    return vmin(
        real_total_output_by_fuel_and_sector().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@subs(["final sources"], _subscript_dict)
def required_fed_by_fuel():
    """
    Real Name: Required FED by fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Required final energy demand by fuel after heat demand correction.
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = float(
        required_fed_by_fuel_before_heat_correction().loc["electricity"]
    )
    value.loc[{"final sources": ["heat"]}] = float(
        required_fed_by_fuel_before_heat_correction().loc["heat"]
    ) * (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom())
    value.loc[{"final sources": ["liquids"]}] = float(
        required_fed_by_fuel_before_heat_correction().loc["liquids"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"]))
    value.loc[{"final sources": ["gases"]}] = float(
        required_fed_by_fuel_before_heat_correction().loc["gases"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"]))
    value.loc[{"final sources": ["solids"]}] = float(
        required_fed_by_fuel_before_heat_correction().loc["solids"]
    ) * (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"]))
    return value


@subs(["final sources"], _subscript_dict)
def required_fed_by_fuel_before_heat_correction():
    """
    Real Name: Required FED by fuel before heat correction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Required final energy demand by fuel before heat demand correction. The final energy demand is modified with the feedback from the change of the EROEI.
    """
    return required_fed_sectors_by_fuel() + households_final_energy_demand()


@subs(["final sources"], _subscript_dict)
def required_fed_sectors_by_fuel():
    """
    Real Name: required FED sectors by fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']


    """
    return sum(
        required_final_energy_by_sector_and_fuel().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@subs(["final sources", "sectors"], _subscript_dict)
def required_final_energy_by_sector_and_fuel():
    """
    Real Name: Required final energy by sector and fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Required final energy by sector and fuel (35 WIOD sectors & 5 final sources).
    """
    return (
        xr.DataArray(
            0,
            {
                "final sources": _subscript_dict["final sources"],
                "sectors": _subscript_dict["sectors"],
            },
            ["final sources", "sectors"],
        )
        + (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + required_total_output_by_sector()
        )
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "final sources": _subscript_dict["final sources"],
                },
                ["sectors", "final sources"],
            )
            + final_energy_intensity_by_sector_and_fuel()
        )
        / 1000000.0
    )


@subs(["sectors"], _subscript_dict)
def required_total_output_by_sector():
    """
    Real Name: Required total output by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Required total output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + demand_by_sector().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


def tfei_sectors():
    """
    Real Name: TFEI sectors
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy intensity of the 35 WIOD sectors.
    """
    return sum(
        final_energy_intensity_by_sector_and_fuel().rename(
            {"final sources": "final sources!", "sectors": "sectors!"}
        ),
        dim=["final sources!", "sectors!"],
    )
