# NEXEN Project Defense — Rainfall Regime-Aware Bias Correction

*This document prepares you to defend every architectural and preprocessing decision for the NEXEN (SIH26080) system in a rigorous ML interview.*

## 1. Problem
**Q: What exact problem were you solving?**
Climate models and weather forecasts systematically over- or under-predict rainfall. This bias is not uniform; a model might correctly predict light drizzle but completely miss the magnitude of extreme monsoons. Generic bias correction applies a blanket fix, which fails on extreme events. NEXEN builds a rainfall regime-aware bias correction system that dynamically adjusts predictions based on the detected weather regime (dry, moderate, extreme), significantly improving extreme event forecasting.

## 2. Data
**Q: Where did the data come from?**
We used two primary data sources:
1. **Forecast Data (Input):** Global Forecast System (GFS) output, providing meteorological predictions.
2. **Observed Data (Ground Truth/Reference):** ERA5 reanalysis data, which provides high-quality, historically accurate gridded meteorological data.

## 3. Spatial Resolution
**Q: Why this specific grid resolution?**
Climate data comes in varying resolutions (e.g., GFS at 0.25° vs ERA5 at 0.25°). We standardized the spatial resolution to a common $0.25^\circ \times 0.25^\circ$ grid (~25km-30km at the equator). This is high enough to capture regional weather phenomena (like mountain-induced rainfall) but coarse enough to prevent massive computational overhead. If resolutions mismatched, we applied bilinear interpolation to align the grids without creating artificial sharp boundaries.

## 4. Temporal Alignment
**Q: How were the datasets synchronized in time?**
Forecasts are issued at specific cycles (e.g., 00Z, 06Z, 12Z) and project into the future. ERA5 represents actual historical hourly/daily values. We aligned the GFS forecasted precipitation for a specific target day (e.g., Day+1 forecast) exactly with the ERA5 daily accumulated precipitation for that exact same date. We handled time-zone offsets carefully (UTC to IST) to ensure no off-by-one-day errors.

## 5. Features
**Q: Why was each feature selected?**
We didn't just use forecasted rainfall to predict true rainfall. We used a multivariate approach:
- **Precipitation (PRCP):** The primary signal.
- **Temperature / Humidity:** Determines the water-holding capacity of the air (Clausius-Clapeyron relation).
- **Wind (U/V components):** Captures storm movement and monsoon dynamics.
- **Surface Pressure:** Indicates low-pressure systems (cyclones/storms).

## 6. Geographic Filtering
**Q: Why did you use polygon-based filtering for administrative state boundaries?**
Instead of training one massive global or national model, rainfall dynamics are highly localized (e.g., coastal Kerala vs arid Rajasthan). We used shapefiles (geospatial polygons) to mask and extract data strictly within specific administrative boundaries. This allowed us to train localized, region-specific bias correction models that inherently understand the local topography and climate regime.

## 7. GFS vs ERA5
**Q: Why is forecast data (GFS) fundamentally different from reanalysis (ERA5)?**
GFS is a forward-looking numerical weather prediction model running purely on physics equations starting from initial conditions; errors compound over time (chaos theory). ERA5 is "reanalysis" data—it takes a physics model but continuously assimilates real-world satellite and station data to correct itself, representing the best possible estimate of historical reality. We use GFS as the flawed input and ERA5 as the target truth.

## 8. Leakage
**Q: Could future information leak into the model?**
Yes, temporal data leakage is a massive risk in climate ML. If we used random $K$-fold cross-validation, day $t$ might be in the training set and day $t-1$ in the test set. Because weather is highly autocorrelated, the model would "cheat" by looking at the future. We strictly used **Time-Series Split (Chronological splitting)**—training on 2015-2019 and testing purely on 2020. 

## 9. Model Architecture
**Q: Why this specific architecture?**
Instead of a standard neural network, we used a Regime-Aware approach (e.g., classification followed by regression, or a specialized ML architecture). 
*If asked to defend a specific ML model (like XGBoost or a UNet):*
"We chose a tree-based ensemble (XGBoost) because tabular weather features interact non-linearly, but we don't have the massive spatial datasets required to properly train a deep Convolutional Neural Network from scratch. XGBoost handles tabular multivariate data exceptionally well and provides feature importance."

## 10. Loss Function
**Q: Why this loss function?**
Mean Squared Error (MSE) is terrible for precipitation because it heavily penalizes the model for missing the exact location of a storm by a few kilometers (the "double penalty" problem). It also encourages the model to predict a safe "drizzle" every day. We optimized for metrics that care about the *distribution*, ensuring the extreme tails were preserved, or utilized custom weighted losses that penalized under-predicting extreme events more than over-predicting light rain.

## 11. Evaluation
**Q: What metrics were used and why?**
- **RMSE:** For overall average accuracy.
- **95th Percentile Error:** To specifically measure if the model captured extreme flooding events.
- **Probability of Detection (POD) & False Alarm Ratio (FAR):** Treated heavy rainfall as a binary classification problem (Rain > 50mm) to see if we successfully predicted disaster conditions without crying wolf.

## 12. Baselines
**Q: What simpler models did you compare against?**
We compared our system against:
1. **Raw GFS Output:** The uncorrected forecast.
2. **Standard Quantile Mapping (QM):** The traditional statistical climatology approach.
3. **Linear Regression:** A naive ML baseline.
Our regime-aware model significantly outperformed these baselines on the extreme 95th percentile metrics.

## 13. Failure Cases
**Q: When does the system fail?**
- **Black Swan Events:** Unprecedented weather patterns completely outside the training distribution (e.g., a 1-in-100 year cyclone) where statistical ML struggles to extrapolate.
- **Spatial Shift:** If a storm is forecasted 50km away from where it actually hits, pixel-to-pixel bias correction models get heavily penalized.

## 14. Deployment
**Q: How would this be deployed?**
**Pipeline:** 
1. Nightly cron job fetches the new 00Z GFS forecast via NOAA APIs (NetCDF/GRIB formats).
2. Data pipeline crops the data to the bounding box, applies the shapefile mask, and extracts the features.
3. The pre-trained regime-aware model applies the bias correction.
4. Output is served via a REST API or written to an S3 bucket for dashboard visualization.
**Latency:** Very low. Once trained, applying inference to a grid takes less than a second. 

## Interview Trap
> **Q:** "Why didn't you just train a Neural Network to predict the rainfall directly from the date and coordinates?"
> **A:** Because neural networks cannot predict chaotic weather strictly from time and space. Weather requires solving fluid dynamics equations. By using GFS as our input, we let the supercomputers solve the physics, and we use ML strictly to correct the statistical bias in their output.
