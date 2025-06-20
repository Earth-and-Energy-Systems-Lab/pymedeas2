"""
Module energy.supply.ctl_and_gtl_supply
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_liquids_CTL",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs": 2, "ctl_potential_production": 1},
)
def abundance_liquids_ctl():
    """
    Variable to moderate the growth of CTL when it comes close to supply all the liquids. This variable limits the growth of a technology supplying a particular final energy type when its supply increases its share in relation to the total supply of this energy type (to avoid overshootings).
    """
    return float(
        np.sqrt(
            float(
                np.abs(
                    xidz(
                        float(ped_fs().loc["liquids"]) - ctl_potential_production(),
                        float(ped_fs().loc["liquids"]),
                        0,
                    )
                )
            )
        )
    )


@component.add(
    name="abundance_liquids_GTL",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs": 2, "gtl_potential_production": 1},
)
def abundance_liquids_gtl():
    """
    Variable to moderate the growth of GTL when it comes close to supply all the liquids. This variable limits the growth of a technology supplying a particular final energy type when its supply increases its share in relation to the total supply of this energy type (to avoid overshootings).
    """
    return float(
        np.sqrt(
            float(
                np.abs(
                    xidz(
                        float(ped_fs().loc["liquids"]) - gtl_potential_production(),
                        float(ped_fs().loc["liquids"]),
                        0,
                    )
                )
            )
        )
    )


@component.add(
    name='"Additional_PE_production_of_CTL+GTL_for_liquids"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl": 1, "ped_nat_gas_for_gtl_ej": 1, "fes_ctlgtl_ej": 1},
)
def additional_pe_production_of_ctlgtl_for_liquids():
    """
    Additional primary energy production of CTL and GTL for liquids. We need to account for this difference since the oil replaced by CTL liquids is accounted for primary energy in WoLiM, while there are additional losses to process coal to obtain CTL (required to balance the TPES with the TPED).
    """
    return ped_coal_for_ctl() + ped_nat_gas_for_gtl_ej() - fes_ctlgtl_ej()


@component.add(
    name="check_liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs": 2, "pes_fs": 1},
)
def check_liquids():
    """
    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0, demand<supply (oversupply). Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(
        float(ped_fs().loc["liquids"]) - float(pes_fs().loc["liquids"]),
        float(ped_fs().loc["liquids"]),
    )


@component.add(
    name='"constrain_liquids_exogenous_growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"check_liquids": 2},
)
def constrain_liquids_exogenous_growth():
    """
    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > 0, lambda: 1, lambda: check_liquids())


@component.add(
    name='"Crash_programme_CTL?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_crash_programme_ctl"},
)
def crash_programme_ctl():
    """
    0- Crash programme CTL NOT activated 1- Crash programme CTL activated
    """
    return _ext_constant_crash_programme_ctl()


_ext_constant_crash_programme_ctl = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "crash_programme_CTL",
    {},
    _root,
    {},
    "_ext_constant_crash_programme_ctl",
)


@component.add(
    name='"Crash_programme_GTL?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_crash_programme_gtl"},
)
def crash_programme_gtl():
    """
    0- Crash programme GTL NOT activated 1- Crash programme GTL activated
    """
    return _ext_constant_crash_programme_gtl()


_ext_constant_crash_programme_gtl = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "crash_programme_GTL",
    {},
    _root,
    {},
    "_ext_constant_crash_programme_gtl",
)


@component.add(
    name="CTL_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_ctl_efficiency"},
)
def ctl_efficiency():
    """
    Efficiency of CTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_ctl_efficiency()


_ext_constant_ctl_efficiency = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "ctl_efficiency",
    {},
    _root,
    {},
    "_ext_constant_ctl_efficiency",
)


@component.add(
    name="CTL_potential_production",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ctl_potential_production": 1},
    other_deps={
        "_integ_ctl_potential_production": {
            "initial": {"initial_ctl_production": 1},
            "step": {"replacement_ctl": 1, "variation_ctl": 1, "wear_ctl": 1},
        }
    },
)
def ctl_potential_production():
    """
    Annual CTL potential production.
    """
    return _integ_ctl_potential_production()


_integ_ctl_potential_production = Integ(
    lambda: replacement_ctl() + variation_ctl() - wear_ctl(),
    lambda: initial_ctl_production(),
    "_integ_ctl_potential_production",
)


