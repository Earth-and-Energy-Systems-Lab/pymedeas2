"""
Module final_energy_footprint
Translated using PySD version 2.1.0
"""


def coverage_energy_rate():
    """
    Real Name: Coverage energy rate
    Original Eqn: Total final energy footprint/Real TFEC-1
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    EU28 energy consumption covering total energy carriers of EU28 economy.
    """
    return total_final_energy_footprint() / real_tfec() - 1


@subs(["final sources", "sectors"], _subscript_dict)
def energy_embedded_in_aut_imports_by_sector_and_fuel():
    """
    Real Name: Energy embedded in AUT imports by sector and fuel
    Original Eqn: Energy embedded in AUT imports from RoEU by sector and fuel[final sources,sectors]+Enery embedded in AUT imports from RoW by sector and fuel[final sources,sectors]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Energy embedded in EU28 final products imports. Energy required to
        produced to output necessary to satisfy EU28 imports.
    """
    return (
        energy_embedded_in_aut_imports_from_roeu_by_sector_and_fuel()
        + enery_embedded_in_aut_imports_from_row_by_sector_and_fuel()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def energy_embedded_in_aut_imports_from_roeu_by_sector_and_fuel():
    """
    Real Name: Energy embedded in AUT imports from RoEU by sector and fuel
    Original Eqn: Final energy intensity by sector and fuel RoW 0[final sources,sectors]*RoEU output required for AUT imports by sector[sectors]/M per T
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']


    """
    return (
        final_energy_intensity_by_sector_and_fuel_row_0()
        * roeu_output_required_for_aut_imports_by_sector()
        / m_per_t()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def energy_embedded_in_eu_exports_by_sector_and_fuel():
    """
    Real Name: Energy embedded in EU exports by sector and fuel
    Original Eqn: Final energy intensity by sector and fuel EU[final sources,sectors]*Required total output for exports[ sectors]/M per T
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Final energy embedded in EU28 exports.Energy required to produce the
        output necessary to satisfy Rest of the World demand of EU28 products
    """
    return (
        final_energy_intensity_by_sector_and_fuel_eu()
        * required_total_output_for_exports()
        / m_per_t()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def enery_embedded_in_aut_imports_from_row_by_sector_and_fuel():
    """
    Real Name: Enery embedded in AUT imports from RoW by sector and fuel
    Original Eqn: Final energy intensity by sector and fuel RoW[final sources,sectors]*RoW output required for AUT imports by sector[sectors]/M per T
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']


    """
    return (
        final_energy_intensity_by_sector_and_fuel_row()
        * row_output_required_for_aut_imports_by_sector()
        / m_per_t()
    )


@subs(["final sources"], _subscript_dict)
def final_energy_footprint_by_fuel():
    """
    Real Name: Final energy footprint by fuel
    Original Eqn: Households final energy demand[final sources]+required FED sectors by fuel[final sources]+Total energy embedded in EU28 imports [final sources]-Total energy embedded in EU28 exports[final sources]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Final energy consumption to satisfy EU28 domestic final demand by sector
    """
    return (
        households_final_energy_demand()
        + required_fed_sectors_by_fuel()
        + total_energy_embedded_in_eu28_imports()
        - total_energy_embedded_in_eu28_exports()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_by_sector_and_fuel_row():
    """
    Real Name: Final energy intensity by sector and fuel RoW
    Original Eqn: Real final energy by sector and fuel RoW[final sources,sectors]/Real total output by sector RoW[sectors]*1e+06
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Final energy intensity of Rest of the World sectors. (Energy consumed by
        RoW/Value of output in RoW).
    """
    return (
        real_final_energy_by_sector_and_fuel_row()
        / real_total_output_by_sector_row()
        * 1e06
    )


@subs(["final sources", "sectors"], _subscript_dict)
def final_energy_intensity_by_sector_and_fuel_row_0():
    """
    Real Name: Final energy intensity by sector and fuel RoW 0
    Original Eqn: Real final energy by sector and fuel RoEU[final sources,sectors]/Real total output by sector RoEU[sectors]*1e+06
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Final energy intensity of Rest of the World sectors. (Energy consumed by
        RoW/Value of output in RoW).
    """
    return (
        real_final_energy_by_sector_and_fuel_roeu()
        / real_total_output_by_sector_roeu()
        * 1e06
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_roeu():
    """
    Real Name: Real final energy by sector and fuel RoEU
    Original Eqn: Real final energy by sector and fuel EU28[final sources,sectors]-Real final energy by sector and fuel AUT[final sources,sectors]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_eu28()
        - real_final_energy_by_sector_and_fuel_aut()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_row():
    """
    Real Name: Real final energy by sector and fuel RoW
    Original Eqn: Real final energy by sector and fuel World[final sources,sectors]-Real final energy by sector and fuel EU28[final sources,sectors]
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['final sources', 'sectors']

    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_world()
        - real_final_energy_by_sector_and_fuel_eu28()
    )


@subs(["sectors"], _subscript_dict)
def roeu_output_required_for_aut_imports_by_sector():
    """
    Real Name: RoEU output required for AUT imports by sector
    Original Eqn: SUM(Leontief Matrix Imports 1[sectors,sectors1!]*Real final demand by sector AUT[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Value of Rest of the World output (production) required to satisfy EU28
        demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports_1()
        * rearrange(real_final_demand_by_sector_aut(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["sectors"], _subscript_dict)
def row_output_required_for_aut_imports_by_sector():
    """
    Real Name: RoW output required for AUT imports by sector
    Original Eqn: SUM(Leontief Matrix Imports 0[sectors,sectors1!]*Real final demand by sector AUT[sectors1!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Value of Rest of the World output (production) required to satisfy EU28
        demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports_0()
        * rearrange(real_final_demand_by_sector_aut(), ["sectors1"], _subscript_dict),
        dim=("sectors1",),
    )


@subs(["final sources"], _subscript_dict)
def total_energy_embedded_in_eu28_exports():
    """
    Real Name: Total energy embedded in EU28 exports
    Original Eqn: SUM(Energy embedded in EU exports by sector and fuel[final sources,sectors!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Whole economy energy requirements to export.
    """
    return sum(energy_embedded_in_eu_exports_by_sector_and_fuel(), dim=("sectors",))


@subs(["final sources"], _subscript_dict)
def total_energy_embedded_in_eu28_imports():
    """
    Real Name: Total energy embedded in EU28 imports
    Original Eqn: SUM(Energy embedded in AUT imports by sector and fuel[final sources,sectors!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Whole economy (Rest of the World) energy requirements to satisfy EU28
        imports.
    """
    return sum(energy_embedded_in_aut_imports_by_sector_and_fuel(), dim=("sectors",))


def total_final_energy_footprint():
    """
    Real Name: Total final energy footprint
    Original Eqn: SUM(Final energy footprint by fuel[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy final energy consumption to satisfy EU28 domestic final
        demand
    """
    return sum(final_energy_footprint_by_fuel(), dim=("final sources",))
