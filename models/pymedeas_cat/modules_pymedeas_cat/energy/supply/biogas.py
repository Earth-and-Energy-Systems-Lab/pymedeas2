"""
Module energy.supply.biogas
Translated using PySD version 3.9.1
"""


@component.add(
    name="Desired biogas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "historic_biogas_pes": 3,
        "start_year_p_growth_res_elec": 3,
        "policy_biogas": 2,
    },
)
def desired_biogas():
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_biogas_pes(time()),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: historic_biogas_pes(end_hist_data())
            + (
                (
                    policy_biogas(start_year_p_growth_res_elec())
                    - historic_biogas_pes(end_hist_data())
                )
                / (start_year_p_growth_res_elec() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: policy_biogas(time()),
        ),
    )


@component.add(
    name="efficiency biogas for elec CHP plants",
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
    "../energy.xlsx",
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
    name="efficiency biogas for elec plants",
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
    "../energy.xlsx",
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
    name="efficiency biogas for heat",
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
    name="efficiency biogas for heat CHP plants",
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
    "../energy.xlsx",
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
    name="efficiency biogas for heat plants",
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
    "../energy.xlsx",
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
    name='"FES biogas for heat-com plants"',
    units="EJ",
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
    name="FES elec from biogas EJ",
    units="EJ",
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
    name="FES elec from biogas in CHP plants",
    units="EJ",
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
    name="FES elec from biogas in elec plants",
    units="EJ",
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
    name="FES elec from biogas TWh",
    units="TWh",
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
    name='"FES heat-com from biogas EJ"',
    units="EJ",
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
    name='"FES heat-com from biogas in CHP plants"',
    units="EJ",
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
    name="Historic biogas PES",
    units="EJ",
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
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_primary_energy_supply_biogas",
    {},
    _root,
    {},
    "_ext_lookup_historic_biogas_pes",
)


@component.add(
    name="Losses CHP biogas",
    units="EJ",
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
    name="max biogas for TFC",
    units="EJ",
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
    name="max PE biogas EJ",
    units="EJ",
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
    "../energy.xlsx",
    "Catalonia",
    "max_PE_biogas",
    {},
    _root,
    {},
    "_ext_constant_max_pe_biogas_ej",
)


@component.add(
    name="PES biogas",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_biogas": 2, "max_pe_biogas_ej": 2},
)
def pes_biogas():
    return if_then_else(
        desired_biogas() > max_pe_biogas_ej(),
        lambda: max_pe_biogas_ej(),
        lambda: desired_biogas(),
    )


@component.add(
    name="PES biogas for CHP",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas": 1, "share_pes_biogas_for_chp": 1},
)
def pes_biogas_for_chp():
    """
    Primary energy supply biogas for CHP plants.
    """
    return pes_biogas() * share_pes_biogas_for_chp()


@component.add(
    name="PES biogas for elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas": 1, "share_pes_biogas_for_elec_plants": 1},
)
def pes_biogas_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from biogas.
    """
    return pes_biogas() * share_pes_biogas_for_elec_plants()


@component.add(
    name='"PES biogas for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas": 1, "share_pes_biogas_for_heatcom_plants": 1},
)
def pes_biogas_for_heatcom_plants():
    """
    Primary energy supply of heat in commercial Heat plants from biogas.
    """
    return pes_biogas() * share_pes_biogas_for_heatcom_plants()


@component.add(
    name="PES biogas for TFC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "potential_pes_biogas_for_tfc": 1},
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
    name='"PES tot biogas for heat-com"',
    units="EJ",
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
    name="policy biogas",
    units="EJ",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_biogas",
        "__lookup__": "_ext_lookup_policy_biogas",
    },
)
def policy_biogas(x, final_subs=None):
    return _ext_lookup_policy_biogas(x, final_subs)


_ext_lookup_policy_biogas = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "p_biogas_energy",
    {},
    _root,
    {},
    "_ext_lookup_policy_biogas",
)


@component.add(
    name="Potential PES biogas for TFC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas": 1, "share_pes_biogas_tfc": 1},
)
def potential_pes_biogas_for_tfc():
    """
    Potential primary energy supply biogas for total final consumption.
    """
    return pes_biogas() * share_pes_biogas_tfc()


@component.add(
    name="share efficiency biogas for elec in CHP plants",
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
    name="share PES biogas for CHP",
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
    "../energy.xlsx",
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
    name="share PES biogas for elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_elec": 1, "pes_biogas": 1},
)
def share_pes_biogas_for_elec():
    return zidz(pes_tot_biogas_for_elec(), pes_biogas())


@component.add(
    name="share PES biogas for elec plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_pes_biogas_for_elec_plants",
        "__data__": "_ext_data_share_pes_biogas_for_elec_plants",
        "time": 1,
    },
)
def share_pes_biogas_for_elec_plants():
    """
    Share of PES biogas for elec plants.
    """
    return _ext_data_share_pes_biogas_for_elec_plants(time())


_ext_data_share_pes_biogas_for_elec_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_for_elec_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_biogas_for_elec_plants",
)


@component.add(
    name="share PES biogas for heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_tot_biogas_for_heatcom": 1, "pes_biogas": 1},
)
def share_pes_biogas_for_heat():
    return zidz(pes_tot_biogas_for_heatcom(), pes_biogas())


@component.add(
    name='"share PES biogas for heat-com plants"',
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
    "../energy.xlsx",
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
    name="share PES biogas TFC",
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
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_biogas_tfc",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_biogas_tfc",
)
