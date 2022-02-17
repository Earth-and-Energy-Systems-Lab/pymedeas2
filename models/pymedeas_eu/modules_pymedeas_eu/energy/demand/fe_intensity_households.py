"""
Module fe_intensity_households
Translated using PySD version 2.2.1
"""


def available_improvement_efficiency_h():
    """
    Real Name: available improvement efficiency H
    Original Eqn: MIN(1,IF THEN ELSE(Time>2009, ZIDZ( (Global energy intensity H-(min energy intensity vs intial H*Initial global energy intensity 2009[Households] )), (1-min energy intensity vs intial H)*Initial global energy intensity 2009[Households]), 1))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remainig improvement of energy intensity respect to the minimum value.
    """
    return np.minimum(
        1,
        if_then_else(
            time() > 2009,
            lambda: zidz(
                (
                    global_energy_intensity_h()
                    - (
                        min_energy_intensity_vs_intial_h()
                        * float(
                            initial_global_energy_intensity_2009().loc["Households"]
                        )
                    )
                ),
                (1 - min_energy_intensity_vs_intial_h())
                * float(initial_global_energy_intensity_2009().loc["Households"]),
            ),
            lambda: 1,
        ),
    )


@subs(["final sources"], _subscript_dict)
def change_total_intensity_to_rest():
    """
    Real Name: change total intensity to rest
    Original Eqn:
      1-STEP(0.78, 2009)
      1-STEP(0.025, 2009)
      1-STEP(0.007, 2009)
    Units: EJ/Tdollar
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Adjust to separate in 2009 among transport households and the rest in households. We
        assume that in 2009, 78% of the households liquids are from transport.
        This data is from WIOD (Diesel & gasoline from households is for
        transport) 1,245=0.78*1.596        For other sources, we asume 0% of the energy is for transport
    """
    return xrmerge(
        rearrange(
            1 - step(__data["time"], 0.78, 2009),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            1 - step(__data["time"], 0.025, 2009),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            1 - step(__data["time"], 0.007, 2009),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
    )


def choose_energy_intensity_target_method():
    """
    Real Name: Choose energy intensity target method
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'choose_energy_intensity_target_method')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Choose energy intensity target method:        1- Energy intensity target defined by user        2- Variation in energy intensity over the intensity in defined year
    """
    return _ext_constant_choose_energy_intensity_target_method()


@subs(["final sources"], _subscript_dict)
def decrease_of_intensity_due_to_change_energy_technology_h_top_down():
    """
    Real Name: Decrease of intensity due to change energy technology H TOP DOWN
    Original Eqn: IF THEN ELSE((ZIDZ(Evol final energy intensity H[final sources], Global energy intensity H)) >= minimum fraction source [Households,final sources],(max yearly change between sources[Households,final sources]*(1+Percentage of change over the historic maximun variation of energy intensities)) *Evol final energy intensity H[final sources] * Pressure to change energy technology H [final sources], 0 )
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    When in households, one type of energy (a) is replaced by another (b), the energy
        intensity of (b) will increase and the energy intensity of (a) will
        decrease. This flow represents the decrease of (a).                IF THEN ELSE((ZIDZ(Evol final energy intensity H[final sources], Global energy
        intensity H)) >= minimum fraction source[Households,final sources]        ,max yearly change between sources[Households,final sources]  *Evol final energy
        intensity H[final sources] * Pressure to change energy technology H        [final sources], 0 )
    """
    return if_then_else(
        (zidz(evol_final_energy_intensity_h(), global_energy_intensity_h()))
        >= rearrange(
            minimum_fraction_source().loc["Households", :].reset_coords(drop=True),
            ["final sources"],
            _subscript_dict,
        ),
        lambda: (
            rearrange(
                max_yearly_change_between_sources()
                .loc["Households", :]
                .reset_coords(drop=True),
                ["final sources"],
                _subscript_dict,
            )
            * (
                1
                + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
            )
        )
        * evol_final_energy_intensity_h()
        * pressure_to_change_energy_technology_h(),
        lambda: 0,
    )


@subs(["final sources"], _subscript_dict)
def energy_intensity_of_households():
    """
    Real Name: Energy intensity of households
    Original Eqn: IF THEN ELSE(Time<2009,Energy intensity of households rest[final sources], IF THEN ELSE(Activate BOTTOM UP method[Households]=0,Energy intensity of households rest[final sources],Energy intensity of households transport [final sources]+Energy intensity of households rest[final sources]))
    Units: EJ/Tdollar
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Energy intensity of households by final source
    """
    return if_then_else(
        time() < 2009,
        lambda: energy_intensity_of_households_rest(),
        lambda: if_then_else(
            float(activate_bottom_up_method().loc["Households"]) == 0,
            lambda: energy_intensity_of_households_rest(),
            lambda: energy_intensity_of_households_transport()
            + energy_intensity_of_households_rest(),
        ),
    )


@subs(["final sources"], _subscript_dict)
def evol_final_energy_intensity_h():
    """
    Real Name: Evol final energy intensity H
    Original Eqn: INTEG ( Increase of intensity due to change energy technology H TOP DOWN[final sources ]+inertial rate energy intensity H TOP DOWN[final sources]-Decrease of intensity due to change energy technology H TOP DOWN [final sources], Initial energy intensity 1995[Households,final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Energy intensity of households by final source. This variable models the
        dynamic evolution of the vetor of final energy intensities of the 5 types
        of final energy. The evolution of the intensities is considered to be due
        to two main effects: (1) the variation of the energy efficiency (flow due
        to the variable inertial rate energy intensity) and (2) the change of one
        type of final energy by another, As a consequence of a technological
        change (flow due to the variables Increase / decrease of intensity due to
        energy to technology change), as for example the change due to the
        electrification of the transport.
    """
    return _integ_evol_final_energy_intensity_h()


@subs(["final sources"], _subscript_dict)
def final_energy_intensity_2020_h():
    """
    Real Name: Final energy intensity 2020 H
    Original Eqn: SAMPLE IF TRUE(Time<year energy intensity target,Evol final energy intensity H[final sources],Evol final energy intensity H[final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Energy intensity of households by final source in 2009
    """
    return _sample_if_true_final_energy_intensity_2020_h()


@subs(["final sources"], _subscript_dict)
def fuel_scarcity_pressure_h():
    """
    Real Name: Fuel scarcity pressure H
    Original Eqn: IF THEN ELSE(scarcity feedback final fuel replacement flag=1,perception of final energy scarcity H[ final sources],0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Pressure due significant variations in the fuel scarcity of each type of
        final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: perception_of_final_energy_scarcity_h(),
        lambda: 0,
    )


@subs(["final sources"], _subscript_dict)
def energy_intensity_of_households_rest():
    """
    Real Name: Energy intensity of households rest
    Original Eqn:
      IF THEN ELSE(Activate BOTTOM UP method[Households]=1,Evol final energy intensity H[liquids]*change total intensity to rest[liquids],Evol final energy intensity H[liquids])
      Evol final energy intensity H[solids]
      IF THEN ELSE(Activate BOTTOM UP method[Households]=1,Evol final energy intensity H[gases]*change total intensity to rest [gases],Evol final energy intensity H[gases])
      IF THEN ELSE(Activate BOTTOM UP method[Households]=1,Evol final energy intensity H[electricity ]*change total intensity to rest[electricity],Evol final energy intensity H[electricity])
      Evol final energy intensity H[heat]
    Units: EJ/Tdollar
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Energy intensity of households by final source without considering the
        energy of transports for households
    """
    return xrmerge(
        rearrange(
            if_then_else(
                float(activate_bottom_up_method().loc["Households"]) == 1,
                lambda: float(evol_final_energy_intensity_h().loc["liquids"])
                * float(change_total_intensity_to_rest().loc["liquids"]),
                lambda: float(evol_final_energy_intensity_h().loc["liquids"]),
            ),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(evol_final_energy_intensity_h().loc["solids"]),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
        rearrange(
            if_then_else(
                float(activate_bottom_up_method().loc["Households"]) == 1,
                lambda: float(evol_final_energy_intensity_h().loc["gases"])
                * float(change_total_intensity_to_rest().loc["gases"]),
                lambda: float(evol_final_energy_intensity_h().loc["gases"]),
            ),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            if_then_else(
                float(activate_bottom_up_method().loc["Households"]) == 1,
                lambda: float(evol_final_energy_intensity_h().loc["electricity"])
                * float(change_total_intensity_to_rest().loc["electricity"]),
                lambda: float(evol_final_energy_intensity_h().loc["electricity"]),
            ),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(evol_final_energy_intensity_h().loc["heat"]),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
    )


def global_energy_intensity_h():
    """
    Real Name: Global energy intensity H
    Original Eqn: SUM(Evol final energy intensity H[final sources!])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Global energy intensity of households considering the energy intensity of
        five final fuels.
    """
    return sum(evol_final_energy_intensity_h(), dim=("final sources",))


@subs(["final sources"], _subscript_dict)
def households_final_energy_demand():
    """
    Real Name: Households final energy demand
    Original Eqn: Household demand total*Energy intensity of households[final sources]/1e+06
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Final energy demand of households
    """
    return household_demand_total() * energy_intensity_of_households() / 1e06


@subs(["final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_change_energy_technology_eff_h():
    """
    Real Name: Increase of intensity due to change energy technology eff H
    Original Eqn: IF THEN ELSE(efficiency rate of substitution[Households,final sources1,final sources]=0,Increase of intensity due to change energy technology net H [final sources1,final sources],Increase of intensity due to change energy technology net H[final sources1,final sources]*efficiency rate of substitution[Households,final sources1,final sources])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources1', 'final sources']

    Increase of intensity due to change a energy technology by fuel
    """
    return if_then_else(
        rearrange(
            efficiency_rate_of_substitution()
            .loc["Households", :, :]
            .reset_coords(drop=True),
            ["final sources1", "final sources"],
            _subscript_dict,
        )
        == 0,
        lambda: increase_of_intensity_due_to_change_energy_technology_net_h(),
        lambda: increase_of_intensity_due_to_change_energy_technology_net_h()
        * rearrange(
            efficiency_rate_of_substitution()
            .loc["Households", :, :]
            .reset_coords(drop=True),
            ["final sources1", "final sources"],
            _subscript_dict,
        ),
    )


@subs(["final sources"], _subscript_dict)
def increase_of_intensity_due_to_change_energy_technology_h_top_down():
    """
    Real Name: Increase of intensity due to change energy technology H TOP DOWN
    Original Eqn: SUM(Increase of intensity due to change energy technology eff H[final sources,final sources1!])
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    When in households, one type of energy (a) is replaced by another (b), the energy
        intensity of (b) will increase and the energy intensity of (a) will
        decrease. This flow represents the increase of (b).                Decrease of intensity due to energy a technology change H TOP
        DOWN[solids]*efficiency rate of substitution[Households,        liquids,solids]+Decrease of intensity due to energy a technology change H TOP
        DOWN[gases]*efficiency rate of substitution        [Households,liquids,gases]+Decrease of intensity due to energy a technology change H
        TOP DOWN[electricity]*efficiency rate of substitution        [Households,liquids,electricity]+Decrease of intensity due to energy a technology
        change H TOP DOWN[heat]*efficiency rate of substitution        [Households,liquids,heat]                        ------                Decrease of intensity due to energy a technology change H TOP
        DOWN[solids]*efficiency rate of substitution[Households,        gases,solids]+Decrease of intensity due to energy a technology change H TOP
        DOWN[electricity]*efficiency rate of substitution        [Households,gases,electricity]+Decrease of intensity due to energy a technology
        change H TOP DOWN[heat]*efficiency rate of substitution        [Households,gases,heat]+Decrease of intensity due to energy a technology change H
        TOP DOWN[liquids]*efficiency rate of substitution        [Households,gases,liquids]                -----                Decrease of intensity due to energy a technology change H TOP DOWN[gases]*efficiency
        rate of substitution[Households,        solids,gases]+Decrease of intensity due to energy a technology change H TOP
        DOWN[electricity]*efficiency rate of substitution        [Households,solids,electricity]+Decrease of intensity due to energy a technology
        change H TOP DOWN[heat]*efficiency rate of substitution        [Households,solids,heat]+Decrease of intensity due to energy a technology change H
        TOP DOWN[liquids]*efficiency rate of substitution        [Households,solids,liquids]                ----                Decrease of intensity due to energy a technology change H TOP
        DOWN[solids]*efficiency rate of substitution[Households,        electricity,solids]+Decrease of intensity due to energy a technology change H TOP
        DOWN[gases]*efficiency rate of substitution        [Households,electricity,gases]+Decrease of intensity due to energy a technology
        change H TOP DOWN[heat]*efficiency rate of substitution        [Households,electricity,heat]+Decrease of intensity due to energy a technology
        change H TOP DOWN[liquids]*efficiency rate of substitution        [Households,electricity,liquids]                --                Decrease of intensity due to energy a technology change H TOP
        DOWN[solids]*efficiency rate of substitution[Households,        heat,solids]+Decrease of intensity due to energy a technology change H TOP
        DOWN[gases]*efficiency rate of substitution        [Households,heat,gases]+Decrease of intensity due to energy a technology change H
        TOP DOWN[electricity]*efficiency rate of substitution        [Households,heat,electricity]+Decrease of intensity due to energy a technology
        change H TOP DOWN[liquids]*efficiency rate of substitution        [Households,heat,liquids]
    """
    return sum(
        rearrange(
            increase_of_intensity_due_to_change_energy_technology_eff_h(),
            ["final sources", "final sources1"],
            _subscript_dict,
        ),
        dim=("final sources1",),
    )


@subs(["final sources1", "final sources"], _subscript_dict)
def increase_of_intensity_due_to_change_energy_technology_net_h():
    """
    Real Name: Increase of intensity due to change energy technology net H
    Original Eqn: Decrease of intensity due to change energy technology H TOP DOWN[final sources]*share tech change fuel H[final sources1,final sources]
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources1', 'final sources']

    Increase of intensity due to change a energy technology without
        considering efficieny rate of susbsitution by fuel
    """
    return (
        decrease_of_intensity_due_to_change_energy_technology_h_top_down()
        * share_tech_change_fuel_h()
    )


@subs(["final sources"], _subscript_dict)
def inertial_rate_energy_intensity_h_top_down():
    """
    Real Name: inertial rate energy intensity H TOP DOWN
    Original Eqn: IF THEN ELSE(Time<2009, historic rate final energy intensity[Households,final sources],IF THEN ELSE(Choose final sectoral energy intensities evolution method =1,IF THEN ELSE(Efficiency energy acceleration[Households,final sources]<0,Evol final energy intensity H[ final sources]*Efficiency energy acceleration[Households,final sources]*available improvement efficiency H, Initial energy intensity 1995 [Households,final sources] *Efficiency energy acceleration[Households,final sources]), IF THEN ELSE(Time<year energy intensity target,IF THEN ELSE((historic mean rate energy intensity[Households,final sources ]+Efficiency energy acceleration[Households,final sources])<0,Evol final energy intensity H[final sources]*(historic mean rate energy intensity [Households,final sources] +Efficiency energy acceleration[Households,final sources])*available improvement efficiency H,Initial energy intensity 1995 [Households,final sources] *(historic mean rate energy intensity[Households,final sources]+Efficiency energy acceleration[Households,final sources])), IF THEN ELSE(Choose final sectoral energy intensities evolution method=2,IF THEN ELSE((historic mean rate energy intensity [Households,final sources]+Efficiency energy acceleration[Households,final sources])<0,Evol final energy intensity H[final sources ]*(historic mean rate energy intensity[Households,final sources] +Efficiency energy acceleration[Households,final sources])*available improvement efficiency H,Initial energy intensity 1995 [Households,final sources] *(historic mean rate energy intensity[Households,final sources]+Efficiency energy acceleration[Households,final sources])),IF THEN ELSE ((Efficiency energy acceleration[Households,final sources])<0,Evol final energy intensity H[final sources]*Efficiency energy acceleration [Households,final sources]*available improvement efficiency H,Initial energy intensity 1995[Households,final sources] *Efficiency energy acceleration[Households,final sources])+Variation energy intensity TARGET H[final sources] ))))
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    This variable models the variation of the energy intensity according to
        the historical trend and represents the variation of the technological
        energy efficiency in households for each type of energy. By default it
        will follow the historical trend but can be modified by policies or market
        conditions that accelerate change.
    """
    return if_then_else(
        time() < 2009,
        lambda: rearrange(
            historic_rate_final_energy_intensity()
            .loc["Households", :]
            .reset_coords(drop=True),
            ["final sources"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            choose_final_sectoral_energy_intensities_evolution_method() == 1,
            lambda: if_then_else(
                rearrange(
                    efficiency_energy_acceleration()
                    .loc["Households", :]
                    .reset_coords(drop=True),
                    ["final sources"],
                    _subscript_dict,
                )
                < 0,
                lambda: evol_final_energy_intensity_h()
                * rearrange(
                    efficiency_energy_acceleration()
                    .loc["Households", :]
                    .reset_coords(drop=True),
                    ["final sources"],
                    _subscript_dict,
                )
                * available_improvement_efficiency_h(),
                lambda: rearrange(
                    initial_energy_intensity_1995()
                    .loc["Households", :]
                    .reset_coords(drop=True),
                    ["final sources"],
                    _subscript_dict,
                )
                * rearrange(
                    efficiency_energy_acceleration()
                    .loc["Households", :]
                    .reset_coords(drop=True),
                    ["final sources"],
                    _subscript_dict,
                ),
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: if_then_else(
                    (
                        rearrange(
                            historic_mean_rate_energy_intensity()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        + rearrange(
                            efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                    )
                    < 0,
                    lambda: evol_final_energy_intensity_h()
                    * (
                        rearrange(
                            historic_mean_rate_energy_intensity()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        + rearrange(
                            efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                    )
                    * available_improvement_efficiency_h(),
                    lambda: rearrange(
                        initial_energy_intensity_1995()
                        .loc["Households", :]
                        .reset_coords(drop=True),
                        ["final sources"],
                        _subscript_dict,
                    )
                    * (
                        rearrange(
                            historic_mean_rate_energy_intensity()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        + rearrange(
                            efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                    ),
                ),
                lambda: if_then_else(
                    choose_final_sectoral_energy_intensities_evolution_method() == 2,
                    lambda: if_then_else(
                        (
                            rearrange(
                                historic_mean_rate_energy_intensity()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                        )
                        < 0,
                        lambda: evol_final_energy_intensity_h()
                        * (
                            rearrange(
                                historic_mean_rate_energy_intensity()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                        )
                        * available_improvement_efficiency_h(),
                        lambda: rearrange(
                            initial_energy_intensity_1995()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        * (
                            rearrange(
                                historic_mean_rate_energy_intensity()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                            + rearrange(
                                efficiency_energy_acceleration()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                        ),
                    ),
                    lambda: if_then_else(
                        (
                            rearrange(
                                efficiency_energy_acceleration()
                                .loc["Households", :]
                                .reset_coords(drop=True),
                                ["final sources"],
                                _subscript_dict,
                            )
                        )
                        < 0,
                        lambda: evol_final_energy_intensity_h()
                        * rearrange(
                            efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        * available_improvement_efficiency_h(),
                        lambda: rearrange(
                            initial_energy_intensity_1995()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        * rearrange(
                            efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        ),
                    )
                    + variation_energy_intensity_target_h(),
                ),
            ),
        ),
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def interfuel_scarcity_pressure_h():
    """
    Real Name: "Inter-fuel scarcity pressure H"
    Original Eqn: IF THEN ELSE(scarcity feedback final fuel replacement flag=1,MAX(0,"perception of inter-fuel final energy scarcities H" [final sources,final sources1]),0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'final sources1']

    Pressure due to variations in the inter-fuel scarcity of each type of
        final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: np.maximum(0, perception_of_interfuel_final_energy_scarcities_h()),
        lambda: 0,
    )


