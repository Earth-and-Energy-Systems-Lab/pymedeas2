"""
Module storage_demand_and_supply
Translated using PySD version 2.2.1
"""


def abundance_storage():
    """
    Real Name: "\"abundance\" storage"
    Original Eqn: 1-IF THEN ELSE(demand storage capacity <= Total capacity elec storage TW , 1, MAX(0, 1-(demand storage capacity-Total capacity elec storage TW )/Total capacity elec storage TW))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Increases the planning of PHS if there is a deficit of electric storage.
    """
    return 1 - if_then_else(
        demand_storage_capacity() <= total_capacity_elec_storage_tw(),
        lambda: 1,
        lambda: np.maximum(
            0,
            1
            - (demand_storage_capacity() - total_capacity_elec_storage_tw())
            / total_capacity_elec_storage_tw(),
        ),
    )


@subs(["RES elec"], _subscript_dict)
def constraint_elec_storage_availability():
    """
    Real Name: constraint elec storage availability
    Original Eqn: IF THEN ELSE("RES elec variables?"[RES elec]=0,1, IF THEN ELSE(demand storage capacity <= Total capacity elec storage TW , 1, MAX(0, 1-(demand storage capacity-Total capacity elec storage TW )/Total capacity elec storage TW)))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Remaining potential available as a fraction of unity. This feedback
        ensures that the electricity storage levels required by the penetration of
        the RES variables for the generation of electricity are respected.
    """
    return if_then_else(
        res_elec_variables() == 0,
        lambda: 1,
        lambda: if_then_else(
            demand_storage_capacity() <= total_capacity_elec_storage_tw(),
            lambda: 1,
            lambda: np.maximum(
                0,
                1
                - (demand_storage_capacity() - total_capacity_elec_storage_tw())
                / total_capacity_elec_storage_tw(),
            ),
        ),
    )


def cp_ev_batteries_for_elec_storage():
    """
    Real Name: Cp EV batteries for elec storage
    Original Eqn: MIN(Cp EV batteries required, max Cp EV batteries for elec storage)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Dynamic evolution of the Cp of EV batteries for electricity storage.
    """
    return np.minimum(
        cp_ev_batteries_required(), max_cp_ev_batteries_for_elec_storage()
    )


def cp_ev_batteries_required():
    """
    Real Name: Cp EV batteries required
    Original Eqn: MAX(0, demand EV batteries for elec storage/EV batteries TW)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.maximum(0, demand_ev_batteries_for_elec_storage() / ev_batteries_tw())


def demand_ev_batteries_for_elec_storage():
    """
    Real Name: demand EV batteries for elec storage
    Original Eqn: MAX(0, demand storage capacity-installed capacity PHS TW)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of EV batteries for storage of electricity.
    """
    return np.maximum(0, demand_storage_capacity() - installed_capacity_phs_tw())


def demand_storage_capacity():
    """
    Real Name: demand storage capacity
    Original Eqn: "share capacity storage/RES elec var"*Total installed capacity RES elec var
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Required storage capacity to install to deal with the variability of RES
        for electricity.
    """
    return (
        share_capacity_storageres_elec_var() * total_installed_capacity_res_elec_var()
    )


def esoi_elec_storage():
    """
    Real Name: ESOI elec storage
    Original Eqn: (ESOI PHS*installed capacity PHS TW+ESOI EV batteries *Used EV batteries for elec storage)/Total capacity elec storage TW
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    ESOI of electric storage (PHS and EV batteries).
    """
    return (
        esoi_phs() * installed_capacity_phs_tw()
        + esoi_ev_batteries() * used_ev_batteries_for_elec_storage()
    ) / total_capacity_elec_storage_tw()


def max_capacity_elec_storage():
    """
    Real Name: max capacity elec storage
    Original Eqn: max capacity potential PHS+Used EV batteries for elec storage
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum capacity potential of electricity storage (PHS and electric
        bateries).
    """
    return max_capacity_potential_phs() + used_ev_batteries_for_elec_storage()


def real_fe_elec_stored_ev_batteries_twh():
    """
    Real Name: real FE elec stored EV batteries TWh
    Original Eqn: Used EV batteries for elec storage/TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    installed capacity PHS TW*Cp PHS/TWe per TWh        Electricity stored in EV batteries. It does not add up to the electricity
        generation of other sources since this electricity has already been
        accounted for! (stored).
    """
    return used_ev_batteries_for_elec_storage() / twe_per_twh()


@subs(["RES elec"], _subscript_dict)
def remaining_potential_elec_storage_by_res_techn():
    """
    Real Name: remaining potential elec storage by RES techn
    Original Eqn: IF THEN ELSE(max capacity elec storage >= demand storage capacity , (max capacity elec storage-demand storage capacity)/max capacity elec storage, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_capacity_elec_storage() >= demand_storage_capacity(),
        lambda: (max_capacity_elec_storage() - demand_storage_capacity())
        / max_capacity_elec_storage(),
        lambda: 0,
    )


