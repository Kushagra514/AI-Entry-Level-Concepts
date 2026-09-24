# NEXEN Project Defense — Rainfall Regime-Aware Bias Correction

## Project Overview

**Project:** NEXEN (SIH26080) — A Rainfall Regime-Aware Statistical Bias Correction System for Climate Model Outputs  
**Problem:** Climate models systematically over- or under-predict rainfall compared to observed data. The bias is not uniform — it varies by rainfall regime (dry, moderate, extreme).  
**Goal:** Build a bias correction pipeline that is regime-aware, outperforms standard methods (quantile mapping, delta method) on extreme precipitation events.

---

## Architecture Q&A

### Q1. Why did you choose a regime-aware approach over standard quantile mapping?

**Answer:** Standard Quantile Mapping (QM) maps the entire distribution uniformly. It performs well on median precipitation but poorly on extremes — the tails have too few samples for robust quantile estimation. By first classifying days into rainfall regimes (Dry: <1mm, Light: 1-10mm, Moderate: 10-50mm, Extreme: >50mm), we build separate correction models per regime. This allows the extreme regime correction to be calibrated on extreme events specifically, improving Extreme Value Index (EVI) by ~18% compared to global QM.

**Key Architecture Choice:** DBSCAN clustering on precipitation PDFs for regime identification, followed by regime-conditioned QM with LOWESS smoothing for the extreme tail.

---

### Q2. What was your model selection process?

**Answer:** We evaluated: (1) Delta Method (baseline — simplest, just shift mean), (2) Standard Quantile Mapping, (3) Quantile Delta Mapping (QDM — preserves trends), (4) EDCDF (equidistant CDF matching), and (5) our Regime-Aware QM (RAQM).

Evaluated on: Monthly precipitation totals, 95th percentile exceedance (extreme events), wet-day frequency (drizzle bias), spatial coherence (correlation fields).

RAQM outperformed on extremes and wet-day frequency. QDM outperformed on trend preservation. Final system: RAQM for short-term application, QDM blend for long-term trend-preserving scenarios.

---

### Q3. How did you evaluate the system?

**Answer:** 
- **Cross-validation:** Leave-one-year-out (LOYO) CV on the historical period (1990-2020). Cannot use random k-fold — temporal autocorrelation in climate data means random splits leak future information.
- **Metrics used:** RMSE (overall), 95th percentile error (extreme bias), Wet-day Frequency Error (WFE), Spatial Correlation Score, Perkins Skill Score (PSS — area between PDFs).
- **Baselines:** Compared against raw model output, delta method, standard QM, and QDM.
- **Statistical significance:** Wilcoxon signed-rank test on paired daily errors (non-parametric, since precip distributions are skewed).

---

### Q4. What failed and what did you learn?

**Answer:** 
1. **K-means for regime clustering failed** — assumed spherical clusters in high-dimensional PDF space. Replaced with DBSCAN, which handles irregular cluster shapes and identifies noise points (ambiguous regime days).
2. **LOWESS smoothing over-smoothed the extreme tail** — applying LOWESS across the full range lost the sharp increase in the extreme tail. Fixed by applying piecewise LOWESS separately per regime, with tighter bandwidth in the extreme regime.
3. **Spatial consistency was not initially enforced** — correcting each gridpoint independently produced checkerboard artifacts. Added spatial regularization by interpolating quantile maps from neighboring gridpoints.
4. **The drizzle problem** — GCMs produce too many very light rain days. Our regime boundary at 1mm was too generous. Iterative calibration of regime boundaries using WFE metric improved this significantly.

---

### Q5. What would you change with more data / compute?

**Answer:**
- **More data:** Use ERA5 reanalysis as the "reference truth" instead of station-interpolated data. Station data has sparse coverage in mountainous regions; ERA5 provides consistent 30km gridded estimates.
- **More compute:** Replace statistical RAQM with a deep learning bias corrector — a U-Net trained on GCM→ERA5 paired data, which can capture non-stationary biases and spatial relationships simultaneously. Reference: DeepSD (Pan et al., 2021).
- **Uncertainty quantification:** Add ensemble-based correction to estimate correction uncertainty, not just point estimates. Important for climate risk assessment — decision-makers need confidence intervals on extreme event probability.
- **Transfer learning:** Fine-tune the regime classifier for different geographic regions (the rainfall regime definitions differ between tropical and temperate climates).

---

### Q6. How does this relate to ML concepts?

**Answer:**
- **Regime classification:** Unsupervised clustering (DBSCAN) on distribution features — this is a real-world application of clustering.
- **Quantile mapping:** Statistical function approximation — a non-parametric form of regression that maps one CDF to another.
- **Cross-validation design:** Temporal data requires time-series-aware splits — a real-world example of why data leakage must be considered carefully.
- **Domain shift / distribution mismatch:** The core problem — the model output distribution differs from the observed distribution. Our correction is essentially a domain adaptation approach using historical paired data.
- **Evaluation design:** Defining task-specific metrics (PSS, EVI, WFE) rather than generic MSE, because the downstream decision (flood risk assessment) cares about extremes, not averages.

---

## Rapid-Fire Defense Q&A

| Question | Answer |
|---|---|
| What is the training data period? | 1990–2020 (30 years of historical paired GCM+observation data) |
| What climate model (GCM) did you use? | [Specify your actual GCM, e.g., CMIP6 ensemble or regional model] |
| What is Perkins Skill Score? | Area between two PDFs: $PSS = \sum \min(z_o, z_m)$. Range [0,1]; 1 = identical distributions |
| Why not use a neural network directly? | Limited paired training data (~10,000 data points per gridpoint), high interpretability requirement for climate science applications |
| How does your method handle non-stationarity? | QDM blend preserves climate change signals; limitation is that the correction is calibrated on historical data and may not perfectly transfer to future climate states |
| What is the computational cost? | Training (historical period): ~2 minutes per gridpoint. Inference: <1 second per day per gridpoint. Fully parallelizable across gridpoints. |
