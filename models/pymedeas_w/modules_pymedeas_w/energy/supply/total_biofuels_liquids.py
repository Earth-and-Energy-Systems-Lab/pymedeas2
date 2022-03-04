"""
Module total_biofuels_liquids
Translated using PySD version 2.2.1
"""


def additional_pe_production_of_bioenergy_for_biofuels():
    """
    Real Name: Additional PE production of bioenergy for biofuels
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Additional primary energy demand of bioenergy (NPP) for biofuels in relation to the PEavail. We assume than 1 unit of energy of biofuels substitutes 1 unit of energy of oil.
    """
    return pe_biomass_for_biofuels_production_ej() - oil_liquids_saved_by_biofuels_ej()


def fes_total_biofuels_production_ej():
    """
    Real Name: FES total biofuels production EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply total biofuels liquids production. Equivalent to "FES total biofuels production EJ 2" but obtained disaggregately.
    """
    return (
        peavail_biofuels_2gen_land_compet_ej()
        + peavail_biofuels_3gen_land_compet_ej()
        + peavail_biofuels_land_marg_ej()
        + peavail_cellulosic_biofuel_ej()
    )


def fes_total_biofuels_production_ej_2():
    """
    Real Name: FES total biofuels production EJ 2
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply total biofuels liquids production. Equivalent to "FES total biofuels production EJ" but obtained aggregately to estimate the "share biofuels overcapacity".
    """
    return np.minimum(ped_liquids_ej(), potential_peavail_total_biofuels())


def fes_total_biofuels_production_mbd():
    """
    Real Name: "FES total biofuels production Mb/d"
    Original Eqn:
    Units: Mb/d
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply total biofuels liquids production.
    """
    return fes_total_biofuels_production_ej() * mbd_per_ejyear()


def max_peavail_biofuels_potential():
    """
    Real Name: Max PEavail biofuels potential
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum biofuels potential (primary energy) available.
    """
    return (
        max_peavail_potential_bioe_residues_for_cellulosic_biofuels()
        + max_peavail_potential_biofuels_23gen()
        + max_peavail_potential_biofuels_marginal_lands()
    )


def oil_liquids_saved_by_biofuels_ej():
    """
    Real Name: Oil liquids saved by biofuels EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Oil liquids saved by biofuels.
    """
    return fes_total_biofuels_production_ej()


def pe_biomass_for_biofuels_production_ej():
    """
    Real Name: PE biomass for biofuels production EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy of biomass for biofuels production.
    """
    return (
        pe_biofuels_land_marg_ej()
        + pe_cellulosic_biofuel_ej()
        + pe_biofuels_prod_2gen3gen_ej()
    )


def potential_peavail_total_biofuels():
    """
    Real Name: Potential PEavail total biofuels
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        potential_peavail_biofuels_2gen_land_compet_ej()
        + potential_peavail_biofuels_prod_3gen_ej()
        + potential_peavail_biofuels_land_marg_ej()
        + potential_peavail_cellulosic_biofuel_ej()
    )


def share_biofuels_overcapacity():
    """
    Real Name: share biofuels overcapacity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(
        potential_peavail_total_biofuels() - fes_total_biofuels_production_ej_2(),
        potential_peavail_total_biofuels(),
    )
