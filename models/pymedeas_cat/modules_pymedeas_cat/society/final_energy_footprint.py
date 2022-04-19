"""
Module final_energy_footprint
Translated using PySD version 3.0.0
"""


@component.add(
    name="Coverage energy rate", comp_type="Auxiliary", comp_subtype="Normal"
)
def coverage_energy_rate():
    """
    EU28 energy consumption covering total energy carriers of EU28 economy.
    """
    return total_final_energy_footprint() / real_tfec() - 1


@component.add(
    name="Energy embedded in AUT imports by sector and fuel",
    units="EJ",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_embedded_in_aut_imports_by_sector_and_fuel():
    """
    Energy embedded in EU28 final products imports. Energy required to produced to output necessary to satisfy EU28 imports.
    """
    return (
        energy_embedded_in_aut_imports_from_roeu_by_sector_and_fuel()
        + enery_embedded_in_aut_imports_from_row_by_sector_and_fuel()
    )


@component.add(
    name="Energy embedded in AUT imports from RoEU by sector and fuel",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_embedded_in_aut_imports_from_roeu_by_sector_and_fuel():
    return (
        final_energy_intensity_by_sector_and_fuel_row_0()
        * (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + roeu_output_required_for_aut_imports_by_sector()
        )
        / m_per_t()
    )


@component.add(
    name="Energy embedded in EU exports by sector and fuel",
    units="EJ",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_embedded_in_eu_exports_by_sector_and_fuel():
    """
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
            + required_total_output_for_exports()
        )
        / m_per_t()
    )


@component.add(
    name="Enery embedded in AUT imports from RoW by sector and fuel",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def enery_embedded_in_aut_imports_from_row_by_sector_and_fuel():
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
            + row_output_required_for_aut_imports_by_sector()
        )
        / m_per_t()
    )


@component.add(
    name="Final energy footprint by fuel",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def final_energy_footprint_by_fuel():
    """
    Final energy consumption to satisfy EU28 domestic final demand by sector
    """
    return (
        households_final_energy_demand()
        + required_fed_sectors_by_fuel()
        + total_energy_embedded_in_eu28_imports()
        - total_energy_embedded_in_eu28_exports()
    )


@component.add(
    name="Final energy intensity by sector and fuel RoW",
    units="Dmnl",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def final_energy_intensity_by_sector_and_fuel_row():
    """
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


@component.add(
    name="Final energy intensity by sector and fuel RoW 0",
    units="Dmnl",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def final_energy_intensity_by_sector_and_fuel_row_0():
    """
    Final energy intensity of Rest of the World sectors. (Energy consumed by RoW/Value of output in RoW).
    """
    return (
        real_final_energy_by_sector_and_fuel_roeu()
        / (
            xr.DataArray(
                0,
                {
                    "final sources": _subscript_dict["final sources"],
                    "sectors": _subscript_dict["sectors"],
                },
                ["final sources", "sectors"],
            )
            + real_total_output_by_sector_roeu()
        )
        * 1000000.0
    )


@component.add(
    name="Real final energy by sector and fuel RoEU",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_final_energy_by_sector_and_fuel_roeu():
    """
    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_eu28()
        - real_final_energy_by_sector_and_fuel_aut()
    )


@component.add(
    name="Real final energy by sector and fuel RoW",
    subscripts=["final sources", "sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_final_energy_by_sector_and_fuel_row():
    """
    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_world()
        - real_final_energy_by_sector_and_fuel_eu28()
    )


@component.add(
    name="RoEU output required for AUT imports by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def roeu_output_required_for_aut_imports_by_sector():
    """
    Value of Rest of the World output (production) required to satisfy EU28 demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports_1().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + real_final_demand_by_sector_aut().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@component.add(
    name="RoW output required for AUT imports by sector",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def row_output_required_for_aut_imports_by_sector():
    """
    Value of Rest of the World output (production) required to satisfy EU28 demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports_0().rename({"sectors1": "sectors1!"})
        * (
            xr.DataArray(
                0,
                {
                    "sectors": _subscript_dict["sectors"],
                    "sectors1!": _subscript_dict["sectors1"],
                },
                ["sectors", "sectors1!"],
            )
            + real_final_demand_by_sector_aut().rename({"sectors": "sectors1!"})
        ),
        dim=["sectors1!"],
    )


@component.add(
    name="Total energy embedded in EU28 exports",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_embedded_in_eu28_exports():
    """
    Whole economy energy requirements to export.
    """
    return sum(
        energy_embedded_in_eu_exports_by_sector_and_fuel().rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    )


@component.add(
    name="Total energy embedded in EU28 imports",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_embedded_in_eu28_imports():
    """
    Whole economy (Rest of the World) energy requirements to satisfy EU28 imports.
    """
    return sum(
        energy_embedded_in_aut_imports_by_sector_and_fuel().rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    )


@component.add(
    name="Total final energy footprint",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_final_energy_footprint():
    """
    Whole economy final energy consumption to satisfy EU28 domestic final demand
    """
    return sum(
        final_energy_footprint_by_fuel().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )
