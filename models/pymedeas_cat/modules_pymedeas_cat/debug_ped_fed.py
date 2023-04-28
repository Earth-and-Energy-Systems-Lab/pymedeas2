"""
Module debug_ped_fed
Translated using PySD version 3.9.1
"""


@component.add(
    name="DEBUG demand electricity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_demand_ej": 1},
)
def debug_demand_electricity():
    return total_fe_elec_demand_ej()


@component.add(
    name="DEBUG FED gases",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def debug_fed_gases():
    return float(required_fed_by_fuel_before_heat_correction().loc["gases"])


@component.add(
    name="DEBUG FED liquids",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def debug_fed_liquids():
    return float(required_fed_by_fuel_before_heat_correction().loc["liquids"])


@component.add(
    name="DEBUG FED solids",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel_before_heat_correction": 1},
)
def debug_fed_solids():
    return float(required_fed_by_fuel_before_heat_correction().loc["solids"])


@component.add(
    name="DEBUG historic FEC electricity",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_fec_electricity",
        "__lookup__": "_ext_lookup_debug_historic_fec_electricity",
    },
)
def debug_historic_fec_electricity(x, final_subs=None):
    return _ext_lookup_debug_historic_fec_electricity(x, final_subs)


_ext_lookup_debug_historic_fec_electricity = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec",
    "electricity_fec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_fec_electricity",
)


@component.add(
    name="DEBUG historic FEC gases",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_fec_gases",
        "__lookup__": "_ext_lookup_debug_historic_fec_gases",
    },
)
def debug_historic_fec_gases(x, final_subs=None):
    return _ext_lookup_debug_historic_fec_gases(x, final_subs)


_ext_lookup_debug_historic_fec_gases = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec",
    "gases_fec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_fec_gases",
)


@component.add(
    name="DEBUG historic FEC liquids",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_fec_liquids",
        "__lookup__": "_ext_lookup_debug_historic_fec_liquids",
    },
)
def debug_historic_fec_liquids(x, final_subs=None):
    return _ext_lookup_debug_historic_fec_liquids(x, final_subs)


_ext_lookup_debug_historic_fec_liquids = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec",
    "liquids_fec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_fec_liquids",
)


@component.add(
    name="DEBUG historic FEC solids",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_fec_solids",
        "__lookup__": "_ext_lookup_debug_historic_fec_solids",
    },
)
def debug_historic_fec_solids(x, final_subs=None):
    return _ext_lookup_debug_historic_fec_solids(x, final_subs)


_ext_lookup_debug_historic_fec_solids = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec",
    "solids_fec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_fec_solids",
)


@component.add(
    name="DEBUG historic PEC electricity", comp_type="Constant", comp_subtype="Normal"
)
def debug_historic_pec_electricity():
    return 0


@component.add(
    name="DEBUG historic PEC gases",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_pec_gases",
        "__lookup__": "_ext_lookup_debug_historic_pec_gases",
    },
)
def debug_historic_pec_gases(x, final_subs=None):
    return _ext_lookup_debug_historic_pec_gases(x, final_subs)


_ext_lookup_debug_historic_pec_gases = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_pec",
    "gases_pec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_pec_gases",
)


@component.add(
    name="DEBUG historic PEC liquids",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_pec_liquids",
        "__lookup__": "_ext_lookup_debug_historic_pec_liquids",
    },
)
def debug_historic_pec_liquids(x, final_subs=None):
    return _ext_lookup_debug_historic_pec_liquids(x, final_subs)


_ext_lookup_debug_historic_pec_liquids = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_pec",
    "liquids_pec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_pec_liquids",
)


@component.add(
    name="DEBUG historic PEC solids",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_historic_pec_solids",
        "__lookup__": "_ext_lookup_debug_historic_pec_solids",
    },
)
def debug_historic_pec_solids(x, final_subs=None):
    return _ext_lookup_debug_historic_pec_solids(x, final_subs)


_ext_lookup_debug_historic_pec_solids = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_pec",
    "solids_pec",
    {},
    _root,
    {},
    "_ext_lookup_debug_historic_pec_solids",
)


@component.add(
    name="DEBUG PED gases",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1},
)
def debug_ped_gases():
    return ped_gases()


@component.add(
    name="DEBUG PED liquids",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1},
)
def debug_ped_liquids():
    return ped_liquids()


@component.add(
    name="DEBUG PED solids",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_solids": 1},
)
def debug_ped_solids():
    return ped_solids()


@component.add(
    name="DEBUG supply electricity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_electricity": 1},
)
def debug_supply_electricity():
    return pes_electricity()


@component.add(
    name="DEBUG supply gases",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_gases": 1},
)
def debug_supply_gases():
    return pes_gases()


@component.add(
    name="DEBUG supply liquids",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_liquids": 1},
)
def debug_supply_liquids():
    return pes_liquids()


@component.add(
    name="DEBUG supply solids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids": 1},
)
def debug_supply_solids():
    return pes_solids()


@component.add(
    name="PES electricity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_elec_generation_twh_cat": 1},
)
def pes_electricity():
    """
    1 Terawatt hour [TWh] = 0.0036 Exajoule [EJ]
    """
    return total_fe_elec_generation_twh_cat() * 0.0036
