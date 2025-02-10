# Los Angeles Heat Emergency Research
In partnership with the Los Angeles Climate Emergency Management Office (CEMO) we sought to assess the impact of extreme heat events on health emergencies in the city of Los Angeles. This Github Repository contains the code used in our analysis and research. This project was completed in partial fulfilment of the requiremtns for the Master of Urban and Regional Planning Degree at the UCLA Luskin School of Public Affairs for the individuals listed in the [roles](#roles) section below.
The final results of our analysis can be found chapter 1 of [this report](https://innovation.luskin.ucla.edu/wp-content/uploads/2023/06/CEMO-Comprehensive-Project-Report.pdf).

In our report we find that there is a correlation between extreme heat and call volumes for emergency services and estimate the number excess emergency calls that occur due to heat events. To do this we performed an analysis that estimated a daily heat index across the city of Los Angeles using air temperatures and relative humidity recorded daily at the weather stations shown in the map below:
![Map of Weather Stations in Los Angeles](./Final%20Graphics/statipons.png)

We then interpolated these readings to assess the daily heat index in each fire  district and assessed which days qualified as "Heat Events" — days where there were two or more consecutive days with a heat index over a set threshold (with thresholds 90, 95, and 100 degrees Farenheit explored). We were then able to compare the typical call volumes during heat and non-heat days in each fire district as well as city wide, determining that heat events typically see higher call volumes for emergency services than non heat events, with the average call volumes rising as the threshold for a heat event rises.

![Call Volumes during Heat Events and Non-heat Events](./Final%20Graphics/Call%20Distribution.svg)

A detailed flow chart of the data processing methodology can be found below:

![Data Processing Flow Chart](./Final%20Graphics/flowchart.png)

## Code Review and Replication Guide
If you would like to review the code and methodology used in this analysis we recommend working in the following order. This reflects the core of our analysis and other files are useful, but suplementary. Core functions used throughout this repository and their documentation can be found in `cemo_functions.py`.
- [Heat_Analysis > 01_Mesonet_Pull.ipynb](./Heat_Analysis/01_Mesonet_Pull.ipynb) — Pulls air temperature and relative humidity readings from the Mesonet API and calculates the heat index for weather stations.
- [Heat_Analysis > 02_Heat_Interpolation_Clean.ipynb](./Heat_Analysis/02_Heat_Interpolation_Clean.ipynb) — Develops and utilizes geospatial interpolation to identify heat index by fire district from point features.
- [911 Analysis > 01_ExploratoryResults.ipynb](./911%20Analysis/01_ExploratoryResults.ipynb) — Performs intial calculations to identify heat events and explore correlations between heat and call volumes.
- [911 Analysis > 02_Sensitivity_Tests.ipynb](./911%20Analysis/02_Sensitivity_Tests.ipynb) — Explores impact of variations in temperature thresholds on call volumes and sample size.
- [911 > 03_Excess Call Calculations.ipynb](./911%20Analysis/03_Excess%20Call%20Calculations.ipynb) — Calculates typical call volumes and estimates the number of excess calls due to heat


## Roles
| Author | Role |
|--------|------|
| Emma Ramirez | Team Leader & Emergency Systems Research |
| Seth Reichert | Lead Data Scientist — Heat Analysis and Emergency Call Analysis |
|Tiffany Rivera| Data Scientist — 311 Calls and Equity Analysis|
|George Karam|Graphic Designer|

