"""
Module confrontation_demand_with_limits_eecn
Translated using PySD version 2.1.0
"""


def activate_elf_by_scen():
    """
    Real Name: "activate ELF by scen?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C119')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Active/deactivate the energy loss function by scenario:        1: activate        0: not active
    """
    return _ext_constant_activate_elf_by_scen()


def activate_energy_scarcity_feedback():
    """
    Real Name: "Activate energy scarcity feedback?"
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0- NOT activated        1- ACTIVATED
    """
    return 1


def annual_gdp_growth_rate_eu():
    """
    Real Name: Annual GDP growth rate EU
    Original Eqn: -1+ZIDZ( GDP EU, GDP delayed 1yr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual GDP growth rate.
    """
    return -1 + zidz(gdp_eu(), gdp_delayed_1yr())


def cc_impacts_feedback_shortage_coeff():
    """
    Real Name: CC impacts feedback shortage coeff
    Original Eqn: (1-share E losses CC world)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    This coefficient adapts the real final energy by fuel to be used by
        economic sectors taking into account climate change impacts.
    """
    return 1 - share_e_losses_cc_world()


def diff_annual_gdp_growth_rate():
    """
    Real Name: diff annual GDP growth rate
    Original Eqn: ZIDZ( (Annual GDP growth rate EU-Desired annual GDP growth rate ), Desired annual GDP growth rate )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Difference between the annual GDP growth rate desired and the real
        obtained.
    """
    return zidz(
        (annual_gdp_growth_rate_eu() - desired_annual_gdp_growth_rate()),
        desired_annual_gdp_growth_rate(),
    )


def dollars_to_tdollars():
    """
    Real Name: dollars to Tdollars
    Original Eqn: 1e+12
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion from dollars to Tdollars (1 T$ = 1e12 $).
    """
    return 1e12


@subs(["sectors"], _subscript_dict)
def domestic_demand_by_sector():
    """
    Real Name: Domestic demand by sector
    Original Eqn: demand by sector FD adjusted[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    EU28 total final demand by sector
    """
    return demand_by_sector_fd_adjusted()


