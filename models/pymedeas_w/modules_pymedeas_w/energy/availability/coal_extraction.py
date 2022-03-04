"""
Module coal_extraction
Translated using PySD version 2.2.1
"""


def abundance_coal():
    """
    Real Name: abundance coal
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        extraction_coal_ej() > ped_coal_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_coal_ej() - extraction_coal_ej(), ped_coal_ej()),
    )


def coal_to_leave_underground():
    """
    Real Name: coal to leave underground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Coal to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_coal(),
        lambda: 0,
        lambda: share_rurr_coal_to_leave_underground() * rurr_coal_start_year_plg(),
    )


def cumulated_coal_extraction():
    """
    Real Name: Cumulated coal extraction
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Cumulated coal extraction.
    """
    return _integ_cumulated_coal_extraction()


_integ_cumulated_coal_extraction = Integ(
    lambda: extraction_coal_ej(),
    lambda: cumulated_coal_extraction_to_1995(),
    "_integ_cumulated_coal_extraction",
)


def cumulated_coal_extraction_to_1995():
    """
    Real Name: cumulated coal extraction to 1995
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Cumulated coal extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_coal_extraction_to_1995()


_ext_constant_cumulated_coal_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_coal_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_coal_extraction_to_1995",
)


def extraction_coal_ej():
    """
    Real Name: extraction coal EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual extraction of coal.
    """
    return if_then_else(
        rurr_coal() < 0,
        lambda: 0,
        lambda: if_then_else(
            np.logical_or(unlimited_nre() == 1, unlimited_coal() == 1),
            lambda: ped_coal_ej(),
            lambda: np.minimum(ped_coal_ej(), max_extraction_coal_ej()),
        ),
    )


def extraction_coal_emissions_relevant_ej():
    """
    Real Name: extraction coal emissions relevant EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Extraction of emission-relevant coal, i.e. excepting the resource used for non-energy uses.
    """
    return np.maximum(
        0,
        extraction_coal_without_ctl_ej()
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]),
    )


def extraction_coal_for_ctl_ej():
    """
    Real Name: extraction coal for CTL EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Extraction of coal for CTL. CTL demand is given priority over other uses since it is an exogenous assumption depending on the scenario.
    """
    return ped_coal_for_ctl_ej()


def extraction_coal_mtoe():
    """
    Real Name: extraction coal Mtoe
    Original Eqn:
    Units: MToe/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual extraction of coal.
    """
    return extraction_coal_ej() * mtoe_per_ej()


def extraction_coal_without_ctl_ej():
    """
    Real Name: extraction coal without CTL EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Extraction of conventional gas excepting the resource used to produce GTL.
    """
    return np.maximum(extraction_coal_ej() - extraction_coal_for_ctl_ej(), 0)


def flow_coal_left_in_ground():
    """
    Real Name: Flow coal left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Flow of coal left in the ground. We assume that this amount is removed from the stock of coal available in 1 year.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_coal(),
        lambda: 0,
        lambda: if_then_else(
            time() >= start_policy_leave_in_ground_coal() + 1,
            lambda: 0,
            lambda: coal_to_leave_underground(),
        ),
    )


def max_extraction_coal_ej():
    """
    Real Name: max extraction coal EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_coal(tot_rurr_coal())


def max_extraction_coal_mtoe():
    """
    Real Name: max extraction coal Mtoe
    Original Eqn:
    Units: MToe/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum extraction curve selected for the simulations.
    """
    return max_extraction_coal_ej() * mtoe_per_ej()


def ped_coal_without_ctl():
    """
    Real Name: PED coal without CTL
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total demand of coal without CTL.
    """
    return ped_coal_ej() - ped_coal_for_ctl_ej()


def rurr_coal():
    """
    Real Name: RURR coal
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR coal. 4400 EJ extracted before 1990.
    """
    return _integ_rurr_coal()


_integ_rurr_coal = Integ(
    lambda: -extraction_coal_ej() - flow_coal_left_in_ground(),
    lambda: urr_coal() - cumulated_coal_extraction_to_1995(),
    "_integ_rurr_coal",
)


def rurr_coal_start_year_plg():
    """
    Real Name: RURR coal start year PLG
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_coal_start_year_plg()


_sampleiftrue_rurr_coal_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_coal(),
    lambda: rurr_coal(),
    lambda: rurr_coal(),
    "_sampleiftrue_rurr_coal_start_year_plg",
)


def share_rurr_coal_to_leave_underground():
    """
    Real Name: share RURR coal to leave underground
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    RURR's coal to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_coal_to_leave_underground()


_ext_constant_share_rurr_coal_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_coal_underground",
    {},
    _root,
    "_ext_constant_share_rurr_coal_to_leave_underground",
)


def start_policy_leave_in_ground_coal():
    """
    Real Name: Start policy leave in ground coal
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when the policy to leave in the ground an amount of coal RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_coal()


_ext_constant_start_policy_leave_in_ground_coal = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_coal_underground",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_coal",
)


def table_max_extraction_coal(x):
    """
    Real Name: table max extraction coal
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_max_extraction_coal(x)


_ext_lookup_table_max_extraction_coal = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_coal",
    "max_extraction_coal",
    {},
    _root,
    "_ext_lookup_table_max_extraction_coal",
)


def tot_rurr_coal():
    """
    Real Name: Tot RURR coal
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total RURR of coal considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_coal() + total_coal_left_in_ground()


def total_coal_left_in_ground():
    """
    Real Name: Total coal left in ground
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_total_coal_left_in_ground()


_integ_total_coal_left_in_ground = Integ(
    lambda: flow_coal_left_in_ground(), lambda: 0, "_integ_total_coal_left_in_ground"
)


def unlimited_coal():
    """
    Real Name: "unlimited coal?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Switch to consider if coal is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_coal()


_ext_constant_unlimited_coal = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_coal",
    {},
    _root,
    "_ext_constant_unlimited_coal",
)


def urr_coal():
    """
    Real Name: URR coal
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        np.logical_or(unlimited_nre() == 1, unlimited_coal() == 1),
        lambda: nan,
        lambda: urr_coal_input(),
    )


def urr_coal_input():
    """
    Real Name: URR coal input
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_urr_coal_input()


_ext_constant_urr_coal_input = ExtConstant(
    "../energy.xlsx", "World", "URR_coal", {}, _root, "_ext_constant_urr_coal_input"
)


def year_scarcity_coal():
    """
    Real Name: Year scarcity coal
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_coal() > 0.95, lambda: 0, lambda: time())
