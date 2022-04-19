"""
Module energy_consumption
Translated using PySD version 3.0.0
"""


@component.add(
    name="Energy cons per unit of material cons for RES elec",
    units="MJ/kg",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_cons_per_unit_of_material_cons_for_res_elec():
    """
    Average energy consumption per unit of material consumption accounting for recycling rates for RES elec technologies. recycling rates minerals RES elec[materials]*"Initial energy cons per unit of material cons (recycled)"[materials]+(1-recycling rates minerals RES elec[materials])*"Initial energy cons per unit of material cons (virgin)"[materials]
    """
    return (
        recycling_rates_minerals_alt_techn()
        * initial_energy_cons_per_unit_of_material_cons_recycled()
        + (1 - recycling_rates_minerals_alt_techn())
        * initial_energy_cons_per_unit_of_material_cons_virgin()
    )


@component.add(
    name="Energy required for material consumption for EV batteries",
    units="EJ",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_required_for_material_consumption_for_ev_batteries():
    """
    Energy required for material consumption for EV batteries.
    """
    return (
        materials_required_for_ev_batteries_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name="Energy required for material consumption for new RES elec",
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_required_for_material_consumption_for_new_res_elec():
    """
    Energy required for material consumption for new RES elec.
    """
    return (
        materials_required_for_new_res_elec_mt()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + energy_cons_per_unit_of_material_cons_for_res_elec()
        )
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name='"Energy required for material consumption for O&M RES elec"',
    units="EJ",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_required_for_material_consumption_for_om_res_elec():
    return (
        materials_required_for_om_res_elec_mt()
        * (
            xr.DataArray(
                0,
                {
                    "RES elec": _subscript_dict["RES elec"],
                    "materials": _subscript_dict["materials"],
                },
                ["RES elec", "materials"],
            )
            + energy_cons_per_unit_of_material_cons_for_res_elec()
        )
        * kg_per_mt()
        / mj_per_ej()
    )


@component.add(
    name="Energy required for material consumption per RES elec",
    units="EJ/Year",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def energy_required_for_material_consumption_per_res_elec():
    """
    Energy required for material consumption per material per RES elec technologies.
    """
    return (
        energy_required_for_material_consumption_for_om_res_elec()
        + energy_required_for_material_consumption_for_new_res_elec()
    )


@component.add(
    name='"Initial energy cons per unit of material cons (recycled) - data"',
    units="MJ/kg",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
)
def initial_energy_cons_per_unit_of_material_cons_recycled_data():
    """
    Energy consumption required to use recycled materials per unit of material consumption. This variable has 0s for those materials for which information was not found.
    """
    return _ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled_data()


_ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled_data = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_energy_cons_per_material_recycled*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {
        "materials": [
            "Adhesive",
            "Aluminium",
            "Aluminium mirrors",
            "Cadmium",
            "Carbon fiber",
            "Cement",
            "Chromium",
            "Copper",
            "diesel",
            "Dy",
            "electronic components",
            "Evacuation lines",
            "Fiberglass",
            "Foam glass",
            "Galium",
            "Glass",
            "Glass reinforcing plastic",
            "gravel",
            "Indium",
            "Iron",
            "KNO3 mined",
            "Asphalt",
            "Lime",
            "Limestone",
            "Lithium",
            "Lubricant",
            "Magnesium",
            "Manganese",
            "Heavy equipment",
            "Concrete",
            "Molybdenum",
            "NaNO3 mined",
            "NaNO3 synthetic",
            "Neodymium",
            "Nickel",
            "over grid 15perc",
            "over grid 5perc",
            "Paint",
            "Lead",
            "Plastics",
            "Polypropylene",
            "Rock",
            "Rock wool",
            "Sand",
            "Silicon sand",
            "Silicon wafer modules",
            "Silver",
            "Site preparation",
            "Tin",
            "soda ash",
            "steel",
            "synthetic oil",
            "tellurium",
            "titanium",
            "titanium dioxide",
            "vanadium",
            "wires",
            "zinc",
        ]
    },
    "_ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled_data",
)


@component.add(
    name='"Initial energy cons per unit of material cons (recycled)"',
    units="MJ/kg",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_energy_cons_per_unit_of_material_cons_recycled():
    """
    Energy consumption required to use recycled materials per unit of material consumption. When data for recycled materials was not available, the energy consumption for virgin materials was assumed.
    """
    return if_then_else(
        initial_energy_cons_per_unit_of_material_cons_recycled_data() == 0,
        lambda: initial_energy_cons_per_unit_of_material_cons_virgin(),
        lambda: initial_energy_cons_per_unit_of_material_cons_recycled_data(),
    )


@component.add(
    name='"Initial energy cons per unit of material cons (virgin)"',
    units="MJ/kg",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
)
def initial_energy_cons_per_unit_of_material_cons_virgin():
    """
    Energy consumption required to extract and use virgin materials per unit of material consumption.
    """
    return _ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin()


_ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_energy_cons_per_material_virgin*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {
        "materials": [
            "Adhesive",
            "Aluminium",
            "Aluminium mirrors",
            "Cadmium",
            "Carbon fiber",
            "Cement",
            "Chromium",
            "Copper",
            "diesel",
            "Dy",
            "electronic components",
            "Evacuation lines",
            "Fiberglass",
            "Foam glass",
            "Galium",
            "Glass",
            "Glass reinforcing plastic",
            "gravel",
            "Indium",
            "Iron",
            "KNO3 mined",
            "Asphalt",
            "Lime",
            "Limestone",
            "Lithium",
            "Lubricant",
            "Magnesium",
            "Manganese",
            "Heavy equipment",
            "Concrete",
            "Molybdenum",
            "NaNO3 mined",
            "NaNO3 synthetic",
            "Neodymium",
            "Nickel",
            "over grid 15perc",
            "over grid 5perc",
            "Paint",
            "Lead",
            "Plastics",
            "Polypropylene",
            "Rock",
            "Rock wool",
            "Sand",
            "Silicon sand",
            "Silicon wafer modules",
            "Silver",
            "Site preparation",
            "Tin",
            "soda ash",
            "steel",
            "synthetic oil",
            "tellurium",
            "titanium",
            "titanium dioxide",
            "vanadium",
            "wires",
            "zinc",
        ]
    },
    "_ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin",
)


@component.add(
    name="MJ per EJ", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mj_per_ej():
    return 1000000000000.0


@component.add(
    name="share energy for material consumption for alt techn vs TFEC",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_energy_for_material_consumption_for_alt_techn_vs_tfec():
    """
    Share of energy requirements for alternative technologies (RES elec & EV Batteries) vs TFES.
    """
    return tfe_required_for_total_material_consumption_for_alt_techn() / real_tfec()


@component.add(
    name="TFE required for total material consumption for alt techn",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def tfe_required_for_total_material_consumption_for_alt_techn():
    """
    Total final energy required for total material consumption for alternative technologies (RES elec & EV Batteries).
    """
    return (
        total_energy_required_for_material_consumption_for_res_elec()
        + total_energy_required_for_total_material_consumption_for_ev_batteries()
    )


@component.add(
    name="Total energy required for material consumption for RES elec",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_required_for_material_consumption_for_res_elec():
    """
    Total energy required for material consumption for RES elec.
    """
    return sum(
        energy_required_for_material_consumption_per_res_elec().rename(
            {"RES elec": "RES elec!", "materials": "materials!"}
        ),
        dim=["RES elec!", "materials!"],
    )


@component.add(
    name="Total energy required for material consumption per RES elec",
    units="EJ",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_required_for_material_consumption_per_res_elec():
    """
    Total energy required for material consumption per RES elec
    """
    return sum(
        energy_required_for_material_consumption_per_res_elec().rename(
            {"materials": "materials!"}
        ),
        dim=["materials!"],
    )


@component.add(
    name="Total energy required for total material consumption for EV batteries",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_required_for_total_material_consumption_for_ev_batteries():
    """
    Total energy required for total material consumption for EV batteries.
    """
    return sum(
        energy_required_for_material_consumption_for_ev_batteries().rename(
            {"materials": "materials!"}
        ),
        dim=["materials!"],
    )


@component.add(
    name="Total energy required per material for alt techn",
    units="EJ/Year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_energy_required_per_material_for_alt_techn():
    """
    Total energy required for total material consumption per material for alternative technologies (RES elec & EV Batteries).
    """
    return (
        sum(
            energy_required_for_material_consumption_per_res_elec().rename(
                {"RES elec": "RES elec!"}
            ),
            dim=["RES elec!"],
        )
        + energy_required_for_material_consumption_for_ev_batteries()
    )
