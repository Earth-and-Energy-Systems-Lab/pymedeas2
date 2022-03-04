"""
Module inland_transport_sector
Translated using PySD version 2.2.1
"""


def activate_policy_inlandt():
    """
    Real Name: Activate policy inlandT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    1 to set growth of alternative inland transportation, starting in T ini and ending in T fin with the desired share defined in policies, linear growth
    """
    return _ext_constant_activate_policy_inlandt()


_ext_constant_activate_policy_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "activate_policy_inland_trans",
    {},
    _root,
    "_ext_constant_activate_policy_inlandt",
)


@subs(["vehicleT"], _subscript_dict)
def adapt_var_inlandt():
    """
    Real Name: adapt var inlandT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Growth of percent of vehicles adapted to saturation and shorgate of energy
    """
    return (
        if_then_else(
            time() < t_fin_inlandt(),
            lambda: if_then_else(
                np.logical_and(
                    activate_policy_inlandt() == 1, time() > t_ini_inlandt()
                ),
                lambda: (p_inlandt() - initial_percent_t_vehicles())
                / (t_fin_inlandt() - t_ini_inlandt()),
                lambda: hist_var_inlandt(),
            ),
            lambda: xr.DataArray(
                0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
            ),
        )
        * efects_shortage_inlandt()
    )


def adjust_energy_for_transport_to_inland_transport():
    """
    Real Name: adjust energy for transport to inland transport
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, considers in 2015 about 34 EJ of liquids for commercial transport. However WIOD database considers to inland transport sector about 12 EJ. Provisionally, we adjust OECD/IEA data to WIOD. We consider OECD/IEA data in relative terms.
    """
    return _ext_constant_adjust_energy_for_transport_to_inland_transport()


_ext_constant_adjust_energy_for_transport_to_inland_transport = ExtConstant(
    "../energy.xlsx",
    "World",
    "adjust_energy_for_transport_to_inland_transport",
    {},
    _root,
    "_ext_constant_adjust_energy_for_transport_to_inland_transport",
)


@subs(["vehicleT"], _subscript_dict)
def efects_shortage_inlandt():
    """
    Real Name: Efects shortage inlandT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant, Auxiliary
    Subs: ['vehicleT']

    Efects of shortage of alternative fuels
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = 1
    value.loc[{"vehicleT": ["HV hib"]}] = 1
    value.loc[{"vehicleT": ["HV gas"]}] = effects_shortage_gas()
    value.loc[{"vehicleT": ["LV liq"]}] = 1
    value.loc[{"vehicleT": ["LV elec"]}] = effects_shortage_elec_on_ev()
    value.loc[{"vehicleT": ["LV gas"]}] = effects_shortage_gas()
    value.loc[{"vehicleT": ["bus liq"]}] = 1
    value.loc[{"vehicleT": ["bus elec"]}] = effects_shortage_elec_on_ev()
    value.loc[{"vehicleT": ["bus hib"]}] = 1
    value.loc[{"vehicleT": ["bus gas"]}] = effects_shortage_gas()
    value.loc[{"vehicleT": ["train liq"]}] = 1
    value.loc[{"vehicleT": ["train elec"]}] = effects_shortage_elec_on_ev()
    value.loc[{"vehicleT": ["LV hib"]}] = 1
    return value


def effects_shortage_gas():
    """
    Real Name: effects shortage gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The eventual scarcity of gas would likely constrain the development of NGVs/GTLs. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of NGVs/GTLs.
    """
    return if_then_else(
        abundance_gases() > 0.8, lambda: ((abundance_gases() - 0.8) * 5) ** 2, lambda: 0
    )


@subs(["vehicleT"], _subscript_dict)
def energy_initial_inland_transport():
    """
    Real Name: Energy initial inland transport
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: ['vehicleT']

    Initial energy consumed by the inland transport sector, before politics, TpolicyT (default 2015) data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,
    """
    return _ext_constant_energy_initial_inland_transport()


_ext_constant_energy_initial_inland_transport = ExtConstant(
    "../transport.xlsx",
    "World",
    "energy_initial_inland_transport*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_energy_initial_inland_transport",
)


@subs(["vehicleT"], _subscript_dict)
def energy_per_x_t():
    """
    Real Name: energy per X t
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Energy per T$ of economic activity of inland transport sector. TODO
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV liq"]
    )
    value.loc[{"vehicleT": ["HV hib"]}] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV hib"]
    )
    value.loc[{"vehicleT": ["HV gas"]}] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV gas"]
    )
    value.loc[{"vehicleT": ["LV liq"]}] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV liq"]
    )
    value.loc[{"vehicleT": ["LV elec"]}] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV elec"]
    )
    value.loc[{"vehicleT": ["LV hib"]}] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV hib"]
    )
    value.loc[{"vehicleT": ["LV gas"]}] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV gas"]
    )
    value.loc[{"vehicleT": ["bus liq"]}] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus liq"]
    )
    value.loc[{"vehicleT": ["bus hib"]}] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus hib"]
    )
    value.loc[{"vehicleT": ["bus gas"]}] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus gas"]
    )
    value.loc[{"vehicleT": ["train liq"]}] = energy_per_x_train() * 0.8
    value.loc[{"vehicleT": ["train elec"]}] = energy_per_x_train() * 0.2
    value.loc[{"vehicleT": ["bus elec"]}] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus elec"]
    )
    return value


