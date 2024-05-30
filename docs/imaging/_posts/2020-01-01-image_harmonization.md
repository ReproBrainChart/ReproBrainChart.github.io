---
title: "Image Harmonization"
excerpt: "Image Harmonization"
layout: single

---

RBC provides both raw and processed neuroimaging data (structural and functional MRI) for each dataset. However,  due to differences in scanners and sequences used in data collection, there is significant technical variance that requires harmonization.  As such, users may want to harmonize the data across datasets and data acquisition sites. As part of our initial analyses of RBC data, we have used CovBat-GAM (Johnson et al., 2007; Fortune et al., 2017; 2018; Chen et al., 2022). Specifically, we used the “covfam” function with Generalized Additive Model (GAM) from ComBatFamility in R. The “covfam” function uses CovBat (Correcting Covariance Batch Effects; Chen et al., 2022) to harmonize the mean and covariance of data across multiple batches (e.g., sites, datasets). In our developmental analysis, “datasets” were treated as batches. Covariates included in harmonization included age (as a smooth term), sex, and data quality (i.e., Euler number for structural data and mean FD for functional data); overall psychopathology from the bifactor model was also included in analyses of trans-diagnostic psychopathology.   CovBAT-GAM yields harmonized structural and functional data while preserving the effects of model covariates.

<div style="text-align: center;">
     <img src="/assets/images/misc/function_age_harmonized_website.png" width="100%" height="auto" />
</div>
