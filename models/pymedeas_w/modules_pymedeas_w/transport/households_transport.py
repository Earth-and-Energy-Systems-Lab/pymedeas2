"""
Module households_transport
Translated using PySD version 2.2.1
"""


def a1_coef_th():
    """
    Real Name: A1 coef tH
    Original Eqn: ((Liq 4w/Demand H)-(A2 coef tH*percent 2w liq))/percent 4w liq
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    Coeficients for the calculation of variations of trasnport intensities        A1=  ( LH t(0) / DH(0)  - A2%Hliq2w  )/ %Hliq
    """
    return (
        (liq_4w() / demand_h()) - (a2_coef_th() * percent_2w_liq())
    ) / percent_4w_liq()


def a2_coef_th():
    """
    Real Name: A2 coef tH
    Original Eqn: Electricity 2wE/(Demand H*percent H vehicles initial[elec 2wheels]*saving ratio 2wE)
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    Coeficients for the calculation of variations of trasnport intensities        A2 = EH 2w(0)  / ( DH(0) %HE2w ·srE2w )=
    """
    return electricity_2we() / (
        demand_h()
        * float(percent_h_vehicles_initial().loc["elec 2wheels"])
        * saving_ratio_2we()
    )


def activate_policy_h_transp():
    """
    Real Name: Activate policy H transp
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'activate_policy_Households_trans')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1 to set growth of alternative households transportation based on desired
        share in 2050, 0 for BAU linear growth
    """
    return _ext_constant_activate_policy_h_transp()


