"""
Module by_fuel_for_sectors_i
Translated using PySD version 2.1.0
"""


@subs(["SECTORS H"], _subscript_dict)
def activate_bottom_up_method():
    """
    Real Name: Activate BOTTOM UP method
    Original Eqn: 0
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H']

    Activate BOTTOM UP method or maintain TOP DOWN method. Activate for each sector (by
        default, only inland transport sector)        0. Bottom-up NOT activated        1. Bottom-up activated
    """
    return xr.DataArray(0, {"SECTORS H": _subscript_dict["SECTORS H"]}, ["SECTORS H"])


@subs(["sectors"], _subscript_dict)
def available_improvement_efficiency():
    """
    Real Name: available improvement efficiency
    Original Eqn: MIN(1,IF THEN ELSE(Time>2009, ZIDZ( (Global energy intensity by sector[sectors]-(min energy intensity vs intial*Initial global energy intensity 2009[sectors])), (1-min energy intensity vs intial)*Initial global energy intensity 2009[sectors]), 1))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Remainig improvement of energy intensity respect to the minimum value.
    """
    return np.minimum(
        1,
        if_then_else(
            time() > 2009,
            lambda: zidz(
                (
                    global_energy_intensity_by_sector()
                    - (
                        min_energy_intensity_vs_intial()
                        * rearrange(
                            initial_global_energy_intensity_2009(),
                            ["sectors"],
                            _subscript_dict,
                        )
                    )
                ),
                (1 - min_energy_intensity_vs_intial())
                * rearrange(
                    initial_global_energy_intensity_2009(), ["sectors"], _subscript_dict
                ),
            ),
            lambda: 1,
        ),
    )


def choose_final_sectoral_energy_intensities_evolution_method():
    """
    Real Name: Choose final sectoral energy intensities evolution method
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C195')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0- Dynamic evolution with policies and feedback of final fuel scarcity        1- Constant at 2009 levels        2- Sectoral energy intensity targets defined by user
    """
    return _ext_constant_choose_final_sectoral_energy_intensities_evolution_method()


@subs(["sectors", "final sources"], _subscript_dict)
def decrease_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    Real Name: Decrease of intensity due to energy a technology change TOP DOWN
    Original Eqn: IF THEN ELSE(Activate BOTTOM UP method[sectors]=0,IF THEN ELSE((ZIDZ(Evol final energy intensity by sector and fuel [ sectors,final sources], Global energy intensity by sector [sectors])) >= minimum fraction source[sectors,final sources],(max yearly change between sources[sectors,final sources]*(1+Percentage of change over the historic maximun variation of energy intensities)) *Evol final energy intensity by sector and fuel[sectors, final sources ] * Pressure to change energy technology[sectors,final sources], 0 ),0)
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    When in one economic sector, one type of energy (a) is replaced by another
        (b), the energy intensity of (b) will increase and the energy intensity of
        (a) will decrease. This flow represents the decrease of (a).
    """
    return if_then_else(
        rearrange(activate_bottom_up_method(), ["sectors"], _subscript_dict) == 0,
        lambda: if_then_else(
            (
                zidz(
                    evol_final_energy_intensity_by_sector_and_fuel(),
                    global_energy_intensity_by_sector(),
                )
            )
            >= rearrange(
                minimum_fraction_source(), ["sectors", "final sources"], _subscript_dict
            ),
            lambda: (
                rearrange(
                    max_yearly_change_between_sources(),
                    ["sectors", "final sources"],
                    _subscript_dict,
                )
                * (
                    1
                    + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
                )
            )
            * evol_final_energy_intensity_by_sector_and_fuel()
            * pressure_to_change_energy_technology(),
            lambda: 0,
        ),
        lambda: 0,
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def efficiency_energy_acceleration():
    """
    Real Name: Efficiency energy acceleration
    Original Eqn: -Maximum yearly acceleration of intensity improvement[SECTORS H,final sources]*(1+Percentage of change over the historic maximun variation of energy intensities)*Pressure to improve energy intensity efficiency[SECTORS H,final sources]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    This variable represents the acceleration of the process of variation of
        the energy intensity that can be produced by polítcas or scarcity
        pressures.
    """
    return (
        -maximum_yearly_acceleration_of_intensity_improvement()
        * (
            1
            + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
        )
        * pressure_to_improve_energy_intensity_efficiency()
    )


@subs(["SECTORS H", "final sources", "final sources1"], _subscript_dict)
def efficiency_rate_of_substitution():
    """
    Real Name: efficiency rate of substitution
    Original Eqn:
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'efficiency_rate_of_substitution_electricity*')
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'efficiency_rate_of_substitution_heat*')
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'efficiency_rate_of_substitution_liquids*')
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'efficiency_rate_of_substitution_gases*')
      GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'efficiency_rate_of_substitution_solids*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources', 'final sources1']

    It is necessary to take into account that the energy efficiencies of the
        two technologies exchanged do not necessarily have to be the same. In
        other words, a decrease in the energy intensity of (a) will not imply the
        same increase in the energy intensity of (b). This possible difference is
        compensated through the parameter “Efficiency rate of substitution”.
    """
    return _ext_constant_efficiency_rate_of_substitution()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def energy_intensity_target():
    """
    Real Name: Energy intensity target
    Original Eqn: energy intensity target Mdollar[SECTORS H,final sources]*Mdollar per Tdollar
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    Energy intensity targets by sector and final energy defined by user
    """
    return energy_intensity_target_mdollar() * mdollar_per_tdollar()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def energy_intensity_target_mdollar():
    """
    Real Name: energy intensity target Mdollar
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'energy_intensity_target*')
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Energy intensity targets by sector and final energy defined by user
    """
    return _ext_constant_energy_intensity_target_mdollar()


@subs(["sectors", "final sources"], _subscript_dict)
def evol_final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Evol final energy intensity by sector and fuel
    Original Eqn: INTEG ( Increase of intensity due to energy a technology change TOP DOWN[sectors,final sources]+inertial rate energy intensity TOP DOWN[sectors,final sources]+rate change intensity BOTTOM UP[sectors,final sources]-Decrease of intensity due to energy a technology change TOP DOWN[sectors,final sources], Initial energy intensity 1995[sectors,final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    This variable models the dynamic evolution of the matrix of energy intensities of
        the 35 economic sectors and the 5 types of final energy. It is a 35x5
        matrix.        The evolution of the intensities is considered to be due to two main
        effects: (1) the variation of the energy efficiency (flow due to the
        variable inertial rate energy intensity) and (2) the change of one type of
        final energy by another, As a consequence of a technological change (flow
        due to the variables Increase / decrease of intensity due to energy to
        technology change), as for example the change due to the electrification
        of the transport.
    """
    return _integ_evol_final_energy_intensity_by_sector_and_fuel()


