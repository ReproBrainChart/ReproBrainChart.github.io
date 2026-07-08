---
title: "How to Get Data"
excerpt: "Get Data"
layout: single
permalink: /docs/get_data

---

<div class="notice--danger notice--lg" markdown="1">
  <b>WARNING!!</b> A TR metadata error affected bandpass filtering in some RBC functional derivatives
  (NOT raw data or structural outputs).
  Impact varies by dataset TR (minimal for TR~1s, larger for TR>2s).
  Affected derivatives have been temporarily removed; corrected versions coming in phases over 3 months.
  For an immediate fix to C-PAC derivatives, you can apply this [patch code](https://github.com/ReproBrainChart/2026FunctionalPatch/tree/main/patch). We have also added a [new release for fMRIPrep + XCP-D derivatives](#fmriprep-xcpd-pipeline-release) as described below.
  Please see [this link](https://gjaxx.r.a.d.sendibm1.com/mk/mr/sh/WCPxRrNLV1LtxMyPT3y1oQhxaYvOr2Of/SZQ42E1kj4hy) for a full description of this issue and our response.
</div>

<a id="fmriprep-xcpd-pipeline-release"></a>
<details class="notice--warning notice--lg" markdown="1">
<summary><b>07/06/2026: fMRIPrep and XCP-D Release</b></summary>
<br>

You can find the FreeSurfer, fMRIPrep and XCP-D derivatives in their corresponding
repositories on GitHub.

The repositories (you can find them all
[here](https://github.com/orgs/ReproBrainChart/repositories)) are named as followed:

 * If you're looking for **fMRIPrep anatomical** (processed with `--anat-only`) and **FreeSurfer** derivatives, the repo will be named `<study>_fMRIPrep-Anat`
 * If you're looking for **fMRIPrep functional** derivatives, the repo will be named `<study>_fMRIPrep-Func`
 * If you're looking for [**FreeSurfer-Post**](https://github.com/PennLINC/freesurfer-post) derivatives, the repo will be named `<study>_FreeSurfer-Post`
 * If you're looking for [**XCP-D**](https://xcp-d.readthedocs.io/en/latest/) derivatives, the repo will be named `<study>_XCP-D`

where `<study>` is replaced with `HBN`, `NKI`, `PNC`, `BHRC` or `CCNP`.

<details class="notice--primary" markdown="1">
<summary><b>Download data</b></summary>
<br>

Clone the repository, then use `datalad get` to retrieve file contents:

```bash
# Clone with HTTPS
datalad clone https://github.com/ReproBrainChart/<study>_<pipeline>.git

# Or clone with SSH
datalad clone git@github.com:ReproBrainChart/<study>_<pipeline>.git

# Example: clone the HBN XCP-D repository
datalad clone https://github.com/ReproBrainChart/HBN_XCP-D.git

# Then enter the repository
cd HBN_XCP-D

# Download specific files
datalad get sub-*/ses-*/func/*fsLR_den-91k_desc-denoised_bold.dtseries.nii
```

</details>

**Boilerplate** detailing processing steps is available in each repository at `logs/CITATION.md`.

<details markdown="1">
<summary><b>fMRIPrep anat only</b> command</summary>

```bash
singularity run --cleanenv \
    -B "${PWD}" \
    -B "code/license.txt:/SGLR/FREESURFER_HOME/license.txt" \
    containers/.datalad/environments/fmriprep-<version>/image \
    inputs/data/BIDS \
    outputs/fmriprep_anat \
    participant \
    -w "${PWD}/.git/tmp/wkdir" \
    --stop-on-first-crash \
    --fs-license-file /SGLR/FREESURFER_HOME/license.txt \
    --output-spaces MNI152NLin6Asym:res-1 \
    --force-bbr \
    --skip-bids-validation \
    -vv \
    --anat-only \
    --cifti-output 91k \
    --n_cpus 9 \
    --mem-mb 14000 \
    --bids-filter-file "${session-filterfile}" \
    --participant-label "${subid}"
```
</details>

<details markdown="1">
<summary><b>fMRIPrep func</b> command</summary>

```bash
singularity run --cleanenv \
    -B "${PWD}" \
    -B "code/license.txt:/SGLR/FREESURFER_HOME/license.txt" \
    containers/.datalad/environments/fmriprep-<version>/image \
    inputs/data/BIDS \
    outputs/fmriprep_func \
    participant \
    -w "${PWD}/.git/tmp/wkdir" \
    --stop-on-first-crash \
    --fs-license-file /SGLR/FREESURFER_HOME/license.txt \
    --output-spaces func T1w MNI152NLin6Asym:res-2 \
    --force-bbr \
    --skip-bids-validation \
    -vv \
    --cifti-output 91k \
    --n_cpus 4 \
    --mem-mb 30000 \
    --fs-subjects-dir inputs/data/fmriprep_anat/fmriprep_anat/sourcedata/freesurfer \
    --bids-filter-file "${session-filterfile}" \
    --participant-label "${subid}"
```
</details>

<details markdown="1">
<summary><b>XCP-D</b> command</summary>

```bash
singularity run --cleanenv \
    -B ${PWD} \
    -B code/license.txt:/SGLR/FREESURFER_HOME/license.txt \
    containers/.datalad/environments/xcpd-0-10-6/image \
    inputs/data/fmriprep_func/fmriprep_func \
    outputs/xcpd \
    participant \
    -w ${PWD}/.git/tmp/wkdir \
    --stop-on-first-crash \
    --fs-license-file /SGLR/FREESURFER_HOME/license.txt \
    -vv \
    --mode linc \
    --dummy-scans auto \
    --input-type fmriprep \
    --nthreads 8 \
    --omp-nthreads 8 \
    --mem-gb 50 \
    --atlases 4S1056Parcels 4S156Parcels 4S256Parcels 4S356Parcels 4S456Parcels 4S556Parcels 4S656Parcels 4S756Parcels 4S856Parcels 4S956Parcels Glasser Gordon HCP MIDB Tian \
    --participant-label "${subid#sub-}"
```
</details>

<br>

The following **QC files** are available in each repository:

 * `study-<study>_desc-T1_qc.tsv`
 * `study-<study>_desc-func_qc.tsv`
</details>

### Install DataLad

RBC is accessible via `datalad`. Follow the instructions [here](https://www.datalad.org/#install)
to get it installed.

Accessing RBC data via DataLad happens in two steps. You will first `clone` a RBC data
repository from github. This will make a copy of the RBC file layout, but none of the
actual data will be present. The next step is to `get` your data, which tells DataLad to
download the content of specific files to your copy. Once the file content is present in
your copy, you can use RBC data just like any other set of files.


### Pick a dataset

You can find each of the unprocessed BIDS MRI data, processed functional and processed structural
derivatives in their corresponding repositories on GitHub.

The repositories (you can find them all
[here](https://github.com/orgs/ReproBrainChart/repositories)) are consistently named such that:

 * If you're looking for BIDS MRI, the repo will be named `<study>_BIDS`
 * If you're looking for processed functional data, the repo will be named `<study>_CPAC`
 * If you're looking for processed structural MRI, the repo will be named `<study>_FreeSurfer`

where `<study>` is replaced with `HBN`, `NKI`, `PNC`, `BHRC` or `CCNP`.

Note: Participant demographics and phenotypic data are under `<study>_BIDS` repository for each study and are named `study-<study>_desc-participants.tsv`.

#### Choose a QC threshold

When you download RBC data at a specific QC threshold you can be sure that
any file you find in your downloaded data is usable for further analysis.
RBC releases data at 3 different QC thresholds:

 * `complete-pass`: Structural and BOLD data have passed QC
 * `complete-artifact`: Structural data can be "Pass" or "Artifact", BOLD is "Pass"
 * `warning-fail`: Contains all the RBC data including QC failures. This threshold
  is not recommended and you'll have to explain why you chose this threshold in
  any publication resulting from it.

#### Choose a version

Lastly, you'll need to pick a _version_ of the data to get. Each time RBC makes
changes to the data, it will be released with a new version number. By picking
a version number for your RBC-based study you can be sure that your input data
will never change. The current release of RBC is `0.1`.


### Clone the data

Getting data on to your system will involve running a command like this:

```bash
$ datalad clone \
    https://github.com/ReproBrainChart/<study>_<content>.git \
    -b <qc_threshold>-<version>
```


## Example walkthrough

Suppose I'd like to get some processed structural data from PNC. I've decided that I don't
want to include T1ws with notable artifacts, so I choose the QC threshold to be `complete-pass`.
I've checked the RBC website and see that the most recent release is `0.1`. This means that
my last argument to `datalad clone` will be `-b complete-pass-0.1`.

From the example command in [ths documentation](#clone-the-data) I replace `<study>`
with `PNC` and `<content>` with `FreeSurfer`. My command would be:

```bash
$ datalad clone \
    https://github.com/ReproBrainChart/PNC_FreeSurfer.git \
    -b complete-pass-0.1
```

I see some warnings such as these:

```
[INFO   ] Unable to parse git config from origin
[INFO   ] Remote origin does not have git-annex installed; setting annex-ignore
[INFO   ] This could be a problem with the git-annex installation on the remote. Please make sure that git-annex-shell is available in PATH when you ssh into the remote. Once you have fixed the git-annex installation, run: git annex enableremote origin
install(ok): /home/cieslakm/data/PNC_FreeSurfer (dataset)
```

but these are ok. I now have a `DataLad` dataset with everything I need to start exploring
RBC data.


That command finishes surprisingly quickly: PNC
FreeSurfer has over a thousand subjects in it! But this is normal for `DataLad`.
(Note that cloning the processed functional data (i.e., `CPAC` files) will take
longer as `CPAC` functional outputs include more files compared to
`FreeSurfer`.) There is now a `PNC_FreeSurfer` directory that I can look
around in. Since I don't know which files I might want, I will explore this directory
in my terminal:

```bash
$ cd PNC_FreeSurfer/freesurfer/sub-192413932
$ ls
sub-192413932_brainmeasures.json@  sub-192413932_fsaverage.tar.xz@
sub-192413932_brainmeasures.tsv@   sub-192413932_fsLR_den-164k.tar.xz@
sub-192413932_freesurfer.tar.xz@   sub-192413932_regionsurfacestats.tsv@
```

These two tsv files contain the anatomical variables in tabular form, so I'd like
to copy these contents to my computer:

```bash
$ datalad get *.tsv
get(ok): freesurfer/sub-192413932/sub-192413932_regionsurfacestats.tsv (file) [from output-storage...]
get(ok): freesurfer/sub-192413932/sub-192413932_brainmeasures.tsv (file) [from output-storage...]
action summary:
  get (ok: 2)
```

Shell glob patterns can be used to get whichever files you might need.

<div class="alert alert-primary" role="alert">
  <b>WARNING:</b> DO NOT attempt to `get` all the file content! These studies take up
  a lot of disk space and you will likely run out of space unless you have a very big
  hard drive.
</div>


# FAQs

#### Running `datalad get` appears to be stuck - what should I do?

The first time you run `datalad get` may take 30 minutes or more to finish
copying the file. Subsequent runs of `datalad get` will be much faster.

Unless you see an error message when running `datalad get`, you should let
the command run until you see something printed out.

#### Do I need a supercomputer to get this data?

You can clone any of these datasets to any machine with internet access,
[`DataLad` (`git` and `git-annex`) installed](https://www.datalad.org/#install)
and your agreement with the License. The rest of the answer depends on what type
of data you plan on copying to your computer:

 * If you plan on copying only tabular data content to your computer you will need
at most a few free GB.
 * If you plan on copying 3D imaging data (e.g. ALFF, REHO) you will need hundreds of GB free.
 * If you plan on copying 4D denoised BOLD timeseries data you will need up to 4TB of free space.
