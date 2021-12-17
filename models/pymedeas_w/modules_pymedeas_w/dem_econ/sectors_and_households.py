"""
Module sectors_and_households
Translated using PySD version 2.2.0
"""


def annual_gdppc_growth_rate():
    """
    Real Name: Annual GDPpc growth rate
    Original Eqn: IF THEN ELSE(select GDPpc evolution input=0, input GDPpc annual growth, IF THEN ELSE(select GDPpc evolution input=1, P timeseries GDPpc growth rate, IF THEN ELSE (Time<P customized year GDPpc evolution, P timeseries GDPpc growth rate, P customized cte GDPpc variation )))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        select_gdppc_evolution_input() == 0,
        lambda: input_gdppc_annual_growth(),
        lambda: if_then_else(
            select_gdppc_evolution_input() == 1,
            lambda: p_timeseries_gdppc_growth_rate(),
            lambda: if_then_else(
                time() < p_customized_year_gdppc_evolution(),
                lambda: p_timeseries_gdppc_growth_rate(),
                lambda: p_customized_cte_gdppc_variation(),
            ),
        ),
    )


@subs(["sectors"], _subscript_dict)
def beta_0_gfcf():
    """
    Real Name: beta 0 GFCF
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'beta_0_GFCF*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_0_gfcf()


@subs(["sectors"], _subscript_dict)
def beta_0_hd():
    """
    Real Name: beta 0 HD
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'beta_0_HD*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_0_hd()


def beta_1_gfcf():
    """
    Real Name: beta 1 GFCF
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'beta_1_GFCF')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_1_gfcf()


