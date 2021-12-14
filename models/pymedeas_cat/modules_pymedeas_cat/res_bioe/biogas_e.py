"""
Module biogas_e
Translated using PySD version 2.1.0
"""


def adapt_growth_biogas():
    """
    Real Name: adapt growth biogas
    Original Eqn: IF THEN ELSE(Time<2015, past biogas growth, IF THEN ELSE(Time<2020, past biogas growth+(P biogas-past biogas growth )*(Time-2015)/5, P biogas))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual growth per for biogas. Modeling of a soft transition from current
        historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_biogas_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_biogas_growth()
            + (p_biogas() - past_biogas_growth()) * (time() - 2015) / 5,
            lambda: p_biogas(),
        ),
    )


def efficiency_biogas_for_elec_chp_plants():
    """
    Real Name: efficiency biogas for elec CHP plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'efficiency_biogas_for_elec_in_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of biogas in elec in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_chp_plants()


def efficiency_biogas_for_elec_plants():
    """
    Real Name: efficiency biogas for elec plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'efficiency_biogas_for_elec_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of biogas in elec plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_plants()


def efficiency_biogas_for_heat():
    """
    Real Name: efficiency biogas for heat
    Original Eqn: "FES heat-com from biogas EJ"/"PES tot biogas for heat-com"
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Efficiency of biogas for heat (from heat plants and CHP).
    """
    return fes_heatcom_from_biogas_ej() / pes_tot_biogas_for_heatcom()


def efficiency_biogas_for_heat_chp_plants():
    """
    Real Name: efficiency biogas for heat CHP plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'efficiency_biogas_for_heat_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of biogas in heat in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_chp_plants()


def efficiency_biogas_for_heat_plants():
    """
    Real Name: efficiency biogas for heat plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'efficiency_biogas_for_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation of biogas in heat plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_plants()


def fes_biogas_for_heatcom_plants():
    """
    Real Name: "FES biogas for heat-com plants"
    Original Eqn: "PES biogas for heat-com plants"*efficiency biogas for heat plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of commercial heat in Heat plants from biogas.
    """
    return pes_biogas_for_heatcom_plants() * efficiency_biogas_for_heat_plants()


def fes_elec_from_biogas_ej():
    """
    Real Name: FES elec from biogas EJ
    Original Eqn: FES elec from biogas in CHP plants+FES elec from biogas in elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_in_chp_plants() + fes_elec_from_biogas_in_elec_plants()


def fes_elec_from_biogas_in_chp_plants():
    """
    Real Name: FES elec from biogas in CHP plants
    Original Eqn: PES biogas for CHP*efficiency biogas for elec CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of elec in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_elec_chp_plants()


def fes_elec_from_biogas_in_elec_plants():
    """
    Real Name: FES elec from biogas in elec plants
    Original Eqn: PES biogas for elec plants*efficiency biogas for elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of electricity in Elec plants from biogas.
    """
    return pes_biogas_for_elec_plants() * efficiency_biogas_for_elec_plants()


def fes_elec_from_biogas_twh():
    """
    Real Name: FES elec from biogas TWh
    Original Eqn: FES elec from biogas EJ/EJ per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_ej() / ej_per_twh()


def fes_heatcom_from_biogas_ej():
    """
    Real Name: "FES heat-com from biogas EJ"
    Original Eqn: "FES biogas for heat-com plants"+"FES heat-com from biogas in CHP plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    TFES commercial heat from biogas.
    """
    return fes_biogas_for_heatcom_plants() + fes_heatcom_from_biogas_in_chp_plants()


