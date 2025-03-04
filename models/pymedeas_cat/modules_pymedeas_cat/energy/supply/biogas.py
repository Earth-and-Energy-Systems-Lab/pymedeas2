"""
Module energy.supply.biogas
Translated using PySD version 3.14.2
"""

@component.add(
    name="adapt_growth_biogas",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "past_biogas_growth": 3, "nvs_5_years_ts": 1, "p_biogas": 2},
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
            + (p_biogas() - past_biogas_growth()) * (time() - 2015) / nvs_5_years_ts(),
            lambda: p_biogas(),
        ),
    )


@component.add(
    name="efficiency_biogas_for_elec_CHP_plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_biogas_for_elec_chp_plants",
        "__data__": "_ext_data_efficiency_biogas_for_elec_chp_plants",
        "time": 1,
    },
)
def efficiency_biogas_for_elec_chp_plants():
    """
    Efficiency of the transformation of biogas in elec in CHP plants.
    """
    return _ext_data_efficiency_biogas_for_elec_chp_plants(time())


_ext_data_efficiency_biogas_for_elec_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_biogas_for_elec_in_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_biogas_for_elec_chp_plants",
)


@component.add(
    name="efficiency_biogas_for_elec_plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_biogas_for_elec_plants",
        "__data__": "_ext_data_efficiency_biogas_for_elec_plants",
        "time": 1,
    },
)
def efficiency_biogas_for_elec_plants():
    """
    Efficiency of the transformation of biogas in elec plants.
    """
    return _ext_data_efficiency_biogas_for_elec_plants(time())


_ext_data_efficiency_biogas_for_elec_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_biogas_for_elec_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_biogas_for_elec_plants",
)


@component.add(
    name="efficiency_biogas_for_heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_heatcom_from_biogas_ej": 1, "pes_tot_biogas_for_heatcom": 1},
)
def efficiency_biogas_for_heat():
    """
    Efficiency of biogas for heat (from heat plants and CHP).
    """
    return zidz(fes_heatcom_from_biogas_ej(), pes_tot_biogas_for_heatcom())


@component.add(
    name="efficiency_biogas_for_heat_CHP_plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_biogas_for_heat_chp_plants",
        "__data__": "_ext_data_efficiency_biogas_for_heat_chp_plants",
        "time": 1,
    },
)
def efficiency_biogas_for_heat_chp_plants():
    """
    Efficiency of the transformation of biogas in heat in CHP plants.
    """
    return _ext_data_efficiency_biogas_for_heat_chp_plants(time())


_ext_data_efficiency_biogas_for_heat_chp_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_biogas_for_heat_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_biogas_for_heat_chp_plants",
)


@component.add(
    name="efficiency_biogas_for_heat_plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_biogas_for_heat_plants",
        "__data__": "_ext_data_efficiency_biogas_for_heat_plants",
        "time": 1,
    },
)
def efficiency_biogas_for_heat_plants():
    """
    Efficiency of the transformation of biogas in heat plants.
    """
    return _ext_data_efficiency_biogas_for_heat_plants(time())


_ext_data_efficiency_biogas_for_heat_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_biogas_for_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_biogas_for_heat_plants",
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
    "Catalonia",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_lookup_historic_biogas_pes",
)


@component.add(
    name="historic_share_PES_biogas_for_elec_plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_share_pes_biogas_for_elec_plants",
        "__data__": "_ext_data_historic_share_pes_biogas_for_elec_plants",
        "time": 1,
    },
)
def historic_share_pes_biogas_for_elec_plants():
    """
    Share of PES biogas for elec plants.
    """
    return _ext_data_historic_share_pes_biogas_for_elec_plants(time())


_ext_data_historic_share_pes_biogas_for_elec_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_for_elec_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_share_pes_biogas_for_elec_plants",
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
    name="max_biogas_for_TFC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_biogas_ej": 1, "share_pes_biogas_tfc": 1},
)
def max_biogas_for_tfc():
    """
    Maximum potential of biogas used directly as total final consumption.
    """
    return max_pe_biogas_ej() * share_pes_biogas_tfc()


@component.add(
    name="max_PE_biogas_EJ",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_pe_biogas_ej"},
)
def max_pe_biogas_ej():
    """
    Maximun potencial (primary energy) of biogases production.
    """
    return _ext_constant_max_pe_biogas_ej()


_ext_constant_max_pe_biogas_ej = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "max_PE_biogas",
    {},
    _root,
    {},
    "_ext_constant_max_pe_biogas_ej",
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
        "max_pe_biogas_ej": 2,
        "pes_biogas_ej": 2,
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
        lambda: ((max_pe_biogas_ej() - pes_biogas_ej()) / max_pe_biogas_ej())
        * adapt_growth_biogas()
        * pes_biogas_ej(),
    )


