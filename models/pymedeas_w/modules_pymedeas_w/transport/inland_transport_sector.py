"""
Module inland_transport_sector
Translated using PySD version 2.2.1
"""


def activate_policy_inlandt():
    """
    Real Name: Activate policy inlandT
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'activate_policy_inland_trans')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1 to set growth of alternative inland transportation, starting in T ini
        and ending in T fin with the desired share defined in policies, linear
        growth
    """
    return _ext_constant_activate_policy_inlandt()


@subs(["vehicleT"], _subscript_dict)
def adapt_var_inlandt():
    """
    Real Name: adapt var inlandT
    Original Eqn: IF THEN ELSE(Time<T fin inlandT, IF THEN ELSE( Activate policy inlandT=1 :AND:Time>T ini inlandT, (P inlandT[vehicleT]-initial percent T vehicles[vehicleT] )/(T fin inlandT-T ini inlandT), hist var inlandT[vehicleT]), 0)*Efects shortage inlandT[vehicleT]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Growth of percent of vehicles adapted to saturation and shorgate of energy
    """
    return (
        if_then_else(
            time() < t_fin_inlandt(),
            lambda: if_then_else(
                logical_and(activate_policy_inlandt() == 1, time() > t_ini_inlandt()),
                lambda: (p_inlandt() - initial_percent_t_vehicles())
                / (t_fin_inlandt() - t_ini_inlandt()),
                lambda: hist_var_inlandt(),
            ),
            lambda: 0,
        )
        * efects_shortage_inlandt()
    )


def adjust_energy_for_transport_to_inland_transport():
    """
    Real Name: adjust energy for transport to inland transport
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'World', 'adjust_energy_for_transport_to_inland_transport')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    'International Energy Agency (2016), Energy Technology Perspectives 2016,
        OECD/IEA, considers in 2015 about 34 EJ of liquids for commercial
        transport. However WIOD database considers to inland transport sector
        about 12 EJ. Provisionally, we adjust OECD/IEA data to WIOD. We consider
        OECD/IEA data in relative terms.
    """
    return _ext_constant_adjust_energy_for_transport_to_inland_transport()


@subs(["vehicleT"], _subscript_dict)
def efects_shortage_inlandt():
    """
    Real Name: Efects shortage inlandT
    Original Eqn:
      1
        .
        .
        .
      1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    Efects of shortage of alternative fuels
    """
    return xrmerge(
        xr.DataArray(1, {"vehicleT": ["HV liq"]}, ["vehicleT"]),
        xr.DataArray(1, {"vehicleT": ["HV hib"]}, ["vehicleT"]),
        rearrange(effects_shortage_gas(), ["vehicleT"], {"vehicleT": ["HV gas"]}),
        xr.DataArray(1, {"vehicleT": ["LV liq"]}, ["vehicleT"]),
        rearrange(
            effects_shortage_elec_on_ev(), ["vehicleT"], {"vehicleT": ["LV elec"]}
        ),
        rearrange(effects_shortage_gas(), ["vehicleT"], {"vehicleT": ["LV gas"]}),
        xr.DataArray(1, {"vehicleT": ["bus liq"]}, ["vehicleT"]),
        rearrange(
            effects_shortage_elec_on_ev(), ["vehicleT"], {"vehicleT": ["bus elec"]}
        ),
        xr.DataArray(1, {"vehicleT": ["bus hib"]}, ["vehicleT"]),
        rearrange(effects_shortage_gas(), ["vehicleT"], {"vehicleT": ["bus gas"]}),
        xr.DataArray(1, {"vehicleT": ["train liq"]}, ["vehicleT"]),
        rearrange(
            effects_shortage_elec_on_ev(), ["vehicleT"], {"vehicleT": ["train elec"]}
        ),
        xr.DataArray(1, {"vehicleT": ["LV hib"]}, ["vehicleT"]),
    )


