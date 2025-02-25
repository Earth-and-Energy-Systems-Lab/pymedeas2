"""
Module transport.transport_energy_demand
Translated using PySD version 3.14.0
"""

@component.add(
    name="Share_demand_by_fuel_in_transport",
    units="Dmnl",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_transport_fed_by_fuel": 1, "transport_tfed": 1},
)
def share_demand_by_fuel_in_transport():
    """
    Share demand by fuel in transport
    """
    return total_transport_fed_by_fuel() / transport_tfed()


@component.add(
    name="Total_transport_FED_by_fuel",
    units="EJ/year",
    subscripts=[np.str_("final_sources")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_final_energy_by_sector_and_fuel_eu": 1,
        "transport_fraction": 1,
        "transport_households_final_energy_demand": 1,
    },
)
def total_transport_fed_by_fuel():
    """
    Total energy in transport. This model considers transport the four sector in WIOD related with transport and households transport.
    """
    return (
        sum(
            required_final_energy_by_sector_and_fuel_eu().rename(
                {np.str_("sectors"): "sectors!"}
            )
            * transport_fraction().rename({np.str_("sectors"): "sectors!"}),
            dim=["sectors!"],
        )
        + transport_households_final_energy_demand()
    )


@component.add(
    name="transport_fraction",
    units="Dmnl",
    subscripts=[np.str_("sectors")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_transport_fraction"},
)
def transport_fraction():
    return _ext_constant_transport_fraction()


_ext_constant_transport_fraction = ExtConstant(
    "../economy.xlsx",
    "Global",
    "transport_fraction",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_transport_fraction",
)


@component.add(
    name="Transport_TFED",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_transport_fed_by_fuel": 1},
)
def transport_tfed():
    """
    Total Final Energy demand in transport
    """
    return sum(
        total_transport_fed_by_fuel().rename(
            {np.str_("final_sources"): "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name="Transport_TFED_energy_intensity",
    units="EJ/Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"transport_tfed": 1, "gdp_eu": 1, "nvs_1_year": 1},
)
def transport_tfed_energy_intensity():
    return zidz(transport_tfed(), gdp_eu()) * nvs_1_year()