@component.add(
    name="CTL_production",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctl_potential_production": 1, "share_ctlgtl_overcapacity": 1},
)
def ctl_production():
    """
    CTL production.
    """
    return ctl_potential_production() * (1 - share_ctlgtl_overcapacity())


@component.add(
    name='"CTL+GTL_Gb"',
    units="Gboe/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_ctlgtl_ej": 1, "gboe_per_ej": 1},
)
def ctlgtl_gb():
    """
    CTL and GTL production.
    """
    return fes_ctlgtl_ej() / gboe_per_ej()


@component.add(
    name="Exogenous_growth_CTL",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "hist_growth_ctl": 2,
        "p_ctl": 2,
        "crash_programme_ctl": 2,
        "abundance_fs": 1,
    },
)
def exogenous_growth_ctl():
    """
    If there is not scarcity of liquids, CTL production increases at historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_ctl(),
        lambda: if_then_else(
            crash_programme_ctl() == 0,
            lambda: p_ctl(),
            lambda: if_then_else(
                np.logical_and(
                    crash_programme_ctl() == 1,
                    float(abundance_fs().loc["liquids"]) >= 1,
                ),
                lambda: hist_growth_ctl(),
                lambda: p_ctl(),
            ),
        ),
    )


@component.add(
    name="Exogenous_growth_GTL",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "hist_growth_gtl": 2,
        "crash_programme_gtl": 2,
        "ped_fs": 1,
        "p_gtl": 2,
    },
)
def exogenous_growth_gtl():
    """
    If there is not scarcity of liquids, GTL production increases at historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_gtl(),
        lambda: if_then_else(
            crash_programme_gtl() == 0,
            lambda: p_gtl(),
            lambda: if_then_else(
                np.logical_and(
                    crash_programme_gtl() == 1, float(ped_fs().loc["liquids"]) >= 1
                ),
                lambda: hist_growth_gtl(),
                lambda: p_gtl(),
            ),
        ),
    )


@component.add(
    name='"FES_CTL+GTL_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_fs_liquids": 1, "potential_fes_ctlgtl": 1},
)
def fes_ctlgtl_ej():
    """
    CTL and GTL production.
    """
    return float(np.minimum(ped_nre_fs_liquids(), potential_fes_ctlgtl()))


@component.add(
    name="Gboe_per_EJ", units="EJ/Gboe", comp_type="Constant", comp_subtype="Normal"
)
def gboe_per_ej():
    """
    Unit conversion (1 EJ = 5.582 Gb).
    """
    return 5.582


@component.add(
    name="GTL_efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtl_efficiency"},
)
def gtl_efficiency():
    """
    Efficiency of GTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_gtl_efficiency()


_ext_constant_gtl_efficiency = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "gtl_efficiency",
    {},
    _root,
    {},
    "_ext_constant_gtl_efficiency",
)


@component.add(
    name="GTL_potential_production",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gtl_potential_production": 1},
    other_deps={
        "_integ_gtl_potential_production": {
            "initial": {"initial_gtl_production": 1},
            "step": {"replacement_gtl": 1, "variation_gtl": 1, "wear_gtl": 1},
        }
    },
)
def gtl_potential_production():
    """
    Annual GTL potential production.
    """
    return _integ_gtl_potential_production()


_integ_gtl_potential_production = Integ(
    lambda: replacement_gtl() + variation_gtl() - wear_gtl(),
    lambda: initial_gtl_production(),
    "_integ_gtl_potential_production",
)


@component.add(
    name="GTL_production",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gtl_potential_production": 1, "share_ctlgtl_overcapacity": 1},
)
def gtl_production():
    """
    GTL production.
    """
    return gtl_potential_production() * (1 - share_ctlgtl_overcapacity())


@component.add(
    name="Hist_growth_CTL",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_hist_growth_ctl"},
)
def hist_growth_ctl():
    """
    Historic growth of CTL 1990-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_ctl()


_ext_constant_hist_growth_ctl = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "historic_growth_ctl",
    {},
    _root,
    {},
    "_ext_constant_hist_growth_ctl",
)