def exp_rapid_evol_change_energy():
    """
    Real Name: exp rapid evol change energy
    Original Eqn: 1/2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Parameter that define the speed of application of policies in the rapid
        way.
    """
    return 1 / 2


def exp_rapid_evol_improve_efficiency():
    """
    Real Name: exp rapid evol improve efficiency
    Original Eqn: 1/2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Parameter that define the speed of application of policies in the rapid
        way.
    """
    return 1 / 2


def exp_slow_evol_change_energy():
    """
    Real Name: exp slow evol change energy
    Original Eqn: 2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


def exp_slow_evol_improve_efficiency():
    """
    Real Name: exp slow evol improve efficiency
    Original Eqn: 2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Parameter that define the speed of application of policies in the slow way.
    """
    return 2


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_2020():
    """
    Real Name: Final energy intensity 2020
    Original Eqn: SAMPLE IF TRUE(Time<year energy intensity target, Evol final energy intensity by sector and fuel[sectors,final sources], Evol final energy intensity by sector and fuel[sectors,final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Energy intensity by sector and final source in 2009
    """
    return _sample_if_true_final_energy_intensity_2020()


def final_year_energy_intensity_target():
    """
    Real Name: final year energy intensity target
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'final_year_energy_intensity_target')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year defined by user in which the energy intensity targets are set.
    """
    return _ext_constant_final_year_energy_intensity_target()


@subs(["final sources"], _subscript_dict)
def fuel_scarcity_pressure():
    """
    Real Name: Fuel scarcity pressure
    Original Eqn: IF THEN ELSE(scarcity feedback final fuel replacement flag=1,perception of final energy scarcity[ final sources],0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Pressure due significant variations in the fuel scarcity of each type of
        final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: perception_of_final_energy_scarcity(),
        lambda: 0,
    )


@subs(["sectors"], _subscript_dict)
def global_energy_intensity_by_sector():
    """
    Real Name: Global energy intensity by sector
    Original Eqn: SUM(Evol final energy intensity by sector and fuel[sectors,final sources!])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Global energy intensity of one sector considering the energy intensity of
        five final fuels.
    """
    return sum(evol_final_energy_intensity_by_sector_and_fuel(), dim=("final sources",))


def historic_final_energy_intensity(x):
    """
    Real Name: historic final energy intensity
    Original Eqn:
      GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_final_energy_intensity_electricity')
      GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_final_energy_intensity_heat')
      GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_final_energy_intensity_liquids')
      GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_final_energy_intensity_gases')
      GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_final_energy_intensity_solids')
    Units: EJ/Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['final sources', 'SECTORS H']

    Historic final energy intensity, households + 14 sectors & final sources.
        US$1995.
    """
    return _ext_lookup_historic_final_energy_intensity(x)


@subs(["SECTORS H", "final sources"], _subscript_dict)
def historic_mean_rate_energy_intensity():
    """
    Real Name: historic mean rate energy intensity
    Original Eqn:
      GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'historic_mean_rate_energy_intensity_electricity*')
      GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'historic_mean_rate_energy_intensity_heat*')
      GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'historic_mean_rate_energy_intensity_liquids*')
      GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'historic_mean_rate_energy_intensity_gases*')
      GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'historic_mean_rate_energy_intensity_solids*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Historical trend of sectors energy intensity by final source (OLS method).
    """
    return _ext_constant_historic_mean_rate_energy_intensity()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def historic_rate_final_energy_intensity():
    """
    Real Name: historic rate final energy intensity
    Original Eqn: (historic final energy intensity[final sources,SECTORS H](INTEGER(Time+1))-historic final energy intensity [final sources,SECTORS H](INTEGER(Time)))*Mdollar per Tdollar
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    Historic variation of final energy intensity by final source (WIOD data)
    """
    return (
        historic_final_energy_intensity(integer(time() + 1))
        - historic_final_energy_intensity(integer(time()))
    ) * mdollar_per_tdollar()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def implementation_policy_to_change_final_energy():
    """
    Real Name: Implementation policy to change final energy
    Original Eqn: IF THEN ELSE(Choose final sectoral energy intensities evolution method<>2:OR:Year policy change energy[SECTORS H,final sources]<2015:OR:Year policy change energy[SECTORS H,final sources]>Year to finish energy intensity policies[SECTORS H,final sources]:OR:Time<Year policy change energy[SECTORS H,final sources], 0, IF THEN ELSE(Time>Year to finish energy intensity policies[SECTORS H,final sources], 1, IF THEN ELSE(Policy change energy speed[SECTORS H,final sources]=1, ((Time-Year policy change energy[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy change energy[SECTORS H,final sources]))^exp rapid evol change energy, IF THEN ELSE(Policy change energy speed[SECTORS H,final sources]=2, ((Time-Year policy change energy[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy change energy[SECTORS H,final sources])), IF THEN ELSE(Policy change energy speed[SECTORS H,final sources]=3, ((Time-Year policy change energy[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy change energy[SECTORS H,final sources]))^exp slow evol change energy, 0 )))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    Pressure due to energy policies, eg incentives for change the final energy
    """
    return if_then_else(
        logical_or(
            choose_final_sectoral_energy_intensities_evolution_method() != 2,
            year_policy_change_energy() < 2015,
            year_policy_change_energy() > year_to_finish_energy_intensity_policies(),
            time() < year_policy_change_energy(),
        ),
        lambda: 0,
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: 1,
            lambda: if_then_else(
                policy_change_energy_speed() == 1,
                lambda: (
                    (time() - year_policy_change_energy())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_change_energy()
                    )
                )
                ** exp_rapid_evol_change_energy(),
                lambda: if_then_else(
                    policy_change_energy_speed() == 2,
                    lambda: (
                        (time() - year_policy_change_energy())
                        / (
                            year_to_finish_energy_intensity_policies()
                            - year_policy_change_energy()
                        )
                    ),
                    lambda: if_then_else(
                        policy_change_energy_speed() == 3,
                        lambda: (
                            (time() - year_policy_change_energy())
                            / (
                                year_to_finish_energy_intensity_policies()
                                - year_policy_change_energy()
                            )
                        )
                        ** exp_slow_evol_change_energy(),
                        lambda: 0,
                    ),
                ),
            ),
        ),
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def implementation_policy_to_improve_energy_intensity_efficiency():
    """
    Real Name: Implementation policy to improve energy intensity efficiency
    Original Eqn: IF THEN ELSE(Choose final sectoral energy intensities evolution method<>2:OR:Year policy to improve efficiency[SECTORS H,final sources]<2015:OR:Year policy to improve efficiency[SECTORS H,final sources]>Year to finish energy intensity policies[SECTORS H,final sources]:OR:Time<Year policy to improve efficiency[SECTORS H,final sources], 0, IF THEN ELSE(Time>Year to finish energy intensity policies[SECTORS H,final sources], 1, IF THEN ELSE(Policy to improve efficiency speed[SECTORS H,final sources]=1, ((Time-Year policy to improve efficiency[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy to improve efficiency[SECTORS H,final sources]))^exp rapid evol improve efficiency, IF THEN ELSE(Policy to improve efficiency speed[SECTORS H,final sources]=2, ((Time-Year policy to improve efficiency[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy to improve efficiency[SECTORS H,final sources])), IF THEN ELSE(Policy to improve efficiency speed[SECTORS H,final sources]=3, ((Time-Year policy to improve efficiency[SECTORS H,final sources])/(Year to finish energy intensity policies[SECTORS H,final sources]-Year policy to improve efficiency[SECTORS H,final sources]))^exp slow evol improve efficiency, 0 )))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    Pressure due to energy policies, eg incentives for energy efficiency,
    """
    return if_then_else(
        logical_or(
            choose_final_sectoral_energy_intensities_evolution_method() != 2,
            year_policy_to_improve_efficiency() < 2015,
            year_policy_to_improve_efficiency()
            > year_to_finish_energy_intensity_policies(),
            time() < year_policy_to_improve_efficiency(),
        ),
        lambda: 0,
        lambda: if_then_else(
            time() > year_to_finish_energy_intensity_policies(),
            lambda: 1,
            lambda: if_then_else(
                policy_to_improve_efficiency_speed() == 1,
                lambda: (
                    (time() - year_policy_to_improve_efficiency())
                    / (
                        year_to_finish_energy_intensity_policies()
                        - year_policy_to_improve_efficiency()
                    )
                )
                ** exp_rapid_evol_improve_efficiency(),
                lambda: if_then_else(
                    policy_to_improve_efficiency_speed() == 2,
                    lambda: (
                        (time() - year_policy_to_improve_efficiency())
                        / (
                            year_to_finish_energy_intensity_policies()
                            - year_policy_to_improve_efficiency()
                        )
                    ),
                    lambda: if_then_else(
                        policy_to_improve_efficiency_speed() == 3,
                        lambda: (
                            (time() - year_policy_to_improve_efficiency())
                            / (
                                year_to_finish_energy_intensity_policies()
                                - year_policy_to_improve_efficiency()
                            )
                        )
                        ** exp_slow_evol_improve_efficiency(),
                        lambda: 0,
                    ),
                ),
            ),
        ),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_change_top_down():
    """
    Real Name: Increase of intensity due to energy a technology change TOP DOWN
    Original Eqn: SUM(Increase of intensity due to energy a technology eff[sectors,final sources,final sources1!])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    When in one economic sector, one type of energy (a) is replaced by another
        (b), the energy intensity of (b) will increase and the energy intensity of
        (a) will decrease. This flow represents the increase of (b).
    """
    return sum(
        rearrange(
            increase_of_intensity_due_to_energy_a_technology_eff(),
            ["sectors", "final sources", "final sources1"],
            _subscript_dict,
        ),
        dim=("final sources1",),
    )


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_eff():
    """
    Real Name: Increase of intensity due to energy a technology eff
    Original Eqn: IF THEN ELSE(efficiency rate of substitution[sectors,final sources1,final sources]=0,Increase of intensity due to energy a technology net [sectors,final sources1,final sources],Increase of intensity due to energy a technology net[sectors, final sources1,final sources]*efficiency rate of substitution[sectors,final sources1,final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources1', 'final sources']

    Increase of intensity due to change a energy technology by fuel
    """
    return if_then_else(
        rearrange(
            efficiency_rate_of_substitution(),
            ["sectors", "final sources1", "final sources"],
            _subscript_dict,
        )
        == 0,
        lambda: increase_of_intensity_due_to_energy_a_technology_net(),
        lambda: increase_of_intensity_due_to_energy_a_technology_net()
        * rearrange(
            efficiency_rate_of_substitution(),
            ["sectors", "final sources1", "final sources"],
            _subscript_dict,
        ),
    )


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_energy_a_technology_net():
    """
    Real Name: Increase of intensity due to energy a technology net
    Original Eqn: Decrease of intensity due to energy a technology change TOP DOWN[sectors,final sources]*share tech change fuel[sectors,final sources1,final sources]
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources1', 'final sources']

    Increase of intensity due to change a energy technology without
        considering efficieny rate of susbsitution by fuel
    """
    return (
        decrease_of_intensity_due_to_energy_a_technology_change_top_down()
        * share_tech_change_fuel()
    )


@subs(["sectors", "final sources"], _subscript_dict)
def inertial_rate_energy_intensity_top_down():
    """
    Real Name: inertial rate energy intensity TOP DOWN
    Original Eqn: IF THEN ELSE(Time<2009, historic rate final energy intensity[sectors,final sources], IF THEN ELSE(Choose final sectoral energy intensities evolution method=1, IF THEN ELSE(Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[sectors,final sources]=0, IF THEN ELSE(Efficiency energy acceleration[sectors,final sources]<0, Evol final energy intensity by sector and fuel[sectors,final sources]*Efficiency energy acceleration[sectors,final sources]*available improvement efficiency [sectors], Initial energy intensity 1995[sectors,final sources]*Efficiency energy acceleration[sectors,final sources]), 0), IF THEN ELSE(Time<year energy intensity target, IF THEN ELSE(Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[sectors,final sources]=0, IF THEN ELSE((historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])<0, Evol final energy intensity by sector and fuel[sectors,final sources]*(historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors], Initial energy intensity 1995[sectors,final sources]*(historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])), 0), IF THEN ELSE(Choose final sectoral energy intensities evolution method=2, IF THEN ELSE(Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[sectors,final sources]=0, IF THEN ELSE((historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])<0, Evol final energy intensity by sector and fuel[sectors,final sources]*(historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])*available improvement efficiency[sectors], Initial energy intensity 1995[sectors,final sources]*(historic mean rate energy intensity[sectors,final sources]+Efficiency energy acceleration[sectors,final sources])), 0), IF THEN ELSE(Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[sectors,final sources]=0, IF THEN ELSE((Efficiency energy acceleration[sectors,final sources])<0, Evol final energy intensity by sector and fuel[sectors,final sources]*Efficiency energy acceleration[sectors,final sources]*available improvement efficiency[sectors], Initial energy intensity 1995[sectors,final sources]*Efficiency energy acceleration[sectors,final sources])+variation energy intensity TARGET[sectors,final sources], 0)))))
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    This variable models the variation of the energy intensity according to the
        historical trend and represents the variation of the technological energy
        efficiency in each economic sector for each type of energy. By default it
        will follow the historical trend but can be modified by policies or market
        conditions that accelerate change.                IF THEN ELSE(Choose final sectoral energy intensities evolution method=3,IF THEN
        ELSE(Time<2009,        historic rate final energy intensity[sectors,final sources],IF THEN
        ELSE(Time<2020,IF THEN ELSE(Activate BOTTOM UP method        [sectors]=0:OR:rate change intensity BOTTOM UP[        sectors,final sources]=0, IF THEN ELSE((historical mean rate energy
        intensity[sectors,final sources]+Efficiency energy acceleration        [sectors,final sources])<0,Evol final energy intensity by sector and fuel        [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources]        +Efficiency energy acceleration[sectors,final sources])*available improvement
        efficiency[sectors],Initial energy intensity 1995        [sectors,final sources]        *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy
        acceleration[        sectors,final sources])),0), IF THEN ELSE        (Activate BOTTOM UP method[sectors]=0:OR:rate change intensity BOTTOM UP[        sectors,final sources]=0, IF THEN ELSE((Efficiency energy acceleration        [sectors,final sources])<0,Evol final energy intensity by sector and fuel        [sectors,final sources]*(Efficiency energy acceleration[sectors,final
        sources])*available improvement efficiency        [sectors],Initial energy intensity 1995        [sectors,final sources]        *(Efficiency energy acceleration[        sectors,final sources])),0)))+variation energy intensity TARGET[sectors,final
        sources],IF THEN ELSE(Time>2009, IF THEN ELSE(Activate BOTTOM UP method        [sectors]=0:OR:rate change intensity BOTTOM UP[        sectors,final sources]=0, IF THEN ELSE((historical mean rate energy
        intensity[sectors,final sources]+Efficiency energy acceleration        [sectors,final sources])<0,Evol final energy intensity by sector and fuel        [sectors,final sources]*(historical mean rate energy intensity[sectors,final sources]        +Efficiency energy acceleration[sectors,final sources])*available improvement
        efficiency[sectors],Initial energy intensity 1995        [sectors,final sources]        *(historical mean rate energy intensity[sectors,final sources]+Efficiency energy
        acceleration[        sectors,final sources])),0),        historic rate final energy intensity[sectors,final sources]))
    """
    return if_then_else(
        time() < 2009,
        lambda: rearrange(
            historic_rate_final_energy_intensity(),
            ["sectors", "final sources"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            choose_final_sectoral_energy_intensities_evolution_method() == 1,
            lambda: if_then_else(
                logical_or(
                    rearrange(activate_bottom_up_method(), ["sectors"], _subscript_dict)
                    == 0,
                    rate_change_intensity_bottom_up() == 0,
                ),
                lambda: if_then_else(
                    rearrange(
                        efficiency_energy_acceleration(),
                        ["sectors", "final sources"],
                        _subscript_dict,
                    )
                    < 0,
                    lambda: evol_final_energy_intensity_by_sector_and_fuel()
                    * rearrange(
                        efficiency_energy_acceleration(),
                        ["sectors", "final sources"],
                        _subscript_dict,
                    )
                    * available_improvement_efficiency(),
                    lambda: rearrange(
                        initial_energy_intensity_1995(),
                        ["sectors", "final sources"],
                        _subscript_dict,
                    )
                    * rearrange(
                        efficiency_energy_acceleration(),
                        ["sectors", "final sources"],
                        _subscript_dict,
                    ),
                ),
                lambda: 0,
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: if_then_else(
                    logical_or(
                        rearrange(
                            activate_bottom_up_method(), ["sectors"], _subscript_dict
                        )
                        == 0,
                        rate_change_intensity_bottom_up() == 0,
                    ),
                    lambda: if_then_else(
                        (
                            rearrange(
                                historic_mean_rate_energy_intensity(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                        )
                        < 0,
                        lambda: evol_final_energy_intensity_by_sector_and_fuel()
                        * (
                            rearrange(
                                historic_mean_rate_energy_intensity(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                        )
                        * available_improvement_efficiency(),
                        lambda: rearrange(
                            initial_energy_intensity_1995(),
                            ["sectors", "final sources"],
                            _subscript_dict,
                        )
                        * (
                            rearrange(
                                historic_mean_rate_energy_intensity(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                        ),
                    ),
                    lambda: 0,
                ),
                lambda: if_then_else(
                    choose_final_sectoral_energy_intensities_evolution_method() == 2,
                    lambda: if_then_else(
                        logical_or(
                            rearrange(
                                activate_bottom_up_method(),
                                ["sectors"],
                                _subscript_dict,
                            )
                            == 0,
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            (
                                rearrange(
                                    historic_mean_rate_energy_intensity(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                                + rearrange(
                                    efficiency_energy_acceleration(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                            )
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * (
                                rearrange(
                                    historic_mean_rate_energy_intensity(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                                + rearrange(
                                    efficiency_energy_acceleration(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                            )
                            * available_improvement_efficiency(),
                            lambda: rearrange(
                                initial_energy_intensity_1995(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            * (
                                rearrange(
                                    historic_mean_rate_energy_intensity(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                                + rearrange(
                                    efficiency_energy_acceleration(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                            ),
                        ),
                        lambda: 0,
                    ),
                    lambda: if_then_else(
                        logical_or(
                            rearrange(
                                activate_bottom_up_method(),
                                ["sectors"],
                                _subscript_dict,
                            )
                            == 0,
                            rate_change_intensity_bottom_up() == 0,
                        ),
                        lambda: if_then_else(
                            (
                                rearrange(
                                    efficiency_energy_acceleration(),
                                    ["sectors", "final sources"],
                                    _subscript_dict,
                                )
                            )
                            < 0,
                            lambda: evol_final_energy_intensity_by_sector_and_fuel()
                            * rearrange(
                                efficiency_energy_acceleration(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            * available_improvement_efficiency(),
                            lambda: rearrange(
                                initial_energy_intensity_1995(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            )
                            * rearrange(
                                efficiency_energy_acceleration(),
                                ["sectors", "final sources"],
                                _subscript_dict,
                            ),
                        )
                        + variation_energy_intensity_target(),
                        lambda: 0,
                    ),
                ),
            ),
        ),
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def initial_energy_intensity_1995():
    """
    Real Name: Initial energy intensity 1995
    Original Eqn: historic final energy intensity[final sources,SECTORS H](1995)*Mdollar per Tdollar
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    Initial energy intensity by sector and fuel in 1995
    """
    return historic_final_energy_intensity(1995) * mdollar_per_tdollar()


@subs(["SECTORS H"], _subscript_dict)
def initial_global_energy_intensity_2009():
    """
    Real Name: Initial global energy intensity 2009
    Original Eqn: SUM(historic final energy intensity[final sources!, SECTORS H](2009))*Mdollar per Tdollar
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H']

    Initial global energy intensity by sector 2009
    """
    return (
        sum(historic_final_energy_intensity(2009), dim=("final sources",))
        * mdollar_per_tdollar()
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def interfuel_scarcity_pressure():
    """
    Real Name: "Inter-fuel scarcity pressure"
    Original Eqn: IF THEN ELSE(scarcity feedback final fuel replacement flag=1,MAX(0,"perception of inter-fuel final energy scarcities" [final sources,final sources1]),0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'final sources1']

    Pressure due to variations in the inter-fuel scarcity of each final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: np.maximum(0, perception_of_interfuel_final_energy_scarcities()),
        lambda: 0,
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def max_yearly_change_between_sources():
    """
    Real Name: max yearly change between sources
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'max_yearly_change_between_sources*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    maximum annual change for one type of energy in a sector.
    """
    return _ext_constant_max_yearly_change_between_sources()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def maximum_yearly_acceleration_of_intensity_improvement():
    """
    Real Name: Maximum yearly acceleration of intensity improvement
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'maximum_yearly_acceleration_of_intensity_improvement*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Maximum feasible annual changes that could be sustained in the future in
        the energy intensity of each economic sector have been estimated based on
        the observation of trends and historical changes in the available data.
    """
    return _ext_constant_maximum_yearly_acceleration_of_intensity_improvement()


def mdollar_per_tdollar():
    """
    Real Name: Mdollar per Tdollar
    Original Eqn: 1e+06
    Units: Mdollar/Tdollar
    Limits: (None, None)
    Type: constant
    Subs: None

    Million dollars per  Tdollar (1 T$ = 1e6 M$).
    """
    return 1e06


def min_energy_intensity_vs_intial():
    """
    Real Name: min energy intensity vs intial
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C199')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Minimum value that the energy intensity for each economic sector could
        reach, obviously always above zero. This minimum value is very difficult
        to estimate, but based on historical values it has been considered that it
        can reach 30% of the value of 2009. (Capellán-Pérez et al., 2014)
    """
    return _ext_constant_min_energy_intensity_vs_intial()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def minimum_fraction_source():
    """
    Real Name: minimum fraction source
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'minimum_fraction_source*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    minimum energy of each type of energy that should be used in each sector
        because it is irreplaceable
    """
    return _ext_constant_minimum_fraction_source()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def policy_change_energy_speed():
    """
    Real Name: Policy change energy speed
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'policy_change_energy_speed*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Selection of the speed of application of the different policies to change
        the final energy
    """
    return _ext_constant_policy_change_energy_speed()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def policy_to_improve_efficiency_speed():
    """
    Real Name: Policy to improve efficiency speed
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'policy_to_improve_efficiency_speed*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Selection of the speed of application of the different policies to improve
        the efficiency.
    """
    return _ext_constant_policy_to_improve_efficiency_speed()


@subs(["sectors", "final sources"], _subscript_dict)
def pressure_to_change_energy_technology():
    """
    Real Name: Pressure to change energy technology
    Original Eqn: MIN(1,SUM(Pressure to change energy technology by fuel[sectors,final sources1!,final sources]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    This variable represents the pressure in one sector for substituting a
        final energy source for all the other energies.
    """
    return np.minimum(
        1,
        sum(
            rearrange(
                pressure_to_change_energy_technology_by_fuel(),
                ["sectors", "final sources1", "final sources"],
                _subscript_dict,
            ),
            dim=("final sources1",),
        ),
    )


@subs(["sectors", "final sources", "final sources1"], _subscript_dict)
def pressure_to_change_energy_technology_by_fuel():
    """
    Real Name: Pressure to change energy technology by fuel
    Original Eqn: IF THEN ELSE(efficiency rate of substitution[sectors, final sources,final sources1]=0,MIN(MAX("Inter-fuel scarcity pressure" [final sources,final sources1],0),1),MIN(MAX("Inter-fuel scarcity pressure"[final sources,final sources1 ] + Implementation policy to change final energy [sectors,final sources1], 0), 1 ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources', 'final sources1']

    This variable represents the pressure in each economic sector for
        substituting a final energy source for another. This change depending on
        the sectors will have different technological difficulty and different
        cost. This pressure may be due to (1) energy policies, eg substitution of
        fossil fuels for electrical energy, or (2) by variations in the scarcity
        of each type of final energy.
    """
    return if_then_else(
        rearrange(
            efficiency_rate_of_substitution(),
            ["sectors", "final sources", "final sources1"],
            _subscript_dict,
        )
        == 0,
        lambda: np.minimum(np.maximum(interfuel_scarcity_pressure(), 0), 1),
        lambda: np.minimum(
            np.maximum(
                interfuel_scarcity_pressure()
                + rearrange(
                    implementation_policy_to_change_final_energy(),
                    ["sectors", "final sources1"],
                    _subscript_dict,
                ),
                0,
            ),
            1,
        ),
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def pressure_to_improve_energy_intensity_efficiency():
    """
    Real Name: Pressure to improve energy intensity efficiency
    Original Eqn: MIN(1,Fuel scarcity pressure[final sources]+Implementation policy to improve energy intensity efficiency[SECTORS H,final sources])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['SECTORS H', 'final sources']

    This variable represents the pressure in each economic sector to improve
        energy efficiency in the technology used. This change according to the
        sectors will have different technological difficulty and different cost.
        This pressure may be due to (1) energy policies, eg incentives for energy
        efficiency, or (2) significant variations in the scarcity of each type of
        final energy.
    """
    return np.minimum(
        1,
        fuel_scarcity_pressure()
        + implementation_policy_to_improve_energy_intensity_efficiency(),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def rate_change_intensity_bottom_up():
    """
    Real Name: rate change intensity BOTTOM UP
    Original Eqn: IF THEN ELSE(Activate BOTTOM UP method[sectors]=1, inland transport variation intensity[final sources], 0)
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    Variation of the energy intensity of inland transport in BOTTOM UP method
    """
    return if_then_else(
        rearrange(activate_bottom_up_method(), ["sectors"], _subscript_dict) == 1,
        lambda: inland_transport_variation_intensity(),
        lambda: 0,
    )


def scarcity_feedback_final_fuel_replacement_flag():
    """
    Real Name: scarcity feedback final fuel replacement flag
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'scarcity_feedback_final_fuel_replacement_flag')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to (de)activate the scarcity feedback fuel replacement.
    """
    return _ext_constant_scarcity_feedback_final_fuel_replacement_flag()


@subs(["sectors", "final sources1", "final sources"], _subscript_dict)
def share_tech_change_fuel():
    """
    Real Name: share tech change fuel
    Original Eqn: ZIDZ( Pressure to change energy technology by fuel[sectors,final sources1,final sources], SUM(Pressure to change energy technology by fuel[sectors,final sources1!,final sources]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources1', 'final sources']

    Share of the global pressure to change energy technology that corresponds
        to each fuel.
    """
    return zidz(
        rearrange(
            pressure_to_change_energy_technology_by_fuel(),
            ["sectors", "final sources1", "final sources"],
            _subscript_dict,
        ),
        sum(
            rearrange(
                pressure_to_change_energy_technology_by_fuel(),
                ["sectors", "final sources1", "final sources"],
                _subscript_dict,
            ),
            dim=("final sources1",),
        ),
    )


@subs(["sectors", "final sources"], _subscript_dict)
def variation_energy_intensity_target():
    """
    Real Name: variation energy intensity TARGET
    Original Eqn: IF THEN ELSE(Choose energy intensity target method=1,IF THEN ELSE(Time>=final year energy intensity target,0,IF THEN ELSE(Time<year energy intensity target,0,((Energy intensity target[sectors,final sources]-Evol final energy intensity by sector and fuel[ sectors,final sources])/(final year energy intensity target-Time)))),IF THEN ELSE(Time>=final year energy intensity target,0,IF THEN ELSE(Time<year energy intensity target ,0,((Final energy intensity 2020[final sources,sectors]*(1+pct change energy intensity target)-Evol final energy intensity by sector and fuel[sectors,final sources])/(final year energy intensity target-Time)))))
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'final sources']

    Variation in energy intensity by sector and final energy defined by user
        targets.
    """
    return if_then_else(
        choose_energy_intensity_target_method() == 1,
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: 0,
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: 0,
                lambda: (
                    (
                        rearrange(
                            energy_intensity_target(),
                            ["sectors", "final sources"],
                            _subscript_dict,
                        )
                        - evol_final_energy_intensity_by_sector_and_fuel()
                    )
                    / (final_year_energy_intensity_target() - time())
                ),
            ),
        ),
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: 0,
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: 0,
                lambda: (
                    (
                        final_energy_intensity_2020()
                        * (1 + pct_change_energy_intensity_target())
                        - evol_final_energy_intensity_by_sector_and_fuel()
                    )
                    / (final_year_energy_intensity_target() - time())
                ),
            ),
        ),
    )


@subs(["SECTORS H", "final sources"], _subscript_dict)
def year_policy_change_energy():
    """
    Real Name: Year policy change energy
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'year_policy_change_energy*')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Year when the policy to change final energy in the sectors start. For each
        of five final energies.
    """
    return _ext_constant_year_policy_change_energy()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def year_policy_to_improve_efficiency():
    """
    Real Name: Year policy to improve efficiency
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'year_policy_to_improve_efficiency*')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Year when the policy to improve efficiency in sectors start. For each of
        five final energies.
    """
    return _ext_constant_year_policy_to_improve_efficiency()


@subs(["SECTORS H", "final sources"], _subscript_dict)
def year_to_finish_energy_intensity_policies():
    """
    Real Name: Year to finish energy intensity policies
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'year_to_finish_energy_intensity_policies*')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: ['SECTORS H', 'final sources']

    Year when the policy to improve efficiency in sectors finish.
    """
    return _ext_constant_year_to_finish_energy_intensity_policies()


def year_to_finish_policy_change_energy():
    """
    Real Name: Year to finish policy change energy
    Original Eqn: 2050
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when the policy to change final energy in the sectors finish.
    """
    return 2050


_ext_constant_choose_final_sectoral_energy_intensities_evolution_method = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C195",
    {},
    _root,
    "_ext_constant_choose_final_sectoral_energy_intensities_evolution_method",
)


_ext_constant_efficiency_rate_of_substitution = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_electricity*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["electricity"],
    },
    _root,
    "_ext_constant_efficiency_rate_of_substitution",
)


_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_heat*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["heat"],
    },
)


_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_liquids*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["liquids"],
    },
)


_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_gases*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["gases"],
    },
)


_ext_constant_efficiency_rate_of_substitution.add(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "efficiency_rate_of_substitution_solids*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
        "final sources1": ["solids"],
    },
)


_ext_constant_energy_intensity_target_mdollar = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "energy_intensity_target*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_energy_intensity_target_mdollar",
)


@subs(["sectors", "final sources"], _subscript_dict)
def _integ_init_evol_final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for evol_final_energy_intensity_by_sector_and_fuel
    Limits: None
    Type: setup
    Subs: ['sectors', 'final sources']

    Provides initial conditions for evol_final_energy_intensity_by_sector_and_fuel function
    """
    return rearrange(
        initial_energy_intensity_1995(), ["sectors", "final sources"], _subscript_dict
    )


@subs(["sectors", "final sources"], _subscript_dict)
def _integ_input_evol_final_energy_intensity_by_sector_and_fuel():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for evol_final_energy_intensity_by_sector_and_fuel
    Limits: None
    Type: component
    Subs: ['sectors', 'final sources']

    Provides derivative for evol_final_energy_intensity_by_sector_and_fuel function
    """
    return (
        increase_of_intensity_due_to_energy_a_technology_change_top_down()
        + inertial_rate_energy_intensity_top_down()
        + rate_change_intensity_bottom_up()
        - decrease_of_intensity_due_to_energy_a_technology_change_top_down()
    )


_integ_evol_final_energy_intensity_by_sector_and_fuel = Integ(
    _integ_input_evol_final_energy_intensity_by_sector_and_fuel,
    _integ_init_evol_final_energy_intensity_by_sector_and_fuel,
    "_integ_evol_final_energy_intensity_by_sector_and_fuel",
)


@subs(["final sources", "sectors"], _subscript_dict)
def _sample_if_true_init_final_energy_intensity_2020():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for final_energy_intensity_2020
    Limits: None
    Type: setup
    Subs: ['final sources', 'sectors']

    Provides initial conditions for final_energy_intensity_2020 function
    """
    return evol_final_energy_intensity_by_sector_and_fuel()


_sample_if_true_final_energy_intensity_2020 = SampleIfTrue(
    lambda: time() < year_energy_intensity_target(),
    lambda: evol_final_energy_intensity_by_sector_and_fuel(),
    _sample_if_true_init_final_energy_intensity_2020,
    "_sample_if_true_final_energy_intensity_2020",
)


_ext_constant_final_year_energy_intensity_target = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "final_year_energy_intensity_target",
    {},
    _root,
    "_ext_constant_final_year_energy_intensity_target",
)


_ext_lookup_historic_final_energy_intensity = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_electricity",
    {"final sources": ["electricity"], "SECTORS H": _subscript_dict["SECTORS H"]},
    _root,
    "_ext_lookup_historic_final_energy_intensity",
)


_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_heat",
    {"final sources": ["heat"], "SECTORS H": _subscript_dict["SECTORS H"]},
)


_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_liquids",
    {"final sources": ["liquids"], "SECTORS H": _subscript_dict["SECTORS H"]},
)


_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_gases",
    {"final sources": ["gases"], "SECTORS H": _subscript_dict["SECTORS H"]},
)


_ext_lookup_historic_final_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_final_energy_intensity_solids",
    {"final sources": ["solids"], "SECTORS H": _subscript_dict["SECTORS H"]},
)


_ext_constant_historic_mean_rate_energy_intensity = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_electricity*",
    {"SECTORS H": _subscript_dict["SECTORS H"], "final sources": ["electricity"]},
    _root,
    "_ext_constant_historic_mean_rate_energy_intensity",
)


_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_heat*",
    {"SECTORS H": _subscript_dict["SECTORS H"], "final sources": ["heat"]},
)


_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_liquids*",
    {"SECTORS H": _subscript_dict["SECTORS H"], "final sources": ["liquids"]},
)


_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_gases*",
    {"SECTORS H": _subscript_dict["SECTORS H"], "final sources": ["gases"]},
)


_ext_constant_historic_mean_rate_energy_intensity.add(
    "../economy.xlsx",
    "Europe",
    "historic_mean_rate_energy_intensity_solids*",
    {"SECTORS H": _subscript_dict["SECTORS H"], "final sources": ["solids"]},
)


_ext_constant_max_yearly_change_between_sources = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "max_yearly_change_between_sources*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_max_yearly_change_between_sources",
)


_ext_constant_maximum_yearly_acceleration_of_intensity_improvement = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "maximum_yearly_acceleration_of_intensity_improvement*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_maximum_yearly_acceleration_of_intensity_improvement",
)


_ext_constant_min_energy_intensity_vs_intial = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C199",
    {},
    _root,
    "_ext_constant_min_energy_intensity_vs_intial",
)


_ext_constant_minimum_fraction_source = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "minimum_fraction_source*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_minimum_fraction_source",
)


_ext_constant_policy_change_energy_speed = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "policy_change_energy_speed*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_policy_change_energy_speed",
)


_ext_constant_policy_to_improve_efficiency_speed = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "policy_to_improve_efficiency_speed*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_policy_to_improve_efficiency_speed",
)


_ext_constant_scarcity_feedback_final_fuel_replacement_flag = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "scarcity_feedback_final_fuel_replacement_flag",
    {},
    _root,
    "_ext_constant_scarcity_feedback_final_fuel_replacement_flag",
)


_ext_constant_year_policy_change_energy = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_policy_change_energy*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_policy_change_energy",
)


_ext_constant_year_policy_to_improve_efficiency = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_policy_to_improve_efficiency*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_policy_to_improve_efficiency",
)


_ext_constant_year_to_finish_energy_intensity_policies = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_to_finish_energy_intensity_policies*",
    {
        "SECTORS H": _subscript_dict["SECTORS H"],
        "final sources": _subscript_dict["final sources"],
    },
    _root,
    "_ext_constant_year_to_finish_energy_intensity_policies",
)