def min_energy_intensity_vs_intial_h():
    """
    Real Name: min energy intensity vs intial H
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'min_FEI_vs_initial')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Minimum value that the energy intensity for each economic sector could
        reach, obviously always above zero. This minimum value is very difficult
        to estimate, but based on historical values it has been considered that it
        can reach 30% of the value of 2009. (Capellán-Pérez et al., 2014)
    """
    return _ext_constant_min_energy_intensity_vs_intial_h()


def pct_change_energy_intensity_target():
    """
    Real Name: pct change energy intensity target
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'pct_change_energy_intensity_target')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    In energy intensity target method option 2, the percentage of change in
        energy intensities over the given year
    """
    return _ext_constant_pct_change_energy_intensity_target()


def percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities():
    """
    Real Name: Percentage of change over the historic maximun variation of energy intensities
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'p_change_over_hist_max_variation_FEI')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    From the available data, the maximum historical variations of the energy
        intensities have been statistically estimated. If in the future these
        maximum variations are different, this variable establishes the percentage
        of variation that can occur over the defined data.
    """
    return (
        _ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
    )


@subs(["final sources", "final sources1"], _subscript_dict)
def pressure_to_change_energy_technology_by_fuel_h():
    """
    Real Name: Pressure to change energy technology by fuel H
    Original Eqn: IF THEN ELSE(efficiency rate of substitution[Households,final sources,final sources1]=0,MIN(MAX("Inter-fuel scarcity pressure H" [final sources,final sources1],0),1),MIN(MAX("Inter-fuel scarcity pressure H"[final sources,final sources1 ] + Implementation policy to change final energy [Households,final sources1], 0), 1 ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'final sources1']

    This variable represents the pressure in households for substituting a
        final energy source for another. This pressure may be due to (1) energy
        policies, eg substitution of fossil fuels for electrical energy, or (2) by
        variations in the scarcity of each type of final energy.
    """
    return if_then_else(
        rearrange(
            efficiency_rate_of_substitution()
            .loc["Households", :, :]
            .reset_coords(drop=True),
            ["final sources", "final sources1"],
            _subscript_dict,
        )
        == 0,
        lambda: np.minimum(np.maximum(interfuel_scarcity_pressure_h(), 0), 1),
        lambda: np.minimum(
            np.maximum(
                interfuel_scarcity_pressure_h()
                + rearrange(
                    implementation_policy_to_change_final_energy()
                    .loc["Households", :]
                    .reset_coords(drop=True),
                    ["final sources1"],
                    _subscript_dict,
                ),
                0,
            ),
            1,
        ),
    )


