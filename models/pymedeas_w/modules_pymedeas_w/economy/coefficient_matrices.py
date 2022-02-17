"""
Module coefficient_matrices
Translated using PySD version 2.2.1
"""


@subs(["economic years", "sectors A matrix", "sectors A matrix1"], _subscript_dict)
def historic_a_matrix():
    """
    Real Name: historic A Matrix
    Original Eqn:
      GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'historic_A_Matrix_year1995')
        .
        .
        .
      GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'historic_A_Matrix_year2014')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['economic years', 'sectors A matrix', 'sectors A matrix1']

    Historic A Matrix WIOD database.
    """
    return _ext_constant_historic_a_matrix()


@subs(["economic years", "sectors A matrix", "sectors A matrix1"], _subscript_dict)
def historic_ia_matrix():
    """
    Real Name: historic IA Matrix
    Original Eqn: I Matrix[sectors A matrix,sectors A matrix1]-historic A Matrix[economic years,sectors A matrix,sectors A matrix1]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['economic years', 'sectors A matrix', 'sectors A matrix1']

    Historic I-A Matrix.
    """
    return i_matrix() - historic_a_matrix()


@subs(["economic years", "sectors A matrix", "sectors A matrix1"], _subscript_dict)
def historic_leontief_matrix():
    """
    Real Name: historic Leontief Matrix
    Original Eqn: INVERT MATRIX(historic IA Matrix[economic years,sectors A matrix,sectors A matrix1],ELMCOUNT(sectors A matrix))
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['economic years', 'sectors A matrix', 'sectors A matrix1']


    """
    return invert_matrix(historic_ia_matrix())


@subs(["sectors A matrix", "sectors A matrix1"], _subscript_dict)
def i_matrix():
    """
    Real Name: I Matrix
    Original Eqn: IF THEN ELSE(sectors A matrix=sectors A matrix1, 1, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors A matrix', 'sectors A matrix1']

    Identity matrix.
    """
    return xr.DataArray(
        np.eye(len(_subscript_dict["sectors A matrix"])),
        {
            "sectors A matrix": _subscript_dict["sectors A matrix"],
            "sectors A matrix1": _subscript_dict["sectors A matrix1"]
        },
        ["sectors A matrix", "sectors A matrix1"]
    )



