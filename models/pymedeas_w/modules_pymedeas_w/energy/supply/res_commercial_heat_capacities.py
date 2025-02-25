"""
Module energy.supply.res_commercial_heat_capacities
Translated using PySD version 3.14.0
"""

@component.add(
    name='"abundance RES heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_after_priorities": 3,
        "fe_real_supply_res_for_heatcom_tot": 1,
    },
)
def abundance_res_heatcom():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that heat generation from RES is far to cover to whole heat demand, if "abundance RES heat"=0 it means that RES heat cover the whole heat demand. IF THEN ELSE(Total FED Heat EJ delayed 1yr=0,0, IF THEN ELSE(Total FED Heat EJ delayed 1yr > FE real supply RES for heat tot EJ, (Total FED Heat EJ delayed 1yr-FE real supply RES for heat tot EJ)/Total FED Heat EJ delayed 1yr, 0))
    """
    return if_then_else(
        fed_heatcom_after_priorities() == 0,
        lambda: 0,
        lambda: zidz(
            fed_heatcom_after_priorities() - fe_real_supply_res_for_heatcom_tot(),
            fed_heatcom_after_priorities(),
        ),
    )


@component.add(
    name='"abundance RES heat-com2"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_res_heatcom": 1},
)
def abundance_res_heatcom2():
    """
    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_heatcom())


@component.add(
    name='"adapt growth RES for heat-com"',
    units="1/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "past_res_growth_for_heatcom": 3,
        "p_res_for_heat": 2,
        "start_year_p_growth_res_heat": 2,
    },
)
def adapt_growth_res_for_heatcom():
    """
    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2014,
        lambda: past_res_growth_for_heatcom(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_heat(),
            lambda: past_res_growth_for_heatcom()
            + (p_res_for_heat() - past_res_growth_for_heatcom())
            * (time() - 2014)
            / (start_year_p_growth_res_heat() - 2014),
            lambda: p_res_for_heat(),
        ),
    )


@component.add(
    name="Efficiency conversion BioE plants to heat",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_efficiency_conversion_bioe_plants_to_heat"
    },
)
def efficiency_conversion_bioe_plants_to_heat():
    """
    Efficiency of the transformation from bioenergy to heat in heat and CHP plants (aggregated). Efficiency of the transformation from bioenergy to electricity (estimation for 2014 from the IEA balances.
    """
    return _ext_constant_efficiency_conversion_bioe_plants_to_heat()


_ext_constant_efficiency_conversion_bioe_plants_to_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_plants_to_heat",
    {},
    _root,
    {},
    "_ext_constant_efficiency_conversion_bioe_plants_to_heat",
)


@component.add(
    name="Efficiency geothermal for heat",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_geothermal_for_heat"},
)
def efficiency_geothermal_for_heat():
    return _ext_constant_efficiency_geothermal_for_heat()


_ext_constant_efficiency_geothermal_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_geothermal_for_heat",
    {},
    _root,
    {},
    "_ext_constant_efficiency_geothermal_for_heat",
)


@component.add(
    name="Efficiency RES heat",
    units="Dmnl",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "losses_solar_for_heat": 1,
        "efficiency_geothermal_for_heat": 1,
        "efficiency_conversion_bioe_plants_to_heat": 1,
    },
)
def efficiency_res_heat():
    """
    Efficiency solar panels for heat*(1-Losses solar for heat)
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, [np.str_("RES heat")]
    )
    value.loc[["solar heat"]] = 1 - losses_solar_for_heat()
    value.loc[["geot heat"]] = efficiency_geothermal_for_heat()
    value.loc[["solid bioE heat"]] = efficiency_conversion_bioe_plants_to_heat()
    return value


@component.add(
    name="Efficiency solar panels for heat",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_solar_panels_for_heat"},
)
def efficiency_solar_panels_for_heat():
    return _ext_constant_efficiency_solar_panels_for_heat()


_ext_constant_efficiency_solar_panels_for_heat = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_solar_panels_for_heat",
    {},
    _root,
    {},
    "_ext_constant_efficiency_solar_panels_for_heat",
)


