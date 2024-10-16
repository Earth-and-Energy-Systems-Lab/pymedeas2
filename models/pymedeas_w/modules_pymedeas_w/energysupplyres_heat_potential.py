"""
Module energysupplyres_heat_potential
Translated using PySD version 3.14.0
"""

@component.add(
    name="FE solar potential for heat",
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_fe_solar_potential_for_heat"},
)
def fe_solar_potential_for_heat():
    """
    Global solar thermal potential. We assume that the primary energy coincides with the final energy. See Technical Report Appendix D.
    """
    return _ext_constant_fe_solar_potential_for_heat()


_ext_constant_fe_solar_potential_for_heat = ExtConstant(
    "../energy.xlsx",
    "World",
    "solar_thermal_pot_FE",
    {},
    _root,
    {},
    "_ext_constant_fe_solar_potential_for_heat",
)


@component.add(
    name="Geot PE potential for heat EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "geot_pe_potential_for_heat_twth": 1,
        "ej_per_twh": 1,
        "twe_per_twh": 1,
    },
)
def geot_pe_potential_for_heat_ej():
    """
    Geothermal potential (primary energy) for producing heat.
    """
    return geot_pe_potential_for_heat_twth() * ej_per_twh() / twe_per_twh()


@component.add(
    name="Geot PE potential for heat TWth",
    units="TWth",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_geot_pe_potential_for_heat_twth"},
)
def geot_pe_potential_for_heat_twth():
    """
    Geothermal primary energy potential for heat.
    """
    return _ext_constant_geot_pe_potential_for_heat_twth()


_ext_constant_geot_pe_potential_for_heat_twth = ExtConstant(
    "../energy.xlsx",
    "World",
    "geothermal_PE_pot_heat",
    {},
    _root,
    {},
    "_ext_constant_geot_pe_potential_for_heat_twth",
)


@component.add(
    name="Max FE potential RES for heat",
    units="EJ/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_potential_res_for_heat": 1, "efficiency_res_heat": 1},
)
def max_fe_potential_res_for_heat():
    """
    Potential (final energy) for producing heat from renewables.
    """
    return max_pe_potential_res_for_heat() * efficiency_res_heat()


@component.add(
    name="max PE potential biogas for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_biogas_ej": 1, "share_pes_biogas_for_heat": 1},
)
def max_pe_potential_biogas_for_heat():
    """
    Primary energy potential of biogas for heat taking into account the current share.
    """
    return max_biogas_ej() * share_pes_biogas_for_heat()


@component.add(
    name="Max PE potential RES for heat",
    units="EJ/year",
    subscripts=[np.str_("RES heat")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_solar_potential_for_heat": 1,
        "geot_pe_potential_for_heat_ej": 1,
        "available_pe_potential_solid_bioe_for_heat": 1,
    },
)
def max_pe_potential_res_for_heat():
    """
    Potential (primary energy) for producing heat from renewables.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, [np.str_("RES heat")]
    )
    value.loc[["solar heat"]] = fe_solar_potential_for_heat()
    value.loc[["geot heat"]] = geot_pe_potential_for_heat_ej()
    value.loc[["solid bioE heat"]] = available_pe_potential_solid_bioe_for_heat()
    return value


@component.add(
    name="max PE potential tot RES heat EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_pe_potential_biogas_for_heat": 1,
        "max_pe_potential_res_for_heat": 1,
    },
)
def max_pe_potential_tot_res_heat_ej():
    """
    Maximum total primary energy potential of RES for heat.
    """
    return max_pe_potential_biogas_for_heat() + sum(
        max_pe_potential_res_for_heat().rename({np.str_("RES heat"): "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name="Percent remaining potential tot RES heat",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"remaining_potential_tot_res_heat": 1},
)
def percent_remaining_potential_tot_res_heat():
    """
    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_heat() * 100


@component.add(
    name="PES tot RES for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
        "pes_tot_biogas_for_heatcom": 1,
    },
)
def pes_tot_res_for_heat():
    """
    Total primary energy supply for generating commercial and non-commercial heat from renewables.
    """
    return (
        sum(
            pes_res_for_heatcom_by_techn().rename({np.str_("RES heat"): "RES heat!"}),
            dim=["RES heat!"],
        )
        + sum(
            pes_res_for_heatnc_by_techn().rename({np.str_("RES heat"): "RES heat!"}),
            dim=["RES heat!"],
        )
        + pes_tot_biogas_for_heatcom()
    )


@component.add(
    name="remaining potential tot RES heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_potential_tot_res_heat_ej": 3, "pes_tot_res_for_heat": 2},
)
def remaining_potential_tot_res_heat():
    """
    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_pe_potential_tot_res_heat_ej() > pes_tot_res_for_heat(),
        lambda: zidz(
            max_pe_potential_tot_res_heat_ej() - pes_tot_res_for_heat(),
            max_pe_potential_tot_res_heat_ej(),
        ),
        lambda: 0,
    )
