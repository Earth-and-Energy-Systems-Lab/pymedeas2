"""
Module final_energy_footprint
Translated using PySD version 2.2.1
"""


def coverage_energy_rate():
    """
    Real Name: Coverage energy rate
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EU28 energy consumption covering total energy carriers of EU28 economy.
    """
    return total_final_energy_footprint() / real_tfec() - 1


@subs(["final sources", "sectors"], _subscript_dict)
def energy_embedded_in_eu_exports_by_sector_and_fuel():
    """
    Real Name: Energy embedded in EU exports by sector and fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Final energy embedded in EU28 exports.Energy required to produce the output necessary to satisfy Rest of the World demand of EU28 products
    """
    return (
        final_energy_intensity_by_sector_and_fuel_eu()
        * (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + total_domestic_output_required_for_exports_by_sector()
        )
        / m_per_t()
    )


@subs(["final sources", "sectors"], _subscript_dict)
def energy_embedded_in_eu_imports_by_sector_and_fuel():
    """
    Real Name: Energy embedded in EU imports by sector and fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Energy embedded in EU28 final products imports. Energy required to produced to output necessary to satisfy EU28 imports.
    """
    return (
        final_energy_intensity_by_sector_and_fuel_row()
        * (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + row_output_required_for_eu28_imports_by_sector()
        )
        / m_per_t()
    )


@subs(["final sources"], _subscript_dict)
def final_energy_footprint_by_fuel():
    """
    Real Name: Final energy footprint by fuel
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Final energy intensity of Rest of the World sectors. (Energy consumed by RoW/Value of output in RoW).
    """
    return (
        real_final_energy_by_sector_and_fuel_row()
        / (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + real_total_output_by_sector_row()
        )
        * 1000000.0
    )


@subs(["final sources", "sectors"], _subscript_dict)
def real_final_energy_by_sector_and_fuel_row():
    """
    Real Name: Real final energy by sector and fuel RoW
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources', 'sectors']

    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_world()
        - real_final_energy_by_sector_and_fuel_eu()
    )


@subs(["sectors"], _subscript_dict)
def row_output_required_for_eu28_imports_by_sector():
    """
    Real Name: RoW output required for EU28 imports by sector
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['sectors']

    Value of Rest of the World output (production) required to satisfy EU28 demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + real_final_demand_by_sector_eu().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@subs(["final sources"], _subscript_dict)
def total_energy_embedded_in_eu28_exports():
    """
    Real Name: Total energy embedded in EU28 exports
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Whole economy energy requirements to export.
    """
    return sum(
        energy_embedded_in_eu_exports_by_sector_and_fuel().rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    )


@subs(["final sources"], _subscript_dict)
def total_energy_embedded_in_eu28_imports():
    """
    Real Name: Total energy embedded in EU28 imports
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Whole economy (Rest of the World) energy requirements to satisfy EU28 imports.
    """
    return sum(
        energy_embedded_in_eu_imports_by_sector_and_fuel().rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    )


def total_final_energy_footprint():
    """
    Real Name: Total final energy footprint
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Whole economy final energy consumption to satisfy EU28 domestic final demand
    """
    return sum(
        final_energy_footprint_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )
