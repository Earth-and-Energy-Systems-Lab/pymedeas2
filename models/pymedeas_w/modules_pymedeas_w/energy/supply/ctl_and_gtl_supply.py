"""
Module ctl_and_gtl_supply
Translated using PySD version 2.2.3
"""


def abundance_liquids_ctl():
    """
    Real Name: abundance liquids CTL
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variable to moderate the growth of CTL when it comes close to supply all the liquids. This variable limits the growth of a technology supplying a particular final energy type when its supply increases its share in relation to the total supply of this energy type (to avoid overshootings).
    """
    return np.sqrt(
        np.abs((ped_liquids_ej() - ctl_potential_production()) / ped_liquids_ej())
    )


def abundance_liquids_gtl():
    """
    Real Name: abundance liquids GTL
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variable to moderate the growth of GTL when it comes close to supply all the liquids. This variable limits the growth of a technology supplying a particular final energy type when its supply increases its share in relation to the total supply of this energy type (to avoid overshootings).
    """
    return np.sqrt(
        np.abs((ped_liquids_ej() - gtl_potential_production()) / ped_liquids_ej())
    )


def additional_pe_production_of_ctlgtl_for_liquids():
    """
    Real Name: "Additional PE production of CTL+GTL for liquids"
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Additional primary energy production of CTL and GTL for liquids. We need to account for this difference since the oil replaced by CTL liquids is accounted for primary energy in WoLiM, while there are additional losses to process coal to obtain CTL (required to balance the TPES with the TPED).
    """
    return ped_coal_for_ctl_ej() + ped_nat_gas_for_gtl_ej() - fes_ctlgtl_ej()


def crash_programme_ctl():
    """
    Real Name: "Crash programme CTL?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0- Crash programme CTL NOT activated 1- Crash programme CTL activated
    """
    return _ext_constant_crash_programme_ctl()


_ext_constant_crash_programme_ctl = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "crash_programme_CTL",
    {},
    _root,
    "_ext_constant_crash_programme_ctl",
)


def crash_programme_gtl():
    """
    Real Name: "Crash programme GTL?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0- Crash programme GTL NOT activated 1- Crash programme GTL activated
    """
    return _ext_constant_crash_programme_gtl()


_ext_constant_crash_programme_gtl = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "crash_programme_GTL",
    {},
    _root,
    "_ext_constant_crash_programme_gtl",
)


def ctl_efficiency():
    """
    Real Name: CTL efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of CTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_ctl_efficiency()


_ext_constant_ctl_efficiency = ExtConstant(
    "../energy.xlsx",
    "Global",
    "ctl_efficiency",
    {},
    _root,
    "_ext_constant_ctl_efficiency",
)


def ctl_potential_production():
    """
    Real Name: CTL potential production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Annual CTL potential production.
    """
    return _integ_ctl_potential_production()


_integ_ctl_potential_production = Integ(
    lambda: replacement_ctl() + variation_ctl() - wear_ctl(),
    lambda: initial_ctl_production(),
    "_integ_ctl_potential_production",
)


def ctl_production():
    """
    Real Name: CTL production
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    CTL production.
    """
    return ctl_potential_production() * (1 - share_ctlgtl_overcapacity())


def ctlgtl_gb():
    """
    Real Name: "CTL+GTL Gb"
    Original Eqn:
    Units: Gboe/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    CTL and GTL production.
    """
    return fes_ctlgtl_ej() / gboe_per_ej()


def exogenous_growth_ctl():
    """
    Real Name: Exogenous growth CTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If there is not scarcity of liquids, CTL production increases at historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_ctl(),
        lambda: if_then_else(
            crash_programme_ctl() == 0,
            lambda: p_ctl(),
            lambda: if_then_else(
                np.logical_and(crash_programme_ctl() == 1, abundance_liquids() >= 1),
                lambda: hist_growth_ctl(),
                lambda: p_ctl(),
            ),
        ),
    )


def exogenous_growth_gtl():
    """
    Real Name: Exogenous growth GTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If there is not scarcity of liquids, GTL production increases at historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_gtl(),
        lambda: if_then_else(
            crash_programme_gtl() == 0,
            lambda: p_gtl(),
            lambda: if_then_else(
                np.logical_and(crash_programme_gtl() == 1, abundance_liquids() >= 1),
                lambda: hist_growth_gtl(),
                lambda: p_gtl(),
            ),
        ),
    )


def fes_ctlgtl_ej():
    """
    Real Name: "FES CTL+GTL EJ"
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    CTL and GTL production.
    """
    return np.minimum(ped_nre_liquids(), potential_fes_ctlgtl_ej())


def gboe_per_ej():
    """
    Real Name: Gboe per EJ
    Original Eqn:
    Units: EJ/Gboe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Unit conversion (1 EJ = 5.582 Gb).
    """
    return 5.582


def gtl_efficiency():
    """
    Real Name: GTL efficiency
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of GTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_gtl_efficiency()


_ext_constant_gtl_efficiency = ExtConstant(
    "../energy.xlsx",
    "Global",
    "gtl_efficiency",
    {},
    _root,
    "_ext_constant_gtl_efficiency",
)


def gtl_potential_production():
    """
    Real Name: GTL potential production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Annual GTL potential production.
    """
    return _integ_gtl_potential_production()


_integ_gtl_potential_production = Integ(
    lambda: replacement_gtl() + variation_gtl() - wear_gtl(),
    lambda: initial_gtl_production(),
    "_integ_gtl_potential_production",
)


def gtl_production():
    """
    Real Name: GTL production
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    GTL production.
    """
    return gtl_potential_production() * (1 - share_ctlgtl_overcapacity())


def hist_growth_ctl():
    """
    Real Name: Hist growth CTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic growth of CTL 1990-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_ctl()


_ext_constant_hist_growth_ctl = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_ctl",
    {},
    _root,
    "_ext_constant_hist_growth_ctl",
)


def hist_growth_gtl():
    """
    Real Name: Hist growth GTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic growth of GTL 2000-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_gtl()


_ext_constant_hist_growth_gtl = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_gtl",
    {},
    _root,
    "_ext_constant_hist_growth_gtl",
)


def historic_ctl_production(x):
    """
    Real Name: Historic CTL production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic generation of CTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_ctl_production(x)


_ext_lookup_historic_ctl_production = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_ctl_production",
    {},
    _root,
    "_ext_lookup_historic_ctl_production",
)


def historic_gtl_production(x):
    """
    Real Name: historic GTL production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic generation of GTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_gtl_production(x)


_ext_lookup_historic_gtl_production = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_gtl_production",
    {},
    _root,
    "_ext_lookup_historic_gtl_production",
)


def initial_ctl_production():
    """
    Real Name: initial CTL production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    CTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_ctl_production()


_ext_constant_initial_ctl_production = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_ctl_production",
    {},
    _root,
    "_ext_constant_initial_ctl_production",
)


def initial_gtl_production():
    """
    Real Name: initial GTL production
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    GTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_gtl_production()


_ext_constant_initial_gtl_production = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_gtl_production",
    {},
    _root,
    "_ext_constant_initial_gtl_production",
)


def lifetime_ctl():
    """
    Real Name: lifetime CTL
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Lifetime of CTL plants.
    """
    return _ext_constant_lifetime_ctl()


_ext_constant_lifetime_ctl = ExtConstant(
    "../energy.xlsx", "Global", "lifetime_ctl", {}, _root, "_ext_constant_lifetime_ctl"
)


def lifetime_gtl():
    """
    Real Name: lifetime GTL
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Lifetime of GTL plants.
    """
    return _ext_constant_lifetime_gtl()


