"""
Module economy.coefficient_matrices
Translated using PySD version 3.14.2
"""

@component.add(
    name="historic_A_Matrix",
    units="Dmnl",
    subscripts=["economic_years", "sectors_A_matrix", "sectors_A_matrix1"],
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
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1995",
    {
        "economic_years": ["year1995"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
    _root,
    {
        "economic_years": _subscript_dict["economic_years"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
    "_ext_constant_historic_a_matrix",
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1996",
    {
        "economic_years": ["year1996"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1997",
    {
        "economic_years": ["year1997"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1998",
    {
        "economic_years": ["year1998"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year1999",
    {
        "economic_years": ["year1999"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2000",
    {
        "economic_years": ["year2000"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2001",
    {
        "economic_years": ["year2001"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2002",
    {
        "economic_years": ["year2002"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2003",
    {
        "economic_years": ["year2003"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2004",
    {
        "economic_years": ["year2004"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2005",
    {
        "economic_years": ["year2005"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2006",
    {
        "economic_years": ["year2006"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2007",
    {
        "economic_years": ["year2007"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2008",
    {
        "economic_years": ["year2008"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2009",
    {
        "economic_years": ["year2009"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2010",
    {
        "economic_years": ["year2010"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2011",
    {
        "economic_years": ["year2011"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2012",
    {
        "economic_years": ["year2012"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2013",
    {
        "economic_years": ["year2013"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)

_ext_constant_historic_a_matrix.add(
    r"../economy.xlsx",
    "Catalonia",
    "historic_A_Matrix_year2014",
    {
        "economic_years": ["year2014"],
        "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
        "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
    },
)


@component.add(
    name="historic_IA_Matrix",
    units="Dmnl",
    subscripts=["economic_years", "sectors_A_matrix", "sectors_A_matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"i_matrix": 1, "historic_a_matrix": 1},
)
def historic_ia_matrix():
    return (
        i_matrix()
        - historic_a_matrix().transpose(
            "sectors_A_matrix", "sectors_A_matrix1", "economic_years"
        )
    ).transpose("economic_years", "sectors_A_matrix", "sectors_A_matrix1")


@component.add(
    name="historic_Leontief_Matrix",
    units="Dmnl",
    subscripts=["economic_years", "sectors_A_matrix", "sectors_A_matrix1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_ia_matrix": 1},
)
def historic_leontief_matrix():
    return invert_matrix(historic_ia_matrix())


@component.add(
    name="I_Matrix",
    units="Dmnl",
    subscripts=["sectors_A_matrix", "sectors_A_matrix1"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def i_matrix():
    return if_then_else(
        xr.DataArray(
            np.arange(1, len(_subscript_dict["sectors_A_matrix"]) + 1),
            {"sectors_A_matrix": _subscript_dict["sectors_A_matrix"]},
            ["sectors_A_matrix"],
        )
        == xr.DataArray(
            np.arange(1, len(_subscript_dict["sectors_A_matrix1"]) + 1),
            {"sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"]},
            ["sectors_A_matrix1"],
        ),
        lambda: xr.DataArray(
            1,
            {
                "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
                "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
            },
            ["sectors_A_matrix", "sectors_A_matrix1"],
        ),
        lambda: xr.DataArray(
            0,
            {
                "sectors_A_matrix": _subscript_dict["sectors_A_matrix"],
                "sectors_A_matrix1": _subscript_dict["sectors_A_matrix1"],
            },
            ["sectors_A_matrix", "sectors_A_matrix1"],
        ),
    )


@component.add(
    name="IA_Matrix",
    units="Dmnl",
    subscripts=["sectors_A_matrix", "sectors_A_matrix1"],
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
    name="IA_Matrix_Domestic",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_domestic():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA_Matrix_Exports_0",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_exports_0():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_0"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_0"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA_Matrix_Exports_1",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_exports_1():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_1"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_1"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA_Matrix_Imports_0",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_imports_0():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec_map_0"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_0", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="IA_Matrix_Imports_1",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ia_matrix": 1},
)
def ia_matrix_imports_1():
    return xr.DataArray(
        ia_matrix()
        .loc[_subscript_dict["sec_map_1"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_1", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief_Matrix",
    units="Dmnl",
    subscripts=["sectors_A_matrix", "sectors_A_matrix1"],
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
    name="Leontief_Matrix_Domestic",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_domestic():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief_Matrix_Exports_0",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_exports_0():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_0"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_0"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief_Matrix_Exports_1",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_exports_1():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec_map_2"], _subscript_dict["secb_map_1"]]
        .rename({"sectors_A_matrix": "sec_map_2", "sectors_A_matrix1": "secb_map_1"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief_Matrix_Imports_0",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_imports_0():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec_map_0"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_0", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )


@component.add(
    name="Leontief_Matrix_Imports_1",
    units="Dmnl",
    subscripts=["sectors", "sectors1"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix": 1},
)
def leontief_matrix_imports_1():
    return xr.DataArray(
        leontief_matrix()
        .loc[_subscript_dict["sec_map_1"], _subscript_dict["secb_map_2"]]
        .rename({"sectors_A_matrix": "sec_map_1", "sectors_A_matrix1": "secb_map_2"})
        .values,
        {
            "sectors": _subscript_dict["sectors"],
            "sectors1": _subscript_dict["sectors1"],
        },
        ["sectors", "sectors1"],
    )
