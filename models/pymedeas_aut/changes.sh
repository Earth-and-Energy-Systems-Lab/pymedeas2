sed -i 's/lambda: share_e_losses_cc()/lambda: share_e_losses_cc(time())/' pymedeas_aut.py

variables2replace=("total_extraction_nre_ej" "pes_oil_ej"
"pes_nat_gas" "share_conv_vs_total_gas_extraction"
"share_conv_vs_total_oil_extraction" "annual_gdp_growth_rate"
"abundance_total_nat_gas" "abundance_coal"
"abundance_total_oil" "extraction_coal_ej"
"extraction_uranium_ej" "real_demand_by_sector"
"real_total_output_by_sector" "real_final_energy_by_sector_and_fuel"
"total_fe_elec_generation_twh_eu" "gdp_eu" 
"annual_gdp_growth_rate_eu" "real_final_demand_by_sector_eu"
"real_total_output_by_sector_eu" "real_final_energy_by_sector_and_fuel_eu")

for variable in ${variables2replace[@]}; do
    sed -i "s/return $variable()/return $variable(time())/" pymedeas_aut.py
done
