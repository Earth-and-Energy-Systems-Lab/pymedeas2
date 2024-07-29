"""
Module economy.economic_demand
Translated using PySD version 3.14.1
"""

@component.add(
    name="demand by sector FD adjusted",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_cat": 1, "diff_demand_cat": 1},
)
def demand_by_sector_fd_adjusted():
    """
    Demand by sector after adjustment to match the desired GDP level.
    """
    return demand_by_sector_fd_cat() * diff_demand_cat()


@component.add(
    name="Demand by sector FD CAT",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_demand_by_sector_fd_cat": 1},
    other_deps={
        "_integ_demand_by_sector_fd_cat": {
            "initial": {"initial_demand": 1},
            "step": {
                "variation_demand_flow_fd_cat": 1,
                "demand_not_covered_by_sector_fd_cat": 1,
            },
        }
    },
)
def demand_by_sector_fd_cat():
    """
    Final demand by EU28 35 industrial sectors
    """
    return _integ_demand_by_sector_fd_cat()


_integ_demand_by_sector_fd_cat = Integ(
    lambda: variation_demand_flow_fd_cat() - demand_not_covered_by_sector_fd_cat(),
    lambda: initial_demand(),
    "_integ_demand_by_sector_fd_cat",
)


@component.add(
    name="demand not covered by sector FD CAT",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "real_final_demand_by_sector_cat": 1,
        "demand_by_sector_fd_cat": 1,
        "nvs_1_year": 1,
    },
)
def demand_not_covered_by_sector_fd_cat():
    """
    Gap between final demand required and real final demand (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: (demand_by_sector_fd_cat() - real_final_demand_by_sector_cat())
        / nvs_1_year(),
    )


@component.add(
    name="demand not covered total FD",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_not_covered_by_sector_fd_cat": 1},
)
def demand_not_covered_total_fd():
    return sum(
        demand_not_covered_by_sector_fd_cat().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="diff demand CAT",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "real_demand_delayed_1yr": 1,
        "total_demand": 1,
        "desired_annual_total_demand_growth_rate_delayed_1_yr": 1,
        "nvs_1_year": 1,
    },
)
def diff_demand_cat():
    """
    Ratio between the desired GDP and the real GDP level after applying the demand function.
    """
    return (
        if_then_else(
            time() < 2009,
            lambda: 1,
            lambda: (
                real_demand_delayed_1yr()
                * (1 + desired_annual_total_demand_growth_rate_delayed_1_yr())
            )
            / total_demand(),
        )
        * nvs_1_year()
    )


@component.add(
    name="historic change in inventories",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_change_in_inventories",
        "__lookup__": "_ext_lookup_historic_change_in_inventories",
    },
)
def historic_change_in_inventories(x, final_subs=None):
    """
    Historical change in inventories (14 sectors).
    """
    return _ext_lookup_historic_change_in_inventories(x, final_subs)


_ext_lookup_historic_change_in_inventories = ExtLookup(
    r"../economy.xlsx",
    "Catalonia",
    "time_index2009",
    "historic_change_in_inventories",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_change_in_inventories",
)


@component.add(
    name="historic demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 6,
        "historic_gfcf": 1,
        "historic_hd": 1,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
        "historic_exports_demand": 1,
        "historic_exports_demand_1": 1,
    },
)
def historic_demand():
    """
    Historic demand (35 WIOD sectors). US$1995
    """
    return (
        historic_gfcf(time())
        + historic_hd(time())
        + historic_goverment_expenditures(time())
        + historic_change_in_inventories(time())
        + historic_exports_demand(time())
        + historic_exports_demand_1(time())
    )


@component.add(
    name="historic demand next year",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 6,
        "historic_gfcf": 1,
        "historic_hd": 1,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
        "historic_exports_demand": 1,
        "historic_exports_demand_1": 1,
    },
)
def historic_demand_next_year():
    return (
        historic_gfcf(time() + 1)
        + historic_hd(time() + 1)
        + historic_goverment_expenditures(time() + 1)
        + historic_change_in_inventories(time() + 1)
        + historic_exports_demand(time() + 1)
        + historic_exports_demand_1(time() + 1)
    )


@component.add(
    name="historic goverment expenditures",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_goverment_expenditures",
        "__lookup__": "_ext_lookup_historic_goverment_expenditures",
    },
)
def historic_goverment_expenditures(x, final_subs=None):
    """
    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_goverment_expenditures(x, final_subs)


_ext_lookup_historic_goverment_expenditures = ExtLookup(
    r"../economy.xlsx",
    "Catalonia",
    "time_index2009",
    "historic_goverment_expenditures",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_goverment_expenditures",
)


@component.add(
    name="historic variation demand",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_demand_next_year": 1, "historic_demand": 1, "nvs_1_year": 1},
)
def historic_variation_demand():
    """
    Historic variation of demand (35 WIOD sectors). US$1995
    """
    return (historic_demand_next_year() - historic_demand()) / nvs_1_year()


@component.add(
    name="initial demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_demand": 1},
    other_deps={
        "_initial_initial_demand": {"initial": {"historic_demand": 1}, "step": {}}
    },
)
def initial_demand():
    return _initial_initial_demand()


_initial_initial_demand = Initial(lambda: historic_demand(), "_initial_initial_demand")


