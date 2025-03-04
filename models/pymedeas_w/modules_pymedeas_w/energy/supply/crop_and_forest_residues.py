"""
Module energy.supply.crop_and_forest_residues
Translated using PySD version 3.14.2
"""

@component.add(
    name='"BioE_residues_for_heat+elec_available"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues_for_heat_and_elec": 2,
        "pe_bioe_residues_for_heatelec_ej": 1,
    },
)
def bioe_residues_for_heatelec_available():
    """
    Remaining potential available of bioenergy residues for heat and electricity as given as a fraction of unity.
    """
    return (
        max_npp_potential_bioe_residues_for_heat_and_elec()
        - pe_bioe_residues_for_heatelec_ej()
    ) / max_npp_potential_bioe_residues_for_heat_and_elec()


@component.add(
    name="Cellulosic_biofuels_available",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues_for_cellulosic_biofuels": 2,
        "potential_pe_cellulosic_biofuel_ej": 1,
    },
)
def cellulosic_biofuels_available():
    """
    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        max_npp_potential_bioe_residues_for_cellulosic_biofuels()
        - potential_pe_cellulosic_biofuel_ej(),
        max_npp_potential_bioe_residues_for_cellulosic_biofuels(),
    )


@component.add(
    name="Efficiency_bioE_residues_to_cellulosic_liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"conv_efficiency_from_npp_to_biofuels": 1},
)
def efficiency_bioe_residues_to_cellulosic_liquids():
    """
    Efficiency of the transformation from bioenergy residues to cellulosic liquids. We assume it is the same efficiency than for the conversion from biomass to 2nd generation biofuels.
    """
    return conv_efficiency_from_npp_to_biofuels()


@component.add(
    name="Max_NPP_potential_bioE_residues",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_npp_potential_bioe_residues"},
)
def max_npp_potential_bioe_residues():
    """
    Potencial following WBGU (2009).
    """
    return _ext_constant_max_npp_potential_bioe_residues()


_ext_constant_max_npp_potential_bioe_residues = ExtConstant(
    r"../energy.xlsx",
    "World",
    "max_NPP_pot_bioe_res",
    {},
    _root,
    {},
    "_ext_constant_max_npp_potential_bioe_residues",
)


@component.add(
    name="Max_NPP_potential_BioE_residues_for_cellulosic_biofuels",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues": 1,
        "share_cellulosic_biofuels_vs_bioe_residues": 1,
    },
)
def max_npp_potential_bioe_residues_for_cellulosic_biofuels():
    """
    Potential assigned to the cellulosic biofuels from bioE residues.
    """
    return (
        max_npp_potential_bioe_residues() * share_cellulosic_biofuels_vs_bioe_residues()
    )


@component.add(
    name="Max_NPP_potential_BioE_residues_for_heat_and_elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues": 1,
        "share_cellulosic_biofuels_vs_bioe_residues": 1,
    },
)
def max_npp_potential_bioe_residues_for_heat_and_elec():
    """
    Share of bioE for heat and electricity.
    """
    return max_npp_potential_bioe_residues() * (
        1 - share_cellulosic_biofuels_vs_bioe_residues()
    )


@component.add(
    name="Max_PEavail_potential_bioE_residues_for_cellulosic_biofuels",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues_for_cellulosic_biofuels": 1,
        "efficiency_bioe_residues_to_cellulosic_liquids": 1,
    },
)
def max_peavail_potential_bioe_residues_for_cellulosic_biofuels():
    return (
        max_npp_potential_bioe_residues_for_cellulosic_biofuels()
        * efficiency_bioe_residues_to_cellulosic_liquids()
    )


@component.add(
    name='"new_BioE_residues_for_heat+elec"',
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "start_year_bioe_residues_for_heatelec": 3,
        "pe_bioe_residues_for_heatelec_ej": 1,
        "p_bioe_residues_for_heatelec": 1,
        "ej_per_ktoe": 1,
        "bioe_residues_for_heatelec_available": 1,
        "nvs_1_year": 1,
        "start_production_biofuels": 1,
    },
)
def new_bioe_residues_for_heatelec():
    """
    BioE residues used for heat and electricity. For the first 5 years, we assume the same rate of energy produced than the one achieved by conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_bioe_residues_for_heatelec(),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_bioe_residues_for_heatelec() + 5,
            lambda: start_production_biofuels(
                time() - start_year_bioe_residues_for_heatelec()
            )
            * ej_per_ktoe()
            / nvs_1_year(),
            lambda: p_bioe_residues_for_heatelec()
            * pe_bioe_residues_for_heatelec_ej()
            * bioe_residues_for_heatelec_available(),
        ),
    )


@component.add(
    name="new_cellulosic_biofuels",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "start_year_cellulosic_biofuels": 3,
        "p_cellulosic_biofuels": 1,
        "ej_per_ktoe": 1,
        "cellulosic_biofuels_available": 1,
        "constrain_liquids_exogenous_growth": 1,
        "potential_pe_cellulosic_biofuel_ej": 2,
        "check_liquids": 1,
        "nvs_1_year": 2,
        "start_production_biofuels": 1,
    },
)
def new_cellulosic_biofuels():
    """
    New annual production of cellulosic biofuels from bioE residues. For the first 5 years, we assume the same rate of energy produced than the one achieved by conventional biofuels (2nd generation).
    """
    return if_then_else(
        time() < start_year_cellulosic_biofuels(),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_cellulosic_biofuels() + 5,
            lambda: start_production_biofuels(time() - start_year_cellulosic_biofuels())
            * ej_per_ktoe()
            / nvs_1_year(),
            lambda: if_then_else(
                check_liquids() < -0.0001,
                lambda: constrain_liquids_exogenous_growth()
                * potential_pe_cellulosic_biofuel_ej()
                / nvs_1_year(),
                lambda: p_cellulosic_biofuels()
                * potential_pe_cellulosic_biofuel_ej()
                * cellulosic_biofuels_available(),
            ),
        ),
    )


@component.add(
    name='"P_bioE_residues_for_heat+elec"',
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_bioe_residues_for_heatelec"},
)
def p_bioe_residues_for_heatelec():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_bioe_residues_for_heatelec()


_ext_constant_p_bioe_residues_for_heatelec = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "p_bioe_residues_for_heat_electr",
    {},
    _root,
    {},
    "_ext_constant_p_bioe_residues_for_heatelec",
)


@component.add(
    name="P_cellulosic_biofuels",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_cellulosic_biofuels"},
)
def p_cellulosic_biofuels():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_cellulosic_biofuels()


_ext_constant_p_cellulosic_biofuels = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "p_cellulosic_biofuels",
    {},
    _root,
    {},
    "_ext_constant_p_cellulosic_biofuels",
)


@component.add(
    name='"PE_bioE_residues_for_heat+elec_EJ"',
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pe_bioe_residues_for_heatelec_ej": 1},
    other_deps={
        "_integ_pe_bioe_residues_for_heatelec_ej": {
            "initial": {},
            "step": {"new_bioe_residues_for_heatelec": 1},
        }
    },
)
def pe_bioe_residues_for_heatelec_ej():
    """
    Total annual bioE residues production.
    """
    return _integ_pe_bioe_residues_for_heatelec_ej()


_integ_pe_bioe_residues_for_heatelec_ej = Integ(
    lambda: new_bioe_residues_for_heatelec(),
    lambda: 0,
    "_integ_pe_bioe_residues_for_heatelec_ej",
)


@component.add(
    name="PE_cellulosic_biofuel",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_pe_cellulosic_biofuel_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def pe_cellulosic_biofuel():
    """
    Annual primary energy biomass used for cellulosic biofuels.
    """
    return potential_pe_cellulosic_biofuel_ej() * (1 - share_biofuels_overcapacity())


@component.add(
    name="PEavail_cellulosic_biofuel_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_cellulosic_biofuel": 1,
        "efficiency_bioe_residues_to_cellulosic_liquids": 1,
    },
)
def peavail_cellulosic_biofuel_ej():
    """
    Cellulosic biofuels production from bioenergy-residues.
    """
    return pe_cellulosic_biofuel() * efficiency_bioe_residues_to_cellulosic_liquids()


@component.add(
    name="Potential_PE_cellulosic_biofuel_EJ",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_pe_cellulosic_biofuel_ej": 1},
    other_deps={
        "_integ_potential_pe_cellulosic_biofuel_ej": {
            "initial": {},
            "step": {"new_cellulosic_biofuels": 1},
        }
    },
)
def potential_pe_cellulosic_biofuel_ej():
    """
    Potential annual primary energy biomass used for cellulosic biofuels.
    """
    return _integ_potential_pe_cellulosic_biofuel_ej()


_integ_potential_pe_cellulosic_biofuel_ej = Integ(
    lambda: new_cellulosic_biofuels(),
    lambda: 0,
    "_integ_potential_pe_cellulosic_biofuel_ej",
)


@component.add(
    name="Potential_PEavail_cellulosic_biofuel_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_pe_cellulosic_biofuel_ej": 1,
        "conv_efficiency_from_npp_to_biofuels": 1,
    },
)
def potential_peavail_cellulosic_biofuel_ej():
    return potential_pe_cellulosic_biofuel_ej() * conv_efficiency_from_npp_to_biofuels()


@component.add(
    name="share_cellulosic_biofuels_vs_BioE_residues",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_share_cellulosic_biofuels_vs_bioe_residues"
    },
)
def share_cellulosic_biofuels_vs_bioe_residues():
    """
    Share bioenergy residues potential allocated to cellulosic biofuels production.
    """
    return _ext_constant_share_cellulosic_biofuels_vs_bioe_residues()


_ext_constant_share_cellulosic_biofuels_vs_bioe_residues = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "share_cell_biofuels_vs_bioe_residues",
    {},
    _root,
    {},
    "_ext_constant_share_cellulosic_biofuels_vs_bioe_residues",
)


@component.add(
    name='"start_year_BioE_residues_for_heat+elec"',
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_bioe_residues_for_heatelec"},
)
def start_year_bioe_residues_for_heatelec():
    """
    First year when the technology is available.
    """
    return _ext_constant_start_year_bioe_residues_for_heatelec()


_ext_constant_start_year_bioe_residues_for_heatelec = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_bioe_residues_heat_electr",
    {},
    _root,
    {},
    "_ext_constant_start_year_bioe_residues_for_heatelec",
)


@component.add(
    name="start_year_cellulosic_biofuels",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_cellulosic_biofuels"},
)
def start_year_cellulosic_biofuels():
    """
    First year when the technology is available.
    """
    return _ext_constant_start_year_cellulosic_biofuels()


_ext_constant_start_year_cellulosic_biofuels = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "start_year_cell_biofuels",
    {},
    _root,
    {},
    "_ext_constant_start_year_cellulosic_biofuels",
)
