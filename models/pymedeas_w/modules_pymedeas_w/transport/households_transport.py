"""
Module households_transport
Translated using PySD version 3.2.0
"""


@component.add(
    name="A1 coef tH",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "liq_4w": 1,
        "demand_h": 1,
        "a2_coef_th": 1,
        "percent_2w_liq": 1,
        "percent_4w_liq": 1,
    },
)
def a1_coef_th():
    """
    Coeficients for the calculation of variations of trasnport intensities A1= ( LH t(0) / DH(0) - A2%Hliq2w )/ %Hliq
    """
    return (liq_4w() / demand_h() - a2_coef_th() * percent_2w_liq()) / percent_4w_liq()


@component.add(
    name="A2 coef tH",
    units="EJ/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electricity_2we": 1,
        "saving_ratio_2we": 1,
        "demand_h": 1,
        "percent_h_vehicles_initial": 1,
    },
)
def a2_coef_th():
    """
    Coeficients for the calculation of variations of trasnport intensities A2 = EH 2w(0) / ( DH(0) %HE2w ·srE2w )=
    """
    return electricity_2we() / (
        demand_h()
        * float(percent_h_vehicles_initial().loc["elec 2wheels"])
        * saving_ratio_2we()
    )


@component.add(
    name="Activate policy H transp",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_policy_h_transp"},
)
def activate_policy_h_transp():
    """
    1 to set growth of alternative households transportation based on desired share in 2050, 0 for BAU linear growth
    """
    return _ext_constant_activate_policy_h_transp()


_ext_constant_activate_policy_h_transp = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "activate_policy_Households_trans",
    {},
    _root,
    {},
    "_ext_constant_activate_policy_h_transp",
)


