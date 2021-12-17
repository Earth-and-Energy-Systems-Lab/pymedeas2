"""
Module ghg_emissions_per_sector
Translated using PySD version 2.2.0
"""


@subs(["final sources", "sectors"], _subscript_dict)
def fe_by_sector_and_fuel():
    """
    Real Name: FE by sector and fuel
    Original Eqn: Real final energy by sector and fuel AUT[final sources,sectors]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']


    """
    return real_final_energy_by_sector_and_fuel_aut()


def fe_households():
    """
    Real Name: FE Households
    Original Eqn: SUM(Households final energy demand[final sources!])
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(households_final_energy_demand(), dim=("final sources",))


@subs(["sectors"], _subscript_dict)
def final_energy_by_sector():
    """
    Real Name: Final Energy by sector
    Original Eqn: SUM(FE by sector and fuel[final sources!,sectors])
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return sum(fe_by_sector_and_fuel(), dim=("final sources",))


@subs(["final sources"], _subscript_dict)
def ghg_emissions():
    """
    Real Name: GHG emissions
    Original Eqn:
      Total per FE CO2 emissions[electricity]+ Total per FE CH4 emissions[electricity]*IF THEN ELSE(Choose GWP time frame=1, GWP 20 year[CH4], GWP 100 year [CH4])/Mt per Gt
      Total per FE CO2 emissions[heat]+ Total per FE CH4 emissions[heat]*IF THEN ELSE(Choose GWP time frame =1, GWP 20 year[CH4], GWP 100 year[CH4])/Mt per Gt
      Total per FE CO2 emissions[liquids]+ Total per FE CH4 emissions[liquids]*IF THEN ELSE(Choose GWP time frame =1, GWP 20 year[CH4], GWP 100 year[CH4])/Mt per Gt
      Total per FE CO2 emissions[gases]+ Total per FE CH4 emissions[gases]*IF THEN ELSE(Choose GWP time frame =1, GWP 20 year[CH4], GWP 100 year[CH4])/Mt per Gt
      Total per FE CO2 emissions[solids]+ Total per FE CH4 emissions[solids]*IF THEN ELSE(Choose GWP time frame =1, GWP 20 year[CH4], GWP 100 year[CH4])/Mt per Gt
    Units: GtCO2‍e/Year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            float(total_per_fe_co2_emissions().loc["electricity"])
            + float(total_per_fe_ch4_emissions().loc["electricity"])
            * if_then_else(
                choose_gwp_time_frame() == 1,
                lambda: float(gwp_20_year().loc["CH4"]),
                lambda: float(gwp_100_year().loc["CH4"]),
            )
            / mt_per_gt(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(total_per_fe_co2_emissions().loc["heat"])
            + float(total_per_fe_ch4_emissions().loc["heat"])
            * if_then_else(
                choose_gwp_time_frame() == 1,
                lambda: float(gwp_20_year().loc["CH4"]),
                lambda: float(gwp_100_year().loc["CH4"]),
            )
            / mt_per_gt(),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            float(total_per_fe_co2_emissions().loc["liquids"])
            + float(total_per_fe_ch4_emissions().loc["liquids"])
            * if_then_else(
                choose_gwp_time_frame() == 1,
                lambda: float(gwp_20_year().loc["CH4"]),
                lambda: float(gwp_100_year().loc["CH4"]),
            )
            / mt_per_gt(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(total_per_fe_co2_emissions().loc["gases"])
            + float(total_per_fe_ch4_emissions().loc["gases"])
            * if_then_else(
                choose_gwp_time_frame() == 1,
                lambda: float(gwp_20_year().loc["CH4"]),
                lambda: float(gwp_100_year().loc["CH4"]),
            )
            / mt_per_gt(),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            float(total_per_fe_co2_emissions().loc["solids"])
            + float(total_per_fe_ch4_emissions().loc["solids"])
            * if_then_else(
                choose_gwp_time_frame() == 1,
                lambda: float(gwp_20_year().loc["CH4"]),
                lambda: float(gwp_100_year().loc["CH4"]),
            )
            / mt_per_gt(),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


@subs(["final sources"], _subscript_dict)
def ghg_emissions_by_households():
    """
    Real Name: GHG emissions by households
    Original Eqn:
      Households final energy demand[electricity]*ratio GHG by FE emissions[ electricity]
      Households final energy demand[heat]*ratio GHG by FE emissions[heat]
      Households final energy demand[liquids]*ratio GHG by FE emissions[ liquids]
      Households final energy demand[gases]*ratio GHG by FE emissions[gases]
      Households final energy demand[solids]*ratio GHG by FE emissions[ solids]
    Units: GtCO2‍e/Year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            float(households_final_energy_demand().loc["electricity"])
            * float(ratio_ghg_by_fe_emissions().loc["electricity"]),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            float(households_final_energy_demand().loc["heat"])
            * float(ratio_ghg_by_fe_emissions().loc["heat"]),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            float(households_final_energy_demand().loc["liquids"])
            * float(ratio_ghg_by_fe_emissions().loc["liquids"]),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            float(households_final_energy_demand().loc["gases"])
            * float(ratio_ghg_by_fe_emissions().loc["gases"]),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            float(households_final_energy_demand().loc["solids"])
            * float(ratio_ghg_by_fe_emissions().loc["solids"]),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


