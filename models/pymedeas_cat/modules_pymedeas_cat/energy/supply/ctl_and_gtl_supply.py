"""
Module ctl_and_gtl_supply
Translated using PySD version 2.2.0
"""


def abundance_liquids_ctl():
    """
    Real Name: abundance liquids CTL
    Original Eqn: SQRT(ABS((XIDZ( PED liquids EJ-CTL potential production, PED liquids EJ, 0))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Variable to moderate the growth of CTL when it comes close to supply all
        the liquids. This variable limits the growth of a technology supplying a
        particular final energy type when its supply increases its share in
        relation to the total supply of this energy type (to avoid overshootings).
    """
    return np.sqrt(
        np.abs(
            (xidz(ped_liquids_ej() - ctl_potential_production(), ped_liquids_ej(), 0))
        )
    )


def abundance_liquids_gtl():
    """
    Real Name: abundance liquids GTL
    Original Eqn: SQRT(ABS((XIDZ( PED liquids EJ-GTL potential production, PED liquids EJ,0))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Variable to moderate the growth of GTL when it comes close to supply all
        the liquids. This variable limits the growth of a technology supplying a
        particular final energy type when its supply increases its share in
        relation to the total supply of this energy type (to avoid overshootings).
    """
    return np.sqrt(
        np.abs(
            (xidz(ped_liquids_ej() - gtl_potential_production(), ped_liquids_ej(), 0))
        )
    )


def additional_pe_production_of_ctlgtl_for_liquids():
    """
    Real Name: "Additional PE production of CTL+GTL for liquids"
    Original Eqn: PED coal for CTL EJ+"PED nat. gas for GTL EJ"-"FES CTL+GTL EJ"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Additional primary energy production of CTL and GTL for liquids. We need
        to account for this difference since the oil replaced by CTL liquids is
        accounted for primary energy in WoLiM, while there are additional losses
        to process coal to obtain CTL (required to balance the TPES with the TPED).
    """
    return ped_coal_for_ctl_ej() + ped_nat_gas_for_gtl_ej() - fes_ctlgtl_ej()


def crash_programme_ctl():
    """
    Real Name: "Crash programme CTL?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'D110')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0- Crash programme CTL NOT activated        1- Crash programme CTL activated
    """
    return _ext_constant_crash_programme_ctl()


def crash_programme_gtl():
    """
    Real Name: "Crash programme GTL?"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'D112')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0- Crash programme GTL NOT activated        1- Crash programme GTL activated
    """
    return _ext_constant_crash_programme_gtl()


def ctl_efficiency():
    """
    Real Name: CTL efficiency
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'ctl_efficiency')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of CTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_ctl_efficiency()


def ctl_potential_production():
    """
    Real Name: CTL potential production
    Original Eqn: INTEG ( replacement CTL+variation CTL-wear CTL, initial CTL production)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual CTL potential production.
    """
    return _integ_ctl_potential_production()


def ctl_production():
    """
    Real Name: CTL production
    Original Eqn: CTL potential production*(1-"share CTL+GTL overcapacity")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    CTL production.
    """
    return ctl_potential_production() * (1 - share_ctlgtl_overcapacity())


def ctlgtl_gb():
    """
    Real Name: "CTL+GTL Gb"
    Original Eqn: "FES CTL+GTL EJ"/Gboe per EJ
    Units: Gboe/Year
    Limits: (None, None)
    Type: component
    Subs: None

    CTL and GTL production.
    """
    return fes_ctlgtl_ej() / gboe_per_ej()


def exogenous_growth_ctl():
    """
    Real Name: Exogenous growth CTL
    Original Eqn: IF THEN ELSE(Time<2015, Hist growth CTL, IF THEN ELSE("Crash programme CTL?"=0,P CTL, IF THEN ELSE("Crash programme CTL?"=1 :AND: abundance liquids>=1, Hist growth CTL, P CTL)))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    If there is not scarcity of liquids, CTL production increases at
        historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_ctl(),
        lambda: if_then_else(
            crash_programme_ctl() == 0,
            lambda: p_ctl(),
            lambda: if_then_else(
                logical_and(crash_programme_ctl() == 1, abundance_liquids() >= 1),
                lambda: hist_growth_ctl(),
                lambda: p_ctl(),
            ),
        ),
    )


def exogenous_growth_gtl():
    """
    Real Name: Exogenous growth GTL
    Original Eqn: IF THEN ELSE(Time<2015, Hist growth GTL, IF THEN ELSE("Crash programme GTL?"=0,P GTL, IF THEN ELSE("Crash programme GTL?"=1 :AND: abundance liquids>=1, Hist growth GTL, P GTL)))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    If there is not scarcity of liquids, GTL production increases at
        historical past rates.
    """
    return if_then_else(
        time() < 2015,
        lambda: hist_growth_gtl(),
        lambda: if_then_else(
            crash_programme_gtl() == 0,
            lambda: p_gtl(),
            lambda: if_then_else(
                logical_and(crash_programme_gtl() == 1, abundance_liquids() >= 1),
                lambda: hist_growth_gtl(),
                lambda: p_gtl(),
            ),
        ),
    )


