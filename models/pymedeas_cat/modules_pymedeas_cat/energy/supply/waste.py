"""
Module waste
Translated using PySD version 3.0.0
"""


@component.add(
    name="adapt growth waste",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def adapt_growth_waste():
    """
    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_waste_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_waste_growth()
            + (waste_change() - past_waste_growth()) * (time() - 2015) / 5,
            lambda: waste_change(),
        ),
    )


@component.add(
    name="efficiency waste for elec CHP plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_waste_for_elec_chp_plants():
    """
    Efficiency of the transformation of waste in elec in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_elec_chp_plants()


_ext_constant_efficiency_waste_for_elec_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_waste_for_elec_chp_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_waste_for_elec_chp_plants",
)


@component.add(
    name="efficiency waste for elec plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_waste_for_elec_plants():
    """
    Efficiency of the transformation of waste in elec plants.
    """
    return _ext_constant_efficiency_waste_for_elec_plants()


_ext_constant_efficiency_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_waste_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_waste_for_elec_plants",
)


@component.add(
    name="efficiency waste for heat CHP plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_waste_for_heat_chp_plants():
    """
    Efficiency of the transformation of waste in heat in CHP plants.
    """
    return _ext_constant_efficiency_waste_for_heat_chp_plants()


_ext_constant_efficiency_waste_for_heat_chp_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_waste_for_heat_CHP_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_waste_for_heat_chp_plants",
)


@component.add(
    name="efficiency waste for heat plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_waste_for_heat_plants():
    """
    Efficiency of the transformation of waste in heat plants.
    """
    return _ext_constant_efficiency_waste_for_heat_plants()


_ext_constant_efficiency_waste_for_heat_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_waste_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_efficiency_waste_for_heat_plants",
)


@component.add(
    name="FES elec from waste EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_waste_ej():
    """
    TFES electricity from waste.
    """
    return fes_elec_from_waste_in_chp_plants() + fes_elec_from_waste_in_elec_plants()


@component.add(
    name="FES elec from waste in CHP plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_waste_in_chp_plants():
    """
    Final energy supply of elec in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_elec_chp_plants()


@component.add(
    name="FES elec from waste in elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_waste_in_elec_plants():
    """
    Final energy supply of electricity in Elec plants from waste.
    """
    return pes_waste_for_elec_plants() * efficiency_waste_for_elec_plants()


@component.add(
    name="FES elec from waste TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_elec_from_waste_twh():
    """
    TFES electricity from waste.
    """
    return fes_elec_from_waste_ej() / ej_per_twh()


@component.add(
    name='"FES heat-com from waste EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_heatcom_from_waste_ej():
    """
    TFES commercial heat from waste.
    """
    return fes_waste_for_heatcom_plants() + fes_heatcom_from_waste_in_chp_plants()


@component.add(
    name='"FES heat-com from waste in CHP plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_heatcom_from_waste_in_chp_plants():
    """
    Final energy supply of commercial heat in CHP plants from waste.
    """
    return pes_waste_for_chp_plants() * efficiency_waste_for_heat_chp_plants()


@component.add(
    name='"FES waste for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_waste_for_heatcom_plants():
    """
    Final energy supply of heat in commercial Heat plants from waste.
    """
    return pes_waste_for_heatcom_plants() * efficiency_waste_for_heat_plants()


@component.add(
    name="Historic PES waste EJ",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_pes_waste_ej(x, final_subs=None):
    """
    Historic primary energy supply of waste (1990-2014).
    """
    return _ext_lookup_historic_pes_waste_ej(x, final_subs)


_ext_lookup_historic_pes_waste_ej = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_primary_energy_supply_of_waste",
    {},
    _root,
    {},
    "_ext_lookup_historic_pes_waste_ej",
)


@component.add(
    name="initial PES waste", units="EJ", comp_type="Constant", comp_subtype="External"
)
def initial_pes_waste():
    """
    Waste primary energy supply in 1995.
    """
    return _ext_constant_initial_pes_waste()


_ext_constant_initial_pes_waste = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_primary_energy_supply_from_waste",
    {},
    _root,
    {},
    "_ext_constant_initial_pes_waste",
)


@component.add(
    name="Losses CHP waste", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def losses_chp_waste():
    """
    Losses in waste CHP plants.
    """
    return (
        pes_waste_for_chp_plants()
        - fes_elec_from_waste_in_chp_plants()
        - fes_heatcom_from_waste_in_chp_plants()
    )


@component.add(
    name="max PE waste", units="EJ", comp_type="Constant", comp_subtype="External"
)
def max_pe_waste():
    """
    Maximun potencial of waste (primary energy supply).
    """
    return _ext_constant_max_pe_waste()


_ext_constant_max_pe_waste = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "max_PE_waste",
    {},
    _root,
    {},
    "_ext_constant_max_pe_waste",
)


@component.add(
    name="new waste supply EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_waste_supply_ej():
    """
    New annual waste primary energy supply.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_pes_waste_ej(time() + 1) - historic_pes_waste_ej(time()),
        lambda: if_then_else(
            max_pe_waste() == 0,
            lambda: pes_waste_ej() * p_waste_change(),
            lambda: ((max_pe_waste() - pes_waste_ej()) / max_pe_waste())
            * adapt_growth_waste()
            * pes_waste_ej(),
        ),
    )


@component.add(
    name="P waste change", units="1/Year", comp_type="Constant", comp_subtype="External"
)
def p_waste_change():
    """
    Annual PES growth depending on the policy of the scenario.
    """
    return _ext_constant_p_waste_change()


_ext_constant_p_waste_change = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_waste_growth",
    {},
    _root,
    {},
    "_ext_constant_p_waste_change",
)


