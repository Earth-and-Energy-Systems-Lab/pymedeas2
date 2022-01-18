"""
Module coal_extraction
Translated using PySD version 2.2.0
"""


def abundance_coal_eu():
    """
    Real Name: abundance coal EU
    Original Eqn: IF THEN ELSE((extraction coal EJ EU+imports EU coal from RoW EJ )>PED coal EJ, 1, 1-ZIDZ( (PED coal EJ-extraction coal EJ EU -imports EU coal from RoW EJ), PED coal EJ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        (extraction_coal_ej_eu() + imports_eu_coal_from_row_ej()) > ped_coal_ej(),
        lambda: 1,
        lambda: 1
        - zidz(
            (ped_coal_ej() - extraction_coal_ej_eu() - imports_eu_coal_from_row_ej()),
            ped_coal_ej(),
        ),
    )


def coal_to_leave_underground():
    """
    Real Name: coal to leave underground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground coal, 0, share RURR coal to leave underground*RURR coal start year PLG)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Coal to be left underground due to the application of a policy.
    """
    return if_then_else(
        time() < start_policy_leave_in_ground_coal(),
        lambda: 0,
        lambda: share_rurr_coal_to_leave_underground() * rurr_coal_start_year_plg(),
    )


def consumption_ue_coal_emissions_relevant_ej():
    """
    Real Name: consumption UE coal emissions relevant EJ
    Original Eqn: MAX(0, PEC coal-"Non-energy use demand by final fuel EJ"[solids])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Consumption of emission-relevant coal, i.e. excepting the resource used
        for non-energy uses.
    """
    return np.maximum(
        0, pec_coal() - float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


def cumulated_coal_extraction():
    """
    Real Name: Cumulated coal extraction
    Original Eqn: INTEG ( extraction coal EJ EU, cumulated coal extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulated coal extraction.
    """
    return _integ_cumulated_coal_extraction()


def cumulated_coal_extraction_to_1995():
    """
    Real Name: cumulated coal extraction to 1995
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'cumulative_coal_extraction_until_1995')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulated coal extraction to 1995 (Mohr et al., 2015).
    """
    return _ext_constant_cumulated_coal_extraction_to_1995()


def extraction_coal_ej_eu():
    """
    Real Name: extraction coal EJ EU
    Original Eqn: IF THEN ELSE(RURR coal<0,0, IF THEN ELSE(Time<2016 :OR: "unlimited NRE?"=1 :OR: "unlimited coal?"=1, PED domestic EU coal EJ,MIN(PED domestic EU coal EJ, max extraction coal EJ) ))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of coal.
    """
    return if_then_else(
        rurr_coal() < 0,
        lambda: 0,
        lambda: if_then_else(
            logical_or(time() < 2016, unlimited_nre() == 1, unlimited_coal() == 1),
            lambda: ped_domestic_eu_coal_ej(),
            lambda: np.minimum(ped_domestic_eu_coal_ej(), max_extraction_coal_ej()),
        ),
    )


def extraction_coal_emissions_relevant_ej():
    """
    Real Name: extraction coal emissions relevant EJ
    Original Eqn: MAX(0, extraction coal without CTL EJ-"Non-energy use demand by final fuel EJ"[solids])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of emission-relevant coal, i.e. excepting the resource used for
        non-energy uses.
    """
    return np.maximum(
        0,
        extraction_coal_without_ctl_ej()
        - float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]),
    )


def extraction_coal_for_ctl_ej():
    """
    Real Name: extraction coal for CTL EJ
    Original Eqn: PED coal for CTL EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of coal for CTL. CTL demand is given priority over other uses
        since it is an exogenous assumption depending on the scenario.
    """
    return ped_coal_for_ctl_ej()


def extraction_coal_mtoe():
    """
    Real Name: extraction coal Mtoe
    Original Eqn: extraction coal EJ EU*MToe per EJ
    Units: MToe/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual extraction of coal.
    """
    return extraction_coal_ej_eu() * mtoe_per_ej()


def extraction_coal_without_ctl_ej():
    """
    Real Name: extraction coal without CTL EJ
    Original Eqn: MAX(extraction coal EJ EU-extraction coal for CTL EJ, 0)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Extraction of conventional gas excepting the resource used to produce GTL.
    """
    return np.maximum(extraction_coal_ej_eu() - extraction_coal_for_ctl_ej(), 0)


def flow_coal_left_in_ground():
    """
    Real Name: Flow coal left in ground
    Original Eqn: IF THEN ELSE(Time<Start policy leave in ground coal,0, IF THEN ELSE(Time>=Start policy leave in ground coal+1,0, coal to leave underground))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Flow of coal left in the ground. We assume that this amount is removed
        from the stock of coal available in 1 year.
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
    Original Eqn: table max extraction coal(Tot RURR coal)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return table_max_extraction_coal(tot_rurr_coal())


def max_extraction_coal_mtoe():
    """
    Real Name: max extraction coal Mtoe
    Original Eqn: max extraction coal EJ*MToe per EJ
    Units: MToe/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum extraction curve selected for the simulations.
    """
    return max_extraction_coal_ej() * mtoe_per_ej()


