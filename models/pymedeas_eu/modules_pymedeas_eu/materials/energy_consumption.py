"""
Module energy_consumption
Translated using PySD version 2.2.1
"""


@subs(["materials"], _subscript_dict)
def energy_cons_per_unit_of_material_cons_for_res_elec():
    """
    Real Name: Energy cons per unit of material cons for RES elec
    Original Eqn: recycling rates minerals alt techn[materials]*"Initial energy cons per unit of material cons (recycled)"[materials]+(1-recycling rates minerals alt techn[materials])*"Initial energy cons per unit of material cons (virgin)"[materials]
    Units: MJ/kg
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Average energy consumption per unit of material consumption accounting for recycling
        rates for RES elec technologies.        recycling rates minerals RES elec[materials]*"Initial energy cons per unit
        of material cons (recycled)"[materials]+(1-recycling rates minerals RES
        elec[materials])*"Initial energy cons per unit of material cons
        (virgin)"[materials]
    """
    return (
        recycling_rates_minerals_alt_techn()
        * initial_energy_cons_per_unit_of_material_cons_recycled()
        + (1 - recycling_rates_minerals_alt_techn())
        * initial_energy_cons_per_unit_of_material_cons_virgin()
    )


@subs(["materials"], _subscript_dict)
def energy_required_for_material_consumption_for_ev_batteries():
    """
    Real Name: Energy required for material consumption for EV batteries
    Original Eqn: materials required for EV batteries Mt[materials]*Energy cons per unit of material cons for RES elec [materials]*kg per Mt/MJ per EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Energy required for material consumption for EV batteries.
    """
    return (
        materials_required_for_ev_batteries_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def energy_required_for_material_consumption_for_new_res_elec():
    """
    Real Name: Energy required for material consumption for new RES elec
    Original Eqn: materials required for new RES elec Mt[RES elec,materials]*Energy cons per unit of material cons for RES elec[materials]*kg per Mt/MJ per EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Energy required for material consumption for new RES elec.
    """
    return (
        materials_required_for_new_res_elec_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def energy_required_for_material_consumption_for_om_res_elec():
    """
    Real Name: "Energy required for material consumption for O&M RES elec"
    Original Eqn: "materials required for O&M RES elec Mt"[RES elec,materials]*Energy cons per unit of material cons for RES elec[materials]*kg per Mt/MJ per EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']


    """
    return (
        materials_required_for_om_res_elec_mt()
        * energy_cons_per_unit_of_material_cons_for_res_elec()
        * kg_per_mt()
        / mj_per_ej()
    )


@subs(["RES elec", "materials"], _subscript_dict)
def energy_required_for_material_consumption_per_res_elec():
    """
    Real Name: Energy required for material consumption per RES elec
    Original Eqn: "Energy required for material consumption for O&M RES elec"[RES elec,materials] +Energy required for material consumption for new RES elec[RES elec, materials]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec', 'materials']

    Energy required for material consumption per material per RES elec
        technologies.
    """
    return (
        energy_required_for_material_consumption_for_om_res_elec()
        + energy_required_for_material_consumption_for_new_res_elec()
    )


@subs(["materials"], _subscript_dict)
def initial_energy_cons_per_unit_of_material_cons_recycled__data():
    """
    Real Name: "Initial energy cons per unit of material cons (recycled) - data"
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'initial_energy_cons_per_material_recycled*')
    Units: MJ/kg
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Energy consumption required to use recycled materials per unit of material
        consumption. This variable has 0s for those materials for which
        information was not found.
    """
    return _ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled__data()


@subs(["materials"], _subscript_dict)
def initial_energy_cons_per_unit_of_material_cons_recycled():
    """
    Real Name: "Initial energy cons per unit of material cons (recycled)"
    Original Eqn: IF THEN ELSE("Initial energy cons per unit of material cons (recycled) - data"[materials]=0,"Initial energy cons per unit of material cons (virgin)"[materials], "Initial energy cons per unit of material cons (recycled) - data"[materials])
    Units: MJ/kg
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Energy consumption required to use recycled materials per unit of material
        consumption. When data for recycled materials was not available, the
        energy consumption for virgin materials was assumed.
    """
    return if_then_else(
        initial_energy_cons_per_unit_of_material_cons_recycled__data() == 0,
        lambda: initial_energy_cons_per_unit_of_material_cons_virgin(),
        lambda: initial_energy_cons_per_unit_of_material_cons_recycled__data(),
    )


@subs(["materials"], _subscript_dict)
def initial_energy_cons_per_unit_of_material_cons_virgin():
    """
    Real Name: "Initial energy cons per unit of material cons (virgin)"
    Original Eqn: GET DIRECT CONSTANTS('../materials.xlsx', 'Global', 'initial_energy_cons_per_material_virgin*')
    Units: MJ/kg
    Limits: (None, None)
    Type: constant
    Subs: ['materials']

    Energy consumption required to extract and use virgin materials per unit
        of material consumption.
    """
    return _ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin()


def mj_per_ej():
    """
    Real Name: MJ per EJ
    Original Eqn: 1e+12
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1e12


def share_energy_for_material_consumption_for_alt_techn_vs_tfec():
    """
    Real Name: share energy for material consumption for alt techn vs TFEC
    Original Eqn: TFE required for total material consumption for alt techn/Real TFEC
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of energy requirements for alternative technologies (RES elec & EV
        Batteries) vs TFES.
    """
    return tfe_required_for_total_material_consumption_for_alt_techn() / real_tfec()


def tfe_required_for_total_material_consumption_for_alt_techn():
    """
    Real Name: TFE required for total material consumption for alt techn
    Original Eqn: Total energy required for material consumption for RES elec+Total energy required for total material consumption for EV batteries
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy required for total material consumption for alternative
        technologies (RES elec & EV Batteries).
    """
    return (
        total_energy_required_for_material_consumption_for_res_elec()
        + total_energy_required_for_total_material_consumption_for_ev_batteries()
    )


def total_energy_required_for_material_consumption_for_res_elec():
    """
    Real Name: Total energy required for material consumption for RES elec
    Original Eqn: SUM(Energy required for material consumption per RES elec[RES elec!,materials!] )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total energy required for material consumption for RES elec.
    """
    return sum(
        energy_required_for_material_consumption_per_res_elec(),
        dim=("RES elec", "materials"),
    )


@subs(["RES elec"], _subscript_dict)
def total_energy_required_for_material_consumption_per_res_elec():
    """
    Real Name: Total energy required for material consumption per RES elec
    Original Eqn: SUM(Energy required for material consumption per RES elec[RES elec,materials!] )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Total energy required for material consumption per RES elec
    """
    return sum(
        energy_required_for_material_consumption_per_res_elec(), dim=("materials",)
    )


def total_energy_required_for_total_material_consumption_for_ev_batteries():
    """
    Real Name: Total energy required for total material consumption for EV batteries
    Original Eqn: SUM(Energy required for material consumption for EV batteries[materials!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total energy required for total material consumption for EV batteries.
    """
    return sum(
        energy_required_for_material_consumption_for_ev_batteries(), dim=("materials",)
    )


@subs(["materials"], _subscript_dict)
def total_energy_required_per_material_for_alt_techn():
    """
    Real Name: Total energy required per material for alt techn
    Original Eqn: SUM(Energy required for material consumption per RES elec[RES elec!,materials] )+Energy required for material consumption for EV batteries[materials]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: ['materials']

    Total energy required for total material consumption per material for
        alternative technologies (RES elec & EV Batteries).
    """
    return (
        sum(energy_required_for_material_consumption_per_res_elec(), dim=("RES elec",))
        + energy_required_for_material_consumption_for_ev_batteries()
    )


_ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled__data = (
    ExtConstant(
        "../materials.xlsx",
        "Global",
        "initial_energy_cons_per_material_recycled*",
        {"materials": _subscript_dict["materials"]},
        _root,
        "_ext_constant_initial_energy_cons_per_unit_of_material_cons_recycled__data",
    )
)


_ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin = ExtConstant(
    "../materials.xlsx",
    "Global",
    "initial_energy_cons_per_material_virgin*",
    {"materials": _subscript_dict["materials"]},
    _root,
    "_ext_constant_initial_energy_cons_per_unit_of_material_cons_virgin",
)