def energy_per_x_train():
    """
    Real Name: energy per X train
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector In the case of trains the number of vehicles is set to 1 since there are no data of the number of trains
    """
    return (
        float(energy_initial_inland_transport().loc["train liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


@subs(["vehicleT"], _subscript_dict)
def hist_var_inlandt():
    """
    Real Name: hist var inlandT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['vehicleT']

    Historical growth of alternative percentages of transport vehicles. For inland transport vehicles the initial percentages of vehicles are neglictible in 2015.
    """
    return xr.DataArray(0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"])


@subs(["vehicleT"], _subscript_dict)
def initial_percent_t_vehicles():
    """
    Real Name: initial percent T vehicles
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['vehicleT']

    Initial percentage of vehicles of each fuel, percents relative to each class of vehicles (LV; HV, bus, train)
    """
    return _ext_constant_initial_percent_t_vehicles()


_ext_constant_initial_percent_t_vehicles = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_percent_T_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_initial_percent_t_vehicles",
)


@subs(["vehicleT"], _subscript_dict)
def initial_vehicles_inland():
    """
    Real Name: initial vehicles inland
    Original Eqn:
    Units: vehicle
    Limits: (None, None)
    Type: Constant
    Subs: ['vehicleT']

    Initial number of vehicles in time TpolicyT, 2015 by default, vehicles 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, Paris' No data for train vehicles
    """
    return _ext_constant_initial_vehicles_inland()


_ext_constant_initial_vehicles_inland = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_vehicles_inland*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_initial_vehicles_inland",
)


def initial_xt_inland():
    """
    Real Name: initial Xt inland
    Original Eqn:
    Units: T$
    Limits: (None, None)
    Type: Constant
    Subs: []

    Economic activity of inland transport sector in the year of start of policies (2015 default) T$
    """
    return _ext_constant_initial_xt_inland()


_ext_constant_initial_xt_inland = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_Xt_inland",
    {},
    _root,
    "_ext_constant_initial_xt_inland",
)


@subs(["sectors"], _subscript_dict)
def inland_transport_fraction():
    """
    Real Name: inland transport fraction
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['sectors']

    Fraction of the sectors that represent the inland transport output.
    """
    return _ext_constant_inland_transport_fraction()


_ext_constant_inland_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "inland_transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_inland_transport_fraction",
)


@subs(["final sources"], _subscript_dict)
def inland_transport_variation_intensity():
    """
    Real Name: inland transport variation intensity
    Original Eqn:
    Units: EJ/TS/yr
    Limits: (None, None)
    Type: Constant, Auxiliary
    Subs: ['final sources']

    Variation of the energy intensity of inland transport
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = var_i_inland_elec()
    value.loc[{"final sources": ["heat"]}] = 0
    value.loc[{"final sources": ["liquids"]}] = var_i_inlandt_liq()
    value.loc[{"final sources": ["solids"]}] = 0
    value.loc[{"final sources": ["gases"]}] = var_i_inlandt_gas()
    return value


def liquids_per_x_bus():
    """
    Real Name: liquids per X bus
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,data data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, for energy number of buses from http://www.theicct.org/global-transportation-roadmap-model
    """
    return (
        float(energy_initial_inland_transport().loc["bus liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def liquids_per_x_hv():
    """
    Real Name: liquids per X HV
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,
    """
    return (
        float(energy_initial_inland_transport().loc["HV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def liquids_per_x_lv():
    """
    Real Name: liquids per X LV
    Original Eqn:
    Units: EJ/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,data
    """
    return (
        float(energy_initial_inland_transport().loc["LV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def nx_bus_inlandt():
    """
    Real Name: NX bus inlandT
    Original Eqn:
    Units: Mvehicles/Mdollar
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    number of vehicles per unit of economic activity (e6 dollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["bus liq"])
        + float(initial_vehicles_inland().loc["bus hib"])
        + float(initial_vehicles_inland().loc["bus gas"])
        + float(initial_vehicles_inland().loc["bus elec"])
    ) / initial_xt_inland()