def effects_shortage_gas():
    """
    Real Name: effects shortage gas
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


@subs(["vehicleT"], _subscript_dict)
def energy_initial_inland_transport():
    """
    Real Name: Energy initial inland transport
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'energy_initial_inland_transport*')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    Initial energy consumed by the inland transport sector, before politics, TpolicyT
        (default 2015)        data 'International Energy Agency (2016), Energy Technology Perspectives
        2016, OECD/IEA,
    """
    return _ext_constant_energy_initial_inland_transport()


@subs(["vehicleT"], _subscript_dict)
def energy_per_x_t():
    """
    Real Name: energy per X t
    Original Eqn:
      liquids per X HV*saving ratios vehicles[HV liq]
        .
        .
        .
      liquids per X bus*saving ratios vehicles[bus elec]
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Energy per T$ of economic activity of inland transport sector. TODO
    """
    return xrmerge(
        rearrange(
            liquids_per_x_hv() * float(saving_ratios_vehicles().loc["HV liq"]),
            ["vehicleT"],
            {"vehicleT": ["HV liq"]},
        ),
        rearrange(
            liquids_per_x_hv() * float(saving_ratios_vehicles().loc["HV hib"]),
            ["vehicleT"],
            {"vehicleT": ["HV hib"]},
        ),
        rearrange(
            liquids_per_x_hv() * float(saving_ratios_vehicles().loc["HV gas"]),
            ["vehicleT"],
            {"vehicleT": ["HV gas"]},
        ),
        rearrange(
            liquids_per_x_lv() * float(saving_ratios_vehicles().loc["LV liq"]),
            ["vehicleT"],
            {"vehicleT": ["LV liq"]},
        ),
        rearrange(
            liquids_per_x_lv() * float(saving_ratios_vehicles().loc["LV elec"]),
            ["vehicleT"],
            {"vehicleT": ["LV elec"]},
        ),
        rearrange(
            liquids_per_x_lv() * float(saving_ratios_vehicles().loc["LV hib"]),
            ["vehicleT"],
            {"vehicleT": ["LV hib"]},
        ),
        rearrange(
            liquids_per_x_lv() * float(saving_ratios_vehicles().loc["LV gas"]),
            ["vehicleT"],
            {"vehicleT": ["LV gas"]},
        ),
        rearrange(
            liquids_per_x_bus() * float(saving_ratios_vehicles().loc["bus liq"]),
            ["vehicleT"],
            {"vehicleT": ["bus liq"]},
        ),
        rearrange(
            liquids_per_x_bus() * float(saving_ratios_vehicles().loc["bus hib"]),
            ["vehicleT"],
            {"vehicleT": ["bus hib"]},
        ),
        rearrange(
            liquids_per_x_bus() * float(saving_ratios_vehicles().loc["bus gas"]),
            ["vehicleT"],
            {"vehicleT": ["bus gas"]},
        ),
        rearrange(
            energy_per_x_train() * 0.8, ["vehicleT"], {"vehicleT": ["train liq"]}
        ),
        rearrange(
            energy_per_x_train() * 0.2, ["vehicleT"], {"vehicleT": ["train elec"]}
        ),
        rearrange(
            liquids_per_x_bus() * float(saving_ratios_vehicles().loc["bus elec"]),
            ["vehicleT"],
            {"vehicleT": ["bus elec"]},
        ),
    )


def energy_per_x_train():
    """
    Real Name: energy per X train
    Original Eqn: Energy initial inland transport[train liq]*adjust energy for transport to inland transport/initial Xt inland
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    EJ/T$economic activity  Average consumption of vehicles from historical data= energy
        used in that kind of transport/ economic activity of the sector        In the case of trains the number of vehicles is set to 1 since there are
        no data of the number of trains
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
    Original Eqn: 0
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    Historical growth of alternative percentages of transport vehicles. For
        inland transport vehicles the initial percentages of vehicles are
        neglictible in 2015.
    """
    return xr.DataArray(0, {"vehicleT": _subscript_dict["vehicleT"]}, ["vehicleT"])


@subs(["vehicleT"], _subscript_dict)
def initial_percent_t_vehicles():
    """
    Real Name: initial percent T vehicles
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_percent_T_vehicles*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    Initial percentage of vehicles of each fuel, percents relative to each
        class of vehicles (LV; HV, bus, train)
    """
    return _ext_constant_initial_percent_t_vehicles()


@subs(["vehicleT"], _subscript_dict)
def initial_vehicles_inland():
    """
    Real Name: initial vehicles inland
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_vehicles_inland*')
    Units: vehicle
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    Initial number of vehicles in time TpolicyT, 2015 by default, vehicles         'International Energy Agency (2016), Energy Technology Perspectives 2016, OECD/IEA,
        Paris'        No data for train vehicles
    """
    return _ext_constant_initial_vehicles_inland()


def initial_xt_inland():
    """
    Real Name: initial Xt inland
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'World', 'initial_Xt_inland')
    Units: T$
    Limits: (None, None)
    Type: constant
    Subs: None

    Economic activity of inland transport sector in the year of start of
        policies (2015 default) T$
    """
    return _ext_constant_initial_xt_inland()


@subs(["sectors"], _subscript_dict)
def inland_transport_fraction():
    """
    Real Name: inland transport fraction
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Global', 'inland_transport_fraction')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Fraction of the sectors that represent the inland transport output.
    """
    return _ext_constant_inland_transport_fraction()


@subs(["final sources"], _subscript_dict)
def inland_transport_variation_intensity():
    """
    Real Name: inland transport variation intensity
    Original Eqn:
      var I inland Elec
      0
      var I inlandT liq
      0
      var I inlandT Gas
    Units: EJ/TS/yr
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Variation of the energy intensity of inland transport
    """
    return xrmerge(
        rearrange(
            var_i_inland_elec(), ["final sources"], {"final sources": ["electricity"]}
        ),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
        rearrange(
            var_i_inlandt_liq(), ["final sources"], {"final sources": ["liquids"]}
        ),
        xr.DataArray(0, {"final sources": ["solids"]}, ["final sources"]),
        rearrange(var_i_inlandt_gas(), ["final sources"], {"final sources": ["gases"]}),
    )


def liquids_per_x_bus():
    """
    Real Name: liquids per X bus
    Original Eqn: Energy initial inland transport[bus liq]*adjust energy for transport to inland transport/initial Xt inland
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    EJ/T$economic activity  Average consumption of vehicles from historical data= energy
        used in that kind of transport/ economic activity of the sector        data 'International Energy Agency (2016), Energy Technology Perspectives 2016,
        OECD/IEA,data data 'International Energy Agency (2016), Energy Technology
        Perspectives 2016, OECD/IEA,   for energy        number of buses from
        http://www.theicct.org/global-transportation-roadmap-model
    """
    return (
        float(energy_initial_inland_transport().loc["bus liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def liquids_per_x_hv():
    """
    Real Name: liquids per X HV
    Original Eqn: Energy initial inland transport[HV liq]*adjust energy for transport to inland transport/initial Xt inland
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    EJ/T$economic activity  Average consumption of vehicles from historical data= energy
        used in that kind of transport/ economic activity of the sector        data 'International Energy Agency (2016), Energy Technology Perspectives
        2016, OECD/IEA,
    """
    return (
        float(energy_initial_inland_transport().loc["HV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def liquids_per_x_lv():
    """
    Real Name: liquids per X LV
    Original Eqn: Energy initial inland transport[LV liq]*adjust energy for transport to inland transport/initial Xt inland
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    EJ/T$economic activity  Average consumption of vehicles from historical data= energy
        used in that kind of transport/ economic activity of the sector        data 'International Energy Agency (2016), Energy Technology Perspectives
        2016, OECD/IEA,data
    """
    return (
        float(energy_initial_inland_transport().loc["LV liq"])
        * adjust_energy_for_transport_to_inland_transport()
        / initial_xt_inland()
    )


def nx_bus_inlandt():
    """
    Real Name: NX bus inlandT
    Original Eqn: (initial vehicles inland[bus liq]+initial vehicles inland[bus hib]+initial vehicles inland[bus gas]+initial vehicles inland[bus elec])/initial Xt inland
    Units: Mvehicles/Mdollar
    Limits: (None, None)
    Type: component
    Subs: None

    number of vehicles per unit of economic activity (e6 dollars) initial
        values in the year of initial policy (default 2015)
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
    Original Eqn: (initial vehicles inland[HV liq]+initial vehicles inland[HV hib]+initial vehicles inland[HV gas])/initial Xt inland
    Units: vehicles/T$
    Limits: (None, None)
    Type: component
    Subs: None

    number of vehicles per unit of economic activity (e12 dollars) initial
        values in the year of initial policy (default 2015)
    """
    return (
        float(initial_vehicles_inland().loc["HV liq"])
        + float(initial_vehicles_inland().loc["HV hib"])
        + float(initial_vehicles_inland().loc["HV gas"])
    ) / initial_xt_inland()


def nx_lv_inland_t():
    """
    Real Name: NX LV inland T
    Original Eqn: (initial vehicles inland[LV liq]+initial vehicles inland[LV elec]+initial vehicles inland[LV hib]+initial vehicles inland[LV gas])/initial Xt inland
    Units: vehicles/Tdollar
    Limits: (None, None)
    Type: component
    Subs: None

    number of vehicles per unit of economic activity (Tdollars) initial values
        in the year of initial policy (default 2015)
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
    Original Eqn: 1/initial Xt inland
    Units: vehicles/Tdollar
    Limits: (None, None)
    Type: component
    Subs: None

    no number of trains found in data, assume the number of trains is 1
    """
    return 1 / initial_xt_inland()


@subs(["vehicleT"], _subscript_dict)
def nx0_vehicles_per_xinland_t():
    """
    Real Name: NX0 vehicles per Xinland T
    Original Eqn:
      NX HV inland T
        .
        .
        .
      NX bus inlandT
    Units: vehicles/T$
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Estimated number of vehicles per unit of inland transport economic activity
    """
    return xrmerge(
        rearrange(nx_hv_inland_t(), ["vehicleT"], {"vehicleT": ["HV liq"]}),
        rearrange(nx_hv_inland_t(), ["vehicleT"], {"vehicleT": ["HV hib"]}),
        rearrange(nx_hv_inland_t(), ["vehicleT"], {"vehicleT": ["HV gas"]}),
        rearrange(nx_lv_inland_t(), ["vehicleT"], {"vehicleT": ["LV liq"]}),
        rearrange(nx_lv_inland_t(), ["vehicleT"], {"vehicleT": ["LV elec"]}),
        rearrange(nx_lv_inland_t(), ["vehicleT"], {"vehicleT": ["LV hib"]}),
        rearrange(nx_lv_inland_t(), ["vehicleT"], {"vehicleT": ["LV gas"]}),
        rearrange(nx_bus_inlandt(), ["vehicleT"], {"vehicleT": ["bus liq"]}),
        rearrange(nx_bus_inlandt(), ["vehicleT"], {"vehicleT": ["bus hib"]}),
        rearrange(nx_bus_inlandt(), ["vehicleT"], {"vehicleT": ["bus gas"]}),
        rearrange(nx_train_inland_t(), ["vehicleT"], {"vehicleT": ["train liq"]}),
        rearrange(nx_train_inland_t(), ["vehicleT"], {"vehicleT": ["train elec"]}),
        rearrange(nx_bus_inlandt(), ["vehicleT"], {"vehicleT": ["bus elec"]}),
    )


def p_bus_elec():
    """
    Real Name: P bus elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_electric_bus_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of bus. Desired percent of bus electric in T fin relative
        to the total bus
    """
    return _ext_constant_p_bus_elec()


def p_bus_gas():
    """
    Real Name: P bus gas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_gas_bus_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of bus. Desired percent of bus gas in T fin relative to
        the total  bus
    """
    return _ext_constant_p_bus_gas()


def p_bus_hyb():
    """
    Real Name: P bus hyb
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_hibrid_bus_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of bus. Desired percent of bus hibrid in T fin relative
        to the total of bus
    """
    return _ext_constant_p_bus_hyb()


def p_hv_gas():
    """
    Real Name: P HV gas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_gas_HV_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of heavy vehicles. Desired percent of HV gas in T fin
        relative to total Heavy Vehicles
    """
    return _ext_constant_p_hv_gas()


def p_hv_hyb():
    """
    Real Name: P HV hyb
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_hybrid_HV_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of heavy vehicles. Desired percent of HV hibrid in T fin
        relative to total Heavy Vehicles
    """
    return _ext_constant_p_hv_hyb()


@subs(["vehicleT"], _subscript_dict)
def p_inlandt():
    """
    Real Name: P inlandT
    Original Eqn:
      -P HV gas-P HV hyb
        .
        .
        .
      P LV hyb
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Desired percent each type of inland transport vehicle in T fin, Liquids
        policies are obtained by substracting the rest of vehicles, the sum of all
        policies must be 1 for each type of vehicle (HV, LV, bus, train).
    """
    return xrmerge(
        rearrange(-p_hv_gas() - p_hv_hyb(), ["vehicleT"], {"vehicleT": ["HV liq"]}),
        rearrange(p_hv_hyb(), ["vehicleT"], {"vehicleT": ["HV hib"]}),
        rearrange(p_hv_gas(), ["vehicleT"], {"vehicleT": ["HV gas"]}),
        rearrange(
            -p_lv_elec() - p_lv_hyb() - p_lv_gas(),
            ["vehicleT"],
            {"vehicleT": ["LV liq"]},
        ),
        rearrange(p_lv_elec(), ["vehicleT"], {"vehicleT": ["LV elec"]}),
        rearrange(p_lv_gas(), ["vehicleT"], {"vehicleT": ["LV gas"]}),
        rearrange(
            -p_bus_hyb() - p_bus_gas() - p_bus_elec(),
            ["vehicleT"],
            {"vehicleT": ["bus liq"]},
        ),
        rearrange(p_bus_elec(), ["vehicleT"], {"vehicleT": ["bus elec"]}),
        rearrange(p_bus_hyb(), ["vehicleT"], {"vehicleT": ["bus hib"]}),
        rearrange(p_bus_gas(), ["vehicleT"], {"vehicleT": ["bus gas"]}),
        rearrange(-p_train_elec(), ["vehicleT"], {"vehicleT": ["train liq"]}),
        rearrange(p_train_elec(), ["vehicleT"], {"vehicleT": ["train elec"]}),
        rearrange(p_lv_hyb(), ["vehicleT"], {"vehicleT": ["LV hib"]}),
    )


def p_lv_elec():
    """
    Real Name: P LV elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_electric_LV_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of light cargo vehicles. Percent of LV electric in T fin
        relative to the total of Light Vehicles
    """
    return _ext_constant_p_lv_elec()


def p_lv_gas():
    """
    Real Name: P LV gas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_gas_LV_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of light cargo vehicles. Desired percent of LV gas in T
        fin relative to the total Light Vehicles
    """
    return _ext_constant_p_lv_gas()


def p_lv_hyb():
    """
    Real Name: P LV hyb
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_hybrid_LV_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of light cargo vehicles. Desired percent of LV hibrid in
        T fin relative to the total Light Vehicles
    """
    return _ext_constant_p_lv_hyb()


def p_train_elec():
    """
    Real Name: P train elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'policy_electric_train_tfin')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy of change of trains. Desired percent of train electric in T fin
        relative to the total of trains
    """
    return _ext_constant_p_train_elec()


@subs(["vehicleT"], _subscript_dict)
def percent_t_vehicles():
    """
    Real Name: percent T vehicles
    Original Eqn: INTEG ( var percent T vehicles[vehicleT], initial percent T vehicles[vehicleT])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Percents of inland transport vehicles, each type relative to its own:
        heavy vehicles (%liq+%hib+%gas) add 1, light vehicles
        (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains
        ((%liq+%elec) add 1.
    """
    return _integ_percent_t_vehicles()


def real_total_output_inland_transport():
    """
    Real Name: Real total output inland transport
    Original Eqn: SUM(Real total output by sector[sectors!]*inland transport fraction[sectors!])/1e+06
    Units: T$
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        sum(
            real_total_output_by_sector() * inland_transport_fraction(),
            dim=("sectors",),
        )
        / 1e06
    )


@subs(["vehicleT"], _subscript_dict)
def saving_ratios_vehicles():
    """
    Real Name: saving ratios vehicles
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'saving_ratios_vehicles*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['vehicleT']

    ratios of energy consumption of diferente vehicles per Km compared to
        conventional  liquids vechicles
    """
    return _ext_constant_saving_ratios_vehicles()


@subs(["vehicleT"], _subscript_dict)
def shares_available_t():
    """
    Real Name: shares available T
    Original Eqn:
      1-(percent T vehicles[HV hib]+percent T vehicles[HV gas])
        .
        .
        .
      1-percent T vehicles[train elec]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Share of the total percent of each type of vehicle available for growth,
        is the same for each type of vehicle. When it approaches zero the growth
        of all of them stops
    """
    return xrmerge(
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["HV hib"])
                + float(percent_t_vehicles().loc["HV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["HV liq"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["HV hib"])
                + float(percent_t_vehicles().loc["HV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["HV hib"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["HV hib"])
                + float(percent_t_vehicles().loc["HV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["HV gas"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["LV elec"])
                + float(percent_t_vehicles().loc["LV hib"])
                + float(percent_t_vehicles().loc["LV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["LV liq"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["LV elec"])
                + float(percent_t_vehicles().loc["LV hib"])
                + float(percent_t_vehicles().loc["LV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["LV elec"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["LV elec"])
                + float(percent_t_vehicles().loc["LV hib"])
                + float(percent_t_vehicles().loc["LV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["LV gas"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["LV elec"])
                + float(percent_t_vehicles().loc["LV hib"])
                + float(percent_t_vehicles().loc["LV gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["LV hib"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["bus elec"])
                + float(percent_t_vehicles().loc["bus hib"])
                + float(percent_t_vehicles().loc["bus gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["bus liq"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["bus elec"])
                + float(percent_t_vehicles().loc["bus hib"])
                + float(percent_t_vehicles().loc["bus gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["bus elec"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["bus elec"])
                + float(percent_t_vehicles().loc["bus hib"])
                + float(percent_t_vehicles().loc["bus gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["bus hib"]},
        ),
        rearrange(
            1
            - (
                float(percent_t_vehicles().loc["bus elec"])
                + float(percent_t_vehicles().loc["bus hib"])
                + float(percent_t_vehicles().loc["bus gas"])
            ),
            ["vehicleT"],
            {"vehicleT": ["bus gas"]},
        ),
        rearrange(
            1 - float(percent_t_vehicles().loc["train elec"]),
            ["vehicleT"],
            {"vehicleT": ["train liq"]},
        ),
        rearrange(
            1 - float(percent_t_vehicles().loc["train elec"]),
            ["vehicleT"],
            {"vehicleT": ["train elec"]},
        ),
    )


def t_fin_inlandt():
    """
    Real Name: T fin inlandT
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'tfin_H_inlandT')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    Time of begining of inland transport policies
    """
    return _ext_constant_t_fin_inlandt()


def t_ini_inlandt():
    """
    Real Name: T ini inlandT
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'tini_inlandT_veh')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    By this time the policy objectives defined in policies must be obtained
    """
    return _ext_constant_t_ini_inlandt()


def var_i_inland_elec():
    """
    Real Name: var I inland Elec
    Original Eqn: energy per X t[LV elec]*var percent T vehicles[LV elec]+energy per X t[train elec]*var percent T vehicles[train elec]+energy per X t[ bus elec]*var percent T vehicles[bus elec]
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of the energy intensity of inland transport relative to
        electricity and due to the variations of electricity based vehicles
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
    Original Eqn: energy per X t[HV gas]*var percent T vehicles[HV gas]+energy per X t[bus gas]*var percent T vehicles[bus gas]+energy per X t[ LV gas]*var percent T vehicles[LV gas]
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of the energy intensity of inland transport relative to gas and
        due to the variations of gas based vehicles
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
    Original Eqn: energy per X t[HV liq]*var percent T vehicles[HV liq]+energy per X t[LV liq]*var percent T vehicles[LV liq]+energy per X t[ bus liq]*var percent T vehicles[bus liq]+energy per X t[HV liq]*var percent T vehicles[HV hib]+energy per X t[LV liq]*var percent T vehicles[LV hib]+energy per X t[bus liq]*var percent T vehicles[ bus hib]+ energy per X t[train liq]*var percent T vehicles[train liq]
    Units: EJ/T$/yr
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of the energy intensity of inland transport relative to liquids
        and due to the variations of liquids based vehicles
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
      -adapt var inlandT[HV hib]-adapt var inlandT[HV gas]
        .
        .
        .
      adapt var inlandT[bus elec]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    growth of percents of inland transport vehicles, each type relative to its own:
        heavy vehicles (%liq+%hib+%gas) add 1, light vehicles
        (%liq+%elec+%gas+%hib) add 1, bus (%liq+%elec+%gas+%hib) add 1 and trains
        ((%liq+%elec) add 1.        The growth of liquids allways adapts to the one of the rest, we assume
        that the policies are passing from liquids to other fuels
    """
    return xrmerge(
        rearrange(
            -float(adapt_var_inlandt().loc["HV hib"])
            - float(adapt_var_inlandt().loc["HV gas"]),
            ["vehicleT"],
            {"vehicleT": ["HV liq"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["HV hib"]),
            ["vehicleT"],
            {"vehicleT": ["HV hib"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["HV gas"]),
            ["vehicleT"],
            {"vehicleT": ["HV gas"]},
        ),
        rearrange(
            -float(adapt_var_inlandt().loc["LV hib"])
            - float(adapt_var_inlandt().loc["LV elec"])
            - float(adapt_var_inlandt().loc["LV gas"]),
            ["vehicleT"],
            {"vehicleT": ["LV liq"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["LV elec"]),
            ["vehicleT"],
            {"vehicleT": ["LV elec"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["LV hib"]),
            ["vehicleT"],
            {"vehicleT": ["LV hib"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["LV gas"]),
            ["vehicleT"],
            {"vehicleT": ["LV gas"]},
        ),
        rearrange(
            -float(adapt_var_inlandt().loc["bus elec"])
            - float(adapt_var_inlandt().loc["bus hib"])
            - float(adapt_var_inlandt().loc["bus gas"]),
            ["vehicleT"],
            {"vehicleT": ["bus liq"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["bus hib"]),
            ["vehicleT"],
            {"vehicleT": ["bus hib"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["bus gas"]),
            ["vehicleT"],
            {"vehicleT": ["bus gas"]},
        ),
        rearrange(
            -float(adapt_var_inlandt().loc["train elec"]),
            ["vehicleT"],
            {"vehicleT": ["train liq"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["train elec"]),
            ["vehicleT"],
            {"vehicleT": ["train elec"]},
        ),
        rearrange(
            float(adapt_var_inlandt().loc["bus elec"]),
            ["vehicleT"],
            {"vehicleT": ["bus elec"]},
        ),
    )


@subs(["vehicleT"], _subscript_dict)
def vehicles_inlandt():
    """
    Real Name: vehicles inlandT
    Original Eqn: percent T vehicles[vehicleT]*Real total output inland transport*NX0 vehicles per Xinland T[vehicleT]
    Units: vehicles
    Limits: (None, None)
    Type: component
    Subs: ['vehicleT']

    Estimation of the number of vehicles of inland transport sector by types,
        based on a constant ratio number ob vehicles per economic activity of the
        inland transport sector
    """
    return (
        percent_t_vehicles()
        * real_total_output_inland_transport()
        * nx0_vehicles_per_xinland_t()
    )


_ext_constant_activate_policy_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "activate_policy_inland_trans",
    {},
    _root,
    "_ext_constant_activate_policy_inlandt",
)


_ext_constant_adjust_energy_for_transport_to_inland_transport = ExtConstant(
    "../energy.xlsx",
    "World",
    "adjust_energy_for_transport_to_inland_transport",
    {},
    _root,
    "_ext_constant_adjust_energy_for_transport_to_inland_transport",
)


_ext_constant_energy_initial_inland_transport = ExtConstant(
    "../transport.xlsx",
    "World",
    "energy_initial_inland_transport*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_energy_initial_inland_transport",
)


_ext_constant_initial_percent_t_vehicles = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_percent_T_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_initial_percent_t_vehicles",
)


_ext_constant_initial_vehicles_inland = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_vehicles_inland*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_initial_vehicles_inland",
)


_ext_constant_initial_xt_inland = ExtConstant(
    "../transport.xlsx",
    "World",
    "initial_Xt_inland",
    {},
    _root,
    "_ext_constant_initial_xt_inland",
)


_ext_constant_inland_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "inland_transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_inland_transport_fraction",
)


_ext_constant_p_bus_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_elec",
)


_ext_constant_p_bus_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_gas",
)


_ext_constant_p_bus_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hibrid_bus_tfin",
    {},
    _root,
    "_ext_constant_p_bus_hyb",
)


_ext_constant_p_hv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_HV_tfin",
    {},
    _root,
    "_ext_constant_p_hv_gas",
)


_ext_constant_p_hv_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_HV_tfin",
    {},
    _root,
    "_ext_constant_p_hv_hyb",
)


_ext_constant_p_lv_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_elec",
)


_ext_constant_p_lv_gas = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_gas_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_gas",
)


_ext_constant_p_lv_hyb = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_hybrid_LV_tfin",
    {},
    _root,
    "_ext_constant_p_lv_hyb",
)


_ext_constant_p_train_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "policy_electric_train_tfin",
    {},
    _root,
    "_ext_constant_p_train_elec",
)


@subs(["vehicleT"], _subscript_dict)
def _integ_init_percent_t_vehicles():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for percent_t_vehicles
    Limits: None
    Type: setup
    Subs: ['vehicleT']

    Provides initial conditions for percent_t_vehicles function
    """
    return initial_percent_t_vehicles()


@subs(["vehicleT"], _subscript_dict)
def _integ_input_percent_t_vehicles():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for percent_t_vehicles
    Limits: None
    Type: component
    Subs: ['vehicleT']

    Provides derivative for percent_t_vehicles function
    """
    return var_percent_t_vehicles()


_integ_percent_t_vehicles = Integ(
    _integ_input_percent_t_vehicles,
    _integ_init_percent_t_vehicles,
    "_integ_percent_t_vehicles",
)


_ext_constant_saving_ratios_vehicles = ExtConstant(
    "../transport.xlsx",
    "Global",
    "saving_ratios_vehicles*",
    {"vehicleT": _subscript_dict["vehicleT"]},
    _root,
    "_ext_constant_saving_ratios_vehicles",
)


_ext_constant_t_fin_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tfin_H_inlandT",
    {},
    _root,
    "_ext_constant_t_fin_inlandt",
)


_ext_constant_t_ini_inlandt = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "tini_inlandT_veh",
    {},
    _root,
    "_ext_constant_t_ini_inlandt",
)
