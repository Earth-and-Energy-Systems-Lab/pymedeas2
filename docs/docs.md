---
title: 'Documentation for the pymedeas models'
tags:
  - Python
  - System Dynamics
  - Integrated Assessment Models
  - Biophisical limits

authors:
  - name: Eneko Martin-Martínez'co-first author'
    orcid: 0000-0002-9213-7818
    affiliation: 1
  - name: Roger Samsó
    orcid: 0000-0003-0348-3047
    affiliation: 1
  - name: Enric Alcover
    orcid: #TODO
    affiliation: 1
  - name: Jordi Solé
    orcid: 0000-0002-2371-1652
    affiliation: "1, 2"
affiliations:
 - name: Centre for Ecological Research and Forestry Applications (CREAF)
   index: 1
 - name: Department of Earth and Ocean Dynamics, Faculty of Earth Sciences, University of Barcelona
   index: 2
date: 20 January 2022
bibliography: references.bib

---



# General logic of the pymedeas models

The MEDEAS models dynamically operate as follows: for each
period, a sectoral economic demand is estimated from exogenous
pathways of expected Gross Domestic Product per capita  (GDPpc) and population evolution. The final energy demand required to fulfil production is obtained using energy-economy hybrid input-output analysis, and energy intensities by type of final energy. The energy sub-module computes the available final energy supply, which may or may not satisfy demand, adapting the economic production to the available energy. The materials required by the economy, with emphasis on those
required by alternative green technologies, are estimated; this allows to
assess eventual future mineral bottlenecks. The new energy infrastructure requires energy investments, whose computation allows to estimate
the variation of the EROI (Energy Return over Energy Invested) of the
system, which in turn affects the final energy demand. The climate sub-
module computes the greenhouse gas (GHG) emissions associated to the
resulting energy mix (complemented by exogenous pathways for non-energy emissions), which feeds back to the economy, affecting final
demand. Additional land requirements are accounted for. Finally, the
social and environmental impacts are computed. For more detail the
reader is referred to Refs. --> **all this is taken from [@SAMSO2020100582] and needs to be either cited or modified**

# Main hypothesis behind the pymedeas models
blah blah blah

# Main features of the pymedeas models

## Modules
The pymedeas models are structured in the following modules.

### Energy
This module is in charge of the estimation of energy demand, the enrgy supply, the energy resource availability, the modelling of electricity and heat generation and the modelling of non-energy use. The module is diveded in 6 submodules:

- Availability
- Supply
- Demand
- Consumption
- Storage
- EROI

##### Availabiliy
This submodule calculates the availability of non-renewable energy sources: oil, natural gas, coal and uranium.

**Oil Extraction**

This view takes into account the limitation of the oil resources, and models availability of oil depending on two constraints: the stock (EJ) and the flows (Watts). The model priorizes the others NRE liquids fuels, then the oil demand is obtained as follows:

```math
Oil\_demand=PED\_NRE\_Liquids-FES_{CTL}- FES_{GTL}- ORF
```
Where PED_NRE_Liquieds is the Primary energy demand of non-renewable eneregy liquids (EJ), FES_GTL is the final energy demand of GTL (Gas-to-liquids) (EJ),  FES_CTL is the final energy demand of GTL (Coal-to-liquids) (EJ) and ORF is the oil refinery gains. 


**Coal extraction**

This view is in charge of obtaining the coal extraction taking into account the limitations of the coal resources. The model priorizes other solid NRE sources for satisfying the primary energy demand.

```math
Coal_{demand}=PED_{solids}-PE_{trad\_bio}-PES_{peat}-PES_{waste}-LCP
```
Where, PED_solids is the primary energy demand of the solids (EJ), PE_trad_bio is the primary energy of the traditional biomass (EJ), PES_peat is the Primary energy suplly of peat (EJ), PES_waste is the primary energy obtained from waste (EJ) and LCP are the losses in charcoal plants (EJ).

The amount of coal that can be extracted is limited by the Hubbert curves if the parameters *unlimited coal?* and *unlimited NRE?* are desactivated. Then, the extraction of coal is limited by the maximum extraction limit as:

```math
Coal_{extraction}=min(PED_{coal}, max\_extract\_coal))
```
**Uranium extraction**

This view is in charge of calculating the uranium extraction, taking into account the Hubbert curve of maxim extraction of the uranium. The demand of uranium is obtained from the potential generation of nuclear electricity divided by the efficiency of uranium for electricity. If the parameters *unlimited uranium?* and *unlimited NRE?* are desactivated, the extraction of uranium is limited by the maximum extraction limit as:

```math
Uranium_{extraction}=min(PED_{uranium}, max\_extract\_uranium))
```

### Economy
This module does.....
### Climate
This module does.....
### Environment
This module does.....
### Materials
This module does.....
### Society
This module does.....

**Population**

This view calculates the evolution of the population from exogenous drivers. There are three different ways to obtain the population evolution: From SSPs, from timeseries introduced manually or from annual constant variation. In this way, the population growth follows an independent evolution from other variables. 

```diff
- The population submodule has to be revised introducing some limitation on the population growth, that can depend on the GDP, the damage function, etc. 
```
**Social and environmental impacts**

This view relates the biophysicals results with social and environmental indexes. There is a need of indetifying factors that influence social welfare by covering more aspects than only income levels. Thios social welfare indicators are influenced byeconomic variables such as population and GDP, but also connected to climate module.

The first calculated index is the Human Development Index. It has been observed that above certain level of GDP, the HDI decouples from income. Therefore it is important to consider other relations that may explain the HDI evolution. Among these, energy consumption is found to have an importnat relation, so it is used by the model, following the next equation:
```math
HDI=0.1508+0.1395 \cdot ln(TFEC_{pc})
```

```diff
- The correlation of the HDI with the TFEC is not the best approax, it can be approximated by the relation with the Final Energy Footprint per capita (FEFpc) (Deliverable 4.1)
```
Then the carbon footprint per capita and the water use per capita are calculated dividing the total ammounts by the population. Finally, the CO2 emissions per value added is obtained dividing the total CO2 emissions by the GDP.

### Transport
This module does.....

## Nestings
The pymedeas models are organized in three nestings, corresponding to ....
