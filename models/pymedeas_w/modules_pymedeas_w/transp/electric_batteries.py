"""
Module electric_batteries
Translated using PySD version 2.1.0
"""


def bat_number_2w():
    """
    Real Name: bat number 2w
    Original Eqn: Number vehicles H[elec 2wheels]*bateries ratio 2w E
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Required number of  electric batteries for 2w vehicles expressed in terms
        of a stantad a 21,3KWh battery, but taking into account the smaller size
        of 2 wheeler's batteries
    """
    return float(number_vehicles_h().loc["elec 2wheels"]) * bateries_ratio_2w_e()


def bat_number_ev():
    """
    Real Name: bat number EV
    Original Eqn: Number vehicles H[elec 4wheels]+vehicles inlandT[LV elec]+vehicles inlandT[bus elec]*bateries ratio bus E
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Required number of  electric batteries for hybrid vehicles expressed in
        terms of a stantad a 21,3KWh battery,
    """
    return (
        float(number_vehicles_h().loc["elec 4wheels"])
        + float(vehicles_inlandt().loc["LV elec"])
        + float(vehicles_inlandt().loc["bus elec"]) * bateries_ratio_bus_e()
    )


def bat_number_hib():
    """
    Real Name: bat number hib
    Original Eqn: vehicles inlandT[LV hib]*bateries ratio hib LV+vehicles inlandT[HV hib]*bateries ratio hib HV+vehicles inlandT [bus hib]*bateries ratio hib bus+Number vehicles H[hib 4wheels]*bateries ratio hib LV
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Required number of  electric batteries for hybrid vehicles expressed in
        terms of a stantad a 21,3KWh battery, but taking into account the greater
        size of heavy vehicle's batteries and the smaller one of hybrid ligh
        vehicles
    """
    return (
        float(vehicles_inlandt().loc["LV hib"]) * bateries_ratio_hib_lv()
        + float(vehicles_inlandt().loc["HV hib"]) * bateries_ratio_hib_hv()
        + float(vehicles_inlandt().loc["bus hib"]) * bateries_ratio_hib_bus()
        + float(number_vehicles_h().loc["hib 4wheels"]) * bateries_ratio_hib_lv()
    )


def bateries_ratio_2w_e():
    """
    Real Name: bateries ratio 2w E
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'bateries_ratio_2w_E')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Ratio between the size of the electric 2 wheeler batteries and the
        standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_2w_e()


def bateries_ratio_bus_e():
    """
    Real Name: bateries ratio bus E
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'bateries_ratio_bus_E')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Ratio between the size of the electric bus batteries and the standard
        21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_bus_e()


def bateries_ratio_hib_bus():
    """
    Real Name: bateries ratio hib bus
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'bateries_ratio_hib_bus')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Ratio between the size of the hybrid bus batteries and the standard
        21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_bus()


def bateries_ratio_hib_hv():
    """
    Real Name: bateries ratio hib HV
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'bateries_ratio_hib_hv')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Ratio between the size of the hybrid HV batteries and the standard 21,3KWh
        batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_hv()


def bateries_ratio_hib_lv():
    """
    Real Name: bateries ratio hib LV
    Original Eqn: GET DIRECT CONSTANTS('../transport.xlsx', 'Global', 'bateries_ratio_hib_lv')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Ratio between the size of the electric LV hybrid batteries and the
        standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_lv()


def batteries_evhib2we():
    """
    Real Name: "batteries EV+hib+2wE"
    Original Eqn: INTEG ( new batteries+replacement batteries-discarded batteries , 1)
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Number of batteries required for electric and hybrid mobility espreseed in
        termos of "standard" electric batteries of 21,3KWh
    """
    return _integ_batteries_evhib2we()


def discarded_batteries():
    """
    Real Name: discarded batteries
    Original Eqn: MAX(0,ZIDZ( "batteries EV+hib+2wE", lifetime EV batteries ))
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Discarded electric batteries due to wear.
    """
    return np.maximum(0, zidz(batteries_evhib2we(), lifetime_ev_batteries()))


def ev_batteries_tw():
    """
    Real Name: EV batteries TW
    Original Eqn: "batteries EV+hib+2wE"*kW per battery EV/kWh per TWh
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Electric batteries from electric vehicles, expresed in terms of power
        available (TW)
    """
    return batteries_evhib2we() * kw_per_battery_ev() / kwh_per_twh()


def kw_per_battery_ev():
    """
    Real Name: kW per battery EV
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'kw_per_battery_ev')
    Units: kW/battery
    Limits: (None, None)
    Type: constant
    Subs: None

    Average kW per battery of electrical vehicle.
    """
    return _ext_constant_kw_per_battery_ev()


def new_batteries():
    """
    Real Name: new batteries
    Original Eqn: required number standard batteries-"batteries EV+hib+2wE"
    Units: batteries/year
    Limits: (None, None)
    Type: component
    Subs: None

    New standard electric batteries. The number of batteries converges to the
        desired number via a logistic funcion. Number 10 is an arbitrary
        parameter, the bigger the faster the convergence to the desired number of
        batteries.
    """
    return required_number_standard_batteries() - batteries_evhib2we()


def newreplaced_batteries_tw():
    """
    Real Name: "new+replaced batteries TW"
    Original Eqn: (new batteries+replacement batteries)*kW per battery EV/kWh per TWh
    Units: batteries/year
    Limits: (None, None)
    Type: component
    Subs: None

    New and replaced electric batteries.
    """
    return (
        (new_batteries() + replacement_batteries())
        * kw_per_battery_ev()
        / kwh_per_twh()
    )


def replacement_batteries():
    """
    Real Name: replacement batteries
    Original Eqn: discarded batteries
    Units: batteries/year
    Limits: (None, None)
    Type: component
    Subs: None

    Replacement of electric batteries.due to degradation of existing ones
    """
    return discarded_batteries()


def required_number_standard_batteries():
    """
    Real Name: required number standard batteries
    Original Eqn: bat number 2w+bat number EV+bat number hib+1
    Units: batteries
    Limits: (None, None)
    Type: component
    Subs: None

    Required number of  electric batteries taking as a stantad a 21,3KWh
        battery (average size of purely electric vehicle). The batteries of other
        vehicles are described in terms of this standard one using the batteries
        ratio coefficient, (relative to the size and amount of minerals). .
    """
    return bat_number_2w() + bat_number_ev() + bat_number_hib() + 1


_ext_constant_bateries_ratio_2w_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_2w_E",
    {},
    _root,
    "_ext_constant_bateries_ratio_2w_e",
)


_ext_constant_bateries_ratio_bus_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_bus_E",
    {},
    _root,
    "_ext_constant_bateries_ratio_bus_e",
)


_ext_constant_bateries_ratio_hib_bus = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_bus",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_bus",
)


_ext_constant_bateries_ratio_hib_hv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_hv",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_hv",
)


_ext_constant_bateries_ratio_hib_lv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_lv",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_lv",
)


_integ_batteries_evhib2we = Integ(
    lambda: new_batteries() + replacement_batteries() - discarded_batteries(),
    lambda: 1,
    "_integ_batteries_evhib2we",
)


_ext_constant_kw_per_battery_ev = ExtConstant(
    "../energy.xlsx",
    "Global",
    "kw_per_battery_ev",
    {},
    _root,
    "_ext_constant_kw_per_battery_ev",
)
