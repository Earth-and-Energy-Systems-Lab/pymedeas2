"""
Module energy.supply.biogas
Translated using PySD version 3.14.2
"""

@component.add(
    name="adapt_growth_biogas",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "past_biogas_growth": 3,
        "nvs_5_years_ts": 1,
        "growth_biogas": 2,
    },
)
def adapt_growth_biogas():
    """
    Annual growth per for biogas. Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_biogas_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_biogas_growth()
            + (growth_biogas() - past_biogas_growth())
            * (time() - 2015)
            / nvs_5_years_ts(),
            lambda: growth_biogas(),
        ),
    )


@component.add(
    name="biogas_evol",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_biogas_evol"},
)
def biogas_evol():
    """
    This variable represents the projected annual growth in relation to past growth trends.
    """
    return _ext_constant_biogas_evol()


_ext_constant_biogas_evol = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "p_biogas_evol",
    {},
    _root,
    {},
    "_ext_constant_biogas_evol",
)


@component.add(
    name="efficiency_biogas_for_elec_CHP_plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_biogas_for_elec_chp_plants"},
)
def efficiency_biogas_for_elec_chp_plants():
    """
    Efficiency of the transformation of biogas in elec in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_chp_plants()


_ext_constant_efficiency_biogas_for_elec_chp_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_in_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_elec_chp_plants",
)


@component.add(
    name="efficiency_biogas_for_elec_plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_biogas_for_elec_plants"},
)
def efficiency_biogas_for_elec_plants():
    """
    Efficiency of the transformation of biogas in elec plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_plants()


_ext_constant_efficiency_biogas_for_elec_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_elec_plants",
)


@component.add(
    name="efficiency_biogas_for_heat_CHP_plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_biogas_for_heat_chp_plants"},
)
def efficiency_biogas_for_heat_chp_plants():
    """
    Efficiency of the transformation of biogas in heat in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_chp_plants()


_ext_constant_efficiency_biogas_for_heat_chp_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_heat_chp_plants",
)


@component.add(
    name="efficiency_biogas_for_heat_plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_biogas_for_heat_plants"},
)
def efficiency_biogas_for_heat_plants():
    """
    Efficiency of the transformation of biogas in heat plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_plants()


_ext_constant_efficiency_biogas_for_heat_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_heat_plants",
)


@component.add(
    name='"FES_biogas_for_heat-com_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_heatcom_plants": 1,
        "efficiency_biogas_for_heat_plants": 1,
    },
)
def fes_biogas_for_heatcom_plants():
    """
    Final energy supply of commercial heat in Heat plants from biogas.
    """
    return pes_biogas_for_heatcom_plants() * efficiency_biogas_for_heat_plants()


@component.add(
    name="FES_elec_from_biogas_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_elec_from_biogas_in_chp_plants": 1,
        "fes_elec_from_biogas_in_elec_plants": 1,
    },
)
def fes_elec_from_biogas_ej():
    """
    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_in_chp_plants() + fes_elec_from_biogas_in_elec_plants()


@component.add(
    name="FES_elec_from_biogas_in_CHP_plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_chp": 1, "efficiency_biogas_for_elec_chp_plants": 1},
)
def fes_elec_from_biogas_in_chp_plants():
    """
    Final energy supply of elec in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_elec_chp_plants()


@component.add(
    name="FES_elec_from_biogas_in_elec_plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_elec_plants": 1,
        "efficiency_biogas_for_elec_plants": 1,
    },
)
def fes_elec_from_biogas_in_elec_plants():
    """
    Final energy supply of electricity in Elec plants from biogas.
    """
    return pes_biogas_for_elec_plants() * efficiency_biogas_for_elec_plants()


@component.add(
    name="FES_elec_from_biogas_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_elec_from_biogas_ej": 1, "ej_per_twh": 1},
)
def fes_elec_from_biogas_twh():
    """
    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_ej() / ej_per_twh()


@component.add(
    name='"FES_heat-com_from_biogas_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_biogas_for_heatcom_plants": 1,
        "fes_heatcom_from_biogas_in_chp_plants": 1,
    },
)
def fes_heatcom_from_biogas_ej():
    """
    TFES commercial heat from biogas.
    """
    return fes_biogas_for_heatcom_plants() + fes_heatcom_from_biogas_in_chp_plants()