def nx_hv_inland_t():
    """
    Real Name: NX HV inland T
    Original Eqn:
    Units: vehicles/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    number of vehicles per unit of economic activity (e12 dollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["HV liq"])
        + float(initial_vehicles_inland().loc["HV hib"])
        + float(initial_vehicles_inland().loc["HV gas"])
    ) / initial_xt_inland()


def nx_lv_inland_t():
    """
    Real Name: NX LV inland T
    Original Eqn:
    Units: vehicles/Tdollar
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    number of vehicles per unit of economic activity (Tdollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["LV liq"])
        + float(initial_vehicles_inland().loc["LV elec"])
        + float(initial_vehicles_inland().loc["LV hib"])
        + float(initial_vehicles_inland().loc["LV gas"])
    ) / initial_xt_inland()


def nx_train_inland_t():
    """
    Real Name: NX train inland T
    Original Eqn:
    Units: vehicles/Tdollar
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    no number of trains found in data, assume the number of trains is 1
    """
    return 1 / initial_xt_inland()


@subs(["vehicleT"], _subscript_dict)
def nx0_vehicles_per_xinland_t():
    """
    Real Name: NX0 vehicles per Xinland T
    Original Eqn:
    Units: vehicles/T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Estimated number of vehicles per unit of inland transport economic activity
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = nx_hv_inland_t()
    value.loc[{"vehicleT": ["HV hib"]}] = nx_hv_inland_t()
    value.loc[{"vehicleT": ["HV gas"]}] = nx_hv_inland_t()
    value.loc[{"vehicleT": ["LV liq"]}] = nx_lv_inland_t()
    value.loc[{"vehicleT": ["LV elec"]}] = nx_lv_inland_t()
    value.loc[{"vehicleT": ["LV hib"]}] = nx_lv_inland_t()
    value.loc[{"vehicleT": ["LV gas"]}] = nx_lv_inland_t()
    value.loc[{"vehicleT": ["bus liq"]}] = nx_bus_inlandt()
    value.loc[{"vehicleT": ["bus hib"]}] = nx_bus_inlandt()
    value.loc[{"vehicleT": ["bus gas"]}] = nx_bus_inlandt()
    value.loc[{"vehicleT": ["train liq"]}] = nx_train_inland_t()
    value.loc[{"vehicleT": ["train elec"]}] = nx_train_inland_t()
    value.loc[{"vehicleT": ["bus elec"]}] = nx_bus_inlandt()
    return value


def p_bus_elec():
    """
    Real Name: P bus elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of bus. Desired percent of bus electric in T fin relative to the total bus
    """
    return _ext_constant_p_bus_elec()


_ext_constant_p_bus_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_elec",
)


def p_bus_gas():
    """
    Real Name: P bus gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of bus. Desired percent of bus gas in T fin relative to the total bus
    """
    return _ext_constant_p_bus_gas()


_ext_constant_p_bus_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_gas",
)


def p_bus_hyb():
    """
    Real Name: P bus hyb
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of bus. Desired percent of bus hibrid in T fin relative to the total of bus
    """
    return _ext_constant_p_bus_hyb()


_ext_constant_p_bus_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hibrid_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_hyb",
)


def p_hv_gas():
    """
    Real Name: P HV gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of heavy vehicles. Desired percent of HV gas in T fin relative to total Heavy Vehicles
    """
    return _ext_constant_p_hv_gas()


_ext_constant_p_hv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_HV_tfin",
    {},
    _root,
    "_ext_constant_p_hv_gas",
)


def p_hv_hyb():
    """
    Real Name: P HV hyb
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of heavy vehicles. Desired percent of HV hibrid in T fin relative to total Heavy Vehicles
    """
    return _ext_constant_p_hv_hyb()


_ext_constant_p_hv_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_HV_tfin",
    {},
    _root,
    "_ext_constant_p_hv_hyb",
)


@subs(["vehicleT"], _subscript_dict)
def p_inlandt():
    """
    Real Name: P inlandT
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Desired percent each type of inland transport vehicle in T fin, Liquids policies are obtained by substracting the rest of vehicles, the sum of all policies must be 1 for each type of vehicle (HV, LV, bus, train).
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = -p_hv_gas() - p_hv_hyb()
    value.loc[{"vehicleT": ["HV hib"]}] = p_hv_hyb()
    value.loc[{"vehicleT": ["HV gas"]}] = p_hv_gas()
    value.loc[{"vehicleT": ["LV liq"]}] = -p_lv_elec() - p_lv_hyb() - p_lv_gas()
    value.loc[{"vehicleT": ["LV elec"]}] = p_lv_elec()
    value.loc[{"vehicleT": ["LV gas"]}] = p_lv_gas()
    value.loc[{"vehicleT": ["bus liq"]}] = -p_bus_hyb() - p_bus_gas() - p_bus_elec()
    value.loc[{"vehicleT": ["bus elec"]}] = p_bus_elec()
    value.loc[{"vehicleT": ["bus hib"]}] = p_bus_hyb()
    value.loc[{"vehicleT": ["bus gas"]}] = p_bus_gas()
    value.loc[{"vehicleT": ["train liq"]}] = -p_train_elec()
    value.loc[{"vehicleT": ["train elec"]}] = p_train_elec()
    value.loc[{"vehicleT": ["LV hib"]}] = p_lv_hyb()
    return value


