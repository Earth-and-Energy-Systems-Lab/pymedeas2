"""
Module energy.supply.total_biofuels_liquids
Translated using PySD version 3.14.0
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
    name="exports biofuels",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_exports_biofuels": 1,
        "exports_biofuels_policy": 1,
    },
)
def exports_biofuels():
    return if_then_else(
        time() < 2015,
        lambda: historic_exports_biofuels(),
        lambda: exports_biofuels_policy(),
    )


@component.add(
    name="exports biofuels policy",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_exports_biofuels_policy",
        "__data__": "_ext_data_exports_biofuels_policy",
        "time": 1,
    },
)
def exports_biofuels_policy():
    return _ext_data_exports_biofuels_policy(time())


_ext_data_exports_biofuels_policy = ExtData(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "biofuels_exports",
    None,
    {},
    _root,
    {},
    "_ext_data_exports_biofuels_policy",
)


@component.add(
    name="FES total biofuels EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peavail_tot_biofuels_land_compet_ej": 1,
        "peavail_biofuels_land_marg_ej": 1,
        "peavail_cellulosic_biofuel_ej": 1,
        "exports_biofuels": 1,
    },
)
def fes_total_biofuels_ej():
    """
    Final energy supply total biofuels liquids production and imports/exports. Equivalent to "FES total biofuels production EJ 2" but obtained disaggregately.
    """
    return (
        peavail_tot_biofuels_land_compet_ej()
        + peavail_biofuels_land_marg_ej()
        + peavail_cellulosic_biofuel_ej()
        - exports_biofuels()
    )


@component.add(
    name="FES total biofuels production EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "potential_peavail_total_biofuels": 1},
)
def fes_total_biofuels_production_ej():
    """
    Final energy supply total biofuels liquids production. Equivalent to "FES total biofuels production EJ" but obtained aggregately to estimate the "share biofuels overcapacity".
    """
    return np.minimum(ped_liquids(), potential_peavail_total_biofuels())


@component.add(
    name='"FES total biofuels production Mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_ej": 1, "mbd_per_ejyear": 1},
)
def fes_total_biofuels_production_mbd():
    """
    Final energy supply total biofuels liquids production.
    """
    return fes_total_biofuels_ej() * mbd_per_ejyear()


@component.add(
    name="Historic exports biofuels",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_exports_biofuels",
        "__data__": "_ext_data_historic_exports_biofuels",
        "time": 1,
    },
)
def historic_exports_biofuels():
    """
    Exports if >0, else imports
    """
    return _ext_data_historic_exports_biofuels(time())


_ext_data_historic_exports_biofuels = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "biofuels_hist_exports",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_exports_biofuels",
)


@component.add(
    name="Max PEavail biofuels potential",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_peavail_potential_bioe_residues_for_cellulosic_biofuels": 1,
        "max_peavail_potential_biofuels_land_compet": 1,
        "max_peavail_potential_biofuels_marginal_lands": 1,
    },
)
def max_peavail_biofuels_potential():
    """
    Maximum biofuels potential (primary energy) available.
    """
    return (
        max_peavail_potential_bioe_residues_for_cellulosic_biofuels()
        + max_peavail_potential_biofuels_land_compet()
        + max_peavail_potential_biofuels_marginal_lands()
    )


@component.add(
    name="Oil liquids saved by biofuels EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_ej": 1},
)
def oil_liquids_saved_by_biofuels_ej():
    """
    Oil liquids saved by biofuels.
    """
    return fes_total_biofuels_ej()


@component.add(
    name="PE biomass for biofuels production EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_biofuels_land_marg_ej": 1,
        "pe_cellulosic_biofuel": 1,
        "pe_biofuels_prod_2gen3gen_ej": 1,
    },
)
def pe_biomass_for_biofuels_production_ej():
    """
    Primary energy of biomass for biofuels production.
    """
    return (
        pe_biofuels_land_marg_ej()
        + pe_cellulosic_biofuel()
        + pe_biofuels_prod_2gen3gen_ej()
    )


@component.add(
    name="Potential PEavail total biofuels",
    units="EJ/year",
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
    name="remaining potential biofuels",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_peavail_biofuels_potential": 3, "fes_total_biofuels_ej": 2},
)
def remaining_potential_biofuels():
    """
    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_peavail_biofuels_potential() > fes_total_biofuels_ej(),
        lambda: (max_peavail_biofuels_potential() - fes_total_biofuels_ej())
        / max_peavail_biofuels_potential(),
        lambda: 0,
    )


@component.add(
    name="share biofuels overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_peavail_total_biofuels": 2,
        "fes_total_biofuels_production_ej": 1,
    },
)
def share_biofuels_overcapacity():
    return zidz(
        potential_peavail_total_biofuels() - fes_total_biofuels_production_ej(),
        potential_peavail_total_biofuels(),
    )
