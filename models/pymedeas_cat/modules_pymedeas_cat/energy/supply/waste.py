"""
Module energy.supply.waste
Translated using PySD version 3.9.1
"""


@component.add(
    name="Desired waste for energy",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "historic_pes_waste_ej": 3,
        "policy_waste": 2,
        "start_year_p_growth_res_elec": 3,
    },
)
def desired_waste_for_energy():
    """
    Total amount of waste used for energy consumption according to policies.
    """
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_pes_waste_ej(time()),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: historic_pes_waste_ej(end_hist_data())
            + (
                (
                    policy_waste(start_year_p_growth_res_elec())
                    - historic_pes_waste_ej(end_hist_data())
                )
                / (start_year_p_growth_res_elec() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: policy_waste(time()),
        ),
    )


@component.add(
    name="efficiency waste for elec CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_waste_for_elec_chp_plants",
        "__data__": "_ext_data_efficiency_waste_for_elec_chp_plants",
        "time": 1,
    },
)
def efficiency_waste_for_elec_chp_plants():
    """
    Efficiency of the transformation of waste in elec in CHP plants.
    """
    return _ext_data_efficiency_waste_for_elec_chp_plants(time())


_ext_data_efficiency_waste_for_elec_chp_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_waste_for_elec_chp_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_waste_for_elec_chp_plants",
)


@component.add(
    name="efficiency waste for elec plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_waste_for_elec_plants",
        "__data__": "_ext_data_efficiency_waste_for_elec_plants",
        "time": 1,
    },
)
def efficiency_waste_for_elec_plants():
    """
    Efficiency of the transformation of waste in elec plants.
    """
    return _ext_data_efficiency_waste_for_elec_plants(time())


_ext_data_efficiency_waste_for_elec_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_waste_for_elec_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_waste_for_elec_plants",
)


@component.add(
    name="efficiency waste for heat CHP plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_waste_for_heat_chp_plants",
        "__data__": "_ext_data_efficiency_waste_for_heat_chp_plants",
        "time": 1,
    },
)
def efficiency_waste_for_heat_chp_plants():
    """
    Efficiency of the transformation of waste in heat in CHP plants.
    """
    return _ext_data_efficiency_waste_for_heat_chp_plants(time())


_ext_data_efficiency_waste_for_heat_chp_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_waste_for_heat_CHP_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_waste_for_heat_chp_plants",
)


@component.add(
    name="efficiency waste for heat plants",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_efficiency_waste_for_heat_plants",
        "__data__": "_ext_data_efficiency_waste_for_heat_plants",
        "time": 1,
    },
)
def efficiency_waste_for_heat_plants():
    """
    Efficiency of the transformation of waste in heat plants.
    """
    return _ext_data_efficiency_waste_for_heat_plants(time())


_ext_data_efficiency_waste_for_heat_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "efficiency_waste_for_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_efficiency_waste_for_heat_plants",
)


@component.add(
    name="FES elec from waste EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_elec_from_waste_in_chp_plants": 1,
        "fes_elec_from_waste_in_elec_plants": 1,
    },
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
    depends_on={
        "pes_waste_for_chp_plants": 1,
        "efficiency_waste_for_elec_chp_plants": 1,
    },
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
    depends_on={"pes_waste_for_elec_plants": 1, "efficiency_waste_for_elec_plants": 1},
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
    depends_on={"fes_elec_from_waste_ej": 1, "ej_per_twh": 1},
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
    depends_on={
        "fes_waste_for_heatcom_plants": 1,
        "fes_heatcom_from_waste_in_chp_plants": 1,
    },
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
    depends_on={
        "pes_waste_for_chp_plants": 1,
        "efficiency_waste_for_heat_chp_plants": 1,
    },
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
    depends_on={
        "pes_waste_for_heatcom_plants": 1,
        "efficiency_waste_for_heat_plants": 1,
    },
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
    depends_on={
        "__external__": "_ext_lookup_historic_pes_waste_ej",
        "__lookup__": "_ext_lookup_historic_pes_waste_ej",
    },
)
def historic_pes_waste_ej(x, final_subs=None):
    """
    Historic primary energy supply of waste (1990-2014).
    """
    return _ext_lookup_historic_pes_waste_ej(x, final_subs)


