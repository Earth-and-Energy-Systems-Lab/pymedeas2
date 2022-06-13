"""
Module total_biofuels_liquids
Translated using PySD version 3.2.0
"""


@component.add(
    name="Additional PE production of bioenergy for biofuels",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_biomass_for_biofuels_production_ej": 1,
        "oil_liquids_saved_by_biofuels_ej": 1,
    },
)
def additional_pe_production_of_bioenergy_for_biofuels():
    """
    Additional primary energy demand of bioenergy (NPP) for biofuels in relation to the PEavail. We assume than 1 unit of energy of biofuels substitutes 1 unit of energy of oil.
    """
    return pe_biomass_for_biofuels_production_ej() - oil_liquids_saved_by_biofuels_ej()


@component.add(
    name="FES total biofuels production EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peavail_biofuels_2gen_land_compet_ej": 1,
        "peavail_biofuels_3gen_land_compet_ej": 1,
        "peavail_biofuels_land_marg_ej": 1,
        "peavail_cellulosic_biofuel_ej": 1,
    },
)
def fes_total_biofuels_production_ej():
    """
    Final energy supply total biofuels liquids production. Equivalent to "FES total biofuels production EJ 2" but obtained disaggregately.
    """
    return (
        peavail_biofuels_2gen_land_compet_ej()
        + peavail_biofuels_3gen_land_compet_ej()
        + peavail_biofuels_land_marg_ej()
        + peavail_cellulosic_biofuel_ej()
    )


@component.add(
    name="FES total biofuels production EJ 2",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids_ej": 1, "potential_peavail_total_biofuels": 1},
)
def fes_total_biofuels_production_ej_2():
    """
    Final energy supply total biofuels liquids production. Equivalent to "FES total biofuels production EJ" but obtained aggregately to estimate the "share biofuels overcapacity".
    """
    return np.minimum(ped_liquids_ej(), potential_peavail_total_biofuels())


@component.add(
    name='"FES total biofuels production Mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_production_ej": 1, "mbd_per_ejyear": 1},
)
def fes_total_biofuels_production_mbd():
    """
    Final energy supply total biofuels liquids production.
    """
    return fes_total_biofuels_production_ej() * mbd_per_ejyear()


@component.add(
    name="Max PEavail biofuels potential",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_peavail_potential_bioe_residues_for_cellulosic_biofuels": 1,
        "max_peavail_potential_biofuels_23gen": 1,
        "max_peavail_potential_biofuels_marginal_lands": 1,
    },
)
def max_peavail_biofuels_potential():
    """
    Maximum biofuels potential (primary energy) available.
    """
    return (
        max_peavail_potential_bioe_residues_for_cellulosic_biofuels()
        + max_peavail_potential_biofuels_23gen()
        + max_peavail_potential_biofuels_marginal_lands()
    )


@component.add(
    name="Oil liquids saved by biofuels EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_production_ej": 1},
)
def oil_liquids_saved_by_biofuels_ej():
    """
    Oil liquids saved by biofuels.
    """
    return fes_total_biofuels_production_ej()


@component.add(
    name="PE biomass for biofuels production EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_biofuels_land_marg_ej": 1,
        "pe_cellulosic_biofuel_ej": 1,
        "pe_biofuels_prod_2gen3gen_ej": 1,
    },
)
def pe_biomass_for_biofuels_production_ej():
    """
    Primary energy of biomass for biofuels production.
    """
    return (
        pe_biofuels_land_marg_ej()
        + pe_cellulosic_biofuel_ej()
        + pe_biofuels_prod_2gen3gen_ej()
    )


@component.add(
    name="Potential PEavail total biofuels",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_biofuels_2gen_land_compet_ej": 1,
        "potential_peavail_biofuels_prod_3gen_ej": 1,
        "potential_peavail_biofuels_land_marg_ej": 1,
        "potential_peavail_cellulosic_biofuel_ej": 1,
    },
)
def potential_peavail_total_biofuels():
    return (
        potential_peavail_biofuels_2gen_land_compet_ej()
        + potential_peavail_biofuels_prod_3gen_ej()
        + potential_peavail_biofuels_land_marg_ej()
        + potential_peavail_cellulosic_biofuel_ej()
    )


@component.add(
    name="share biofuels overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_total_biofuels": 2,
        "fes_total_biofuels_production_ej_2": 1,
    },
)
def share_biofuels_overcapacity():
    return zidz(
        potential_peavail_total_biofuels() - fes_total_biofuels_production_ej_2(),
        potential_peavail_total_biofuels(),
    )