def p_lv_elec():
    """
    Real Name: P LV elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of light cargo vehicles. Percent of LV electric in T fin relative to the total of Light Vehicles
    """
    return _ext_constant_p_lv_elec()


_ext_constant_p_lv_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_elec",
)


def p_lv_gas():
    """
    Real Name: P LV gas
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of light cargo vehicles. Desired percent of LV gas in T fin relative to the total Light Vehicles
    """
    return _ext_constant_p_lv_gas()


_ext_constant_p_lv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_gas",
)


def p_lv_hyb():
    """
    Real Name: P LV hyb
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of light cargo vehicles. Desired percent of LV hibrid in T fin relative to the total Light Vehicles
    """
    return _ext_constant_p_lv_hyb()


_ext_constant_p_lv_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_hyb",
)


def p_train_elec():
    """
    Real Name: P train elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy of change of trains. Desired percent of train electric in T fin relative to the total of trains
    """
    return _ext_constant_p_train_elec()


_ext_constant_p_train_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_train_tfin",
    {},
    _root,
    "_ext_constant_p_train_elec",
)


@subs(["vehicleT"], _subscript_dict)
def percent_t_vehicles():
    """
    Real Name: percent T vehicles
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: ['vehicleT']

    Percents of inland transport vehicles, each type relative to its own: heavy vehicles (%liq+%hib+%gas) add 1, light vehicles (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains ((%liq+%elec) add 1.
    """
    return _integ_percent_t_vehicles()


_integ_percent_t_vehicles = Integ(
    lambda: var_percent_t_vehicles(),
    lambda: initial_percent_t_vehicles(),
    "_integ_percent_t_vehicles",
)


def real_total_output_inland_transport():
    """
    Real Name: Real total output inland transport
    Original Eqn:
    Units: T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        sum(
            real_total_output_by_sector().rename({"sectors": "sectors!"})
            * inland_transport_fraction().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        / 1000000.0
    )


@subs(["vehicleT"], _subscript_dict)
def saving_ratios_vehicles():
    """
    Real Name: saving ratios vehicles
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['vehicleT']

    ratios of energy consumption of diferente vehicles per Km compared to conventional liquids vechicles
    """
    return _ext_constant_saving_ratios_vehicles()


_ext_constant_saving_ratios_vehicles = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratios_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_saving_ratios_vehicles",
)


@subs(["vehicleT"], _subscript_dict)
def shares_available_t():
    """
    Real Name: shares available T
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Share of the total percent of each type of vehicle available for growth, is the same for each type of vehicle. When it approaches zero the growth of all of them stops
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = 1 - (
        float(percent_t_vehicles().loc["HV hib"])
        + float(percent_t_vehicles().loc["HV gas"])
    )
    value.loc[{"vehicleT": ["HV hib"]}] = 1 - (
        float(percent_t_vehicles().loc["HV hib"])
        + float(percent_t_vehicles().loc["HV gas"])
    )
    value.loc[{"vehicleT": ["HV gas"]}] = 1 - (
        float(percent_t_vehicles().loc["HV hib"])
        + float(percent_t_vehicles().loc["HV gas"])
    )
    value.loc[{"vehicleT": ["LV liq"]}] = 1 - (
        float(percent_t_vehicles().loc["LV elec"])
        + float(percent_t_vehicles().loc["LV hib"])
        + float(percent_t_vehicles().loc["LV gas"])
    )
    value.loc[{"vehicleT": ["LV elec"]}] = 1 - (
        float(percent_t_vehicles().loc["LV elec"])
        + float(percent_t_vehicles().loc["LV hib"])
        + float(percent_t_vehicles().loc["LV gas"])
    )
    value.loc[{"vehicleT": ["LV gas"]}] = 1 - (
        float(percent_t_vehicles().loc["LV elec"])
        + float(percent_t_vehicles().loc["LV hib"])
        + float(percent_t_vehicles().loc["LV gas"])
    )
    value.loc[{"vehicleT": ["LV hib"]}] = 1 - (
        float(percent_t_vehicles().loc["LV elec"])
        + float(percent_t_vehicles().loc["LV hib"])
        + float(percent_t_vehicles().loc["LV gas"])
    )
    value.loc[{"vehicleT": ["bus liq"]}] = 1 - (
        float(percent_t_vehicles().loc["bus elec"])
        + float(percent_t_vehicles().loc["bus hib"])
        + float(percent_t_vehicles().loc["bus gas"])
    )
    value.loc[{"vehicleT": ["bus elec"]}] = 1 - (
        float(percent_t_vehicles().loc["bus elec"])
        + float(percent_t_vehicles().loc["bus hib"])
        + float(percent_t_vehicles().loc["bus gas"])
    )
    value.loc[{"vehicleT": ["bus hib"]}] = 1 - (
        float(percent_t_vehicles().loc["bus elec"])
        + float(percent_t_vehicles().loc["bus hib"])
        + float(percent_t_vehicles().loc["bus gas"])
    )
    value.loc[{"vehicleT": ["bus gas"]}] = 1 - (
        float(percent_t_vehicles().loc["bus elec"])
        + float(percent_t_vehicles().loc["bus hib"])
        + float(percent_t_vehicles().loc["bus gas"])
    )
    value.loc[{"vehicleT": ["train liq"]}] = 1 - float(
        percent_t_vehicles().loc["train elec"]
    )
    value.loc[{"vehicleT": ["train elec"]}] = 1 - float(
        percent_t_vehicles().loc["train elec"]
    )
    return value


def t_fin_inlandt():
    """
    Real Name: T fin inlandT
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Time of begining of inland transport policies
    """
    return _ext_constant_t_fin_inlandt()


_ext_constant_t_fin_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tfin_H_inlandT",
    {},
    _root,
    "_ext_constant_t_fin_inlandt",
)


def t_ini_inlandt():
    """
    Real Name: T ini inlandT
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    By this time the policy objectives defined in policies must be obtained
    """
    return _ext_constant_t_ini_inlandt()


_ext_constant_t_ini_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tini_inlandT_veh",
    {},
    _root,
    "_ext_constant_t_ini_inlandt",
)


def var_i_inland_elec():
    """
    Real Name: var I inland Elec
    Original Eqn:
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variation of the energy intensity of inland transport relative to electricity and due to the variations of electricity based vehicles
    """
    return (
        float(energy_per_x_t().loc["LV elec"])
        * float(var_percent_t_vehicles().loc["LV elec"])
        + float(energy_per_x_t().loc["train elec"])
        * float(var_percent_t_vehicles().loc["train elec"])
        + float(energy_per_x_t().loc["bus elec"])
        * float(var_percent_t_vehicles().loc["bus elec"])
    )


