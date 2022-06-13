"""
Module crop_and_forest_residues
Translated using PySD version 3.2.0
"""


@component.add(
    name='"BioE residues for non-biofuels available"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues_for_nonbiofuels": 2,
        "pe_bioe_residues_nonbiofuels_ej": 1,
    },
)
def bioe_residues_for_nonbiofuels_available():
    """
    Remaining potential available of bioenergy residues for other uses than biofuels (heat, electricity and solids) as given as a fraction of unity.
    """
    return zidz(
        max_npp_potential_bioe_residues_for_nonbiofuels()
        - pe_bioe_residues_nonbiofuels_ej(),
        max_npp_potential_bioe_residues_for_nonbiofuels(),
    )


@component.add(
    name="Cellulosic biofuels available",
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
    name="Efficiency bioE residues to cellulosic liquids",
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
    name="Max NPP potential bioE residues",
    units="EJ/Year",
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
    "../energy.xlsx",
    "Austria",
    "max_NPP_pot_bioe_residues",
    {},
    _root,
    {},
    "_ext_constant_max_npp_potential_bioe_residues",
)


@component.add(
    name="Max NPP potential BioE residues for cellulosic biofuels",
    units="EJ/Year",
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
    name='"Max NPP potential BioE residues for non-biofuels"',
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_npp_potential_bioe_residues": 1,
        "share_cellulosic_biofuels_vs_bioe_residues": 1,
    },
)
def max_npp_potential_bioe_residues_for_nonbiofuels():
    """
    Share of bioE for other uses than biofuels (heat, solids and electricity).
    """
    return max_npp_potential_bioe_residues() * (
        1 - share_cellulosic_biofuels_vs_bioe_residues()
    )


@component.add(
    name="Max PEavail potential bioE residues for cellulosic biofuels",
    units="EJ",
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
    name='"new BioE residues for non-biofuels"',
    units="EJ/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "start_year_bioe_residues_for_nonbiofuels": 3,
        "pe_bioe_residues_nonbiofuels_ej": 1,
        "max_npp_potential_bioe_residues": 1,
        "bioe_residues_for_nonbiofuels_available": 1,
        "p_bioe_residues": 1,
        "start_production_biofuels": 1,
        "ej_per_ktoe": 1,
    },
)
def new_bioe_residues_for_nonbiofuels():
    """
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


@component.add(
    name="new cellulosic biofuels",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "start_year_3gen_cellulosic_biofuels": 3,
        "potential_pe_cellulosic_biofuel_ej": 2,
        "max_npp_potential_bioe_residues": 1,
        "constrain_liquids_exogenous_growth": 1,
        "cellulosic_biofuels_available": 1,
        "check_liquids": 1,
        "p_bioe_residues": 1,
        "start_production_biofuels": 1,
        "ej_per_ktoe": 1,
    },
)
def new_cellulosic_biofuels():
    """
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


@component.add(
    name="P bioE residues",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_bioe_residues"},
)
def p_bioe_residues():
    """
    Annual growth in energy output demand depending on the policy of the scenario.
    """
    return _ext_constant_p_bioe_residues()


_ext_constant_p_bioe_residues = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_bioe_residues_growth",
    {},
    _root,
    {},
    "_ext_constant_p_bioe_residues",
)


@component.add(
    name='"PE bioE residues non-biofuels EJ"',
    units="EJ/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pe_bioe_residues_nonbiofuels_ej": 1},
    other_deps={
        "_integ_pe_bioe_residues_nonbiofuels_ej": {
            "initial": {},
            "step": {"new_bioe_residues_for_nonbiofuels": 1},
        }
    },
)
def pe_bioe_residues_nonbiofuels_ej():
    """
    Total annual bioE residues production for other final uses than biofuels.
    """
    return _integ_pe_bioe_residues_nonbiofuels_ej()


_integ_pe_bioe_residues_nonbiofuels_ej = Integ(
    lambda: new_bioe_residues_for_nonbiofuels(),
    lambda: 0,
    "_integ_pe_bioe_residues_nonbiofuels_ej",
)


@component.add(
    name="PE cellulosic biofuel EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_pe_cellulosic_biofuel_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def pe_cellulosic_biofuel_ej():
    """
    Annual primary energy biomass used for cellulosic biofuels.
    """
    return potential_pe_cellulosic_biofuel_ej() * (1 - share_biofuels_overcapacity())


@component.add(
    name="PEavail cellulosic biofuel EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_cellulosic_biofuel_ej": 1,
        "efficiency_bioe_residues_to_cellulosic_liquids": 1,
    },
)
def peavail_cellulosic_biofuel_ej():
    """
    Cellulosic biofuels production from bioenergy-residues.
    """
    return pe_cellulosic_biofuel_ej() * efficiency_bioe_residues_to_cellulosic_liquids()


@component.add(
    name="Potential PE cellulosic biofuel abanndoned",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_pe_cellulosic_biofuel_ej": 1,
        "share_biofuels_overcapacity": 1,
    },
)
def potential_pe_cellulosic_biofuel_abanndoned():
    return potential_pe_cellulosic_biofuel_ej() * share_biofuels_overcapacity()


@component.add(
    name="Potential PE cellulosic biofuel EJ",
    units="EJ/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_pe_cellulosic_biofuel_ej": 1},
    other_deps={
        "_integ_potential_pe_cellulosic_biofuel_ej": {
            "initial": {},
            "step": {
                "new_cellulosic_biofuels": 1,
                "potential_pe_cellulosic_biofuel_abanndoned": 1,
            },
        }
    },
)
def potential_pe_cellulosic_biofuel_ej():
    """
    Potential annual primary energy biomass used for cellulosic biofuels.
    """
    return _integ_potential_pe_cellulosic_biofuel_ej()


_integ_potential_pe_cellulosic_biofuel_ej = Integ(
    lambda: new_cellulosic_biofuels() - potential_pe_cellulosic_biofuel_abanndoned(),
    lambda: 0,
    "_integ_potential_pe_cellulosic_biofuel_ej",
)


@component.add(
    name="Potential PEavail cellulosic biofuel EJ",
    units="EJ",
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
    name="share cellulosic biofuels vs BioE residues",
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
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "share_cellulosic_biof_vs_bioe_res",
    {},
    _root,
    {},
    "_ext_constant_share_cellulosic_biofuels_vs_bioe_residues",
)


@component.add(
    name='"start year BioE residues for non-biofuels"',
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_year_bioe_residues_for_nonbiofuels"
    },
)
def start_year_bioe_residues_for_nonbiofuels():
    """
    First year when the technology is available.
    """
    return _ext_constant_start_year_bioe_residues_for_nonbiofuels()


_ext_constant_start_year_bioe_residues_for_nonbiofuels = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "start_year_bioe_residues_non_biofuels",
    {},
    _root,
    {},
    "_ext_constant_start_year_bioe_residues_for_nonbiofuels",
)