@component.add(
    name="Past waste growth",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def past_waste_growth():
    """
    Past growth in PES of waste supply.
    """
    return _ext_constant_past_waste_growth()


_ext_constant_past_waste_growth = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_average_pes_from_waste_growth",
    {},
    _root,
    {},
    "_ext_constant_past_waste_growth",
)


@component.add(
    name='"PES tot waste for heat-com"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_tot_waste_for_heatcom():
    """
    Total primary energy supply for generating commercial heat from waste (including CHP plants).
    """
    return (
        pes_waste_for_heatcom_plants()
        + fes_heatcom_from_waste_in_chp_plants()
        + losses_chp_waste() * (1 - share_efficiency_waste_for_elec_in_chp_plants())
    )


@component.add(
    name="PES waste EJ", units="EJ", comp_type="Stateful", comp_subtype="Integ"
)
def pes_waste_ej():
    """
    Waste primary energy supply (includes industrial and municipal (renew and non-renew).
    """
    return _integ_pes_waste_ej()


_integ_pes_waste_ej = Integ(
    lambda: new_waste_supply_ej(), lambda: initial_pes_waste(), "_integ_pes_waste_ej"
)


@component.add(
    name="PES waste for CHP plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_waste_for_chp_plants():
    """
    Primary energy supply waste for CHP plants.
    """
    return pes_waste_ej() * share_pes_waste_for_chp()


@component.add(
    name="PES waste for elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_waste_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_elec_plants()


@component.add(
    name='"PES waste for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_waste_for_heatcom_plants():
    """
    Primary energy supply of commercial heat in Heat plants from waste.
    """
    return pes_waste_ej() * share_pes_waste_for_heatcom_plants()


@component.add(
    name="PES tot waste for elec",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_tot_waste_for_elec():
    """
    Total primary energy supply for generating electricity from biogas (including CHP plants).
    """
    return (
        pes_waste_for_elec_plants()
        + fes_elec_from_waste_in_chp_plants()
        + losses_chp_waste() * share_efficiency_waste_for_elec_in_chp_plants()
    )


@component.add(
    name="PES waste for TFC", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_waste_for_tfc():
    """
    Primary energy supply waste for total final consumption.
    """
    return pes_waste_ej() * share_pes_waste_tfc()


@component.add(
    name="share efficiency waste for elec in CHP plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_efficiency_waste_for_elec_in_chp_plants():
    return efficiency_waste_for_elec_chp_plants() / (
        efficiency_waste_for_elec_chp_plants() + efficiency_waste_for_heat_chp_plants()
    )


@component.add(
    name="share PES waste for CHP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_waste_for_chp():
    """
    Share of PES waste for CHP plants.
    """
    return _ext_constant_share_pes_waste_for_chp()


_ext_constant_share_pes_waste_for_chp = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_waste_for_chp",
    {},
    _root,
    {},
    "_ext_constant_share_pes_waste_for_chp",
)


@component.add(
    name="share PES waste for elec plants",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_waste_for_elec_plants():
    """
    Share of PES waste for elec plants.
    """
    return _ext_constant_share_pes_waste_for_elec_plants()


_ext_constant_share_pes_waste_for_elec_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_waste_for_elec_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_waste_for_elec_plants",
)


@component.add(
    name='"share PES waste for heat-com plants"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_waste_for_heatcom_plants():
    """
    Share of PES waste for commercial heat plants.
    """
    return _ext_constant_share_pes_waste_for_heatcom_plants()


_ext_constant_share_pes_waste_for_heatcom_plants = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_waste_for_heat_plants",
    {},
    _root,
    {},
    "_ext_constant_share_pes_waste_for_heatcom_plants",
)


@component.add(
    name="share PES waste TFC",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def share_pes_waste_tfc():
    """
    Share of PES waste for total final consumption.
    """
    return _ext_constant_share_pes_waste_tfc()


_ext_constant_share_pes_waste_tfc = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "share_pes_waste_tfc",
    {},
    _root,
    {},
    "_ext_constant_share_pes_waste_tfc",
)


@component.add(
    name="waste change", units="1/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def waste_change():
    """
    If GDP becomes negative, annual PES change follows it decreasing trends.
    """
    return if_then_else(
        annual_gdp_growth_rate_aut() < 0,
        lambda: annual_gdp_growth_rate_aut(),
        lambda: p_waste_change(),
    )
