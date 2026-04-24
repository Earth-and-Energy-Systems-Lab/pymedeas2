"""
Module energy.storage.esoi_ev_batteries
Translated using PySD version 3.14.3
"""

@component.add(
    name="Cp_EV_batteries_for_Transp",
    units="Dmnl",
    subscripts=["battery_modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cp_ev_batteries_for_transp"},
)
def cp_ev_batteries_for_transp():
    return _ext_constant_cp_ev_batteries_for_transp()


_ext_constant_cp_ev_batteries_for_transp = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "cp_evs_transport*",
    {"battery_modes": _subscript_dict["battery_modes"]},
    _root,
    {"battery_modes": _subscript_dict["battery_modes"]},
    "_ext_constant_cp_ev_batteries_for_transp",
)


@component.add(
    name="cycles_over_lifetime",
    units="cycles_ev",
    subscripts=["EV_bat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cycles_over_lifetime"},
)
def cycles_over_lifetime():
    return _ext_constant_cycles_over_lifetime()


_ext_constant_cycles_over_lifetime = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "cicles_over_lifetime*",
    {"EV_bat": _subscript_dict["EV_bat"]},
    _root,
    {"EV_bat": _subscript_dict["EV_bat"]},
    "_ext_constant_cycles_over_lifetime",
)


@component.add(
    name='"Energy_intensity_construction_EV_batteries_MJ/MW"',
    units="MJ/MW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_energy_required_for_total_material_consumption_for_ev_batteries": 1,
        "mj_per_ej": 1,
        "mw_per_tw": 1,
        "newreplaced_batteries_tw": 1,
    },
)
def energy_intensity_construction_ev_batteries_mjmw():
    """
    Energy intensity of the construction of EV batteries. Dynamic variable affected by recycling policies.
    """
    return zidz(
        total_energy_required_for_total_material_consumption_for_ev_batteries()
        * mj_per_ej(),
        newreplaced_batteries_tw() * mw_per_tw(),
    )


@component.add(
    name="ESOI_EV_batteries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lifetime_ev_batteries": 1,
        "cp_ev_batteries_for_elec_storage": 1,
        "grid_correction_factor_ev_batteries": 1,
        "gquality_of_electricity": 1,
        "share_energy_requirements_for_decom_ev_batteries": 1,
        "mw_in_1_year_to_mj": 1,
        "energy_intensity_construction_ev_batteries_mjmw": 1,
    },
)
def esoi_ev_batteries():
    """
    ESOI batteries of electric vehicles for electricity storage. (To estimate the ESOI static: g=0.7 and constant recycling rates)
    """
    return (
        float(lifetime_ev_batteries().loc["LFP", "cars"])
        * cp_ev_batteries_for_elec_storage()
        * zidz(
            mw_in_1_year_to_mj(),
            (
                gquality_of_electricity()
                * energy_intensity_construction_ev_batteries_mjmw()
            )
            * (
                1
                + share_energy_requirements_for_decom_ev_batteries()
                + grid_correction_factor_ev_batteries()
            ),
        )
    )


@component.add(
    name="FEI_EV_batteries",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "output_ev_bateries_for_storage_over_lifetime": 1,
        "esoi_ev_batteries": 1,
    },
)
def fei_ev_batteries():
    """
    Final energy invested (equivalent to the denominator of the EROI (=CED*g).
    """
    return zidz(
        sum(
            output_ev_bateries_for_storage_over_lifetime().rename(
                {"EV_bat": "EV_bat!", "battery_modes": "battery_modes!"}
            ),
            dim=["EV_bat!", "battery_modes!"],
        ),
        esoi_ev_batteries(),
    )


@component.add(
    name="Grid_correction_factor_EV_batteries",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_grid_correction_factor_ev_batteries"},
)
def grid_correction_factor_ev_batteries():
    return _ext_constant_grid_correction_factor_ev_batteries()


_ext_constant_grid_correction_factor_ev_batteries = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "grid_correction_factor_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_grid_correction_factor_ev_batteries",
)


@component.add(
    name="kW_per_MW", units="kW/MW", comp_type="Constant", comp_subtype="Normal"
)
def kw_per_mw():
    """
    1000 kW = 1 MW.
    """
    return 1000


@component.add(
    name="lifetime_EV_batteries",
    units="Years",
    subscripts=["EV_bat", "battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "net_stored_energy_ev_battery_over_lifetime": 1,
        "kwh_per_battery_ev": 1,
        "mj_to_kwh": 1,
        "yearly_cycles": 1,
    },
)
def lifetime_ev_batteries():
    """
    Lifetime of standard EV batteries considered.
    """
    return (
        zidz(
            net_stored_energy_ev_battery_over_lifetime(),
            (kwh_per_battery_ev() / mj_to_kwh()).expand_dims(
                {"EV_bat": _subscript_dict["EV_bat"]}, 0
            ),
        )
        / yearly_cycles()
    )


