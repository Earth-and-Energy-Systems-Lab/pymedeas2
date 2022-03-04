"""
Module total_outputs_from_demand
Translated using PySD version 2.2.1
"""


def activate_elf_by_scen():
    """
    Real Name: "activate ELF by scen?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Active/deactivate the energy loss function by scenario: 1: activate 0: not active
    """
    return _ext_constant_activate_elf_by_scen()


_ext_constant_activate_elf_by_scen = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "activate_ELF",
    {},
    _root,
    "_ext_constant_activate_elf_by_scen",
)


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


def annual_gdp_growth_rate_aut():
    """
    Real Name: Annual GDP growth rate AUT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual GDP growth rate.
    """
    return -1 + zidz(gdp_aut(), gdp_delayed_1yr())


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
    return 1 - share_e_losses_cc_world()


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


@subs(["sectors"], _subscript_dict)
def domestic_demand_by_sector():
    """
    Real Name: Domestic demand by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    EU28 total final demand by sector
    """
    return demand_by_sector_fd_adjusted()


@subs(["final sources"], _subscript_dict)
def energy_scarcity_feedback_shortage_coeff_aut():
    """
    Real Name: Energy scarcity feedback shortage coeff AUT
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
def final_energy_intensity_by_sector_and_fuel_eu():
    """
    Real Name: Final energy intensity by sector and fuel EU
    Original Eqn:
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Evolution of final energy intensity by sector and fuel.
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


def gdp_aut():
    """
    Real Name: GDP AUT
    Original Eqn:
    Units: T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global GDP in T1995T$.
    """
    return (
        sum(gdp_by_sector().rename({"sectors": "sectors!"}), dim=["sectors!"])
        / 1000000.0
    )


@subs(["sectors"], _subscript_dict)
def gdp_by_sector():
    """
    Real Name: GDP by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Gross Domestic Product by sector
    """
    return real_final_demand_by_sector_aut() + ic_total_exports() - ic_total_imports()


@subs(["sectors"], _subscript_dict)
def gdp_by_sector_delayed_1yr():
    """
    Real Name: GDP by sector delayed 1yr
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors']


    """
    return _delayfixed_gdp_by_sector_delayed_1yr()


_delayfixed_gdp_by_sector_delayed_1yr = DelayFixed(
    lambda: gdp_by_sector(),
    lambda: 1,
    lambda: gdp_by_sector(),
    time_step,
    "_delayfixed_gdp_by_sector_delayed_1yr",
)


@subs(["sectors"], _subscript_dict)
def gdp_by_sector_growth_rate():
    """
    Real Name: GDP by sector growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return -1 + zidz(gdp_by_sector(), gdp_by_sector_delayed_1yr())


def gdp_delayed_1yr():
    """
    Real Name: GDP delayed 1yr
    Original Eqn:
    Units: Tdollars/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp_aut(), lambda: 1, lambda: 0.22, time_step, "_delayfixed_gdp_delayed_1yr"
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
    return gdp_aut() * dollars_to_tdollars() / population()


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
        real_final_demand_by_sector_aut().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_delayed_aut():
    """
    Real Name: Real demand by sector delayed AUT
    Original Eqn:
    Units: $
    Limits: (None, None)
    Type: Stateful
    Subs: ['sectors']


    """
    return _delayfixed_real_demand_by_sector_delayed_aut()


