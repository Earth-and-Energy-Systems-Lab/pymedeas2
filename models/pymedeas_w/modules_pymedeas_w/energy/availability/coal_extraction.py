"""
Module coal_extraction
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="abundance coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej": 2, "ped_coal_ej": 3},
)
def abundance_coal():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        extraction_coal_ej() > ped_coal_ej(),
        lambda: 1,
        lambda: 1 - zidz(ped_coal_ej() - extraction_coal_ej(), ped_coal_ej()),
    )


@component.add(
    name="coal to leave underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "start_policy_leave_in_ground_coal": 1,
        "share_rurr_coal_to_leave_underground": 1,
        "rurr_coal_start_year_plg": 1,
    },
)
def coal_to_leave_underground():
    """
    Coal to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_coal(),
        lambda: 0,
        lambda: share_rurr_coal_to_leave_underground() * rurr_coal_start_year_plg(),
    )


@component.add(
    name="Cumulated coal extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_coal_extraction": 1},
    other_deps={
        "_integ_cumulated_coal_extraction": {
            "initial": {"cumulated_coal_extraction_to_1995": 1},
            "step": {"extraction_coal_ej": 1},
        }
    },
)
def cumulated_coal_extraction():
    """
    Cumulated coal extraction.
    """
    return _integ_cumulated_coal_extraction()


_integ_cumulated_coal_extraction = Integ(
    lambda: extraction_coal_ej(),
    lambda: cumulated_coal_extraction_to_1995(),
    "_integ_cumulated_coal_extraction",
)


@component.add(
    name="cumulated coal extraction to 1995",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulated_coal_extraction_to_1995"},
)
def cumulated_coal_extraction_to_1995():
    """
    Cumulated coal extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_coal_extraction_to_1995()


_ext_constant_cumulated_coal_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "World",
    "cumulative_coal_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_coal_extraction_to_1995",
)


@component.add(
    name="extraction coal EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rurr_coal": 1,
        "unlimited_nre": 1,
        "ped_coal_ej": 2,
        "unlimited_coal": 1,
        "max_extraction_coal_ej": 1,
    },
)
def extraction_coal_ej():
    """
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


@component.add(
    name="extraction coal emissions relevant",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_without_ctl": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def extraction_coal_emissions_relevant():
    """
    Extraction of emission-relevant coal, i.e. excepting the resource used for non-energy uses.
    """
    return np.maximum(
        0,
        extraction_coal_without_ctl()
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]),
    )


@component.add(
    name="extraction coal for CTL",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl_ej": 1},
)
def extraction_coal_for_ctl():
    """
    Extraction of coal for CTL. CTL demand is given priority over other uses since it is an exogenous assumption depending on the scenario.
    """
    return ped_coal_for_ctl_ej()


@component.add(
    name="extraction coal without CTL",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej": 1, "extraction_coal_for_ctl": 1},
)
def extraction_coal_without_ctl():
    """
    Extraction of conventional gas excepting the resource used to produce GTL.
    """
    return np.maximum(extraction_coal_ej() - extraction_coal_for_ctl(), 0)


@component.add(
    name="Flow coal left in ground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "start_policy_leave_in_ground_coal": 2,
        "coal_to_leave_underground": 1,
    },
)
def flow_coal_left_in_ground():
    """
    Flow of coal left in the ground. We assume that this amount is removed from the stock of coal available in 1 year.
    """
    return if_then_else(
        np.logical_or(
            time() < start_policy_leave_in_ground_coal(),
            time() >= start_policy_leave_in_ground_coal() + 1,
        ),
        lambda: 0,
        lambda: coal_to_leave_underground(),
    )


