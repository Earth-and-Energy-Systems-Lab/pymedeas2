"""
Module energy.supply.net_energy_fluxes
Translated using PySD version 3.14.2
"""

@component.add(
    name="historic_coal_imports",
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
    "Catalonia",
    "time_historic_imports",
    "coal_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_coal_imports",
)


@component.add(
    name="historic_gas_imports",
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
    "Catalonia",
    "time_historic_imports",
    "gas_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_gas_imports",
)


@component.add(
    name="historic_oil_imports",
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
    "Catalonia",
    "time_historic_imports",
    "oil_historic_imports",
    {},
    _root,
    {},
    "_ext_lookup_historic_oil_imports",
)


@component.add(
    name="last_historical_year",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def last_historical_year():
    return 2019


@component.add(
    name="maximum_coal_available_in_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_coal_ej_world": 1},
)
def maximum_coal_available_in_cat():
    return extraction_coal_ej_world()


@component.add(
    name="maximum_gas_available_in_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_nat_gas_ej_world": 1},
)
def maximum_gas_available_in_cat():
    return extraction_nat_gas_ej_world()


@component.add(
    name="maximum_oil_available_in_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"extraction_oil_ej_world": 1},
)
def maximum_oil_available_in_cat():
    return extraction_oil_ej_world()


@component.add(
    name="net_coal_flux_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_ej": 1,
        "maximum_coal_available_in_cat": 1,
        "last_historical_year": 1,
        "projected_net_coal_flux_cat": 1,
        "time": 3,
        "historic_coal_imports": 1,
    },
)
def net_coal_flux_cat():
    return float(
        np.minimum(
            ped_coal_ej(),
            if_then_else(
                time() <= last_historical_year(),
                lambda: historic_coal_imports(time()),
                lambda: float(
                    np.minimum(
                        projected_net_coal_flux_cat(time()),
                        maximum_coal_available_in_cat(),
                    )
                ),
            ),
        )
    )


@component.add(
    name="net_gas_flux_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "projected_net_gas_flux_cat": 1,
        "time": 3,
        "historic_gas_imports": 1,
        "last_historical_year": 1,
        "maximum_gas_available_in_cat": 1,
    },
)
def net_gas_flux_cat():
    return float(
        np.minimum(
            ped_nat_gas_ej(),
            if_then_else(
                time() <= last_historical_year(),
                lambda: historic_gas_imports(time()),
                lambda: float(
                    np.minimum(
                        projected_net_gas_flux_cat(time()),
                        maximum_gas_available_in_cat(),
                    )
                ),
            ),
        )
    )


@component.add(
    name="net_oil_flux_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_total_oil_ej": 1,
        "historic_oil_imports": 1,
        "maximum_oil_available_in_cat": 1,
        "last_historical_year": 1,
        "time": 3,
        "projected_net_oil_flux_cat": 1,
    },
)
def net_oil_flux_cat():
    return float(
        np.minimum(
            ped_total_oil_ej(),
            if_then_else(
                time() <= last_historical_year(),
                lambda: historic_oil_imports(time()),
                lambda: float(
                    np.minimum(
                        projected_net_oil_flux_cat(time()),
                        maximum_oil_available_in_cat(),
                    )
                ),
            ),
        )
    )


@component.add(
    name="projected_net_coal_flux_CAT",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_coal_flux_cat",
        "__lookup__": "_ext_lookup_projected_net_coal_flux_cat",
    },
)
def projected_net_coal_flux_cat(x, final_subs=None):
    return _ext_lookup_projected_net_coal_flux_cat(x, final_subs)


_ext_lookup_projected_net_coal_flux_cat = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_net_energy_flux",
    "coal_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_coal_flux_cat",
)


@component.add(
    name="projected_net_gas_flux_CAT",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_gas_flux_cat",
        "__lookup__": "_ext_lookup_projected_net_gas_flux_cat",
    },
)
def projected_net_gas_flux_cat(x, final_subs=None):
    return _ext_lookup_projected_net_gas_flux_cat(x, final_subs)


_ext_lookup_projected_net_gas_flux_cat = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_net_energy_flux",
    "gas_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_gas_flux_cat",
)


@component.add(
    name="projected_net_oil_flux_CAT",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_projected_net_oil_flux_cat",
        "__lookup__": "_ext_lookup_projected_net_oil_flux_cat",
    },
)
def projected_net_oil_flux_cat(x, final_subs=None):
    return _ext_lookup_projected_net_oil_flux_cat(x, final_subs)


_ext_lookup_projected_net_oil_flux_cat = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_net_energy_flux",
    "oil_net_flux_timeseries",
    {},
    _root,
    {},
    "_ext_lookup_projected_net_oil_flux_cat",
)
