"""
Module biogas
Translated using PySD version 2.2.3
"""


def adapt_growth_biogas():
    """
    Real Name: adapt growth biogas
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual growth per for biogas. Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_biogas_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_biogas_growth()
            + (growth_biogas() - past_biogas_growth()) * (time() - 2015) / 5,
            lambda: growth_biogas(),
        ),
    )


def biogas_evol():
    """
    Real Name: biogas evol
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    This variable represents the projected annual growth in relation to past growth trends.
    """
    return _ext_constant_biogas_evol()


_ext_constant_biogas_evol = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_biogas_evol",
    {},
    _root,
    "_ext_constant_biogas_evol",
)


def efficiency_biogas_for_elec_chp_plants():
    """
    Real Name: efficiency biogas for elec CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of biogas in elec in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_chp_plants()


_ext_constant_efficiency_biogas_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_in_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_elec_chp_plants",
)


def efficiency_biogas_for_elec_plants():
    """
    Real Name: efficiency biogas for elec plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of biogas in elec plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_plants()


_ext_constant_efficiency_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_elec_plants",
)


def efficiency_biogas_for_heat_chp_plants():
    """
    Real Name: efficiency biogas for heat CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of biogas in heat in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_chp_plants()


_ext_constant_efficiency_biogas_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_heat_chp_plants",
)


def efficiency_biogas_for_heat_plants():
    """
    Real Name: efficiency biogas for heat plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation of biogas in heat plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_plants()


_ext_constant_efficiency_biogas_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_heat_plants",
)


def fes_biogas_for_heatcom_plants():
    """
    Real Name: "FES biogas for heat-com plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of commercial heat in Heat plants from biogas.
    """
    return pes_biogas_for_heatcom_plants() * efficiency_biogas_for_heat_plants()


def fes_elec_from_biogas_ej():
    """
    Real Name: FES elec from biogas EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_in_chp_plants() + fes_elec_from_biogas_in_elec_plants()


def fes_elec_from_biogas_in_chp_plants():
    """
    Real Name: FES elec from biogas in CHP plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of elec in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_elec_chp_plants()


def fes_elec_from_biogas_in_elec_plants():
    """
    Real Name: FES elec from biogas in elec plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of electricity in Elec plants from biogas.
    """
    return pes_biogas_for_elec_plants() * efficiency_biogas_for_elec_plants()


def fes_elec_from_biogas_twh():
    """
    Real Name: FES elec from biogas TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_ej() / ej_per_twh()


def fes_heatcom_from_biogas_ej():
    """
    Real Name: "FES heat-com from biogas EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TFES commercial heat from biogas.
    """
    return fes_biogas_for_heatcom_plants() + fes_heatcom_from_biogas_in_chp_plants()


def fes_heatcom_from_biogas_in_chp_plants():
    """
    Real Name: "FES heat-com from biogas in CHP plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy supply of commercial heat in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_heat_chp_plants()


def growth_biogas():
    """
    Real Name: growth biogas
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Biogases growth function of growth past trends
    """
    return biogas_evol() * past_biogas_growth()


def historic_biogas_pes(x):
    """
    Real Name: Historic biogas PES
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic production of biogases (1990-2014).
    """
    return _ext_lookup_historic_biogas_pes(x)


_ext_lookup_historic_biogas_pes = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    "_ext_lookup_historic_biogas_pes",
)


def losses_chp_biogas():
    """
    Real Name: Losses CHP biogas
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Losses in biogas CHP plants.
    """
    return (
        pes_biogas_for_chp()
        - fes_heatcom_from_biogas_in_chp_plants()
        - fes_elec_from_biogas_in_chp_plants()
    )


def max_biogas_ej():
    """
    Real Name: max biogas EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: []

    Maximun potencial of biogases production.
    """
    return _ext_constant_max_biogas_ej()


_ext_constant_max_biogas_ej = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_biogases_potential",
    {},
    _root,
    "_ext_constant_max_biogas_ej",
)


def new_pes_biogas():
    """
    Real Name: new PES biogas
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New annual primary energy supply of biogas.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_biogas_pes(time() + 1) - historic_biogas_pes(time()),
        lambda: ((max_biogas_ej() - pes_biogas_ej()) / max_biogas_ej())
        * adapt_growth_biogas()
        * pes_biogas_ej(),
    )