@subs(["sectors", "sectors1"], _subscript_dict)
def ia_matrix():
    """
    Real Name: IA matrix
    Original Eqn: IF THEN ELSE(Time>=2009, historic IA Matrix[year2009,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2008, historic IA Matrix[year2008,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2007, historic IA Matrix[year2007,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2006, historic IA Matrix[year2006,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2005, historic IA Matrix[year2005,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2004, historic IA Matrix[year2004,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2003, historic IA Matrix[year2003,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2002, historic IA Matrix[year2002,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2001, historic IA Matrix[year2001,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2000, historic IA Matrix[year2000,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1999, historic IA Matrix[year1999,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1998, historic IA Matrix[year1998,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1997, historic IA Matrix[year1997,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1996, historic IA Matrix[year1996,sectors A matrix,sectors A matrix1], historic IA Matrix[year1995,sectors A matrix,sectors A matrix1]))))))))))))))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'sectors1']

    I-A matrix WIOD database
    """
    return if_then_else(
        time() >= 2009,
        lambda: rearrange(
            rearrange(
                historic_ia_matrix().loc["year2009", :, :].reset_coords(drop=True),
                ["sectors A matrix", "sectors A matrix1"],
                _subscript_dict,
            ),
            ["sectors", "sectors1"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            time() >= 2008,
            lambda: rearrange(
                rearrange(
                    historic_ia_matrix().loc["year2008", :, :].reset_coords(drop=True),
                    ["sectors A matrix", "sectors A matrix1"],
                    _subscript_dict,
                ),
                ["sectors", "sectors1"],
                _subscript_dict,
            ),
            lambda: if_then_else(
                time() >= 2007,
                lambda: rearrange(
                    rearrange(
                        historic_ia_matrix()
                        .loc["year2007", :, :]
                        .reset_coords(drop=True),
                        ["sectors A matrix", "sectors A matrix1"],
                        _subscript_dict,
                    ),
                    ["sectors", "sectors1"],
                    _subscript_dict,
                ),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: rearrange(
                        rearrange(
                            historic_ia_matrix()
                            .loc["year2006", :, :]
                            .reset_coords(drop=True),
                            ["sectors A matrix", "sectors A matrix1"],
                            _subscript_dict,
                        ),
                        ["sectors", "sectors1"],
                        _subscript_dict,
                    ),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: rearrange(
                            rearrange(
                                historic_ia_matrix()
                                .loc["year2005", :, :]
                                .reset_coords(drop=True),
                                ["sectors A matrix", "sectors A matrix1"],
                                _subscript_dict,
                            ),
                            ["sectors", "sectors1"],
                            _subscript_dict,
                        ),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: rearrange(
                                rearrange(
                                    historic_ia_matrix()
                                    .loc["year2004", :, :]
                                    .reset_coords(drop=True),
                                    ["sectors A matrix", "sectors A matrix1"],
                                    _subscript_dict,
                                ),
                                ["sectors", "sectors1"],
                                _subscript_dict,
                            ),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: rearrange(
                                    rearrange(
                                        historic_ia_matrix()
                                        .loc["year2003", :, :]
                                        .reset_coords(drop=True),
                                        ["sectors A matrix", "sectors A matrix1"],
                                        _subscript_dict,
                                    ),
                                    ["sectors", "sectors1"],
                                    _subscript_dict,
                                ),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: rearrange(
                                        rearrange(
                                            historic_ia_matrix()
                                            .loc["year2002", :, :]
                                            .reset_coords(drop=True),
                                            ["sectors A matrix", "sectors A matrix1"],
                                            _subscript_dict,
                                        ),
                                        ["sectors", "sectors1"],
                                        _subscript_dict,
                                    ),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: rearrange(
                                            rearrange(
                                                historic_ia_matrix()
                                                .loc["year2001", :, :]
                                                .reset_coords(drop=True),
                                                [
                                                    "sectors A matrix",
                                                    "sectors A matrix1",
                                                ],
                                                _subscript_dict,
                                            ),
                                            ["sectors", "sectors1"],
                                            _subscript_dict,
                                        ),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: rearrange(
                                                rearrange(
                                                    historic_ia_matrix()
                                                    .loc["year2000", :, :]
                                                    .reset_coords(drop=True),
                                                    [
                                                        "sectors A matrix",
                                                        "sectors A matrix1",
                                                    ],
                                                    _subscript_dict,
                                                ),
                                                ["sectors", "sectors1"],
                                                _subscript_dict,
                                            ),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: rearrange(
                                                    rearrange(
                                                        historic_ia_matrix()
                                                        .loc["year1999", :, :]
                                                        .reset_coords(drop=True),
                                                        [
                                                            "sectors A matrix",
                                                            "sectors A matrix1",
                                                        ],
                                                        _subscript_dict,
                                                    ),
                                                    ["sectors", "sectors1"],
                                                    _subscript_dict,
                                                ),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: rearrange(
                                                        rearrange(
                                                            historic_ia_matrix()
                                                            .loc["year1998", :, :]
                                                            .reset_coords(drop=True),
                                                            [
                                                                "sectors A matrix",
                                                                "sectors A matrix1",
                                                            ],
                                                            _subscript_dict,
                                                        ),
                                                        ["sectors", "sectors1"],
                                                        _subscript_dict,
                                                    ),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: rearrange(
                                                            rearrange(
                                                                historic_ia_matrix()
                                                                .loc["year1997", :, :]
                                                                .reset_coords(
                                                                    drop=True
                                                                ),
                                                                [
                                                                    "sectors A matrix",
                                                                    "sectors A matrix1",
                                                                ],
                                                                _subscript_dict,
                                                            ),
                                                            ["sectors", "sectors1"],
                                                            _subscript_dict,
                                                        ),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: rearrange(
                                                                rearrange(
                                                                    historic_ia_matrix()
                                                                    .loc[
                                                                        "year1996", :, :
                                                                    ]
                                                                    .reset_coords(
                                                                        drop=True
                                                                    ),
                                                                    [
                                                                        "sectors A matrix",
                                                                        "sectors A matrix1",
                                                                    ],
                                                                    _subscript_dict,
                                                                ),
                                                                ["sectors", "sectors1"],
                                                                _subscript_dict,
                                                            ),
                                                            lambda: rearrange(
                                                                rearrange(
                                                                    historic_ia_matrix()
                                                                    .loc[
                                                                        "year1995", :, :
                                                                    ]
                                                                    .reset_coords(
                                                                        drop=True
                                                                    ),
                                                                    [
                                                                        "sectors A matrix",
                                                                        "sectors A matrix1",
                                                                    ],
                                                                    _subscript_dict,
                                                                ),
                                                                ["sectors", "sectors1"],
                                                                _subscript_dict,
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


@subs(["sectors", "sectors1"], _subscript_dict)
def leontief_matrix():
    """
    Real Name: Leontief Matrix
    Original Eqn: IF THEN ELSE(Time>=2009, historic Leontief Matrix[year2009,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2008, historic Leontief Matrix[year2008,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2007, historic Leontief Matrix[year2007,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2006, historic Leontief Matrix[year2006,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2005, historic Leontief Matrix[year2005,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2004, historic Leontief Matrix[year2004,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2003, historic Leontief Matrix[year2003,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2002, historic Leontief Matrix[year2002,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2001, historic Leontief Matrix[year2001,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=2000, historic Leontief Matrix[year2000,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1999, historic Leontief Matrix[year1999,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1998, historic Leontief Matrix[year1998,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1997, historic Leontief Matrix[year1997,sectors A matrix,sectors A matrix1], IF THEN ELSE(Time>=1996, historic Leontief Matrix[year1996,sectors A matrix,sectors A matrix1], historic Leontief Matrix[year1995,sectors A matrix,sectors A matrix1]))))))))))))))
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors', 'sectors1']

    Leontieff matrix.
    """
    return if_then_else(
        time() >= 2009,
        lambda: rearrange(
            rearrange(
                historic_leontief_matrix()
                .loc["year2009", :, :]
                .reset_coords(drop=True),
                ["sectors A matrix", "sectors A matrix1"],
                _subscript_dict,
            ),
            ["sectors", "sectors1"],
            _subscript_dict,
        ),
        lambda: if_then_else(
            time() >= 2008,
            lambda: rearrange(
                rearrange(
                    historic_leontief_matrix()
                    .loc["year2008", :, :]
                    .reset_coords(drop=True),
                    ["sectors A matrix", "sectors A matrix1"],
                    _subscript_dict,
                ),
                ["sectors", "sectors1"],
                _subscript_dict,
            ),
            lambda: if_then_else(
                time() >= 2007,
                lambda: rearrange(
                    rearrange(
                        historic_leontief_matrix()
                        .loc["year2007", :, :]
                        .reset_coords(drop=True),
                        ["sectors A matrix", "sectors A matrix1"],
                        _subscript_dict,
                    ),
                    ["sectors", "sectors1"],
                    _subscript_dict,
                ),
                lambda: if_then_else(
                    time() >= 2006,
                    lambda: rearrange(
                        rearrange(
                            historic_leontief_matrix()
                            .loc["year2006", :, :]
                            .reset_coords(drop=True),
                            ["sectors A matrix", "sectors A matrix1"],
                            _subscript_dict,
                        ),
                        ["sectors", "sectors1"],
                        _subscript_dict,
                    ),
                    lambda: if_then_else(
                        time() >= 2005,
                        lambda: rearrange(
                            rearrange(
                                historic_leontief_matrix()
                                .loc["year2005", :, :]
                                .reset_coords(drop=True),
                                ["sectors A matrix", "sectors A matrix1"],
                                _subscript_dict,
                            ),
                            ["sectors", "sectors1"],
                            _subscript_dict,
                        ),
                        lambda: if_then_else(
                            time() >= 2004,
                            lambda: rearrange(
                                rearrange(
                                    historic_leontief_matrix()
                                    .loc["year2004", :, :]
                                    .reset_coords(drop=True),
                                    ["sectors A matrix", "sectors A matrix1"],
                                    _subscript_dict,
                                ),
                                ["sectors", "sectors1"],
                                _subscript_dict,
                            ),
                            lambda: if_then_else(
                                time() >= 2003,
                                lambda: rearrange(
                                    rearrange(
                                        historic_leontief_matrix()
                                        .loc["year2003", :, :]
                                        .reset_coords(drop=True),
                                        ["sectors A matrix", "sectors A matrix1"],
                                        _subscript_dict,
                                    ),
                                    ["sectors", "sectors1"],
                                    _subscript_dict,
                                ),
                                lambda: if_then_else(
                                    time() >= 2002,
                                    lambda: rearrange(
                                        rearrange(
                                            historic_leontief_matrix()
                                            .loc["year2002", :, :]
                                            .reset_coords(drop=True),
                                            ["sectors A matrix", "sectors A matrix1"],
                                            _subscript_dict,
                                        ),
                                        ["sectors", "sectors1"],
                                        _subscript_dict,
                                    ),
                                    lambda: if_then_else(
                                        time() >= 2001,
                                        lambda: rearrange(
                                            rearrange(
                                                historic_leontief_matrix()
                                                .loc["year2001", :, :]
                                                .reset_coords(drop=True),
                                                [
                                                    "sectors A matrix",
                                                    "sectors A matrix1",
                                                ],
                                                _subscript_dict,
                                            ),
                                            ["sectors", "sectors1"],
                                            _subscript_dict,
                                        ),
                                        lambda: if_then_else(
                                            time() >= 2000,
                                            lambda: rearrange(
                                                rearrange(
                                                    historic_leontief_matrix()
                                                    .loc["year2000", :, :]
                                                    .reset_coords(drop=True),
                                                    [
                                                        "sectors A matrix",
                                                        "sectors A matrix1",
                                                    ],
                                                    _subscript_dict,
                                                ),
                                                ["sectors", "sectors1"],
                                                _subscript_dict,
                                            ),
                                            lambda: if_then_else(
                                                time() >= 1999,
                                                lambda: rearrange(
                                                    rearrange(
                                                        historic_leontief_matrix()
                                                        .loc["year1999", :, :]
                                                        .reset_coords(drop=True),
                                                        [
                                                            "sectors A matrix",
                                                            "sectors A matrix1",
                                                        ],
                                                        _subscript_dict,
                                                    ),
                                                    ["sectors", "sectors1"],
                                                    _subscript_dict,
                                                ),
                                                lambda: if_then_else(
                                                    time() >= 1998,
                                                    lambda: rearrange(
                                                        rearrange(
                                                            historic_leontief_matrix()
                                                            .loc["year1998", :, :]
                                                            .reset_coords(drop=True),
                                                            [
                                                                "sectors A matrix",
                                                                "sectors A matrix1",
                                                            ],
                                                            _subscript_dict,
                                                        ),
                                                        ["sectors", "sectors1"],
                                                        _subscript_dict,
                                                    ),
                                                    lambda: if_then_else(
                                                        time() >= 1997,
                                                        lambda: rearrange(
                                                            rearrange(
                                                                historic_leontief_matrix()
                                                                .loc["year1997", :, :]
                                                                .reset_coords(
                                                                    drop=True
                                                                ),
                                                                [
                                                                    "sectors A matrix",
                                                                    "sectors A matrix1",
                                                                ],
                                                                _subscript_dict,
                                                            ),
                                                            ["sectors", "sectors1"],
                                                            _subscript_dict,
                                                        ),
                                                        lambda: if_then_else(
                                                            time() >= 1996,
                                                            lambda: rearrange(
                                                                rearrange(
                                                                    historic_leontief_matrix()
                                                                    .loc[
                                                                        "year1996", :, :
                                                                    ]
                                                                    .reset_coords(
                                                                        drop=True
                                                                    ),
                                                                    [
                                                                        "sectors A matrix",
                                                                        "sectors A matrix1",
                                                                    ],
                                                                    _subscript_dict,
                                                                ),
                                                                ["sectors", "sectors1"],
                                                                _subscript_dict,
                                                            ),
                                                            lambda: rearrange(
                                                                rearrange(
                                                                    historic_leontief_matrix()
                                                                    .loc[
                                                                        "year1995", :, :
                                                                    ]
                                                                    .reset_coords(
                                                                        drop=True
                                                                    ),
                                                                    [
                                                                        "sectors A matrix",
                                                                        "sectors A matrix1",
                                                                    ],
                                                                    _subscript_dict,
                                                                ),
                                                                ["sectors", "sectors1"],
                                                                _subscript_dict,
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
