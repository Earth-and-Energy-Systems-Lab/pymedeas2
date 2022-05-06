"""
Module inland_transport_sector
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="aaux Tveh",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "t_ini_inlandt": 1, "time_step": 1, "percent_t_vehicles": 1},
)
def aaux_tveh():
    return if_then_else(
        np.abs(time() - t_ini_inlandt()) < 1 * time_step(),
        lambda: percent_t_vehicles(),
        lambda: xr.DataArray(
            0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
        ),
    )


@component.add(
    name="aaux Tveh ini",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aaux_tveh": 1, "aaux_tveh_t": 1},
)
def aaux_tveh_ini():
    return np.maximum(aaux_tveh(), aaux_tveh_t())


@component.add(
    name="aaux Tveh t",
    subscripts=["vehicleT"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_aaux_tveh_t": 1},
    other_deps={
        "_delayfixed_aaux_tveh_t": {
            "initial": {"time_step": 1},
            "step": {"aaux_tveh_ini": 1},
        }
    },
)
def aaux_tveh_t():
    return _delayfixed_aaux_tveh_t()


_delayfixed_aaux_tveh_t = DelayFixed(
    lambda: aaux_tveh_ini(),
    lambda: time_step(),
    lambda: xr.DataArray(0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]),
    time_step,
    "_delayfixed_aaux_tveh_t",
)


@component.add(
    name="Activate policy inlandT",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_policy_inlandt"},
)
def activate_policy_inlandt():
    """
    1 to set growth of alternative inland transportation, starting in T ini and ending in T fin with the desired share defined in policies, linear growth
    """
    return _ext_constant_activate_policy_inlandt()


_ext_constant_activate_policy_inlandt = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "activate_policy_inlandT",
    {},
    _root,
    {},
    "_ext_constant_activate_policy_inlandt",
)


@component.add(
    name="adapt var inlandT",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_inlandt": 2,
        "t_ini_inlandt": 2,
        "hist_var_inlandt": 1,
        "activate_policy_inlandt": 1,
        "percent_t_veh_tini": 1,
        "p_inlandt": 1,
    },
)
def adapt_var_inlandt():
    """
    Growth of percent of vehicles adapted to saturation and shorgate of energy
    """
    return if_then_else(
        time() < t_fin_inlandt(),
        lambda: if_then_else(
            np.logical_and(activate_policy_inlandt() == 1, time() > t_ini_inlandt()),
            lambda: (p_inlandt() - percent_t_veh_tini())
            / (t_fin_inlandt() - t_ini_inlandt()),
            lambda: hist_var_inlandt(),
        ),
        lambda: xr.DataArray(
            0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
        ),
    )


@component.add(
    name="adjust energy for transport to inland transport",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_adjust_energy_for_transport_to_inland_transport"
    },
)
def adjust_energy_for_transport_to_inland_transport():
    """
    'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, considers in 2015 about 34 EJ of liquids for commercial transport. However WIOD database considers to inland transport sector about 12 EJ. Provisionally, we adjust OECD/IEA data to WIOD. We consider OECD/IEA data in relative terms
    """
    return _ext_constant_adjust_energy_for_transport_to_inland_transport()


_ext_constant_adjust_energy_for_transport_to_inland_transport = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "adjust_energy_for_transport_to_inland_transport",
    {},
    _root,
    {},
    "_ext_constant_adjust_energy_for_transport_to_inland_transport",
)


@component.add(
    name="aux hist Tveh",
    units="1/yr",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hist_var_percent_tveh": 17},
)
def aux_hist_tveh():
    """
    auxiliar variable to set the variation of liquid vehicles
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = -float(hist_var_percent_tveh().loc["HV hib"]) - float(
        hist_var_percent_tveh().loc["HV gas"]
    )
    value.loc[["HV hib"]] = float(hist_var_percent_tveh().loc["HV hib"])
    value.loc[["HV gas"]] = float(hist_var_percent_tveh().loc["HV gas"])
    value.loc[["LV liq"]] = (
        -float(hist_var_percent_tveh().loc["LV elec"])
        - float(hist_var_percent_tveh().loc["LV hib"])
        - float(hist_var_percent_tveh().loc["LV gas"])
    )
    value.loc[["LV elec"]] = float(hist_var_percent_tveh().loc["LV elec"])
    value.loc[["LV hib"]] = float(hist_var_percent_tveh().loc["LV hib"])
    value.loc[["LV gas"]] = float(hist_var_percent_tveh().loc["LV gas"])
    value.loc[["bus liq"]] = (
        -float(hist_var_percent_tveh().loc["bus elec"])
        - float(hist_var_percent_tveh().loc["bus hib"])
        - float(hist_var_percent_tveh().loc["bus gas"])
    )
    value.loc[["bus hib"]] = float(hist_var_percent_tveh().loc["bus hib"])
    value.loc[["bus gas"]] = float(hist_var_percent_tveh().loc["bus gas"])
    value.loc[["train liq"]] = float(hist_var_percent_tveh().loc["train liq"])
    value.loc[["train elec"]] = float(hist_var_percent_tveh().loc["train elec"])
    return value


