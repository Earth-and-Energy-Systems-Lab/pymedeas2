"""
Module crop_and_forest_residues
Translated using PySD version 2.2.1
"""


def bioe_residues_for_nonbiofuels_available():
    """
    Real Name: "BioE residues for non-biofuels available"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available of bioenergy residues for other uses than biofuels (heat, electricity and solids) as given as a fraction of unity.
    """
    return zidz(
        max_npp_potential_bioe_residues_for_nonbiofuels()
        - pe_bioe_residues_nonbiofuels_ej(),
        max_npp_potential_bioe_residues_for_nonbiofuels(),
    )


def cellulosic_biofuels_available():
    """
    Real Name: Cellulosic biofuels available
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        max_npp_potential_bioe_residues_for_cellulosic_biofuels()
        - potential_pe_cellulosic_biofuel_ej(),
        max_npp_potential_bioe_residues_for_cellulosic_biofuels(),
    )


def efficiency_bioe_residues_to_cellulosic_liquids():
    """
    Real Name: Efficiency bioE residues to cellulosic liquids
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Efficiency of the transformation from bioenergy residues to cellulosic liquids. We assume it is the same efficiency than for the conversion from biomass to 2nd generation biofuels.
    """
    return conv_efficiency_from_npp_to_biofuels()


def max_npp_potential_bioe_residues():
    """
    Real Name: Max NPP potential bioE residues
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Potencial following WBGU (2009).
    """
    return _ext_constant_max_npp_potential_bioe_residues()


_ext_constant_max_npp_potential_bioe_residues = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "max_NPP_pot_bioe_residues",
    {},
    _root,
    "_ext_constant_max_npp_potential_bioe_residues",
)


def max_npp_potential_bioe_residues_for_cellulosic_biofuels():
    """
    Real Name: Max NPP potential BioE residues for cellulosic biofuels
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential assigned to the cellulosic biofuels from bioE residues.
    """
    return (
        max_npp_potential_bioe_residues() * share_cellulosic_biofuels_vs_bioe_residues()
    )


def max_npp_potential_bioe_residues_for_nonbiofuels():
    """
    Real Name: "Max NPP potential BioE residues for non-biofuels"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of bioE for other uses than biofuels (heat, solids and electricity).
    """
    return max_npp_potential_bioe_residues() * (
        1 - share_cellulosic_biofuels_vs_bioe_residues()
    )


def max_peavail_potential_bioe_residues_for_cellulosic_biofuels():
    """
    Real Name: Max PEavail potential bioE residues for cellulosic biofuels
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        max_npp_potential_bioe_residues_for_cellulosic_biofuels()
        * efficiency_bioe_residues_to_cellulosic_liquids()
    )


def new_bioe_residues_for_nonbiofuels():
    """
    Real Name: "new BioE residues for non-biofuels"
    Original Eqn:
    Units: EJ/(Year*Year)
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    BioE residues used for other uses than biofuels (heat, solids and electricity). For the first 5 years, we assume the same rate of energy produced than the one achieved by conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_bioe_residues_for_nonbiofuels(),
        lambda: 0,
        lambda: if_then_else(
            max_npp_potential_bioe_residues() == 0,
            lambda: 0,
            lambda: if_then_else(
                time() < start_year_bioe_residues_for_nonbiofuels() + 5,
                lambda: start_production_biofuels(
                    time() - start_year_bioe_residues_for_nonbiofuels()
                )
                * ej_per_ktoe(),
                lambda: p_bioe_residues()
                * pe_bioe_residues_nonbiofuels_ej()
                * bioe_residues_for_nonbiofuels_available(),
            ),
        ),
    )


def new_cellulosic_biofuels():
    """
    Real Name: new cellulosic biofuels
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New annual production of cellulosic biofuels from bioE residues. For the first 5 years, we assume the same rate of energy produced than the one achieved by conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_3gen_cellulosic_biofuels(),
        lambda: 0,
        lambda: if_then_else(
            max_npp_potential_bioe_residues() == 0,
            lambda: 0,
            lambda: if_then_else(
                time() < start_year_3gen_cellulosic_biofuels() + 5,
                lambda: start_production_biofuels(
                    time() - start_year_3gen_cellulosic_biofuels()
                )
                * ej_per_ktoe(),
                lambda: if_then_else(
                    check_liquids() < 0,
                    lambda: constrain_liquids_exogenous_growth()
                    * potential_pe_cellulosic_biofuel_ej(),
                    lambda: p_bioe_residues()
                    * potential_pe_cellulosic_biofuel_ej()
                    * cellulosic_biofuels_available(),
                ),
            ),
        ),
    )