@component.add(
    name="aux hist H",
    units="1/yr",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hist_var_percent_h": 8},
)
def aux_hist_h():
    """
    auxiliar variable to set the variation of liquid vehicles
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = (
        -float(hist_var_percent_h().loc["hib 4wheels"])
        - float(hist_var_percent_h().loc["elec 4wheels"])
        - float(hist_var_percent_h().loc["gas 4wheels"])
    )
    value.loc[["hib 4wheels"]] = float(hist_var_percent_h().loc["hib 4wheels"])
    value.loc[["elec 4wheels"]] = float(hist_var_percent_h().loc["elec 4wheels"])
    value.loc[["liq 2wheels"]] = -float(hist_var_percent_h().loc["elec 2wheels"])
    value.loc[["elec 2wheels"]] = float(hist_var_percent_h().loc["elec 2wheels"])
    value.loc[["gas 4wheels"]] = float(hist_var_percent_h().loc["gas 4wheels"])
    return value


@component.add(
    name="Demand H",
    units="T$",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_demand_h"},
)
def demand_h():
    """
    Initial households economic demand in T dollars, in the year of start of alternative households vehicle policy (default 2015) 30.3 T$
    """
    return _ext_constant_demand_h()


_ext_constant_demand_h = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_households_demand",
    {},
    _root,
    {},
    "_ext_constant_demand_h",
)


@component.add(
    name="effects shortage elec on EV",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_electricity": 2},
)
def effects_shortage_elec_on_ev():
    """
    The eventual scarcity of electricity would likely constrain the development of EVs. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the electricity abundance that constrains the development of EVs.
    """
    return if_then_else(
        abundance_electricity() > 0.8,
        lambda: ((abundance_electricity() - 0.8) * 5) ** 2,
        lambda: 0,
    )


@component.add(
    name="effects shortage gas H veh",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 2},
)
def effects_shortage_gas_h_veh():
    """
    The eventual scarcity of gas would likely constrain the development of NGVs/GTLs. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of NGVs/GTLs.
    """
    return if_then_else(
        abundance_gases() > 0.8, lambda: ((abundance_gases() - 0.8) * 5) ** 2, lambda: 0
    )


@component.add(
    name="Electricity 2wE",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_electricity_2we"},
)
def electricity_2we():
    """
    Initial electricity used by 2 wheelers in the year of start of policies (2015 default) 0.3415
    """
    return _ext_constant_electricity_2we()


_ext_constant_electricity_2we = ExtConstant(
    "../transport.xlsx",
    "World",
    "elec_2w",
    {},
    _root,
    {},
    "_ext_constant_electricity_2we",
)


@component.add(
    name="Energy intensity of households transport",
    units="EJ/T$",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_energy_intensity_of_households_transport": 1},
    other_deps={
        "_integ_energy_intensity_of_households_transport": {
            "initial": {"initial_energy_intensity_of_households_transport_2009": 1},
            "step": {"variation_energy_intensity_of_households_transport": 1},
        }
    },
)
def energy_intensity_of_households_transport():
    return _integ_energy_intensity_of_households_transport()


_integ_energy_intensity_of_households_transport = Integ(
    lambda: variation_energy_intensity_of_households_transport(),
    lambda: initial_energy_intensity_of_households_transport_2009(),
    "_integ_energy_intensity_of_households_transport",
)


@component.add(
    name="H 2w initial growth",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_h_veh": 2,
        "t_ini_h_veh": 2,
        "activate_policy_h_transp": 1,
        "aux_hist_h": 1,
        "percent_h_vehicles_initial": 1,
        "p_h_vehicle": 1,
    },
)
def h_2w_initial_growth():
    """
    Growth of percent of electric 2w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["elec 2wheels"])
                - float(percent_h_vehicles_initial().loc["elec 2wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["elec 2wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H 2wE adapt growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h_2w_initial_growth": 1},
)
def h_2we_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w. growth of the percentage of electric 2 wheelers vehicles is linear at first but slows down when the maximum is reached. No efects on the electricity shortage are noticed for these vehicles since their consumption is so low compared to others.
    """
    return h_2w_initial_growth()


@component.add(
    name="H elec initial growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_h_veh": 2,
        "t_ini_h_veh": 2,
        "activate_policy_h_transp": 1,
        "aux_hist_h": 1,
        "percent_h_vehicles_initial": 1,
        "p_h_vehicle": 1,
    },
)
def h_elec_initial_growth():
    """
    Growth of percent of electrical 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["elec 4wheels"])
                - float(percent_h_vehicles_initial().loc["elec 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["elec 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H EV adapt growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h_elec_initial_growth": 1, "effects_shortage_elec_on_ev": 1},
)
def h_ev_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w.growth of the percentage of EV vehicles is linear at first but adapted to the shortage of electricity and slows down when the maximum is reached
    """
    return h_elec_initial_growth() * effects_shortage_elec_on_ev()


@component.add(
    name="H gas adapt growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h_gas_initial_growth": 1, "effects_shortage_gas_h_veh": 1},
)
def h_gas_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w. growth of the percentage of gas vehicles is linear at first but adapted to the shortage of gas and slows down when the maximum is reached.
    """
    return h_gas_initial_growth() * effects_shortage_gas_h_veh()


@component.add(
    name="H gas initial growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_h_veh": 2,
        "t_ini_h_veh": 2,
        "activate_policy_h_transp": 1,
        "aux_hist_h": 1,
        "percent_h_vehicles_initial": 1,
        "p_h_vehicle": 1,
    },
)
def h_gas_initial_growth():
    """
    Growth of percent of gas 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["gas 4wheels"])
                - float(percent_h_vehicles_initial().loc["gas 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["gas 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H hyb adapt growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"h_hyb_initial_growth": 1},
)
def h_hyb_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w.growth of the percentage of hibrid vehicles is linear at first but slows down when the maximum is reached
    """
    return h_hyb_initial_growth()