@component.add(
    name="Efects shortage inlandT",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"effects_shortage_gas": 3, "effects_shortage_elec_on_ev": 3},
)
def efects_shortage_inlandt():
    """
    Efects of shortage of alternative fuels
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = 1
    value.loc[["HV hib"]] = 1
    value.loc[["HV gas"]] = effects_shortage_gas()
    value.loc[["LV liq"]] = 1
    value.loc[["LV elec"]] = effects_shortage_elec_on_ev()
    value.loc[["LV gas"]] = effects_shortage_gas()
    value.loc[["bus liq"]] = 1
    value.loc[["bus elec"]] = effects_shortage_elec_on_ev()
    value.loc[["bus hib"]] = 1
    value.loc[["bus gas"]] = effects_shortage_gas()
    value.loc[["train liq"]] = 1
    value.loc[["train elec"]] = effects_shortage_elec_on_ev()
    value.loc[["LV hib"]] = 1
    return value


@component.add(
    name="effects shortage gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 2},
)
def effects_shortage_gas():
    """
    The eventual scarcity of gas would likely constrain the development of NGVs/GTLs. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of NGVs/GTLs.
    """
    return if_then_else(
        abundance_gases() > 0.8, lambda: ((abundance_gases() - 0.8) * 5) ** 2, lambda: 0
    )


@component.add(
    name="Energy initial inland transport",
    units="EJ",
    subscripts=["vehicleT"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_energy_initial_inland_transport"},
)
def energy_initial_inland_transport():
    """
    Initial energy consumed by the inland transport sector, before politics, TpolicyT (default 2015) data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,
    """
    return _ext_constant_energy_initial_inland_transport()


_ext_constant_energy_initial_inland_transport = ExtConstant(
    "../transport.xlsx",
    "Europe",
    "energy_initial_inland_transport*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    {"vehicleT": _subscript_dict["vehicleT"]},
    "_ext_constant_energy_initial_inland_transport",
)


@component.add(
    name="energy per X t",
    units="EJ/T$",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "liquids_per_x_hv": 3,
        "saving_ratios_vehicles": 11,
        "liquids_per_x_lv": 4,
        "liquids_per_x_bus": 4,
        "energy_per_x_train": 2,
    },
)
def energy_per_x_t():
    """
    Energy per T$ of economic activity of inland transport sector. TODO
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV liq"]
    )
    value.loc[["HV hib"]] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV hib"]
    )
    value.loc[["HV gas"]] = liquids_per_x_hv() * float(
        saving_ratios_vehicles().loc["HV gas"]
    )
    value.loc[["LV liq"]] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV liq"]
    )
    value.loc[["LV elec"]] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV elec"]
    )
    value.loc[["LV hib"]] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV hib"]
    )
    value.loc[["LV gas"]] = liquids_per_x_lv() * float(
        saving_ratios_vehicles().loc["LV gas"]
    )
    value.loc[["bus liq"]] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus liq"]
    )
    value.loc[["bus hib"]] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus hib"]
    )
    value.loc[["bus gas"]] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus gas"]
    )
    value.loc[["train liq"]] = energy_per_x_train() * 0.8
    value.loc[["train elec"]] = energy_per_x_train() * 0.2
    value.loc[["bus elec"]] = liquids_per_x_bus() * float(
        saving_ratios_vehicles().loc["bus elec"]
    )
    return value


