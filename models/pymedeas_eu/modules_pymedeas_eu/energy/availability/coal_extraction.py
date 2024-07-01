"""
Module energy.availability.coal_extraction
Translated using PySD version 3.14.0
"""

@component.add(
    name="abundance_coal_EU",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_eu": 2,
        "imports_eu_coal_from_row_ej": 2,
        "ped_nre_fs": 3,
    },
)
def abundance_coal_eu():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        extraction_coal_eu() + imports_eu_coal_from_row_ej()
        > float(ped_nre_fs().loc["solids"]),
        lambda: 1,
        lambda: 1
        - zidz(
            float(ped_nre_fs().loc["solids"])
            - extraction_coal_eu()
            - imports_eu_coal_from_row_ej(),
            float(ped_nre_fs().loc["solids"]),
        ),
    )


@component.add(
    name="Activate_force_leaving_underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_force_leaving_underground"},
)
def activate_force_leaving_underground():
    """
    Switch to force if the share of RURRs to leave underground must be blocked or not. If not blocked, it serves as an indicator (for example, an indicator of the time when the extractable resources that are compatible with the Paris Agreement have already been exctracted).Options: 0 - No (Do not force) 1 - Yes (Force)
    """
    return _ext_constant_activate_force_leaving_underground()


_ext_constant_activate_force_leaving_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "activate_policy_leaving_underground",
    {},
    _root,
    {},
    "_ext_constant_activate_force_leaving_underground",
)


@component.add(
    name="coal_to_leave_underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_rurr_coal_to_leave_underground": 1,
        "rurr_coal_in_reference_year": 1,
    },
)
def coal_to_leave_underground():
    """
    Coal to be left underground due to the application of policies that leave coal underground.
    """
    return share_rurr_coal_to_leave_underground() * rurr_coal_in_reference_year()


@component.add(
    name="consumption_UE_coal_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_ff": 1, "nonenergy_use_demand_by_final_fuel": 1},
)
def consumption_ue_coal_emissions_relevant_ej():
    """
    Consumption of emission-relevant coal, i.e. excepting the resource used for non-energy uses.
    """
    return np.maximum(
        0,
        float(pec_ff().loc["solids"])
        - float(nonenergy_use_demand_by_final_fuel().loc["solids"]),
    )


@component.add(
    name="Cumulated_coal_extraction",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulated_coal_extraction": 1},
    other_deps={
        "_integ_cumulated_coal_extraction": {
            "initial": {"cumulated_coal_extraction_to_1995": 1},
            "step": {"extraction_coal_eu": 1},
        }
    },
)
def cumulated_coal_extraction():
    """
    Cumulated coal extraction.
    """
    return _integ_cumulated_coal_extraction()


_integ_cumulated_coal_extraction = Integ(
    lambda: extraction_coal_eu(),
    lambda: cumulated_coal_extraction_to_1995(),
    "_integ_cumulated_coal_extraction",
)


@component.add(
    name="cumulated_coal_extraction_to_1995",
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
    "Europe",
    "cumulative_coal_extraction_until_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulated_coal_extraction_to_1995",
)


@component.add(
    name="delay_coal_to_leave_underground",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_delay_coal_to_leave_underground": 1},
    other_deps={
        "_sampleiftrue_delay_coal_to_leave_underground": {
            "initial": {},
            "step": {
                "time": 1,
                "start_year_policy_leave_in_ground_coal": 1,
                "coal_to_leave_underground": 1,
            },
        }
    },
)
def delay_coal_to_leave_underground():
    """
    This function is used so that the amount of coal to be left underground is substracted from the (technological) RURR from the Start year to leave coal undeground onwards.
    """
    return _sampleiftrue_delay_coal_to_leave_underground()


_sampleiftrue_delay_coal_to_leave_underground = SampleIfTrue(
    lambda: time() == start_year_policy_leave_in_ground_coal(),
    lambda: coal_to_leave_underground(),
    lambda: 0,
    "_sampleiftrue_delay_coal_to_leave_underground",
)


@component.add(
    name="evol_extraction_rate_constraint",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "year_to_end_coal_extraction": 2, "extraction_coal_eu": 1},
)
def evol_extraction_rate_constraint():
    """
    Slope of linear fit to limit extraction from current extraction to zero,where the are under the curve is the remainig extractable resources to comply with leave in ground targets.
    """
    return if_then_else(
        time() < year_to_end_coal_extraction(),
        lambda: -extraction_coal_eu() / (year_to_end_coal_extraction() - time()),
        lambda: 0,
    )


@component.add(
    name="evol_extraction_rate_delayed",
    units="EJ/(year*year)",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_evol_extraction_rate_delayed": 1},
    other_deps={
        "_delayfixed_evol_extraction_rate_delayed": {
            "initial": {"time_step": 1},
            "step": {"evol_extraction_rate_constraint": 1},
        }
    },
)
def evol_extraction_rate_delayed():
    """
    Slope of linear fit to limit extraction from current extraction to zero,where the are under the curve is the remainig extractable resources to comply with leave in ground targets. Delayed one time step.
    """
    return _delayfixed_evol_extraction_rate_delayed()