@component.add(
    name='"FE real generation RES heat-com EJ"',
    units="EJ/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatcom": 1, "res_heatcom_tot_overcapacity": 1},
)
def fe_real_generation_res_heatcom_ej():
    """
    Commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatcom() * (1 - res_heatcom_tot_overcapacity())


@component.add(
    name='"FE real supply RES for heat-com tot"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_heatcom_after_priorities": 1,
        "potential_fes_tot_res_for_heatcom": 1,
    },
)
def fe_real_supply_res_for_heatcom_tot():
    """
    Total final energy supply delivered by RES for commercial heat.
    """
    return np.minimum(
        np.maximum(fed_heatcom_after_priorities(), 0),
        potential_fes_tot_res_for_heatcom(),
    )


@component.add(
    name='"Historic RES capacity for heat-com"',
    units="TW",
    subscripts=[np.str_("RES heat")],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_res_capacity_for_heatcom",
        "__lookup__": "_ext_lookup_historic_res_capacity_for_heatcom",
    },
)
def historic_res_capacity_for_heatcom(x, final_subs=None):
    """
    Historic installed capacity of RES technologies for commercial heat generation.
    """
    return _ext_lookup_historic_res_capacity_for_heatcom(x, final_subs)


_ext_lookup_historic_res_capacity_for_heatcom = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_res_capacity_for_heat_commercial",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_lookup_historic_res_capacity_for_heatcom",
)


@component.add(
    name='"initial value RES for heat-com"',
    units="TW",
    subscripts=[np.str_("RES heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_value_res_for_heatcom"},
)
def initial_value_res_for_heatcom():
    """
    RES supply by technology for commercial heat in the year 1995.
    """
    return _ext_constant_initial_value_res_for_heatcom()


_ext_constant_initial_value_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_res_capacity_for_heat_commercial*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_initial_value_res_for_heatcom",
)


@component.add(
    name='"installed capacity RES heat-com TW"',
    units="TW",
    subscripts=[np.str_("RES heat")],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_installed_capacity_res_heatcom_tw": 1},
    other_deps={
        "_integ_installed_capacity_res_heatcom_tw": {
            "initial": {"initial_value_res_for_heatcom": 1},
            "step": {
                "new_res_capacity_for_heatcom_tw": 1,
                "replacement_res_for_heatcom_tw": 1,
                "wear_res_capacity_for_heatcom_tw": 1,
            },
        }
    },
)
def installed_capacity_res_heatcom_tw():
    """
    Installed capacity of RES for commercial heat.
    """
    return _integ_installed_capacity_res_heatcom_tw()


_integ_installed_capacity_res_heatcom_tw = Integ(
    lambda: new_res_capacity_for_heatcom_tw()
    + replacement_res_for_heatcom_tw()
    - wear_res_capacity_for_heatcom_tw(),
    lambda: initial_value_res_for_heatcom(),
    "_integ_installed_capacity_res_heatcom_tw",
)


@component.add(
    name="life time RES for heat",
    units="year",
    subscripts=[np.str_("RES heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_life_time_res_for_heat"},
)
def life_time_res_for_heat():
    """
    Lifetime RES thermal technologies and plants.
    """
    return _ext_constant_life_time_res_for_heat()


_ext_constant_life_time_res_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_life_time_res_for_heat",
)


@component.add(
    name="Losses solar for heat",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_losses_solar_for_heat"},
)
def losses_solar_for_heat():
    return _ext_constant_losses_solar_for_heat()


_ext_constant_losses_solar_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "losses_solar_for_heat",
    {},
    _root,
    {},
    "_ext_constant_losses_solar_for_heat",
)


@component.add(
    name='"new RES capacity for heat-com TW"',
    units="TW/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_res_capacity_for_heatcom": 2,
        "nvs_1_year": 1,
        "remaining_potential_constraint_on_new_res_heat_capacity": 1,
        "adapt_growth_res_for_heatcom": 1,
        "installed_capacity_res_heatcom_tw": 1,
        "abundance_res_heatcom2": 1,
    },
)
def new_res_capacity_for_heatcom_tw():
    """
    New annual installed capacity of RES technologies for commercial heat.
    """
    return (
        if_then_else(
            time() < 2013,
            lambda: (
                historic_res_capacity_for_heatcom(time() + 1)
                - historic_res_capacity_for_heatcom(time())
            )
            / nvs_1_year(),
            lambda: adapt_growth_res_for_heatcom()
            * installed_capacity_res_heatcom_tw()
            * remaining_potential_constraint_on_new_res_heat_capacity(),
        )
        * abundance_res_heatcom2()
    )


@component.add(
    name="P geothermal for heat",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_geothermal_for_heat"},
)
def p_geothermal_for_heat():
    """
    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_geothermal_for_heat()