def past_biogas_growth():
    """
    Real Name: past biogas growth
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current growth patterns.
    """
    return _ext_constant_past_biogas_growth()


_ext_constant_past_biogas_growth = ExtConstant(
    "../energy.xlsx",
    "World",
    "average_historic_primary_energy_supply_biogas",
    {},
    _root,
    "_ext_constant_past_biogas_growth",
)


def pes_biogas_ej():
    """
    Real Name: PES Biogas EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Biogases primary energy supply. Includes all uses: heat, electricity, total final energy consumption, etc. The same share for final energy uses as well as the efficiency of transformation than for natural fossil gas are assumed.
    """
    return _integ_pes_biogas_ej()


_integ_pes_biogas_ej = Integ(
    lambda: new_pes_biogas(), lambda: 0.13135, "_integ_pes_biogas_ej"
)


def pes_biogas_for_chp():
    """
    Real Name: PES biogas for CHP
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply biogas for CHP plants.
    """
    return pes_biogas_ej() * share_pes_biogas_for_chp()


def pes_biogas_for_elec_plants():
    """
    Real Name: PES biogas for elec plants
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_elec_plants()


def pes_biogas_for_heatcom_plants():
    """
    Real Name: "PES biogas for heat-com plants"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply of heat in commercial Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_heatcom_plants()


def pes_biogas_for_tfc():
    """
    Real Name: PES biogas for TFC
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy supply biogas for total final consumption.
    """
    return np.minimum(ped_gases(), potential_pes_biogas_for_tfc())


def pes_tot_biogas_for_elec():
    """
    Real Name: PES tot biogas for elec
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply for generating electricity from biogas (including CHP plants).
    """
    return (
        pes_biogas_for_elec_plants()
        + fes_elec_from_biogas_in_chp_plants()
        + losses_chp_biogas() * share_efficiency_biogas_for_elec_in_chp_plants()
    )


def pes_tot_biogas_for_heatcom():
    """
    Real Name: "PES tot biogas for heat-com"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply for generating commercial heat from biogas (including CHP plants).
    """
    return (
        pes_biogas_for_heatcom_plants()
        + fes_heatcom_from_biogas_in_chp_plants()
        + losses_chp_biogas() * (1 - share_efficiency_biogas_for_elec_in_chp_plants())
    )


def potential_pes_biogas_for_tfc():
    """
    Real Name: Potential PES biogas for TFC
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential primary energy supply biogas for total final consumption.
    """
    return pes_biogas_ej() * share_pes_biogas_tfc()


def share_efficiency_biogas_for_elec_in_chp_plants():
    """
    Real Name: share efficiency biogas for elec in CHP plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return efficiency_biogas_for_elec_chp_plants() / (
        efficiency_biogas_for_elec_chp_plants()
        + efficiency_biogas_for_heat_chp_plants()
    )


def share_pes_biogas_for_chp():
    """
    Real Name: share PES biogas for CHP
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES biogas for CHP plants.
    """
    return _ext_constant_share_pes_biogas_for_chp()


_ext_constant_share_pes_biogas_for_chp = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_chp_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_chp",
)


def share_pes_biogas_for_elec():
    """
    Real Name: share PES biogas for elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_tot_biogas_for_elec() / pes_biogas_ej()


def share_pes_biogas_for_elec_plants():
    """
    Real Name: share PES biogas for elec plants
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES biogas for elec plants.
    """
    return _ext_constant_share_pes_biogas_for_elec_plants()


_ext_constant_share_pes_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_elec_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_elec_plants",
)


def share_pes_biogas_for_heat():
    """
    Real Name: share PES biogas for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pes_tot_biogas_for_heatcom() / pes_biogas_ej()


def share_pes_biogas_for_heatcom_plants():
    """
    Real Name: "share PES biogas for heat-com plants"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES biogas for commercial heat plants.
    """
    return _ext_constant_share_pes_biogas_for_heatcom_plants()


_ext_constant_share_pes_biogas_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_heat_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_heatcom_plants",
)


def share_pes_biogas_tfc():
    """
    Real Name: share PES biogas TFC
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Share of PES biogas for total final consumption.
    """
    return _ext_constant_share_pes_biogas_tfc()


_ext_constant_share_pes_biogas_tfc = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_tfc",
    {},
    _root,
    "_ext_constant_share_pes_biogas_tfc",
)
