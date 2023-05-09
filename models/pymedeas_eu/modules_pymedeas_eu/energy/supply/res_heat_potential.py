"""
Module energy.supply.res_heat_potential
Translated using PySD version 3.10.0
"""


@component.add(
    name="Geot PE potential for heat EJ",
    units="EJ/Year",
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
    "Europe",
    "geot_PE_potential_heat",
    {},
    _root,
    {},
    "_ext_constant_geot_pe_potential_for_heat_twth",
)


@component.add(
    name="max FE potential biogas for heat",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_pe_biogas_ej": 1,
        "share_pes_biogas_for_heat": 1,
        "efficiency_biogas_for_heat": 1,
    },
)
def max_fe_potential_biogas_for_heat():
    """
    Potential (final energy) of biogas for heat.
    """
    return (
        max_pe_biogas_ej() * share_pes_biogas_for_heat() * efficiency_biogas_for_heat()
    )


@component.add(
    name="Max FE potential RES for heat",
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_fe_res_for_heat": 2,
        "max_pe_potential_solid_bioe_for_heat_ej": 1,
        "efficiency_res_heat": 1,
    },
)
def max_fe_potential_res_for_heat():
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[["solar heat"]] = float(max_fe_res_for_heat().loc["solar heat"])
    value.loc[["geot heat"]] = float(max_fe_res_for_heat().loc["geot heat"])
    value.loc[["solid bioE heat"]] = max_pe_potential_solid_bioe_for_heat_ej() * float(
        efficiency_res_heat().loc["solid bioE heat"]
    )
    return value


@component.add(
    name="Max FE RES for heat",
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_fe_solar_thermal_urban_twth": 1,
        "ej_per_twh": 1,
        "twe_per_twh": 1,
        "max_pe_res_for_heat": 2,
        "efficiency_res_heat": 2,
    },
)
def max_fe_res_for_heat():
    """
    Maximum level of final energy for producing heat from renewables by technology. For technologies solar heat and geot heat this variable corresponds with the maximum potential, but not for solids bioenergy due to the competing use for heat and electricity.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[["solar heat"]] = (
        max_fe_solar_thermal_urban_twth() * ej_per_twh() / twe_per_twh()
    )
    value.loc[["geot heat"]] = float(max_pe_res_for_heat().loc["geot heat"]) * float(
        efficiency_res_heat().loc["geot heat"]
    )
    value.loc[["solid bioE heat"]] = float(
        max_pe_res_for_heat().loc["solid bioE heat"]
    ) * float(efficiency_res_heat().loc["solid bioE heat"])
    return value


@component.add(
    name="max PE potential biogas for heat",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_biogas_ej": 1, "share_pes_biogas_for_heat": 1},
)
def max_pe_potential_biogas_for_heat():
    """
    Primary energy potential of biogas for heat taking into account the current share.
    """
    return max_pe_biogas_ej() * share_pes_biogas_for_heat()


@component.add(
    name="Max PE potential RES for heat",
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_pe_res_for_heat": 2, "max_pe_potential_solid_bioe_for_heat_ej": 1},
)
def max_pe_potential_res_for_heat():
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[["solar heat"]] = float(max_pe_res_for_heat().loc["solar heat"])
    value.loc[["geot heat"]] = float(max_pe_res_for_heat().loc["geot heat"])
    value.loc[["solid bioE heat"]] = max_pe_potential_solid_bioe_for_heat_ej()
    return value


@component.add(
    name="max PE potential tot RES heat EJ",
    units="EJ",
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
        max_pe_potential_res_for_heat().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name="Max PE RES for heat",
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_fe_solar_thermal_urban_twth": 1,
        "efficiency_res_heat": 1,
        "geot_pe_potential_for_heat_ej": 1,
        "available_max_pe_solid_bioe_for_heat_ej": 1,
    },
)
def max_pe_res_for_heat():
    """
    Maximum level of primary energy for producing heat from renewables by technology.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[["solar heat"]] = max_fe_solar_thermal_urban_twth() / float(
        efficiency_res_heat().loc["solar heat"]
    )
    value.loc[["geot heat"]] = geot_pe_potential_for_heat_ej()
    value.loc[["solid bioE heat"]] = available_max_pe_solid_bioe_for_heat_ej()
    return value


@component.add(
    name="Max tot FE potential RES for heat",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_fe_potential_res_for_heat": 1,
        "max_fe_potential_biogas_for_heat": 1,
    },
)
def max_tot_fe_potential_res_for_heat():
    """
    Potential (final energy) for producing heat from renewables.
    """
    return (
        sum(
            max_fe_potential_res_for_heat().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
        + max_fe_potential_biogas_for_heat()
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