_ext_constant_p_geothermal_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "p_geothermal_heat_growth",
    {},
    _root,
    {},
    "_ext_constant_p_geothermal_for_heat",
)


@component.add(
    name="P RES for heat",
    units="1/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_solar_for_heat": 1,
        "p_geothermal_for_heat": 1,
        "p_solid_bioe_for_heat": 1,
    },
)
def p_res_for_heat():
    """
    Annual growth in RES supply for heat depending on the policy of the scenario.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, [np.str_("RES heat")]
    )
    value.loc[["solar heat"]] = p_solar_for_heat()
    value.loc[["geot heat"]] = p_geothermal_for_heat()
    value.loc[["solid bioE heat"]] = p_solid_bioe_for_heat()
    return value


@component.add(
    name="P solar for heat",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_solar_for_heat"},
)
def p_solar_for_heat():
    """
    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solar_for_heat()


_ext_constant_p_solar_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "p_solar_heat_growth",
    {},
    _root,
    {},
    "_ext_constant_p_solar_for_heat",
)


@component.add(
    name="P solid bioE for heat",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_solid_bioe_for_heat"},
)
def p_solid_bioe_for_heat():
    """
    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solid_bioe_for_heat()


_ext_constant_p_solid_bioe_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "p_solid_bioe_heat_growth",
    {},
    _root,
    {},
    "_ext_constant_p_solid_bioe_for_heat",
)


@component.add(
    name='"past RES growth for heat-com"',
    units="1/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_past_res_growth_for_heatcom"},
)
def past_res_growth_for_heatcom():
    """
    Historic annual average growth.
    """
    return _ext_constant_past_res_growth_for_heatcom()


_ext_constant_past_res_growth_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_res_for_heat_com*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_past_res_growth_for_heatcom",
)


@component.add(
    name='"PES RES for heat-com by techn"',
    units="EJ/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_real_generation_res_heatcom_ej": 3,
        "efficiency_res_heat": 3,
        "efficiency_solar_panels_for_heat": 1,
    },
)
def pes_res_for_heatcom_by_techn():
    """
    Primary energy supply of RES technologies for commercial heat.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, [np.str_("RES heat")]
    )
    value.loc[["geot heat"]] = float(
        fe_real_generation_res_heatcom_ej().loc["geot heat"]
    ) / float(efficiency_res_heat().loc["geot heat"])
    value.loc[["solar heat"]] = (
        float(fe_real_generation_res_heatcom_ej().loc["solar heat"])
        * efficiency_solar_panels_for_heat()
        / float(efficiency_res_heat().loc["solar heat"])
    )
    value.loc[["solid bioE heat"]] = float(
        fe_real_generation_res_heatcom_ej().loc["solid bioE heat"]
    ) / float(efficiency_res_heat().loc["solid bioE heat"])
    return value


@component.add(
    name='"potential FES RES for heat-com"',
    units="EJ/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatcom_twh": 1, "ej_per_twh": 1},
)
def potential_fes_res_for_heatcom():
    """
    Potential final energy supply renewables for commercial heat given the installed capacity.
    """
    return potential_fes_res_for_heatcom_twh() * ej_per_twh()