def beta_1_hd():
    """
    Real Name: beta 1 HD
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'World', 'beta_1_HD')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_1_hd()


def capital_share():
    """
    Real Name: capital share
    Original Eqn: 1-labour share
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Capital share.
    """
    return 1 - labour_share()


@subs(["sectors"], _subscript_dict)
def cc_sectoral():
    """
    Real Name: CC sectoral
    Original Eqn: CC total*share CC[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Capital compensation by industrial sectors
    """
    return cc_total() * share_cc()


def cc_total():
    """
    Real Name: CC total
    Original Eqn: INTEG (variation CC-CC total not covered, initial CC total)
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Capital compensation
    """
    return _integ_cc_total()


def cc_total_not_covered():
    """
    Real Name: CC total not covered
    Original Eqn: demand not covered total FD*capital share
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Gap between capital compensation required and real capital compensation
        (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * capital_share()


@subs(["sectors"], _subscript_dict)
def demand_by_sector_fd():
    """
    Real Name: Demand by sector FD
    Original Eqn: INTEG ( variation demand flow FD[sectors]-demand not covered by sector FD[ sectors], initial demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Final demand by 35 industrial sectors
    """
    return _integ_demand_by_sector_fd()


@subs(["sectors"], _subscript_dict)
def demand_by_sector_fd_adjusted():
    """
    Real Name: demand by sector FD adjusted
    Original Eqn: Demand by sector FD[sectors]*diff demand
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Demand by sector after adjustment to match the desired GDP level.
    """
    return demand_by_sector_fd() * diff_demand()


@subs(["sectors"], _subscript_dict)
def demand_not_covered_by_sector_fd():
    """
    Real Name: demand not covered by sector FD
    Original Eqn: IF THEN ELSE(Time>2009,Demand by sector FD[sectors]-Real demand by sector[ sectors],0)
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return if_then_else(
        time() > 2009,
        lambda: demand_by_sector_fd() - real_demand_by_sector(),
        lambda: 0,
    )


def demand_not_covered_total_fd():
    """
    Real Name: demand not covered total FD
    Original Eqn: SUM(demand not covered by sector FD[sectors!])
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(demand_not_covered_by_sector_fd(), dim=("sectors",))


def desired_annual_gdp_growth_rate():
    """
    Real Name: Desired annual GDP growth rate
    Original Eqn: -1+(Desired GDP/Desired GDP delayed 1yr)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Desired annual GDP growth rate.
    """
    return -1 + (desired_gdp() / desired_gdp_delayed_1yr())


def desired_gdp():
    """
    Real Name: Desired GDP
    Original Eqn: IF THEN ELSE(Time<2009, total demand,Desired GDPpc*Population /dollars to Tdollars-0.56)
    Units: T$
    Limits: (None, None)
    Type: component
    Subs: None

    Desired GDP level for each scenario (user selection). The factor "0.56"
        corrects for a discrepancy when the TIME STEP < frequency of historical
        data.
    """
    return if_then_else(
        time() < 2009,
        lambda: total_demand(),
        lambda: desired_gdppc() * population() / dollars_to_tdollars() - 0.56,
    )


def desired_gdp_delayed_1yr():
    """
    Real Name: Desired GDP delayed 1yr
    Original Eqn: DELAY FIXED ( Desired GDP, 1, 29.16)
    Units: T$/year
    Limits: (None, None)
    Type: component
    Subs: None

    Desired GDP delayed 1 year.
    """
    return _delayfixed_desired_gdp_delayed_1yr()


def desired_gdppc():
    """
    Real Name: Desired GDPpc
    Original Eqn: INTEG ( Desired variation GDPpc, GDPpc initial year)
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_desired_gdppc()


def desired_variation_gdppc():
    """
    Real Name: Desired variation GDPpc
    Original Eqn: IF THEN ELSE(Time<2013, variation historic GDPpc, Desired GDPpc*Annual GDPpc growth rate)
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2013,
        lambda: variation_historic_gdppc(),
        lambda: desired_gdppc() * annual_gdppc_growth_rate(),
    )


def diff_demand():
    """
    Real Name: diff demand
    Original Eqn: IF THEN ELSE(Time<2009, 1, (GDP delayed 1yr*(1+Desired annual GDP growth rate ))/total demand)
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
        lambda: (gdp_delayed_1yr() * (1 + desired_annual_gdp_growth_rate()))
        / total_demand(),
    )


def dollar_per_mdollar():
    """
    Real Name: dollar per Mdollar
    Original Eqn: 1e+06
    Units: dollar/Mdollar
    Limits: (None, None)
    Type: constant
    Subs: None

    Dollars per million dollar (1 M$ = 1e6 $).
    """
    return 1e06


def gdppc_initial_year():
    """
    Real Name: GDPpc initial year
    Original Eqn: historic GDP(1995)/historic population(1995)*dollar per Mdollar
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


@subs(["sectors"], _subscript_dict)
def gfcf_not_covered():
    """
    Real Name: GFCF not covered
    Original Eqn: IF THEN ELSE(Time<2009,0,Gross fixed capital formation[sectors]-Real GFCF[ sectors])
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between gross fixed capital formation required and real gross fixed
        capital formation (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009, lambda: 0, lambda: gross_fixed_capital_formation() - real_gfcf()
    )


@subs(["sectors"], _subscript_dict)
def gross_fixed_capital_formation():
    """
    Real Name: Gross fixed capital formation
    Original Eqn: INTEG ( variation GFCF[sectors]-GFCF not covered[sectors], initial GFCF[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Value of gross fixed capital formation
    """
    return _integ_gross_fixed_capital_formation()


def growth_capital_share():
    """
    Real Name: growth capital share
    Original Eqn: -growth labour share*labour share/(1-labour share)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic capital share variation (own calculations from WIOD-SEA).
    """
    return -growth_labour_share() * labour_share() / (1 - labour_share())


def growth_labour_share():
    """
    Real Name: growth labour share
    Original Eqn: IF THEN ELSE(Time>2013,IF THEN ELSE(Time>2050,0,Labour share growth*"Labor share cte?"),historic labour share variation)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation rate of labour share depending on activation.
    """
    return if_then_else(
        time() > 2013,
        lambda: if_then_else(
            time() > 2050, lambda: 0, lambda: labour_share_growth() * labor_share_cte()
        ),
        lambda: historic_labour_share_variation(),
    )


def historic_capital_compensation(x):
    """
    Real Name: historic capital compensation
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2014', 'historic_capital_compensation')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_capital_compensation(x)


def historic_change_in_inventories(x):
    """
    Real Name: historic change in inventories
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2009', 'historic_change_in_inventories')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_change_in_inventories(x)


@subs(["sectors"], _subscript_dict)
def historic_demand():
    """
    Real Name: historic demand
    Original Eqn: historic GFCF[sectors](Time)+historic HD[sectors](Time)+historic goverment expenditures[sectors](Time)+historic change in inventories[sectors](Time)
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic demand (35 WIOD sectors). US$1995.
    """
    return (
        historic_gfcf(time())
        + historic_hd(time())
        + historic_goverment_expenditures(time())
        + historic_change_in_inventories(time())
    )


@subs(["sectors"], _subscript_dict)
def historic_demand_next_year():
    """
    Real Name: historic demand next year
    Original Eqn: historic GFCF[sectors](Time+1)+historic HD[sectors](Time+1)+historic goverment expenditures[sectors](Time+1)+historic change in inventories[sectors](Time+1)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return (
        historic_gfcf(time() + 1)
        + historic_hd(time() + 1)
        + historic_goverment_expenditures(time() + 1)
        + historic_change_in_inventories(time() + 1)
    )


def historic_gdp(x):
    """
    Real Name: historic GDP
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2014', 'historic_GDP')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic GDP Million dollars. Data derived from A matrix. US$1995.
    """
    return _ext_lookup_historic_gdp(x)


def historic_gfcf(x):
    """
    Real Name: historic GFCF
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2009', 'historic_GFCF')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historic gross fixed capital formation (WIOD-14 sectors).
    """
    return _ext_lookup_historic_gfcf(x)


def historic_goverment_expenditures(x):
    """
    Real Name: historic goverment expenditures
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2009', 'historic_goverment_expenditures')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_goverment_expenditures(x)


def historic_hd(x):
    """
    Real Name: historic HD
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2009', 'historic_HD')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical final demand by households (WIOD-14 sectors).
    """
    return _ext_lookup_historic_hd(x)


def historic_labour_compensation(x):
    """
    Real Name: historic labour compensation
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'World', 'time_index2014', 'historic_labour_compensation')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical labour compensation (14 sectors).
    """
    return _ext_lookup_historic_labour_compensation(x)


def historic_labour_share_variation():
    """
    Real Name: historic labour share variation
    Original Eqn: (labour compensation share next step-labour compensation share)/labour compensation share
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of labour share (own calculations from WIOD-SEA).
    """
    return (
        labour_compensation_share_next_step() - labour_compensation_share()
    ) / labour_compensation_share()


@subs(["sectors"], _subscript_dict)
def historic_variation_demand():
    """
    Real Name: historic variation demand
    Original Eqn: historic demand next year[sectors]-historic demand[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of demand (35 WIOD sectors). US$1995
    """
    return historic_demand_next_year() - historic_demand()


@subs(["sectors"], _subscript_dict)
def household_demand():
    """
    Real Name: Household demand
    Original Eqn: INTEG (variation household demand[sectors]-Household demand not covered[sectors], initial household demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Finald demand by Households
    """
    return _integ_household_demand()


@subs(["sectors"], _subscript_dict)
def household_demand_not_covered():
    """
    Real Name: Household demand not covered
    Original Eqn: IF THEN ELSE(Time<2009,0,Household demand[sectors]-Real Household demand[ sectors])
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between households consumption required and households real
        consumption (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009, lambda: 0, lambda: household_demand() - real_household_demand()
    )


def household_demand_total():
    """
    Real Name: Household demand total
    Original Eqn: SUM(Household demand[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Economic households demand (in millionUS$1995)
    """
    return sum(household_demand(), dim=("sectors",))


def initial_cc_total():
    """
    Real Name: initial CC total
    Original Eqn: 1.05739e+07
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1.05739e07


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
def initial_gfcf():
    """
    Real Name: initial GFCF
    Original Eqn: historic GFCF[sectors](1995)
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial gross fixed capital formation
    """
    return historic_gfcf(1995)


@subs(["sectors"], _subscript_dict)
def initial_household_demand():
    """
    Real Name: initial household demand
    Original Eqn: historic HD[sectors](1995)
    Units:
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial final demand by households
    """
    return historic_hd(1995)


def initial_labour_share():
    """
    Real Name: Initial Labour share
    Original Eqn: 0.5621
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Historic 2014 Labour share
    """
    return 0.5621


def initial_lc_total():
    """
    Real Name: initial LC total
    Original Eqn: 1.85847e+07
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial labour compensation
    """
    return 1.85847e07


def input_gdppc_annual_growth():
    """
    Real Name: input GDPpc annual growth
    Original Eqn: GET DIRECT DATA('../economy.xlsx', 'World', 'time_index_projection', 'input_GDPpc_annual_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Original values for annual growth of GDPpc from SSP2.
    """
    return _ext_data_input_gdppc_annual_growth(time())


def labor_share_cte():
    """
    Real Name: "Labor share cte?"
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0: Labor share: cte        1: Labor share evolves following "P labor share"
    """
    return 1


def labour_compensation_share():
    """
    Real Name: labour compensation share
    Original Eqn: SUM(historic labour compensation[sectors!](Time))/SUM(historic labour compensation[sectors!](Time)+historic capital compensation[sectors!](Time))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(historic_labour_compensation(time()), dim=("sectors",)) / sum(
        historic_labour_compensation(time()) + historic_capital_compensation(time()),
        dim=("sectors",),
    )


def labour_compensation_share_next_step():
    """
    Real Name: labour compensation share next step
    Original Eqn: SUM(historic labour compensation[sectors!](Time+1))/SUM(historic labour compensation[sectors!](Time+1)+historic capital compensation[sectors!](Time+1))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(historic_labour_compensation(time() + 1), dim=("sectors",)) / sum(
        historic_labour_compensation(time() + 1)
        + historic_capital_compensation(time() + 1),
        dim=("sectors",),
    )


def labour_share():
    """
    Real Name: labour share
    Original Eqn: INTEG ( variation labour share, 0.6374)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_labour_share()


def labour_share_growth():
    """
    Real Name: Labour share growth
    Original Eqn: ((P labour share 2050/Initial Labour share)^(1/(Year Final Labour share-Year Initial Labour share)))-1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Mean cummulative growth rate of labour share.
    """
    return (
        (p_labour_share_2050() / initial_labour_share())
        ** (1 / (year_final_labour_share() - year_initial_labour_share()))
    ) - 1


def lc():
    """
    Real Name: LC
    Original Eqn: INTEG (variation LC-LC not covered, initial LC total)
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Labour compensation
    """
    return _integ_lc()


def lc_not_covered():
    """
    Real Name: LC not covered
    Original Eqn: demand not covered total FD*labour share
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Gap between labour compensation required andreal labour compensation
        (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * labour_share()


def p_customized_cte_gdppc_variation():
    """
    Real Name: P customized cte GDPpc variation
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'G7')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_gdppc_variation()


def p_customized_year_gdppc_evolution():
    """
    Real Name: P customized year GDPpc evolution
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'E7')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_gdppc_evolution()


def p_labour_share_2050():
    """
    Real Name: P labour share 2050
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'C3')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share_2050()


def p_timeseries_gdppc_growth_rate():
    """
    Real Name: P timeseries GDPpc growth rate
    Original Eqn: GET DIRECT DATA('../../scenarios/scen_w.xlsx', 'BAU', '5', 'E6')
    Units: 1/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Annual GDPpc growth from timeseries.
    """
    return _ext_data_p_timeseries_gdppc_growth_rate(time())


@subs(["sectors"], _subscript_dict)
def pct_gfcf_vs_gfcfhd():
    """
    Real Name: "pct GFCF vs GFCF+HD"
    Original Eqn: Gross fixed capital formation[sectors]/(Gross fixed capital formation[ sectors]+Household demand[sectors])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Share of Gross Fixed Capital Formation in final demand by households and
        enterprises.
    """
    return gross_fixed_capital_formation() / (
        gross_fixed_capital_formation() + household_demand()
    )


@subs(["sectors"], _subscript_dict)
def real_gfcf():
    """
    Real Name: Real GFCF
    Original Eqn: Real demand by sector[sectors]*(1-share consum goverment and inventories[sectors])*"pct GFCF vs GFCF+HD"[sectors]
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Real Gross Fixed Capital Formation
    """
    return (
        real_demand_by_sector()
        * (1 - share_consum_goverment_and_inventories())
        * pct_gfcf_vs_gfcfhd()
    )


@subs(["sectors"], _subscript_dict)
def real_household_demand():
    """
    Real Name: Real Household demand
    Original Eqn: Real demand by sector[sectors]*(1-share consum goverment and inventories[sectors])*(1-"pct GFCF vs GFCF+HD"[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return (
        real_demand_by_sector()
        * (1 - share_consum_goverment_and_inventories())
        * (1 - pct_gfcf_vs_gfcfhd())
    )


def select_gdppc_evolution_input():
    """
    Real Name: select GDPpc evolution input
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'B4')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0. SSP2        1. Timeseries        2. From customized year, set annual constant variation
    """
    return _ext_constant_select_gdppc_evolution_input()


@subs(["sectors"], _subscript_dict)
def share_cc():
    """
    Real Name: share CC
    Original Eqn: historic capital compensation[sectors](Time)/SUM(historic capital compensation[sectors!](Time))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectoral share of capital compensation. (Capital compensation[i]/Total
        capital compensation)
    """
    return historic_capital_compensation(time()) / sum(
        historic_capital_compensation(time()), dim=("sectors",)
    )


@subs(["sectors"], _subscript_dict)
def share_cc_next_step():
    """
    Real Name: share CC next step
    Original Eqn: historic capital compensation[sectors](Time+1)/SUM(historic capital compensation[sectors!](Time+1))
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return historic_capital_compensation(time() + 1) / sum(
        historic_capital_compensation(time() + 1), dim=("sectors",)
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


    """
    return (
        historic_goverment_expenditures(time()) + historic_change_in_inventories(time())
    ) / historic_demand()


@subs(["sectors"], _subscript_dict)
def share_consum_goverments_and_inventories_next_year():
    """
    Real Name: share consum goverments and inventories next year
    Original Eqn: (historic goverment expenditures[sectors](Time+1)+historic change in inventories[sectors](Time+1))/historic demand next year[sectors]
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


def sum_variation():
    """
    Real Name: sum variation
    Original Eqn: SUM(variation demand flow FD[sectors!])
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of total final demand
    """
    return sum(variation_demand_flow_fd(), dim=("sectors",))


def total_demand():
    """
    Real Name: total demand
    Original Eqn: SUM(Demand by sector FD[sectors!])/1e+06
    Units: Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total final demand
    """
    return sum(demand_by_sector_fd(), dim=("sectors",)) / 1e06


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


def variation_cc():
    """
    Real Name: variation CC
    Original Eqn: capital share*(Desired annual GDP growth rate+growth capital share+Desired annual GDP growth rate*growth capital share )*Real demand
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of capital compensation
    """
    return (
        capital_share()
        * (
            desired_annual_gdp_growth_rate()
            + growth_capital_share()
            + desired_annual_gdp_growth_rate() * growth_capital_share()
        )
        * real_demand()
    )


@subs(["sectors"], _subscript_dict)
def variation_cc_sectoral():
    """
    Real Name: variation CC sectoral
    Original Eqn: (CC total+variation CC)*share CC next step[sectors]-CC total*share CC[sectors]
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of capital compensation by industrial sectors
    """
    return (
        cc_total() + variation_cc()
    ) * share_cc_next_step() - cc_total() * share_cc()


@subs(["sectors"], _subscript_dict)
def variation_demand_flow_fd():
    """
    Real Name: variation demand flow FD
    Original Eqn: IF THEN ELSE(Time<2009,historic variation demand[sectors],(Gross fixed capital formation[sectors]* (1-((1-share consum goverments and inventories next year[sectors])/(1-share consum goverment and inventories[sectors]))) +Household demand[sectors]*(1-((1-share consum goverments and inventories next year[sectors])/(1-share consum goverment and inventories [sectors])))+variation GFCF[sectors]+variation household demand[sectors])/(1-share consum goverments and inventories next year [sectors]))
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    variation of final demand by industrial sectors
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
        )
        / (1 - share_consum_goverments_and_inventories_next_year()),
    )


@subs(["sectors"], _subscript_dict)
def variation_gfcf():
    """
    Real Name: variation GFCF
    Original Eqn: IF THEN ELSE(Time>2009, 0, IF THEN ELSE(Time<2009, variation historic GFCF[sectors],EXP(beta 0 GFCF[sectors])*((CC sectoral[sectors]+variation CC sectoral[sectors])^beta 1 GFCF-CC sectoral[sectors]^beta 1 GFCF)))
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of gross fixed capital formation by industrial sectors
    """
    return if_then_else(
        time() > 2009,
        lambda: 0,
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_gfcf(),
            lambda: np.exp(beta_0_gfcf())
            * (
                (cc_sectoral() + variation_cc_sectoral()) ** beta_1_gfcf()
                - cc_sectoral() ** beta_1_gfcf()
            ),
        ),
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_demand():
    """
    Real Name: variation historic demand
    Original Eqn: historic HD[sectors](Time+1)-historic HD[sectors](Time)
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of final demand by households
    """
    return historic_hd(time() + 1) - historic_hd(time())


def variation_historic_gdppc():
    """
    Real Name: variation historic GDPpc
    Original Eqn: IF THEN ELSE(Time<2013, (historic GDP(Time+1)/historic population(Time+1)-historic GDP(Time)/historic population(Time))*dollar per Mdollar, 0)
    Units: $/(person*year)
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of historic GDP per capita.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_gdp(time() + 1) / historic_population(time() + 1)
            - historic_gdp(time()) / historic_population(time())
        )
        * dollar_per_mdollar(),
        lambda: 0,
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_gfcf():
    """
    Real Name: variation historic GFCF
    Original Eqn: historic GFCF[sectors](Time+1)-historic GFCF[sectors](Time)
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of gross fixed capital formation (WIOD-35 sectors)
    """
    return historic_gfcf(time() + 1) - historic_gfcf(time())


@subs(["sectors"], _subscript_dict)
def variation_household_demand():
    """
    Real Name: variation household demand
    Original Eqn: IF THEN ELSE(Time<2009,variation historic demand[sectors],EXP(beta 0 HD[sectors])*((LC+variation LC)^beta 1 HD- LC^beta 1 HD))
    Units: Mdollars/year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of final demand by households by industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: variation_historic_demand(),
        lambda: np.exp(beta_0_hd())
        * ((lc() + variation_lc()) ** beta_1_hd() - lc() ** beta_1_hd()),
    )


def variation_labour_share():
    """
    Real Name: variation labour share
    Original Eqn: growth labour share*labour share
    Units: 1/year
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation of labor share.
    """
    return growth_labour_share() * labour_share()


def variation_lc():
    """
    Real Name: variation LC
    Original Eqn: Real demand*labour share*(Desired annual GDP growth rate +growth labour share +Desired annual GDP growth rate*growth labour share)
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Variation of labour compensation
    """
    return (
        real_demand()
        * labour_share()
        * (
            desired_annual_gdp_growth_rate()
            + growth_labour_share()
            + desired_annual_gdp_growth_rate() * growth_labour_share()
        )
    )


def year_final_labour_share():
    """
    Real Name: Year Final Labour share
    Original Eqn: 2050
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Year of final labour share by scenarios to use in the mean accumulative
        growth rate.
    """
    return 2050


def year_initial_labour_share():
    """
    Real Name: Year Initial Labour share
    Original Eqn: 2014
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2014


_ext_constant_beta_0_gfcf = ExtConstant(
    "../economy.xlsx",
    "World",
    "beta_0_GFCF*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_gfcf",
)


_ext_constant_beta_0_hd = ExtConstant(
    "../economy.xlsx",
    "World",
    "beta_0_HD*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_hd",
)


_ext_constant_beta_1_gfcf = ExtConstant(
    "../economy.xlsx", "World", "beta_1_GFCF", {}, _root, "_ext_constant_beta_1_gfcf"
)


_ext_constant_beta_1_hd = ExtConstant(
    "../economy.xlsx", "World", "beta_1_HD", {}, _root, "_ext_constant_beta_1_hd"
)


_integ_cc_total = Integ(
    lambda: variation_cc() - cc_total_not_covered(),
    lambda: initial_cc_total(),
    "_integ_cc_total",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_demand_by_sector_fd():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for demand_by_sector_fd
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for demand_by_sector_fd function
    """
    return initial_demand()


@subs(["sectors"], _subscript_dict)
def _integ_input_demand_by_sector_fd():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for demand_by_sector_fd
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for demand_by_sector_fd function
    """
    return variation_demand_flow_fd() - demand_not_covered_by_sector_fd()


_integ_demand_by_sector_fd = Integ(
    _integ_input_demand_by_sector_fd,
    _integ_init_demand_by_sector_fd,
    "_integ_demand_by_sector_fd",
)


_delayfixed_desired_gdp_delayed_1yr = DelayFixed(
    lambda: desired_gdp(),
    lambda: 1,
    lambda: 29.16,
    time_step,
    "_delayfixed_desired_gdp_delayed_1yr",
)


_integ_desired_gdppc = Integ(
    lambda: desired_variation_gdppc(),
    lambda: gdppc_initial_year(),
    "_integ_desired_gdppc",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_gross_fixed_capital_formation():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for gross_fixed_capital_formation
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for gross_fixed_capital_formation function
    """
    return initial_gfcf()


@subs(["sectors"], _subscript_dict)
def _integ_input_gross_fixed_capital_formation():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for gross_fixed_capital_formation
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for gross_fixed_capital_formation function
    """
    return variation_gfcf() - gfcf_not_covered()


_integ_gross_fixed_capital_formation = Integ(
    _integ_input_gross_fixed_capital_formation,
    _integ_init_gross_fixed_capital_formation,
    "_integ_gross_fixed_capital_formation",
)


_ext_lookup_historic_capital_compensation = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_capital_compensation",
)


_ext_lookup_historic_change_in_inventories = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_change_in_inventories",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_change_in_inventories",
)


_ext_lookup_historic_gdp = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    "_ext_lookup_historic_gdp",
)


_ext_lookup_historic_gfcf = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_gfcf",
)