def fes_heatcom_from_biogas_in_chp_plants():
    """
    Real Name: "FES heat-com from biogas in CHP plants"
    Original Eqn: PES biogas for CHP*efficiency biogas for heat CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy supply of commercial heat in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_heat_chp_plants()


def historic_biogas_pes(x):
    """
    Real Name: Historic biogas PES
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_efficiencies', 'historic_primary_energy_supply_biogas')
    Units: EJ/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic production of biogases (1990-2014).
    """
    return _ext_lookup_historic_biogas_pes(x)


def losses_chp_biogas():
    """
    Real Name: Losses CHP biogas
    Original Eqn: PES biogas for CHP-"FES heat-com from biogas in CHP plants"-FES elec from biogas in CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Losses in biogas CHP plants.
    """
    return (
        pes_biogas_for_chp()
        - fes_heatcom_from_biogas_in_chp_plants()
        - fes_elec_from_biogas_in_chp_plants()
    )


def max_biogas_for_tfc():
    """
    Real Name: max biogas for TFC
    Original Eqn: max PE biogas EJ*share PES biogas TFC
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum potential of biogas used directly as total final consumption.
    """
    return max_pe_biogas_ej() * share_pes_biogas_tfc()


def max_pe_biogas_ej():
    """
    Real Name: max PE biogas EJ
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C52')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Maximun potencial (primary energy) of biogases production.
    """
    return _ext_constant_max_pe_biogas_ej()


def new_pes_biogas():
    """
    Real Name: new PES biogas
    Original Eqn: IF THEN ELSE(Time<2014, (Historic biogas PES(INTEGER(Time+1))-Historic biogas PES(INTEGER(Time))), ((max PE biogas EJ-PES Biogas EJ )/max PE biogas EJ)*adapt growth biogas*PES Biogas EJ)
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    New annual primary energy supply of biogas.
    """
    return if_then_else(
        time() < 2014,
        lambda: (
            historic_biogas_pes(integer(time() + 1))
            - historic_biogas_pes(integer(time()))
        ),
        lambda: ((max_pe_biogas_ej() - pes_biogas_ej()) / max_pe_biogas_ej())
        * adapt_growth_biogas()
        * pes_biogas_ej(),
    )


def p_biogas():
    """
    Real Name: P biogas
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C53')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Projected annual growth.
    """
    return _ext_constant_p_biogas()


def past_biogas_growth():
    """
    Real Name: past biogas growth
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'average_historic_primary_energy_supply_biogas')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Current growth patterns.
    """
    return _ext_constant_past_biogas_growth()


def pes_biogas_ej():
    """
    Real Name: PES Biogas EJ
    Original Eqn: INTEG ( new PES biogas, 0.00084)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Biogases primary energy supply. Includes all uses: heat, electricity,
        total final energy consumption, etc. The same share for final energy uses
        as well as the efficiency of transformation than for natural fossil gas
        are assumed.
    """
    return _integ_pes_biogas_ej()


def pes_biogas_for_chp():
    """
    Real Name: PES biogas for CHP
    Original Eqn: PES Biogas EJ*share PES biogas for CHP
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply biogas for CHP plants.
    """
    return pes_biogas_ej() * share_pes_biogas_for_chp()


def pes_biogas_for_elec_plants():
    """
    Real Name: PES biogas for elec plants
    Original Eqn: PES Biogas EJ*share PES biogas for elec plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_elec_plants()


def pes_biogas_for_heatcom_plants():
    """
    Real Name: "PES biogas for heat-com plants"
    Original Eqn: PES Biogas EJ*"share PES biogas for heat-com plants"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply of heat in commercial Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_heatcom_plants()


def pes_biogas_for_tfc():
    """
    Real Name: PES biogas for TFC
    Original Eqn: MIN(PED gases, Potential PES biogas for TFC)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy supply biogas for total final consumption.
    """
    return np.minimum(ped_gases(), potential_pes_biogas_for_tfc())


def pes_tot_biogas_for_elec():
    """
    Real Name: PES tot biogas for elec
    Original Eqn: PES biogas for elec plants+FES elec from biogas in CHP plants+Losses CHP biogas*share efficiency biogas for elec in CHP plants
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply for generating electricity from biogas
        (including CHP plants).
    """
    return (
        pes_biogas_for_elec_plants()
        + fes_elec_from_biogas_in_chp_plants()
        + losses_chp_biogas() * share_efficiency_biogas_for_elec_in_chp_plants()
    )


def pes_tot_biogas_for_heatcom():
    """
    Real Name: "PES tot biogas for heat-com"
    Original Eqn: "PES biogas for heat-com plants"+"FES heat-com from biogas in CHP plants"+Losses CHP biogas*(1-share efficiency biogas for elec in CHP plants)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply for generating commercial heat from biogas
        (including CHP plants).
    """
    return (
        pes_biogas_for_heatcom_plants()
        + fes_heatcom_from_biogas_in_chp_plants()
        + losses_chp_biogas() * (1 - share_efficiency_biogas_for_elec_in_chp_plants())
    )


def potential_pes_biogas_for_tfc():
    """
    Real Name: Potential PES biogas for TFC
    Original Eqn: PES Biogas EJ*share PES biogas TFC
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential primary energy supply biogas for total final consumption.
    """
    return pes_biogas_ej() * share_pes_biogas_tfc()


def share_efficiency_biogas_for_elec_in_chp_plants():
    """
    Real Name: share efficiency biogas for elec in CHP plants
    Original Eqn: efficiency biogas for elec CHP plants/(efficiency biogas for elec CHP plants+efficiency biogas for heat CHP plants)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return efficiency_biogas_for_elec_chp_plants() / (
        efficiency_biogas_for_elec_chp_plants()
        + efficiency_biogas_for_heat_chp_plants()
    )