@component.add(
    name='"potential FES RES for heat-com TWh"',
    units="TWh/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_heatcom_tw": 1,
        "efficiency_res_heat": 1,
        "cp_res_for_heat": 1,
        "twe_per_twh": 1,
    },
)
def potential_fes_res_for_heatcom_twh():
    """
    Potential final energy supply renewables for commercial heat given the installed capacity.
    """
    return (
        installed_capacity_res_heatcom_tw()
        * efficiency_res_heat()
        * cp_res_for_heat()
        / twe_per_twh()
    )


@component.add(
    name='"potential FES tot RES for heat-com"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatcom": 1},
)
def potential_fes_tot_res_for_heatcom():
    """
    Potential total final energy supply renewables for commercial heat given the installed capacity.
    """
    return sum(
        potential_fes_res_for_heatcom().rename({np.str_("RES heat"): "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name="remaining potential constraint on new RES heat capacity",
    units="Dmnl",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "remaining_potential_res_for_heat": 2,
        "threshold_remaining_potential_new_capacity": 2,
    },
)
def remaining_potential_constraint_on_new_res_heat_capacity():
    """
    Constraint of remaining potential on new RES elec capacity. Another alternative: SQRT(remaining potential RES elec after intermitt[RES elec])
    """
    return if_then_else(
        remaining_potential_res_for_heat()
        > threshold_remaining_potential_new_capacity(),
        lambda: xr.DataArray(
            1, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
        ),
        lambda: remaining_potential_res_for_heat()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@component.add(
    name="remaining potential RES for heat",
    units="Dmnl",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_fe_potential_res_for_heat": 2,
        "potential_fes_res_for_heatcom": 1,
        "potential_fes_res_for_heatnc_ej": 1,
    },
)
def remaining_potential_res_for_heat():
    """
    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        np.maximum(
            0,
            max_fe_potential_res_for_heat()
            - potential_fes_res_for_heatcom()
            - potential_fes_res_for_heatnc_ej(),
        ),
        max_fe_potential_res_for_heat(),
    )


@component.add(
    name='"replacement RES for heat-com"',
    units="Dmnl",
    subscripts=[np.str_("RES heat")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_replacement_res_for_heatcom"},
)
def replacement_res_for_heatcom():
    """
    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_res_for_heatcom()


_ext_constant_replacement_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_replacement_res_for_heatcom",
)


@component.add(
    name='"replacement RES for heat-com TW"',
    units="TW/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wear_res_capacity_for_heatcom_tw": 1,
        "replacement_res_for_heatcom": 1,
        "res_heatcom_tot_overcapacity": 1,
    },
)
def replacement_res_for_heatcom_tw():
    """
    Annual replacement of RES for commercial heat by technology.
    """
    return (
        wear_res_capacity_for_heatcom_tw()
        * replacement_res_for_heatcom()
        * (1 - res_heatcom_tot_overcapacity())
    )


@component.add(
    name='"RES heat-com tot overcapacity"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fes_tot_res_for_heatcom": 3,
        "fe_real_supply_res_for_heatcom_tot": 1,
    },
)
def res_heatcom_tot_overcapacity():
    """
    Overcapacity for each technology RES for heat-com taking into account the installed capacity and the real generation.
    """
    return if_then_else(
        potential_fes_tot_res_for_heatcom() == 0,
        lambda: 0,
        lambda: (
            potential_fes_tot_res_for_heatcom() - fe_real_supply_res_for_heatcom_tot()
        )
        / potential_fes_tot_res_for_heatcom(),
    )


@component.add(
    name="Start year P growth RES heat",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_growth_res_heat"},
)
def start_year_p_growth_res_heat():
    """
    Start year of the policy growth of RES technologies for generating heat.
    """
    return _ext_constant_start_year_p_growth_res_heat()


_ext_constant_start_year_p_growth_res_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_P_growth_RES_heat",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_growth_res_heat",
)


@component.add(
    name="threshold remaining potential new capacity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def threshold_remaining_potential_new_capacity():
    return 1


@component.add(
    name='"wear RES capacity for heat-com TW"',
    units="TW/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_res_heatcom_tw": 1, "life_time_res_for_heat": 1},
)
def wear_res_capacity_for_heatcom_tw():
    """
    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatcom_tw() / life_time_res_for_heat()
