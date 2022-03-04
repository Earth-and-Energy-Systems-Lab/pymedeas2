"""
Module imports_and_exports
Translated using PySD version 2.2.1
"""


@subs(["sectors"], _subscript_dict)
def demand_by_sector_roeu():
    """
    Real Name: Demand by sector RoEU
    Original Eqn:
    Units: Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return if_then_else(
        time() < 2009, lambda: historic_demand_1(), lambda: real_demand_by_sector_roeu()
    )


@subs(["sectors"], _subscript_dict)
def demand_by_sector_row():
    """
    Real Name: Demand by sector RoW
    Original Eqn:
    Units: Tdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return if_then_else(
        time() < 2009, lambda: historic_demand_0(), lambda: real_demand_by_sector_row()
    )


@subs(["sectors"], _subscript_dict)
def domestic_output_required_for_exports_roeu_by_sector():
    """
    Real Name: Domestic output required for exports RoEU by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports_1().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + demand_by_sector_roeu().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def domestic_output_required_for_exports_row_by_sector():
    """
    Real Name: Domestic output required for exports Row by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports_0().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + demand_by_sector_row().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def historic_demand_0():
    """
    Real Name: historic demand 0
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']

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
    "_ext_data_historic_demand_0",
)


@subs(["sectors"], _subscript_dict)
def historic_demand_1():
    """
    Real Name: historic demand 1
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']

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
    "_ext_data_historic_demand_1",
)


@subs(["sectors"], _subscript_dict)
def ic_exports_aut_from_roeu():
    """
    Real Name: IC exports AUT from RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products exports
    """
    return sum(
        ic_exports_aut_matrix_to_roeu().rename({"sectors1": "sectors1!"}),
        dim=["sectors1!"],
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_exports_aut_matrix_to_roeu():
    """
    Real Name: IC exports AUT matrix to RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products exports by sector
    """
    return -ia_matrix_exports_1() * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        )
        + real_total_output_by_sector_roeu().rename({"sectors": "sectors1"})
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_exports_aut_matrix_to_row():
    """
    Real Name: IC exports AUT matrix to RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products exports by sector
    """
    return -ia_matrix_exports_0() * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        )
        + real_total_output_by_sector_row().rename({"sectors": "sectors1"})
    )


@subs(["sectors"], _subscript_dict)
def ic_exports_aut_to_row():
    """
    Real Name: IC exports AUT to RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products exports
    """
    return sum(
        ic_exports_aut_matrix_to_row().rename({"sectors1": "sectors1!"}),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def ic_imports_aut_from_row():
    """
    Real Name: IC imports AUT from RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products imports
    """
    return sum(
        ic_imports_aut_matrix_from_row().rename(
            {"sectors": "sectors1!", "sectors1": "sectors"}
        ),
        dim=["sectors1!"],
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_imports_aut_matrix_from_roeu():
    """
    Real Name: IC imports AUT matrix from RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products imports by sector
    """
    return -ia_matrix_imports_1() * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        )
        + real_total_output_by_sector_aut().rename({"sectors": "sectors1"})
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_imports_aut_matrix_from_row():
    """
    Real Name: IC imports AUT matrix from RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products imports by sector
    """
    return -ia_matrix_imports_0() * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        )
        + real_total_output_by_sector_aut().rename({"sectors": "sectors1"})
    )


@subs(["sectors"], _subscript_dict)
def ic_imports_aut_to_roeu():
    """
    Real Name: IC imports AUT to RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products imports
    """
    return sum(
        ic_imports_aut_matrix_from_roeu().rename(
            {"sectors": "sectors1!", "sectors1": "sectors"}
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def ic_total_exports():
    """
    Real Name: IC total exports
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return ic_exports_aut_from_roeu() + ic_exports_aut_to_row()


@subs(["sectors"], _subscript_dict)
def ic_total_imports():
    """
    Real Name: IC total imports
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return ic_imports_aut_from_row() + ic_imports_aut_to_roeu()


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_roeu():
    """
    Real Name: Real demand by sector RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return real_demand_by_sector_eu28() - real_demand_by_sector_delayed_aut()


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_row():
    """
    Real Name: Real demand by sector RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return real_demand_by_sector_world() - real_demand_by_sector_eu28()


@subs(["sectors"], _subscript_dict)
def real_final_demand_of_exports():
    """
    Real Name: Real Final Demand of Exports
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return (
        real_final_demand_of_exports_to_roeu() + real_final_demand_of_exports_to_row()
    )


@subs(["sectors"], _subscript_dict)
def real_final_demand_of_exports_to_roeu():
    """
    Real Name: Real Final Demand of exports to RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports_1().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + real_total_output_by_sector_roeu().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def real_final_demand_of_exports_to_row():
    """
    Real Name: Real Final Demand of exports to RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports_0().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + real_total_output_by_sector_row().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_roeu():
    """
    Real Name: Real total output by sector RoEU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_eu28() - real_total_output_by_sector_aut()


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_row():
    """
    Real Name: Real total output by sector RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu28()


@subs(["sectors"], _subscript_dict)
def required_total_output_for_exports():
    """
    Real Name: Required total output for exports
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Required total output (domestic+foreign)
    """
    return (
        domestic_output_required_for_exports_row_by_sector()
        + domestic_output_required_for_exports_roeu_by_sector()
    )


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_for_exports_from_roeu_by_sector():
    """
    Real Name: Total domestic output required for exports from RoEU by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_roeu_by_sector()


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_for_exports_from_row_by_sector():
    """
    Real Name: Total domestic output required for exports from RoW by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_row_by_sector()