@component.add(
    name="Hist_growth_GTL",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_hist_growth_gtl"},
)
def hist_growth_gtl():
    """
    Historic growth of GTL 2000-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_gtl()


_ext_constant_hist_growth_gtl = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "historic_growth_gtl",
    {},
    _root,
    {},
    "_ext_constant_hist_growth_gtl",
)


@component.add(
    name="Historic_CTL_production",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_ctl_production",
        "__lookup__": "_ext_lookup_historic_ctl_production",
    },
)
def historic_ctl_production(x, final_subs=None):
    """
    Historic generation of CTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_ctl_production(x, final_subs)


_ext_lookup_historic_ctl_production = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_ctl_production",
    {},
    _root,
    {},
    "_ext_lookup_historic_ctl_production",
)


@component.add(
    name="Historic_GTL_production",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_gtl_production",
        "__lookup__": "_ext_lookup_historic_gtl_production",
    },
)
def historic_gtl_production(x, final_subs=None):
    """
    Historic generation of GTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_gtl_production(x, final_subs)


_ext_lookup_historic_gtl_production = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_gtl_production",
    {},
    _root,
    {},
    "_ext_lookup_historic_gtl_production",
)


@component.add(
    name="initial_CTL_production",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_ctl_production"},
)
def initial_ctl_production():
    """
    CTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_ctl_production()


_ext_constant_initial_ctl_production = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "initial_ctl_production",
    {},
    _root,
    {},
    "_ext_constant_initial_ctl_production",
)


@component.add(
    name="initial_GTL_production",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_gtl_production"},
)
def initial_gtl_production():
    """
    GTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_gtl_production()


_ext_constant_initial_gtl_production = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "initial_gtl_production",
    {},
    _root,
    {},
    "_ext_constant_initial_gtl_production",
)


@component.add(
    name="lifetime_CTL",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_lifetime_ctl"},
)
def lifetime_ctl():
    """
    Lifetime of CTL plants.
    """
    return _ext_constant_lifetime_ctl()


_ext_constant_lifetime_ctl = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "lifetime_ctl",
    {},
    _root,
    {},
    "_ext_constant_lifetime_ctl",
)


@component.add(
    name="lifetime_GTL",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_lifetime_gtl"},
)
def lifetime_gtl():
    """
    Lifetime of GTL plants.
    """
    return _ext_constant_lifetime_gtl()


_ext_constant_lifetime_gtl = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "lifetime_gtl",
    {},
    _root,
    {},
    "_ext_constant_lifetime_gtl",
)


@component.add(
    name="P_CTL",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_ctl"},
)
def p_ctl():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_ctl()


_ext_constant_p_ctl = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_CTL_growth",
    {},
    _root,
    {},
    "_ext_constant_p_ctl",
)


@component.add(
    name="P_GTL",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_gtl"},
)
def p_gtl():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_gtl()


_ext_constant_p_gtl = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_GTL_growth",
    {},
    _root,
    {},
    "_ext_constant_p_gtl",
)


@component.add(
    name="PED_coal_for_CTL",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctl_production": 1, "ctl_efficiency": 1},
)
def ped_coal_for_ctl():
    """
    Demand of coal for CTL.
    """
    return ctl_production() / ctl_efficiency()


@component.add(
    name='"PED_nat._gas_for_GTL_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gtl_production": 1, "gtl_efficiency": 1},
)
def ped_nat_gas_for_gtl_ej():
    """
    Demand of gas for CTL.
    """
    return gtl_production() / gtl_efficiency()


@component.add(
    name='"Potential_FES_CTL+GTL"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ctl_potential_production": 1, "gtl_potential_production": 1},
)
def potential_fes_ctlgtl():
    return ctl_potential_production() + gtl_potential_production()


@component.add(
    name="real_growth_CTL",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "abundance_coal_eu": 2,
        "abundance_fs": 1,
        "exogenous_growth_ctl": 1,
        "abundance_liquids_ctl": 1,
        "scarcity_conv_oil": 1,
    },
)
def real_growth_ctl():
    """
    The real growth of CTL depends on the relative abundance of coal and liquids, as well as on the availability of coal.
    """
    return (
        if_then_else(
            abundance_coal_eu() >= float(abundance_fs().loc["liquids"]),
            lambda: if_then_else(
                abundance_coal_eu() == 1, lambda: exogenous_growth_ctl(), lambda: 0
            ),
            lambda: 0,
        )
        * abundance_liquids_ctl()
        * scarcity_conv_oil()
    )


@component.add(
    name="real_growth_GTL",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "abundance_fs": 3,
        "exogenous_growth_gtl": 1,
        "abundance_liquids_gtl": 1,
        "scarcity_conv_oil": 1,
    },
)
def real_growth_gtl():
    """
    The real growth of GTL depends on the relative abundance of gas and liquids, as well as on the availability of gas.
    """
    return (
        if_then_else(
            float(abundance_fs().loc["gases"]) >= float(abundance_fs().loc["liquids"]),
            lambda: if_then_else(
                float(abundance_fs().loc["gases"]) == 1,
                lambda: exogenous_growth_gtl(),
                lambda: 0,
            ),
            lambda: 0,
        )
        * abundance_liquids_gtl()
        * scarcity_conv_oil()
    )


@component.add(
    name="replacement_CTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "check_liquids": 1,
        "crash_programme_ctl": 1,
        "wear_ctl": 2,
        "constrain_liquids_exogenous_growth": 1,
        "scarcity_conv_oil": 1,
    },
)
def replacement_ctl():
    """
    Replacement of CTL.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: 0,
            lambda: if_then_else(
                crash_programme_ctl() == 0,
                lambda: 0,
                lambda: if_then_else(
                    check_liquids() < 0,
                    lambda: constrain_liquids_exogenous_growth() * wear_ctl(),
                    lambda: wear_ctl(),
                ),
            ),
        )
        * scarcity_conv_oil()
    )


