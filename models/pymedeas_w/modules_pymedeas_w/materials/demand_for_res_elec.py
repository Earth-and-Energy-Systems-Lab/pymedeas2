"""
Module demand_for_res_elec
Translated using PySD version 2.2.0
"""


@subs(["materials"], _subscript_dict)
def cum_materials_requirements_for_res_elec():
    """
    Real Name: cum materials requirements for RES elec
    Original Eqn: INTEG ( Total materials required for RES elec Mt[materials], initial cumulated material requirements for RES elec 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total cumulative materials requirements for the installation and O&M of
        RES for electricity generation.
    """
    return _integ_cum_materials_requirements_for_res_elec()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_res_elec():
    """
    Real Name: cum materials to extract for RES elec
    Original Eqn: INTEG ( Total materials to extract for RES elec Mt[materials], initial cumulated material requirements for RES elec 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for the installation and O&M of RES for
        electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec()


@subs(["materials"], _subscript_dict)
def cum_materials_to_extract_for_res_elec_from_2015():
    """
    Real Name: cum materials to extract for RES elec from 2015
    Original Eqn: INTEG ( Total materials to extract for RES elec from 2015 Mt[materials], initial cumulated material requirements for RES elec 1995)
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Cumulative materials to be mined for the installation and O&M of RES for
        electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec_from_2015()


def include_materials_for_overgrids():
    """
    Real Name: "include materials for overgrids?"
    Original Eqn: 0
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1. Include materials for overgrids in the CED of RES elec var        0: NOT include materials for overgrids in the CED of RES elec var
    """
    return 0


def initial_cumulated_material_requirements_for_res_elec_1995():
    """
    Real Name: initial cumulated material requirements for RES elec 1995
    Original Eqn: 0
    Units: Mt
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0


def kg_per_mt():
    """
    Real Name: kg per Mt
    Original Eqn: 1e+09
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion factor from Mt to kg.
    """
    return 1e09


def m_per_t():
    """
    Real Name: M per T
    Original Eqn: 1e+06
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion factor from Tera (T, 1e12) to Mega (M, 1e6).
    """
    return 1e06


@subs(["RES elec", "materials"], _subscript_dict)
def materials_for_new_res_elec_per_capacity_installed():
    """
    Real Name: materials for new RES elec per capacity installed
    Original Eqn:
      0
      materials per new capacity installed RES[RES ELEC MAINTENANCE, materials]+(materials per new RES elec capacity installed HVDCs [materials]+materials per new RES elec capacity installed material overgrid high power[materials])*"include materials for overgrids?"
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec', 'materials']


    """
    return xrmerge(
        xr.DataArray(
            0,
            {
                "RES elec": _subscript_dict["RES ELEC NO MAINTENANCE"],
                "materials": _subscript_dict["materials"],
            },
            ["RES elec", "materials"],
        ),
        rearrange(
            materials_per_new_capacity_installed_res()
            + (
                materials_per_new_res_elec_capacity_installed_hvdcs()
                + materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
            )
            * include_materials_for_overgrids(),
            ["RES elec", "materials"],
            {
                "RES elec": ["wind onshore", "wind offshore", "solar PV", "CSP"],
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
                ],
            },
        ),
    )


@subs(["RES elec", "materials"], _subscript_dict)
def materials_for_om_per_capacity_installed_res_elec():
    """
    Real Name: "materials for O&M per capacity installed RES elec"
    Original Eqn:
      0
      GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'materials_for_om_per_capacity_installed_res_elec*')
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec', 'materials']

    Materials requirements for operation and maintenance per unit of new
        installed capacity of RES elec.
    """
    return xrmerge(
        xr.DataArray(
            0,
            {
                "RES elec": _subscript_dict["RES ELEC NO MAINTENANCE"],
                "materials": _subscript_dict["materials"],
            },
            ["RES elec", "materials"],
        ),
        _ext_constant_materials_for_om_per_capacity_installed_res_elec(),
    )


@subs(["RES ELEC MAINTENANCE", "materials"], _subscript_dict)
def materials_per_new_capacity_installed_res():
    """
    Real Name: materials per new capacity installed RES
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'materials_per_new_capacity_installed_res*')
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['RES ELEC MAINTENANCE', 'materials']

    Materials requirements per unit of new installed capacity of RES.
    """
    return _ext_constant_materials_per_new_capacity_installed_res()


@subs(["materials"], _subscript_dict)
def materials_per_new_res_elec_capacity_installed_hvdcs():
    """
    Real Name: materials per new RES elec capacity installed HVDCs
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'materials_per_new_res_elec_capacity_installed_hvdcs*')
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Materials requirements for inter-regional grids (HVDCs) per unit of new
        installed capacity of RES variable for electricity.
    """
    return _ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs()


@subs(["materials"], _subscript_dict)
def materials_per_new_res_elec_capacity_installed_material_overgrid_high_power():
    """
    Real Name: materials per new RES elec capacity installed material overgrid high power
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'materials_per_new_res_elec_capacity_installed_material_overgrid_high_power*')
    Units: kg/MW
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Materials requirements for overgrid high power per unit of new installed
        capacity of RES variable for electricity.
    """
    return (
        _ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def materials_required_for_new_res_elec_mt():
    """
    Real Name: materials required for new RES elec Mt
    Original Eqn: RES elec capacity under construction TW[RES elec]*materials for new RES elec per capacity installed[RES elec,materials]*M per T/kg per Mt
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Annual materials required for the installation of new capacity of RES for
        electricity by technology.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * materials_for_new_res_elec_per_capacity_installed()
        * m_per_t()
        / kg_per_mt()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def materials_required_for_om_res_elec_mt():
    """
    Real Name: "materials required for O&M RES elec Mt"
    Original Eqn: installed capacity RES elec TW[RES elec]*"materials for O&M per capacity installed RES elec"[RES elec,materials]*M per T/kg per Mt
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Annual materials required for the operation and maintenance of the
        capacity of RES for electricity in operation by technology.
    """
    return (
        installed_capacity_res_elec_tw()
        * materials_for_om_per_capacity_installed_res_elec()
        * m_per_t()
        / kg_per_mt()
    )