@subs(["final sources"], _subscript_dict)
def pressure_to_change_energy_technology_h():
    """
    Real Name: Pressure to change energy technology H
    Original Eqn: MIN(1,SUM(Pressure to change energy technology by fuel H[final sources1!,final sources]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    This variable represents the pressure in households for substituting a
        final energy source for all the other energies.
    """
    return np.minimum(
        1,
        sum(
            rearrange(
                pressure_to_change_energy_technology_by_fuel_h(),
                ["final sources1", "final sources"],
                _subscript_dict,
            ),
            dim=("final sources1",),
        ),
    )


@subs(["final sources1", "final sources"], _subscript_dict)
def share_tech_change_fuel_h():
    """
    Real Name: share tech change fuel H
    Original Eqn: ZIDZ( Pressure to change energy technology by fuel H[final sources1,final sources], SUM(Pressure to change energy technology by fuel H[final sources1!,final sources]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources1', 'final sources']

    Share of the global pressure to change energy technology that corresponds
        to each fuel.
    """
    return zidz(
        rearrange(
            pressure_to_change_energy_technology_by_fuel_h(),
            ["final sources1", "final sources"],
            _subscript_dict,
        ),
        sum(
            rearrange(
                pressure_to_change_energy_technology_by_fuel_h(),
                ["final sources1", "final sources"],
                _subscript_dict,
            ),
            dim=("final sources1",),
        ),
    )


