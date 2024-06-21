---
title: "Image Processing"
excerpt: "Image Processing"
layout: single

---
The [“FAIRly-big” strategy](https://www.nature.com/articles/s41597-022-01163-2) (Wagner et al., 2021) was adopted for reproducible image processing, ensuring all preparation and analyses were accompanied by a full audit trail in [Datalad](https://www.datalad.org/) (Halchenko et al., 2021).
Structural MRI data were processed using [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) and [sMRIPrep](https://www.nipreps.org/smriprep/), yielding commonly used measures of brain structure
RBC provides full FreeSurfer outputs and structural features in fsLR and fsaverage surface spaces.
In addition, RBC provides tabulated data parcellated using 35 anatomical, functional, and multimodal atlases such as Desikan Killiany, Glasser, Gordon, and multiple Schaefer parcellations.
Specific features include commonly used measures such as regional surface area, cortical thickness, gray matter volume, folding and curvature indices, etc.
Moreover, summary brain measures (e.g., mean and standard deviation of various measures) are provided for the whole brain and per hemisphere.
Tabulated data are also accompanied by .json files describing each structural feature in detail.

Functional data were processed using [C-PAC](https://fcp-indi.github.io/docs/nightly/user/quick) -
or Configurable Pipeline for the Analysis of Connectomes (Craddock et al., 2013).
These steps were all carried out in [Datalad](https://www.datalad.org/) to keep track of provenance and ensure the ultimate reproducibility for all datasets.
Following [extensive benchmarking and harmonization studies](https://www.biorxiv.org/content/10.1101/2021.12.01.470790v3.abstract) (Li et al., 2021), C-PAC was executed using a configuration file that was crafted specifically for RBC, which is available [here](https://github.com/FCP-INDI/C-PAC/blob/0182f98c61cb7fbb495c8300e6a6a7991c859240/CPAC/resources/configs/pipeline_config_rbc-options.yml#L172).
C-PAC outputs include measures such fully-processed functional timeseries, functional connectivity matrices, ReHo (regional homogeneity), ALFF (amplitude of low frequency fluctuation), as well as extensive measures of quality control.
Derivatives are available in volumetric MNI space as well as in parcellated format using 16 different atlases, including Glasser and Schaefer parcellations.
A more detailed description of the list of outputs can be obtained [here](https://fcp-indi.github.io/docs/nightly/user/output_dir).

A repository describing all of the atlases used by C-PAC in RBC can be found [here](https://github.com/FCP-INDI/C-PAC_templates/tree/d2913cd6d5861d9cb5ffb79aa03da18b6eb603eb/sourcedata/atlases).
