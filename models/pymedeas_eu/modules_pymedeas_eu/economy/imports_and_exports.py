"""
Module imports_and_exports
Translated using PySD version 2.2.1
"""


@subs(["sectors"], _subscript_dict)
def demand_by_sector_row():
    """
    Real Name: Demand by sector RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']


    """
    return if_then_else(
        time() < 2009,
        lambda: historic_demand_row(),
        lambda: real_demand_by_sector_row(),
    )


@subs(["sectors"], _subscript_dict)
def domestic_output_required_for_exports_by_sector():
    """
    Real Name: Domestic output required for exports by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports().rename({"sectors1": "sectors1!"})
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
def historic_demand_row():
    """
    Real Name: historic demand RoW
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Data
    Subs: ['sectors']

    Final demand by sector (Rest of the World).
    """
    return _ext_data_historic_demand_row(time())


_ext_data_historic_demand_row = ExtData(
    "../economy.xlsx",
    "Europe",
    "time_index_2009",
    "historic_demand_RoW",
    None,
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_data_historic_demand_row",
)


@subs(["sectors"], _subscript_dict)
def ic_exports_eu():
    """
    Real Name: IC exports EU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products exports
    """
    return sum(
        ic_exports_eu_matrix().rename({"sectors1": "sectors1!"}), dim=["sectors1!"]
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_exports_eu_matrix():
    """
    Real Name: IC exports EU matrix
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products exports by sector
    """
    return -ia_matrix_exports() * (
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
def ic_imports_eu():
    """
    Real Name: IC imports EU
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Total intermediate products imports
    """
    return sum(
        ic_imports_eu_matrix().rename({"sectors": "sectors1!", "sectors1": "sectors"}),
        dim=["sectors1!"],
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_imports_eu_matrix():
    """
    Real Name: IC imports EU matrix
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors', 'sectors1']

    Intermediate products imports by sector
    """
    return -ia_matrix_imports() * (
        xr.DataArray(
            0,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        )
        + real_total_output_by_sector_eu().rename({"sectors": "sectors1"})
    )


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
    return real_demand_by_sector_world() - real_demand_by_sector_delayed_eu()


@subs(["sectors"], _subscript_dict)
def real_final_demand_of_exports():
    """
    Real Name: Real Final Demand of exports
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports().rename({"sectors1": "sectors1!"})
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
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu()


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_for_exports_by_sector():
    """
    Real Name: Total domestic output required for exports by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_by_sector()