@component.add(
    name="max_Cp_EV_batteries",
    units="Dmnl",
    subscripts=["EV_bat", "battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "net_stored_energy_ev_battery_over_lifetime": 1,
        "kw_per_mw": 1,
        "min_lifetime_ev_batteries": 1,
        "mw_in_1_year_to_mj": 1,
        "kw_per_battery_ev": 1,
    },
)
def max_cp_ev_batteries():
    """
    Maximum Cp allowed associated to the minimum lifetime.
    """
    return net_stored_energy_ev_battery_over_lifetime() / (
        min_lifetime_ev_batteries()
        * mw_in_1_year_to_mj()
        * (kw_per_battery_ev() / kw_per_mw())
    )


@component.add(
    name="max_Cp_EV_batteries_for_elec_storage",
    units="Dmnl",
    subscripts=["battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cp_ev_batteries_for_transp": 1},
)
def max_cp_ev_batteries_for_elec_storage():
    """
    We assume a maximum Cp of EV batteries dedicated for electric storage which equates the use for Transportation uses.
    """
    return cp_ev_batteries_for_transp()


@component.add(
    name="min_lifetime_EV_batteries",
    units="Years",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_min_lifetime_ev_batteries"},
)
def min_lifetime_ev_batteries():
    """
    User-selection of the minimum lifetime of the batteries for electric vehicles given the issues arising from ain increased Cp for electric storage, i.e. a reduced lifetime of the battery (lower availability for the user, replace more often the battery, worsening of EROI of the system, etc.). It would be more interesting that Governments invest in electric batteries for storage if the performance of the electric vehicles would be significantly negatively affected.
    """
    return _ext_constant_min_lifetime_ev_batteries()


_ext_constant_min_lifetime_ev_batteries = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "minimum_lifetime_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_min_lifetime_ev_batteries",
)


@component.add(
    name="MJ_to_KWh", units="kWh/MJ", comp_type="Constant", comp_subtype="Normal"
)
def mj_to_kwh():
    return 0.27778


@component.add(
    name="MW_in_1_year_to_MJ",
    units="MJ/(year*MW)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mw_in_1_year_to_mj():
    """
    Conversion factor MW in 1 year to MJ.
    """
    return 24 * 365 * 3600


@component.add(
    name="Net_stored_energy_EV_battery_over_lifetime",
    units="MJ/battery",
    subscripts=["EV_bat", "battery_modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_net_stored_energy_ev_battery_over_lifetime"
    },
)
def net_stored_energy_ev_battery_over_lifetime():
    """
    Net stored energy EV battery in whole lifetime.
    """
    return _ext_constant_net_stored_energy_ev_battery_over_lifetime()


_ext_constant_net_stored_energy_ev_battery_over_lifetime = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "net_stored_energy_ev_battery_over_lifetime",
    {
        "EV_bat": _subscript_dict["EV_bat"],
        "battery_modes": _subscript_dict["battery_modes"],
    },
    _root,
    {
        "EV_bat": _subscript_dict["EV_bat"],
        "battery_modes": _subscript_dict["battery_modes"],
    },
    "_ext_constant_net_stored_energy_ev_battery_over_lifetime",
)


@component.add(
    name="output_EV_bateries_for_storage_over_lifetime",
    units="EJ/year",
    subscripts=["EV_bat", "battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_ev_batteries_for_elec_storage": 1,
        "newreplaced_batteries_tw": 1,
        "twe_per_twh": 1,
        "lifetime_ev_batteries": 1,
        "ej_per_twh": 1,
    },
)
def output_ev_bateries_for_storage_over_lifetime():
    """
    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
    """
    return (
        cp_ev_batteries_for_elec_storage()
        * newreplaced_batteries_tw()
        * (1 / twe_per_twh())
        * lifetime_ev_batteries()
        * ej_per_twh()
    )


@component.add(
    name="Share_energy_requirements_for_decom_EV_batteries",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_energy_requirements_for_decom_ev_batteries"
    },
)
def share_energy_requirements_for_decom_ev_batteries():
    return _ext_constant_share_energy_requirements_for_decom_ev_batteries()


_ext_constant_share_energy_requirements_for_decom_ev_batteries = ExtConstant(
    r"../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_share_energy_requirements_for_decom_ev_batteries",
)


@component.add(
    name="T_cycles",
    units="hours",
    subscripts=["battery_modes"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_t_cycles"},
)
def t_cycles():
    return _ext_constant_t_cycles()


_ext_constant_t_cycles = ExtConstant(
    r"../transport.xlsx",
    "Global",
    "t_cycle*",
    {"battery_modes": _subscript_dict["battery_modes"]},
    _root,
    {"battery_modes": _subscript_dict["battery_modes"]},
    "_ext_constant_t_cycles",
)


@component.add(
    name="yearly_cycles",
    units="cycles",
    subscripts=["battery_modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_ev_batteries_for_transp": 1,
        "cp_ev_batteries_for_elec_storage": 1,
        "t_cycles": 1,
    },
)
def yearly_cycles():
    return (
        (cp_ev_batteries_for_transp() + cp_ev_batteries_for_elec_storage())
        * 8760
        / t_cycles()
    )