def fes_ctlgtl_ej():
    """
    Real Name: "FES CTL+GTL EJ"
    Original Eqn: MIN(PED NRE Liquids, "Potential FES CTL+GTL EJ")
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    CTL and GTL production.
    """
    return np.minimum(ped_nre_liquids(), potential_fes_ctlgtl_ej())


def gboe_per_ej():
    """
    Real Name: Gboe per EJ
    Original Eqn: 5.582
    Units: EJ/Gboe
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion (1 EJ = 5.582 Gb).
    """
    return 5.582


def gtl_efficiency():
    """
    Real Name: GTL efficiency
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'gtl_efficiency')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of GTL plants. Source: IEA balances (see Technical Report).
    """
    return _ext_constant_gtl_efficiency()


def gtl_potential_production():
    """
    Real Name: GTL potential production
    Original Eqn: INTEG ( replacement GTL+variation GTL-wear GTL, initial GTL production)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual GTL potential production.
    """
    return _integ_gtl_potential_production()


def gtl_production():
    """
    Real Name: GTL production
    Original Eqn: GTL potential production*(1-"share CTL+GTL overcapacity")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    GTL production.
    """
    return gtl_potential_production() * (1 - share_ctlgtl_overcapacity())


def hist_growth_ctl():
    """
    Real Name: Hist growth CTL
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'historic_growth_ctl')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Historic growth of CTL 1990-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_ctl()


def hist_growth_gtl():
    """
    Real Name: Hist growth GTL
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'historic_growth_gtl')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Historic growth of GTL 2000-2014 (IEA Balances).
    """
    return _ext_constant_hist_growth_gtl()


def historic_ctl_production(x):
    """
    Real Name: Historic CTL production
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_ctl_production')
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic generation of CTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_ctl_production(x)


def historic_gtl_production(x):
    """
    Real Name: Historic GTL production
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_gtl_production')
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic generation of GTL 1990-2014 (IEA Balances).
    """
    return _ext_lookup_historic_gtl_production(x)


def initial_ctl_production():
    """
    Real Name: initial CTL production
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_ctl_production')
    Units: EJ/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    CTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_ctl_production()


def initial_gtl_production():
    """
    Real Name: initial GTL production
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_gtl_production')
    Units: EJ/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    GTL production in the initial year 1995 (IEA balances).
    """
    return _ext_constant_initial_gtl_production()


def lifetime_ctl():
    """
    Real Name: lifetime CTL
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'lifetime_ctl')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Lifetime of CTL plants.
    """
    return _ext_constant_lifetime_ctl()


def lifetime_gtl():
    """
    Real Name: lifetime GTL
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'lifetime_gtl')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Lifetime of GTL plants.
    """
    return _ext_constant_lifetime_gtl()


def p_ctl():
    """
    Real Name: P CTL
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C110')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_ctl()


def p_gtl():
    """
    Real Name: P GTL
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C112')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_gtl()


def ped_coal_for_ctl_ej():
    """
    Real Name: PED coal for CTL EJ
    Original Eqn: CTL production/CTL efficiency
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of coal for CTL.
    """
    return ctl_production() / ctl_efficiency()


def ped_nat_gas_for_gtl_ej():
    """
    Real Name: "PED nat. gas for GTL EJ"
    Original Eqn: GTL production/GTL efficiency
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Demand of gas for CTL.
    """
    return gtl_production() / gtl_efficiency()


def potential_fes_ctlgtl_ej():
    """
    Real Name: "Potential FES CTL+GTL EJ"
    Original Eqn: CTL potential production+GTL potential production
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ctl_potential_production() + gtl_potential_production()


def real_growth_ctl():
    """
    Real Name: real growth CTL
    Original Eqn: IF THEN ELSE(abundance coal AUT>=abundance liquids, IF THEN ELSE(abundance coal AUT=1, Exogenous growth CTL,0 ),0)*abundance liquids CTL*scarcity conv oil
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    The real growth of CTL depends on the relative abundance of coal and
        liquids, as well as on the availability of coal.
    """
    return (
        if_then_else(
            abundance_coal_aut() >= abundance_liquids(),
            lambda: if_then_else(
                abundance_coal_aut() == 1, lambda: exogenous_growth_ctl(), lambda: 0
            ),
            lambda: 0,
        )
        * abundance_liquids_ctl()
        * scarcity_conv_oil()
    )


def real_growth_gtl():
    """
    Real Name: real growth GTL
    Original Eqn: IF THEN ELSE(abundance gases>=abundance liquids, IF THEN ELSE(abundance gases=1, Exogenous growth GTL,0 ),0)*abundance liquids GTL*scarcity conv oil
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    The real growth of GTL depends on the relative abundance of gas and
        liquids, as well as on the availability of gas.
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
    Original Eqn: IF THEN ELSE(Time<2015,0, IF THEN ELSE("Crash programme CTL?"=0,0, IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?" *wear CTL, wear CTL)))*scarcity conv oil
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

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


def replacement_gtl():
    """
    Real Name: replacement GTL
    Original Eqn: IF THEN ELSE(Time<2015,0, IF THEN ELSE("Crash programme GTL?"=0,0, IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?" *wear GTL, wear GTL)))*scarcity conv oil
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

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


def share_ctlgtl_overcapacity():
    """
    Real Name: "share CTL+GTL overcapacity"
    Original Eqn: ZIDZ( ("Potential FES CTL+GTL EJ"-"FES CTL+GTL EJ"), "Potential FES CTL+GTL EJ")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(
        (potential_fes_ctlgtl_ej() - fes_ctlgtl_ej()), potential_fes_ctlgtl_ej()
    )


def variation_ctl():
    """
    Real Name: variation CTL
    Original Eqn: IF THEN ELSE(Time<2013, Historic CTL production(INTEGER(Time+1))-Historic CTL production(INTEGER(Time)), IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?" *CTL potential production, CTL potential production*real growth CTL))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual CTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: historic_ctl_production(integer(time() + 1))
        - historic_ctl_production(integer(time())),
        lambda: if_then_else(
            check_liquids() < 0,
            lambda: constrain_liquids_exogenous_growth() * ctl_potential_production(),
            lambda: ctl_potential_production() * real_growth_ctl(),
        ),
    )


def variation_gtl():
    """
    Real Name: variation GTL
    Original Eqn: IF THEN ELSE(Time<2013, Historic GTL production(INTEGER(Time+1))-Historic GTL production(INTEGER(Time)), IF THEN ELSE(check liquids<0, "constrain liquids exogenous growth?" *GTL potential production, GTL potential production*real growth GTL))
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual GTL production.
    """
    return if_then_else(
        time() < 2013,
        lambda: historic_gtl_production(integer(time() + 1))
        - historic_gtl_production(integer(time())),
        lambda: if_then_else(
            check_liquids() < 0,
            lambda: constrain_liquids_exogenous_growth() * gtl_potential_production(),
            lambda: gtl_potential_production() * real_growth_gtl(),
        ),
    )


def wear_ctl():
    """
    Real Name: wear CTL
    Original Eqn: IF THEN ELSE(Time<2015, 0, CTL potential production/lifetime CTL)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Depreciation of CTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: ctl_potential_production() / lifetime_ctl()
    )


def wear_gtl():
    """
    Real Name: wear GTL
    Original Eqn: IF THEN ELSE(Time<2015, 0, GTL potential production/lifetime GTL)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Depreciation of GTL plants.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: gtl_potential_production() / lifetime_gtl()
    )


_ext_constant_crash_programme_ctl = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "D110",
    {},
    _root,
    "_ext_constant_crash_programme_ctl",
)


_ext_constant_crash_programme_gtl = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "D112",
    {},
    _root,
    "_ext_constant_crash_programme_gtl",
)


_ext_constant_ctl_efficiency = ExtConstant(
    "../energy.xlsx",
    "Global",
    "ctl_efficiency",
    {},
    _root,
    "_ext_constant_ctl_efficiency",
)


_integ_ctl_potential_production = Integ(
    lambda: replacement_ctl() + variation_ctl() - wear_ctl(),
    lambda: initial_ctl_production(),
    "_integ_ctl_potential_production",
)


_ext_constant_gtl_efficiency = ExtConstant(
    "../energy.xlsx",
    "Global",
    "gtl_efficiency",
    {},
    _root,
    "_ext_constant_gtl_efficiency",
)


_integ_gtl_potential_production = Integ(
    lambda: replacement_gtl() + variation_gtl() - wear_gtl(),
    lambda: initial_gtl_production(),
    "_integ_gtl_potential_production",
)


_ext_constant_hist_growth_ctl = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_ctl",
    {},
    _root,
    "_ext_constant_hist_growth_ctl",
)


_ext_constant_hist_growth_gtl = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_gtl",
    {},
    _root,
    "_ext_constant_hist_growth_gtl",
)


_ext_lookup_historic_ctl_production = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_ctl_production",
    {},
    _root,
    "_ext_lookup_historic_ctl_production",
)


_ext_lookup_historic_gtl_production = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_gtl_production",
    {},
    _root,
    "_ext_lookup_historic_gtl_production",
)


_ext_constant_initial_ctl_production = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_ctl_production",
    {},
    _root,
    "_ext_constant_initial_ctl_production",
)


_ext_constant_initial_gtl_production = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_gtl_production",
    {},
    _root,
    "_ext_constant_initial_gtl_production",
)


_ext_constant_lifetime_ctl = ExtConstant(
    "../energy.xlsx", "Global", "lifetime_ctl", {}, _root, "_ext_constant_lifetime_ctl"
)


_ext_constant_lifetime_gtl = ExtConstant(
    "../energy.xlsx", "Global", "lifetime_gtl", {}, _root, "_ext_constant_lifetime_gtl"
)


_ext_constant_p_ctl = ExtConstant(
    "../../scenarios/scen_aut.xlsx", "BAU", "C110", {}, _root, "_ext_constant_p_ctl"
)


_ext_constant_p_gtl = ExtConstant(
    "../../scenarios/scen_aut.xlsx", "BAU", "C112", {}, _root, "_ext_constant_p_gtl"
)