_delayfixed_evol_extraction_rate_delayed = DelayFixed(
    lambda: evol_extraction_rate_constraint(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_evol_extraction_rate_delayed",
)


@component.add(
    name="extraction_coal_emissions_relevant_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_without_ctl_ej": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def extraction_coal_emissions_relevant_ej():
    """
    Extraction of emission-relevant coal, i.e. excepting the resource used for non-energy uses.
    """
    return np.maximum(
        0,
        extraction_coal_without_ctl_ej()
        - float(nonenergy_use_demand_by_final_fuel().loc["solids"]),
    )


@component.add(
    name="extraction_coal_EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ped_domestic_ff": 3,
        "nvs_1_year": 1,
        "max_extraction_coal": 2,
        "activate_force_leaving_underground": 1,
        "remaining_extractable_coal_with_left_underground": 1,
    },
)
def extraction_coal_eu():
    """
    Annual extraction of coal.
    """
    return if_then_else(
        time() < 2016,
        lambda: float(ped_domestic_ff().loc["solids"]),
        lambda: if_then_else(
            activate_force_leaving_underground() == 0,
            lambda: np.minimum(
                float(ped_domestic_ff().loc["solids"]), max_extraction_coal()
            ),
            lambda: np.minimum(
                np.minimum(
                    float(ped_domestic_ff().loc["solids"]), max_extraction_coal()
                ),
                remaining_extractable_coal_with_left_underground() / nvs_1_year(),
            ),
        ),
    )


@component.add(
    name="extraction_coal_EU_delayed",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_extraction_coal_eu_delayed": 1},
    other_deps={
        "_delayfixed_extraction_coal_eu_delayed": {
            "initial": {"time_step": 1},
            "step": {"extraction_coal_eu": 1},
        }
    },
)
def extraction_coal_eu_delayed():
    """
    Annual extraction of coal delayed one year. The delay allows to progressively limit extraction of coal (due to leave underground policies) using previous extraction rates.
    """
    return _delayfixed_extraction_coal_eu_delayed()


_delayfixed_extraction_coal_eu_delayed = DelayFixed(
    lambda: extraction_coal_eu(),
    lambda: time_step(),
    lambda: 1,
    time_step,
    "_delayfixed_extraction_coal_eu_delayed",
)


@component.add(
    name="extraction_coal_for_CTL_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl": 1},
)
def extraction_coal_for_ctl_ej():
    """
    Extraction of coal for CTL. CTL demand is given priority over other uses since it is an exogenous assumption depending on the scenario.
    """
    return ped_coal_for_ctl()


@component.add(
    name="extraction_coal_without_CTL_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_eu": 1, "extraction_coal_for_ctl_ej": 1},
)
def extraction_coal_without_ctl_ej():
    """
    Extraction of conventional gas excepting the resource used to produce GTL.
    """
    return np.maximum(extraction_coal_eu() - extraction_coal_for_ctl_ej(), 0)


@component.add(
    name="max_extraction_coal",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_force_leaving_underground": 1,
        "max_extraction_coal_technical": 3,
        "start_year_policy_leave_in_ground_coal": 1,
        "time": 1,
        "max_extraction_coal_policy": 1,
    },
)
def max_extraction_coal():
    """
    Maximum ectraction of coal due to technical reasons (Hubbert) and, if applies, leave underground policy.
    """
    return if_then_else(
        activate_force_leaving_underground() == 0,
        lambda: max_extraction_coal_technical(),
        lambda: if_then_else(
            time() > start_year_policy_leave_in_ground_coal(),
            lambda: np.minimum(
                max_extraction_coal_technical(), max_extraction_coal_policy()
            ),
            lambda: max_extraction_coal_technical(),
        ),
    )


@component.add(
    name="max_extraction_coal_policy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "evol_extraction_rate_delayed": 1,
        "time_step": 1,
        "extraction_coal_eu_delayed": 1,
    },
)
def max_extraction_coal_policy():
    """
    Maximum extraction of coal allowed by leave underground policy (progressive linear decrease assumed).
    """
    return np.maximum(
        0, evol_extraction_rate_delayed() * time_step() + extraction_coal_eu_delayed()
    )


@component.add(
    name="max_extraction_coal_technical",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_coal": 1, "table_max_extraction_coal": 1},
)
def max_extraction_coal_technical():
    """
    Maximum extraction of coal due to technical constraints (Hubbert).
    """
    return table_max_extraction_coal(rurr_coal())


@component.add(
    name="PED_coal_without_CTL",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_fs": 1, "ped_coal_for_ctl": 1},
)
def ped_coal_without_ctl():
    """
    Total demand of coal without CTL.
    """
    return float(ped_nre_fs().loc["solids"]) - ped_coal_for_ctl()


@component.add(
    name="remaining_extractable_coal_with_left_underground",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rurr_coal": 1, "delay_coal_to_leave_underground": 1},
)
def remaining_extractable_coal_with_left_underground():
    """
    Remaining extractable resources, after substracting the amount that must be left underground to comply with policy targets.
    """
    return np.maximum(0, rurr_coal() - delay_coal_to_leave_underground())