_ext_lookup_historic_pes_waste_ej = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_primary_energy_supply_of_waste",
    {},
    _root,
    {},
    "_ext_lookup_historic_pes_waste_ej",
)


@component.add(
    name="historic share PES waste for CHP",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_share_pes_waste_for_chp",
        "__lookup__": "_ext_lookup_historic_share_pes_waste_for_chp",
    },
)
def historic_share_pes_waste_for_chp(x, final_subs=None):
    """
    Share of PES waste for CHP plants.
    """
    return _ext_lookup_historic_share_pes_waste_for_chp(x, final_subs)


_ext_lookup_historic_share_pes_waste_for_chp = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_waste_for_chp",
    {},
    _root,
    {},
    "_ext_lookup_historic_share_pes_waste_for_chp",
)


@component.add(
    name="historic share PES waste for elec plants",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_share_pes_waste_for_elec_plants",
        "__lookup__": "_ext_lookup_historic_share_pes_waste_for_elec_plants",
    },
)
def historic_share_pes_waste_for_elec_plants(x, final_subs=None):
    """
    Share of PES waste for elec plants.
    """
    return _ext_lookup_historic_share_pes_waste_for_elec_plants(x, final_subs)


_ext_lookup_historic_share_pes_waste_for_elec_plants = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_waste_for_elec_plants",
    {},
    _root,
    {},
    "_ext_lookup_historic_share_pes_waste_for_elec_plants",
)


@component.add(
    name="Losses CHP waste",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_waste_for_chp_plants": 1,
        "fes_elec_from_waste_in_chp_plants": 1,
        "fes_heatcom_from_waste_in_chp_plants": 1,
    },
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
    name="max PE waste",
    units="EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_max_pe_waste"},
)
def max_pe_waste():
    """
    Maximun potencial of waste (primary energy supply).
    """
    return _ext_constant_max_pe_waste()


_ext_constant_max_pe_waste = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "max_PE_waste",
    {},
    _root,
    {},
    "_ext_constant_max_pe_waste",
)


@component.add(
    name="PES tot waste for elec",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_waste_for_elec_plants": 1,
        "fes_elec_from_waste_in_chp_plants": 1,
        "losses_chp_waste": 1,
        "share_efficiency_waste_for_elec_in_chp_plants": 1,
    },
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
    name='"PES tot waste for heat-com"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_waste_for_heatcom_plants": 1,
        "fes_heatcom_from_waste_in_chp_plants": 1,
        "losses_chp_waste": 1,
        "share_efficiency_waste_for_elec_in_chp_plants": 1,
    },
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
    name="PES waste",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_waste_for_energy": 2, "max_pe_waste": 2},
)
def pes_waste():
    """
    Limited due to a maximum capacity of waste for energy defined
    """
    return if_then_else(
        desired_waste_for_energy() > max_pe_waste(),
        lambda: max_pe_waste(),
        lambda: desired_waste_for_energy(),
    )


@component.add(
    name="PES waste for CHP plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_waste": 1, "share_pes_waste_for_chp": 1},
)
def pes_waste_for_chp_plants():
    """
    Primary energy supply waste for CHP plants.
    """
    return pes_waste() * share_pes_waste_for_chp()


@component.add(
    name="PES waste for elec plants",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_waste": 1, "share_pes_waste_for_elec_plants": 1},
)
def pes_waste_for_elec_plants():
    """
    Primary energy supply of heat in Heat plants from waste.
    """
    return pes_waste() * share_pes_waste_for_elec_plants()


@component.add(
    name='"PES waste for heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_waste": 1, "share_pes_waste_for_heatcom_plants": 1},
)
def pes_waste_for_heatcom_plants():
    """
    Primary energy supply of commercial heat in Heat plants from waste.
    """
    return pes_waste() * share_pes_waste_for_heatcom_plants()


