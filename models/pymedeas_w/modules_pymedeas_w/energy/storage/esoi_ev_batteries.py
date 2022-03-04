"""
Module esoi_ev_batteries
Translated using PySD version 2.2.1
"""


def cp_ev_batteries_for_transp():
    """
    Real Name: Cp EV batteries for Transp
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return 0.0055


def energy_intensity_construction_ev_batteries_mjmw():
    """
    Real Name: "Energy intensity construction EV batteries MJ/MW"
    Original Eqn:
    Units: MJ/MW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Energy intensity of the construction of EV batteries. Dynamic variable affected by recycling policies.
    """
    return zidz(
        total_energy_required_for_total_material_consumption_for_ev_batteries()
        * mj_per_ej(),
        newreplaced_batteries_tw() * m_per_t(),
    )


def esoi_ev_batteries():
    """
    Real Name: ESOI EV batteries
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    ESOI batteries of electric vehicles for electricity storage. (To estimate the ESOI static: g=0.7 and constant recycling rates)
    """
    return (
        lifetime_ev_batteries()
        * cp_ev_batteries_for_elec_storage()
        * mw_in_1_year_to_mj()
        / (
            quality_of_electricity()
            * energy_intensity_construction_ev_batteries_mjmw()
            * (
                1
                + share_energy_requirements_for_decom_ev_batteries()
                + grid_correction_factor_ev_batteries()
            )
        )
    )


def fei_ev_batteries():
    """
    Real Name: FEI EV batteries
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy invested (equivalent to the denominator of the EROI (=CED*g).
    """
    return zidz(output_ev_bateries_for_storage_over_lifetime(), esoi_ev_batteries())


def grid_correction_factor_ev_batteries():
    """
    Real Name: Grid correction factor EV batteries
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_grid_correction_factor_ev_batteries()


_ext_constant_grid_correction_factor_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "grid_correction_factor_ev_batteries",
    {},
    _root,
    "_ext_constant_grid_correction_factor_ev_batteries",
)


def kw_per_mw():
    """
    Real Name: kW per MW
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    1000 kW = 1 MW.
    """
    return 1000


def lifetime_ev_batteries():
    """
    Real Name: lifetime EV batteries
    Original Eqn:
    Units: years
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Lifetime of standard EV batteries considered.
    """
    return zidz(
        net_stored_energy_ev_battery_over_lifetime(),
        (cp_ev_batteries_for_elec_storage() + cp_ev_batteries_for_transp())
        * mw_in_1_year_to_mj()
        * (kw_per_battery_ev() / kw_per_mw()),
    )


def max_cp_ev_batteries():
    """
    Real Name: max Cp EV batteries
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum Cp allowed associated to the minimum lifetime.
    """
    return net_stored_energy_ev_battery_over_lifetime() / (
        min_lifetime_ev_batteries()
        * mw_in_1_year_to_mj()
        * (kw_per_battery_ev() / kw_per_mw())
    )


def max_cp_ev_batteries_for_elec_storage():
    """
    Real Name: max Cp EV batteries for elec storage
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    We assume a maximum Cp of EV batteries dedicated for electric storage which equates the use for Transportation uses.
    """
    return cp_ev_batteries_for_transp()


def min_lifetime_ev_batteries():
    """
    Real Name: min lifetime EV batteries
    Original Eqn:
    Units: years
    Limits: (None, None)
    Type: Constant
    Subs: []

    User-selection of the minimum lifetime of the batteries for electric vehicles given the issues arising from ain increased Cp for electric storage, i.e. a reduced lifetime of the battery (lower availability for the user, replace more often the battery, worsening of EROI of the system, etc.). It would be more interesting that Governments invest in electric batteries for storage if the performance of the electric vehicles would be significantly negatively affected.
    """
    return _ext_constant_min_lifetime_ev_batteries()


_ext_constant_min_lifetime_ev_batteries = ExtConstant(
    "../energy.xlsx",
    "Global",
    "minimum_lifetime_ev_batteries",
    {},
    _root,
    "_ext_constant_min_lifetime_ev_batteries",
)


def mw_in_1_year_to_mj():
    """
    Real Name: MW in 1 year to MJ
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion factor MW in 1 year to MJ.
    """
    return 24 * 365 * 3600


def net_stored_energy_ev_battery_over_lifetime():
    """
    Real Name: Net stored energy EV battery over lifetime
    Original Eqn:
    Units: MJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Net stored energy EV battery in whole lifetime.
    """
    return _ext_constant_net_stored_energy_ev_battery_over_lifetime()


_ext_constant_net_stored_energy_ev_battery_over_lifetime = ExtConstant(
    "../energy.xlsx",
    "Global",
    "net_stored_energy_ev_battery_over_lifetime",
    {},
    _root,
    "_ext_constant_net_stored_energy_ev_battery_over_lifetime",
)


def output_ev_bateries_for_storage_over_lifetime():
    """
    Real Name: output EV bateries for storage over lifetime
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
    """
    return (
        cp_ev_batteries_for_elec_storage()
        * newreplaced_batteries_tw()
        * (1 / twe_per_twh())
        * lifetime_ev_batteries()
        * ej_per_twh()
    )


def share_energy_requirements_for_decom_ev_batteries():
    """
    Real Name: Share energy requirements for decom EV batteries
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_share_energy_requirements_for_decom_ev_batteries()


_ext_constant_share_energy_requirements_for_decom_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_ev_batteries",
    {},
    _root,
    "_ext_constant_share_energy_requirements_for_decom_ev_batteries",
)