@component.add(
    name="RURR_coal",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rurr_coal": 1},
    other_deps={
        "_integ_rurr_coal": {
            "initial": {"urr_coal": 1, "cumulated_coal_extraction_to_1995": 1},
            "step": {"extraction_coal_eu": 1},
        }
    },
)
def rurr_coal():
    """
    Remaining Ultimate Recoverable Resources (RURR) of coal. This is the techno-economically remaining extractable resource: corresponds to the difference between the tecnho Remaining Ultimate Recoverable Resources and the coal that has already been extracted.
    """
    return _integ_rurr_coal()


_integ_rurr_coal = Integ(
    lambda: -extraction_coal_eu(),
    lambda: urr_coal() - cumulated_coal_extraction_to_1995(),
    "_integ_rurr_coal",
)


@component.add(
    name="RURR_coal_in_reference_year",
    units="EJ",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_rurr_coal_in_reference_year": 1},
    other_deps={
        "_sampleiftrue_rurr_coal_in_reference_year": {
            "initial": {},
            "step": {"time": 1, "year_reference_rurr": 1, "rurr_coal": 1},
        }
    },
)
def rurr_coal_in_reference_year():
    """
    RURR in the year used to calculate the share to leave underground under the policy to leave in the ground the resource.
    """
    return _sampleiftrue_rurr_coal_in_reference_year()


_sampleiftrue_rurr_coal_in_reference_year = SampleIfTrue(
    lambda: time() == year_reference_rurr(),
    lambda: rurr_coal(),
    lambda: 0,
    "_sampleiftrue_rurr_coal_in_reference_year",
)


@component.add(
    name="share_RURR_coal_to_leave_underground",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_rurr_coal_to_leave_underground"},
)
def share_rurr_coal_to_leave_underground():
    """
    RURR's coal to be left in the ground as a share of the RURR in the reference year.
    """
    return _ext_constant_share_rurr_coal_to_leave_underground()


_ext_constant_share_rurr_coal_to_leave_underground = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "share_RURR_coal_underground",
    {},
    _root,
    {},
    "_ext_constant_share_rurr_coal_to_leave_underground",
)


@component.add(
    name='"share_to_leave_underground_feasible?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "year_to_end_coal_extraction": 1},
)
def share_to_leave_underground_feasible():
    """
    Control variable: 0- No 1- Yes
    """
    return if_then_else(time() > year_to_end_coal_extraction(), lambda: 0, lambda: 1)


@component.add(
    name="Start_year_policy_leave_in_ground_coal",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_policy_leave_in_ground_coal"},
)
def start_year_policy_leave_in_ground_coal():
    """
    Year when the policy to progressively leave coal in the ground enters into force.
    """
    return _ext_constant_start_year_policy_leave_in_ground_coal()


_ext_constant_start_year_policy_leave_in_ground_coal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_coal_underground",
    {},
    _root,
    {},
    "_ext_constant_start_year_policy_leave_in_ground_coal",
)


@component.add(
    name="table_max_extraction_coal",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_max_extraction_coal",
        "__lookup__": "_ext_lookup_table_max_extraction_coal",
    },
)
def table_max_extraction_coal(x, final_subs=None):
    """
    Data tables with maximum extraction of coal due to technical constraints (Hubbert).
    """
    return _ext_lookup_table_max_extraction_coal(x, final_subs)


_ext_lookup_table_max_extraction_coal = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "RURR_coal",
    "max_extraction_coal",
    {},
    _root,
    {},
    "_ext_lookup_table_max_extraction_coal",
)


@component.add(
    name="URR_coal",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urr_coal"},
)
def urr_coal():
    """
    Ultimately Recoverable Resources (URR) associated to the selected depletion curve.
    """
    return _ext_constant_urr_coal()


_ext_constant_urr_coal = ExtConstant(
    "../energy.xlsx", "Europe", "URR_coal", {}, _root, {}, "_ext_constant_urr_coal"
)


@component.add(
    name="Year_reference_RURR",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_year_reference_rurr"},
)
def year_reference_rurr():
    """
    Year to use as a reference for calculating the share of RURRs to be left underground.
    """
    return _ext_constant_year_reference_rurr()


_ext_constant_year_reference_rurr = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_ref_RURR",
    {},
    _root,
    {},
    "_ext_constant_year_reference_rurr",
)


@component.add(
    name="Year_scarcity_coal",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_coal_eu": 1, "time": 1},
)
def year_scarcity_coal():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_coal_eu() > 0.95, lambda: 0, lambda: time())


@component.add(
    name="year_to_end_coal_extraction",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_eu": 2,
        "rurr_coal": 1,
        "time": 1,
        "remaining_extractable_coal_with_left_underground": 1,
    },
)
def year_to_end_coal_extraction():
    """
    Year when coal extraction has to end in order to comply with leave in ground policy. This year is dinamically determined, according to the actual extraction rate.
    """
    return if_then_else(
        np.logical_or(extraction_coal_eu() <= 0, rurr_coal() <= 0),
        lambda: 0,
        lambda: 2
        * remaining_extractable_coal_with_left_underground()
        / extraction_coal_eu()
        + time(),
    )