@component.add(
    name="H hyb initial growth",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_h_veh": 2,
        "t_ini_h_veh": 2,
        "activate_policy_h_transp": 1,
        "aux_hist_h": 1,
        "percent_h_vehicles_initial": 1,
        "p_h_vehicle": 1,
    },
)
def h_hyb_initial_growth():
    """
    Growth of percent of hibrid 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["hib 4wheels"])
                - float(percent_h_vehicles_initial().loc["hib 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["hib 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="hist var percent H",
    units="1/yr",
    subscripts=["Households vehicles"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4, "percent_h_vehicles_initial": 4, "t_hist_h_transp": 4},
)
def hist_var_percent_h():
    """
    historical evolution of percent of vehicles based on the linear interpolation between 2005 and T hist H transp(default 2015). Before 2005 all vehicle s are liquid based. Percents relative to 2w+4w
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = 0
    value.loc[["hib 4wheels"]] = if_then_else(
        time() > 2005,
        lambda: (float(percent_h_vehicles_initial().loc["hib 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
        lambda: 0,
    )
    value.loc[["elec 4wheels"]] = if_then_else(
        time() < 2005,
        lambda: 0,
        lambda: (float(percent_h_vehicles_initial().loc["elec 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
    )
    value.loc[["gas 4wheels"]] = if_then_else(
        time() < 2005,
        lambda: 0,
        lambda: (float(percent_h_vehicles_initial().loc["gas 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
    )
    value.loc[["liq 2wheels"]] = 0
    value.loc[["elec 2wheels"]] = if_then_else(
        time() < 2005,
        lambda: 0,
        lambda: (float(percent_h_vehicles_initial().loc["elec 2wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
    )
    return value


@component.add(
    name="increase Households energy final demand for Transp",
    units="EJ/T$",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_intensity_of_households_transport": 1,
        "initial_energy_intensity_of_households_transport_2009": 1,
        "household_demand_total": 1,
    },
)
def increase_households_energy_final_demand_for_transp():
    return (
        (
            energy_intensity_of_households_transport()
            - initial_energy_intensity_of_households_transport_2009()
        )
        * household_demand_total()
        / 1000000.0
    )


@component.add(
    name="initial 2w percent",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percent_h_vehicles_initial": 2},
)
def initial_2w_percent():
    """
    2015 percent of 2 wheelers 0,332
    """
    return float(percent_h_vehicles_initial().loc["liq 2wheels"]) + float(
        percent_h_vehicles_initial().loc["elec 2wheels"]
    )


@component.add(
    name="Initial energy intensity of households transport 2009",
    units="EJ/T$",
    subscripts=["final sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_initial_energy_intensity_of_households_transport_2009"
    },
)
def initial_energy_intensity_of_households_transport_2009():
    """
    Initial values of household trasnport intensity. Starting year = 2009, before that year alternative vehicles are neglictible
    """
    return _ext_constant_initial_energy_intensity_of_households_transport_2009()


_ext_constant_initial_energy_intensity_of_households_transport_2009 = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_energy_intensity_households_transport*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_constant_initial_energy_intensity_of_households_transport_2009",
)


@component.add(
    name="Liq 4w",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_liq_4w"},
)
def liq_4w():
    """
    liquids userd in households 4 wheelers in the initial year of policy (2015 default) 45.9341
    """
    return _ext_constant_liq_4w()


_ext_constant_liq_4w = ExtConstant(
    "../transport.xlsx", "World", "liq_4w", {}, _root, {}, "_ext_constant_liq_4w"
)


@component.add(
    name="max percent 2 wheels",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_max_percent_2_wheels": 1},
    other_deps={
        "_integ_max_percent_2_wheels": {
            "initial": {"initial_2w_percent": 1},
            "step": {"rate_4w_to_2w": 1},
        }
    },
)
def max_percent_2_wheels():
    """
    maximum share of 2wheel vehicles (in terms of number of vehicles) policies or shortage can make people move form 4wheel vehicles to two wheelers
    """
    return _integ_max_percent_2_wheels()


_integ_max_percent_2_wheels = Integ(
    lambda: rate_4w_to_2w(), lambda: initial_2w_percent(), "_integ_max_percent_2_wheels"
)


@component.add(
    name="max percent 4 wheels",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_max_percent_4_wheels": 1},
    other_deps={
        "_integ_max_percent_4_wheels": {
            "initial": {"initial_2w_percent": 1},
            "step": {"rate_4w_to_2w": 1},
        }
    },
)
def max_percent_4_wheels():
    """
    max percent of 4 wheelers relative to total amount 2w+4w
    """
    return _integ_max_percent_4_wheels()


_integ_max_percent_4_wheels = Integ(
    lambda: -rate_4w_to_2w(),
    lambda: 1 - initial_2w_percent(),
    "_integ_max_percent_4_wheels",
)


@component.add(
    name="N vehicles H",
    units="vehicles",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_n_vehicles_h"},
)
def n_vehicles_h():
    """
    Initial number of household vehicles in time 2015 vehicles 2w+4w 2476
    """
    return _ext_constant_n_vehicles_h()


_ext_constant_n_vehicles_h = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_household_vehicles",
    {},
    _root,
    {},
    "_ext_constant_n_vehicles_h",
)


@component.add(
    name="Number 2w",
    units="vehicles",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_vehicles_h": 2},
)
def number_2w():
    """
    total number of 2w vehicles househols
    """
    return float(number_vehicles_h().loc["liq 2wheels"]) + float(
        number_vehicles_h().loc["elec 2wheels"]
    )


@component.add(
    name="Number 4w",
    units="vehicles",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_vehicles_h": 4},
)
def number_4w():
    """
    agregated number of 4w vehicles
    """
    return (
        float(number_vehicles_h().loc["liq 4wheels"])
        + float(number_vehicles_h().loc["hib 4wheels"])
        + float(number_vehicles_h().loc["elec 4wheels"])
        + float(number_vehicles_h().loc["gas 4wheels"])
    )


@component.add(
    name="Number vehicles H",
    units="vehicles",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ratio_n_veh_demand_h": 1,
        "household_demand_total": 1,
        "percents_h_vehicles": 1,
    },
)
def number_vehicles_h():
    """
    Estimated number of households vehicles asuming constant ratios of vehicles per households demand
    """
    return (
        ratio_n_veh_demand_h()
        * household_demand_total()
        * 1e-06
        * percents_h_vehicles()
    )


@component.add(
    name="P 2wE",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_2we"},
)
def p_2we():
    """
    Desired percent of electrical 2 wheelers in T fin our of TOTAL 2 WHEEL vehicles
    """
    return _ext_constant_p_2we()


_ext_constant_p_2we = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_2w_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_2we",
)


@component.add(
    name="P elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_elec"},
)
def p_elec():
    """
    Desired percent of electrical vehicles (4 wheelers) in T fin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_elec()


_ext_constant_p_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_household_4w_veh_transp",
    {},
    _root,
    {},
    "_ext_constant_p_elec",
)


@component.add(
    name="P gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_gas"},
)
def p_gas():
    """
    Desired percent of gas vehicles (4 wheelers) in Tfin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_gas()


_ext_constant_p_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_hh_veh_4w_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_gas",
)


@component.add(
    name="P H vehicle",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_share_2_wheelers": 6,
        "p_gas": 2,
        "p_hyb": 2,
        "p_elec": 2,
        "p_2we": 2,
    },
)
def p_h_vehicle():
    """
    desired percent of vehicles from each type in T fin. These are percentages relatives TO THE TOTAL AMOUNT OF VEHICLES ( 2 wheelers + 4 wheelers).
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = (1 - p_share_2_wheelers()) * (
        -p_elec() - p_gas() - p_hyb()
    )
    value.loc[["elec 4wheels"]] = p_elec() * (1 - p_share_2_wheelers())
    value.loc[["hib 4wheels"]] = p_hyb() * (1 - p_share_2_wheelers())
    value.loc[["gas 4wheels"]] = p_gas() * (1 - p_share_2_wheelers())
    value.loc[["liq 2wheels"]] = p_share_2_wheelers() * (1 - p_2we())
    value.loc[["elec 2wheels"]] = p_share_2_wheelers() * p_2we()
    return value


@component.add(
    name="P hyb",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_hyb"},
)
def p_hyb():
    """
    Desired percent of hibrid vehicles (4 wheelers) in T fin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_hyb()


_ext_constant_p_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_household_4w_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_hyb",
)


@component.add(
    name="P share 2 wheelers",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_share_2_wheelers"},
)
def p_share_2_wheelers():
    """
    desired percent of all 2 WHEELS vehicles in T fin relative to total 2w+4w, initial value in 2015 is 0.34
    """
    return _ext_constant_p_share_2_wheelers()


_ext_constant_p_share_2_wheelers = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_change_2w_h_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_share_2_wheelers",
)


@component.add(
    name="percent 2w",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percents_h_vehicles": 2},
)
def percent_2w():
    """
    percentages of 2 wheels and 3 wheels vehicles
    """
    return float(percents_h_vehicles().loc["liq 2wheels"]) + float(
        percents_h_vehicles().loc["elec 2wheels"]
    )


@component.add(
    name="percent 2w liq",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percent_h_vehicles_initial": 1},
)
def percent_2w_liq():
    """
    Percent of 2wheelers of liquids in the initial year of policy (2015 default). percents relative to total number 4w+2w DEFAULT: 0.2712
    """
    return float(percent_h_vehicles_initial().loc["liq 2wheels"])


@component.add(
    name="percent 4w",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percents_h_vehicles": 4},
)
def percent_4w():
    """
    percentages of 4 wheels vehicles
    """
    return (
        float(percents_h_vehicles().loc["liq 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
    )


@component.add(
    name="percent 4w liq",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percent_h_vehicles_initial": 1},
)
def percent_4w_liq():
    """
    Percent of 4wheelers of liquids in the initial year of policy (2015 default). percents relative to total number 4w+2w 0.658
    """
    return float(percent_h_vehicles_initial().loc["liq 4wheels"])


@component.add(
    name="percent H vehicles initial",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_percent_h_vehicles_initial"},
)
def percent_h_vehicles_initial():
    """
    percents in the year of calibration (2015 ) of vehciles relative to total 4w+2w:
    """
    return _ext_constant_percent_h_vehicles_initial()


_ext_constant_percent_h_vehicles_initial = ExtConstant(
    "../transport.xlsx",
    "World",
    "percent_H_vehicles_initial*",
    {"Households vehicles": _subscript_dict["Households vehicles"]},
    _root,
    {"Households vehicles": _subscript_dict["Households vehicles"]},
    "_ext_constant_percent_h_vehicles_initial",
)


@component.add(
    name="percents 2w H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"percents_h_vehicles": 6},
)
def percents_2w_h_vehicles():
    """
    Percent of electrical 2 wheeler as a percent of ONLY TWO WHEELERS
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 2wheels"]] = float(percents_h_vehicles().loc["liq 2wheels"]) / (
        float(percents_h_vehicles().loc["elec 2wheels"])
        + float(percents_h_vehicles().loc["liq 2wheels"])
    )
    value.loc[["elec 2wheels"]] = float(percents_h_vehicles().loc["elec 2wheels"]) / (
        float(percents_h_vehicles().loc["elec 2wheels"])
        + float(percents_h_vehicles().loc["liq 2wheels"])
    )
    value.loc[["liq 4wheels"]] = 0
    value.loc[["elec 4wheels"]] = 0
    value.loc[["gas 4wheels"]] = 0
    value.loc[["hib 4wheels"]] = 0
    return value


@component.add(
    name="percents 4w H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"percents_h_vehicles": 20},
)
def percents_4w_h_vehicles():
    """
    Percent of alternative 4 wheelers as a percent of ONLY 4 WHEELERS
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = float(percents_h_vehicles().loc["liq 4wheels"]) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[["elec 4wheels"]] = float(percents_h_vehicles().loc["elec 4wheels"]) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[["hib 4wheels"]] = float(percents_h_vehicles().loc["hib 4wheels"]) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[["gas 4wheels"]] = float(percents_h_vehicles().loc["gas 4wheels"]) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[["liq 2wheels"]] = 0
    value.loc[["elec 2wheels"]] = 0
    return value


@component.add(
    name="percents H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_percents_h_vehicles": 1,
        "_integ_percents_h_vehicles_1": 1,
        "_integ_percents_h_vehicles_2": 1,
        "_integ_percents_h_vehicles_3": 1,
        "_integ_percents_h_vehicles_4": 1,
        "_integ_percents_h_vehicles_5": 1,
    },
    other_deps={
        "_integ_percents_h_vehicles": {
            "initial": {"initial_2w_percent": 1},
            "step": {"var_percents_h_vehicles": 1},
        },
        "_integ_percents_h_vehicles_1": {
            "initial": {},
            "step": {"var_percents_h_vehicles": 1},
        },
        "_integ_percents_h_vehicles_2": {
            "initial": {},
            "step": {"var_percents_h_vehicles": 1},
        },
        "_integ_percents_h_vehicles_3": {
            "initial": {},
            "step": {"var_percents_h_vehicles": 1},
        },
        "_integ_percents_h_vehicles_4": {
            "initial": {"initial_2w_percent": 1},
            "step": {"var_percents_h_vehicles": 1},
        },
        "_integ_percents_h_vehicles_5": {
            "initial": {},
            "step": {"var_percents_h_vehicles": 1},
        },
    },
)
def percents_h_vehicles():
    """
    Percent relative to total number of vehicles 2w+4w. Initial percentages in 1995 of alternative vehicles are considered cero, This is done that way in order to allow a lineal growth that matches historical vehaviour from 2005 to 2015. Percents relative to total 4w+2w.
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = _integ_percents_h_vehicles().values
    value.loc[["elec 4wheels"]] = _integ_percents_h_vehicles_1().values
    value.loc[["hib 4wheels"]] = _integ_percents_h_vehicles_2().values
    value.loc[["gas 4wheels"]] = _integ_percents_h_vehicles_3().values
    value.loc[["liq 2wheels"]] = _integ_percents_h_vehicles_4().values
    value.loc[["elec 2wheels"]] = _integ_percents_h_vehicles_5().values
    return value


_integ_percents_h_vehicles = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["liq 4wheels"]),
        {"Households vehicles": ["liq 4wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        1 - initial_2w_percent(),
        {"Households vehicles": ["liq 4wheels"]},
        ["Households vehicles"],
    ),
    "_integ_percents_h_vehicles",
)

_integ_percents_h_vehicles_1 = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["elec 4wheels"]),
        {"Households vehicles": ["elec 4wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        0, {"Households vehicles": ["elec 4wheels"]}, ["Households vehicles"]
    ),
    "_integ_percents_h_vehicles_1",
)

_integ_percents_h_vehicles_2 = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["hib 4wheels"]),
        {"Households vehicles": ["hib 4wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        0, {"Households vehicles": ["hib 4wheels"]}, ["Households vehicles"]
    ),
    "_integ_percents_h_vehicles_2",
)

_integ_percents_h_vehicles_3 = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["gas 4wheels"]),
        {"Households vehicles": ["gas 4wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        0, {"Households vehicles": ["gas 4wheels"]}, ["Households vehicles"]
    ),
    "_integ_percents_h_vehicles_3",
)

_integ_percents_h_vehicles_4 = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["liq 2wheels"]),
        {"Households vehicles": ["liq 2wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        initial_2w_percent(),
        {"Households vehicles": ["liq 2wheels"]},
        ["Households vehicles"],
    ),
    "_integ_percents_h_vehicles_4",
)

_integ_percents_h_vehicles_5 = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["elec 2wheels"]),
        {"Households vehicles": ["elec 2wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        0, {"Households vehicles": ["elec 2wheels"]}, ["Households vehicles"]
    ),
    "_integ_percents_h_vehicles_5",
)


@component.add(
    name="policy 2wheels",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "t_fin_h_veh": 2,
        "t_ini_h_veh": 2,
        "p_share_2_wheelers": 1,
        "activate_policy_h_transp": 1,
        "initial_2w_percent": 1,
    },
)
def policy_2wheels():
    """
    Growth of percent of all types of 2wheelers relative to the total amount of vehicles. relative to all vehicles 2w+4w
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (p_share_2_wheelers() - initial_2w_percent())
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: 0,
        ),
        lambda: 0,
    )


@component.add(
    name="rate 4w to 2w",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"policy_2wheels": 1},
)
def rate_4w_to_2w():
    """
    change from 4 wheelers based mobility to 2 wheelers, linear change until the limit aproaches
    """
    return policy_2wheels()


