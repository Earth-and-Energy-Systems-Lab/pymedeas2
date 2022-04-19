"""
Module transport_electric_batteries
Translated using PySD version 3.0.0
"""


@component.add(
    name="bat number 2w",
    units="batteries",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def bat_number_2w():
    """
    Required number of electric batteries for 2w vehicles expressed in terms of a stantad a 21,3KWh battery, but taking into account the smaller size of 2 wheeler's batteries
    """
    return float(number_vehicles_h().loc["elec 2wheels"]) * bateries_ratio_2w_e()


@component.add(
    name="bat number EV",
    units="batteries",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def bat_number_ev():
    """
    Required number of electric batteries for hybrid vehicles expressed in terms of a stantad a 21,3KWh battery,
    """
    return (
        float(number_vehicles_h().loc["elec 4wheels"])
        + float(vehicles_inlandt().loc["LV elec"])
        + float(vehicles_inlandt().loc["bus elec"]) * bateries_ratio_bus_e()
    )


@component.add(
    name="bat number hyb",
    units="batteries",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def bat_number_hyb():
    """
    Required number of electric batteries for hybrid vehicles expressed in terms of a stantad a 21,3KWh battery, but taking into account the greater size of heavy vehicle's batteries and the smaller one of hybrid ligh vehicles
    """
    return (
        float(vehicles_inlandt().loc["LV hib"]) * bateries_ratio_hib_lv()
        + float(vehicles_inlandt().loc["HV hib"]) * bateries_ratio_hib_hv()
        + float(vehicles_inlandt().loc["bus hib"]) * bateries_ratio_hib_bus()
        + float(number_vehicles_h().loc["hib 4wheels"]) * bateries_ratio_hib_lv()
    )


@component.add(
    name="bateries ratio 2w E", comp_type="Constant", comp_subtype="External"
)
def bateries_ratio_2w_e():
    """
    Ratio between the size of the electric 2 wheeler batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_2w_e()


_ext_constant_bateries_ratio_2w_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_2w_E",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_2w_e",
)


@component.add(
    name="bateries ratio bus E",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def bateries_ratio_bus_e():
    """
    Ratio between the size of the electric bus batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_bus_e()


_ext_constant_bateries_ratio_bus_e = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_bus_E",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_bus_e",
)


@component.add(
    name="bateries ratio hib bus",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def bateries_ratio_hib_bus():
    """
    Ratio between the size of the hybrid bus batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_bus()


_ext_constant_bateries_ratio_hib_bus = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_bus",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_hib_bus",
)


@component.add(
    name="bateries ratio hib HV",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def bateries_ratio_hib_hv():
    """
    Ratio between the size of the hybrid HV batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_hv()


_ext_constant_bateries_ratio_hib_hv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_hv",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_hib_hv",
)


@component.add(
    name="bateries ratio hib LV", comp_type="Constant", comp_subtype="External"
)
def bateries_ratio_hib_lv():
    """
    Ratio between the size of the electric LV hybrid batteries and the standard 21,3KWh batteries, per vehicle
    """
    return _ext_constant_bateries_ratio_hib_lv()


_ext_constant_bateries_ratio_hib_lv = ExtConstant(
    "../transport.xlsx",
    "Global",
    "bateries_ratio_hib_lv",
    {},
    _root,
    {},
    "_ext_constant_bateries_ratio_hib_lv",
)


@component.add(
    name='"batteries EV+hib+2wE"',
    units="batteries",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def batteries_evhib2we():
    """
    Number of batteries required for electric and hybrid mobility espreseed in termos of "standard" electric batteries of 21,3KWh
    """
    return _integ_batteries_evhib2we()


_integ_batteries_evhib2we = Integ(
    lambda: new_batteries() + replacement_batteries() - discarded_batteries(),
    lambda: 1,
    "_integ_batteries_evhib2we",
)


@component.add(
    name="discarded batteries",
    units="batteries",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def discarded_batteries():
    """
    Discarded electric batteries due to wear.
    """
    return np.maximum(0, zidz(batteries_evhib2we(), lifetime_ev_batteries()))


@component.add(
    name="EV batteries TW", units="TW", comp_type="Auxiliary", comp_subtype="Normal"
)
def ev_batteries_tw():
    """
    Electric batteries from electric vehicles, expresed in terms of power available (TW)
    """
    return batteries_evhib2we() * kw_per_battery_ev() / kwh_per_twh()


@component.add(
    name="kW per battery EV",
    units="kW/battery",
    comp_type="Constant",
    comp_subtype="External",
)
def kw_per_battery_ev():
    """
    Average kW per battery of electrical vehicle.
    """
    return _ext_constant_kw_per_battery_ev()


_ext_constant_kw_per_battery_ev = ExtConstant(
    "../energy.xlsx",
    "Global",
    "kw_per_battery_ev",
    {},
    _root,
    {},
    "_ext_constant_kw_per_battery_ev",
)


@component.add(
    name="new batteries",
    units="batteries/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_batteries():
    """
    New standard electric batteries. The number of batteries converges to the desired number via a logistic funcion. Number 10 is an arbitrary parameter, the bigger the faster the convergence to the desired number of batteries. 5*"batteries EV+hib+2wE"*(1-(MIN(1,"batteries EV+hib+2wE"/required number standard batteries)))
    """
    return required_number_standard_batteries() - batteries_evhib2we()


@component.add(
    name='"new+replaced batteries TW"',
    units="batteries/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def newreplaced_batteries_tw():
    """
    New and replaced electric batteries.
    """
    return (
        (new_batteries() + replacement_batteries())
        * kw_per_battery_ev()
        / kwh_per_twh()
    )


@component.add(
    name="replacement batteries",
    units="batteries/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_batteries():
    """
    Replacement of electric batteries.due to degradation of existing ones
    """
    return discarded_batteries()


@component.add(
    name="required number standard batteries",
    units="batteries",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def required_number_standard_batteries():
    """
    Required number of electric batteries taking as a stantad a 21,3KWh battery (average size of purely electric vehicle). The batteries of other vehicles are described in terms of this standard one using the batteries ratio coefficient, (relative to the size and amount of minerals). .
    """
    return bat_number_2w() + bat_number_ev() + bat_number_hyb() + 1