def start_year_modification_ei():
    """
    Real Name: start year modification EI
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_modification_EI')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_start_year_modification_ei()


def total_fed_households():
    """
    Real Name: Total FED households
    Original Eqn: SUM(Households final energy demand[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy demand of households
    """
    return sum(households_final_energy_demand(), dim=("final sources",))


def total_fed_trasnport_households():
    """
    Real Name: Total FED trasnport households
    Original Eqn: SUM(Transport households final energy demand[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy in transport households
    """
    return sum(transport_households_final_energy_demand(), dim=("final sources",))


@subs(["final sources"], _subscript_dict)
def transport_households_final_energy_demand():
    """
    Real Name: Transport households final energy demand
    Original Eqn: Energy intensity of households transport[final sources]*Household demand total/1e+06
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Final energy in transport households
    """
    return energy_intensity_of_households_transport() * household_demand_total() / 1e06


@subs(["final sources"], _subscript_dict)
def variation_energy_intensity_target_h():
    """
    Real Name: Variation energy intensity TARGET H
    Original Eqn: IF THEN ELSE(Choose energy intensity target method=1,IF THEN ELSE(Time>=final year energy intensity target,0,IF THEN ELSE(Time<year energy intensity target,0,((Energy intensity target[Households,final sources]-Evol final energy intensity H[final sources])/(final year energy intensity target-Time)))),IF THEN ELSE(Time>=final year energy intensity target ,0,IF THEN ELSE(Time<year energy intensity target,0,((Final energy intensity 2020 H[final sources]*(1+pct change energy intensity target)-Evol final energy intensity H[final sources])/(final year energy intensity target-Time)))))
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Variation in energy intensity of households by final energy defined by
        user targets.
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
                            energy_intensity_target()
                            .loc["Households", :]
                            .reset_coords(drop=True),
                            ["final sources"],
                            _subscript_dict,
                        )
                        - evol_final_energy_intensity_h()
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
                        final_energy_intensity_2020_h()
                        * (1 + pct_change_energy_intensity_target())
                        - evol_final_energy_intensity_h()
                    )
                    / (final_year_energy_intensity_target() - time())
                ),
            ),
        ),
    )


