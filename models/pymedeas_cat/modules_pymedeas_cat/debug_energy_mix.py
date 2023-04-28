"""
Module debug_energy_mix
Translated using PySD version 3.9.1
"""


@component.add(
    name="DEBUG FE nuclear Elec generation EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_nuclear_elec_generation_twh": 1, "ej_per_twh": 1},
)
def debug_fe_nuclear_elec_generation_ej():
    return fe_nuclear_elec_generation_twh() * ej_per_twh()


@component.add(
    name="DEBUG net electricity flux",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"importsexports_electricity": 1, "ej_per_twh": 1},
)
def debug_net_electricity_flux():
    return importsexports_electricity() * ej_per_twh()