def var_i_inlandt_gas():
    """
    Real Name: var I inlandT Gas
    Original Eqn:
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variation of the energy intensity of inland transport relative to gas and due to the variations of gas based vehicles
    """
    return (
        float(energy_per_x_t().loc["HV gas"])
        * float(var_percent_t_vehicles().loc["HV gas"])
        + float(energy_per_x_t().loc["bus gas"])
        * float(var_percent_t_vehicles().loc["bus gas"])
        + float(energy_per_x_t().loc["LV gas"])
        * float(var_percent_t_vehicles().loc["LV gas"])
    )


def var_i_inlandt_liq():
    """
    Real Name: var I inlandT liq
    Original Eqn:
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variation of the energy intensity of inland transport relative to liquids and due to the variations of liquids based vehicles
    """
    return (
        float(energy_per_x_t().loc["HV liq"])
        * float(var_percent_t_vehicles().loc["HV liq"])
        + float(energy_per_x_t().loc["LV liq"])
        * float(var_percent_t_vehicles().loc["LV liq"])
        + float(energy_per_x_t().loc["bus liq"])
        * float(var_percent_t_vehicles().loc["bus liq"])
        + float(energy_per_x_t().loc["HV liq"])
        * float(var_percent_t_vehicles().loc["HV hib"])
        + float(energy_per_x_t().loc["LV liq"])
        * float(var_percent_t_vehicles().loc["LV hib"])
        + float(energy_per_x_t().loc["bus liq"])
        * float(var_percent_t_vehicles().loc["bus hib"])
        + float(energy_per_x_t().loc["train liq"])
        * float(var_percent_t_vehicles().loc["train liq"])
    )


@subs(["vehicleT"], _subscript_dict)
def var_percent_t_vehicles():
    """
    Real Name: var percent T vehicles
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    growth of percents of inland transport vehicles, each type relative to its own: heavy vehicles (%liq+%hib+%gas) add 1, light vehicles (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains ((%liq+%elec) add 1. The growth of liquids allways adapts to the one of the rest, we assume that the policies are passing from liquids to other fuels
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[{"vehicleT": ["HV liq"]}] = -float(
        adapt_var_inlandt().loc["HV hib"]
    ) - float(adapt_var_inlandt().loc["HV gas"])
    value.loc[{"vehicleT": ["HV hib"]}] = float(adapt_var_inlandt().loc["HV hib"])
    value.loc[{"vehicleT": ["HV gas"]}] = float(adapt_var_inlandt().loc["HV gas"])
    value.loc[{"vehicleT": ["LV liq"]}] = (
        -float(adapt_var_inlandt().loc["LV hib"])
        - float(adapt_var_inlandt().loc["LV elec"])
        - float(adapt_var_inlandt().loc["LV gas"])
    )
    value.loc[{"vehicleT": ["LV elec"]}] = float(adapt_var_inlandt().loc["LV elec"])
    value.loc[{"vehicleT": ["LV hib"]}] = float(adapt_var_inlandt().loc["LV hib"])
    value.loc[{"vehicleT": ["LV gas"]}] = float(adapt_var_inlandt().loc["LV gas"])
    value.loc[{"vehicleT": ["bus liq"]}] = (
        -float(adapt_var_inlandt().loc["bus elec"])
        - float(adapt_var_inlandt().loc["bus hib"])
        - float(adapt_var_inlandt().loc["bus gas"])
    )
    value.loc[{"vehicleT": ["bus hib"]}] = float(adapt_var_inlandt().loc["bus hib"])
    value.loc[{"vehicleT": ["bus gas"]}] = float(adapt_var_inlandt().loc["bus gas"])
    value.loc[{"vehicleT": ["train liq"]}] = -float(
        adapt_var_inlandt().loc["train elec"]
    )
    value.loc[{"vehicleT": ["train elec"]}] = float(
        adapt_var_inlandt().loc["train elec"]
    )
    value.loc[{"vehicleT": ["bus elec"]}] = float(adapt_var_inlandt().loc["bus elec"])
    return value


@subs(["vehicleT"], _subscript_dict)
def vehicles_inlandt():
    """
    Real Name: vehicles inlandT
    Original Eqn:
    Units: vehicles
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['vehicleT']

    Estimation of the number of vehicles of inland transport sector by types, based on a constant ratio number ob vehicles per economic activity of the inland transport sector
    """
    return (
        percent_t_vehicles()
        * real_total_output_inland_transport()
        * nx0_vehicles_per_xinland_t()
    )