def year_change_pct_energy_intensity_target():
    """
    Real Name: year change pct energy intensity target
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'year_change_pct_energy_intensity_target')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    In energy intensity target method option 2, the year over which the energy
        intensities target is calculated
    """
    return _ext_constant_year_change_pct_energy_intensity_target()


def year_energy_intensity_target():
    """
    Real Name: year energy intensity target
    Original Eqn: IF THEN ELSE(Choose energy intensity target method=1, start year modification EI, year change pct energy intensity target)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year over which the energy intensities target is calculated
    """
    return if_then_else(
        choose_energy_intensity_target_method() == 1,
        lambda: start_year_modification_ei(),
        lambda: year_change_pct_energy_intensity_target(),
    )


_ext_constant_choose_energy_intensity_target_method = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "choose_energy_intensity_target_method",
    {},
    _root,
    "_ext_constant_choose_energy_intensity_target_method",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_evol_final_energy_intensity_h():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for evol_final_energy_intensity_h
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for evol_final_energy_intensity_h function
    """
    return rearrange(
        initial_energy_intensity_1995().loc["Households", :].reset_coords(drop=True),
        ["final sources"],
        _subscript_dict,
    )


@subs(["final sources"], _subscript_dict)
def _integ_input_evol_final_energy_intensity_h():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for evol_final_energy_intensity_h
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for evol_final_energy_intensity_h function
    """
    return (
        increase_of_intensity_due_to_change_energy_technology_h_top_down()
        + inertial_rate_energy_intensity_h_top_down()
        - decrease_of_intensity_due_to_change_energy_technology_h_top_down()
    )


