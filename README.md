[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Assimila/ClimateRiskDisclosure/master?filepath=src)

## Assimila -- Climate Risk Disclosure multivariate analysis demo

This is a demo of how the use [ERA5](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5) data and MODIS data to find extreme events, defined as dates where the observations are above the 90th or below the 10th percentile, these areas will be shown as shaded areas.

- The demo shows the ERA5 2m temperature, total precipitation, wind power for Europe and the US from 1979 to 2019 and MODIS LAI monthly averages for the US and Europe from 2002 to 2019.
- The upper panel depicts the standarised anomalies as the number of standard deviations that the observations depart from the climatology.
- The lower panel shows total precipitation the time series

#### How to use it.

- Click on [![here](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Assimila/ClimateRiskDisclosure/master?filepath=src) to launch the Binder environment and then select one of the following Jupyter Notebooks:
  - For multivariate analysis:
    - Assimila_ERA5_anomalies_analysis_Europe.ipynb
    - Assimila_ERA5_MODIS_LAI_anomalies_analysis_Europe.ipynb
    - Assimila_ERA5_anomalies_analysis_US.ipynb
  - For univariate analysis:
    - t2m.ipynb
    - total_precipitation.ipynb
    - wind_power.ipynb