@component.add(
    name="Real Exports demand to RoEU by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_by_sector_cat": 1,
        "share_consum_goverment_and_inventories": 1,
        "share_exp_roeu_vs_gfcfhdexp": 1,
    },
)
def real_exports_demand_to_roeu_by_sector():
    return (
        real_final_demand_by_sector_cat()
        * (1 - share_consum_goverment_and_inventories())
        * share_exp_roeu_vs_gfcfhdexp()
    )


@component.add(
    name="Real Exports demand to RoW by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_by_sector_cat": 1,
        "share_consum_goverment_and_inventories": 1,
        "share_exp_row_vs_gfcfhdexp": 1,
    },
)
def real_exports_demand_to_row_by_sector():
    """
    Real exports after energy feedback.
    """
    return (
        real_final_demand_by_sector_cat()
        * (1 - share_consum_goverment_and_inventories())
        * share_exp_row_vs_gfcfhdexp()
    )


@component.add(
    name="Real GFCF by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_by_sector_cat": 1,
        "share_consum_goverment_and_inventories": 1,
        "share_gfcf_vs_gfcfhdexp": 1,
    },
)
def real_gfcf_by_sector():
    """
    Real Gross Fixed Capital Formation after energy feedback
    """
    return (
        real_final_demand_by_sector_cat()
        * (1 - share_consum_goverment_and_inventories())
        * share_gfcf_vs_gfcfhdexp()
    )


@component.add(
    name="Real Household demand by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_demand_by_sector_cat": 1,
        "share_consum_goverment_and_inventories": 1,
        "share_exp_row_vs_gfcfhdexp": 1,
        "share_exp_roeu_vs_gfcfhdexp": 1,
        "share_gfcf_vs_gfcfhdexp": 1,
    },
)
def real_household_demand_by_sector():
    """
    Real Households demand after energy feedback.
    """
    return (
        real_final_demand_by_sector_cat()
        * (1 - share_consum_goverment_and_inventories())
        * (
            1
            - share_gfcf_vs_gfcfhdexp()
            - share_exp_row_vs_gfcfhdexp()
            - share_exp_roeu_vs_gfcfhdexp()
        )
    )


@component.add(
    name="share consum goverment and inventories",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
        "historic_demand": 1,
    },
)
def share_consum_goverment_and_inventories():
    """
    Government expenditure share in total sectoral final demand and changes in inventories share in total sectoral final demand.
    """
    return (
        historic_goverment_expenditures(time()) + historic_change_in_inventories(time())
    ) / historic_demand()


@component.add(
    name='"share Exp RoEU vs GFCF+HD+Exp"',
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exports_demand_to_roeu": 2,
        "gross_fixed_capital_formation": 1,
        "household_demand": 1,
        "exports_demand_to_row": 1,
    },
)
def share_exp_roeu_vs_gfcfhdexp():
    return exports_demand_to_roeu() / (
        gross_fixed_capital_formation()
        + household_demand()
        + exports_demand_to_row()
        + exports_demand_to_roeu()
    )


@component.add(
    name='"share Exp RoW vs GFCF+HD+Exp"',
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exports_demand_to_row": 2,
        "gross_fixed_capital_formation": 1,
        "exports_demand_to_roeu": 1,
        "household_demand": 1,
    },
)
def share_exp_row_vs_gfcfhdexp():
    """
    Ratio 'Exports/GFCF+Exports+Households demand'.
    """
    return exports_demand_to_row() / (
        gross_fixed_capital_formation()
        + household_demand()
        + exports_demand_to_row()
        + exports_demand_to_roeu()
    )


@component.add(
    name='"share GFCF vs GFCF+HD+Exp"',
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_fixed_capital_formation": 2,
        "household_demand": 1,
        "exports_demand_to_roeu": 1,
        "exports_demand_to_row": 1,
    },
)
def share_gfcf_vs_gfcfhdexp():
    """
    Ratio 'GFCF/GFCF+Exports+Households demand'.
    """
    return gross_fixed_capital_formation() / (
        gross_fixed_capital_formation()
        + household_demand()
        + exports_demand_to_row()
        + exports_demand_to_roeu()
    )


@component.add(
    name="total demand",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_cat": 1, "m_to_t": 1},
)
def total_demand():
    """
    Total final demand
    """
    return (
        sum(demand_by_sector_fd_cat().rename({"sectors": "sectors!"}), dim=["sectors!"])
        * m_to_t()
    )


@component.add(
    name="total demand adjusted",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1, "m_to_t": 1},
)
def total_demand_adjusted():
    """
    Total demand after adjustment of the demand function.
    """
    return (
        sum(
            demand_by_sector_fd_adjusted().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        * m_to_t()
    )


@component.add(
    name="variation demand flow FD CAT",
    units="M$/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_variation_demand": 1,
        "variation_household_demand": 1,
        "variation_exports_demand_to_row": 1,
        "variation_exports_demand_to_roeu": 1,
        "share_consum_goverment_and_inventories": 1,
        "variation_gfcf": 1,
    },
)
def variation_demand_flow_fd_cat():
    """
    variation of final demand by EU28 industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: historic_variation_demand(),
        lambda: (
            variation_gfcf()
            + variation_household_demand()
            + variation_exports_demand_to_row()
            + variation_exports_demand_to_roeu()
        )
        / (1 - share_consum_goverment_and_inventories()),
    )