_ext_constant_lifetime_gtl = ExtConstant(
    "../energy.xlsx", "Global", "lifetime_gtl", {}, _root, "_ext_constant_lifetime_gtl"
)


def p_ctl():
    """
    Real Name: P CTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_ctl()


_ext_constant_p_ctl = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_CTL_annual_growth",
    {},
    _root,
    "_ext_constant_p_ctl",
)


def p_gtl():
    """
    Real Name: P GTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_gtl()


_ext_constant_p_gtl = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_gtl_growth",
    {},
    _root,
    "_ext_constant_p_gtl",
)


def ped_coal_for_ctl_ej():
    """
    Real Name: PED coal for CTL EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of coal for CTL.
    """
    return ctl_production() / ctl_efficiency()


def ped_nat_gas_for_gtl_ej():
    """
    Real Name: "PED nat. gas for GTL EJ"
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Demand of gas for CTL.
    """
    return gtl_production() / gtl_efficiency()


def potential_fes_ctlgtl_ej():
    """
    Real Name: "Potential FES CTL+GTL EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return ctl_potential_production() + gtl_potential_production()


def real_growth_ctl():
    """
    Real Name: real growth CTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The real growth of CTL depends on the relative abundance of coal and liquids, as well as on the availability of coal.
    """
    return (
        if_then_else(
            abundance_coal() >= abundance_liquids(),
            lambda: if_then_else(
                abundance_coal() == 1, lambda: exogenous_growth_ctl(), lambda: 0
            ),
            lambda: 0,
        )
        * abundance_liquids_ctl()
        * scarcity_conv_oil()
    )


def real_growth_gtl():
    """
    Real Name: real growth GTL
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The real growth of GTL depends on the relative abundance of gas and liquids, as well as on the availability of gas.
    """
    return (
        if_then_else(
            abundance_gases() >= abundance_liquids(),
            lambda: if_then_else(
                abundance_gases() == 1, lambda: exogenous_growth_gtl(), lambda: 0
            ),
            lambda: 0,
        )
        * abundance_liquids_gtl()
        * scarcity_conv_oil()
    )


def replacement_ctl():
    """
    Real Name: replacement CTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
                    check_liquids() < -0.0001,
                    lambda: constrain_liquids_exogenous_growth() * wear_ctl(),
                    lambda: wear_ctl(),
                ),
            ),
        )
        * scarcity_conv_oil()
    )


def replacement_gtl():
    """
    Real Name: replacement GTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
                    check_liquids() < -0.0001,
                    lambda: constrain_liquids_exogenous_growth() * wear_gtl(),
                    lambda: wear_gtl(),
                ),
            ),
        )
        * scarcity_conv_oil()
    )


def share_ctlgtl_overcapacity():
    """
    Real Name: "share CTL+GTL overcapacity"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(potential_fes_ctlgtl_ej() - fes_ctlgtl_ej(), potential_fes_ctlgtl_ej())


def variation_ctl():
    """
    Real Name: variation CTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New annual CTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: historic_ctl_production(time() + 1) - historic_ctl_production(time()),
        lambda: if_then_else(
            check_liquids() < -0.0001,
            lambda: constrain_liquids_exogenous_growth() * ctl_potential_production(),
            lambda: ctl_potential_production() * real_growth_ctl(),
        ),
    )


def variation_gtl():
    """
    Real Name: variation GTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New annual GTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: historic_gtl_production(time() + 1) - historic_gtl_production(time()),
        lambda: if_then_else(
            check_liquids() < -0.0001,
            lambda: constrain_liquids_exogenous_growth() * gtl_potential_production(),
            lambda: gtl_potential_production() * real_growth_gtl(),
        ),
    )


def wear_ctl():
    """
    Real Name: wear CTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Depreciation of CTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: ctl_potential_production() / lifetime_ctl()
    )


def wear_gtl():
    """
    Real Name: wear GTL
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Depreciation of GTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: gtl_potential_production() / lifetime_gtl()
    )
