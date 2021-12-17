"""
Module ev_batteries_en
Translated using PySD version 2.2.0
"""


def cp_ev_batteries_for_transp():
    """
    Real Name: Cp EV batteries for Transp
    Original Eqn: 0.0055
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.0055


def energy_intensity_construction_ev_batteries_mjmw():
    """
    Real Name: "Energy intensity construction EV batteries MJ/MW"
    Original Eqn: ZIDZ( Total energy required for total material consumption for EV batteries *MJ per EJ, "new+replaced batteries TW"*M per T )
    Units: MJ/MW
    Limits: (None, None)
    Type: component
    Subs: None

    Energy intensity of the construction of EV batteries. Dynamic variable
        affected by recycling policies.
    """
    return zidz(
        total_energy_required_for_total_material_consumption_for_ev_batteries()
        * mj_per_ej(),
        newreplaced_batteries_tw() * m_per_t(),
    )


def esoi_ev_batteries():
    """
    Real Name: ESOI EV batteries
    Original Eqn: lifetime EV batteries*Cp EV batteries for elec storage*MW in 1 year to MJ/("g=quality of electricity"*"Energy intensity construction EV batteries MJ/MW"*(1+Share energy requirements for decom EV batteries+Grid correction factor EV batteries))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    ESOI batteries of electric vehicles for electricity storage.        (To estimate the ESOI static: g=0.7 and constant recycling rates)
    """
    return (
        lifetime_ev_batteries()
        * cp_ev_batteries_for_elec_storage()
        * mw_in_1_year_to_mj()
        / (
            gquality_of_electricity()
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
    Original Eqn: ZIDZ( output EV bateries for storage over lifetime, ESOI EV batteries )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy invested (equivalent to the denominator of the EROI (=CED*g).
    """
    return zidz(output_ev_bateries_for_storage_over_lifetime(), esoi_ev_batteries())


def grid_correction_factor_ev_batteries():
    """
    Real Name: Grid correction factor EV batteries
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'grid_correction_factor_ev_batteries')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_grid_correction_factor_ev_batteries()


def kw_per_mw():
    """
    Real Name: kW per MW
    Original Eqn: 1000
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1000 kW = 1 MW.
    """
    return 1000


def lifetime_ev_batteries():
    """
    Real Name: lifetime EV batteries
    Original Eqn: ZIDZ( Net stored energy EV battery over lifetime, ((Cp EV batteries for elec storage+Cp EV batteries for Transp)*MW in 1 year to MJ*(kW per battery EV /kW per MW)) )
    Units: Years
    Limits: (None, None)
    Type: component
    Subs: None

    Lifetime of standard EV batteries considered.
    """
    return zidz(
        net_stored_energy_ev_battery_over_lifetime(),
        (
            (cp_ev_batteries_for_elec_storage() + cp_ev_batteries_for_transp())
            * mw_in_1_year_to_mj()
            * (kw_per_battery_ev() / kw_per_mw())
        ),
    )


def max_cp_ev_batteries():
    """
    Real Name: max Cp EV batteries
    Original Eqn: Net stored energy EV battery over lifetime/(min lifetime EV batteries*MW in 1 year to MJ*(kW per battery EV/kW per MW))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: Cp EV batteries for Transp
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    We assume a maximum Cp of EV batteries dedicated for electric storage
        which equates the use for Transportation uses.
    """
    return cp_ev_batteries_for_transp()


def min_lifetime_ev_batteries():
    """
    Real Name: min lifetime EV batteries
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'minimum_lifetime_ev_batteries')
    Units: Years
    Limits: (None, None)
    Type: constant
    Subs: None

    User-selection of the minimum lifetime of the batteries for electric
        vehicles given the issues arising from ain increased Cp for electric
        storage, i.e. a reduced lifetime of the battery (lower availability for
        the user, replace more often the battery, worsening of EROI of the system,
        etc.). It would be more interesting that Governments invest in electric
        batteries for storage if the performance of the electric vehicles would be
        significantly negatively affected.
    """
    return _ext_constant_min_lifetime_ev_batteries()


def mw_in_1_year_to_mj():
    """
    Real Name: MW in 1 year to MJ
    Original Eqn: 24*365*3600
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion factor MW in 1 year to MJ.
    """
    return 24 * 365 * 3600


def net_stored_energy_ev_battery_over_lifetime():
    """
    Real Name: Net stored energy EV battery over lifetime
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'net_stored_energy_ev_battery_over_lifetime')
    Units: MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Net stored energy EV battery in whole lifetime.
    """
    return _ext_constant_net_stored_energy_ev_battery_over_lifetime()


def output_ev_bateries_for_storage_over_lifetime():
    """
    Real Name: output EV bateries for storage over lifetime
    Original Eqn: Cp EV batteries for elec storage*"new+replaced batteries TW"*(1/TWe per TWh)*lifetime EV batteries*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total electricity output generated over the full operation of the
        infrastructure of the new capacity installed.
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
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'share_energy_requirements_for_decom_ev_batteries')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_share_energy_requirements_for_decom_ev_batteries()


_ext_constant_grid_correction_factor_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "grid_correction_factor_ev_batteries",
    {},
    _root,
    "_ext_constant_grid_correction_factor_ev_batteries",
)


_ext_constant_min_lifetime_ev_batteries = ExtConstant(
    "../energy.xlsx",
    "Global",
    "minimum_lifetime_ev_batteries",
    {},
    _root,
    "_ext_constant_min_lifetime_ev_batteries",
)


_ext_constant_net_stored_energy_ev_battery_over_lifetime = ExtConstant(
    "../energy.xlsx",
    "Global",
    "net_stored_energy_ev_battery_over_lifetime",
    {},
    _root,
    "_ext_constant_net_stored_energy_ev_battery_over_lifetime",
)


_ext_constant_share_energy_requirements_for_decom_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_ev_batteries",
    {},
    _root,
    "_ext_constant_share_energy_requirements_for_decom_ev_batteries",
)
