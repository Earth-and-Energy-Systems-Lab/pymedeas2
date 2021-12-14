"""
Module economic_demand_function_demand_de
Translated using PySD version 2.1.0
"""


@subs(["sectors"], _subscript_dict)
def demand_by_sector_fd_adjusted():
    """
    Real Name: demand by sector FD adjusted
    Original Eqn: Demand by sector FD EU[sectors]*diff demand EU
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Demand by sector after adjustment to match the desired GDP level.
    """
    return demand_by_sector_fd_eu() * diff_demand_eu()


@subs(["sectors"], _subscript_dict)
def demand_by_sector_fd_eu():
    """
    Real Name: Demand by sector FD EU
    Original Eqn: INTEG ( variation demand flow FD EU[sectors]-demand not covered by sector FD EU[ sectors], initial demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Final demand by EU28 35 industrial sectors
    """
    return _integ_demand_by_sector_fd_eu()


@subs(["sectors"], _subscript_dict)
def demand_not_covered_by_sector_fd_eu():
    """
    Real Name: demand not covered by sector FD EU
    Original Eqn: IF THEN ELSE(Time<2009,0,Demand by sector FD EU[sectors]-Real final demand by sector EU[sectors])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between final demand required and real final demand (after
        energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: demand_by_sector_fd_eu() - real_final_demand_by_sector_eu(),
    )


def demand_not_covered_total_fd():
    """
    Real Name: demand not covered total FD
    Original Eqn: SUM(demand not covered by sector FD EU[sectors!])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(demand_not_covered_by_sector_fd_eu(), dim=("sectors",))


def diff_demand_eu():
    """
    Real Name: diff demand EU
    Original Eqn: IF THEN ELSE(Time<2009, 1, (Real demand delayed 1yr*(1+Desired annual total demand growth rate delayed 1 yr ))/total demand)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio between the desired GDP and the real GDP level after applying the
        demand function.
    """
    return if_then_else(
        time() < 2009,
        lambda: 1,
        lambda: (
            real_demand_delayed_1yr()
            * (1 + desired_annual_total_demand_growth_rate_delayed_1_yr())
        )
        / total_demand(),
    )


def historic_change_in_inventories(x):
    """
    Real Name: historic change in inventories
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_change_in_inventories')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical change in inventories (14 sectors).
    """
    return _ext_lookup_historic_change_in_inventories(x)


@subs(["sectors"], _subscript_dict)
def historic_demand():
    """
    Real Name: historic demand
    Original Eqn: historic GFCF[sectors](Time)+historic HD[sectors](Time)+historic goverment expenditures[sectors](Time)+historic change in inventories [sectors](Time)+historic exports demand[sectors](Time)
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic demand (14 sectors). US$1995.
    """
    return (
        historic_gfcf(time())
        + historic_hd(time())
        + historic_goverment_expenditures(time())
        + historic_change_in_inventories(time())
        + historic_exports_demand(time())
    )


@subs(["sectors"], _subscript_dict)
def historic_demand_next_year():
    """
    Real Name: historic demand next year
    Original Eqn: historic GFCF[sectors](Time+1)+historic HD[sectors](Time+1)+historic goverment expenditures[sectors](Time+1)+historic change in inventories [sectors](Time+1)+historic exports demand[sectors](Time+1)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic demand (14 sectors). US$1995.
    """
    return (
        historic_gfcf(time() + 1)
        + historic_hd(time() + 1)
        + historic_goverment_expenditures(time() + 1)
        + historic_change_in_inventories(time() + 1)
        + historic_exports_demand(time() + 1)
    )