def p_bioe_residues():
    """
    Real Name: P bioE residues
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_bioe_residues()


_ext_constant_p_bioe_residues = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_bioe_residues_growth",
    {},
    _root,
    "_ext_constant_p_bioe_residues",
)


def pe_bioe_residues_nonbiofuels_ej():
    """
    Real Name: "PE bioE residues non-biofuels EJ"
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Total annual bioE residues production for other final uses than biofuels.
    """
    return _integ_pe_bioe_residues_nonbiofuels_ej()


_integ_pe_bioe_residues_nonbiofuels_ej = Integ(
    lambda: new_bioe_residues_for_nonbiofuels(),
    lambda: 0,
    "_integ_pe_bioe_residues_nonbiofuels_ej",
)


def pe_cellulosic_biofuel_ej():
    """
    Real Name: PE cellulosic biofuel EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual primary energy biomass used for cellulosic biofuels.
    """
    return potential_pe_cellulosic_biofuel_ej() * (1 - share_biofuels_overcapacity())


def peavail_cellulosic_biofuel_ej():
    """
    Real Name: PEavail cellulosic biofuel EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Cellulosic biofuels production from bioenergy-residues.
    """
    return pe_cellulosic_biofuel_ej() * efficiency_bioe_residues_to_cellulosic_liquids()


def potential_pe_cellulosic_biofuel_abanndoned():
    """
    Real Name: Potential PE cellulosic biofuel abanndoned
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return potential_pe_cellulosic_biofuel_ej() * share_biofuels_overcapacity()


def potential_pe_cellulosic_biofuel_ej():
    """
    Real Name: Potential PE cellulosic biofuel EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Potential annual primary energy biomass used for cellulosic biofuels.
    """
    return _integ_potential_pe_cellulosic_biofuel_ej()


_integ_potential_pe_cellulosic_biofuel_ej = Integ(
    lambda: new_cellulosic_biofuels() - potential_pe_cellulosic_biofuel_abanndoned(),
    lambda: 0,
    "_integ_potential_pe_cellulosic_biofuel_ej",
)


def potential_peavail_cellulosic_biofuel_ej():
    """
    Real Name: Potential PEavail cellulosic biofuel EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return potential_pe_cellulosic_biofuel_ej() * conv_efficiency_from_npp_to_biofuels()


def share_cellulosic_biofuels_vs_bioe_residues():
    """
    Real Name: share cellulosic biofuels vs BioE residues
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share bioenergy residues potential allocated to cellulosic biofuels production.
    """
    return _ext_constant_share_cellulosic_biofuels_vs_bioe_residues()


_ext_constant_share_cellulosic_biofuels_vs_bioe_residues = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "share_cellulosic_biof_vs_bioe_res",
    {},
    _root,
    "_ext_constant_share_cellulosic_biofuels_vs_bioe_residues",
)


def start_year_bioe_residues_for_nonbiofuels():
    """
    Real Name: "start year BioE residues for non-biofuels"
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    First year when the technology is available.
    """
    return _ext_constant_start_year_bioe_residues_for_nonbiofuels()


_ext_constant_start_year_bioe_residues_for_nonbiofuels = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "start_year_bioe_residues_non_biofuels",
    {},
    _root,
    "_ext_constant_start_year_bioe_residues_for_nonbiofuels",
)
