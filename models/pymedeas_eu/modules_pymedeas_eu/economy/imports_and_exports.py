"""
Module economy.imports_and_exports
Translated using PySD version 3.14.0
"""

@component.add(
    name="Demand by sector RoW",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "historic_demand_row": 1, "real_demand_by_sector_row": 1},
)
def demand_by_sector_row():
    return if_then_else(
        time() < 2019,
        lambda: historic_demand_row(),
        lambda: real_demand_by_sector_row(),
    )


@component.add(
    name="Domestic output required for exports by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_exports": 1, "demand_by_sector_row": 1},
)
def domestic_output_required_for_exports_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports().rename({np.str_("sectors1"): "sectors1!"})
        * demand_by_sector_row().rename({np.str_("sectors"): "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="historic demand RoW",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_demand_row",
        "__data__": "_ext_data_historic_demand_row",
        "time": 1,
    },
)
def historic_demand_row():
    """
    Final demand by sector (Rest of the World).
    """
    return _ext_data_historic_demand_row(time())


_ext_data_historic_demand_row = ExtData(
    "../economy.xlsx",
    "Europe",
    "time_index2019",
    "historic_demand_RoW",
    "interpolate",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_data_historic_demand_row",
)


@component.add(
    name="IC exports EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_exports_eu_matrix": 1},
)
def ic_exports_eu():
    """
    Total intermediate products exports
    """
    return sum(
        ic_exports_eu_matrix().rename({np.str_("sectors1"): "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="IC exports EU matrix",
    units="Mdollars",
    subscripts=[np.str_("sectors"), np.str_("sectors1")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports": 1, "real_total_output_by_sector_row": 1},
)
def ic_exports_eu_matrix():
    """
    Intermediate products exports by sector
    """
    return -ia_matrix_exports() * real_total_output_by_sector_row().rename(
        {np.str_("sectors"): "sectors1"}
    )


@component.add(
    name="IC imports EU",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_imports_eu_matrix": 1},
)
def ic_imports_eu():
    """
    Total intermediate products imports
    """
    return sum(
        ic_imports_eu_matrix().rename(
            {np.str_("sectors"): "sectors1!", np.str_("sectors1"): "sectors"}
        ),
        dim=["sectors1!"],
    )


@component.add(
    name="IC imports EU matrix",
    units="Mdollars",
    subscripts=[np.str_("sectors"), np.str_("sectors1")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_imports": 1, "real_total_output_by_sector_eu": 1},
)
def ic_imports_eu_matrix():
    """
    Intermediate products imports by sector
    """
    return -ia_matrix_imports() * real_total_output_by_sector_eu().rename(
        {np.str_("sectors"): "sectors1"}
    )


@component.add(
    name="Real demand by sector RoW",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand_by_sector_world": 1,
        "real_demand_by_sector_delayed_eu": 1,
    },
)
def real_demand_by_sector_row():
    return real_demand_by_sector_world() - real_demand_by_sector_delayed_eu()


@component.add(
    name="Real Final Demand of exports",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports": 1, "real_total_output_by_sector_row": 1},
)
def real_final_demand_of_exports():
    """
    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports().rename({np.str_("sectors1"): "sectors1!"})
        * real_total_output_by_sector_row().rename({np.str_("sectors"): "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Real total output by sector RoW",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_total_output_by_sector_world": 1,
        "real_total_output_by_sector_eu": 1,
    },
)
def real_total_output_by_sector_row():
    """
    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu()


@component.add(
    name="Total domestic output required for exports by sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_output_required_for_exports_by_sector": 1},
)
def total_domestic_output_required_for_exports_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_by_sector()
