"""
Module coefficient_matrices
Translated using PySD version 3.2.0
"""


@component.add(
    name="historic A Matrix",
    units="Dmnl",
    subscripts=["economic years", "sectors A matrix", "sectors A matrix1"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_historic_a_matrix"},
)
def historic_a_matrix():
    """
    Historic A Matrix for 14 sectors and 2 regions.
    """
    return _ext_constant_historic_a_matrix()


_ext_constant_historic_a_matrix = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1995",
    {
        "economic years": ["year1995"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
    _root,
    {
        "economic years": _subscript_dict["economic years"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
    "_ext_constant_historic_a_matrix",
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1996",
    {
        "economic years": ["year1996"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1997",
    {
        "economic years": ["year1997"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1998",
    {
        "economic years": ["year1998"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1999",
    {
        "economic years": ["year1999"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2000",
    {
        "economic years": ["year2000"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2001",
    {
        "economic years": ["year2001"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2002",
    {
        "economic years": ["year2002"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2003",
    {
        "economic years": ["year2003"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2004",
    {
        "economic years": ["year2004"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2005",
    {
        "economic years": ["year2005"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2006",
    {
        "economic years": ["year2006"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2007",
    {
        "economic years": ["year2007"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2008",
    {
        "economic years": ["year2008"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2009",
    {
        "economic years": ["year2009"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2010",
    {
        "economic years": ["year2010"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2011",
    {
        "economic years": ["year2011"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2012",
    {
        "economic years": ["year2012"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2013",
    {
        "economic years": ["year2013"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2014",
    {
        "economic years": ["year2014"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)


@component.add(
    name="historic IA Matrix",
    subscripts=["economic years", "sectors A matrix", "sectors A matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"i_matrix": 1, "historic_a_matrix": 1},
)
def historic_ia_matrix():
    return (
        i_matrix()
        - historic_a_matrix().transpose(
            "sectors A matrix", "sectors A matrix1", "economic years"
        )
    ).transpose("economic years", "sectors A matrix", "sectors A matrix1")


@component.add(
    name="historic Leontief Matrix",
    subscripts=["economic years", "sectors A matrix", "sectors A matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_ia_matrix": 1},
)
def historic_leontief_matrix():
    return invert_matrix(historic_ia_matrix())


@component.add(
    name="I Matrix",
    subscripts=["sectors A matrix", "sectors A matrix1"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def i_matrix():
    return if_then_else(
        xr.DataArray(
            np.arange(1, len(_subscript_dict["sectors A matrix"]) + 1),
            {"sectors A matrix": _subscript_dict["sectors A matrix"]},
            ["sectors A matrix"],
        )
        == xr.DataArray(
            np.arange(1, len(_subscript_dict["sectors A matrix1"]) + 1),
            {"sectors A matrix1": _subscript_dict["sectors A matrix1"]},
            ["sectors A matrix1"],
        ),
        lambda: xr.DataArray(
            1,
            {
                "sectors A matrix": _subscript_dict["sectors A matrix"],
                "sectors A matrix1": _subscript_dict["sectors A matrix1"],
            },
            ["sectors A matrix", "sectors A matrix1"],
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors A matrix": _subscript_dict["sectors A matrix"],
                "sectors A matrix1": _subscript_dict["sectors A matrix1"],
            },
            ["sectors A matrix", "sectors A matrix1"],
        ),
    )


@component.add(
    name="IA Matrix",
    subscripts=["sectors A matrix", "sectors A matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 14, "historic_ia_matrix": 15},
)
def ia_matrix():
    return if_then_else(
        time() >= 2009,
        lambda: historic_ia_matrix().loc["year2009", :, :].reset_coords(drop=True),
        lambda: if_then_else(
            time() >= 2008,
            lambda: historic_ia_matrix().loc["year2008", :, :].reset_coords(drop=True),
            lambda: if_then_else(
                time() >= 2007,
                lambda: historic_ia_matrix()
                .loc["year2007", :, :]
                .reset_coords(drop=True),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: historic_ia_matrix()
                    .loc["year2006", :, :]
                    .reset_coords(drop=True),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: historic_ia_matrix()
                        .loc["year2005", :, :]
                        .reset_coords(drop=True),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: historic_ia_matrix()
                            .loc["year2004", :, :]
                            .reset_coords(drop=True),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: historic_ia_matrix()
                                .loc["year2003", :, :]
                                .reset_coords(drop=True),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: historic_ia_matrix()
                                    .loc["year2002", :, :]
                                    .reset_coords(drop=True),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: historic_ia_matrix()
                                        .loc["year2001", :, :]
                                        .reset_coords(drop=True),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: historic_ia_matrix()
                                            .loc["year2000", :, :]
                                            .reset_coords(drop=True),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: historic_ia_matrix()
                                                .loc["year1999", :, :]
                                                .reset_coords(drop=True),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: historic_ia_matrix()
                                                    .loc["year1998", :, :]
                                                    .reset_coords(drop=True),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: historic_ia_matrix()
                                                        .loc["year1997", :, :]
                                                        .reset_coords(drop=True),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: historic_ia_matrix()
                                                            .loc["year1996", :, :]
                                                            .reset_coords(drop=True),
                                                            lambda: historic_ia_matrix()
                                                            .loc["year1995", :, :]
                                                            .reset_coords(drop=True),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="IA Matrix Domestic",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_domestic():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA Matrix Exports 0",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_exports_0():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 0"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 0"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA Matrix Exports 1",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_exports_1():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 1"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 1"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA Matrix Imports 0",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_imports_0():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec map 0"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 0", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA Matrix Imports 1",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_imports_1():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec map 1"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 1", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief Matrix",
    subscripts=["sectors A matrix", "sectors A matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 14, "historic_leontief_matrix": 15},
)
def leontief_matrix():
    return if_then_else(
        time() >= 2009,
        lambda: historic_leontief_matrix()
        .loc["year2009", :, :]
        .reset_coords(drop=True),
        lambda: if_then_else(
            time() >= 2008,
            lambda: historic_leontief_matrix()
            .loc["year2008", :, :]
            .reset_coords(drop=True),
            lambda: if_then_else(
                time() >= 2007,
                lambda: historic_leontief_matrix()
                .loc["year2007", :, :]
                .reset_coords(drop=True),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: historic_leontief_matrix()
                    .loc["year2006", :, :]
                    .reset_coords(drop=True),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: historic_leontief_matrix()
                        .loc["year2005", :, :]
                        .reset_coords(drop=True),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: historic_leontief_matrix()
                            .loc["year2004", :, :]
                            .reset_coords(drop=True),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: historic_leontief_matrix()
                                .loc["year2003", :, :]
                                .reset_coords(drop=True),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: historic_leontief_matrix()
                                    .loc["year2002", :, :]
                                    .reset_coords(drop=True),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: historic_leontief_matrix()
                                        .loc["year2001", :, :]
                                        .reset_coords(drop=True),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: historic_leontief_matrix()
                                            .loc["year2000", :, :]
                                            .reset_coords(drop=True),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: historic_leontief_matrix()
                                                .loc["year1999", :, :]
                                                .reset_coords(drop=True),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: historic_leontief_matrix()
                                                    .loc["year1998", :, :]
                                                    .reset_coords(drop=True),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: historic_leontief_matrix()
                                                        .loc["year1997", :, :]
                                                        .reset_coords(drop=True),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: historic_leontief_matrix()
                                                            .loc["year1996", :, :]
                                                            .reset_coords(drop=True),
                                                            lambda: historic_leontief_matrix()
                                                            .loc["year1995", :, :]
                                                            .reset_coords(drop=True),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Leontief Matrix Domestic",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_domestic():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief Matrix Exports 0",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_exports_0():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 0"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 0"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief Matrix Exports 1",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_exports_1():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec map 2"], _subscript_dict["secb map 1"]]
        .rename({"sectors A matrix": "sec map 2", "sectors A matrix1": "secb map 1"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief Matrix Imports 0",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_imports_0():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec map 0"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 0", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief Matrix Imports 1",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_imports_1():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec map 1"], _subscript_dict["secb map 2"]]
        .rename({"sectors A matrix": "sec map 1", "sectors A matrix1": "secb map 2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )
