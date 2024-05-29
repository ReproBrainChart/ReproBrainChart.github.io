---
title: "How to Get Data"
excerpt: "Get Data"
layout: single
permalink: /docs/get_data

---

### Step 1: Install DataLad

RBC is accessible via `datalad`. Follow the instructions [here](https://www.datalad.org/#install)
to get it installed.

### Step 2: Pick a dataset to clone

You can find each of the unprocessed BIDS MRI data, processed functional and processed structural
derivatives in their own git repositories.

The git repositories (you can find then all
[here](https://github.com/orgs/ReproBrainChart/repositories)) are consistently named such that:

 * If you're looking for BIDS MRI, the repo will be named `<study>_BIDS`
 * If you're looking for processed functional data, the repo will be named `<study>_CPAC`
 * If you're looking for BIDS MRI, the repo will be named `<study>_FreeSurfer`

where `<study>` is replaced with `HBN`, `NKI`, `PNC`, `BHRC` of `CCNP`.


### Step 3: Clone the data and take a look

#### Cloning

Getting data on to your system will involve running a command like this:

```bash
$ datalad clone https://github.com/ReproBrainChart/<study>_<content>.git
```

Suppose I'd like to get some processed anatomical data from PNC. I would replace `<study>`
with `PNC` and `<content>` with `FreeSurfer`. My command would be

```bash
$ datalad clone https://github.com/ReproBrainChart/PNC_FreeSurfer.git
```

You will see some warnings such as these:

```
[INFO   ] Unable to parse git config from origin
[INFO   ] Remote origin does not have git-annex installed; setting annex-ignore
[INFO   ] This could be a problem with the git-annex installation on the remote. Please make sure that git-annex-shell is available in PATH when you ssh into the remote. Once you have fixed the git-annex installation, run: git annex enableremote origin
install(ok): /home/cieslakm/data/PNC_FreeSurfer (dataset)
```

but you now have a `DataLad` dataset with everything you need to look at some data!

#### Getting data

That command probably finished a lot faster than you were expecting: PNC FreeSurfer has 1592
subjects in it! But this is normal for `DataLad`. You will see a `PNC_FreeSurfer` directory
that you can look around in and see all the files you might want to copy to your workspace.

For example, let's take a look at the data we might want from one of the PNC subjects:

```bash
$ cd PNC_FreeSurfer/freesurfer/sub-192413932
$ ls
sub-192413932_brainmeasures.json@  sub-192413932_fsaverage.tar.xz@
sub-192413932_brainmeasures.tsv@   sub-192413932_fsLR_den-164k.tar.xz@
sub-192413932_freesurfer.tar.xz@   sub-192413932_regionsurfacestats.tsv@
```

We know from the data dictionary that the tabular data is available in the
two TSV files, so let's get a copy of them that we can open:

```bash
$ datalad get *.tsv
get(ok): freesurfer/sub-192413932/sub-192413932_regionsurfacestats.tsv (file) [from output-storage...]
get(ok): freesurfer/sub-192413932/sub-192413932_brainmeasures.tsv (file) [from output-storage...]
action summary:
  get (ok: 2)
```

Shell glob patterns can be used to get whichever files you might need.