@component.add(
    name="ratio N veh Demand H",
    units="vehicles/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n_vehicles_h": 1, "demand_h": 1},
)
def ratio_n_veh_demand_h():
    """
    Ration of number of vehicles by unit of household conomic demand, we assume that it is kept constant and variations are due to the change in the number of vehicles from one type to another
    """
    return n_vehicles_h() / demand_h()


@component.add(
    name="saving ratio 2wE",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_saving_ratio_2we"},
)
def saving_ratio_2we():
    """
    saving ratio of electrical 2wheelers compared to gasoline 2 wheelers
    """
    return _ext_constant_saving_ratio_2we()


_ext_constant_saving_ratio_2we = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratio_2wE",
    {},
    _root,
    {},
    "_ext_constant_saving_ratio_2we",
)


@component.add(
    name="share available 2w",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_percent_2_wheels": 2, "percents_h_vehicles": 1},
)
def share_available_2w():
    """
    Difference between the share of 2w and the maximum. It's used to saturate the growth when limits are close. share of 2w relative to total amount 2w+4w
    """
    return (
        max_percent_2_wheels() - float(percents_h_vehicles().loc["elec 2wheels"])
    ) / max_percent_2_wheels()


@component.add(
    name="share available 4w",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_percent_4_wheels": 2, "sum_4w_shares": 1},
)
def share_available_4w():
    """
    share of 4wheelers available for alternatives. Percent relative to total number of vehicles 2w+4w.It's used to saturate the growth when limits are close
    """
    return (max_percent_4_wheels() - sum_4w_shares()) / max_percent_4_wheels()


