"""
Module households_transport
Translated using PySD version 3.0.0
"""


@component.add(
    name="A1 coef tH", units="EJ/T$", comp_type="Auxiliary", comp_subtype="Normal"
)
def a1_coef_th():
    """
    Coeficients for the calculation of variations of trasnport intensities
    """
    return liq_4w() / (demand_h() * (percent_4w_liq() / 100))


@component.add(
    name="A2 coef tH", units="EJ/T$", comp_type="Auxiliary", comp_subtype="Normal"
)
def a2_coef_th():
    """
    Coeficients for the calculation of variations of trasnport intensities
    """
    return liq_2w() / (demand_h() * (percent_2w_liq() / 100))


@component.add(
    name="aaux Hveh",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def aaux_hveh():
    return if_then_else(
        np.abs(time() - t_ini_hveh()) < time_step(),
        lambda: percents_h_vehicles(),
        lambda: xr.DataArray(
            0,
            {"Households vehicles": _subscript_dict["Households vehicles"]},
            ["Households vehicles"],
        ),
    )


@component.add(
    name="aaux Hveh ini",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def aaux_hveh_ini():
    return np.maximum(aaux_hveh(), aaux_hveh_t())


@component.add(
    name="aaux Hveh t",
    subscripts=["Households vehicles"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def aaux_hveh_t():
    return _delayfixed_aaux_hveh_t()


_delayfixed_aaux_hveh_t = DelayFixed(
    lambda: aaux_hveh_ini(),
    lambda: time_step(),
    lambda: xr.DataArray(
        0,
        {"Households vehicles": _subscript_dict["Households vehicles"]},
        ["Households vehicles"],
    ),
    time_step,
    "_delayfixed_aaux_hveh_t",
)


@component.add(
    name="Activate policy H transp",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def activate_policy_h_transp():
    """
    1 to set growth of alternative households transportation based on desired share in 2050, 0 for BAU linear growth
    """
    return _ext_constant_activate_policy_h_transp()


_ext_constant_activate_policy_h_transp = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "activate_poicy_hh_transp",
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
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = (
        -float(hist_var_percent_h().loc["hib 4wheels"])
        - float(hist_var_percent_h().loc["elec 4wheels"])
        - float(hist_var_percent_h().loc["gas 4wheels"])
    )
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = float(
        hist_var_percent_h().loc["hib 4wheels"]
    )
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = float(
        hist_var_percent_h().loc["elec 4wheels"]
    )
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = -float(
        hist_var_percent_h().loc["elec 2wheels"]
    )
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = float(
        hist_var_percent_h().loc["elec 2wheels"]
    )
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = float(
        hist_var_percent_h().loc["gas 4wheels"]
    )
    return value


@component.add(name="aux reach zero", comp_type="Auxiliary", comp_subtype="with Lookup")
def aux_reach_zero():
    return np.interp(
        float(energy_intensity_of_households_transport().loc["liquids"]),
        [-1.0e-02, 0.0e00, 1.0e-08, 1.0e-06, 1.0e-02, 1.0e00, 1.0e02],
        [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
    )


@component.add(
    name="Demand H", units="T$", comp_type="Constant", comp_subtype="External"
)
def demand_h():
    """
    Initial households economic demand in T dollars, in the year of start of alternative households vehicle policy (default 2015) 30.3 T$
    """
    return _ext_constant_demand_h()


_ext_constant_demand_h = ExtConstant(
    "../transport.xlsx",
    "Austria",
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
)
def effects_shortage_gas_h_veh():
    """
    The eventual scarcity of gas would likely constrain the development of NGVs/GTLs. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of NGVs/GTLs.
    """
    return if_then_else(
        abundance_gases() > 0.8, lambda: ((abundance_gases() - 0.8) * 5) ** 2, lambda: 0
    )


@component.add(
    name="Energy intensity of households transport",
    units="EJ/T$",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def energy_intensity_of_households_transport():
    return _integ_energy_intensity_of_households_transport()


_integ_energy_intensity_of_households_transport = Integ(
    lambda: variation_energy_intensity_of_households_transport(),
    lambda: initial_energy_intensity_of_households_transport_2009(),
    "_integ_energy_intensity_of_households_transport",
)


@component.add(
    name="H 2w elec adapt growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_2w_elec_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w. growth of the percentage of electric 2 wheelers vehicles is linear at first but slows down when the maximum is reached. No efects on the electricity shortage are noticed for these vehicles since their consumption is so low compared to others.
    """
    return h_2w_elec_initial_growth()


@component.add(
    name="H 2w elec initial growth", comp_type="Auxiliary", comp_subtype="Normal"
)
def h_2w_elec_initial_growth():
    """
    Growth of percent of electric 2w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_hveh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_hveh()),
            lambda: (
                float(p_h_vehicle().loc["elec 2wheels"])
                - float(percent_h_vehicles_tini().loc["elec 2wheels"])
            )
            / (t_fin_hveh() - t_ini_hveh()),
            lambda: float(aux_hist_h().loc["elec 2wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H 2w liq adapt growth", comp_type="Auxiliary", comp_subtype="Normal"
)
def h_2w_liq_adapt_growth():
    return h_2w_liq_initial_growth()


@component.add(
    name="H 2w liq initial growth", comp_type="Auxiliary", comp_subtype="Normal"
)
def h_2w_liq_initial_growth():
    return if_then_else(
        time() < t_fin_hveh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_hveh()),
            lambda: (
                float(p_h_vehicle().loc["liq 2wheels"])
                - float(percent_h_vehicles_tini().loc["liq 2wheels"])
            )
            / (t_fin_hveh() - t_ini_hveh()),
            lambda: float(aux_hist_h().loc["liq 2wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H elec adapt growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_elec_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w.growth of the percentage of EV vehicles is linear at first but adapted to the shortage of electricity and slows down when the maximum is reached
    """
    return h_elec_initial_growth()


@component.add(
    name="H elec initial growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_elec_initial_growth():
    """
    Growth of percent of electrical 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_hveh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_hveh()),
            lambda: (
                float(p_h_vehicle().loc["elec 4wheels"])
                - float(percent_h_vehicles_tini().loc["elec 4wheels"])
            )
            / (t_fin_hveh() - t_ini_hveh()),
            lambda: float(aux_hist_h().loc["elec 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H gas adapt growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_gas_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w. growth of the percentage of gas vehicles is linear at first but adapted to the shortage of gas and slows down when the maximum is reached.
    """
    return h_gas_initial_growth()


@component.add(
    name="H gas initial growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_gas_initial_growth():
    """
    Growth of percent of gas 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_hveh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_hveh()),
            lambda: (
                float(p_h_vehicle().loc["gas 4wheels"])
                - float(percent_h_vehicles_tini().loc["gas 4wheels"])
            )
            / (t_fin_hveh() - t_ini_hveh()),
            lambda: float(aux_hist_h().loc["gas 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="H hyb adapt growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_hyb_adapt_growth():
    """
    Percent relative to total number of vehicles 2w+4w.growth of the percentage of hibrid vehicles is linear at first but slows down when the maximum is reached
    """
    return h_hyb_initial_growth()


@component.add(
    name="H hyb initial growth",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def h_hyb_initial_growth():
    """
    Growth of percent of hibrid 4w without restrictions derived from saturation and shortage of electricity Percent relative to total number of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_hveh(),
        lambda: if_then_else(
            np.logical_and(activate_policy_h_transp() == 1, time() > t_ini_hveh()),
            lambda: (
                float(p_h_vehicle().loc["hib 4wheels"])
                - float(percent_h_vehicles_tini().loc["hib 4wheels"])
            )
            / (t_fin_hveh() - t_ini_hveh()),
            lambda: float(aux_hist_h().loc["hib 4wheels"]),
        ),
        lambda: 0,
    )


@component.add(
    name="hist var percent H",
    units="1/yr",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
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
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = 0
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = if_then_else(
        time() > 2005,
        lambda: (float(percent_h_vehicles_initial().loc["hib 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
        lambda: 0,
    )
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = if_then_else(
        time() < 2005,
        lambda: 0,
        lambda: (float(percent_h_vehicles_initial().loc["elec 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
    )
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = if_then_else(
        time() < 2005,
        lambda: 0,
        lambda: (float(percent_h_vehicles_initial().loc["gas 4wheels"]) - 0)
        / (t_hist_h_transp() - 2005),
    )
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = 0
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = if_then_else(
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
)
def initial_energy_intensity_of_households_transport_2009():
    """
    Initial values of household trasnport intensity. Starting year = 2009, before that year alternative vehicles are neglictible
    """
    return _ext_constant_initial_energy_intensity_of_households_transport_2009()


_ext_constant_initial_energy_intensity_of_households_transport_2009 = ExtConstant(
    "../transport.xlsx",
    "Austria",
    "initial_energy_intensity_households_transport*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    {"final sources": ["electricity", "heat", "liquids", "gases", "solids"]},
    "_ext_constant_initial_energy_intensity_of_households_transport_2009",
)


@component.add(name="Liq 2w", comp_type="Constant", comp_subtype="External")
def liq_2w():
    """
    Initial liquids used by 2 wheelers in the year of start of policies (2015 default)
    """
    return _ext_constant_liq_2w()


_ext_constant_liq_2w = ExtConstant(
    "../transport.xlsx", "Austria", "liq_2w", {}, _root, {}, "_ext_constant_liq_2w"
)


@component.add(name="Liq 4w", units="EJ", comp_type="Constant", comp_subtype="External")
def liq_4w():
    """
    liquids userd in households 4 wheelers in the initial year of policy (2015 default) 45.9341
    """
    return _ext_constant_liq_4w()


_ext_constant_liq_4w = ExtConstant(
    "../transport.xlsx", "Austria", "liq_4w", {}, _root, {}, "_ext_constant_liq_4w"
)


@component.add(
    name="N vehicles H", units="vehicles", comp_type="Constant", comp_subtype="External"
)
def n_vehicles_h():
    """
    Initial number of household vehicles in time 2015 vehicles 2w+4w 2476
    """
    return _ext_constant_n_vehicles_h()


_ext_constant_n_vehicles_h = ExtConstant(
    "../transport.xlsx",
    "Austria",
    "initial_household_vehicles",
    {},
    _root,
    {},
    "_ext_constant_n_vehicles_h",
)


@component.add(
    name="Number 2w", units="vehicles", comp_type="Auxiliary", comp_subtype="Normal"
)
def number_2w():
    """
    total number of 2w vehicles househols
    """
    return float(number_vehicles_h().loc["liq 2wheels"]) + float(
        number_vehicles_h().loc["elec 2wheels"]
    )


@component.add(
    name="Number 4w", units="vehicles", comp_type="Auxiliary", comp_subtype="Normal"
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
        / 100
    )


@component.add(
    name="P H vehicle",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = (
        1 - p_share_2wheelers() / 100
    ) * (100 - p_percent_elec_hveh() - p_percent_gas_hveh() - p_percent_hyb_hveh())
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = p_percent_elec_hveh() * (
        1 - p_share_2wheelers() / 100
    )
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = p_percent_hyb_hveh() * (
        1 - p_share_2wheelers() / 100
    )
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = p_percent_gas_hveh() * (
        1 - p_share_2wheelers() / 100
    )
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = (
        p_share_2wheelers() / 100
    ) * (100 - p_percent_2w_elec())
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = (
        p_share_2wheelers() / 100
    ) * p_percent_2w_elec()
    return value


@component.add(
    name="P percent 2w elec",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_percent_2w_elec():
    """
    Desired percent of electrical 2 wheelers in T fin our of TOTAL 2 WHEEL vehicles
    """
    return _ext_constant_p_percent_2w_elec()


_ext_constant_p_percent_2w_elec = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "percent_electric_2w_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_2w_elec",
)


@component.add(
    name="P percent elec Hveh",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_percent_elec_hveh():
    """
    Desired percent of electrical vehicles (4 wheelers) in T fin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_percent_elec_hveh()


_ext_constant_p_percent_elec_hveh = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "percent_electr_hh_4w_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_elec_hveh",
)


@component.add(
    name="P percent gas Hveh",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_percent_gas_hveh():
    """
    Desired percent of gas vehicles (4 wheelers) in Tfin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_percent_gas_hveh()


_ext_constant_p_percent_gas_hveh = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "percent_gas_hh_veh_4w_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_gas_hveh",
)


@component.add(
    name="P percent hyb Hveh",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_percent_hyb_hveh():
    """
    Desired percent of hibrid vehicles (4 wheelers) in T fin our of TOTAL 4 WHEEL vehicles
    """
    return _ext_constant_p_percent_hyb_hveh()


_ext_constant_p_percent_hyb_hveh = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "percent_hybrid_hh_4w_veh_tfin",
    {},
    _root,
    {},
    "_ext_constant_p_percent_hyb_hveh",
)


@component.add(
    name="P share 2wheelers",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def p_share_2wheelers():
    """
    desired percent of all 2 WHEELS vehicles in T fin relative to total 2w+4w, initial value in 2015 is 0.34
    """
    return _ext_constant_p_share_2wheelers()


_ext_constant_p_share_2wheelers = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "percent_2w_tfin_over_hh_veh",
    {},
    _root,
    {},
    "_ext_constant_p_share_2wheelers",
)


@component.add(
    name="percent 2w", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def percent_2w():
    """
    percentages of 2 wheels and 3 wheels vehicles
    """
    return float(percents_h_vehicles().loc["liq 2wheels"]) + float(
        percents_h_vehicles().loc["elec 2wheels"]
    )


@component.add(name="percent 2w liq", comp_type="Auxiliary", comp_subtype="Normal")
def percent_2w_liq():
    """
    Percent of 2wheelers of liquids in the initial year of policy (2015 default). percents relative to total number 4w+2w
    """
    return float(percent_h_vehicles_initial().loc["liq 2wheels"])


@component.add(
    name="percent 4w", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="percent 4w liq", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
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
)
def percent_h_vehicles_initial():
    """
    percents in the year of calibration (2015 ) of vehciles relative to total 4w+2w:
    """
    return _ext_constant_percent_h_vehicles_initial()


_ext_constant_percent_h_vehicles_initial = ExtConstant(
    "../transport.xlsx",
    "Austria",
    "percent_H_vehicles_initial*",
    {"Households vehicles": _subscript_dict["Households vehicles"]},
    _root,
    {
        "Households vehicles": [
            "liq 4wheels",
            "elec 4wheels",
            "hib 4wheels",
            "gas 4wheels",
            "liq 2wheels",
            "elec 2wheels",
        ]
    },
    "_ext_constant_percent_h_vehicles_initial",
)


@component.add(
    name="percent H vehicles Tini",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def percent_h_vehicles_tini():
    """
    percents in the year Tini of start of policy of vehicles relative to total 4w+2w:
    """
    return if_then_else(
        time() < t_ini_hveh(),
        lambda: percent_h_vehicles_initial(),
        lambda: aaux_hveh_ini(),
    )


@component.add(
    name="percents 2w H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
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
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = float(
        percents_h_vehicles().loc["liq 2wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 2wheels"])
        + float(percents_h_vehicles().loc["liq 2wheels"])
    )
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = float(
        percents_h_vehicles().loc["elec 2wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 2wheels"])
        + float(percents_h_vehicles().loc["liq 2wheels"])
    )
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = 0
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = 0
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = 0
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = 0
    return value


@component.add(
    name="percents 4w H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
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
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = float(
        percents_h_vehicles().loc["liq 4wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = float(
        percents_h_vehicles().loc["elec 4wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = float(
        percents_h_vehicles().loc["hib 4wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = float(
        percents_h_vehicles().loc["gas 4wheels"]
    ) / (
        float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
        + float(percents_h_vehicles().loc["liq 4wheels"])
    )
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = 0
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = 0
    return value


@component.add(
    name="percents H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Stateful",
    comp_subtype="Integ",
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
    value.loc[
        {"Households vehicles": ["liq 4wheels"]}
    ] = _integ_percents_h_vehicles().values
    value.loc[
        {"Households vehicles": ["elec 4wheels"]}
    ] = _integ_percents_h_vehicles_1().values
    value.loc[
        {"Households vehicles": ["hib 4wheels"]}
    ] = _integ_percents_h_vehicles_2().values
    value.loc[
        {"Households vehicles": ["gas 4wheels"]}
    ] = _integ_percents_h_vehicles_3().values
    value.loc[
        {"Households vehicles": ["liq 2wheels"]}
    ] = _integ_percents_h_vehicles_4().values
    value.loc[
        {"Households vehicles": ["elec 2wheels"]}
    ] = _integ_percents_h_vehicles_5().values
    return value


_integ_percents_h_vehicles = Integ(
    lambda: xr.DataArray(
        float(var_percents_h_vehicles().loc["liq 4wheels"]),
        {"Households vehicles": ["liq 4wheels"]},
        ["Households vehicles"],
    ),
    lambda: xr.DataArray(
        100 - initial_2w_percent(),
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
    name="ratio N veh Demand H",
    units="vehicles/T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_n_veh_demand_h():
    """
    Ration of number of vehicles by unit of household conomic demand, we assume that it is kept constant and variations are due to the change in the number of vehicles from one type to another
    """
    return n_vehicles_h() / demand_h()


@component.add(
    name="saving ratio 2wE", units="Dmnl", comp_type="Constant", comp_subtype="External"
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
    name="T fin Hveh", units="Year", comp_type="Constant", comp_subtype="External"
)
def t_fin_hveh():
    """
    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_fin_hveh()


_ext_constant_t_fin_hveh = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "tfin_policy_hh_veh",
    {},
    _root,
    {},
    "_ext_constant_t_fin_hveh",
)


@component.add(
    name="T hist H transp", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def t_hist_h_transp():
    """
    Year used to calibrate the historical growth of vehicles, 2015
    """
    return 2015


@component.add(
    name="T ini Hveh", units="Year", comp_type="Constant", comp_subtype="External"
)
def t_ini_hveh():
    """
    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_ini_hveh()


_ext_constant_t_ini_hveh = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "tini_policy_hh_veh",
    {},
    _root,
    {},
    "_ext_constant_t_ini_hveh",
)


@component.add(
    name="var IH E2", units="EJ/T$/yr", comp_type="Auxiliary", comp_subtype="Normal"
)
def var_ih_e2():
    """
    variation of the intensity of households transportation due of the change to electricity
    """
    return (
        a1_coef_th()
        * (float(var_percents_h_vehicles().loc["elec 4wheels"]) / 100)
        * float(saving_ratios_vehicles().loc["LV elec"])
        + a2_coef_th()
        * (float(var_percents_h_vehicles().loc["elec 2wheels"]) / 100)
        * saving_ratio_2we()
    )


@component.add(
    name="var IH gas2", units="EJ/T$/yr", comp_type="Auxiliary", comp_subtype="Normal"
)
def var_ih_gas2():
    """
    variation of the intensity of households transportation due of the change to gas
    """
    return (
        a1_coef_th()
        * (float(var_percents_h_vehicles().loc["gas 4wheels"]) / 100)
        * float(saving_ratios_vehicles().loc["LV gas"])
    )


@component.add(
    name="var IH liq2", units="EJ/T$/yr", comp_type="Auxiliary", comp_subtype="Normal"
)
def var_ih_liq2():
    """
    variation of the intensity of households transportation due of the change in liquids
    """
    return (
        a1_coef_th() * (float(var_percents_h_vehicles().loc["liq 4wheels"]) / 100)
        + a1_coef_th() * (float(var_percents_h_vehicles().loc["hib 4wheels"]) / 100)
        + a2_coef_th() * (float(var_percents_h_vehicles().loc["liq 2wheels"]) / 100)
    )


@component.add(
    name="var percents H vehicles",
    units="Dmnl",
    subscripts=["Households vehicles"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    value.loc[{"Households vehicles": ["liq 4wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["liq 4wheels"]),
        lambda: -h_elec_adapt_growth()
        - h_hyb_adapt_growth()
        - h_gas_adapt_growth()
        - h_2w_elec_adapt_growth()
        - h_2w_liq_adapt_growth(),
    )
    value.loc[{"Households vehicles": ["elec 4wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["elec 4wheels"]),
        lambda: h_elec_adapt_growth(),
    )
    value.loc[{"Households vehicles": ["hib 4wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["hib 4wheels"]),
        lambda: h_hyb_adapt_growth(),
    )
    value.loc[{"Households vehicles": ["gas 4wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["gas 4wheels"]),
        lambda: h_gas_adapt_growth(),
    )
    value.loc[{"Households vehicles": ["liq 2wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["liq 2wheels"]),
        lambda: h_2w_liq_adapt_growth(),
    )
    value.loc[{"Households vehicles": ["elec 2wheels"]}] = if_then_else(
        time() < t_ini_hveh(),
        lambda: float(aux_hist_h().loc["elec 2wheels"]),
        lambda: h_2w_elec_adapt_growth(),
    )
    return value


@component.add(
    name="variation energy intensity of households transport",
    units="EJ/T$/yr",
    subscripts=["final sources"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
)
def variation_energy_intensity_of_households_transport():
    """
    Variation of intensity of households due to change of vehicles
    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["liquids"]}] = (
        if_then_else(time() < 2009, lambda: 0, lambda: var_ih_liq2()) * aux_reach_zero()
    )
    value.loc[{"final sources": ["solids"]}] = 0
    value.loc[{"final sources": ["gases"]}] = (
        if_then_else(time() > 2009, lambda: var_ih_gas2(), lambda: 0) * aux_reach_zero()
    )
    value.loc[{"final sources": ["electricity"]}] = (
        if_then_else(time() > 2009, lambda: var_ih_e2(), lambda: 0) * aux_reach_zero()
    )
    value.loc[{"final sources": ["heat"]}] = 0
    return value
