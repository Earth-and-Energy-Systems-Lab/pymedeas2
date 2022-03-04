"""
Module transport_electric_batteries
Translated using PySD version 2.2.1
"""


def bat_number_2w():
    """
    Real Name: bat number 2w
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required number of electric batteries for 2w vehicles expressed in terms of a stantad a 21,3KWh battery, but taking into account the smaller size of 2 wheeler's batteries
    """
    return float(number_vehicles_h().loc["elec 2wheels"]) * bateries_ratio_2w_e()


def bat_number_ev():
    """
    Real Name: bat number EV
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required number of electric batteries for hybrid vehicles expressed in terms of a stantad a 21,3KWh battery,
    """
    return (
        float(number_vehicles_h().loc["elec 4wheels"])
        + float(vehicles_inlandt().loc["LV elec"])
        + float(vehicles_inlandt().loc["bus elec"]) * bateries_ratio_bus_e()
    )


def bat_number_hib():
    """
    Real Name: bat number hib
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required number of electric batteries for hybrid vehicles expressed in terms of a stantad a 21,3KWh battery, but taking into account the greater size of heavy vehicle's batteries and the smaller one of hybrid ligh vehicles
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
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Ratio between the size of the electric 2 wheeler batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_2w_e()


_ext_constant_bateries_ratio_2w_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_2w_E",
    {},
    _root,
    "_ext_constant_bateries_ratio_2w_e",
)


def bateries_ratio_bus_e():
    """
    Real Name: bateries ratio bus E
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Ratio between the size of the electric bus batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_bus_e()


_ext_constant_bateries_ratio_bus_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_bus_E",
    {},
    _root,
    "_ext_constant_bateries_ratio_bus_e",
)


def bateries_ratio_hib_bus():
    """
    Real Name: bateries ratio hib bus
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Ratio between the size of the hybrid bus batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_bus()


_ext_constant_bateries_ratio_hib_bus = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_bus",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_bus",
)


def bateries_ratio_hib_hv():
    """
    Real Name: bateries ratio hib HV
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Ratio between the size of the hybrid HV batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_hv()


_ext_constant_bateries_ratio_hib_hv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_hv",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_hv",
)


def bateries_ratio_hib_lv():
    """
    Real Name: bateries ratio hib LV
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Ratio between the size of the electric LV hybrid batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_lv()


_ext_constant_bateries_ratio_hib_lv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_lv",
    {},
    _root,
    "_ext_constant_bateries_ratio_hib_lv",
)


def batteries_evhib2we():
    """
    Real Name: "batteries EV+hib+2wE"
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Number of batteries required for electric and hybrid mobility espreseed in termos of "standard" electric batteries of 21,3KWh
    """
    return _integ_batteries_evhib2we()


_integ_batteries_evhib2we = Integ(
    lambda: new_batteries() + replacement_batteries() - discarded_batteries(),
    lambda: 1,
    "_integ_batteries_evhib2we",
)


def discarded_batteries():
    """
    Real Name: discarded batteries
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Discarded electric batteries due to wear.
    """
    return np.maximum(0, zidz(batteries_evhib2we(), lifetime_ev_batteries()))


def ev_batteries_tw():
    """
    Real Name: EV batteries TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electric batteries from electric vehicles, expresed in terms of power available (TW)
    """
    return batteries_evhib2we() * kw_per_battery_ev() / kwh_per_twh()


def kw_per_battery_ev():
    """
    Real Name: kW per battery EV
    Original Eqn:
    Units: kW/battery
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average kW per battery of electrical vehicle.
    """
    return _ext_constant_kw_per_battery_ev()


_ext_constant_kw_per_battery_ev = ExtConstant(
    "../energy.xlsx",
    "Global",
    "kw_per_battery_ev",
    {},
    _root,
    "_ext_constant_kw_per_battery_ev",
)


def new_batteries():
    """
    Real Name: new batteries
    Original Eqn:
    Units: batteries/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New standard electric batteries. The number of batteries converges to the desired number via a logistic funcion. Number 10 is an arbitrary parameter, the bigger the faster the convergence to the desired number of batteries. 5*"batteries EV+hib+2wE"*(1-(MIN(1,"batteries EV+hib+2wE"/required number standard batteries)))
    """
    return required_number_standard_batteries() - batteries_evhib2we()


def newreplaced_batteries_tw():
    """
    Real Name: "new+replaced batteries TW"
    Original Eqn:
    Units: batteries/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: batteries/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Replacement of electric batteries.due to degradation of existing ones
    """
    return discarded_batteries()


def required_number_standard_batteries():
    """
    Real Name: required number standard batteries
    Original Eqn:
    Units: batteries
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Required number of electric batteries taking as a stantad a 21,3KWh battery (average size of purely electric vehicle). The batteries of other vehicles are described in terms of this standard one using the batteries ratio coefficient, (relative to the size and amount of minerals). .
    """
    return bat_number_2w() + bat_number_ev() + bat_number_hib() + 1