def share_pes_biogas_for_chp():
    """
    Real Name: share PES biogas for CHP
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'share_pes_biogas_for_chp_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES biogas for CHP plants.
    """
    return _ext_constant_share_pes_biogas_for_chp()


def share_pes_biogas_for_elec():
    """
    Real Name: share PES biogas for elec
    Original Eqn: PES tot biogas for elec/PES Biogas EJ
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_tot_biogas_for_elec() / pes_biogas_ej()


def share_pes_biogas_for_elec_plants():
    """
    Real Name: share PES biogas for elec plants
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'share_pes_biogas_for_elec_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES biogas for elec plants.
    """
    return _ext_constant_share_pes_biogas_for_elec_plants()


def share_pes_biogas_for_heat():
    """
    Real Name: share PES biogas for heat
    Original Eqn: "PES tot biogas for heat-com"/PES Biogas EJ
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pes_tot_biogas_for_heatcom() / pes_biogas_ej()


def share_pes_biogas_for_heatcom_plants():
    """
    Real Name: "share PES biogas for heat-com plants"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'share_pes_biogas_for_heat_plants')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES biogas for commercial heat plants.
    """
    return _ext_constant_share_pes_biogas_for_heatcom_plants()


def share_pes_biogas_tfc():
    """
    Real Name: share PES biogas TFC
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'share_pes_biogas_tfc')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Share of PES biogas for total final consumption.
    """
    return _ext_constant_share_pes_biogas_tfc()


_ext_constant_efficiency_biogas_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_biogas_for_elec_in_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_elec_chp_plants",
)


_ext_constant_efficiency_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_biogas_for_elec_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_elec_plants",
)


_ext_constant_efficiency_biogas_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_biogas_for_heat_chp_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_heat_chp_plants",
)


_ext_constant_efficiency_biogas_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_biogas_for_heat_plants",
    {},
    _root,
    "_ext_constant_efficiency_biogas_for_heat_plants",
)


_ext_lookup_historic_biogas_pes = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    "_ext_lookup_historic_biogas_pes",
)


_ext_constant_max_pe_biogas_ej = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C52",
    {},
    _root,
    "_ext_constant_max_pe_biogas_ej",
)


_ext_constant_p_biogas = ExtConstant(
    "../../scenarios/scen_aut.xlsx", "BAU", "C53", {}, _root, "_ext_constant_p_biogas"
)


_ext_constant_past_biogas_growth = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "average_historic_primary_energy_supply_biogas",
    {},
    _root,
    "_ext_constant_past_biogas_growth",
)


_integ_pes_biogas_ej = Integ(
    lambda: new_pes_biogas(), lambda: 0.00084, "_integ_pes_biogas_ej"
)


_ext_constant_share_pes_biogas_for_chp = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_biogas_for_chp_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_chp",
)


_ext_constant_share_pes_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_biogas_for_elec_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_elec_plants",
)


_ext_constant_share_pes_biogas_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_biogas_for_heat_plants",
    {},
    _root,
    "_ext_constant_share_pes_biogas_for_heatcom_plants",
)


_ext_constant_share_pes_biogas_tfc = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_biogas_tfc",
    {},
    _root,
    "_ext_constant_share_pes_biogas_tfc",
)