@component.add(
    name='"FES_heat-com_from_biogas_in_CHP_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_for_chp": 1, "efficiency_biogas_for_heat_chp_plants": 1},
)
def fes_heatcom_from_biogas_in_chp_plants():
    """
    Final energy supply of commercial heat in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_heat_chp_plants()


@component.add(
    name="growth_biogas",
    units="1/(year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biogas_evol": 1, "past_biogas_growth": 1},
)
def growth_biogas():
    """
    Biogases growth function of growth past trends
    """
    return biogas_evol() * past_biogas_growth()


@component.add(
    name="Historic_biogas_PES",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_biogas_pes",
        "__lookup__": "_ext_lookup_historic_biogas_pes",
    },
)
def historic_biogas_pes(x, final_subs=None):
    """
    Historic production of biogases (1990-2014).
    """
    return _ext_lookup_historic_biogas_pes(x, final_subs)


_ext_lookup_historic_biogas_pes = ExtLookup(
    r"../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_lookup_historic_biogas_pes",
)


@component.add(
    name="Losses_CHP_biogas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_chp": 1,
        "fes_heatcom_from_biogas_in_chp_plants": 1,
        "fes_elec_from_biogas_in_chp_plants": 1,
    },
)
def losses_chp_biogas():
    """
    Losses in biogas CHP plants.
    """
    return (
        pes_biogas_for_chp()
        - fes_heatcom_from_biogas_in_chp_plants()
        - fes_elec_from_biogas_in_chp_plants()
    )


@component.add(
    name="max_biogas_EJ",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_biogas_ej"},
)
def max_biogas_ej():
    """
    Maximun potencial of biogases production.
    """
    return _ext_constant_max_biogas_ej()


_ext_constant_max_biogas_ej = ExtConstant(
    r"../energy.xlsx",
    "World",
    "max_biogases_potential",
    {},
    _root,
    {},
    "_ext_constant_max_biogas_ej",
)


@component.add(
    name="new_PES_biogas",
    units="EJ/(year*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "time_step": 2,
        "historic_biogas_pes": 2,
        "pes_biogas_ej": 2,
        "max_biogas_ej": 2,
        "adapt_growth_biogas": 1,
    },
)
def new_pes_biogas():
    """
    New annual primary energy supply of biogas.
    """
    return if_then_else(
        time() < 2014,
        lambda: (
            historic_biogas_pes(time() + time_step()) - historic_biogas_pes(time())
        )
        / time_step(),
        lambda: ((max_biogas_ej() - pes_biogas_ej()) / max_biogas_ej())
        * adapt_growth_biogas()
        * pes_biogas_ej(),
    )


@component.add(
    name="past_biogas_growth",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_past_biogas_growth"},
)
def past_biogas_growth():
    """
    Current anual growth patterns.
    """
    return _ext_constant_past_biogas_growth()


_ext_constant_past_biogas_growth = ExtConstant(
    r"../energy.xlsx",
    "World",
    "average_historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_constant_past_biogas_growth",
)


@component.add(
    name="PES_Biogas_EJ",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pes_biogas_ej": 1},
    other_deps={
        "_integ_pes_biogas_ej": {
            "initial": {"historic_biogas_pes": 1},
            "step": {"new_pes_biogas": 1},
        }
    },
)
def pes_biogas_ej():
    """
    Biogases primary energy supply. Includes all uses: heat, electricity, total final energy consumption, etc. The same share for final energy uses as well as the efficiency of transformation than for natural fossil gas are assumed.
    """
    return _integ_pes_biogas_ej()


_integ_pes_biogas_ej = Integ(
    lambda: new_pes_biogas(), lambda: historic_biogas_pes(1995), "_integ_pes_biogas_ej"
)


@component.add(
    name="PES_biogas_for_CHP",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "share_pes_biogas_for_chp": 1},
)
def pes_biogas_for_chp():
    """
    Primary energy supply biogas for CHP plants.
    """
    return pes_biogas_ej() * share_pes_biogas_for_chp()


@component.add(
    name="PES_biogas_for_elec_plants",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "share_pes_biogas_for_elec_plants": 1},
)
def pes_biogas_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_elec_plants()


@component.add(
    name='"PES_biogas_for_heat-com_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "share_pes_biogas_for_heatcom_plants": 1},
)
def pes_biogas_for_heatcom_plants():
    """
    Primary energy supply of heat in commercial Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_heatcom_plants()


@component.add(
    name="PES_biogas_for_TFC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_pes_biogas_for_tfc": 1},
)
def pes_biogas_for_tfc():
    """
    Primary energy supply biogas for total final consumption.
    """
    return potential_pes_biogas_for_tfc()


