"""
Module debug_sectors
Translated using PySD version 3.9.1
"""


@component.add(
    name="DEBUG FED historic sector domestic",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_fed_historic_sector_domestic",
        "__lookup__": "_ext_lookup_debug_fed_historic_sector_domestic",
    },
)
def debug_fed_historic_sector_domestic(x, final_subs=None):
    return _ext_lookup_debug_fed_historic_sector_domestic(x, final_subs)


_ext_lookup_debug_fed_historic_sector_domestic = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_househ",
    "solids_fec_househ",
    {"final sources": ["solids"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_debug_fed_historic_sector_domestic",
)

_ext_lookup_debug_fed_historic_sector_domestic.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_househ",
    "liquids_fec_househ",
    {"final sources": ["liquids"]},
)

_ext_lookup_debug_fed_historic_sector_domestic.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_househ",
    "gases_fec_househ",
    {"final sources": ["gases"]},
)

_ext_lookup_debug_fed_historic_sector_domestic.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_househ",
    "electricity_fec_househ",
    {"final sources": ["electricity"]},
)

_ext_lookup_debug_fed_historic_sector_domestic.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_househ",
    "heat_fec_househ",
    {"final sources": ["heat"]},
)


@component.add(
    name="DEBUG FED historic sector industrial",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_fed_historic_sector_industrial",
        "__lookup__": "_ext_lookup_debug_fed_historic_sector_industrial",
    },
)
def debug_fed_historic_sector_industrial(x, final_subs=None):
    return _ext_lookup_debug_fed_historic_sector_industrial(x, final_subs)


_ext_lookup_debug_fed_historic_sector_industrial = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_indus",
    "solids_fec_indus",
    {"final sources": ["solids"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_debug_fed_historic_sector_industrial",
)

_ext_lookup_debug_fed_historic_sector_industrial.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_indus",
    "liquids_fec_indus",
    {"final sources": ["liquids"]},
)

_ext_lookup_debug_fed_historic_sector_industrial.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_indus",
    "gases_fec_indus",
    {"final sources": ["gases"]},
)

_ext_lookup_debug_fed_historic_sector_industrial.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_indus",
    "electricity_fec_indus",
    {"final sources": ["electricity"]},
)

_ext_lookup_debug_fed_historic_sector_industrial.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_indus",
    "heat_fec_indus",
    {"final sources": ["heat"]},
)


@component.add(
    name="DEBUG FED historic sector primari",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_fed_historic_sector_primari",
        "__lookup__": "_ext_lookup_debug_fed_historic_sector_primari",
    },
)
def debug_fed_historic_sector_primari(x, final_subs=None):
    return _ext_lookup_debug_fed_historic_sector_primari(x, final_subs)


_ext_lookup_debug_fed_historic_sector_primari = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_prim",
    "solids_fec_prim",
    {"final sources": ["solids"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_debug_fed_historic_sector_primari",
)

_ext_lookup_debug_fed_historic_sector_primari.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_prim",
    "liquids_fec_prim",
    {"final sources": ["liquids"]},
)

_ext_lookup_debug_fed_historic_sector_primari.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_prim",
    "gases_fec_prim",
    {"final sources": ["gases"]},
)

_ext_lookup_debug_fed_historic_sector_primari.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_prim",
    "electricity_fec_prim",
    {"final sources": ["electricity"]},
)

_ext_lookup_debug_fed_historic_sector_primari.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_prim",
    "heat_fec_prim",
    {"final sources": ["heat"]},
)


@component.add(
    name="DEBUG FED historic sector serveis",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_fed_historic_sector_serveis",
        "__lookup__": "_ext_lookup_debug_fed_historic_sector_serveis",
    },
)
def debug_fed_historic_sector_serveis(x, final_subs=None):
    return _ext_lookup_debug_fed_historic_sector_serveis(x, final_subs)


_ext_lookup_debug_fed_historic_sector_serveis = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_serveis",
    "solids_fec_serveis",
    {"final sources": ["solids"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_debug_fed_historic_sector_serveis",
)

_ext_lookup_debug_fed_historic_sector_serveis.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_serveis",
    "liquids_fec_serveis",
    {"final sources": ["liquids"]},
)

_ext_lookup_debug_fed_historic_sector_serveis.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_serveis",
    "gases_fec_serveis",
    {"final sources": ["gases"]},
)

_ext_lookup_debug_fed_historic_sector_serveis.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_serveis",
    "electricity_fec_serveis",
    {"final sources": ["electricity"]},
)

_ext_lookup_debug_fed_historic_sector_serveis.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_serveis",
    "heat_fec_serveis",
    {"final sources": ["heat"]},
)


@component.add(
    name="DEBUG FED historic sector transports",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_debug_fed_historic_sector_transports",
        "__lookup__": "_ext_lookup_debug_fed_historic_sector_transports",
    },
)
def debug_fed_historic_sector_transports(x, final_subs=None):
    return _ext_lookup_debug_fed_historic_sector_transports(x, final_subs)


_ext_lookup_debug_fed_historic_sector_transports = ExtLookup(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_transp",
    "solids_fec_transp",
    {"final sources": ["solids"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_debug_fed_historic_sector_transports",
)

_ext_lookup_debug_fed_historic_sector_transports.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_transp",
    "liquids_fec_transp",
    {"final sources": ["liquids"]},
)

_ext_lookup_debug_fed_historic_sector_transports.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_transp",
    "gases_fec_transp",
    {"final sources": ["gases"]},
)

_ext_lookup_debug_fed_historic_sector_transports.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_transp",
    "electricity_fec_transp",
    {"final sources": ["electricity"]},
)

_ext_lookup_debug_fed_historic_sector_transports.add(
    "../debugging.xlsx",
    "Catalonia",
    "years_fec_transp",
    "heat_fec_transp",
    {"final sources": ["heat"]},
)


@component.add(
    name="DEBUG FED households",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_final_energy_demand": 1},
)
def debug_fed_households():
    return households_final_energy_demand()


@component.add(
    name="DEBUG FED industrial",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_energy_by_sector_and_fuel_cat": 6},
)
def debug_fed_industrial():
    return (
        real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Food Beverages and Tobacco"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Textiles and leather etc"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Electrical and optical equipment and Transport equipment"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Other manufacturing"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Construction"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Distribution"]
        .reset_coords(drop=True)
    )


@component.add(
    name="DEBUG FED primari",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_energy_by_sector_and_fuel_cat": 3},
)
def debug_fed_primari():
    return (
        real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Agriculture"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Mining quarrying and energy supply"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Coke refined petroleum nuclear fuel and chemicals etc"]
        .reset_coords(drop=True)
    )


@component.add(
    name="DEBUG FED serveis",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_final_energy_by_sector_and_fuel_cat": 5},
)
def debug_fed_serveis():
    return (
        real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Hotels and restaurant"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Transport storage and communication"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Financial Intermediation"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Real estate renting and busine activitie"]
        .reset_coords(drop=True)
        + real_final_energy_by_sector_and_fuel_cat()
        .loc[:, "Non Market Service"]
        .reset_coords(drop=True)
    )


@component.add(
    name="DEBUG FED transports",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_transport_fed_by_fuel": 1},
)
def debug_fed_transports():
    return total_transport_fed_by_fuel()


@component.add(
    name="DEBUG historic GDP T$",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "historic_gdp": 1},
)
def debug_historic_gdp_t():
    return historic_gdp(time()) / 1000000.0