@subs(["sectors"], _subscript_dict)
def ghg_emissions_by_sector():
    """
    Real Name: GHG emissions by sector
    Original Eqn: SUM(ratio GHG by FE emissions[final sources!]*FE by sector and fuel[final sources!,sectors])
    Units: GtCO2‍e/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']


    """
    return sum(
        ratio_ghg_by_fe_emissions() * fe_by_sector_and_fuel(), dim=("final sources",)
    )


def ghg_households():
    """
    Real Name: GHG Households
    Original Eqn: Households final energy demand[electricity]*ratio GHG by FE emissions[ electricity]+ Households final energy demand[heat]*ratio GHG by FE emissions[heat]+ Households final energy demand[liquids]*ratio GHG by FE emissions[ liquids]+ Households final energy demand[gases]*ratio GHG by FE emissions[gases]+ Households final energy demand[solids]*ratio GHG by FE emissions[ solids]
    Units: GTCO2e/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        float(households_final_energy_demand().loc["electricity"])
        * float(ratio_ghg_by_fe_emissions().loc["electricity"])
        + float(households_final_energy_demand().loc["heat"])
        * float(ratio_ghg_by_fe_emissions().loc["heat"])
        + float(households_final_energy_demand().loc["liquids"])
        * float(ratio_ghg_by_fe_emissions().loc["liquids"])
        + float(households_final_energy_demand().loc["gases"])
        * float(ratio_ghg_by_fe_emissions().loc["gases"])
        + float(households_final_energy_demand().loc["solids"])
        * float(ratio_ghg_by_fe_emissions().loc["solids"])
    )


@subs(["final sources"], _subscript_dict)
def ratio_ghg_by_fe_emissions():
    """
    Real Name: ratio GHG by FE emissions
    Original Eqn:
      ZIDZ(GHG emissions[electricity], Total FE Elec consumption EJ )
      ZIDZ(GHG emissions[heat], Total FED Heat EJ )
      ZIDZ(GHG emissions[liquids], Total FEC liquids )
      ZIDZ(GHG emissions[gases], real FE consumption gases EJ )
      ZIDZ(GHG emissions[solids], Required FED solids )
    Units: GtCO2‍e/EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            zidz(
                float(ghg_emissions().loc["electricity"]),
                total_fe_elec_consumption_ej(),
            ),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            zidz(float(ghg_emissions().loc["heat"]), total_fed_heat_ej()),
            ["final sources"],
            {"final sources": ["heat"]},
        ),
        rearrange(
            zidz(float(ghg_emissions().loc["liquids"]), total_fec_liquids()),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            zidz(float(ghg_emissions().loc["gases"]), real_fe_consumption_gases_ej()),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            zidz(float(ghg_emissions().loc["solids"]), required_fed_solids()),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


def total_final_energy_all_sectors():
    """
    Real Name: Total Final Energy all sectors
    Original Eqn: SUM(Final Energy by sector[sectors!])+FE Households
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(final_energy_by_sector(), dim=("sectors",)) + fe_households()


def total_ghg_emissions():
    """
    Real Name: Total GHG emissions
    Original Eqn: SUM (GHG emissions[final sources!] )
    Units: GtCO2‍e/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(ghg_emissions(), dim=("final sources",))


def total_ghg_emissions_all_sectors():
    """
    Real Name: Total GHG emissions all sectors
    Original Eqn: SUM(GHG emissions by sector[sectors!])+GHG Households
    Units: GtCO2‍e/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(ghg_emissions_by_sector(), dim=("sectors",)) + ghg_households()
