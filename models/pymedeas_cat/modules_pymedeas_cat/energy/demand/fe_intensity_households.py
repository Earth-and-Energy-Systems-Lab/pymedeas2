"""
Module energy.demand.fe_intensity_households
Translated using PySD version 3.14.2
"""

@component.add(
    name="available_improvement_efficiency_H",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "min_energy_intensity_vs_intial_h": 2,
        "global_energy_intensity_h": 1,
        "initial_global_energy_intensity_2009": 2,
    },
)
def available_improvement_efficiency_h():
    """
    Remainig improvement of energy intensity respect to the minimum value.
    """
    return float(
        np.minimum(
            1,
            if_then_else(
                time() > 2009,
                lambda: zidz(
                    global_energy_intensity_h()
                    - min_energy_intensity_vs_intial_h()
                    * float(initial_global_energy_intensity_2009().loc["Households"]),
                    (1 - min_energy_intensity_vs_intial_h())
                    * float(initial_global_energy_intensity_2009().loc["Households"]),
                ),
                lambda: 1,
            ),
        )
    )


@component.add(
    name="change_total_intensity_to_rest",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3},
)
def change_total_intensity_to_rest():
    """
    Adjust to separate in 2009 among transport households and the rest in households. We assume that in 2009, 78% of the households liquids are from transport. This data is from WIOD (Diesel & gasoline from households is for transport) 1,245=0.78*1.596 For other sources, we asume 0% of the energy is for transport
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["liquids"]] = 1 - step(__data["time"], 0.78, 2009)
    value.loc[["gases"]] = 1 - step(__data["time"], 0.025, 2009)
    value.loc[["electricity"]] = 1 - step(__data["time"], 0.007, 2009)
    return value


@component.add(
    name="Choose_energy_intensity_target_method",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_energy_intensity_target_method"},
)
def choose_energy_intensity_target_method():
    """
    Choose energy intensity target method: 1- Energy intensity target defined by user 2- Variation in energy intensity over the intensity in defined year
    """
    return _ext_constant_choose_energy_intensity_target_method()


_ext_constant_choose_energy_intensity_target_method = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "choose_energy_intensity_target_method",
    {},
    _root,
    {},
    "_ext_constant_choose_energy_intensity_target_method",
)


@component.add(
    name="Decrease_of_intensity_due_to_change_energy_technology_H_TOP_DOWN",
    units="EJ/(year*Tdollars)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_final_energy_intensity_h": 2,
        "global_energy_intensity_h": 1,
        "minimum_fraction_source": 1,
        "pressure_to_change_energy_technology_h": 1,
        "max_yearly_change_between_sources": 1,
        "percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities": 1,
    },
)
def decrease_of_intensity_due_to_change_energy_technology_h_top_down():
    """
    When in households, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the decrease of (a). IF THEN ELSE((ZIDZ(Evol final energy intensity H[final sources], Global energy intensity H)) >= minimum fraction source[Households,final sources] ,max yearly change between sources[Households,final sources] *Evol final energy intensity H[final sources] * Pressure to change energy technology H [final sources], 0 )
    """
    return if_then_else(
        zidz(evol_final_energy_intensity_h(), global_energy_intensity_h())
        >= minimum_fraction_source().loc["Households", :].reset_coords(drop=True),
        lambda: (
            max_yearly_change_between_sources()
            .loc["Households", :]
            .reset_coords(drop=True)
            * (
                1
                + percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
            )
        )
        * evol_final_energy_intensity_h()
        * pressure_to_change_energy_technology_h(),
        lambda: xr.DataArray(
            0, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )


@component.add(
    name="EI_households_transport_delayed",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_ei_households_transport_delayed": 1},
    other_deps={
        "_delayfixed_ei_households_transport_delayed": {
            "initial": {"initial_households_energy_intensity": 1, "time_step": 1},
            "step": {"ei_households_transport": 1},
        }
    },
)
def ei_households_transport_delayed():
    return _delayfixed_ei_households_transport_delayed()


_delayfixed_ei_households_transport_delayed = DelayFixed(
    lambda: ei_households_transport(),
    lambda: time_step(),
    lambda: initial_households_energy_intensity(),
    time_step,
    "_delayfixed_ei_households_transport_delayed",
)


@component.add(
    name="Energy_intensity_of_households",
    units="EJ/Tdollars",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "energy_intensity_of_households_rest": 3,
        "activate_bottom_up_method": 1,
        "ei_households_transport_delayed": 1,
    },
)
def energy_intensity_of_households():
    """
    Energy intensity of households by final source
    """
    return if_then_else(
        time() < 2009,
        lambda: energy_intensity_of_households_rest(),
        lambda: if_then_else(
            float(activate_bottom_up_method().loc["Households"]) == 0,
            lambda: energy_intensity_of_households_rest(),
            lambda: ei_households_transport_delayed()
            + energy_intensity_of_households_rest(),
        ),
    )


@component.add(
    name="Energy_intensity_of_households_rest",
    units="EJ/Tdollar",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_bottom_up_method": 3,
        "evol_final_energy_intensity_h": 8,
        "change_total_intensity_to_rest": 3,
    },
)
def energy_intensity_of_households_rest():
    """
    Energy intensity of households by final source without considering the energy of transports for households
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["liquids"]] = if_then_else(
        float(activate_bottom_up_method().loc["Households"]) == 1,
        lambda: float(evol_final_energy_intensity_h().loc["liquids"])
        * float(change_total_intensity_to_rest().loc["liquids"]),
        lambda: float(evol_final_energy_intensity_h().loc["liquids"]),
    )
    value.loc[["solids"]] = float(evol_final_energy_intensity_h().loc["solids"])
    value.loc[["gases"]] = if_then_else(
        float(activate_bottom_up_method().loc["Households"]) == 1,
        lambda: float(evol_final_energy_intensity_h().loc["gases"])
        * float(change_total_intensity_to_rest().loc["gases"]),
        lambda: float(evol_final_energy_intensity_h().loc["gases"]),
    )
    value.loc[["electricity"]] = if_then_else(
        float(activate_bottom_up_method().loc["Households"]) == 1,
        lambda: float(evol_final_energy_intensity_h().loc["electricity"])
        * float(change_total_intensity_to_rest().loc["electricity"]),
        lambda: float(evol_final_energy_intensity_h().loc["electricity"]),
    )
    value.loc[["heat"]] = float(evol_final_energy_intensity_h().loc["heat"])
    return value


