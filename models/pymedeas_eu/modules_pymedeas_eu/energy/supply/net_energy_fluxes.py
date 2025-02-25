"""
Module energy.supply.net_energy_fluxes
Translated using PySD version 3.14.1
"""

@component.add(
    name="historic coal imports",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_coal_imports",
        "__lookup__": "_ext_lookup_historic_coal_imports",
    },
)
def historic_coal_imports(x, final_subs=None):
    return _ext_lookup_historic_coal_imports(x, final_subs)


_ext_lookup_historic_coal_imports = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_imports",
    "coal_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_coal_imports",
)


@component.add(
    name="historic gas imports",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_gas_imports",
        "__lookup__": "_ext_lookup_historic_gas_imports",
    },
)
def historic_gas_imports(x, final_subs=None):
    return _ext_lookup_historic_gas_imports(x, final_subs)


_ext_lookup_historic_gas_imports = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_imports",
    "gas_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_gas_imports",
)


@component.add(
    name="historic oil imports",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_oil_imports",
        "__lookup__": "_ext_lookup_historic_oil_imports",
    },
)
def historic_oil_imports(x, final_subs=None):
    return _ext_lookup_historic_oil_imports(x, final_subs)


_ext_lookup_historic_oil_imports = ExtLookup(
    r"../energy.xlsx",
    "Europe",
    "time_historic_imports",
    "oil_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_oil_imports",
)


@component.add(
    name="last historical year",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def last_historical_year():
    return 2019


@component.add(
    name="maximum coal available in EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej_world": 1},
)
def maximum_coal_available_in_eu():
    """
    Extraction coal
    """
    return extraction_coal_ej_world()


@component.add(
    name="maximum gas available in EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_nat_gas_ej_world": 1},
)
def maximum_gas_available_in_eu():
    return extraction_nat_gas_ej_world()


@component.add(
    name="maximum oil available in EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_oil_ej_world": 1},
)
def maximum_oil_available_in_eu():
    return extraction_oil_ej_world()


@component.add(
    name="net coal flux EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_fs": 1,
        "projected_net_coal_flux_eu": 1,
        "historic_coal_imports": 1,
        "maximum_coal_available_in_eu": 1,
        "last_historical_year": 1,
        "time": 3,
    },
)
def net_coal_flux_eu():
    return np.minimum(
        float(ped_nre_fs().loc["solids"]),
        if_then_else(
            time() <= last_historical_year(),
            lambda: historic_coal_imports(time()),
            lambda: np.minimum(
                projected_net_coal_flux_eu(time()), maximum_coal_available_in_eu()
            ),
        ),
    )


@component.add(
    name="net gas flux EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_fs": 1,
        "maximum_gas_available_in_eu": 1,
        "last_historical_year": 1,
        "time": 3,
        "historic_gas_imports": 1,
        "projected_net_gas_flux_eu": 1,
    },
)
def net_gas_flux_eu():
    return np.minimum(
        float(ped_nre_fs().loc["gases"]),
        if_then_else(
            time() <= last_historical_year(),
            lambda: historic_gas_imports(time()),
            lambda: np.minimum(
                projected_net_gas_flux_eu(time()), maximum_gas_available_in_eu()
            ),
        ),
    )


@component.add(
    name="net oil flux EU",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_fs": 1,
        "projected_net_oil_flux_eu": 1,
        "maximum_oil_available_in_eu": 1,
        "last_historical_year": 1,
        "time": 3,
        "historic_oil_imports": 1,
    },
)
def net_oil_flux_eu():
    return np.minimum(
        float(ped_nre_fs().loc["liquids"]),
        if_then_else(
            time() <= last_historical_year(),
            lambda: historic_oil_imports(time()),
            lambda: np.minimum(
                projected_net_oil_flux_eu(time()), maximum_oil_available_in_eu()
            ),
        ),
    )


@component.add(
    name="projected net coal flux EU",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_coal_flux_eu",
        "__lookup__": "_ext_lookup_projected_net_coal_flux_eu",
    },
)
def projected_net_coal_flux_eu(x, final_subs=None):
    return _ext_lookup_projected_net_coal_flux_eu(x, final_subs)


_ext_lookup_projected_net_coal_flux_eu = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_net_energy_flux",
    "coal_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_coal_flux_eu",
)


@component.add(
    name="projected net gas flux EU",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_gas_flux_eu",
        "__lookup__": "_ext_lookup_projected_net_gas_flux_eu",
    },
)
def projected_net_gas_flux_eu(x, final_subs=None):
    return _ext_lookup_projected_net_gas_flux_eu(x, final_subs)


_ext_lookup_projected_net_gas_flux_eu = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_net_energy_flux",
    "gas_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_gas_flux_eu",
)


@component.add(
    name="projected net oil flux EU",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_oil_flux_eu",
        "__lookup__": "_ext_lookup_projected_net_oil_flux_eu",
    },
)
def projected_net_oil_flux_eu(x, final_subs=None):
    return _ext_lookup_projected_net_oil_flux_eu(x, final_subs)


_ext_lookup_projected_net_oil_flux_eu = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_net_energy_flux",
    "oil_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_oil_flux_eu",
)