_integ_evol_final_energy_intensity_h = Integ(
    _integ_input_evol_final_energy_intensity_h,
    _integ_init_evol_final_energy_intensity_h,
    "_integ_evol_final_energy_intensity_h",
)


@subs(["final sources"], _subscript_dict)
def _sample_if_true_init_final_energy_intensity_2020_h():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for final_energy_intensity_2020_h
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for final_energy_intensity_2020_h function
    """
    return evol_final_energy_intensity_h()


_sample_if_true_final_energy_intensity_2020_h = SampleIfTrue(
    lambda: time() < year_energy_intensity_target(),
    lambda: evol_final_energy_intensity_h(),
    _sample_if_true_init_final_energy_intensity_2020_h,
    "_sample_if_true_final_energy_intensity_2020_h",
)


_ext_constant_min_energy_intensity_vs_intial_h = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "min_FEI_vs_initial",
    {},
    _root,
    "_ext_constant_min_energy_intensity_vs_intial_h",
)


_ext_constant_pct_change_energy_intensity_target = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "pct_change_energy_intensity_target",
    {},
    _root,
    "_ext_constant_pct_change_energy_intensity_target",
)


_ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_change_over_hist_max_variation_FEI",
    {},
    _root,
    "_ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities",
)


_ext_constant_start_year_modification_ei = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_modification_EI",
    {},
    _root,
    "_ext_constant_start_year_modification_ei",
)


_ext_constant_year_change_pct_energy_intensity_target = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_change_pct_energy_intensity_target",
    {},
    _root,
    "_ext_constant_year_change_pct_energy_intensity_target",
)