@component.add(
    name="Evol_final_energy_intensity_H",
    units="EJ/Tdollars",
    subscripts=["final_sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_evol_final_energy_intensity_h": 1},
    other_deps={
        "_integ_evol_final_energy_intensity_h": {
            "initial": {"initial_energy_intensity_1995": 1},
            "step": {
                "increase_of_intensity_due_to_change_energy_technology_h_top_down": 1,
                "inertial_rate_energy_intensity_h_top_down": 1,
                "decrease_of_intensity_due_to_change_energy_technology_h_top_down": 1,
            },
        }
    },
)
def evol_final_energy_intensity_h():
    """
    Energy intensity of households by final source. This variable models the dynamic evolution of the vetor of final energy intensities of the 5 types of final energy. The evolution of the intensities is considered to be due to two main effects: (1) the variation of the energy efficiency (flow due to the variable inertial rate energy intensity) and (2) the change of one type of final energy by another, As a consequence of a technological change (flow due to the variables Increase / decrease of intensity due to energy to technology change), as for example the change due to the electrification of the transport.
    """
    return _integ_evol_final_energy_intensity_h()


_integ_evol_final_energy_intensity_h = Integ(
    lambda: increase_of_intensity_due_to_change_energy_technology_h_top_down()
    + inertial_rate_energy_intensity_h_top_down()
    - decrease_of_intensity_due_to_change_energy_technology_h_top_down(),
    lambda: initial_energy_intensity_1995()
    .loc["Households", :]
    .reset_coords(drop=True),
    "_integ_evol_final_energy_intensity_h",
)