@component.add(
    name="sum 4w shares",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percents_h_vehicles": 3},
)
def sum_4w_shares():
    """
    sum of shares of 4w and the maximum. It's used to saturate the growth when limits are close.
    """
    return (
        float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
    )


@component.add(
    name="T fin H veh",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_t_fin_h_veh"},
)
def t_fin_h_veh():
    """
    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_fin_h_veh()


_ext_constant_t_fin_h_veh = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tfin_H_veh",
    {},
    _root,
    {},
    "_ext_constant_t_fin_h_veh",
)


@component.add(
    name="T hist H transp", units="year", comp_type="Constant", comp_subtype="Normal"
)
def t_hist_h_transp():
    """
    Year used to calibrate the historical growth of vehicles, 2015
    """
    return 2015


@component.add(
    name="T ini H veh",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_t_ini_h_veh"},
)
def t_ini_h_veh():
    """
    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_ini_h_veh()


_ext_constant_t_ini_h_veh = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tini_H_veh",
    {},
    _root,
    {},
    "_ext_constant_t_ini_h_veh",
)


@component.add(
    name="var IH E2",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a1_coef_th": 1,
        "var_percents_h_vehicles": 2,
        "saving_ratios_vehicles": 1,
        "saving_ratio_2we": 1,
        "a2_coef_th": 1,
    },
)
def var_ih_e2():
    """
    variation of the intensity of households transportation due of the change to electricity
    """
    return (
        a1_coef_th()
        * float(var_percents_h_vehicles().loc["elec 4wheels"])
        * float(saving_ratios_vehicles().loc["LV elec"])
        + a2_coef_th()
        * float(var_percents_h_vehicles().loc["elec 2wheels"])
        * saving_ratio_2we()
    )


