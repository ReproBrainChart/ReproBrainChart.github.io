---
title: "Image Curation"
excerpt: "Image Curation"
layout: single

---

[CuBIDS](Reproducible and open science) was used for the curation of each of these datasets.
CuBIDS is a sanity preserving workflow that summarizes the heterogeneity in a MRI BIDS dataset, helps prepare MRI datasets for preprocessing, and helps users perform metadata-based quality control on MRI BIDS data.

<div style="text-align: center;">
    <img src="/assets/images/misc/cubids_workflow.png" width="auto" height="500" />
</div>

<div id="carouselBox" style="background-color: gray; width: 90%; height: 400px; position: relative; display: flex; align-items: center;">
    <div id="carouselDataHarmonization" class="carousel slide carousel-fade" data-interval="5000" data-ride="carousel" style="width: 90%; margin: auto; background-color: gray;">
        <div class="carousel-inner">
            <div class="carousel-item active">
                <img class="d-block mx-auto" style="height: 400px;" src="/assets/images/datasets/Figure_Harmonization_v1_a.png" alt="First slide">
            </div>
            <div class="carousel-item">
                <img class="d-block mx-auto" style="height: 400px;" src="/assets/images/datasets/Figure_Harmonization_v1_b.png" alt="First slide">
            </div>
            <div class="carousel-item">
                <img class="d-block mx-auto" style="height: 400px;" src="/assets/images/datasets/Figure_Harmonization_v1_c.png" alt="Third slide">
            </div>
            <div class="carousel-item">
                <img class="d-block mx-auto" style="height: 400px;" src="/assets/images/datasets/Figure_Harmonization_v1_d.png" alt="Fourth slide">
            </div>
            <div class="carousel-item">
                <img class="d-block mx-auto" style="width: 80%;" src="/assets/images/datasets/Figure_Harmonization_v1_e.png" alt="Fifth slide">
            </div>
            <a class="carousel-control-prev" href="#carouselDataHarmonization" role="button" data-slide="prev" style="width: 10%;">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </a>
            <a class="carousel-control-next" href="#carouselDataHarmonization" role="button" data-slide="next" style="width: 10%;">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="sr-only">Next</span>
            </a>
        </div>
    </div>
</div>

For each dataset, a CuBIDS summary is created that provides an opportunity to evaluate your data and decide how to handle heterogeneity by grouping the scans on the basis of metadata.
You can find the link to each of the CuBIDS summaries for each study below.
More information about how to interpret CuBIDS summaries can be found [here](https://cubids.readthedocs.io/en/latest/).

- [HBN](https://github.com/ReproBrainChart/HBN_BIDS/blob/main/study-HBN_desc-CuBIDS_summary.tsv)
- [NKI](https://github.com/ReproBrainChart/NKI_BIDS/blob/main/study-NKI_desc-CuBIDS_summary.tsv)
- [PNC](https://github.com/ReproBrainChart/PNC_BIDS/blob/main/study-PNC_desc-CuBIDS_summary.tsv)
- [CCNP](https://github.com/ReproBrainChart/CCNP_BIDS/blob/main/study-CCNP_desc-CuBIDS_summary.tsv)
- [BHRC](https://github.com/ReproBrainChart/BHRC_BIDS/blob/main/study-BHRC_desc-CuBIDS_summary.tsv)