def rt_elec_storage_efficiency():
    """
    Real Name: rt elec storage efficiency
    Original Eqn: (rt storage efficiency PHS*installed capacity PHS TW+rt storage efficiency EV batteries*Used EV batteries for elec storage)/Total capacity elec storage TW
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Round-trip storage efficiency of electric storage (PHS and EV batteries).
    """
    return (
        rt_storage_efficiency_phs() * installed_capacity_phs_tw()
        + rt_storage_efficiency_ev_batteries() * used_ev_batteries_for_elec_storage()
    ) / total_capacity_elec_storage_tw()


def rt_storage_efficiency_ev_batteries():
    """
    Real Name: rt storage efficiency EV batteries
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'round_trip_storage_efficiency_ev_batteries')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Round-trip storage efficiency of electric batteries frome electric
        vehicles.
    """
    return _ext_constant_rt_storage_efficiency_ev_batteries()


def rt_storage_efficiency_phs():
    """
    Real Name: rt storage efficiency PHS
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'round_trip_storage_efficiency_phs')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Round-trip storage efficiency.
    """
    return _ext_constant_rt_storage_efficiency_phs()


def share_capacity_storageres_elec_var():
    """
    Real Name: "share capacity storage/RES elec var"
    Original Eqn: 0.099+0.1132*share Elec demand covered by RES
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share installed capacity of storage vs installed capacity of variable RES
        for electricity. Estimation from NREL (2012).
    """
    return 0.099 + 0.1132 * share_elec_demand_covered_by_res()


def total_capacity_elec_storage_tw():
    """
    Real Name: Total capacity elec storage TW
    Original Eqn: installed capacity PHS TW+Used EV batteries for elec storage
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Total capacity electricity storage installed.
    """
    return installed_capacity_phs_tw() + used_ev_batteries_for_elec_storage()


def total_installed_capacity_res_elec_var():
    """
    Real Name: Total installed capacity RES elec var
    Original Eqn: installed capacity RES elec TW[wind onshore]+installed capacity RES elec TW[wind offshore]+installed capacity RES elec TW[solar PV]+installed capacity RES elec TW[CSP]
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Total installed capacity of RES variables for electricity generation.
    """
    return (
        float(installed_capacity_res_elec_tw().loc["wind onshore"])
        + float(installed_capacity_res_elec_tw().loc["wind offshore"])
        + float(installed_capacity_res_elec_tw().loc["solar PV"])
        + float(installed_capacity_res_elec_tw().loc["CSP"])
    )


def used_ev_batteries_for_elec_storage():
    """
    Real Name: Used EV batteries for elec storage
    Original Eqn: EV batteries TW*Cp EV batteries for elec storage
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Bateries from electric vehicles used for electric storage.
    """
    return ev_batteries_tw() * cp_ev_batteries_for_elec_storage()


_ext_constant_rt_storage_efficiency_ev_batteries = ExtConstant(
    "../energy.xlsx",
    "Global",
    "round_trip_storage_efficiency_ev_batteries",
    {},
    _root,
    "_ext_constant_rt_storage_efficiency_ev_batteries",
)


_ext_constant_rt_storage_efficiency_phs = ExtConstant(
    "../energy.xlsx",
    "Global",
    "round_trip_storage_efficiency_phs",
    {},
    _root,
    "_ext_constant_rt_storage_efficiency_phs",
)
