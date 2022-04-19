"""
Module imports_and_exports
Translated using PySD version 3.0.0
"""


@component.add(
    name="Demand by sector RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def demand_by_sector_row():
    return if_then_else(
        time() < 2009,
        lambda: historic_demand_row(),
        lambda: real_demand_by_sector_row(),
    )


@component.add(
    name="Domestic output required for exports by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def domestic_output_required_for_exports_by_sector():
    """
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


@component.add(
    name="historic demand RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Data",
    comp_subtype="External",
)
def historic_demand_row():
    """
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
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "_ext_data_historic_demand_row",
)


@component.add(
    name="IC exports EU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ic_exports_eu():
    """
    Total intermediate products exports
    """
    return sum(
        ic_exports_eu_matrix().rename({"sectors1": "sectors1!"}), dim=["sectors1!"]
    )


@component.add(
    name="IC exports EU matrix",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ic_exports_eu_matrix():
    """
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


@component.add(
    name="IC imports EU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ic_imports_eu():
    """
    Total intermediate products imports
    """
    return sum(
        ic_imports_eu_matrix().rename({"sectors": "sectors1!", "sectors1": "sectors"}),
        dim=["sectors1!"],
    )


@component.add(
    name="IC imports EU matrix",
    units="Mdollars",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ic_imports_eu_matrix():
    """
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


@component.add(
    name="Real demand by sector RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_demand_by_sector_row():
    return real_demand_by_sector_world() - real_demand_by_sector_delayed_eu()


@component.add(
    name="Real Final Demand of exports",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_final_demand_of_exports():
    """
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


@component.add(
    name="Real total output by sector RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_total_output_by_sector_row():
    """
    Sectoral real total production by Rest of the World.
    """
    return real_total_output_by_sector_world() - real_total_output_by_sector_eu()


@component.add(
    name="Total domestic output required for exports by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_domestic_output_required_for_exports_by_sector():
    """
    Value of output (production) required to satisfy Rest of the World demand of EU28 producs (exports) by sector.
    """
    return domestic_output_required_for_exports_by_sector()