@component.add(
    name="Final_energy_intensity_2020_H",
    units="EJ/Tdollars",
    subscripts=["final_sources"],
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_final_energy_intensity_2020_h": 1},
    other_deps={
        "_sampleiftrue_final_energy_intensity_2020_h": {
            "initial": {"evol_final_energy_intensity_h": 1},
            "step": {
                "time": 1,
                "year_energy_intensity_target": 1,
                "evol_final_energy_intensity_h": 1,
            },
        }
    },
)
def final_energy_intensity_2020_h():
    """
    Energy intensity of households by final source in 2009
    """
    return _sampleiftrue_final_energy_intensity_2020_h()


_sampleiftrue_final_energy_intensity_2020_h = SampleIfTrue(
    lambda: xr.DataArray(
        time() < year_energy_intensity_target(),
        {"final_sources": _subscript_dict["final_sources"]},
        ["final_sources"],
    ),
    lambda: evol_final_energy_intensity_h(),
    lambda: evol_final_energy_intensity_h(),
    "_sampleiftrue_final_energy_intensity_2020_h",
)


@component.add(
    name="Fuel_scarcity_pressure_H",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_feedback_final_fuel_replacement_flag": 1,
        "perception_of_final_energy_scarcity_h": 1,
    },
)
def fuel_scarcity_pressure_h():
    """
    Pressure due significant variations in the fuel scarcity of each type of final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: perception_of_final_energy_scarcity_h(),
        lambda: xr.DataArray(
            0, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )


@component.add(
    name="Global_energy_intensity_H",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"evol_final_energy_intensity_h": 1},
)
def global_energy_intensity_h():
    """
    Global energy intensity of households considering the energy intensity of five final fuels.
    """
    return sum(
        evol_final_energy_intensity_h().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="Households_final_energy_demand",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "household_demand_total": 2,
        "energy_intensity_of_households": 2,
        "m_to_t": 2,
        "nvs_1_year": 2,
        "ccs_energy_demand_sect": 1,
        "ej_per_twh": 1,
    },
)
def households_final_energy_demand():
    """
    Final energy demand of households, taking into account the CCS energy demand
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["electricity"]] = False
    value.values[except_subs.values] = (
        household_demand_total()
        * energy_intensity_of_households()
        * m_to_t()
        / nvs_1_year()
    ).values[except_subs.values]
    value.loc[["electricity"]] = (
        household_demand_total()
        * float(energy_intensity_of_households().loc["electricity"])
        * m_to_t()
        / nvs_1_year()
        + float(ccs_energy_demand_sect().loc["Households"]) * ej_per_twh()
    )
    return value