@component.add(
    name='"5_years_TS"', units="year", comp_type="Constant", comp_subtype="Normal"
)
def nvs_5_years_ts():
    return 5


@component.add(
    name="P_biogas",
    units="Dmnl/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_biogas"},
)
def p_biogas():
    """
    Projected annual growth.
    """
    return _ext_constant_p_biogas()


_ext_constant_p_biogas = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "p_biogas_growth",
    {},
    _root,
    {},
    "_ext_constant_p_biogas",
)


@component.add(
    name="P_biogas_elec",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_p_biogas_elec",
        "__lookup__": "_ext_lookup_p_biogas_elec",
    },
)
def p_biogas_elec(x, final_subs=None):
    return _ext_lookup_p_biogas_elec(x, final_subs)


_ext_lookup_p_biogas_elec = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "share_biogas",
    {},
    _root,
    {},
    "_ext_lookup_p_biogas_elec",
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
    Current growth patterns.
    """
    return _ext_constant_past_biogas_growth()


_ext_constant_past_biogas_growth = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
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
    depends_on={"pes_biogas_ej": 1, "share_pes_biogas_elec_plants": 1},
)
def pes_biogas_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas_ej() * share_pes_biogas_elec_plants()


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
    depends_on={"ped_gases": 1, "potential_pes_biogas_for_tfc": 1},
)
def pes_biogas_for_tfc():
    """
    Primary energy supply biogas for total final consumption.
    """
    return float(np.minimum(ped_gases(), potential_pes_biogas_for_tfc()))


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
    return zidz(
        efficiency_biogas_for_elec_chp_plants(),
        efficiency_biogas_for_elec_chp_plants()
        + efficiency_biogas_for_heat_chp_plants(),
    )


@component.add(
    name="share_PES_biogas_elec_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "historic_share_pes_biogas_for_elec_plants": 3,
        "nvs_5_years_ts": 1,
        "p_biogas_elec": 2,
    },
)
def share_pes_biogas_elec_plants():
    return if_then_else(
        time() < 2015,
        lambda: historic_share_pes_biogas_for_elec_plants(),
        lambda: if_then_else(
            time() < 2020,
            lambda: historic_share_pes_biogas_for_elec_plants()
            + (p_biogas_elec(time()) - historic_share_pes_biogas_for_elec_plants())
            * (time() - 2015)
            / nvs_5_years_ts(),
            lambda: p_biogas_elec(time()),
        ),
    )


@component.add(
    name="share_PES_biogas_for_CHP",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_pes_biogas_for_chp",
        "__data__": "_ext_data_share_pes_biogas_for_chp",
        "time": 1,
    },
)
def share_pes_biogas_for_chp():
    """
    Share of PES biogas for CHP plants.
    """
    return _ext_data_share_pes_biogas_for_chp(time())


_ext_data_share_pes_biogas_for_chp = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_for_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_biogas_for_chp",
)


@component.add(
    name="share_PES_biogas_for_elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_elec": 1, "pes_biogas_ej": 1},
)
def share_pes_biogas_for_elec():
    return zidz(pes_tot_biogas_for_elec(), pes_biogas_ej())


@component.add(
    name="share_PES_biogas_for_heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_heatcom": 1, "pes_biogas_ej": 1},
)
def share_pes_biogas_for_heat():
    return zidz(pes_tot_biogas_for_heatcom(), pes_biogas_ej())


@component.add(
    name='"share_PES_biogas_for_heat-com_plants"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_pes_biogas_for_heatcom_plants",
        "__data__": "_ext_data_share_pes_biogas_for_heatcom_plants",
        "time": 1,
    },
)
def share_pes_biogas_for_heatcom_plants():
    """
    Share of PES biogas for commercial heat plants.
    """
    return _ext_data_share_pes_biogas_for_heatcom_plants(time())


_ext_data_share_pes_biogas_for_heatcom_plants = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_for_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_biogas_for_heatcom_plants",
)


@component.add(
    name="share_PES_biogas_TFC",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_pes_biogas_tfc",
        "__data__": "_ext_data_share_pes_biogas_tfc",
        "time": 1,
    },
)
def share_pes_biogas_tfc():
    """
    Share of PES biogas for total final consumption.
    """
    return _ext_data_share_pes_biogas_tfc(time())


_ext_data_share_pes_biogas_tfc = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_tfc",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_biogas_tfc",
)