def historic_goverment_expenditures(x):
    """
    Real Name: historic goverment expenditures
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_goverment_expenditures')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_goverment_expenditures(x)


@subs(["sectors"], _subscript_dict)
def historic_variation_demand():
    """
    Real Name: historic variation demand
    Original Eqn: historic demand next year[sectors]-historic demand[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of demand (14 sectors). US$1995
    """
    return historic_demand_next_year() - historic_demand()


@subs(["sectors"], _subscript_dict)
def initial_demand():
    """
    Real Name: initial demand
    Original Eqn: INITIAL(historic demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return _initial_initial_demand()


@subs(["sectors"], _subscript_dict)
def real_exports_demand_by_sector():
    """
    Real Name: Real Exports demand by sector
    Original Eqn: Real final demand by sector EU[sectors]*(1-share consum goverment and inventories[sectors])*"share Exp vs GFCF+HD+Exp" [sectors]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real exports after energy feedback.
    """
    return (
        real_final_demand_by_sector_eu()
        * (1 - share_consum_goverment_and_inventories())
        * share_exp_vs_gfcfhdexp()
    )


@subs(["sectors"], _subscript_dict)
def real_gfcf_by_sector():
    """
    Real Name: Real GFCF by sector
    Original Eqn: Real final demand by sector EU[sectors]*(1-share consum goverment and inventories[sectors])*"share GFCF vs GFCF+HD+Exp" [sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real Gross Fixed Capital Formation after energy feedback
    """
    return (
        real_final_demand_by_sector_eu()
        * (1 - share_consum_goverment_and_inventories())
        * share_gfcf_vs_gfcfhdexp()
    )


@subs(["sectors"], _subscript_dict)
def real_household_demand_by_sector():
    """
    Real Name: Real Household demand by sector
    Original Eqn: Real final demand by sector EU[sectors]*(1-share consum goverment and inventories[sectors])*(1-"share GFCF vs GFCF+HD+Exp" [sectors]-"share Exp vs GFCF+HD+Exp"[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real Households demand after energy feedback.
    """
    return (
        real_final_demand_by_sector_eu()
        * (1 - share_consum_goverment_and_inventories())
        * (1 - share_gfcf_vs_gfcfhdexp() - share_exp_vs_gfcfhdexp())
    )


@subs(["sectors"], _subscript_dict)
def share_consum_goverment_and_inventories():
    """
    Real Name: share consum goverment and inventories
    Original Eqn: (historic goverment expenditures[sectors](Time)+historic change in inventories[sectors](Time))/historic demand[sectors]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Government expenditure share in total sectoral final demand and changes in
        inventories share in total sectoral final demand.
    """
    return (
        historic_goverment_expenditures(time()) + historic_change_in_inventories(time())
    ) / historic_demand()


@subs(["sectors"], _subscript_dict)
def share_consum_goverments_and_inventories_next_year():
    """
    Real Name: share consum goverments and inventories next year
    Original Eqn: (historic goverment expenditures[sectors](Time+1)+historic change in inventories[sectors](Time+1))/historic demand next year [sectors]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sum of share of Public expenditures and changes in inventories.
    """
    return (
        historic_goverment_expenditures(time() + 1)
        + historic_change_in_inventories(time() + 1)
    ) / historic_demand_next_year()


@subs(["sectors"], _subscript_dict)
def share_exp_vs_gfcfhdexp():
    """
    Real Name: "share Exp vs GFCF+HD+Exp"
    Original Eqn: Exports demand[sectors]/(Gross fixed capital formation[sectors]+Household demand[ sectors]+Exports demand[sectors])
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Ratio 'Exports/GFCF+Exports+Households demand'.
    """
    return exports_demand() / (
        gross_fixed_capital_formation() + household_demand() + exports_demand()
    )


@subs(["sectors"], _subscript_dict)
def share_gfcf_vs_gfcfhdexp():
    """
    Real Name: "share GFCF vs GFCF+HD+Exp"
    Original Eqn: Gross fixed capital formation[sectors]/(Gross fixed capital formation[ sectors]+Household demand[ sectors]+Exports demand[sectors])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Ratio 'GFCF/GFCF+Exports+Households demand'.
    """
    return gross_fixed_capital_formation() / (
        gross_fixed_capital_formation() + household_demand() + exports_demand()
    )


def sum_variation():
    """
    Real Name: sum variation
    Original Eqn: SUM(variation demand flow FD EU[sectors!])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of total final demand
    """
    return sum(variation_demand_flow_fd_eu(), dim=("sectors",))


def total_demand():
    """
    Real Name: total demand
    Original Eqn: SUM(Demand by sector FD EU[sectors!])/1e+06
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total final demand
    """
    return sum(demand_by_sector_fd_eu(), dim=("sectors",)) / 1e06


def total_demand_adjusted():
    """
    Real Name: total demand adjusted
    Original Eqn: SUM(demand by sector FD adjusted[sectors!])/1e+06
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total demand after adjustment of the demand function.
    """
    return sum(demand_by_sector_fd_adjusted(), dim=("sectors",)) / 1e06


@subs(["sectors"], _subscript_dict)
def variation_demand_flow_fd_eu():
    """
    Real Name: variation demand flow FD EU
    Original Eqn: IF THEN ELSE(Time<2009,historic variation demand[sectors],(Gross fixed capital formation[sectors]* (1-((1-share consum goverments and inventories next year[sectors])/(1-share consum goverment and inventories[sectors])) )+Exports demand[sectors]* (1-((1-share consum goverments and inventories next year[sectors])/(1-share consum goverment and inventories[sectors])) ) +Household demand[sectors]*(1-((1-share consum goverments and inventories next year[sectors])/(1-share consum goverment and inventories [sectors])))+variation GFCF[sectors]+variation household demand[sectors]+variation exports demand[ sectors])/(1-share consum goverments and inventories next year [sectors]))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    variation of final demand by EU28 industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: historic_variation_demand(),
        lambda: (
            gross_fixed_capital_formation()
            * (
                1
                - (
                    (1 - share_consum_goverments_and_inventories_next_year())
                    / (1 - share_consum_goverment_and_inventories())
                )
            )
            + exports_demand()
            * (
                1
                - (
                    (1 - share_consum_goverments_and_inventories_next_year())
                    / (1 - share_consum_goverment_and_inventories())
                )
            )
            + household_demand()
            * (
                1
                - (
                    (1 - share_consum_goverments_and_inventories_next_year())
                    / (1 - share_consum_goverment_and_inventories())
                )
            )
            + variation_gfcf()
            + variation_household_demand()
            + variation_exports_demand()
        )
        / (1 - share_consum_goverments_and_inventories_next_year()),
    )


@subs(["sectors"], _subscript_dict)
def _integ_init_demand_by_sector_fd_eu():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for demand_by_sector_fd_eu
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for demand_by_sector_fd_eu function
    """
    return initial_demand()


@subs(["sectors"], _subscript_dict)
def _integ_input_demand_by_sector_fd_eu():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for demand_by_sector_fd_eu
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for demand_by_sector_fd_eu function
    """
    return variation_demand_flow_fd_eu() - demand_not_covered_by_sector_fd_eu()


_integ_demand_by_sector_fd_eu = Integ(
    _integ_input_demand_by_sector_fd_eu,
    _integ_init_demand_by_sector_fd_eu,
    "_integ_demand_by_sector_fd_eu",
)


_ext_lookup_historic_change_in_inventories = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_change_in_inventories",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_change_in_inventories",
)


_ext_lookup_historic_goverment_expenditures = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_goverment_expenditures",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_goverment_expenditures",
)


_initial_initial_demand = Initial(lambda: historic_demand(), "_initial_initial_demand")
