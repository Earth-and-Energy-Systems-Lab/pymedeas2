"""
Module biogas
Translated using PySD version 3.0.0
"""


@component.add(
    name="adapt growth biogas",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
            + (growth_biogas() - past_biogas_growth()) * (time() - 2015) / 5,
            lambda: growth_biogas(),
        ),
    )


@component.add(
    name="biogas evol", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def biogas_evol():
    """
    This variable represents the projected annual growth in relation to past growth trends.
    """
    return _ext_constant_biogas_evol()


_ext_constant_biogas_evol = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_biogas_evol",
    {},
    _root,
    {},
    "_ext_constant_biogas_evol",
)


@component.add(
    name="efficiency biogas for elec CHP plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_biogas_for_elec_chp_plants():
    """
    Efficiency of the transformation of biogas in elec in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_chp_plants()


_ext_constant_efficiency_biogas_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_in_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_elec_chp_plants",
)


@component.add(
    name="efficiency biogas for elec plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_biogas_for_elec_plants():
    """
    Efficiency of the transformation of biogas in elec plants.
    """
    return _ext_constant_efficiency_biogas_for_elec_plants()


_ext_constant_efficiency_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_elec_plants",
)


@component.add(
    name="efficiency biogas for heat CHP plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_biogas_for_heat_chp_plants():
    """
    Efficiency of the transformation of biogas in heat in CHP plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_chp_plants()


_ext_constant_efficiency_biogas_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_heat_chp_plants",
)


@component.add(
    name="efficiency biogas for heat plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_biogas_for_heat_plants():
    """
    Efficiency of the transformation of biogas in heat plants.
    """
    return _ext_constant_efficiency_biogas_for_heat_plants()


_ext_constant_efficiency_biogas_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_biogas_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_biogas_for_heat_plants",
)


