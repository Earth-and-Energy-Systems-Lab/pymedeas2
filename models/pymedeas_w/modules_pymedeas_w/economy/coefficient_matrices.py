"""
Module economy.coefficient_matrices
Translated using PySD version 3.9.1
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
    Historic A Matrix WIOD database.
    """
    return _ext_constant_historic_a_matrix()


_ext_constant_historic_a_matrix = ExtConstant(
    "../economy.xlsx",
    "World",
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
    "World",
    "historic_A_Matrix_year1996",
    {
        "economic years": ["year1996"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year1997",
    {
        "economic years": ["year1997"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year1998",
    {
        "economic years": ["year1998"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year1999",
    {
        "economic years": ["year1999"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2000",
    {
        "economic years": ["year2000"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2001",
    {
        "economic years": ["year2001"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2002",
    {
        "economic years": ["year2002"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2003",
    {
        "economic years": ["year2003"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2004",
    {
        "economic years": ["year2004"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2005",
    {
        "economic years": ["year2005"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2006",
    {
        "economic years": ["year2006"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2007",
    {
        "economic years": ["year2007"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2008",
    {
        "economic years": ["year2008"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2009",
    {
        "economic years": ["year2009"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2010",
    {
        "economic years": ["year2010"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2011",
    {
        "economic years": ["year2011"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2012",
    {
        "economic years": ["year2012"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
    "historic_A_Matrix_year2013",
    {
        "economic years": ["year2013"],
        "sectors A matrix": _subscript_dict["sectors A matrix"],
        "sectors A matrix1": _subscript_dict["sectors A matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    "../economy.xlsx",
    "World",
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
    """
    Historic I-A Matrix.
    """
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
    """
    Identity matrix.
    """
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
    name="IA matrix",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 14, "historic_ia_matrix": 15},
)
def ia_matrix():
    """
    I-A matrix WIOD database
    """
    return if_then_else(
        time() >= 2009,
        lambda: xr.DataArray(
            historic_ia_matrix().loc["year2009", :, :].reset_coords(drop=True).values,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        ),
        lambda: if_then_else(
            time() >= 2008,
            lambda: xr.DataArray(
                historic_ia_matrix()
                .loc["year2008", :, :]
                .reset_coords(drop=True)
                .values,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1"],
            ),
            lambda: if_then_else(
                time() >= 2007,
                lambda: xr.DataArray(
                    historic_ia_matrix()
                    .loc["year2007", :, :]
                    .reset_coords(drop=True)
                    .values,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "sectors1": _subscript_dict["sectors1"],
                    },
                    ["sectors", "sectors1"],
                ),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: xr.DataArray(
                        historic_ia_matrix()
                        .loc["year2006", :, :]
                        .reset_coords(drop=True)
                        .values,
                        {
                            "sectors": _subscript_dict["sectors"],
                            "sectors1": _subscript_dict["sectors1"],
                        },
                        ["sectors", "sectors1"],
                    ),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: xr.DataArray(
                            historic_ia_matrix()
                            .loc["year2005", :, :]
                            .reset_coords(drop=True)
                            .values,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "sectors1": _subscript_dict["sectors1"],
                            },
                            ["sectors", "sectors1"],
                        ),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: xr.DataArray(
                                historic_ia_matrix()
                                .loc["year2004", :, :]
                                .reset_coords(drop=True)
                                .values,
                                {
                                    "sectors": _subscript_dict["sectors"],
                                    "sectors1": _subscript_dict["sectors1"],
                                },
                                ["sectors", "sectors1"],
                            ),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: xr.DataArray(
                                    historic_ia_matrix()
                                    .loc["year2003", :, :]
                                    .reset_coords(drop=True)
                                    .values,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "sectors1": _subscript_dict["sectors1"],
                                    },
                                    ["sectors", "sectors1"],
                                ),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: xr.DataArray(
                                        historic_ia_matrix()
                                        .loc["year2002", :, :]
                                        .reset_coords(drop=True)
                                        .values,
                                        {
                                            "sectors": _subscript_dict["sectors"],
                                            "sectors1": _subscript_dict["sectors1"],
                                        },
                                        ["sectors", "sectors1"],
                                    ),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: xr.DataArray(
                                            historic_ia_matrix()
                                            .loc["year2001", :, :]
                                            .reset_coords(drop=True)
                                            .values,
                                            {
                                                "sectors": _subscript_dict["sectors"],
                                                "sectors1": _subscript_dict["sectors1"],
                                            },
                                            ["sectors", "sectors1"],
                                        ),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: xr.DataArray(
                                                historic_ia_matrix()
                                                .loc["year2000", :, :]
                                                .reset_coords(drop=True)
                                                .values,
                                                {
                                                    "sectors": _subscript_dict[
                                                        "sectors"
                                                    ],
                                                    "sectors1": _subscript_dict[
                                                        "sectors1"
                                                    ],
                                                },
                                                ["sectors", "sectors1"],
                                            ),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: xr.DataArray(
                                                    historic_ia_matrix()
                                                    .loc["year1999", :, :]
                                                    .reset_coords(drop=True)
                                                    .values,
                                                    {
                                                        "sectors": _subscript_dict[
                                                            "sectors"
                                                        ],
                                                        "sectors1": _subscript_dict[
                                                            "sectors1"
                                                        ],
                                                    },
                                                    ["sectors", "sectors1"],
                                                ),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: xr.DataArray(
                                                        historic_ia_matrix()
                                                        .loc["year1998", :, :]
                                                        .reset_coords(drop=True)
                                                        .values,
                                                        {
                                                            "sectors": _subscript_dict[
                                                                "sectors"
                                                            ],
                                                            "sectors1": _subscript_dict[
                                                                "sectors1"
                                                            ],
                                                        },
                                                        ["sectors", "sectors1"],
                                                    ),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: xr.DataArray(
                                                            historic_ia_matrix()
                                                            .loc["year1997", :, :]
                                                            .reset_coords(drop=True)
                                                            .values,
                                                            {
                                                                "sectors": _subscript_dict[
                                                                    "sectors"
                                                                ],
                                                                "sectors1": _subscript_dict[
                                                                    "sectors1"
                                                                ],
                                                            },
                                                            ["sectors", "sectors1"],
                                                        ),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: xr.DataArray(
                                                                historic_ia_matrix()
                                                                .loc["year1996", :, :]
                                                                .reset_coords(drop=True)
                                                                .values,
                                                                {
                                                                    "sectors": _subscript_dict[
                                                                        "sectors"
                                                                    ],
                                                                    "sectors1": _subscript_dict[
                                                                        "sectors1"
                                                                    ],
                                                                },
                                                                ["sectors", "sectors1"],
                                                            ),
                                                            lambda: xr.DataArray(
                                                                historic_ia_matrix()
                                                                .loc["year1995", :, :]
                                                                .reset_coords(drop=True)
                                                                .values,
                                                                {
                                                                    "sectors": _subscript_dict[
                                                                        "sectors"
                                                                    ],
                                                                    "sectors1": _subscript_dict[
                                                                        "sectors1"
                                                                    ],
                                                                },
                                                                ["sectors", "sectors1"],
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
        ),
    )


@component.add(
    name="Leontief Matrix",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 14, "historic_leontief_matrix": 15},
)
def leontief_matrix():
    """
    Leontieff matrix.
    """
    return if_then_else(
        time() >= 2009,
        lambda: xr.DataArray(
            historic_leontief_matrix()
            .loc["year2009", :, :]
            .reset_coords(drop=True)
            .values,
            {
                "sectors": _subscript_dict["sectors"],
                "sectors1": _subscript_dict["sectors1"],
            },
            ["sectors", "sectors1"],
        ),
        lambda: if_then_else(
            time() >= 2008,
            lambda: xr.DataArray(
                historic_leontief_matrix()
                .loc["year2008", :, :]
                .reset_coords(drop=True)
                .values,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1"],
            ),
            lambda: if_then_else(
                time() >= 2007,
                lambda: xr.DataArray(
                    historic_leontief_matrix()
                    .loc["year2007", :, :]
                    .reset_coords(drop=True)
                    .values,
                    {
                        "sectors": _subscript_dict["sectors"],
                        "sectors1": _subscript_dict["sectors1"],
                    },
                    ["sectors", "sectors1"],
                ),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: xr.DataArray(
                        historic_leontief_matrix()
                        .loc["year2006", :, :]
                        .reset_coords(drop=True)
                        .values,
                        {
                            "sectors": _subscript_dict["sectors"],
                            "sectors1": _subscript_dict["sectors1"],
                        },
                        ["sectors", "sectors1"],
                    ),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: xr.DataArray(
                            historic_leontief_matrix()
                            .loc["year2005", :, :]
                            .reset_coords(drop=True)
                            .values,
                            {
                                "sectors": _subscript_dict["sectors"],
                                "sectors1": _subscript_dict["sectors1"],
                            },
                            ["sectors", "sectors1"],
                        ),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: xr.DataArray(
                                historic_leontief_matrix()
                                .loc["year2004", :, :]
                                .reset_coords(drop=True)
                                .values,
                                {
                                    "sectors": _subscript_dict["sectors"],
                                    "sectors1": _subscript_dict["sectors1"],
                                },
                                ["sectors", "sectors1"],
                            ),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: xr.DataArray(
                                    historic_leontief_matrix()
                                    .loc["year2003", :, :]
                                    .reset_coords(drop=True)
                                    .values,
                                    {
                                        "sectors": _subscript_dict["sectors"],
                                        "sectors1": _subscript_dict["sectors1"],
                                    },
                                    ["sectors", "sectors1"],
                                ),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: xr.DataArray(
                                        historic_leontief_matrix()
                                        .loc["year2002", :, :]
                                        .reset_coords(drop=True)
                                        .values,
                                        {
                                            "sectors": _subscript_dict["sectors"],
                                            "sectors1": _subscript_dict["sectors1"],
                                        },
                                        ["sectors", "sectors1"],
                                    ),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: xr.DataArray(
                                            historic_leontief_matrix()
                                            .loc["year2001", :, :]
                                            .reset_coords(drop=True)
                                            .values,
                                            {
                                                "sectors": _subscript_dict["sectors"],
                                                "sectors1": _subscript_dict["sectors1"],
                                            },
                                            ["sectors", "sectors1"],
                                        ),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: xr.DataArray(
                                                historic_leontief_matrix()
                                                .loc["year2000", :, :]
                                                .reset_coords(drop=True)
                                                .values,
                                                {
                                                    "sectors": _subscript_dict[
                                                        "sectors"
                                                    ],
                                                    "sectors1": _subscript_dict[
                                                        "sectors1"
                                                    ],
                                                },
                                                ["sectors", "sectors1"],
                                            ),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: xr.DataArray(
                                                    historic_leontief_matrix()
                                                    .loc["year1999", :, :]
                                                    .reset_coords(drop=True)
                                                    .values,
                                                    {
                                                        "sectors": _subscript_dict[
                                                            "sectors"
                                                        ],
                                                        "sectors1": _subscript_dict[
                                                            "sectors1"
                                                        ],
                                                    },
                                                    ["sectors", "sectors1"],
                                                ),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: xr.DataArray(
                                                        historic_leontief_matrix()
                                                        .loc["year1998", :, :]
                                                        .reset_coords(drop=True)
                                                        .values,
                                                        {
                                                            "sectors": _subscript_dict[
                                                                "sectors"
                                                            ],
                                                            "sectors1": _subscript_dict[
                                                                "sectors1"
                                                            ],
                                                        },
                                                        ["sectors", "sectors1"],
                                                    ),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: xr.DataArray(
                                                            historic_leontief_matrix()
                                                            .loc["year1997", :, :]
                                                            .reset_coords(drop=True)
                                                            .values,
                                                            {
                                                                "sectors": _subscript_dict[
                                                                    "sectors"
                                                                ],
                                                                "sectors1": _subscript_dict[
                                                                    "sectors1"
                                                                ],
                                                            },
                                                            ["sectors", "sectors1"],
                                                        ),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: xr.DataArray(
                                                                historic_leontief_matrix()
                                                                .loc["year1996", :, :]
                                                                .reset_coords(drop=True)
                                                                .values,
                                                                {
                                                                    "sectors": _subscript_dict[
                                                                        "sectors"
                                                                    ],
                                                                    "sectors1": _subscript_dict[
                                                                        "sectors1"
                                                                    ],
                                                                },
                                                                ["sectors", "sectors1"],
                                                            ),
                                                            lambda: xr.DataArray(
                                                                historic_leontief_matrix()
                                                                .loc["year1995", :, :]
                                                                .reset_coords(drop=True)
                                                                .values,
                                                                {
                                                                    "sectors": _subscript_dict[
                                                                        "sectors"
                                                                    ],
                                                                    "sectors1": _subscript_dict[
                                                                        "sectors1"
                                                                    ],
                                                                },
                                                                ["sectors", "sectors1"],
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
        ),
    )
