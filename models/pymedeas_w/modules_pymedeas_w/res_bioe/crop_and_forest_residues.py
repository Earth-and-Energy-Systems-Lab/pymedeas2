"""
Module crop_and_forest_residues
Translated using PySD version 2.2.0
"""


def bioe_residues_for_heatelec_available():
    """
    Real Name: "BioE residues for heat+elec available"
    Original Eqn: (Max NPP potential BioE residues for heat and elec-"PE bioE residues for heat+elec EJ")/Max NPP potential BioE residues for heat and elec
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential available of bioenergy residues for heat and
        electricity as given as a fraction of unity.
    """
    return (
        max_npp_potential_bioe_residues_for_heat_and_elec()
        - pe_bioe_residues_for_heatelec_ej()
    ) / max_npp_potential_bioe_residues_for_heat_and_elec()


def cellulosic_biofuels_available():
    """
    Real Name: Cellulosic biofuels available
    Original Eqn: ZIDZ( (Max NPP potential BioE residues for cellulosic biofuels-Potential PE cellulosic biofuel EJ), Max NPP potential BioE residues for cellulosic biofuels)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        (
            max_npp_potential_bioe_residues_for_cellulosic_biofuels()
            - potential_pe_cellulosic_biofuel_ej()
        ),
        max_npp_potential_bioe_residues_for_cellulosic_biofuels(),
    )


def efficiency_bioe_residues_to_cellulosic_liquids():
    """
    Real Name: Efficiency bioE residues to cellulosic liquids
    Original Eqn: Conv efficiency from NPP to biofuels
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Efficiency of the transformation from bioenergy residues to cellulosic
        liquids. We assume it is the same efficiency than for the conversion from
        biomass to 2nd generation biofuels.
    """
    return conv_efficiency_from_npp_to_biofuels()


def max_npp_potential_bioe_residues():
    """
    Real Name: Max NPP potential bioE residues
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'G43')
    Units: EJ/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Potencial following WBGU (2009).
    """
    return _ext_constant_max_npp_potential_bioe_residues()


def max_npp_potential_bioe_residues_for_cellulosic_biofuels():
    """
    Real Name: Max NPP potential BioE residues for cellulosic biofuels
    Original Eqn: Max NPP potential bioE residues*share cellulosic biofuels vs BioE residues
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential assigned to the cellulosic biofuels from bioE residues.
    """
    return (
        max_npp_potential_bioe_residues() * share_cellulosic_biofuels_vs_bioe_residues()
    )


def max_npp_potential_bioe_residues_for_heat_and_elec():
    """
    Real Name: Max NPP potential BioE residues for heat and elec
    Original Eqn: Max NPP potential bioE residues*(1-share cellulosic biofuels vs BioE residues)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Share of bioE for heat and electricity.
    """
    return max_npp_potential_bioe_residues() * (
        1 - share_cellulosic_biofuels_vs_bioe_residues()
    )


def max_peavail_potential_bioe_residues_for_cellulosic_biofuels():
    """
    Real Name: Max PEavail potential bioE residues for cellulosic biofuels
    Original Eqn: Max NPP potential BioE residues for cellulosic biofuels*Efficiency bioE residues to cellulosic liquids
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        max_npp_potential_bioe_residues_for_cellulosic_biofuels()
        * efficiency_bioe_residues_to_cellulosic_liquids()
    )


def new_bioe_residues_for_heatelec():
    """
    Real Name: "new BioE residues for heat+elec"
    Original Eqn: IF THEN ELSE(Time<"start year BioE residues for heat+elec", 0, IF THEN ELSE(Time<"start year BioE residues for heat+elec"+5, start production biofuels(Time-"start year BioE residues for heat+elec")*EJ per ktoe, "P bioE residues for heat+elec"*"PE bioE residues for heat+elec EJ"*"BioE residues for heat+elec available"))
    Units: EJ/(year*year)
    Limits: (None, None)
    Type: component
    Subs: None

    BioE residues used for heat and electricity. For the first 5 years, we
        assume the same rate of energy produced than the one achieved by
        conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_bioe_residues_for_heatelec(),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_bioe_residues_for_heatelec() + 5,
            lambda: start_production_biofuels(
                time() - start_year_bioe_residues_for_heatelec()
            )
            * ej_per_ktoe(),
            lambda: p_bioe_residues_for_heatelec()
            * pe_bioe_residues_for_heatelec_ej()
            * bioe_residues_for_heatelec_available(),
        ),
    )


def new_cellulosic_biofuels():
    """
    Real Name: new cellulosic biofuels
    Original Eqn: IF THEN ELSE(Time<start year cellulosic biofuels, 0, IF THEN ELSE(Time<start year cellulosic biofuels+5, start production biofuels(Time-start year cellulosic biofuels )*EJ per ktoe, IF THEN ELSE(check liquids<-0.0001, "constrain liquids exogenous growth?"*Potential PE cellulosic biofuel EJ , P cellulosic biofuels*Potential PE cellulosic biofuel EJ *Cellulosic biofuels available)))
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual production of cellulosic biofuels from bioE residues. For the
        first 5 years, we assume the same rate of energy produced than the one
        achieved by conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_cellulosic_biofuels(),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_cellulosic_biofuels() + 5,
            lambda: start_production_biofuels(time() - start_year_cellulosic_biofuels())
            * ej_per_ktoe(),
            lambda: if_then_else(
                check_liquids() < -0.0001,
                lambda: constrain_liquids_exogenous_growth()
                * potential_pe_cellulosic_biofuel_ej(),
                lambda: p_cellulosic_biofuels()
                * potential_pe_cellulosic_biofuel_ej()
                * cellulosic_biofuels_available(),
            ),
        ),
    )


