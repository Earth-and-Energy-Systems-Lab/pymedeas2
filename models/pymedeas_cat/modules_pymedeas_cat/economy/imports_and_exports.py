"""
Module economy.imports_and_exports
Translated using PySD version 3.10.0
"""


@component.add(
    name="Demand by sector RoEU",
    units="Tdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "historic_demand_1": 1, "real_demand_by_sector_roeu": 1},
)
def demand_by_sector_roeu():
    return if_then_else(
        time() < 2009, lambda: historic_demand_1(), lambda: real_demand_by_sector_roeu()
    )


@component.add(
    name="Demand by sector RoW",
    units="Tdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "historic_demand_0": 1, "real_demand_by_sector_row": 1},
)
def demand_by_sector_row():
    return if_then_else(
        time() < 2009, lambda: historic_demand_0(), lambda: real_demand_by_sector_row()
    )


@component.add(
    name="Domestic output required for exports RoEU by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_exports_1": 1, "demand_by_sector_roeu": 1},
)
def domestic_output_required_for_exports_roeu_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports_1().rename({"sectors1": "sectors1!"})
        * demand_by_sector_roeu().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Domestic output required for exports Row by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_exports_0": 1, "demand_by_sector_row": 1},
)
def domestic_output_required_for_exports_row_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports_0().rename({"sectors1": "sectors1!"})
        * demand_by_sector_row().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="historic demand 0",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_demand_0",
        "__data__": "_ext_data_historic_demand_0",
        "time": 1,
    },
)
def historic_demand_0():
    """
    Final demand by sector level 0 (Rest of the World).
    """
    return _ext_data_historic_demand_0(time())


_ext_data_historic_demand_0 = ExtData(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_demand_0",
    None,
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_data_historic_demand_0",
)


@component.add(
    name="historic demand 1",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_demand_1",
        "__data__": "_ext_data_historic_demand_1",
        "time": 1,
    },
)
def historic_demand_1():
    """
    Final demand by sector level 1 (intermediate nesting).
    """
    return _ext_data_historic_demand_1(time())


_ext_data_historic_demand_1 = ExtData(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_demand_1",
    None,
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_data_historic_demand_1",
)


@component.add(
    name="IC exports CAT from RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_exports_cat_matrix_to_roeu": 1},
)
def ic_exports_cat_from_roeu():
    """
    Total intermediate products exports
    """
    return sum(
        ic_exports_cat_matrix_to_roeu().rename({"sectors1": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="IC exports CAT matrix to RoEU",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports_1": 1, "real_total_output_by_sector_roeu": 1},
)
def ic_exports_cat_matrix_to_roeu():
    """
    Intermediate products exports by sector
    """
    return -ia_matrix_exports_1() * real_total_output_by_sector_roeu().rename(
        {"sectors": "sectors1"}
    )


@component.add(
    name="IC exports CAT matrix to RoW",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports_0": 1, "real_total_output_by_sector_row": 1},
)
def ic_exports_cat_matrix_to_row():
    """
    Intermediate products exports by sector
    """
    return -ia_matrix_exports_0() * real_total_output_by_sector_row().rename(
        {"sectors": "sectors1"}
    )


@component.add(
    name="IC exports CAT to RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_exports_cat_matrix_to_row": 1},
)
def ic_exports_cat_to_row():
    """
    Total intermediate products exports
    """
    return sum(
        ic_exports_cat_matrix_to_row().rename({"sectors1": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="IC imports CAT from RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_imports_cat_matrix_from_row": 1},
)
def ic_imports_cat_from_row():
    """
    Total intermediate products imports
    """
    return sum(
        ic_imports_cat_matrix_from_row().rename(
            {"sectors": "sectors1!", "sectors1": "sectors"}
        ),
        dim=["sectors1!"],
    )


@component.add(
    name="IC imports CAT matrix from RoEU",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_imports_1": 1, "real_total_output_by_sector_cat": 1},
)
def ic_imports_cat_matrix_from_roeu():
    """
    Intermediate products imports by sector
    """
    return -ia_matrix_imports_1() * real_total_output_by_sector_cat().rename(
        {"sectors": "sectors1"}
    )


@component.add(
    name="IC imports CAT matrix from RoW",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_imports_0": 1, "real_total_output_by_sector_cat": 1},
)
def ic_imports_cat_matrix_from_row():
    """
    Intermediate products imports by sector
    """
    return -ia_matrix_imports_0() * real_total_output_by_sector_cat().rename(
        {"sectors": "sectors1"}
    )


@component.add(
    name="IC imports CAT to RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_imports_cat_matrix_from_roeu": 1},
)
def ic_imports_cat_to_roeu():
    """
    Total intermediate products imports
    """
    return sum(
        ic_imports_cat_matrix_from_roeu().rename(
            {"sectors": "sectors1!", "sectors1": "sectors"}
        ),
        dim=["sectors1!"],
    )


@component.add(
    name="IC total exports",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_exports_cat_from_roeu": 1, "ic_exports_cat_to_row": 1},
)
def ic_total_exports():
    return ic_exports_cat_from_roeu() + ic_exports_cat_to_row()


@component.add(
    name="IC total imports",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ic_imports_cat_from_row": 1, "ic_imports_cat_to_roeu": 1},
)
def ic_total_imports():
    return ic_imports_cat_from_row() + ic_imports_cat_to_roeu()


@component.add(
    name="Real demand by sector RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand_by_sector_eu28": 1,
        "real_demand_by_sector_delayed_cat": 1,
    },
)
def real_demand_by_sector_roeu():
    return real_demand_by_sector_eu28() - real_demand_by_sector_delayed_cat()