@component.add(
    name='"FES biogas for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_biogas_for_heatcom_plants():
    """
    Final energy supply of commercial heat in Heat plants from biogas.
    """
    return pes_biogas_for_heatcom_plants() * efficiency_biogas_for_heat_plants()


@component.add(
    name="FES elec from biogas EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_biogas_ej():
    """
    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_in_chp_plants() + fes_elec_from_biogas_in_elec_plants()


@component.add(
    name="FES elec from biogas in CHP plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_biogas_in_chp_plants():
    """
    Final energy supply of elec in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_elec_chp_plants()


@component.add(
    name="FES elec from biogas in elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_biogas_in_elec_plants():
    """
    Final energy supply of electricity in Elec plants from biogas.
    """
    return pes_biogas_for_elec_plants() * efficiency_biogas_for_elec_plants()


@component.add(
    name="FES elec from biogas TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_biogas_twh():
    """
    TFES electricity from biogas.
    """
    return fes_elec_from_biogas_ej() / ej_per_twh()


@component.add(
    name='"FES heat-com from biogas EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_heatcom_from_biogas_ej():
    """
    TFES commercial heat from biogas.
    """
    return fes_biogas_for_heatcom_plants() + fes_heatcom_from_biogas_in_chp_plants()


@component.add(
    name='"FES heat-com from biogas in CHP plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_heatcom_from_biogas_in_chp_plants():
    """
    Final energy supply of commercial heat in CHP plants from biogas.
    """
    return pes_biogas_for_chp() * efficiency_biogas_for_heat_chp_plants()


@component.add(
    name="growth biogas", units="1/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def growth_biogas():
    """
    Biogases growth function of growth past trends
    """
    return biogas_evol() * past_biogas_growth()


@component.add(
    name="Historic biogas PES",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_biogas_pes(x, final_subs=None):
    """
    Historic production of biogases (1990-2014).
    """
    return _ext_lookup_historic_biogas_pes(x, final_subs)


_ext_lookup_historic_biogas_pes = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_lookup_historic_biogas_pes",
)


@component.add(
    name="Losses CHP biogas", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
    name="max biogas EJ", units="EJ", comp_type="Constant", comp_subtype="External"
)
def max_biogas_ej():
    """
    Maximun potencial of biogases production.
    """
    return _ext_constant_max_biogas_ej()


_ext_constant_max_biogas_ej = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_biogases_potential",
    {},
    _root,
    {},
    "_ext_constant_max_biogas_ej",
)


@component.add(
    name="new PES biogas", units="EJ/year", comp_type="Auxiliary", comp_subtype="Normal"
)
def new_pes_biogas():
    """
    New annual primary energy supply of biogas.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_biogas_pes(time() + 1) - historic_biogas_pes(time()),
        lambda: ((max_biogas_ej() - pes_biogas_ej()) / max_biogas_ej())
        * adapt_growth_biogas()
        * pes_biogas_ej(),
    )


@component.add(
    name="past biogas growth",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
)
def past_biogas_growth():
    """
    Current growth patterns.
    """
    return _ext_constant_past_biogas_growth()


_ext_constant_past_biogas_growth = ExtConstant(
    "../energy.xlsx",
    "World",
    "average_historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_constant_past_biogas_growth",
)


@component.add(
    name="PES Biogas EJ", units="EJ", comp_type="Stateful", comp_subtype="Integ"
)
def pes_biogas_ej():
    """
    Biogases primary energy supply. Includes all uses: heat, electricity, total final energy consumption, etc. The same share for final energy uses as well as the efficiency of transformation than for natural fossil gas are assumed.
    """
    return _integ_pes_biogas_ej()


_integ_pes_biogas_ej = Integ(
    lambda: new_pes_biogas(), lambda: 0.13135, "_integ_pes_biogas_ej"
)


@component.add(
    name="PES biogas for CHP", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_biogas_for_chp():
    """
    Primary energy supply biogas for CHP plants.
    """
    return pes_biogas_ej() * share_pes_biogas_for_chp()


@component.add(
    name="PES biogas for elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_biogas_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_elec_plants()


@component.add(
    name='"PES biogas for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_biogas_for_heatcom_plants():
    """
    Primary energy supply of heat in commercial Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_for_heatcom_plants()


@component.add(
    name="PES biogas for TFC", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_biogas_for_tfc():
    """
    Primary energy supply biogas for total final consumption.
    """
    return np.minimum(ped_gases(), potential_pes_biogas_for_tfc())


@component.add(
    name="PES tot biogas for elec",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name='"PES tot biogas for heat-com"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="Potential PES biogas for TFC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def potential_pes_biogas_for_tfc():
    """
    Potential primary energy supply biogas for total final consumption.
    """
    return pes_biogas_ej() * share_pes_biogas_tfc()


@component.add(
    name="share efficiency biogas for elec in CHP plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_efficiency_biogas_for_elec_in_chp_plants():
    return efficiency_biogas_for_elec_chp_plants() / (
        efficiency_biogas_for_elec_chp_plants()
        + efficiency_biogas_for_heat_chp_plants()
    )


@component.add(
    name="share PES biogas for CHP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_biogas_for_chp():
    """
    Share of PES biogas for CHP plants.
    """
    return _ext_constant_share_pes_biogas_for_chp()


_ext_constant_share_pes_biogas_for_chp = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_chp",
)


@component.add(
    name="share PES biogas for elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_pes_biogas_for_elec():
    return pes_tot_biogas_for_elec() / pes_biogas_ej()


@component.add(
    name="share PES biogas for elec plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_biogas_for_elec_plants():
    """
    Share of PES biogas for elec plants.
    """
    return _ext_constant_share_pes_biogas_for_elec_plants()


_ext_constant_share_pes_biogas_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_elec_plants",
)


@component.add(
    name="share PES biogas for heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_pes_biogas_for_heat():
    return pes_tot_biogas_for_heatcom() / pes_biogas_ej()


@component.add(
    name='"share PES biogas for heat-com plants"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_biogas_for_heatcom_plants():
    """
    Share of PES biogas for commercial heat plants.
    """
    return _ext_constant_share_pes_biogas_for_heatcom_plants()


_ext_constant_share_pes_biogas_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_for_heatcom_plants",
)


@component.add(
    name="share PES biogas TFC",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_biogas_tfc():
    """
    Share of PES biogas for total final consumption.
    """
    return _ext_constant_share_pes_biogas_tfc()


_ext_constant_share_pes_biogas_tfc = ExtConstant(
    "../energy.xlsx",
    "World",
    "share_pes_biogas_tfc",
    {},
    _root,
    {},
    "_ext_constant_share_pes_biogas_tfc",
)
