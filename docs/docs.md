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
This module does.....
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
### Population
This submodule calculates the evolution of the population from exogenous drivers. There are three different ways to obtain the population evolution: From SSPs, from timeseries introduced manually or from annual constant variation. In this way, the population growth follows an independent evolution from other variables. 

```diff
- The population submodule has to be revised introducing some limitation on the population growth, that can depend on the GDP, the damage function, etc. 
```

### Transport
This module does.....

## Nestings
The pymedeas models are organized in three nestings, corresponding to ....