@subs(["Households vehicles"], _subscript_dict)
def aux_hist_h():
    """
    Real Name: aux hist H
    Original Eqn:
      -hist var percent H[hib 4wheels]-hist var percent H[elec 4wheels]-hist var percent H[gas 4wheels]
        .
        .
        .
      hist var percent H[gas 4wheels]
    Units: 1/yr
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    auxiliar variable to set the variation of liquid vehicles
    """
    return xrmerge(
        rearrange(
            -float(hist_var_percent_h().loc["hib 4wheels"])
            - float(hist_var_percent_h().loc["elec 4wheels"])
            - float(hist_var_percent_h().loc["gas 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            float(hist_var_percent_h().loc["hib 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            float(hist_var_percent_h().loc["elec 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            -float(hist_var_percent_h().loc["elec 2wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            float(hist_var_percent_h().loc["elec 2wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
        rearrange(
            float(hist_var_percent_h().loc["gas 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
    )


def demand_h():
    """
    Real Name: Demand H
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_households_demand')
    Units: T$
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial households economic demand in T dollars, in the year of start of
        alternative households vehicle policy (default 2015)  30.3 T$
    """
    return _ext_constant_demand_h()


def effects_shortage_elec_on_ev():
    """
    Real Name: effects shortage elec on EV
    Original Eqn: IF THEN ELSE(Abundance electricity>0.8, ((Abundance electricity -0.8)*5)^2, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The eventual scarcity of electricity would likely constrain the
        development of EVs. The proposed relationship avoids an abrupt limitation
        by introducing a range (1;0.8) in the electricity abundance that
        constrains the development of EVs.
    """
    return if_then_else(
        abundance_electricity() > 0.8,
        lambda: ((abundance_electricity() - 0.8) * 5) ** 2,
        lambda: 0,
    )


def effects_shortage_gas_h_veh():
    """
    Real Name: effects shortage gas H veh
    Original Eqn: IF THEN ELSE(abundance gases>0.8, ((abundance gases-0.8)*5)^2, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The eventual scarcity of gas would likely constrain the development of
        NGVs/GTLs. The proposed relationship avoids an abrupt limitation by
        introducing a range (1;0.8) in the gas abundance that constrains the
        development of NGVs/GTLs.
    """
    return if_then_else(
        abundance_gases() > 0.8, lambda: ((abundance_gases() - 0.8) * 5) ** 2, lambda: 0
    )


def electricity_2we():
    """
    Real Name: Electricity 2wE
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'elec_2w')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial electricity used by 2 wheelers in the year of start of policies
        (2015 default) 0.3415
    """
    return _ext_constant_electricity_2we()


@subs(["final sources"], _subscript_dict)
def energy_intensity_of_households_transport():
    """
    Real Name: Energy intensity of households transport
    Original Eqn: INTEG ( variation energy intensity of households transport[final sources], Initial energy intensity of households transport 2009[final sources])
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return _integ_energy_intensity_of_households_transport()


def h_2w_initial_growth():
    """
    Real Name: H 2w initial growth
    Original Eqn: IF THEN ELSE(Time<T fin H veh,IF THEN ELSE( Activate policy H transp =1:AND:Time>T ini H veh, (P H vehicle[elec 2wheels]-percent H vehicles initial[elec 2wheels] )/(T fin H veh-T ini H veh),aux hist H[ elec 2wheels ]),0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Growth of percent of electric 2w without restrictions derived from
        saturation and shortage of electricity  Percent relative to total number
        of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["elec 2wheels"])
                - float(percent_h_vehicles_initial().loc["elec 2wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["elec 2wheels"]),
        ),
        lambda: 0,
    )


def h_2we_adapt_growth():
    """
    Real Name: H 2wE adapt growth
    Original Eqn: H 2w initial growth
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Percent relative to total number of vehicles 2w+4w. growth of the
        percentage of electric 2 wheelers  vehicles is linear at first but slows
        down when the maximum is reached. No efects on the electricity shortage
        are noticed for these vehicles since their consumption is so low compared
        to others.
    """
    return h_2w_initial_growth()


def h_elec_initial_growth():
    """
    Real Name: H elec initial growth
    Original Eqn: IF THEN ELSE(Time<T fin H veh,IF THEN ELSE( Activate policy H transp =1:AND: Time>T ini H veh,(P H vehicle[elec 4wheels]-percent H vehicles initial[elec 4wheels] )/(T fin H veh-T ini H veh), aux hist H[ elec 4wheels]),0)
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Growth of percent of electrical 4w without restrictions derived from
        saturation and shortage of electricity  Percent relative to total number
        of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["elec 4wheels"])
                - float(percent_h_vehicles_initial().loc["elec 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["elec 4wheels"]),
        ),
        lambda: 0,
    )


def h_ev_adapt_growth():
    """
    Real Name: H EV adapt growth
    Original Eqn: H elec initial growth*effects shortage elec on EV
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Percent relative to total number of vehicles 2w+4w.growth of the
        percentage of EV vehicles is linear at first but adapted to the shortage
        of electricity and slows down when the maximum is reached
    """
    return h_elec_initial_growth() * effects_shortage_elec_on_ev()


def h_gas_adapt_growth():
    """
    Real Name: H gas adapt growth
    Original Eqn: H gas initial growth*effects shortage gas H veh
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Percent relative to total number of vehicles 2w+4w.  growth of the
        percentage of gas vehicles is linear at first but adapted to the shortage
        of gas and slows down when the maximum is reached.
    """
    return h_gas_initial_growth() * effects_shortage_gas_h_veh()


def h_gas_initial_growth():
    """
    Real Name: H gas initial growth
    Original Eqn: IF THEN ELSE(Time<T fin H veh,IF THEN ELSE( Activate policy H transp =1:AND:Time>T ini H veh, (P H vehicle[gas 4wheels]-percent H vehicles initial[gas 4wheels] )/(T fin H veh-T ini H veh),aux hist H[ gas 4wheels ]),0)
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Growth of percent of gas 4w without restrictions derived from saturation
        and shortage of electricity  Percent relative to total number of vehicles
        2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["gas 4wheels"])
                - float(percent_h_vehicles_initial().loc["gas 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["gas 4wheels"]),
        ),
        lambda: 0,
    )


def h_hyb_adapt_growth():
    """
    Real Name: H hyb adapt growth
    Original Eqn: H hyb initial growth
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Percent relative to total number of vehicles 2w+4w.growth of the
        percentage of hibrid vehicles is linear at first but slows down when the
        maximum is reached
    """
    return h_hyb_initial_growth()


def h_hyb_initial_growth():
    """
    Real Name: H hyb initial growth
    Original Eqn: IF THEN ELSE(Time<T fin H veh,IF THEN ELSE( Activate policy H transp =1:AND:Time>T ini H veh,(P H vehicle[hib 4wheels]-percent H vehicles initial[hib 4wheels] )/(T fin H veh-T ini H veh),aux hist H[ hib 4wheels ]),0)
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Growth of percent of hibrid 4w without restrictions derived from
        saturation and shortage of electricity  Percent relative to total number
        of vehicles 2w+4w.
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (
                float(p_h_vehicle().loc["hib 4wheels"])
                - float(percent_h_vehicles_initial().loc["hib 4wheels"])
            )
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: float(aux_hist_h().loc["hib 4wheels"]),
        ),
        lambda: 0,
    )


@subs(["Households vehicles"], _subscript_dict)
def hist_var_percent_h():
    """
    Real Name: hist var percent H
    Original Eqn:
      0
        .
        .
        .
      IF THEN ELSE( Time<2005,0, (percent H vehicles initial[elec 2wheels]-0)/(T hist H transp-2005))
    Units: 1/yr
    Limits: (None, None)
    Type: constant
    Subs: ['Households vehicles']

    historical evolution of percent of vehicles based on the linear
        interpolation between 2005 and T hist H transp(default 2015). Before 2005
        all vehicle s are liquid based. Percents relative to 2w+4w
    """
    return xrmerge(
        xr.DataArray(
            0, {"Households vehicles": ["liq 4wheels"]}, ["Households vehicles"]
        ),
        rearrange(
            if_then_else(
                time() > 2005,
                lambda: (float(percent_h_vehicles_initial().loc["hib 4wheels"]) - 0)
                / (t_hist_h_transp() - 2005),
                lambda: 0,
            ),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < 2005,
                lambda: 0,
                lambda: (float(percent_h_vehicles_initial().loc["elec 4wheels"]) - 0)
                / (t_hist_h_transp() - 2005),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < 2005,
                lambda: 0,
                lambda: (float(percent_h_vehicles_initial().loc["gas 4wheels"]) - 0)
                / (t_hist_h_transp() - 2005),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        xr.DataArray(
            0, {"Households vehicles": ["liq 2wheels"]}, ["Households vehicles"]
        ),
        rearrange(
            if_then_else(
                time() < 2005,
                lambda: 0,
                lambda: (float(percent_h_vehicles_initial().loc["elec 2wheels"]) - 0)
                / (t_hist_h_transp() - 2005),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def increase_households_energy_final_demand_for_transp():
    """
    Real Name: increase Households energy final demand for Transp
    Original Eqn: (Energy intensity of households transport[final sources]-Initial energy intensity of households transport 2009[final sources])*Household demand total/1e+06
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return (
        (
            energy_intensity_of_households_transport()
            - initial_energy_intensity_of_households_transport_2009()
        )
        * household_demand_total()
        / 1e06
    )


def initial_2w_percent():
    """
    Real Name: initial 2w percent
    Original Eqn: percent H vehicles initial[liq 2wheels]+percent H vehicles initial[elec 2wheels]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    2015 percent of 2 wheelers 0,332
    """
    return float(percent_h_vehicles_initial().loc["liq 2wheels"]) + float(
        percent_h_vehicles_initial().loc["elec 2wheels"]
    )


@subs(["final sources"], _subscript_dict)
def initial_energy_intensity_of_households_transport_2009():
    """
    Real Name: Initial energy intensity of households transport 2009
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_energy_intensity_households_transport*')
    Units: EJ/T$
    Limits: (None, None)
    Type: constant
    Subs: ['final sources']

    Initial values of household trasnport intensity. Starting year = 2009,
        before that year alternative vehicles are neglictible
    """
    return _ext_constant_initial_energy_intensity_of_households_transport_2009()


def liq_4w():
    """
    Real Name: Liq 4w
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'liq_4w')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    liquids userd in households 4 wheelers in the initial year of policy (2015 default)        45.9341
    """
    return _ext_constant_liq_4w()


def max_percent_2_wheels():
    """
    Real Name: max percent 2 wheels
    Original Eqn: INTEG ( rate 4w to 2w, initial 2w percent)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    maximum share of 2wheel vehicles (in terms of number of vehicles)
        policies or shortage can make people move form 4wheel vehicles to two
        wheelers
    """
    return _integ_max_percent_2_wheels()


def max_percent_4_wheels():
    """
    Real Name: max percent 4 wheels
    Original Eqn: INTEG ( -rate 4w to 2w, 1-initial 2w percent)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    max percent of 4 wheelers relative to total amount 2w+4w
    """
    return _integ_max_percent_4_wheels()


def n_vehicles_h():
    """
    Real Name: N vehicles H
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_household_vehicles')
    Units: vehicles
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial number of household vehicles in time  2015 vehicles 2w+4w  2476
    """
    return _ext_constant_n_vehicles_h()


def number_2w():
    """
    Real Name: Number 2w
    Original Eqn: Number vehicles H[liq 2wheels]+Number vehicles H[elec 2wheels]
    Units: vehicles
    Limits: (None, None)
    Type: component
    Subs: None

    total number of 2w vehicles househols
    """
    return float(number_vehicles_h().loc["liq 2wheels"]) + float(
        number_vehicles_h().loc["elec 2wheels"]
    )


def number_4w():
    """
    Real Name: Number 4w
    Original Eqn: Number vehicles H[liq 4wheels]+Number vehicles H[hib 4wheels]+Number vehicles H[elec 4wheels]+Number vehicles H[gas 4wheels]
    Units: vehicles
    Limits: (None, None)
    Type: component
    Subs: None

    agregated number of 4w vehicles
    """
    return (
        float(number_vehicles_h().loc["liq 4wheels"])
        + float(number_vehicles_h().loc["hib 4wheels"])
        + float(number_vehicles_h().loc["elec 4wheels"])
        + float(number_vehicles_h().loc["gas 4wheels"])
    )


@subs(["Households vehicles"], _subscript_dict)
def number_vehicles_h():
    """
    Real Name: Number vehicles H
    Original Eqn: ratio N veh Demand H*Household demand total*1e-06*percents H vehicles[ Households vehicles]
    Units: vehicles
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    Estimated number of households vehicles asuming constant ratios of
        vehicles per households demand
    """
    return (
        ratio_n_veh_demand_h()
        * household_demand_total()
        * 1e-06
        * percents_h_vehicles()
    )


def p_2we():
    """
    Real Name: P 2wE
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_electric_2w_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Desired percent of electrical 2 wheelers in T fin our of TOTAL 2 WHEEL
        vehicles
    """
    return _ext_constant_p_2we()


def p_elec():
    """
    Real Name: P elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_electric_household_4w_veh_transp')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Desired percent of electrical vehicles (4 wheelers) in T fin our of TOTAL
        4 WHEEL vehicles
    """
    return _ext_constant_p_elec()


def p_gas():
    """
    Real Name: P gas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_gas_hh_veh_4w_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Desired percent of gas vehicles (4 wheelers) in Tfin our of TOTAL 4 WHEEL
        vehicles
    """
    return _ext_constant_p_gas()


@subs(["Households vehicles"], _subscript_dict)
def p_h_vehicle():
    """
    Real Name: P H vehicle
    Original Eqn:
      (1-P share 2 wheelers)*(-P elec-P gas-P hyb )
        .
        .
        .
      P share 2 wheelers*P 2wE
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    desired percent of vehicles from each type in T fin. These are percentages
        relatives TO THE TOTAL AMOUNT OF VEHICLES ( 2 wheelers + 4 wheelers).
    """
    return xrmerge(
        rearrange(
            (1 - p_share_2_wheelers()) * (-p_elec() - p_gas() - p_hyb()),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            p_elec() * (1 - p_share_2_wheelers()),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            p_hyb() * (1 - p_share_2_wheelers()),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            p_gas() * (1 - p_share_2_wheelers()),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        rearrange(
            p_share_2_wheelers() * (1 - p_2we()),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            p_share_2_wheelers() * p_2we(),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
    )


def p_hyb():
    """
    Real Name: P hyb
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_hybrid_household_4w_veh_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Desired percent of hibrid vehicles (4 wheelers) in T fin our of TOTAL 4
        WHEEL vehicles
    """
    return _ext_constant_p_hyb()


def p_share_2_wheelers():
    """
    Real Name: P share 2 wheelers
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_change_2w_h_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    desired percent of all 2 WHEELS vehicles in T fin relative to total 2w+4w,
        initial value in 2015 is 0.34
    """
    return _ext_constant_p_share_2_wheelers()


def percent_2w():
    """
    Real Name: percent 2w
    Original Eqn: percents H vehicles[liq 2wheels]+percents H vehicles[elec 2wheels]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    percentages of 2 wheels and 3 wheels vehicles
    """
    return float(percents_h_vehicles().loc["liq 2wheels"]) + float(
        percents_h_vehicles().loc["elec 2wheels"]
    )


def percent_2w_liq():
    """
    Real Name: percent 2w liq
    Original Eqn: percent H vehicles initial[liq 2wheels]
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Percent of 2wheelers of liquids in the initial year of policy (2015
        default). percents relative to total number 4w+2w   DEFAULT: 0.2712
    """
    return float(percent_h_vehicles_initial().loc["liq 2wheels"])


def percent_4w():
    """
    Real Name: percent 4w
    Original Eqn: percents H vehicles[liq 4wheels]+percents H vehicles[hib 4wheels]+percents H vehicles[elec 4wheels]+percents H vehicles[gas 4wheels]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    percentages of  4 wheels vehicles
    """
    return (
        float(percents_h_vehicles().loc["liq 4wheels"])
        + float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
    )


def percent_4w_liq():
    """
    Real Name: percent 4w liq
    Original Eqn: percent H vehicles initial[liq 4wheels]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Percent of 4wheelers of liquids in the initial year of policy (2015
        default). percents relative to total number 4w+2w  0.658
    """
    return float(percent_h_vehicles_initial().loc["liq 4wheels"])


@subs(["Households vehicles"], _subscript_dict)
def percent_h_vehicles_initial():
    """
    Real Name: percent H vehicles initial
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'percent_H_vehicles_initial*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['Households vehicles']

    percents in the year of calibration (2015 ) of vehciles relative to total
        4w+2w:
    """
    return _ext_constant_percent_h_vehicles_initial()


@subs(["Households vehicles"], _subscript_dict)
def percents_2w_h_vehicles():
    """
    Real Name: percents 2w H vehicles
    Original Eqn:
      percents H vehicles[liq 2wheels]/(percents H vehicles[elec 2wheels]+percents H vehicles[liq 2wheels])
        .
        .
        .
      0
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    Percent of electrical 2 wheeler as a percent of ONLY TWO WHEELERS
    """
    return xrmerge(
        rearrange(
            float(percents_h_vehicles().loc["liq 2wheels"])
            / (
                float(percents_h_vehicles().loc["elec 2wheels"])
                + float(percents_h_vehicles().loc["liq 2wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            float(percents_h_vehicles().loc["elec 2wheels"])
            / (
                float(percents_h_vehicles().loc["elec 2wheels"])
                + float(percents_h_vehicles().loc["liq 2wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
        xr.DataArray(
            0, {"Households vehicles": ["liq 4wheels"]}, ["Households vehicles"]
        ),
        xr.DataArray(
            0, {"Households vehicles": ["elec 4wheels"]}, ["Households vehicles"]
        ),
        xr.DataArray(
            0, {"Households vehicles": ["gas 4wheels"]}, ["Households vehicles"]
        ),
        xr.DataArray(
            0, {"Households vehicles": ["hib 4wheels"]}, ["Households vehicles"]
        ),
    )


@subs(["Households vehicles"], _subscript_dict)
def percents_4w_h_vehicles():
    """
    Real Name: percents 4w H vehicles
    Original Eqn:
      percents H vehicles[liq 4wheels]/(percents H vehicles[elec 4wheels]+percents H vehicles[hib 4wheels]+percents H vehicles[gas 4wheels]+percents H vehicles[liq 4wheels])
        .
        .
        .
      0
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    Percent of alternative 4 wheelers as a percent of ONLY 4 WHEELERS
    """
    return xrmerge(
        rearrange(
            float(percents_h_vehicles().loc["liq 4wheels"])
            / (
                float(percents_h_vehicles().loc["elec 4wheels"])
                + float(percents_h_vehicles().loc["hib 4wheels"])
                + float(percents_h_vehicles().loc["gas 4wheels"])
                + float(percents_h_vehicles().loc["liq 4wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            float(percents_h_vehicles().loc["elec 4wheels"])
            / (
                float(percents_h_vehicles().loc["elec 4wheels"])
                + float(percents_h_vehicles().loc["hib 4wheels"])
                + float(percents_h_vehicles().loc["gas 4wheels"])
                + float(percents_h_vehicles().loc["liq 4wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            float(percents_h_vehicles().loc["hib 4wheels"])
            / (
                float(percents_h_vehicles().loc["elec 4wheels"])
                + float(percents_h_vehicles().loc["hib 4wheels"])
                + float(percents_h_vehicles().loc["gas 4wheels"])
                + float(percents_h_vehicles().loc["liq 4wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            float(percents_h_vehicles().loc["gas 4wheels"])
            / (
                float(percents_h_vehicles().loc["elec 4wheels"])
                + float(percents_h_vehicles().loc["hib 4wheels"])
                + float(percents_h_vehicles().loc["gas 4wheels"])
                + float(percents_h_vehicles().loc["liq 4wheels"])
            ),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        xr.DataArray(
            0, {"Households vehicles": ["liq 2wheels"]}, ["Households vehicles"]
        ),
        xr.DataArray(
            0, {"Households vehicles": ["elec 2wheels"]}, ["Households vehicles"]
        ),
    )


@subs(["Households vehicles"], _subscript_dict)
def percents_h_vehicles():
    """
    Real Name: percents H vehicles
    Original Eqn:
      INTEG ( var percents H vehicles[liq 4wheels], 1-initial 2w percent)
        .
        .
        .
      INTEG ( var percents H vehicles[elec 2wheels], 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    Percent relative to total number of vehicles 2w+4w.        Initial percentages in 1995 of alternative vehicles are considered cero,
        This is done that way in order to allow a lineal growth that matches
        historical vehaviour from 2005 to 2015. Percents relative to total 4w+2w.
    """
    return xrmerge(
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            _integ_percents_h_vehicles(),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
    )


def policy_2wheels():
    """
    Real Name: policy 2wheels
    Original Eqn: IF THEN ELSE(Time<T fin H veh,IF THEN ELSE( Activate policy H transp =1:AND:Time>T ini H veh,(P share 2 wheelers -initial 2w percent)/(T fin H veh-T ini H veh),0),0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Growth of percent of all types of 2wheelers relative to the total amount
        of vehicles. relative to all vehicles 2w+4w
    """
    return if_then_else(
        time() < t_fin_h_veh(),
        lambda: if_then_else(
            logical_and(activate_policy_h_transp() == 1, time() > t_ini_h_veh()),
            lambda: (p_share_2_wheelers() - initial_2w_percent())
            / (t_fin_h_veh() - t_ini_h_veh()),
            lambda: 0,
        ),
        lambda: 0,
    )


def rate_4w_to_2w():
    """
    Real Name: rate 4w to 2w
    Original Eqn: policy 2wheels
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    change from 4 wheelers based mobility to 2 wheelers, linear change until
        the limit aproaches
    """
    return policy_2wheels()


def ratio_n_veh_demand_h():
    """
    Real Name: ratio N veh Demand H
    Original Eqn: N vehicles H/Demand H
    Units: vehicles/T$
    Limits: (None, None)
    Type: component
    Subs: None

    Ration of number of vehicles by unit of household conomic demand, we
        assume that it is kept constant and variations are due to the change in
        the number of vehicles from one type to another
    """
    return n_vehicles_h() / demand_h()


def saving_ratio_2we():
    """
    Real Name: saving ratio 2wE
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'saving_ratio_2wE')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    saving ratio of electrical 2wheelers compared to gasoline 2 wheelers
    """
    return _ext_constant_saving_ratio_2we()


def share_available_2w():
    """
    Real Name: share available 2w
    Original Eqn: (max percent 2 wheels-percents H vehicles[elec 2wheels])/max percent 2 wheels
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Difference between the share of 2w and the maximum. It's used to saturate
        the growth when limits are close. share of 2w relative to total amount
        2w+4w
    """
    return (
        max_percent_2_wheels() - float(percents_h_vehicles().loc["elec 2wheels"])
    ) / max_percent_2_wheels()


def share_available_4w():
    """
    Real Name: share available 4w
    Original Eqn: (max percent 4 wheels-sum 4w shares)/max percent 4 wheels
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    share of 4wheelers available for alternatives. Percent relative to total
        number of vehicles 2w+4w.It's used to saturate the growth when limits are
        close
    """
    return (max_percent_4_wheels() - sum_4w_shares()) / max_percent_4_wheels()


def sum_4w_shares():
    """
    Real Name: sum 4w shares
    Original Eqn: percents H vehicles[hib 4wheels]+percents H vehicles[elec 4wheels]+percents H vehicles[gas 4wheels]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    sum of shares of 4w and the maximum. It's used to saturate the growth
        when limits are close.
    """
    return (
        float(percents_h_vehicles().loc["hib 4wheels"])
        + float(percents_h_vehicles().loc["elec 4wheels"])
        + float(percents_h_vehicles().loc["gas 4wheels"])
    )


def t_fin_h_veh():
    """
    Real Name: T fin H veh
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'tfin_H_veh')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_fin_h_veh()


def t_hist_h_transp():
    """
    Real Name: T hist H transp
    Original Eqn: 2015
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year used to calibrate the historical growth of vehicles, 2015
    """
    return 2015


def t_ini_h_veh():
    """
    Real Name: T ini H veh
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'tini_H_veh')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Time when policies of change in percentages of household vehicles start
    """
    return _ext_constant_t_ini_h_veh()


def var_ih_e2():
    """
    Real Name: var IH E2
    Original Eqn: A1 coef tH*var percents H vehicles[elec 4wheels]*saving ratios vehicles[LV elec]+A2 coef tH*var percents H vehicles[elec 2wheels]*saving ratio 2wE
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    variation of the intensity of households transportation due of the change
        to electricity
    """
    return (
        a1_coef_th()
        * float(var_percents_h_vehicles().loc["elec 4wheels"])
        * float(saving_ratios_vehicles().loc["LV elec"])
        + a2_coef_th()
        * float(var_percents_h_vehicles().loc["elec 2wheels"])
        * saving_ratio_2we()
    )


def var_ih_gas2():
    """
    Real Name: var IH gas2
    Original Eqn: A1 coef tH*var percents H vehicles[gas 4wheels]*saving ratios vehicles[LV gas]
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    variation of the intensity of households transportation due of the change
        to gas
    """
    return (
        a1_coef_th()
        * float(var_percents_h_vehicles().loc["gas 4wheels"])
        * float(saving_ratios_vehicles().loc["LV gas"])
    )


def var_ih_liq2():
    """
    Real Name: var IH liq2
    Original Eqn: A1 coef tH*var percents H vehicles[liq 4wheels]+A1 coef tH*var percents H vehicles[hib 4wheels]+A2 coef tH*var percents H vehicles[liq 2wheels]
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    variation of the intensity of households transportation due of the change
        in liquids
    """
    return (
        a1_coef_th() * float(var_percents_h_vehicles().loc["liq 4wheels"])
        + a1_coef_th() * float(var_percents_h_vehicles().loc["hib 4wheels"])
        + a2_coef_th() * float(var_percents_h_vehicles().loc["liq 2wheels"])
    )


@subs(["Households vehicles"], _subscript_dict)
def var_percents_h_vehicles():
    """
    Real Name: var percents H vehicles
    Original Eqn:
      IF THEN ELSE( Time<T ini H veh,aux hist H[liq 4wheels], -H EV adapt growth-H hyb adapt growth-H gas adapt growth-rate 4w to 2w)
        .
        .
        .
      IF THEN ELSE( Time<T ini H veh,aux hist H[elec 2wheels],H 2wE adapt growth)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['Households vehicles']

    Variation of vehicles percetages. Percentages relative to total 4w+2w.
        Before T_ini_H_veh the percentages follow historical variations
    """
    return xrmerge(
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["liq 4wheels"]),
                lambda: -h_ev_adapt_growth()
                - h_hyb_adapt_growth()
                - h_gas_adapt_growth()
                - rate_4w_to_2w(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["elec 4wheels"]),
                lambda: h_ev_adapt_growth(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["hib 4wheels"]),
                lambda: h_hyb_adapt_growth(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["gas 4wheels"]),
                lambda: h_gas_adapt_growth(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["liq 2wheels"]),
                lambda: -h_2we_adapt_growth() + rate_4w_to_2w(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            if_then_else(
                time() < t_ini_h_veh(),
                lambda: float(aux_hist_h().loc["elec 2wheels"]),
                lambda: h_2we_adapt_growth(),
            ),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def variation_energy_intensity_of_households_transport():
    """
    Real Name: variation energy intensity of households transport
    Original Eqn:
      IF THEN ELSE(Time<2009,0,var IH liq2)
      0
      IF THEN ELSE(Time>2009,var IH gas2,0)
      IF THEN ELSE(Time>2009,var IH E2,0)
      0
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Variation of intensity of households due to change of vehicles
    """
    return xrmerge(
        rearrange(
            if_then_else(time() < 2009, lambda: 0, lambda: var_ih_liq2()),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        xr.DataArray(0, {"final sources": ["solids"]}, ["final sources"]),
        rearrange(
            if_then_else(time() > 2009, lambda: var_ih_gas2(), lambda: 0),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            if_then_else(time() > 2009, lambda: var_ih_e2(), lambda: 0),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
    )


_ext_constant_activate_policy_h_transp = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "activate_policy_Households_trans",
    {},
    _root,
    "_ext_constant_activate_policy_h_transp",
)


_ext_constant_demand_h = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_households_demand",
    {},
    _root,
    "_ext_constant_demand_h",
)


_ext_constant_electricity_2we = ExtConstant(
    "../transport.xlsx", "World", "elec_2w", {}, _root, "_ext_constant_electricity_2we"
)


@subs(["final sources"], _subscript_dict)
def _integ_init_energy_intensity_of_households_transport():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for energy_intensity_of_households_transport
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for energy_intensity_of_households_transport function
    """
    return initial_energy_intensity_of_households_transport_2009()


@subs(["final sources"], _subscript_dict)
def _integ_input_energy_intensity_of_households_transport():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for energy_intensity_of_households_transport
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for energy_intensity_of_households_transport function
    """
    return variation_energy_intensity_of_households_transport()


_integ_energy_intensity_of_households_transport = Integ(
    _integ_input_energy_intensity_of_households_transport,
    _integ_init_energy_intensity_of_households_transport,
    "_integ_energy_intensity_of_households_transport",
)


_ext_constant_initial_energy_intensity_of_households_transport_2009 = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_energy_intensity_households_transport*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    "_ext_constant_initial_energy_intensity_of_households_transport_2009",
)


_ext_constant_liq_4w = ExtConstant(
    "../transport.xlsx", "World", "liq_4w", {}, _root, "_ext_constant_liq_4w"
)


_integ_max_percent_2_wheels = Integ(
    lambda: rate_4w_to_2w(), lambda: initial_2w_percent(), "_integ_max_percent_2_wheels"
)


_integ_max_percent_4_wheels = Integ(
    lambda: -rate_4w_to_2w(),
    lambda: 1 - initial_2w_percent(),
    "_integ_max_percent_4_wheels",
)


_ext_constant_n_vehicles_h = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_household_vehicles",
    {},
    _root,
    "_ext_constant_n_vehicles_h",
)


_ext_constant_p_2we = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_2w_tfin",
    {},
    _root,
    "_ext_constant_p_2we",
)


_ext_constant_p_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_household_4w_veh_transp",
    {},
    _root,
    "_ext_constant_p_elec",
)


_ext_constant_p_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_hh_veh_4w_tfin",
    {},
    _root,
    "_ext_constant_p_gas",
)


_ext_constant_p_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_household_4w_veh_tfin",
    {},
    _root,
    "_ext_constant_p_hyb",
)


_ext_constant_p_share_2_wheelers = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_change_2w_h_tfin",
    {},
    _root,
    "_ext_constant_p_share_2_wheelers",
)


_ext_constant_percent_h_vehicles_initial = ExtConstant(
    "../transport.xlsx",
    "World",
    "percent_H_vehicles_initial*",
    {"Households vehicles": _subscript_dict["Households vehicles"]},
    _root,
    "_ext_constant_percent_h_vehicles_initial",
)


@subs(["Households vehicles"], _subscript_dict)
def _integ_init_percents_h_vehicles():
    """
    Real Name: Implicit
    Original Eqn:
      None
        .
        .
        .
      None
    Units: See docs for percents_h_vehicles
    Limits: None
    Type: setup
    Subs: ['Households vehicles']

    Provides initial conditions for percents_h_vehicles function
    """
    return xrmerge(
        rearrange(
            1 - initial_2w_percent(),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            0, ["Households vehicles"], {"Households vehicles": ["elec 4wheels"]}
        ),
        rearrange(0, ["Households vehicles"], {"Households vehicles": ["hib 4wheels"]}),
        rearrange(0, ["Households vehicles"], {"Households vehicles": ["gas 4wheels"]}),
        rearrange(
            initial_2w_percent(),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            0, ["Households vehicles"], {"Households vehicles": ["elec 2wheels"]}
        ),
    )


@subs(["Households vehicles"], _subscript_dict)
def _integ_input_percents_h_vehicles():
    """
    Real Name: Implicit
    Original Eqn:
      None
        .
        .
        .
      None
    Units: See docs for percents_h_vehicles
    Limits: None
    Type: component
    Subs: ['Households vehicles']

    Provides derivative for percents_h_vehicles function
    """
    return xrmerge(
        rearrange(
            float(var_percents_h_vehicles().loc["liq 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["liq 4wheels"]},
        ),
        rearrange(
            float(var_percents_h_vehicles().loc["elec 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["elec 4wheels"]},
        ),
        rearrange(
            float(var_percents_h_vehicles().loc["hib 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["hib 4wheels"]},
        ),
        rearrange(
            float(var_percents_h_vehicles().loc["gas 4wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["gas 4wheels"]},
        ),
        rearrange(
            float(var_percents_h_vehicles().loc["liq 2wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["liq 2wheels"]},
        ),
        rearrange(
            float(var_percents_h_vehicles().loc["elec 2wheels"]),
            ["Households vehicles"],
            {"Households vehicles": ["elec 2wheels"]},
        ),
    )


_integ_percents_h_vehicles = Integ(
    _integ_input_percents_h_vehicles,
    _integ_init_percents_h_vehicles,
    "_integ_percents_h_vehicles",
)


_ext_constant_saving_ratio_2we = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratio_2wE",
    {},
    _root,
    "_ext_constant_saving_ratio_2we",
)


_ext_constant_t_fin_h_veh = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tfin_H_veh",
    {},
    _root,
    "_ext_constant_t_fin_h_veh",
)


_ext_constant_t_ini_h_veh = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tini_H_veh",
    {},
    _root,
    "_ext_constant_t_ini_h_veh",
)