@subs(["materials"], _subscript_dict)
def total_materials_required_for_new_res_elec_mt():
    """
    Real Name: Total materials required for new RES elec Mt
    Original Eqn: SUM(materials required for new RES elec Mt[RES elec!,materials])
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total annual materials requirements per new installed capacity of RES for
        electricity generation.
    """
    return sum(materials_required_for_new_res_elec_mt(), dim=("RES elec",))


@subs(["materials"], _subscript_dict)
def total_materials_required_for_om_res_elec_mt():
    """
    Real Name: "Total materials required for O&M RES elec Mt"
    Original Eqn: SUM("materials required for O&M RES elec Mt"[RES elec!,materials])
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total annual materials required for the operation and maintenance of the
        capacity of RES for electricity in operation by technology.
    """
    return sum(materials_required_for_om_res_elec_mt(), dim=("RES elec",))


@subs(["materials"], _subscript_dict)
def total_materials_required_for_res_elec_mt():
    """
    Real Name: Total materials required for RES elec Mt
    Original Eqn: Total materials required for new RES elec Mt[materials]+"Total materials required for O&M RES elec Mt"[materials]
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total annual materials requirements for the installation and O&M of RES
        for electricity generation.
    """
    return (
        total_materials_required_for_new_res_elec_mt()
        + total_materials_required_for_om_res_elec_mt()
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_res_elec_from_2015_mt():
    """
    Real Name: Total materials to extract for RES elec from 2015 Mt
    Original Eqn: IF THEN ELSE(Time<2015,0,Total materials to extract for RES elec Mt[materials] )
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual materials to be mined for the installation and O&M of RES for
        electricity generation from 2015.
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: total_materials_to_extract_for_res_elec_mt()
    )


@subs(["materials"], _subscript_dict)
def total_materials_to_extract_for_res_elec_mt():
    """
    Real Name: Total materials to extract for RES elec Mt
    Original Eqn: Total materials required for RES elec Mt[materials]*(1-recycling rates minerals alt techn[materials])
    Units: Mt/year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Annual materials to be mined for the installation and O&M of RES for
        electricity generation.
    """
    return total_materials_required_for_res_elec_mt() * (
        1 - recycling_rates_minerals_alt_techn()
    )


@subs(["materials"], _subscript_dict)
def total_recycled_materials_for_res_elec_mt():
    """
    Real Name: Total recycled materials for RES elec Mt
    Original Eqn: Total materials required for RES elec Mt[materials]-Total materials to extract for RES elec Mt[materials]
    Units: Mt
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total recycled materials for RES technologies for the generation of
        electricity.
    """
    return (
        total_materials_required_for_res_elec_mt()
        - total_materials_to_extract_for_res_elec_mt()
    )


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_requirements_for_res_elec():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_requirements_for_res_elec
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_requirements_for_res_elec function
    """
    return initial_cumulated_material_requirements_for_res_elec_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_requirements_for_res_elec():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_requirements_for_res_elec
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_requirements_for_res_elec function
    """
    return total_materials_required_for_res_elec_mt()


_integ_cum_materials_requirements_for_res_elec = Integ(
    _integ_input_cum_materials_requirements_for_res_elec,
    _integ_init_cum_materials_requirements_for_res_elec,
    "_integ_cum_materials_requirements_for_res_elec",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_for_res_elec():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_res_elec
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_for_res_elec function
    """
    return initial_cumulated_material_requirements_for_res_elec_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_for_res_elec():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_res_elec
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_for_res_elec function
    """
    return total_materials_to_extract_for_res_elec_mt()


_integ_cum_materials_to_extract_for_res_elec = Integ(
    _integ_input_cum_materials_to_extract_for_res_elec,
    _integ_init_cum_materials_to_extract_for_res_elec,
    "_integ_cum_materials_to_extract_for_res_elec",
)


@subs(["materials"], _subscript_dict)
def _integ_init_cum_materials_to_extract_for_res_elec_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_res_elec_from_2015
    Limits: None
    Type: setup
    Subs: ['materials']

    Provides initial conditions for cum_materials_to_extract_for_res_elec_from_2015 function
    """
    return initial_cumulated_material_requirements_for_res_elec_1995()


@subs(["materials"], _subscript_dict)
def _integ_input_cum_materials_to_extract_for_res_elec_from_2015():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for cum_materials_to_extract_for_res_elec_from_2015
    Limits: None
    Type: component
    Subs: ['materials']

    Provides derivative for cum_materials_to_extract_for_res_elec_from_2015 function
    """
    return total_materials_to_extract_for_res_elec_from_2015_mt()


_integ_cum_materials_to_extract_for_res_elec_from_2015 = Integ(
    _integ_input_cum_materials_to_extract_for_res_elec_from_2015,
    _integ_init_cum_materials_to_extract_for_res_elec_from_2015,
    "_integ_cum_materials_to_extract_for_res_elec_from_2015",
)


_ext_constant_materials_for_om_per_capacity_installed_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_for_om_per_capacity_installed_res_elec*",
    {
        "RES elec": _subscript_dict["RES ELEC MAINTENANCE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    "_ext_constant_materials_for_om_per_capacity_installed_res_elec",
)


_ext_constant_materials_per_new_capacity_installed_res = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_capacity_installed_res*",
    {
        "RES ELEC MAINTENANCE": _subscript_dict["RES ELEC MAINTENANCE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    "_ext_constant_materials_per_new_capacity_installed_res",
)


_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_hvdcs*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs",
)


_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_material_overgrid_high_power*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power",
)