@component.add(
    name="PES_tot_biogas_for_elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_elec_plants": 1,
        "fes_elec_from_biogas_in_chp_plants": 1,
        "losses_chp_biogas": 1,
        "share_efficiency_biogas_for_elec_in_chp_plants": 1,
    },
)
def pes_tot_biogas_for_elec():
    """
    Total primary energy supply for generating electricity from biogas (including CHP plants).
    """
    return (
        pes_biogas_for_elec_plants()
        + fes_elec_from_biogas_in_chp_plants()
        + losses_chp_biogas() * share_efficiency_biogas_for_elec_in_chp_plants()
    )


@component.add(
    name='"PES_tot_biogas_for_heat-com"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_biogas_for_heatcom_plants": 1,
        "fes_heatcom_from_biogas_in_chp_plants": 1,
        "losses_chp_biogas": 1,
        "share_efficiency_biogas_for_elec_in_chp_plants": 1,
    },
)
def pes_tot_biogas_for_heatcom():
    """
    Total primary energy supply for generating commercial heat from biogas (including CHP plants).
    """
    return (
        pes_biogas_for_heatcom_plants()
        + fes_heatcom_from_biogas_in_chp_plants()
        + losses_chp_biogas() * (1 - share_efficiency_biogas_for_elec_in_chp_plants())
    )


@component.add(
    name="Potential_PES_biogas_for_TFC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "share_pes_biogas_tfc": 1},
)
def potential_pes_biogas_for_tfc():
    """
    Potential primary energy supply biogas for total final consumption.
    """
    return pes_biogas_ej() * share_pes_biogas_tfc()


@component.add(
    name="share_efficiency_biogas_for_elec_in_CHP_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_biogas_for_elec_chp_plants": 2,
        "efficiency_biogas_for_heat_chp_plants": 1,
    },
)
def share_efficiency_biogas_for_elec_in_chp_plants():
    return efficiency_biogas_for_elec_chp_plants() / (
        efficiency_biogas_for_elec_chp_plants()
        + efficiency_biogas_for_heat_chp_plants()
    )


@component.add(
    name="share_PES_biogas_for_CHP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_pes_biogas_for_chp"},
)
def share_pes_biogas_for_chp():
    """
    Share of PES biogas for CHP plants.
    """
    return _ext_constant_share_pes_biogas_for_chp()


_ext_constant_share_pes_biogas_for_chp = ExtConstant(
    r"../energy.xlsx",
    "World",
    "share_pes_biogas_for_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_chp",
)


@component.add(
    name="share_PES_biogas_for_elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_elec": 1, "pes_biogas_ej": 1},
)
def share_pes_biogas_for_elec():
    return pes_tot_biogas_for_elec() / pes_biogas_ej()


@component.add(
    name="share_PES_biogas_for_elec_plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_pes_biogas_for_elec_plants"},
)
def share_pes_biogas_for_elec_plants():
    """
    Share of PES biogas for elec plants.
    """
    return _ext_constant_share_pes_biogas_for_elec_plants()


_ext_constant_share_pes_biogas_for_elec_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "share_pes_biogas_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_elec_plants",
)


@component.add(
    name="share_PES_biogas_for_heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_heatcom": 1, "pes_biogas_ej": 1},
)
def share_pes_biogas_for_heat():
    return pes_tot_biogas_for_heatcom() / pes_biogas_ej()


@component.add(
    name='"share_PES_biogas_for_heat-com_plants"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_pes_biogas_for_heatcom_plants"},
)
def share_pes_biogas_for_heatcom_plants():
    """
    Share of PES biogas for commercial heat plants.
    """
    return _ext_constant_share_pes_biogas_for_heatcom_plants()


_ext_constant_share_pes_biogas_for_heatcom_plants = ExtConstant(
    r"../energy.xlsx",
    "World",
    "share_pes_biogas_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_heatcom_plants",
)


@component.add(
    name="share_PES_biogas_TFC",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_share_pes_biogas_tfc"},
)
def share_pes_biogas_tfc():
    """
    Share of PES biogas for total final consumption.
    """
    return _ext_constant_share_pes_biogas_tfc()


_ext_constant_share_pes_biogas_tfc = ExtConstant(
    r"../energy.xlsx",
    "World",
    "share_pes_biogas_tfc",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_tfc",
)