@component.add(
    name="max extraction coal EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tot_rurr_coal": 1, "table_max_extraction_coal": 1},
)
def max_extraction_coal_ej():
    """
    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_coal(tot_rurr_coal())


@component.add(
    name="max extraction coal Mtoe",
    units="MToe/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_extraction_coal_ej": 1, "mtoe_per_ej": 1},
)
def max_extraction_coal_mtoe():
    """
    Maximum extraction curve selected for the simulations.
    """
    return max_extraction_coal_ej() * mtoe_per_ej()


@component.add(
    name="PED coal without CTL",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "ped_coal_for_ctl_ej": 1},
)
def ped_coal_without_ctl():
    """
    Total demand of coal without CTL.
    """
    return ped_coal_ej() - ped_coal_for_ctl_ej()


@component.add(
    name="RURR coal",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_coal": 1},
    other_deps={
        "_integ_rurr_coal": {
            "initial": {"urr_coal": 1, "cumulated_coal_extraction_to_1995": 1},
            "step": {"extraction_coal_ej": 1, "flow_coal_left_in_ground": 1},
        }
    },
)
def rurr_coal():
    """
    RURR coal. 4400 EJ extracted before 1990.
    """
    return _integ_rurr_coal()


_integ_rurr_coal = Integ(
    lambda: -extraction_coal_ej() - flow_coal_left_in_ground(),
    lambda: urr_coal() - cumulated_coal_extraction_to_1995(),
    "_integ_rurr_coal",
)


@component.add(
    name="RURR coal start year PLG",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_coal_start_year_plg": 1},
    other_deps={
        "_sampleiftrue_rurr_coal_start_year_plg": {
            "initial": {"rurr_coal": 1},
            "step": {"time": 1, "start_policy_leave_in_ground_coal": 1, "rurr_coal": 1},
        }
    },
)
def rurr_coal_start_year_plg():
    """
    RURR until the start of the policy to leave in the ground (PLG) the resource.
    """
    return _sampleiftrue_rurr_coal_start_year_plg()


_sampleiftrue_rurr_coal_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_coal(),
    lambda: rurr_coal(),
    lambda: rurr_coal(),
    "_sampleiftrue_rurr_coal_start_year_plg",
)


@component.add(
    name="share RURR coal to leave underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_rurr_coal_to_leave_underground"},
)
def share_rurr_coal_to_leave_underground():
    """
    RURR's coal to be left in the ground as a share of the RURR in the year 2015.
    """
    return _ext_constant_share_rurr_coal_to_leave_underground()


_ext_constant_share_rurr_coal_to_leave_underground = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "share_RURR_coal_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_coal_to_leave_underground",
)


@component.add(
    name="Start policy leave in ground coal",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_policy_leave_in_ground_coal"},
)
def start_policy_leave_in_ground_coal():
    """
    Year when the policy to leave in the ground an amount of coal RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_coal()


_ext_constant_start_policy_leave_in_ground_coal = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_policy_year_coal_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_coal",
)


@component.add(
    name="table max extraction coal",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_coal",
        "__lookup__": "_ext_lookup_table_max_extraction_coal",
    },
)
def table_max_extraction_coal(x, final_subs=None):
    return _ext_lookup_table_max_extraction_coal(x, final_subs)


_ext_lookup_table_max_extraction_coal = ExtLookup(
    "../energy.xlsx",
    "World",
    "RURR_coal",
    "max_extraction_coal",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_coal",
)


@component.add(
    name="Tot RURR coal",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_coal": 1, "total_coal_left_in_ground": 1},
)
def tot_rurr_coal():
    """
    Total RURR of coal considering the available RURR and the eventual amount of RURR left in the ground as a policy.
    """
    return rurr_coal() + total_coal_left_in_ground()


@component.add(
    name="Total coal left in ground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_coal_left_in_ground": 1},
    other_deps={
        "_integ_total_coal_left_in_ground": {
            "initial": {},
            "step": {"flow_coal_left_in_ground": 1},
        }
    },
)
def total_coal_left_in_ground():
    return _integ_total_coal_left_in_ground()


_integ_total_coal_left_in_ground = Integ(
    lambda: flow_coal_left_in_ground(), lambda: 0, "_integ_total_coal_left_in_ground"
)


@component.add(
    name='"unlimited coal?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_unlimited_coal"},
)
def unlimited_coal():
    """
    Switch to consider if coal is unlimited (1), or if it is limited (0). If limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_coal()


_ext_constant_unlimited_coal = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "unlimited_coal",
    {},
    _root,
    {},
    "_ext_constant_unlimited_coal",
)


@component.add(
    name="URR coal",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unlimited_nre": 1, "unlimited_coal": 1, "urr_coal_input": 1},
)
def urr_coal():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return if_then_else(
        np.logical_or(unlimited_nre() == 1, unlimited_coal() == 1),
        lambda: np.nan,
        lambda: urr_coal_input(),
    )


@component.add(
    name="URR coal input",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_coal_input"},
)
def urr_coal_input():
    return _ext_constant_urr_coal_input()


_ext_constant_urr_coal_input = ExtConstant(
    "../energy.xlsx", "World", "URR_coal", {}, _root, {}, "_ext_constant_urr_coal_input"
)


@component.add(
    name="Year scarcity coal",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_coal": 1, "time": 1},
)
def year_scarcity_coal():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_coal() > 0.95, lambda: 0, lambda: time())