_delayfixed_real_demand_by_sector_delayed_aut = DelayFixed(
    lambda: real_final_demand_by_sector_aut(),
    lambda: 1,
    lambda: xr.DataArray(10, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    time_step,
    "_delayfixed_real_demand_by_sector_delayed_aut",
)


def real_demand_delayed_1yr():
    """
    Real Name: Real demand delayed 1yr
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _smooth_real_demand_delayed_1yr()


_smooth_real_demand_delayed_1yr = Smooth(
    lambda: real_demand_tdollars(),
    lambda: 1,
    lambda: 0.2,
    lambda: 12,
    "_smooth_real_demand_delayed_1yr",
)


def real_demand_tdollars():
    """
    Real Name: Real demand Tdollars
    Original Eqn:
    Units: Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return real_demand() / 1000000.0


@subs(["sectors"], _subscript_dict)
def real_domestic_demand_by_sector_aut():
    """
    Real Name: Real domestic demand by sector AUT
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total real domestic (without exports) final demand of EU28 products (after energy-economy feedback).
    """
    return np.maximum(
        0,
        sum(
            ia_matrix_domestic().rename({"sectors1": "sectors1!"})
            * (
                xr.DataArray(
                    0,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "sectors1!": _subscript_dict["sectors1"],
                    },
                    ["sectors", "sectors1!"],
                )
                + real_total_output_by_sector_aut().rename({"sectors": "sectors1!"})
            ),
            dim=["sectors1!"],
        ),
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

    Real final energy consumption by fuel after accounting for energy availability. test2+0*Total FE Elec consumption EJ
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = total_fe_elec_consumption_ej()
    value.loc[{"final sources": ["heat"]}] = total_fe_heat_consumption_ej()
    value.loc[{"final sources": ["liquids"]}] = real_fe_consumption_liquids_ej()
    value.loc[{"final sources": ["solids"]}] = real_fe_consumption_solids_ej()
    value.loc[{"final sources": ["gases"]}] = real_fe_consumption_gases_ej()
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


@subs(["final sources"], _subscript_dict)
def real_fec_before_heat_dem_corr():
    """
    Real Name: Real FEC before heat dem corr
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Real energy consumption by final fuel before heat demand correction.
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


@subs(["sectors"], _subscript_dict)
def real_final_demand_by_sector_aut():
    """
    Real Name: Real final demand by sector AUT
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Sectoral final demand of EU28 products (domestic and foreign).
    """
    return np.maximum(
        0, real_domestic_demand_by_sector_aut() + real_final_demand_of_exports()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_aut():
    """
    Real Name: Real final energy by sector and fuel AUT
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Real final energy to be used by economic sectors and fuel after accounting for energy scarcity and CC impacts.
    """
    return (
        required_final_energy_by_sector_and_fuel_aut()
        * (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + energy_scarcity_feedback_shortage_coeff_aut()
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

    Real total final energy consumption (not including non-energy uses).
    """
    return sum(
        real_fe_consumption_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


def real_tfec_before_heat_dem_corr():
    """
    Real Name: Real TFEC before heat dem corr
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real total final energy consumption (not including non-energy uses) before heat demand correction
    """
    return sum(
        real_fec_before_heat_dem_corr().rename({"final sources": "final sources!"}),
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
        real_total_output_by_sector_aut().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
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
            real_final_energy_by_sector_and_fuel_aut(),
            final_energy_intensity_by_sector_and_fuel_eu(),
            (
                xr.DataArray(
                    0,
                    {
                        "final sources": _subscript_dict["final sources"],
                        "sectors": _subscript_dict["sectors"],
                    },
                    ["final sources", "sectors"],
                )
                + total_output_required_by_sector() / 1000000.0
            ),
        )
        * 1000000.0
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_aut():
    """
    Real Name: Real total output by sector AUT
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

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
        required_final_energy_by_sector_and_fuel_aut().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@subs(["final sources", "sectors"], _subscript_dict)
def required_final_energy_by_sector_and_fuel_aut():
    """
    Real Name: Required final energy by sector and fuel AUT
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
            + total_output_required_by_sector()
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
            + final_energy_intensity_by_sector_and_fuel_eu()
        )
        / 1000000.0
    )


def share_e_losses_cc_world():
    """
    Real Name: share E losses CC world
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        activate_elf_by_scen() == 1, lambda: share_e_losses_cc(), lambda: 0
    )


@subs(["final sources"], _subscript_dict)
def shortage_coef_without_min_without_elosses():
    """
    Real Name: "Shortage coef without MIN without E-losses"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    ***Variable to test the consistency of the modeling. IT CAN NEVER BE > 1! (that would mean consumption > demand.***
    """
    return zidz(
        real_fe_consumption_by_fuel_before_heat_correction(),
        required_fed_by_fuel_before_heat_correction(),
    )


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_by_sector():
    """
    Real Name: Total domestic output required by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Required total EU28 output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix_domestic().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + domestic_demand_by_sector().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def total_output_required_by_sector():
    """
    Real Name: Total output required by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total output required to satisfy domestic and foreign final demand.
    """
    return (
        required_total_output_for_exports() + total_domestic_output_required_by_sector()
    )