@subs(["final sources"], _subscript_dict)
def energy_scarcity_feedback_shortage_coeff_eu():
    """
    Real Name: Energy scarcity feedback shortage coeff EU
    Original Eqn: IF THEN ELSE("Activate energy scarcity feedback?"=1, MIN(1, ZIDZ( real FE consumption by fuel before heat correction[ final sources], Required FED by fuel before heat correction[final sources] )), 1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    MIN(1, real FE consumption by fuel before heat correction[final sources]/Required
        FED by fuel before heat correction        [final sources])        This coefficient adapts the real final energy by fuel to be used by
        economic sectors taking into account energy availability.
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
        lambda: 1,
    )


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_by_sector_and_fuel_eu():
    """
    Real Name: Final energy intensity by sector and fuel EU
    Original Eqn: Evol final energy intensity by sector and fuel[sectors,final sources]
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Evolution of final energy intensity by sector and fuel.
    """
    return evol_final_energy_intensity_by_sector_and_fuel()


@subs(["sectors"], _subscript_dict)
def gdp_by_sector():
    """
    Real Name: GDP by sector
    Original Eqn: Real final demand by sector EU[sectors]+IC exports EU[sectors]-IC imports EU[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    EU 28 Gross Domestic Product by sector
    """
    return real_final_demand_by_sector_eu() + ic_exports_eu() - ic_imports_eu()


def gdp_delayed_1yr():
    """
    Real Name: GDP delayed 1yr
    Original Eqn: DELAY FIXED ( GDP EU, 1, 8.6)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


def gdp_eu():
    """
    Real Name: GDP EU
    Original Eqn: SUM(GDP by sector[sectors!])/1e+06
    Units: T$
    Limits: (None, None)
    Type: component
    Subs: None

    Global GDP in T1995T$.
    """
    return sum(gdp_by_sector(), dim=("sectors",)) / 1e06


def gdppc():
    """
    Real Name: GDPpc
    Original Eqn: GDP EU*dollars to Tdollars/Population
    Units: $/people
    Limits: (None, None)
    Type: component
    Subs: None

    GDP per capita (1995T$ per capita).
    """
    return gdp_eu() * dollars_to_tdollars() / population()


def households_total_final_energy_demand():
    """
    Real Name: Households total final energy demand
    Original Eqn: SUM(Households final energy demand[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy demand of households.
    """
    return sum(households_final_energy_demand(), dim=("final sources",))


def ratio_fed_households_vs_sectors():
    """
    Real Name: ratio FED households vs sectors
    Original Eqn: ZIDZ( Households total final energy demand, required TFED sectors )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio of final energy demand of households vs 35 WIOD sectors.
    """
    return zidz(households_total_final_energy_demand(), required_tfed_sectors())


def real_demand():
    """
    Real Name: Real demand
    Original Eqn: SUM(Real final demand by sector EU[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand
    """
    return sum(real_final_demand_by_sector_eu(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_delayed_eu():
    """
    Real Name: Real demand by sector delayed EU
    Original Eqn: DELAY FIXED ( Real final demand by sector EU[sectors], 1, 10)
    Units: $
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return _delayfixed_real_demand_by_sector_delayed_eu()


def real_demand_delayed_1yr():
    """
    Real Name: Real demand delayed 1yr
    Original Eqn: SMOOTH N(Real demand Tdollars, 1, 8.6, 12)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _smooth_real_demand_delayed_1yr()


def real_demand_tdollars():
    """
    Real Name: Real demand Tdollars
    Original Eqn: Real demand/1e+06
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_demand() / 1e06


@subs(["sectors"], _subscript_dict)
def real_domestic_demand_by_sector_eu():
    """
    Real Name: Real domestic demand by sector EU
    Original Eqn: MAX(0, SUM(IA Matrix Domestic[sectors,sectors1!]*Real total output by sector EU[sectors1!]))
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Total real domestic (without exports) final demand of EU28 products (after
        energy-economy feedback).
    """
    return np.maximum(
        0,
        sum(
            ia_matrix_domestic()
            * rearrange(
                real_total_output_by_sector_eu(), ["sectors1"], _subscript_dict
            ),
            dim=("sectors1",),
        ),
    )


@subs(["final sources"], _subscript_dict)
def real_fe_consumption_by_fuel():
    """
    Real Name: real FE consumption by fuel
    Original Eqn:
      Total FE Elec consumption EJ
      Total FE Heat consumption EJ
      real FE consumption liquids EJ
      real FE consumption solids EJ
      real FE consumption gases EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Real final energy consumption by fuel after accounting for energy availability.        test2+0*Total FE Elec consumption EJ
    """
    return xrmerge(
        rearrange(
            total_fe_elec_consumption_ej(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            total_fe_heat_consumption_ej(),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            real_fe_consumption_liquids_ej(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            real_fe_consumption_solids_ej(),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        rearrange(
            real_fe_consumption_gases_ej(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def real_fe_consumption_by_fuel_before_heat_correction():
    """
    Real Name: real FE consumption by fuel before heat correction
    Original Eqn:
      real FE consumption by fuel[electricity]
      real FE consumption by fuel[heat]/(1+"ratio FED for heat-nc vs FED for heat-com")
      real FE consumption by fuel[liquids]/(1-share FEH over FED by final fuel[liquids])
      real FE consumption by fuel[gases]/(1-share FEH over FED by final fuel[gases])
      real FE consumption by fuel[solids]/(1-share FEH over FED by final fuel[solids])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            float(real_fe_consumption_by_fuel().loc["electricity"]),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["heat"])
            / (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom()),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["liquids"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"])),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["gases"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"])),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["solids"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"])),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def real_fec_before_heat_dem_corr():
    """
    Real Name: Real FEC before heat dem corr
    Original Eqn:
      real FE consumption by fuel[electricity]
      real FE consumption by fuel[heat]/(1+"ratio FED for heat-nc vs FED for heat-com")
      real FE consumption by fuel[liquids]/(1-share FEH over FED by final fuel[liquids])
      real FE consumption by fuel[gases]/(1-share FEH over FED by final fuel[gases])
      real FE consumption by fuel[solids]/(1-share FEH over FED by final fuel[solids])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Real energy consumption by final fuel before heat demand correction.
    """
    return xrmerge(
        rearrange(
            float(real_fe_consumption_by_fuel().loc["electricity"]),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["heat"])
            / (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom()),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["liquids"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"])),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["gases"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"])),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            float(real_fe_consumption_by_fuel().loc["solids"])
            / (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"])),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


@subs(["sectors"], _subscript_dict)
def real_final_demand_by_sector_eu():
    """
    Real Name: Real final demand by sector EU
    Original Eqn: MAX(0,Real domestic demand by sector EU[sectors]+Real Final Demand of exports[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectoral final demand of EU28 products (domestic and foreign).
    """
    return np.maximum(
        0, real_domestic_demand_by_sector_eu() + real_final_demand_of_exports()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_eu():
    """
    Real Name: Real final energy by sector and fuel EU
    Original Eqn: Required final energy by sector and fuel EU[final sources,sectors]*Energy scarcity feedback shortage coeff EU[ final sources]*CC impacts feedback shortage coeff
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real final energy to be used by economic sectors and fuel after accounting
        for energy scarcity and CC impacts.
    """
    return (
        required_final_energy_by_sector_and_fuel_eu()
        * energy_scarcity_feedback_shortage_coeff_eu()
        * cc_impacts_feedback_shortage_coeff()
    )


def real_tfec():
    """
    Real Name: Real TFEC
    Original Eqn: SUM(real FE consumption by fuel[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Real total final energy consumption (not including non-energy uses).
    """
    return sum(real_fe_consumption_by_fuel(), dim=("final sources",))


def real_tfec_before_heat_dem_corr():
    """
    Real Name: Real TFEC before heat dem corr
    Original Eqn: SUM(Real FEC before heat dem corr[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Real total final energy consumption (not including non-energy uses) before
        heat demand correction
    """
    return sum(real_fec_before_heat_dem_corr(), dim=("final sources",))


def real_total_output():
    """
    Real Name: Real total output
    Original Eqn: SUM(Real total output by sector EU[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total output (1995$).
    """
    return sum(real_total_output_by_sector_eu(), dim=("sectors",))


@subs(["final sources", "sectors"], _subscript_dict)
def real_total_output_by_fuel_and_sector():
    """
    Real Name: Real total output by fuel and sector
    Original Eqn: XIDZ(Real final energy by sector and fuel EU[final sources,sectors], Final energy intensity by sector and fuel EU[ final sources,sectors], Total output required by sector[sectors]/1e+06)*1e+06
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel_eu(),
            final_energy_intensity_by_sector_and_fuel_eu(),
            total_output_required_by_sector() / 1e06,
        )
        * 1e06
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_eu():
    """
    Real Name: Real total output by sector EU
    Original Eqn: MIN(Real total output by fuel and sector[electricity,sectors], MIN(Real total output by fuel and sector[heat,sectors], MIN(Real total output by fuel and sector[liquids,sectors], MIN(Real total output by fuel and sector[gases,sectors], Real total output by fuel and sector[solids,sectors]))))
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real total output by sector (35 WIOD sectors). US$1995. We assume the most
        limiting resources.
    """
    return np.minimum(
        rearrange(
            real_total_output_by_fuel_and_sector()
            .loc["electricity", :]
            .reset_coords(drop=True),
            ["sectors"],
            _subscript_dict,
        ),
        np.minimum(
            rearrange(
                real_total_output_by_fuel_and_sector()
                .loc["heat", :]
                .reset_coords(drop=True),
                ["sectors"],
                _subscript_dict,
            ),
            np.minimum(
                rearrange(
                    real_total_output_by_fuel_and_sector()
                    .loc["liquids", :]
                    .reset_coords(drop=True),
                    ["sectors"],
                    _subscript_dict,
                ),
                np.minimum(
                    rearrange(
                        real_total_output_by_fuel_and_sector()
                        .loc["gases", :]
                        .reset_coords(drop=True),
                        ["sectors"],
                        _subscript_dict,
                    ),
                    rearrange(
                        real_total_output_by_fuel_and_sector()
                        .loc["solids", :]
                        .reset_coords(drop=True),
                        ["sectors"],
                        _subscript_dict,
                    ),
                ),
            ),
        ),
    )


@subs(["final sources"], _subscript_dict)
def required_fed_by_fuel():
    """
    Real Name: Required FED by fuel
    Original Eqn:
      Required FED by fuel before heat correction[electricity]
      Required FED by fuel before heat correction[heat]*(1+"ratio FED for heat-nc vs FED for heat-com")
      Required FED by fuel before heat correction[liquids]*(1-share FEH over FED by final fuel[liquids])
      Required FED by fuel before heat correction[gases]*(1-share FEH over FED by final fuel[gases])
      Required FED by fuel before heat correction[solids]*(1-share FEH over FED by final fuel[solids])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Required final energy demand by fuel after heat demand correction.
    """
    return xrmerge(
        rearrange(
            float(required_fed_by_fuel_before_heat_correction().loc["electricity"]),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(required_fed_by_fuel_before_heat_correction().loc["heat"])
            * (1 + ratio_fed_for_heatnc_vs_fed_for_heatcom()),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            float(required_fed_by_fuel_before_heat_correction().loc["liquids"])
            * (1 - float(share_feh_over_fed_by_final_fuel().loc["liquids"])),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(required_fed_by_fuel_before_heat_correction().loc["gases"])
            * (1 - float(share_feh_over_fed_by_final_fuel().loc["gases"])),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            float(required_fed_by_fuel_before_heat_correction().loc["solids"])
            * (1 - float(share_feh_over_fed_by_final_fuel().loc["solids"])),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def required_fed_by_fuel_before_heat_correction():
    """
    Real Name: Required FED by fuel before heat correction
    Original Eqn: required FED sectors by fuel[final sources]+Households final energy demand[final sources]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Required final energy demand by fuel before heat demand correction.        The final energy demand is modified with the feedback from the change of
        the EROEI.
    """
    return required_fed_sectors_by_fuel() + households_final_energy_demand()


@subs(["final sources"], _subscript_dict)
def required_fed_sectors_by_fuel():
    """
    Real Name: required FED sectors by fuel
    Original Eqn: SUM(Required final energy by sector and fuel EU[final sources,sectors!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return sum(required_final_energy_by_sector_and_fuel_eu(), dim=("sectors",))


@subs(["final sources", "sectors"], _subscript_dict)
def required_final_energy_by_sector_and_fuel_eu():
    """
    Real Name: Required final energy by sector and fuel EU
    Original Eqn: Total output required by sector[sectors]*Final energy intensity by sector and fuel EU[final sources,sectors]/1e+06
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Required final energy by sector and fuel (35 WIOD sectors & 5 final
        sources).
    """
    return (
        total_output_required_by_sector()
        * final_energy_intensity_by_sector_and_fuel_eu()
        / 1e06
    )


def required_tfed():
    """
    Real Name: Required TFED
    Original Eqn: SUM(Required FED by fuel[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Required total final energy demand after heat demand correction.
        Non-commercial heat is accounted as heat, i.e. not following the data from
        the IEA Balances.
    """
    return sum(required_fed_by_fuel(), dim=("final sources",))


def required_tfed_before_heat_dem_corr():
    """
    Real Name: Required TFED before heat dem corr
    Original Eqn: SUM(Required FED by fuel before heat correction[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy demand before heat demand correction, i.e. following
        the data from the IEA Balances (Non-commercial heat is not accounted as
        heat).
    """
    return sum(required_fed_by_fuel_before_heat_correction(), dim=("final sources",))


def required_tfed_sectors():
    """
    Real Name: required TFED sectors
    Original Eqn: SUM(required FED sectors by fuel[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(required_fed_sectors_by_fuel(), dim=("final sources",))


def share_e_losses_cc_world():
    """
    Real Name: share E losses CC world
    Original Eqn: IF THEN ELSE("activate ELF by scen?"=1,share E losses CC,0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        activate_elf_by_scen() == 1, lambda: share_e_losses_cc(), lambda: 0
    )


def share_tfed_before_heat_dem_corr_vs_real_tfec():
    """
    Real Name: share TFED before heat dem corr vs real TFEC
    Original Eqn: Required TFED/Required TFED before heat dem corr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total final energy demand before heat demand correction vs. real
        TFEC as estimated in MEDEAS correcting for heat demand for non-commercial
        sectors.
    """
    return required_tfed() / required_tfed_before_heat_dem_corr()


@subs(["final sources"], _subscript_dict)
def shortage_coef_without_min_without_elosses():
    """
    Real Name: "Shortage coef without MIN without E-losses"
    Original Eqn: real FE consumption by fuel before heat correction[final sources]/Required FED by fuel before heat correction[final sources]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    ***Variable to test the consistency of the modeling. IT CAN NEVER BE > 1!
        (that would mean consumption > demand.***
    """
    return (
        real_fe_consumption_by_fuel_before_heat_correction()
        / required_fed_by_fuel_before_heat_correction()
    )


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_by_sector():
    """
    Real Name: Total domestic output required by sector
    Original Eqn: SUM(Leontief Matrix Domestic[sectors,sectors1!]*Domestic demand by sector[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Required total EU28 output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix_domestic()
        * rearrange(domestic_demand_by_sector(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["sectors"], _subscript_dict)
def total_output_required_by_sector():
    """
    Real Name: Total output required by sector
    Original Eqn: Domestic output required for exports by sector[sectors]+Total domestic output required by sector[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Total output required to satisfy domestic and foreign final demand.
    """
    return (
        domestic_output_required_for_exports_by_sector()
        + total_domestic_output_required_by_sector()
    )


_ext_constant_activate_elf_by_scen = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C119",
    {},
    _root,
    "_ext_constant_activate_elf_by_scen",
)


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp_eu(), lambda: 1, lambda: 8.6, time_step, "_delayfixed_gdp_delayed_1yr"
)


_delayfixed_real_demand_by_sector_delayed_eu = DelayFixed(
    lambda: real_final_demand_by_sector_eu(),
    lambda: 1,
    lambda: 10,
    time_step,
    "_delayfixed_real_demand_by_sector_delayed_eu",
)


_smooth_real_demand_delayed_1yr = Smooth(
    lambda: real_demand_tdollars(),
    lambda: 1,
    lambda: 8.6,
    lambda: 12,
    "_smooth_real_demand_delayed_1yr",
)