def ped_coal_without_ctl():
    """
    Real Name: PED coal without CTL
    Original Eqn: PED coal EJ-PED coal for CTL EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand of coal without CTL.
    """
    return ped_coal_ej() - ped_coal_for_ctl_ej()


def rurr_coal():
    """
    Real Name: RURR coal
    Original Eqn: INTEG ( -extraction coal EJ EU-Flow coal left in ground, URR coal-cumulated coal extraction to 1995)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR coal. 4400 EJ extracted before 1990.
    """
    return _integ_rurr_coal()


def rurr_coal_start_year_plg():
    """
    Real Name: RURR coal start year PLG
    Original Eqn: SAMPLE IF TRUE(Time<Start policy leave in ground coal, RURR coal, RURR coal)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    RURR until the start of the policy to leave in the ground (PLG) the
        resource.
    """
    return _sample_if_true_rurr_coal_start_year_plg()


def share_rurr_coal_to_leave_underground():
    """
    Real Name: share RURR coal to leave underground
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C131')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    RURR's coal to be left in the ground as a share of the RURR in the year
        2015.
    """
    return _ext_constant_share_rurr_coal_to_leave_underground()


def start_policy_leave_in_ground_coal():
    """
    Real Name: Start policy leave in ground coal
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'C130')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when the policy to leave in the ground an amount of coal RURR enters
        into force.
    """
    return _ext_constant_start_policy_leave_in_ground_coal()


def table_max_extraction_coal(x):
    """
    Real Name: table max extraction coal
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Europe', 'RURR_coal', 'max_extraction_coal'))
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_max_extraction_coal(x)


def tot_rurr_coal():
    """
    Real Name: Tot RURR coal
    Original Eqn: RURR coal+Total coal left in ground
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total RURR of coal considering the available RURR and the eventual amount
        of RURR left in the ground as a policy.
    """
    return rurr_coal() + total_coal_left_in_ground()


def total_coal_left_in_ground():
    """
    Real Name: Total coal left in ground
    Original Eqn: INTEG ( Flow coal left in ground, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_total_coal_left_in_ground()


def unlimited_coal():
    """
    Real Name: "unlimited coal?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'E99')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Switch to consider if coal is unlimited (1), or if it is limited (0). If
        limited then the available depletion curves are considered.
    """
    return _ext_constant_unlimited_coal()


def urr_coal():
    """
    Real Name: URR coal
    Original Eqn: IF THEN ELSE("unlimited NRE?"=1 :OR: "unlimited coal?"=1, :NA:, URR coal input)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Ultimately Recoverable Resources (URR) associated to the selected
        depletion curve.
    """
    return if_then_else(
        logical_or(unlimited_nre() == 1, unlimited_coal() == 1),
        lambda: np.nan,
        lambda: urr_coal_input(),
    )


def urr_coal_input():
    """
    Real Name: URR coal input
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'URR_coal')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_urr_coal_input()


def year_scarcity_coal():
    """
    Real Name: Year scarcity coal
    Original Eqn: IF THEN ELSE(abundance coal EU>0.95, 0, Time)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_coal_eu() > 0.95, lambda: 0, lambda: time())


_integ_cumulated_coal_extraction = Integ(
    lambda: extraction_coal_ej_eu(),
    lambda: cumulated_coal_extraction_to_1995(),
    "_integ_cumulated_coal_extraction",
)


_ext_constant_cumulated_coal_extraction_to_1995 = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cumulative_coal_extraction_until_1995",
    {},
    _root,
    "_ext_constant_cumulated_coal_extraction_to_1995",
)


_integ_rurr_coal = Integ(
    lambda: -extraction_coal_ej_eu() - flow_coal_left_in_ground(),
    lambda: urr_coal() - cumulated_coal_extraction_to_1995(),
    "_integ_rurr_coal",
)


_sample_if_true_rurr_coal_start_year_plg = SampleIfTrue(
    lambda: time() < start_policy_leave_in_ground_coal(),
    lambda: rurr_coal(),
    lambda: rurr_coal(),
    "_sample_if_true_rurr_coal_start_year_plg",
)


_ext_constant_share_rurr_coal_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C131",
    {},
    _root,
    "_ext_constant_share_rurr_coal_to_leave_underground",
)


_ext_constant_start_policy_leave_in_ground_coal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "C130",
    {},
    _root,
    "_ext_constant_start_policy_leave_in_ground_coal",
)


_ext_lookup_table_max_extraction_coal = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_coal",
    "max_extraction_coal",
    {},
    _root,
    "_ext_lookup_table_max_extraction_coal",
)


_integ_total_coal_left_in_ground = Integ(
    lambda: flow_coal_left_in_ground(), lambda: 0, "_integ_total_coal_left_in_ground"
)


_ext_constant_unlimited_coal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "E99",
    {},
    _root,
    "_ext_constant_unlimited_coal",
)


_ext_constant_urr_coal_input = ExtConstant(
    "../energy.xlsx", "Europe", "URR_coal", {}, _root, "_ext_constant_urr_coal_input"
)
