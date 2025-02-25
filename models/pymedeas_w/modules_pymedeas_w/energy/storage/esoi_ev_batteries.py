"""
Module energy.storage.esoi_ev_batteries
Translated using PySD version 3.14.0
"""

@component.add(
    name="Cp EV batteries for Transp",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cp_ev_batteries_for_transp():
    return 0.0055


@component.add(
    name='"Energy intensity construction EV batteries MJ/MW"',
    units="MJ/MW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_energy_required_for_total_material_consumption_for_ev_batteries": 1,
        "mj_per_ej": 1,
        "newreplaced_batteries_tw": 1,
        "mw_per_tw": 1,
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
    name="ESOI EV batteries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lifetime_ev_batteries": 1,
        "cp_ev_batteries_for_elec_storage": 1,
        "mw_in_1_year_to_mj": 1,
        "quality_of_electricity": 1,
        "energy_intensity_construction_ev_batteries_mjmw": 1,
        "share_energy_requirements_for_decom_ev_batteries": 1,
        "grid_correction_factor_ev_batteries": 1,
    },
)
def esoi_ev_batteries():
    """
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


@component.add(
    name="FEI EV batteries",
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
    return zidz(output_ev_bateries_for_storage_over_lifetime(), esoi_ev_batteries())


@component.add(
    name="Grid correction factor EV batteries",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_grid_correction_factor_ev_batteries"},
)
def grid_correction_factor_ev_batteries():
    return _ext_constant_grid_correction_factor_ev_batteries()


_ext_constant_grid_correction_factor_ev_batteries = ExtConstant(
    "../materials.xlsx",
    "Global",
    "grid_correction_factor_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_grid_correction_factor_ev_batteries",
)


@component.add(
    name="kW per MW", units="kW/MW", comp_type="Constant", comp_subtype="Normal"
)
def kw_per_mw():
    """
    1000 kW = 1 MW.
    """
    return 1000


@component.add(
    name="lifetime EV batteries",
    units="years",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "net_stored_energy_ev_battery_over_lifetime": 1,
        "kw_per_battery_ev": 1,
        "cp_ev_batteries_for_transp": 1,
        "cp_ev_batteries_for_elec_storage": 1,
        "kw_per_mw": 1,
        "mw_in_1_year_to_mj": 1,
    },
)
def lifetime_ev_batteries():
    """
    Lifetime of standard EV batteries considered.
    """
    return zidz(
        net_stored_energy_ev_battery_over_lifetime(),
        (cp_ev_batteries_for_elec_storage() + cp_ev_batteries_for_transp())
        * mw_in_1_year_to_mj()
        * (kw_per_battery_ev() / kw_per_mw()),
    )


@component.add(
    name="max Cp EV batteries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "net_stored_energy_ev_battery_over_lifetime": 1,
        "kw_per_battery_ev": 1,
        "min_lifetime_ev_batteries": 1,
        "mw_in_1_year_to_mj": 1,
        "kw_per_mw": 1,
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
    name="max Cp EV batteries for elec storage",
    units="Dmnl",
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
    name="min lifetime EV batteries",
    units="years",
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
    "../energy.xlsx",
    "Global",
    "minimum_lifetime_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_min_lifetime_ev_batteries",
)


@component.add(
    name="MW in 1 year to MJ",
    units="MJ/(MW*year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mw_in_1_year_to_mj():
    """
    Conversion factor MW in 1 year to MJ.
    """
    return 24 * 365 * 3600


@component.add(
    name="Net stored energy EV battery over lifetime",
    units="MJ/battery",
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
    "../energy.xlsx",
    "Global",
    "net_stored_energy_ev_battery_over_lifetime",
    {},
    _root,
    {},
    "_ext_constant_net_stored_energy_ev_battery_over_lifetime",
)


@component.add(
    name="output EV bateries for storage over lifetime",
    units="EJ/year",
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
    name="Share energy requirements for decom EV batteries",
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
    "../materials.xlsx",
    "Global",
    "share_energy_requirements_for_decom_ev_batteries",
    {},
    _root,
    {},
    "_ext_constant_share_energy_requirements_for_decom_ev_batteries",
)