@component.add(
    name="replacement_GTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "crash_programme_gtl": 1,
        "check_liquids": 1,
        "constrain_liquids_exogenous_growth": 1,
        "wear_gtl": 2,
        "scarcity_conv_oil": 1,
    },
)
def replacement_gtl():
    """
    Replacement of GTL.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: 0,
            lambda: if_then_else(
                crash_programme_gtl() == 0,
                lambda: 0,
                lambda: if_then_else(
                    check_liquids() < 0,
                    lambda: constrain_liquids_exogenous_growth() * wear_gtl(),
                    lambda: wear_gtl(),
                ),
            ),
        )
        * scarcity_conv_oil()
    )


@component.add(
    name='"share_CTL+GTL_overcapacity"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_ctlgtl": 2, "fes_ctlgtl_ej": 1},
)
def share_ctlgtl_overcapacity():
    return zidz(potential_fes_ctlgtl() - fes_ctlgtl_ej(), potential_fes_ctlgtl())


@component.add(
    name="variation_CTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_ctl_production": 2,
        "time_step": 2,
        "constrain_liquids_exogenous_growth": 1,
        "nvs_1_year": 1,
        "ctl_potential_production": 2,
        "check_liquids": 1,
        "real_growth_ctl": 1,
    },
)
def variation_ctl():
    """
    New annual CTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_ctl_production(time() + time_step())
            - historic_ctl_production(time())
        )
        / time_step(),
        lambda: if_then_else(
            check_liquids() < 0,
            lambda: constrain_liquids_exogenous_growth()
            * ctl_potential_production()
            / nvs_1_year(),
            lambda: ctl_potential_production() * real_growth_ctl(),
        ),
    )


@component.add(
    name="variation_GTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_gtl_production": 2,
        "time_step": 2,
        "real_growth_gtl": 1,
        "constrain_liquids_exogenous_growth": 1,
        "gtl_potential_production": 2,
        "nvs_1_year": 1,
        "check_liquids": 1,
    },
)
def variation_gtl():
    """
    New annual GTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_gtl_production(time() + time_step())
            - historic_gtl_production(time())
        )
        / time_step(),
        lambda: if_then_else(
            check_liquids() < 0,
            lambda: constrain_liquids_exogenous_growth()
            * gtl_potential_production()
            / nvs_1_year(),
            lambda: gtl_potential_production() * real_growth_gtl(),
        ),
    )


@component.add(
    name="wear_CTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "ctl_potential_production": 1, "lifetime_ctl": 1},
)
def wear_ctl():
    """
    Depreciation of CTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: ctl_potential_production() / lifetime_ctl()
    )


@component.add(
    name="wear_GTL",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "lifetime_gtl": 1, "gtl_potential_production": 1},
)
def wear_gtl():
    """
    Depreciation of GTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: gtl_potential_production() / lifetime_gtl()
    )