@component.add(
    name="Real demand by sector RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_by_sector_world": 1, "real_demand_by_sector_eu28": 1},
)
def real_demand_by_sector_row():
    return real_demand_by_sector_world() - real_demand_by_sector_eu28()


@component.add(
    name="Real Final Demand of Exports",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_of_exports_to_roeu": 1,
        "real_final_demand_of_exports_to_row": 1,
    },
)
def real_final_demand_of_exports():
    return (
        real_final_demand_of_exports_to_roeu() + real_final_demand_of_exports_to_row()
    )


@component.add(
    name="Real Final Demand of exports to RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports_1": 1, "real_total_output_by_sector_roeu": 1},
)
def real_final_demand_of_exports_to_roeu():
    """
    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports_1().rename({"sectors1": "sectors1!"})
        * real_total_output_by_sector_roeu().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Real Final Demand of exports to RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix_exports_0": 1, "real_total_output_by_sector_row": 1},
)
def real_final_demand_of_exports_to_row():
    """
    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports_0().rename({"sectors1": "sectors1!"})
        * real_total_output_by_sector_row().rename({"sectors": "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Real total output by sector RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_total_output_by_sector_eu28": 1,
        "real_total_output_by_sector_cat": 1,
    },
)
def real_total_output_by_sector_roeu():
    """
    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_eu28() - real_total_output_by_sector_cat()


@component.add(
    name="Real total output by sector RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_total_output_by_sector_world": 1,
        "real_total_output_by_sector_eu28": 1,
    },
)
def real_total_output_by_sector_row():
    """
    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu28()


@component.add(
    name="Required total output for exports",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_output_required_for_exports_row_by_sector": 1,
        "domestic_output_required_for_exports_roeu_by_sector": 1,
    },
)
def required_total_output_for_exports():
    """
    Required total output (domestic+foreign)
    """
    return (
        domestic_output_required_for_exports_row_by_sector()
        + domestic_output_required_for_exports_roeu_by_sector()
    )


@component.add(
    name="sum total exports demand",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_total_output_for_exports": 1},
)
def sum_total_exports_demand():
    return sum(
        required_total_output_for_exports().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Total domestic output required for exports from RoEU by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_output_required_for_exports_roeu_by_sector": 1},
)
def total_domestic_output_required_for_exports_from_roeu_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_roeu_by_sector()


@component.add(
    name="Total domestic output required for exports from RoW by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"domestic_output_required_for_exports_row_by_sector": 1},
)
def total_domestic_output_required_for_exports_from_row_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_row_by_sector()
