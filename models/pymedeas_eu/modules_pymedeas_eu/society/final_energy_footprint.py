"""
Module society.final_energy_footprint
Translated using PySD version 3.14.0
"""

@component.add(
    name="Coverage_energy_rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_final_energy_footprint": 1, "real_tfec": 1},
)
def coverage_energy_rate():
    """
    EU28 energy consumption covering total energy carriers of EU28 economy.
    """
    return total_final_energy_footprint() / real_tfec() - 1


@component.add(
    name="Energy_embedded_in_EU_exports_by_sector_and_fuel",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_energy_intensity_by_sector_and_fuel_eu": 1,
        "total_domestic_output_required_for_exports_by_sector": 1,
        "m_to_t": 1,
        "nvs_1_year": 1,
    },
)
def energy_embedded_in_eu_exports_by_sector_and_fuel():
    """
    Final energy embedded in EU28 exports.Energy required to produce the output necessary to satisfy Rest of the World demand of EU28 products
    """
    return (
        final_energy_intensity_by_sector_and_fuel_eu()
        * total_domestic_output_required_for_exports_by_sector()
        * m_to_t()
        / nvs_1_year()
    )


@component.add(
    name="Energy_embedded_in_EU_imports_by_sector_and_fuel",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_energy_intensity_by_sector_and_fuel_row": 1,
        "row_output_required_for_eu28_imports_by_sector": 1,
        "m_to_t": 1,
        "nvs_1_year": 1,
    },
)
def energy_embedded_in_eu_imports_by_sector_and_fuel():
    """
    Energy embedded in EU28 final products imports. Energy required to produced to output necessary to satisfy EU28 imports.
    """
    return (
        final_energy_intensity_by_sector_and_fuel_row()
        * row_output_required_for_eu28_imports_by_sector()
        * m_to_t()
        / nvs_1_year()
    )


@component.add(
    name="Final_energy_footprint_by_fuel",
    units="EJ/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_final_energy_demand": 1,
        "required_fed_sectors_by_fuel": 1,
        "total_energy_embedded_in_eu28_imports": 1,
        "total_energy_embedded_in_eu28_exports": 1,
    },
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
    name="Final_energy_intensity_by_sector_and_fuel_RoW",
    units="EJ/T$",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel_row": 1,
        "real_total_output_by_sector_row": 1,
        "m_to_t": 1,
        "nvs_1_year": 1,
    },
)
def final_energy_intensity_by_sector_and_fuel_row():
    """
    Final energy intensity of Rest of the World sectors. (Energy consumed by RoW/Value of output in RoW).
    """
    return (
        real_final_energy_by_sector_and_fuel_row()
        / real_total_output_by_sector_row()
        / m_to_t()
        * nvs_1_year()
    )


@component.add(
    name="Real_final_energy_by_sector_and_fuel_RoW",
    units="EJ/year",
    subscripts=[np.str_("final_sources"), np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_final_energy_by_sector_and_fuel_world": 1,
        "real_final_energy_by_sector_and_fuel_eu": 1,
    },
)
def real_final_energy_by_sector_and_fuel_row():
    """
    Real final energy consumption made by Rest of the World.
    """
    return (
        real_final_energy_by_sector_and_fuel_world()
        - real_final_energy_by_sector_and_fuel_eu()
    )


@component.add(
    name="RoW_output_required_for_EU28_imports_by_sector",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"leontief_matrix_imports": 1, "real_final_demand_by_sector_eu": 1},
)
def row_output_required_for_eu28_imports_by_sector():
    """
    Value of Rest of the World output (production) required to satisfy EU28 demand of RoW producs (imports).
    """
    return sum(
        leontief_matrix_imports().rename({np.str_("sectors1"): "sectors1!"})
        * real_final_demand_by_sector_eu().rename({np.str_("sectors"): "sectors1!"}),
        dim=["sectors1!"],
    )


@component.add(
    name="Total_energy_embedded_in_EU28_exports",
    units="EJ/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_embedded_in_eu_exports_by_sector_and_fuel": 1},
)
def total_energy_embedded_in_eu28_exports():
    """
    Whole economy energy requirements to export.
    """
    return sum(
        energy_embedded_in_eu_exports_by_sector_and_fuel().rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    )


@component.add(
    name="Total_energy_embedded_in_EU28_imports",
    units="EJ/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_embedded_in_eu_imports_by_sector_and_fuel": 1},
)
def total_energy_embedded_in_eu28_imports():
    """
    Whole economy (Rest of the World) energy requirements to satisfy EU28 imports.
    """
    return sum(
        energy_embedded_in_eu_imports_by_sector_and_fuel().rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    )


@component.add(
    name="Total_final_energy_footprint",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_energy_footprint_by_fuel": 1},
)
def total_final_energy_footprint():
    """
    Whole economy final energy consumption to satisfy EU28 domestic final demand
    """
    return sum(
        final_energy_footprint_by_fuel().rename(
            {np.str_("final_sources"): "final_sources!"}
        ),
        dim=["final_sources!"],
    )
