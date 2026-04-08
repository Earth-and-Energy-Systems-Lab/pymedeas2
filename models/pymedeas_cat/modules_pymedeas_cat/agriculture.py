"""
Module agriculture
Translated using PySD version 3.14.3
"""

@component.add(
    name="Enteric_fermentation_EF",
    units="KgCh4/year/Head",
    subscripts=["Livestock"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_enteric_fermentation_ef",
        "__lookup__": "_ext_lookup_enteric_fermentation_ef",
    },
)
def enteric_fermentation_ef(x, final_subs=None):
    return _ext_lookup_enteric_fermentation_ef(x, final_subs)


_ext_lookup_enteric_fermentation_ef = ExtLookup(
    r"../agriculture.xlsx",
    "Catalonia",
    "time_index2019",
    "historic_enteric_fermentation_ef",
    {"Livestock": _subscript_dict["Livestock"]},
    _root,
    {"Livestock": _subscript_dict["Livestock"]},
    "_ext_lookup_enteric_fermentation_ef",
)


@component.add(
    name="Enteric_fermentation_emissions",
    units="KgCh4/year",
    subscripts=["Livestock"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "enteric_fermentation_ef": 1, "livestock_heads": 1},
)
def enteric_fermentation_emissions():
    return enteric_fermentation_ef(time()) * livestock_heads(time()) * 28 * 1e-06


@component.add(
    name="Livestock_heads",
    units="Head",
    subscripts=["Livestock"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_livestock_heads",
        "__lookup__": "_ext_lookup_livestock_heads",
    },
)
def livestock_heads(x, final_subs=None):
    return _ext_lookup_livestock_heads(x, final_subs)


_ext_lookup_livestock_heads = ExtLookup(
    r"../agriculture.xlsx",
    "Catalonia",
    "time_index2019",
    "historic_livestock_heads",
    {"Livestock": _subscript_dict["Livestock"]},
    _root,
    {"Livestock": _subscript_dict["Livestock"]},
    "_ext_lookup_livestock_heads",
)


@component.add(
    name="Manure_emissions",
    subscripts=["Livestock"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "livestock_heads": 1,
        "vs_rate": 1,
        "methane_production_factor": 1,
        "total_methane_conversion_factor": 1,
    },
)
def manure_emissions():
    return (
        livestock_heads(time())
        * vs_rate(time())
        * 365
        * methane_production_factor()
        * 0.67
        * sum(
            total_methane_conversion_factor().rename(
                {"Manure_management_systems": "Manure_management_systems!"}
            ),
            dim=["Manure_management_systems!"],
        )
        * 28
        * 1e-06
    )


@component.add(
    name="Manure_management_share",
    units="Dmnl",
    subscripts=["Manure_management_systems", "Livestock"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_manure_management_share"},
)
def manure_management_share():
    return _ext_constant_manure_management_share()


_ext_constant_manure_management_share = ExtConstant(
    r"../agriculture.xlsx",
    "Catalonia",
    "manure_management_share*",
    {
        "Manure_management_systems": _subscript_dict["Manure_management_systems"],
        "Livestock": _subscript_dict["Livestock"],
    },
    _root,
    {
        "Manure_management_systems": _subscript_dict["Manure_management_systems"],
        "Livestock": _subscript_dict["Livestock"],
    },
    "_ext_constant_manure_management_share",
)


@component.add(
    name="Methane_conversion_factor_manure_system",
    units="Dmnl",
    subscripts=["Manure_management_systems"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_methane_conversion_factor_manure_system"
    },
)
def methane_conversion_factor_manure_system():
    return _ext_constant_methane_conversion_factor_manure_system()


_ext_constant_methane_conversion_factor_manure_system = ExtConstant(
    r"../agriculture.xlsx",
    "Catalonia",
    "methane_conversion_factor*",
    {"Manure_management_systems": _subscript_dict["Manure_management_systems"]},
    _root,
    {"Manure_management_systems": _subscript_dict["Manure_management_systems"]},
    "_ext_constant_methane_conversion_factor_manure_system",
)


@component.add(
    name="Methane_production_factor",
    units="M3CH4/KgVS",
    subscripts=["Livestock"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_methane_production_factor"},
)
def methane_production_factor():
    return _ext_constant_methane_production_factor()


_ext_constant_methane_production_factor = ExtConstant(
    r"../agriculture.xlsx",
    "Catalonia",
    "livestock_B0*",
    {"Livestock": _subscript_dict["Livestock"]},
    _root,
    {"Livestock": _subscript_dict["Livestock"]},
    "_ext_constant_methane_production_factor",
)


@component.add(
    name="Total_CH4_emissions_livestock",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enteric_fermentation_emissions": 1, "manure_emissions": 1},
)
def total_ch4_emissions_livestock():
    return sum(
        enteric_fermentation_emissions().rename({"Livestock": "Livestock!"}),
        dim=["Livestock!"],
    ) + sum(manure_emissions().rename({"Livestock": "Livestock!"}), dim=["Livestock!"])


@component.add(
    name="Total_methane_conversion_factor",
    subscripts=["Manure_management_systems", "Livestock"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "manure_management_share": 1,
        "methane_conversion_factor_manure_system": 1,
    },
)
def total_methane_conversion_factor():
    return manure_management_share() * methane_conversion_factor_manure_system() * 0.01


@component.add(
    name="VS_rate",
    units="KgVS/Head/year",
    subscripts=["Livestock"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_vs_rate",
        "__lookup__": "_ext_lookup_vs_rate",
    },
)
def vs_rate(x, final_subs=None):
    return _ext_lookup_vs_rate(x, final_subs)


_ext_lookup_vs_rate = ExtLookup(
    r"../agriculture.xlsx",
    "Catalonia",
    "time_index2019",
    "historic_vs",
    {"Livestock": _subscript_dict["Livestock"]},
    _root,
    {"Livestock": _subscript_dict["Livestock"]},
    "_ext_lookup_vs_rate",
)