@component.add(
    name="PES waste for TFC",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_waste": 1, "share_pes_waste_for_tfc": 1},
)
def pes_waste_for_tfc():
    """
    Primary energy supply waste for total final consumption.
    """
    return pes_waste() * share_pes_waste_for_tfc()


@component.add(
    name="Policy waste",
    units="EJ/Year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_waste",
        "__lookup__": "_ext_lookup_policy_waste",
    },
)
def policy_waste(x, final_subs=None):
    return _ext_lookup_policy_waste(x, final_subs)


_ext_lookup_policy_waste = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "p_waste_energy",
    {},
    _root,
    {},
    "_ext_lookup_policy_waste",
)


@component.add(
    name="policy waste for electricity",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_waste_for_electricity",
        "__lookup__": "_ext_lookup_policy_waste_for_electricity",
    },
)
def policy_waste_for_electricity(x, final_subs=None):
    return _ext_lookup_policy_waste_for_electricity(x, final_subs)


_ext_lookup_policy_waste_for_electricity = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "share_waste_elec",
    {},
    _root,
    {},
    "_ext_lookup_policy_waste_for_electricity",
)


@component.add(
    name="share efficiency waste for elec in CHP plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_waste_for_elec_chp_plants": 2,
        "efficiency_waste_for_heat_chp_plants": 1,
    },
)
def share_efficiency_waste_for_elec_in_chp_plants():
    return zidz(
        efficiency_waste_for_elec_chp_plants(),
        efficiency_waste_for_elec_chp_plants() + efficiency_waste_for_heat_chp_plants(),
    )


@component.add(
    name="share PES waste CHP vs CHP and electricity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_share_pes_waste_for_chp": 2,
        "historic_share_pes_waste_for_elec_plants": 1,
    },
)
def share_pes_waste_chp_vs_chp_and_electricity():
    return historic_share_pes_waste_for_chp(time()) / (
        historic_share_pes_waste_for_chp(time())
        + historic_share_pes_waste_for_elec_plants(time())
    )


@component.add(
    name="share PES waste for CHP",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "end_hist_data": 1,
        "historic_share_pes_waste_for_chp": 1,
        "share_pes_waste_chp_vs_chp_and_electricity": 1,
        "share_pes_waste_for_elec_plants": 1,
    },
)
def share_pes_waste_for_chp():
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_share_pes_waste_for_chp(time()),
        lambda: share_pes_waste_chp_vs_chp_and_electricity()
        * share_pes_waste_for_elec_plants(),
    )


@component.add(
    name="share PES waste for elec plants",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "historic_share_pes_waste_for_elec_plants": 3,
        "policy_waste_for_electricity": 2,
        "start_year_p_growth_res_elec": 3,
    },
)
def share_pes_waste_for_elec_plants():
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_share_pes_waste_for_elec_plants(time()),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: historic_share_pes_waste_for_elec_plants(end_hist_data())
            + (
                (
                    policy_waste_for_electricity(start_year_p_growth_res_elec())
                    - historic_share_pes_waste_for_elec_plants(end_hist_data())
                )
                / (start_year_p_growth_res_elec() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: policy_waste_for_electricity(time()),
        ),
    )


@component.add(
    name='"share PES waste for heat-com plants"',
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_share_pes_waste_for_heatcom_plants",
        "__data__": "_ext_data_share_pes_waste_for_heatcom_plants",
        "time": 1,
    },
)
def share_pes_waste_for_heatcom_plants():
    """
    Share of PES waste for commercial heat plants.
    """
    return _ext_data_share_pes_waste_for_heatcom_plants(time())


_ext_data_share_pes_waste_for_heatcom_plants = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "year_waste_biogas",
    "share_pes_waste_for_heat_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_share_pes_waste_for_heatcom_plants",
)


@component.add(
    name="share PES waste for TFC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_pes_waste_for_heatcom_plants": 1,
        "share_pes_waste_for_elec_plants": 1,
        "share_pes_waste_for_chp": 1,
    },
)
def share_pes_waste_for_tfc():
    return (
        1
        - share_pes_waste_for_heatcom_plants()
        - share_pes_waste_for_elec_plants()
        - share_pes_waste_for_chp()
    )