@component.add(
    name="var IH gas2",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a1_coef_th": 1,
        "var_percents_h_vehicles": 1,
        "saving_ratios_vehicles": 1,
    },
)
def var_ih_gas2():
    """
    variation of the intensity of households transportation due of the change to gas
    """
    return (
        a1_coef_th()
        * float(var_percents_h_vehicles().loc["gas 4wheels"])
        * float(saving_ratios_vehicles().loc["LV gas"])
    )


@component.add(
    name="var IH liq2",
    units="EJ/T$/yr",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"a1_coef_th": 2, "var_percents_h_vehicles": 3, "a2_coef_th": 1},
)
def var_ih_liq2():
    """
    variation of the intensity of households transportation due of the change in liquids
    """
    return (
        a1_coef_th() * float(var_percents_h_vehicles().loc["liq 4wheels"])
        + a1_coef_th() * float(var_percents_h_vehicles().loc["hib 4wheels"])
        + a2_coef_th() * float(var_percents_h_vehicles().loc["liq 2wheels"])
    )


@component.add(
    name="var percents H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 6,
        "t_ini_h_veh": 6,
        "aux_hist_h": 6,
        "h_hyb_adapt_growth": 2,
        "rate_4w_to_2w": 2,
        "h_gas_adapt_growth": 2,
        "h_ev_adapt_growth": 2,
        "h_2we_adapt_growth": 2,
    },
)
def var_percents_h_vehicles():
    """
    Variation of vehicles percetages. Percentages relative to total 4w+2w. Before T_ini_H_veh the percentages follow historical variations
    """
    value = xr.DataArray(
        np.nan,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    )
    value.loc[["liq 4wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["liq 4wheels"]),
        lambda: -h_ev_adapt_growth()
        - h_hyb_adapt_growth()
        - h_gas_adapt_growth()
        - rate_4w_to_2w(),
    )
    value.loc[["elec 4wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["elec 4wheels"]),
        lambda: h_ev_adapt_growth(),
    )
    value.loc[["hib 4wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["hib 4wheels"]),
        lambda: h_hyb_adapt_growth(),
    )
    value.loc[["gas 4wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["gas 4wheels"]),
        lambda: h_gas_adapt_growth(),
    )
    value.loc[["liq 2wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["liq 2wheels"]),
        lambda: -h_2we_adapt_growth() + rate_4w_to_2w(),
    )
    value.loc[["elec 2wheels"]] = if_then_else(
        time() < t_ini_h_veh(),
        lambda: float(aux_hist_h().loc["elec 2wheels"]),
        lambda: h_2we_adapt_growth(),
    )
    return value


@component.add(
    name="variation energy intensity of households transport",
    units="EJ/T$/yr",
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "var_ih_liq2": 1, "var_ih_gas2": 1, "var_ih_e2": 1},
)
def variation_energy_intensity_of_households_transport():
    """
    Variation of intensity of households due to change of vehicles
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["liquids"]] = if_then_else(
        time() < 2009, lambda: 0, lambda: var_ih_liq2()
    )
    value.loc[["solids"]] = 0
    value.loc[["gases"]] = if_then_else(time() > 2009, lambda: var_ih_gas2(), lambda: 0)
    value.loc[["electricity"]] = if_then_else(
        time() > 2009, lambda: var_ih_e2(), lambda: 0
    )
    value.loc[["heat"]] = 0
    return value