def p_bioe_residues_for_heatelec():
    """
    Real Name: "P bioE residues for heat+elec"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C46')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_bioe_residues_for_heatelec()


def p_cellulosic_biofuels():
    """
    Real Name: P cellulosic biofuels
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C48')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in energy output demand depending on the policy of the
        scenario.
    """
    return _ext_constant_p_cellulosic_biofuels()


def pe_bioe_residues_for_heatelec_ej():
    """
    Real Name: "PE bioE residues for heat+elec EJ"
    Original Eqn: INTEG ( "new BioE residues for heat+elec", 0)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual bioE residues production.
    """
    return _integ_pe_bioe_residues_for_heatelec_ej()


def pe_cellulosic_biofuel_ej():
    """
    Real Name: PE cellulosic biofuel EJ
    Original Eqn: Potential PE cellulosic biofuel EJ*(1-share biofuels overcapacity )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Annual primary energy biomass used for cellulosic biofuels.
    """
    return potential_pe_cellulosic_biofuel_ej() * (1 - share_biofuels_overcapacity())


def peavail_cellulosic_biofuel_ej():
    """
    Real Name: PEavail cellulosic biofuel EJ
    Original Eqn: PE cellulosic biofuel EJ*Efficiency bioE residues to cellulosic liquids
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Cellulosic biofuels production from bioenergy-residues.
    """
    return pe_cellulosic_biofuel_ej() * efficiency_bioe_residues_to_cellulosic_liquids()


def potential_pe_cellulosic_biofuel_ej():
    """
    Real Name: Potential PE cellulosic biofuel EJ
    Original Eqn: INTEG ( new cellulosic biofuels, 0)
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Potential annual primary energy biomass used for cellulosic biofuels.
    """
    return _integ_potential_pe_cellulosic_biofuel_ej()


def potential_peavail_cellulosic_biofuel_ej():
    """
    Real Name: Potential PEavail cellulosic biofuel EJ
    Original Eqn: Potential PE cellulosic biofuel EJ*Conv efficiency from NPP to biofuels
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return potential_pe_cellulosic_biofuel_ej() * conv_efficiency_from_npp_to_biofuels()


def share_cellulosic_biofuels_vs_bioe_residues():
    """
    Real Name: share cellulosic biofuels vs BioE residues
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C50')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share bioenergy residues potential allocated to cellulosic biofuels
        production.
    """
    return _ext_constant_share_cellulosic_biofuels_vs_bioe_residues()


def start_year_bioe_residues_for_heatelec():
    """
    Real Name: "start year BioE residues for heat+elec"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C47')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    First year when the technology is available.
    """
    return _ext_constant_start_year_bioe_residues_for_heatelec()


def start_year_cellulosic_biofuels():
    """
    Real Name: start year cellulosic biofuels
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C49')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    First year when the technology is available.
    """
    return _ext_constant_start_year_cellulosic_biofuels()


_ext_constant_max_npp_potential_bioe_residues = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "G43",
    {},
    _root,
    "_ext_constant_max_npp_potential_bioe_residues",
)


_ext_constant_p_bioe_residues_for_heatelec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C46",
    {},
    _root,
    "_ext_constant_p_bioe_residues_for_heatelec",
)


_ext_constant_p_cellulosic_biofuels = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C48",
    {},
    _root,
    "_ext_constant_p_cellulosic_biofuels",
)


_integ_pe_bioe_residues_for_heatelec_ej = Integ(
    lambda: new_bioe_residues_for_heatelec(),
    lambda: 0,
    "_integ_pe_bioe_residues_for_heatelec_ej",
)


_integ_potential_pe_cellulosic_biofuel_ej = Integ(
    lambda: new_cellulosic_biofuels(),
    lambda: 0,
    "_integ_potential_pe_cellulosic_biofuel_ej",
)


_ext_constant_share_cellulosic_biofuels_vs_bioe_residues = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C50",
    {},
    _root,
    "_ext_constant_share_cellulosic_biofuels_vs_bioe_residues",
)


_ext_constant_start_year_bioe_residues_for_heatelec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C47",
    {},
    _root,
    "_ext_constant_start_year_bioe_residues_for_heatelec",
)


_ext_constant_start_year_cellulosic_biofuels = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C49",
    {},
    _root,
    "_ext_constant_start_year_cellulosic_biofuels",
)