@component.add(
    name="Increase_of_intensity_due_to_change_energy_technology_eff_H",
    units="EJ/(year*Tdollars)",
    subscripts=["final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_rate_of_substitution": 2,
        "increase_of_intensity_due_to_change_energy_technology_net_h": 2,
    },
)
def increase_of_intensity_due_to_change_energy_technology_eff_h():
    """
    Increase of intensity due to change a energy technology by fuel
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc["Households", :, :]
        .reset_coords(drop=True)
        .rename({"final_sources": "final_sources1", "final_sources1": "final_sources"})
        == 0,
        lambda: increase_of_intensity_due_to_change_energy_technology_net_h(),
        lambda: increase_of_intensity_due_to_change_energy_technology_net_h()
        * efficiency_rate_of_substitution()
        .loc["Households", :, :]
        .reset_coords(drop=True)
        .rename({"final_sources": "final_sources1", "final_sources1": "final_sources"}),
    )


@component.add(
    name="Increase_of_intensity_due_to_change_energy_technology_H_TOP_DOWN",
    units="EJ/(year*T$)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"increase_of_intensity_due_to_change_energy_technology_eff_h": 1},
)
def increase_of_intensity_due_to_change_energy_technology_h_top_down():
    """
    When in households, one type of energy (a) is replaced by another (b), the energy intensity of (b) will increase and the energy intensity of (a) will decrease. This flow represents the increase of (b). Decrease of intensity due to energy a technology change H TOP DOWN[solids]*efficiency rate of substitution[Households, liquids,solids]+Decrease of intensity due to energy a technology change H TOP DOWN[gases]*efficiency rate of substitution [Households,liquids,gases]+Decrease of intensity due to energy a technology change H TOP DOWN[electricity]*efficiency rate of substitution [Households,liquids,electricity]+Decrease of intensity due to energy a technology change H TOP DOWN[heat]*efficiency rate of substitution [Households,liquids,heat] ------ Decrease of intensity due to energy a technology change H TOP DOWN[solids]*efficiency rate of substitution[Households, gases,solids]+Decrease of intensity due to energy a technology change H TOP DOWN[electricity]*efficiency rate of substitution [Households,gases,electricity]+Decrease of intensity due to energy a technology change H TOP DOWN[heat]*efficiency rate of substitution [Households,gases,heat]+Decrease of intensity due to energy a technology change H TOP DOWN[liquids]*efficiency rate of substitution H,[gases,liquids] ----- Decrease of intensity due to energy a technology change H TOP DOWN[gases]*efficiency rate of substitution H[ solids,gases]+Decrease of intensity due to energy a technology change H TOP DOWN[electricity]*efficiency rate of substitution [Households,solids,electricity]+Decrease of intensity due to energy a technology change H TOP DOWN[heat]*efficiency rate of substitution [Households,solids,heat]+Decrease of intensity due to energy a technology change H TOP DOWN[liquids]*efficiency rate of substitution [Households,solids,liquids] ---- Decrease of intensity due to energy a technology change H TOP DOWN[solids]*efficiency rate of substitution[Households, electricity,solids]+Decrease of intensity due to energy a technology change H TOP DOWN[gases]*efficiency rate of substitution [Households,electricity,gases]+Decrease of intensity due to energy a technology change H TOP DOWN[heat]*efficiency rate of substitution [Households,electricity,heat]+Decrease of intensity due to energy a technology change H TOP DOWN[liquids]*efficiency rate of substitution [Households,electricity,liquids] -- Decrease of intensity due to energy a technology change H TOP DOWN[solids]*efficiency rate of substitution[Households, heat,solids]+Decrease of intensity due to energy a technology change H TOP DOWN[gases]*efficiency rate of substitution [Households,heat,gases]+Decrease of intensity due to energy a technology change H TOP DOWN[electricity]*efficiency rate of substitution [Households,heat,electricity]+Decrease of intensity due to energy a technology change H TOP DOWN[liquids]*efficiency rate of substitution [Households,heat,liquids]
    """
    return sum(
        increase_of_intensity_due_to_change_energy_technology_eff_h().rename(
            {"final_sources1": "final_sources", "final_sources": "final_sources1!"}
        ),
        dim=["final_sources1!"],
    )


@component.add(
    name="Increase_of_intensity_due_to_change_energy_technology_net_H",
    units="EJ/(year*Tdollars)",
    subscripts=["final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "decrease_of_intensity_due_to_change_energy_technology_h_top_down": 1,
        "share_tech_change_fuel_h": 1,
    },
)
def increase_of_intensity_due_to_change_energy_technology_net_h():
    """
    Increase of intensity due to change a energy technology without considering efficieny rate of susbsitution by fuel
    """
    return (
        decrease_of_intensity_due_to_change_energy_technology_h_top_down()
        * share_tech_change_fuel_h().transpose("final_sources", "final_sources1")
    ).transpose("final_sources1", "final_sources")


@component.add(
    name="inertial_rate_energy_intensity_H_TOP_DOWN",
    units="EJ/(year*Tdollars)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_rate_final_energy_intensity": 1,
        "choose_final_sectoral_energy_intensities_evolution_method": 2,
        "efficiency_energy_acceleration": 12,
        "historic_mean_rate_energy_intensity": 6,
        "initial_energy_intensity_1995": 4,
        "available_improvement_efficiency_h": 4,
        "variation_energy_intensity_target_h": 1,
        "evol_final_energy_intensity_h": 4,
        "year_energy_intensity_target": 1,
    },
)
def inertial_rate_energy_intensity_h_top_down():
    """
    This variable models the variation of the energy intensity according to the historical trend and represents the variation of the technological energy efficiency in households for each type of energy. By default it will follow the historical trend but can be modified by policies or market conditions that accelerate change.
    """
    return if_then_else(
        time() < 2009,
        lambda: historic_rate_final_energy_intensity()
        .loc["Households", :]
        .reset_coords(drop=True),
        lambda: if_then_else(
            choose_final_sectoral_energy_intensities_evolution_method() == 1,
            lambda: if_then_else(
                efficiency_energy_acceleration()
                .loc["Households", :]
                .reset_coords(drop=True)
                < 0,
                lambda: evol_final_energy_intensity_h()
                * efficiency_energy_acceleration()
                .loc["Households", :]
                .reset_coords(drop=True)
                * available_improvement_efficiency_h(),
                lambda: initial_energy_intensity_1995()
                .loc["Households", :]
                .reset_coords(drop=True)
                * efficiency_energy_acceleration()
                .loc["Households", :]
                .reset_coords(drop=True),
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: if_then_else(
                    historic_mean_rate_energy_intensity()
                    .loc["Households", :]
                    .reset_coords(drop=True)
                    + efficiency_energy_acceleration()
                    .loc["Households", :]
                    .reset_coords(drop=True)
                    < 0,
                    lambda: evol_final_energy_intensity_h()
                    * (
                        historic_mean_rate_energy_intensity()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        + efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                    )
                    * available_improvement_efficiency_h(),
                    lambda: initial_energy_intensity_1995()
                    .loc["Households", :]
                    .reset_coords(drop=True)
                    * (
                        historic_mean_rate_energy_intensity()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        + efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                    ),
                ),
                lambda: if_then_else(
                    choose_final_sectoral_energy_intensities_evolution_method() == 2,
                    lambda: if_then_else(
                        historic_mean_rate_energy_intensity()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        + efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        < 0,
                        lambda: evol_final_energy_intensity_h()
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc["Households", :]
                            .reset_coords(drop=True)
                            + efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True)
                        )
                        * available_improvement_efficiency_h(),
                        lambda: initial_energy_intensity_1995()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        * (
                            historic_mean_rate_energy_intensity()
                            .loc["Households", :]
                            .reset_coords(drop=True)
                            + efficiency_energy_acceleration()
                            .loc["Households", :]
                            .reset_coords(drop=True)
                        ),
                    ),
                    lambda: if_then_else(
                        efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        < 0,
                        lambda: evol_final_energy_intensity_h()
                        * efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        * available_improvement_efficiency_h(),
                        lambda: initial_energy_intensity_1995()
                        .loc["Households", :]
                        .reset_coords(drop=True)
                        * efficiency_energy_acceleration()
                        .loc["Households", :]
                        .reset_coords(drop=True),
                    )
                    + variation_energy_intensity_target_h(),
                ),
            ),
        ),
    )


@component.add(
    name="initial_households_energy_intensity",
    units="EJ/T$",
    subscripts=["final_sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_households_energy_intensity"},
)
def initial_households_energy_intensity():
    return _ext_constant_initial_households_energy_intensity()


_ext_constant_initial_households_energy_intensity = ExtConstant(
    r"../transport.xlsx",
    "Catalonia",
    "initial_ei_households_transport*",
    {"final_sources": _subscript_dict["final_sources"]},
    _root,
    {"final_sources": _subscript_dict["final_sources"]},
    "_ext_constant_initial_households_energy_intensity",
)


@component.add(
    name='"Inter-fuel_scarcity_pressure_H"',
    units="Dmnl",
    subscripts=["final_sources", "final_sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scarcity_feedback_final_fuel_replacement_flag": 1,
        "perception_of_interfuel_final_energy_scarcities_h": 1,
    },
)
def interfuel_scarcity_pressure_h():
    """
    Pressure due to variations in the inter-fuel scarcity of each type of final energy.
    """
    return if_then_else(
        scarcity_feedback_final_fuel_replacement_flag() == 1,
        lambda: np.maximum(0, perception_of_interfuel_final_energy_scarcities_h()),
        lambda: xr.DataArray(
            0,
            {
                "final_sources": _subscript_dict["final_sources"],
                "final_sources1": _subscript_dict["final_sources1"],
            },
            ["final_sources", "final_sources1"],
        ),
    )


@component.add(
    name="min_energy_intensity_vs_intial_H",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_min_energy_intensity_vs_intial_h"},
)
def min_energy_intensity_vs_intial_h():
    """
    Minimum value that the energy intensity for each economic sector could reach, obviously always above zero. This minimum value is very difficult to estimate, but based on historical values it has been considered that it can reach 30% of the value of 2009. (Capellán-Pérez et al., 2014)
    """
    return _ext_constant_min_energy_intensity_vs_intial_h()


_ext_constant_min_energy_intensity_vs_intial_h = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "min_FEI_vs_initial",
    {},
    _root,
    {},
    "_ext_constant_min_energy_intensity_vs_intial_h",
)


@component.add(
    name="pct_change_energy_intensity_target",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_pct_change_energy_intensity_target"},
)
def pct_change_energy_intensity_target():
    """
    In energy intensity target method option 2, the percentage of change in energy intensities over the given year
    """
    return _ext_constant_pct_change_energy_intensity_target()


_ext_constant_pct_change_energy_intensity_target = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "pct_change_energy_intensity_target",
    {},
    _root,
    {},
    "_ext_constant_pct_change_energy_intensity_target",
)


@component.add(
    name="Percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities"
    },
)
def percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities():
    """
    From the available data, the maximum historical variations of the energy intensities have been statistically estimated. If in the future these maximum variations are different, this variable establishes the percentage of variation that can occur over the defined data.
    """
    return (
        _ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities()
    )


_ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "p_change_over_hist_max_variation_FEI",
    {},
    _root,
    {},
    "_ext_constant_percentage_of_change_over_the_historic_maximun_variation_of_energy_intensities",
)


@component.add(
    name="Pressure_to_change_energy_technology_by_fuel_H",
    units="Dmnl",
    subscripts=["final_sources", "final_sources1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_rate_of_substitution": 1,
        "interfuel_scarcity_pressure_h": 2,
        "implementation_policy_to_change_final_energy": 1,
    },
)
def pressure_to_change_energy_technology_by_fuel_h():
    """
    This variable represents the pressure in households for substituting a final energy source for another. This pressure may be due to (1) energy policies, eg substitution of fossil fuels for electrical energy, or (2) by variations in the scarcity of each type of final energy.
    """
    return if_then_else(
        efficiency_rate_of_substitution()
        .loc["Households", :, :]
        .reset_coords(drop=True)
        == 0,
        lambda: np.minimum(np.maximum(interfuel_scarcity_pressure_h(), 0), 1),
        lambda: np.minimum(
            np.maximum(
                interfuel_scarcity_pressure_h()
                + implementation_policy_to_change_final_energy()
                .loc["Households", :]
                .reset_coords(drop=True)
                .rename({"final_sources": "final_sources1"}),
                0,
            ),
            1,
        ),
    )


@component.add(
    name="Pressure_to_change_energy_technology_H",
    units="Dmnl",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_to_change_energy_technology_by_fuel_h": 1},
)
def pressure_to_change_energy_technology_h():
    """
    This variable represents the pressure in households for substituting a final energy source for all the other energies.
    """
    return np.minimum(
        1,
        sum(
            pressure_to_change_energy_technology_by_fuel_h().rename(
                {"final_sources": "final_sources1!", "final_sources1": "final_sources"}
            ),
            dim=["final_sources1!"],
        ),
    )


@component.add(
    name="share_tech_change_fuel_H",
    units="Dmnl",
    subscripts=["final_sources1", "final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_to_change_energy_technology_by_fuel_h": 2},
)
def share_tech_change_fuel_h():
    """
    Share of the global pressure to change energy technology that corresponds to each fuel.
    """
    return zidz(
        pressure_to_change_energy_technology_by_fuel_h().rename(
            {"final_sources": "final_sources1", "final_sources1": "final_sources"}
        ),
        sum(
            pressure_to_change_energy_technology_by_fuel_h().rename(
                {"final_sources": "final_sources1!", "final_sources1": "final_sources"}
            ),
            dim=["final_sources1!"],
        ).expand_dims({"final_sources1": _subscript_dict["final_sources1"]}, 0),
    )


@component.add(
    name="start_year_modification_EI",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_modification_ei"},
)
def start_year_modification_ei():
    return _ext_constant_start_year_modification_ei()


_ext_constant_start_year_modification_ei = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_modification_EI",
    {},
    _root,
    {},
    "_ext_constant_start_year_modification_ei",
)


@component.add(
    name="Total_FED_households",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_final_energy_demand": 1},
)
def total_fed_households():
    """
    Final energy demand of households
    """
    return sum(
        households_final_energy_demand().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="Total_FED_transport_households",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"transport_households_final_energy_demand": 1},
)
def total_fed_transport_households():
    """
    Final energy in transport households
    """
    return sum(
        transport_households_final_energy_demand().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name="Transport_households_final_energy_demand",
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ei_households_transport_delayed": 1,
        "household_demand_total": 1,
        "m_to_t": 1,
        "nvs_1_year": 1,
    },
)
def transport_households_final_energy_demand():
    """
    Final energy in transport households
    """
    return (
        ei_households_transport_delayed()
        * household_demand_total()
        * m_to_t()
        / nvs_1_year()
    )


@component.add(
    name="Variation_energy_intensity_TARGET_H",
    units="EJ/(year*T$)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "choose_energy_intensity_target_method": 1,
        "energy_intensity_target": 1,
        "evol_final_energy_intensity_h": 2,
        "final_year_energy_intensity_target": 4,
        "year_energy_intensity_target": 2,
        "time": 6,
        "pct_change_energy_intensity_target": 1,
        "final_energy_intensity_2020_h": 1,
    },
)
def variation_energy_intensity_target_h():
    """
    Variation in energy intensity of households by final energy defined by user targets.
    """
    return if_then_else(
        choose_energy_intensity_target_method() == 1,
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: xr.DataArray(
                0,
                {"final_sources": _subscript_dict["final_sources"]},
                ["final_sources"],
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {"final_sources": _subscript_dict["final_sources"]},
                    ["final_sources"],
                ),
                lambda: (
                    energy_intensity_target()
                    .loc["Households", :]
                    .reset_coords(drop=True)
                    - evol_final_energy_intensity_h()
                )
                / (final_year_energy_intensity_target() - time()),
            ),
        ),
        lambda: if_then_else(
            time() >= final_year_energy_intensity_target(),
            lambda: xr.DataArray(
                0,
                {"final_sources": _subscript_dict["final_sources"]},
                ["final_sources"],
            ),
            lambda: if_then_else(
                time() < year_energy_intensity_target(),
                lambda: xr.DataArray(
                    0,
                    {"final_sources": _subscript_dict["final_sources"]},
                    ["final_sources"],
                ),
                lambda: (
                    final_energy_intensity_2020_h()
                    * (1 + pct_change_energy_intensity_target())
                    - evol_final_energy_intensity_h()
                )
                / (final_year_energy_intensity_target() - time()),
            ),
        ),
    )


@component.add(
    name="year_change_pct_energy_intensity_target",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_year_change_pct_energy_intensity_target"
    },
)
def year_change_pct_energy_intensity_target():
    """
    In energy intensity target method option 2, the year over which the energy intensities target is calculated
    """
    return _ext_constant_year_change_pct_energy_intensity_target()


_ext_constant_year_change_pct_energy_intensity_target = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_change_pct_energy_intensity_target",
    {},
    _root,
    {},
    "_ext_constant_year_change_pct_energy_intensity_target",
)


@component.add(
    name="year_energy_intensity_target",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "choose_energy_intensity_target_method": 1,
        "start_year_modification_ei": 1,
        "year_change_pct_energy_intensity_target": 1,
    },
)
def year_energy_intensity_target():
    """
    Year over which the energy intensities target is calculated
    """
    return if_then_else(
        choose_energy_intensity_target_method() == 1,
        lambda: start_year_modification_ei(),
        lambda: year_change_pct_energy_intensity_target(),
    )
