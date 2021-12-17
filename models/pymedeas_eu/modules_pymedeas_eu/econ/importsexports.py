"""
Module importsexports
Translated using PySD version 2.2.0
"""


@subs(["sectors"], _subscript_dict)
def demand_by_sector_row():
    """
    Real Name: Demand by sector RoW
    Original Eqn: IF THEN ELSE(Time<2009,historic demand RoW[sectors],Real demand by sector RoW[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
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
    Original Eqn: SUM(Leontief Matrix Exports[sectors,sectors1!]*Demand by sector RoW[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand
        of EU28 producs (exports) by sector.
    """
    return sum(
        leontief_matrix_exports()
        * rearrange(demand_by_sector_row(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["sectors"], _subscript_dict)
def historic_demand_row():
    """
    Real Name: historic demand RoW
    Original Eqn: GET DIRECT DATA('../economy.xlsx', 'Europe', 'time_index_2009', 'historic_demand_RoW')
    Units: Mdollars
    Limits: (None, None)
    Type: component_ext_data
    Subs: ['sectors']

    Final demand by sector (Rest of the World).
    """
    return _ext_data_historic_demand_row(time())


@subs(["sectors"], _subscript_dict)
def ic_exports_eu():
    """
    Real Name: IC exports EU
    Original Eqn: SUM(IC exports EU matrix[sectors,sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Total intermediate products exports
    """
    return sum(ic_exports_eu_matrix(), dim=("sectors1",))


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_exports_eu_matrix():
    """
    Real Name: IC exports EU matrix
    Original Eqn: -IA Matrix Exports[sectors,sectors1]*Real total output by sector RoW[sectors1]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'sectors1']

    Intermediate products exports by sector
    """
    return -ia_matrix_exports() * rearrange(
        real_total_output_by_sector_row(), ["sectors1"], _subscript_dict
    )


@subs(["sectors"], _subscript_dict)
def ic_imports_eu():
    """
    Real Name: IC imports EU
    Original Eqn: SUM(IC imports EU matrix[sectors1!,sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Total intermediate products imports
    """
    return sum(
        rearrange(ic_imports_eu_matrix(), ["sectors1", "sectors"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["sectors", "sectors1"], _subscript_dict)
def ic_imports_eu_matrix():
    """
    Real Name: IC imports EU matrix
    Original Eqn: -IA Matrix Imports[sectors,sectors1]*Real total output by sector EU[sectors1]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'sectors1']

    Intermediate products imports by sector
    """
    return -ia_matrix_imports() * rearrange(
        real_total_output_by_sector_eu(), ["sectors1"], _subscript_dict
    )


@subs(["sectors"], _subscript_dict)
def real_demand_by_sector_row():
    """
    Real Name: Real demand by sector RoW
    Original Eqn: Real demand by sector World[sectors]-Real demand by sector delayed EU[ sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return real_demand_by_sector_world() - real_demand_by_sector_delayed_eu()


@subs(["sectors"], _subscript_dict)
def real_final_demand_of_exports():
    """
    Real Name: Real Final Demand of exports
    Original Eqn: SUM(IA Matrix Exports [sectors,sectors1!]*Real total output by sector RoW[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real final demand of EU28 products made by the Rest of the World (Exports).
    """
    return sum(
        ia_matrix_exports()
        * rearrange(real_total_output_by_sector_row(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["sectors"], _subscript_dict)
def real_total_output_by_sector_row():
    """
    Real Name: Real total output by sector RoW
    Original Eqn: Real total output by sector World[sectors]-Real total output by sector EU[ sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu()


@subs(["sectors"], _subscript_dict)
def required_total_output():
    """
    Real Name: Required total output
    Original Eqn: Domestic output required for exports by sector[sectors]+Total domestic output required by sector[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Required total output (domestic+foreign)
    """
    return (
        domestic_output_required_for_exports_by_sector()
        + total_domestic_output_required_by_sector()
    )


@subs(["sectors"], _subscript_dict)
def total_domestic_output_required_for_exports_by_sector():
    """
    Real Name: Total domestic output required for exports by sector
    Original Eqn: Domestic output required for exports by sector[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Value of output (production) required to satisfy Rest of the World demand
        of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_by_sector()


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
