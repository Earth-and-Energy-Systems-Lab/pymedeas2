"""
Module confrontation_of_demand_to_limits
Translated using PySD version 2.1.0
"""


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


def annual_gdp_growth_rate():
    """
    Real Name: Annual GDP growth rate
    Original Eqn: -1+ZIDZ( GDP, GDP delayed 1yr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual GDP growth rate.
    """
    return -1 + zidz(gdp(), gdp_delayed_1yr())


def cc_impacts_feedback_shortage_coeff():
    """
    Real Name: CC impacts feedback shortage coeff
    Original Eqn: (1-share E losses CC)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    This coefficient adapts the real final energy by fuel to be used by
        economic sectors taking into account climate change impacts.
    """
    return 1 - share_e_losses_cc()


@subs(["sectors"], _subscript_dict)
def demand_by_sector():
    """
    Real Name: Demand by sector
    Original Eqn: demand by sector FD adjusted[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return demand_by_sector_fd_adjusted()


def diff_annual_gdp_growth_rate():
    """
    Real Name: diff annual GDP growth rate
    Original Eqn: ZIDZ( (Annual GDP growth rate-Desired annual GDP growth rate) , Desired annual GDP growth rate)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Difference between the annual GDP growth rate desired and the real
        obtained.
    """
    return zidz(
        (annual_gdp_growth_rate() - desired_annual_gdp_growth_rate()),
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


@subs(["final sources"], _subscript_dict)
def energy_scarcity_feedback_shortage_coeff():
    """
    Real Name: Energy scarcity feedback shortage coeff
    Original Eqn: IF THEN ELSE("Activate energy scarcity feedback?"=1, MIN(1, ZIDZ( real FE consumption by fuel before heat correction[final sources], Required FED by fuel before heat correction[final sources] )), 1)
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
def final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Final energy intensity by sector and fuel
    Original Eqn: Evol final energy intensity by sector and fuel[sectors,final sources]
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Evolution of final energy intensity by sector and fuel.                (1+("Activate EROI tot FC feedback through intensities?"*EROI FC tot from
        2015*1-1)): to test method of EROI feedback through the variation of
        energy intensities. "EROI FC tot from 2015*1", ese "*1" si aumento el
        factor a por ejemplo 2 entonces se ve el efecto de que se reduce el GDP
        progresivamente.
    """
    return evol_final_energy_intensity_by_sector_and_fuel()


def gdp():
    """
    Real Name: GDP
    Original Eqn: Real demand/1e+06
    Units: T$
    Limits: (None, None)
    Type: component
    Subs: None

    Global GDP in T1995T$.
    """
    return real_demand() / 1e06


def gdp_delayed_1yr():
    """
    Real Name: GDP delayed 1yr
    Original Eqn: DELAY FIXED ( GDP, 1, 29.16)
    Units: Tdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    GDP projection delayed 1 year.
    """
    return _delayfixed_gdp_delayed_1yr()


def gdppc():
    """
    Real Name: GDPpc
    Original Eqn: GDP*dollars to Tdollars/Population
    Units: $/people
    Limits: (None, None)
    Type: component
    Subs: None

    GDP per capita (1995T$ per capita).
    """
    return gdp() * dollars_to_tdollars() / population()


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
    Original Eqn: SUM(Real demand by sector[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand
    """
    return sum(real_demand_by_sector(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector():
    """
    Real Name: Real demand by sector
    Original Eqn: MAX(0, SUM(IA matrix[sectors,sectors1!]*Real total output by sector[sectors1!]))
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real demand by sector (35 WIOD sectors). US$1995
    """
    return np.maximum(
        0,
        sum(
            ia_matrix()
            * rearrange(real_total_output_by_sector(), ["sectors1"], _subscript_dict),
            dim=("sectors1",),
        ),
    )


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_delayed():
    """
    Real Name: Real demand by sector delayed
    Original Eqn: DELAY FIXED(Real demand by sector[sectors], 1, 10)
    Units: $
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return _delayfixed_real_demand_by_sector_delayed()


@subs(["final sources"], _subscript_dict)
def real_fe_consumption_by_fuel():
    """
    Real Name: real FE consumption by fuel
    Original Eqn:
      Total FE Elec consumption TWh*EJ per TWh
      Total FE Heat generation EJ/(1+Share heat distribution losses)
      (PES gases-"PED nat. gas for GTL EJ"-Other gases required )*share gases for final energy
      (PES Liquids EJ-Other liquids required EJ)*share liquids for final energy
      (extraction coal EJ+(PE traditional biomass EJ delayed 1yr+PES waste for TFC +PES peat EJ+Losses in charcoal plants EJ)-PED coal for CTL EJ-Other solids required)*share solids for final energy
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Real final energy consumption by fuel after accounting for energy
        availability.
    """
    return xrmerge(
        rearrange(
            total_fe_elec_consumption_twh() * ej_per_twh(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            total_fe_heat_generation_ej() / (1 + share_heat_distribution_losses()),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            (pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required())
            * share_gases_for_final_energy(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            (pes_liquids_ej() - other_liquids_required_ej())
            * share_liquids_for_final_energy(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            (
                extraction_coal_ej()
                + (
                    pe_traditional_biomass_ej_delayed_1yr()
                    + pes_waste_for_tfc()
                    + pes_peat_ej()
                    + losses_in_charcoal_plants_ej()
                )
                - ped_coal_for_ctl_ej()
                - other_solids_required()
            )
            * share_solids_for_final_energy(),
            ["final sources"],
            {"final sources": ["solids"]},
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


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel():
    """
    Real Name: Real final energy by sector and fuel
    Original Eqn: Required final energy by sector and fuel[final sources,sectors]*Energy scarcity feedback shortage coeff[final sources]*CC impacts feedback shortage coeff
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real final energy to be used by economic sectors and fuel after accounting
        for energy scarcity and CC impacts.
    """
    return (
        required_final_energy_by_sector_and_fuel()
        * energy_scarcity_feedback_shortage_coeff()
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

    Real total final energy consumption.
    """
    return sum(real_fe_consumption_by_fuel(), dim=("final sources",))


def real_total_output():
    """
    Real Name: Real total output
    Original Eqn: SUM(Real total output by sector[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total output (1995$).
    """
    return sum(real_total_output_by_sector(), dim=("sectors",))


@subs(["final sources", "sectors"], _subscript_dict)
def real_total_output_by_fuel_and_sector():
    """
    Real Name: Real total output by fuel and sector
    Original Eqn: XIDZ(Real final energy by sector and fuel[final sources,sectors], Final energy intensity by sector and fuel[final sources,sectors], Required total output by sector[sectors]/1e+06)*1e+06
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real total output by sector (35 WIOD sectors). US$1995
    """
    return (
        xidz(
            real_final_energy_by_sector_and_fuel(),
            final_energy_intensity_by_sector_and_fuel(),
            required_total_output_by_sector() / 1e06,
        )
        * 1e06
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector():
    """
    Real Name: Real total output by sector
    Original Eqn: VMIN(Real total output by fuel and sector[final sources!,sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real total output by sector (35 WIOD sectors). US$1995. We assume the most
        limiting resources.
    """
    return vmin(real_total_output_by_fuel_and_sector(), dim=("final sources",))


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
    Original Eqn: SUM(Required final energy by sector and fuel[final sources,sectors!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return sum(required_final_energy_by_sector_and_fuel(), dim=("sectors",))


@subs(["final sources", "sectors"], _subscript_dict)
def required_final_energy_by_sector_and_fuel():
    """
    Real Name: Required final energy by sector and fuel
    Original Eqn: Required total output by sector[sectors]*Final energy intensity by sector and fuel[final sources,sectors]/1e+06
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Required final energy by sector and fuel (35 WIOD sectors & 5 final
        sources).
    """
    return (
        required_total_output_by_sector()
        * final_energy_intensity_by_sector_and_fuel()
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


@subs(["sectors"], _subscript_dict)
def required_total_output_by_sector():
    """
    Real Name: Required total output by sector
    Original Eqn: SUM(Leontief Matrix[sectors,sectors1!]*Demand by sector[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Required total output by sector (35 WIOD sectors). US$1995
    """
    return sum(
        leontief_matrix()
        * rearrange(demand_by_sector(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


def tfei_sectors():
    """
    Real Name: TFEI sectors
    Original Eqn: SUM(Final energy intensity by sector and fuel[final sources!,sectors!])
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy intensity of the 35 WIOD sectors.
    """
    return sum(
        final_energy_intensity_by_sector_and_fuel(), dim=("sectors", "final sources")
    )


_delayfixed_gdp_delayed_1yr = DelayFixed(
    lambda: gdp(), lambda: 1, lambda: 29.16, time_step, "_delayfixed_gdp_delayed_1yr"
)


_delayfixed_real_demand_by_sector_delayed = DelayFixed(
    lambda: real_demand_by_sector(),
    lambda: 1,
    lambda: 10,
    time_step,
    "_delayfixed_real_demand_by_sector_delayed",
)