_ext_lookup_historic_goverment_expenditures = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_goverment_expenditures",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_goverment_expenditures",
)


_ext_lookup_historic_hd = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_HD",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_hd",
)


_ext_lookup_historic_labour_compensation = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_labour_compensation",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_household_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for household_demand
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for household_demand function
    """
    return initial_household_demand()


@subs(["sectors"], _subscript_dict)
def _integ_input_household_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for household_demand
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for household_demand function
    """
    return variation_household_demand() - household_demand_not_covered()


_integ_household_demand = Integ(
    _integ_input_household_demand,
    _integ_init_household_demand,
    "_integ_household_demand",
)


_initial_initial_demand = Initial(lambda: historic_demand(), "_initial_initial_demand")


_ext_data_input_gdppc_annual_growth = ExtData(
    "../economy.xlsx",
    "World",
    "time_index_projection",
    "input_GDPpc_annual_growth",
    None,
    {},
    _root,
    "_ext_data_input_gdppc_annual_growth",
)


_integ_labour_share = Integ(
    lambda: variation_labour_share(), lambda: 0.6374, "_integ_labour_share"
)


_integ_lc = Integ(
    lambda: variation_lc() - lc_not_covered(), lambda: initial_lc_total(), "_integ_lc"
)


_ext_constant_p_customized_cte_gdppc_variation = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "G7",
    {},
    _root,
    "_ext_constant_p_customized_cte_gdppc_variation",
)


_ext_constant_p_customized_year_gdppc_evolution = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "E7",
    {},
    _root,
    "_ext_constant_p_customized_year_gdppc_evolution",
)


_ext_constant_p_labour_share_2050 = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "C3",
    {},
    _root,
    "_ext_constant_p_labour_share_2050",
)


_ext_data_p_timeseries_gdppc_growth_rate = ExtData(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "5",
    "E6",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


_ext_constant_select_gdppc_evolution_input = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "B4",
    {},
    _root,
    "_ext_constant_select_gdppc_evolution_input",
)