@component.add(
    name="energy per X train",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_initial_inland_transport": 1,
        "adjust_energy_for_transport_to_inland_transport": 1,
        "initial_xt_inland": 1,
    },
)
def energy_per_x_train():
    """
    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector In the case of trains the number of vehicles is set to 1 since there are no data of the number of trains
    """
    return (
        float(energy_initial_inland_transport().loc["train liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


@component.add(
    name="hist var inlandT",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def hist_var_inlandt():
    """
    Historical growth of alternative percentages of transport vehicles. For inland transport vehicles the initial percentages of vehicles are neglictible in 2015.
    """
    return xr.DataArray(0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"])


@component.add(
    name="hist var percent Tveh",
    units="1/yr",
    subscripts=["vehicleT"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"time": 8, "t_hist_inlandt": 8, "initial_percent_t_vehicles": 8},
)
def hist_var_percent_tveh():
    """
    historical evolution of percent of vehicles based on the linear interpolation between 2005 and T hist H transp(default 2015). Before 2005 all vehicles are liquid based except trains. Percents relative to each type of vehicle
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = 0
    value.loc[["HV hib"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["HV hib"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["HV gas"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["HV gas"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["LV liq"]] = 0
    value.loc[["LV elec"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["LV elec"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["LV hib"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["LV hib"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["LV gas"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["LV gas"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["bus liq"]] = 0
    value.loc[["bus elec"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["bus elec"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["bus hib"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["bus hib"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["bus gas"]] = if_then_else(
        time() > 2005,
        lambda: (float(initial_percent_t_vehicles().loc["bus gas"]) - 0)
        / (t_hist_inlandt() - 2005),
        lambda: 0,
    )
    value.loc[["train liq"]] = 0
    value.loc[["train elec"]] = 0
    return value


@component.add(
    name="initial percent T vehicles",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_percent_t_vehicles"},
)
def initial_percent_t_vehicles():
    """
    Initial percentage of vehicles of each fuel (2015), percents relative to each class of vehicles (LV; HV, bus, train)
    """
    return _ext_constant_initial_percent_t_vehicles()


_ext_constant_initial_percent_t_vehicles = ExtConstant(
    "../transport.xlsx",
    "Europe",
    "initial_percent_T_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    {"vehicleT": _subscript_dict["vehicleT"]},
    "_ext_constant_initial_percent_t_vehicles",
)


@component.add(
    name="initial vehicles inland",
    units="vehicle",
    subscripts=["vehicleT"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_vehicles_inland"},
)
def initial_vehicles_inland():
    """
    Initial number of vehicles in time TpolicyT, 2015 by default, vehicles 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, Paris' No data for train vehicles
    """
    return _ext_constant_initial_vehicles_inland()


_ext_constant_initial_vehicles_inland = ExtConstant(
    "../transport.xlsx",
    "Europe",
    "initial_vehicles_inland*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    {"vehicleT": _subscript_dict["vehicleT"]},
    "_ext_constant_initial_vehicles_inland",
)


@component.add(
    name="initial Xt inland",
    units="T$",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_xt_inland"},
)
def initial_xt_inland():
    """
    Economic activity of inland transport sector in the year of start of policies (2015 default) T$
    """
    return _ext_constant_initial_xt_inland()


_ext_constant_initial_xt_inland = ExtConstant(
    "../transport.xlsx",
    "Europe",
    "initial_Xt_inland",
    {},
    _root,
    {},
    "_ext_constant_initial_xt_inland",
)


@component.add(
    name="inland transport fraction",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_inland_transport_fraction"},
)
def inland_transport_fraction():
    return _ext_constant_inland_transport_fraction()


_ext_constant_inland_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "inland_transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_inland_transport_fraction",
)


@component.add(
    name="inland transport variation intensity",
    units="EJ/TS/yr",
    subscripts=["final sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"var_i_inland_elec": 1, "var_i_inlandt_liq": 1, "var_i_inlandt_gas": 1},
)
def inland_transport_variation_intensity():
    """
    Variation of the energy intensity of inland transport
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["electricity"]] = var_i_inland_elec()
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = var_i_inlandt_liq()
    value.loc[["solids"]] = 0
    value.loc[["gases"]] = var_i_inlandt_gas()
    return value


@component.add(
    name="liquids per X bus",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_initial_inland_transport": 1,
        "adjust_energy_for_transport_to_inland_transport": 1,
        "initial_xt_inland": 1,
    },
)
def liquids_per_x_bus():
    """
    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,data data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA, for energy number of buses from http://www.theicct.org/global-transportation-roadmap-model
    """
    return (
        float(energy_initial_inland_transport().loc["bus liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


@component.add(
    name="liquids per X HV",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_initial_inland_transport": 1,
        "adjust_energy_for_transport_to_inland_transport": 1,
        "initial_xt_inland": 1,
    },
)
def liquids_per_x_hv():
    """
    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,
    """
    return (
        float(energy_initial_inland_transport().loc["HV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


@component.add(
    name="liquids per X LV",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_initial_inland_transport": 1,
        "adjust_energy_for_transport_to_inland_transport": 1,
        "initial_xt_inland": 1,
    },
)
def liquids_per_x_lv():
    """
    EJ/T$economic activity Average consumption of vehicles from historical data= energy used in that kind of transport/ economic activity of the sector data 'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,data
    """
    return (
        float(energy_initial_inland_transport().loc["LV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


@component.add(
    name="NX bus inlandT",
    units="Mvehicles/Mdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_vehicles_inland": 4, "initial_xt_inland": 1},
)
def nx_bus_inlandt():
    """
    number of vehicles per unit of economic activity (e6 dollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["bus liq"])
        + float(initial_vehicles_inland().loc["bus hib"])
        + float(initial_vehicles_inland().loc["bus gas"])
        + float(initial_vehicles_inland().loc["bus elec"])
    ) / initial_xt_inland()


@component.add(
    name="NX HV inland T",
    units="vehicles/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_vehicles_inland": 3, "initial_xt_inland": 1},
)
def nx_hv_inland_t():
    """
    number of vehicles per unit of economic activity (e12 dollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["HV liq"])
        + float(initial_vehicles_inland().loc["HV hib"])
        + float(initial_vehicles_inland().loc["HV gas"])
    ) / initial_xt_inland()


@component.add(
    name="NX LV inland T",
    units="vehicles/Tdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_vehicles_inland": 4, "initial_xt_inland": 1},
)
def nx_lv_inland_t():
    """
    number of vehicles per unit of economic activity (Tdollars) initial values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["LV liq"])
        + float(initial_vehicles_inland().loc["LV elec"])
        + float(initial_vehicles_inland().loc["LV hib"])
        + float(initial_vehicles_inland().loc["LV gas"])
    ) / initial_xt_inland()


@component.add(
    name="NX train inland T",
    units="vehicles/Tdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_xt_inland": 1},
)
def nx_train_inland_t():
    """
    no number of trains found in data, assume the number of trains is 1
    """
    return 1 / initial_xt_inland()


@component.add(
    name="NX0 vehicles per Xinland T",
    units="vehicles/T$",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nx_hv_inland_t": 3,
        "nx_lv_inland_t": 4,
        "nx_bus_inlandt": 4,
        "nx_train_inland_t": 2,
    },
)
def nx0_vehicles_per_xinland_t():
    """
    Estimated number of vehicles per unit of inland transport economic activity
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = nx_hv_inland_t()
    value.loc[["HV hib"]] = nx_hv_inland_t()
    value.loc[["HV gas"]] = nx_hv_inland_t()
    value.loc[["LV liq"]] = nx_lv_inland_t()
    value.loc[["LV elec"]] = nx_lv_inland_t()
    value.loc[["LV hib"]] = nx_lv_inland_t()
    value.loc[["LV gas"]] = nx_lv_inland_t()
    value.loc[["bus liq"]] = nx_bus_inlandt()
    value.loc[["bus hib"]] = nx_bus_inlandt()
    value.loc[["bus gas"]] = nx_bus_inlandt()
    value.loc[["train liq"]] = nx_train_inland_t()
    value.loc[["train elec"]] = nx_train_inland_t()
    value.loc[["bus elec"]] = nx_bus_inlandt()
    return value


@component.add(
    name="P inlandT",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_percent_hv_gas": 2,
        "p_percent_hv_hyb": 2,
        "p_percent_lv_hyb": 2,
        "p_percent_lv_gas": 2,
        "p_percent_lv_elec": 2,
        "p_percent_bus_gas": 2,
        "p_percent_bus_hyb": 2,
        "p_percent_bus_elec": 2,
        "p_percent_train_elec": 2,
    },
)
def p_inlandt():
    """
    Desired percent each type of inland transport vehicle in T fin, Liquids policies are obtained by substracting the rest of vehicles, the sum of all policies must be 1 for each type of vehicle (HV, LV, bus, train).
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = 100 - p_percent_hv_gas() - p_percent_hv_hyb()
    value.loc[["HV hib"]] = p_percent_hv_hyb()
    value.loc[["HV gas"]] = p_percent_hv_gas()
    value.loc[["LV liq"]] = (
        100 - p_percent_lv_elec() - p_percent_lv_hyb() - p_percent_lv_gas()
    )
    value.loc[["LV elec"]] = p_percent_lv_elec()
    value.loc[["LV gas"]] = p_percent_lv_gas()
    value.loc[["bus liq"]] = (
        100 - p_percent_bus_hyb() - p_percent_bus_gas() - p_percent_bus_elec()
    )
    value.loc[["bus elec"]] = p_percent_bus_elec()
    value.loc[["bus hib"]] = p_percent_bus_hyb()
    value.loc[["bus gas"]] = p_percent_bus_gas()
    value.loc[["train liq"]] = 100 - p_percent_train_elec()
    value.loc[["train elec"]] = p_percent_train_elec()
    value.loc[["LV hib"]] = p_percent_lv_hyb()
    return value


@component.add(
    name="P percent bus elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_bus_elec"},
)
def p_percent_bus_elec():
    """
    Policy of change of bus. Desired percent of bus electric in T fin relative to the total bus
    """
    return _ext_constant_p_percent_bus_elec()


_ext_constant_p_percent_bus_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_electr_bus_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_bus_elec",
)


@component.add(
    name="P percent bus gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_bus_gas"},
)
def p_percent_bus_gas():
    """
    Policy of change of bus. Desired percent of bus gas in T fin relative to the total bus
    """
    return _ext_constant_p_percent_bus_gas()


_ext_constant_p_percent_bus_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_natgas_bus_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_bus_gas",
)


@component.add(
    name="P percent bus hyb",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_bus_hyb"},
)
def p_percent_bus_hyb():
    """
    Policy of change of bus. Desired percent of bus hibrid in T fin relative to the total of bus
    """
    return _ext_constant_p_percent_bus_hyb()


_ext_constant_p_percent_bus_hyb = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_hybrid_bus_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_bus_hyb",
)


@component.add(
    name="P percent HV gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_hv_gas"},
)
def p_percent_hv_gas():
    """
    Policy of change of heavy vehicles. Desired percent of HV gas in T fin relative to total Heavy Vehicles
    """
    return _ext_constant_p_percent_hv_gas()


_ext_constant_p_percent_hv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_gas_heavy_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_hv_gas",
)


@component.add(
    name="P percent HV hyb",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_hv_hyb"},
)
def p_percent_hv_hyb():
    """
    Policy of change of heavy vehicles. Desired percent of HV hibrid in T fin relative to total Heavy Vehicles
    """
    return _ext_constant_p_percent_hv_hyb()


_ext_constant_p_percent_hv_hyb = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_hybrid_heavy_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_hv_hyb",
)


@component.add(
    name="P percent LV elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_lv_elec"},
)
def p_percent_lv_elec():
    """
    Policy of change of light cargo vehicles. Percent of LV electric in T fin relative to the total of Light Vehicles
    """
    return _ext_constant_p_percent_lv_elec()


_ext_constant_p_percent_lv_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_electric_light_cargo_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_lv_elec",
)


@component.add(
    name="P percent LV gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_lv_gas"},
)
def p_percent_lv_gas():
    """
    Policy of change of light cargo vehicles. Desired percent of LV gas in T fin relative to the total Light Vehicles
    """
    return _ext_constant_p_percent_lv_gas()


_ext_constant_p_percent_lv_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_natgas_light_cargo_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_lv_gas",
)


@component.add(
    name="P percent LV hyb",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_lv_hyb"},
)
def p_percent_lv_hyb():
    """
    Policy of change of light cargo vehicles. Desired percent of LV hibrid in T fin relative to the total Light Vehicles
    """
    return _ext_constant_p_percent_lv_hyb()


_ext_constant_p_percent_lv_hyb = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_hybrid_light_cargo_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_lv_hyb",
)


@component.add(
    name="P percent train elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_percent_train_elec"},
)
def p_percent_train_elec():
    """
    Policy of change of trains. Desired percent of train electric in T fin relative to the total of trains
    """
    return _ext_constant_p_percent_train_elec()


_ext_constant_p_percent_train_elec = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "percent_electric_train_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_train_elec",
)


@component.add(
    name="percent T veh Tini",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "t_ini_hveh": 1,
        "initial_percent_t_vehicles": 1,
        "aaux_tveh_ini": 1,
    },
)
def percent_t_veh_tini():
    """
    percents in the year of beguining of policies of vehicles relative to each type
    """
    return if_then_else(
        time() < t_ini_hveh(),
        lambda: initial_percent_t_vehicles(),
        lambda: aaux_tveh_ini(),
    )


@component.add(
    name="percent T vehicles",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_percent_t_vehicles": 1},
    other_deps={
        "_integ_percent_t_vehicles": {
            "initial": {"percent_tveh_1995": 1},
            "step": {"var_percent_t_vehicles": 1},
        }
    },
)
def percent_t_vehicles():
    """
    Percents of inland transport vehicles, each type relative to its own: heavy vehicles (%liq+%hib+%gas) add 1, light vehicles (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains ((%liq+%elec) add 1.
    """
    return _integ_percent_t_vehicles()


_integ_percent_t_vehicles = Integ(
    lambda: var_percent_t_vehicles(),
    lambda: percent_tveh_1995(),
    "_integ_percent_t_vehicles",
)


@component.add(
    name="percent Tveh 1995",
    subscripts=["vehicleT"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"initial_percent_t_vehicles": 2},
)
def percent_tveh_1995():
    """
    TODO
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = 100
    value.loc[["HV hib"]] = 0
    value.loc[["HV gas"]] = 0
    value.loc[["LV liq"]] = 100
    value.loc[["LV elec"]] = 0
    value.loc[["LV hib"]] = 0
    value.loc[["LV gas"]] = 0
    value.loc[["bus liq"]] = 100
    value.loc[["bus elec"]] = 0
    value.loc[["bus hib"]] = 0
    value.loc[["bus gas"]] = 0
    value.loc[["train liq"]] = float(initial_percent_t_vehicles().loc["train liq"])
    value.loc[["train elec"]] = float(initial_percent_t_vehicles().loc["train elec"])
    return value


@component.add(
    name="ratio var T vehicles",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"var_percent_t_vehicles": 1},
)
def ratio_var_t_vehicles():
    return var_percent_t_vehicles() / 100


@component.add(
    name="Real total output inland transport",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_total_output_by_sector_eu": 1, "inland_transport_fraction": 1},
)
def real_total_output_inland_transport():
    """
    /1e+006
    """
    return (
        sum(
            real_total_output_by_sector_eu().rename({"sectors": "sectors!"})
            * inland_transport_fraction().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        / 1000000.0
    )


@component.add(
    name="saving ratios vehicles",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratios_vehicles"},
)
def saving_ratios_vehicles():
    """
    ratios of energy consumption of diferente vehicles per Km compared to conventional liquids vechicles
    """
    return _ext_constant_saving_ratios_vehicles()


_ext_constant_saving_ratios_vehicles = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratios_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    {"vehicleT": _subscript_dict["vehicleT"]},
    "_ext_constant_saving_ratios_vehicles",
)


@component.add(
    name="T fin inlandT",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_t_fin_inlandt"},
)
def t_fin_inlandt():
    """
    Time of begining of inland transport policies
    """
    return _ext_constant_t_fin_inlandt()


_ext_constant_t_fin_inlandt = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "tfin_policy_inland_transp_veh",
    {},
    _root,
    {},
    "_ext_constant_t_fin_inlandt",
)


@component.add(
    name="T hist inlandT", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def t_hist_inlandt():
    """
    Year used to calibrate the historical growth of vehicles, 2015
    """
    return 2015


@component.add(
    name="T ini inlandT",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_t_ini_inlandt"},
)
def t_ini_inlandt():
    """
    By this time the policy objectives defined in policies must be obtained
    """
    return _ext_constant_t_ini_inlandt()


_ext_constant_t_ini_inlandt = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "tini_policy_inland_transp_veh",
    {},
    _root,
    {},
    "_ext_constant_t_ini_inlandt",
)


@component.add(
    name="var I inland Elec",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_per_x_t": 3, "ratio_var_t_vehicles": 3},
)
def var_i_inland_elec():
    """
    Variation of the energy intensity of inland transport relative to electricity and due to the variations of electricity based vehicles
    """
    return (
        float(energy_per_x_t().loc["LV elec"])
        * float(ratio_var_t_vehicles().loc["LV elec"])
        + float(energy_per_x_t().loc["train elec"])
        * float(ratio_var_t_vehicles().loc["train elec"])
        + float(energy_per_x_t().loc["bus elec"])
        * float(ratio_var_t_vehicles().loc["bus elec"])
    )


@component.add(
    name="var I inlandT Gas",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_per_x_t": 3, "ratio_var_t_vehicles": 3},
)
def var_i_inlandt_gas():
    """
    Variation of the energy intensity of inland transport relative to gas and due to the variations of gas based vehicles
    """
    return (
        float(energy_per_x_t().loc["HV gas"])
        * float(ratio_var_t_vehicles().loc["HV gas"])
        + float(energy_per_x_t().loc["bus gas"])
        * float(ratio_var_t_vehicles().loc["bus gas"])
        + float(energy_per_x_t().loc["LV gas"])
        * float(ratio_var_t_vehicles().loc["LV gas"])
    )


@component.add(
    name="var I inlandT liq",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_per_x_t": 7, "ratio_var_t_vehicles": 7},
)
def var_i_inlandt_liq():
    """
    Variation of the energy intensity of inland transport relative to liquids and due to the variations of liquids based vehicles
    """
    return (
        float(energy_per_x_t().loc["HV liq"])
        * float(ratio_var_t_vehicles().loc["HV liq"])
        + float(energy_per_x_t().loc["LV liq"])
        * float(ratio_var_t_vehicles().loc["LV liq"])
        + float(energy_per_x_t().loc["bus liq"])
        * float(ratio_var_t_vehicles().loc["bus liq"])
        + float(energy_per_x_t().loc["HV liq"])
        * float(ratio_var_t_vehicles().loc["HV hib"])
        + float(energy_per_x_t().loc["LV liq"])
        * float(ratio_var_t_vehicles().loc["LV hib"])
        + float(energy_per_x_t().loc["bus liq"])
        * float(ratio_var_t_vehicles().loc["bus hib"])
        + float(energy_per_x_t().loc["train liq"])
        * float(ratio_var_t_vehicles().loc["train liq"])
    )


@component.add(
    name="var percent T vehicles",
    units="Dmnl",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 12,
        "t_ini_inlandt": 12,
        "aux_hist_tveh": 12,
        "adapt_var_inlandt": 18,
    },
)
def var_percent_t_vehicles():
    """
    growth of percents of inland transport vehicles, each type relative to its own: heavy vehicles (%liq+%hib+%gas) add 1, light vehicles (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains ((%liq+%elec) add 1. The growth of liquids allways adapts to the one of the rest, we assume that the policies are passing from liquids to other fuels
    """
    value = xr.DataArray(
        np.nan, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"]
    )
    value.loc[["HV liq"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["HV liq"]),
        lambda: -float(adapt_var_inlandt().loc["HV hib"])
        - float(adapt_var_inlandt().loc["HV gas"]),
    )
    value.loc[["HV hib"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["HV hib"]),
        lambda: float(adapt_var_inlandt().loc["HV hib"]),
    )
    value.loc[["HV gas"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["HV gas"]),
        lambda: float(adapt_var_inlandt().loc["HV gas"]),
    )
    value.loc[["LV liq"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["LV liq"]),
        lambda: -float(adapt_var_inlandt().loc["LV hib"])
        - float(adapt_var_inlandt().loc["LV elec"])
        - float(adapt_var_inlandt().loc["LV gas"]),
    )
    value.loc[["LV elec"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["LV elec"]),
        lambda: float(adapt_var_inlandt().loc["LV elec"]),
    )
    value.loc[["LV hib"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["LV hib"]),
        lambda: float(adapt_var_inlandt().loc["LV hib"]),
    )
    value.loc[["LV gas"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["LV gas"]),
        lambda: float(adapt_var_inlandt().loc["LV gas"]),
    )
    value.loc[["bus liq"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["bus liq"]),
        lambda: -float(adapt_var_inlandt().loc["bus elec"])
        - float(adapt_var_inlandt().loc["bus hib"])
        - float(adapt_var_inlandt().loc["bus gas"]),
    )
    value.loc[["bus hib"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["bus hib"]),
        lambda: float(adapt_var_inlandt().loc["bus hib"]),
    )
    value.loc[["bus gas"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["bus gas"]),
        lambda: float(adapt_var_inlandt().loc["bus gas"]),
    )
    value.loc[["train liq"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["train liq"]),
        lambda: -float(adapt_var_inlandt().loc["train elec"]),
    )
    value.loc[["train elec"]] = if_then_else(
        time() < t_ini_inlandt(),
        lambda: float(aux_hist_tveh().loc["train elec"]),
        lambda: float(adapt_var_inlandt().loc["train elec"]),
    )
    value.loc[["bus elec"]] = float(adapt_var_inlandt().loc["bus elec"])
    return value


@component.add(
    name="vehicles inlandT",
    units="vehicles",
    subscripts=["vehicleT"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "percent_t_vehicles": 1,
        "real_total_output_inland_transport": 1,
        "nx0_vehicles_per_xinland_t": 1,
    },
)
def vehicles_inlandt():
    """
    Estimation of the number of vehicles of inland transport sector by types, based on a constant ratio number ob vehicles per economic activity of the inland transport sector
    """
    return (
        (percent_t_vehicles() / 100)
        * real_total_output_inland_transport()
        * nx0_vehicles_per_xinland_t()
    )
