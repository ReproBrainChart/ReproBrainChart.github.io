"""Update just cumulative files.

In those cases where we have to manually remove daily entries,
this regenerates the cumulative clone files.
"""

import os

import pandas as pd


def main(repo):
    """Fetch download statistics for a GitHub repository and output to a directory.

    Parameters
    ----------
    repo : str
        The name of the repository in the format "owner/repo".
    """
    script_dir = os.path.dirname(__file__)
    stats_dir = os.path.abspath(os.path.join(script_dir, "../../_data/clone-tracking"))
    daily_dir = "daily"
    cum_dir = "cumulative"

    owner_name, repo_name = repo.split("/")
    daily_clones_file = os.path.join(
        stats_dir,
        daily_dir,
        f"{owner_name}_{repo_name}_daily_clones.csv",
    )
    df_clones = pd.read_csv(daily_clones_file, index_col="date")

    # generate cumulative downloads for this repo + output to directory
    cumulative_clones_file = os.path.join(
        stats_dir,
        cum_dir,
        f"{owner_name}_{repo_name}_cum_clones.csv",
    )
    df_cum = df_clones.copy()
    df_cum["clone_count"] = df_cum["clone_count"].cumsum()
    df_cum.to_csv(cumulative_clones_file, index_label="date")


if __name__ == "__main__":
    repos = [
        "ReproBrainChart/BHRC_BIDS",
        "ReproBrainChart/BHRC_CPAC",
        "ReproBrainChart/BHRC_FreeSurfer",
        "ReproBrainChart/BHRC_fMRIPrep-Anat",
        "ReproBrainChart/BHRC_fMRIPrep-Func",
        "ReproBrainChart/BHRC_FreeSurfer-Post",
        "ReproBrainChart/BHRC_XCP-D",
        "ReproBrainChart/CCNP_BIDS",
        "ReproBrainChart/CCNP_CPAC",
        "ReproBrainChart/CCNP_FreeSurfer",
        "ReproBrainChart/CCNP_fMRIPrep-Anat",
        "ReproBrainChart/CCNP_fMRIPrep-Func",
        "ReproBrainChart/CCNP_FreeSurfer-Post",
        "ReproBrainChart/CCNP_XCP-D",
        "ReproBrainChart/HBN_BIDS",
        "ReproBrainChart/HBN_CPAC",
        "ReproBrainChart/HBN_FreeSurfer",
        "ReproBrainChart/HBN_fMRIPrep-Anat",
        "ReproBrainChart/HBN_fMRIPrep-Func",
        "ReproBrainChart/HBN_FreeSurfer-Post",
        "ReproBrainChart/HBN_XCP-D",
        "ReproBrainChart/NKI_BIDS",
        "ReproBrainChart/NKI_CPAC",
        "ReproBrainChart/NKI_FreeSurfer",
        "ReproBrainChart/NKI_fMRIPrep-Anat",
        "ReproBrainChart/NKI_fMRIPrep-Func",
        "ReproBrainChart/NKI_FreeSurfer-Post",
        "ReproBrainChart/NKI_XCP-D",
        "ReproBrainChart/PNC_BIDS",
        "ReproBrainChart/PNC_CPAC",
        "ReproBrainChart/PNC_FreeSurfer",
        "ReproBrainChart/PNC_fMRIPrep-Anat",
        "ReproBrainChart/PNC_fMRIPrep-Func",
        "ReproBrainChart/PNC_FreeSurfer-Post",
        "ReproBrainChart/PNC_XCP-D",
    ]
    for repo in repos:
        main(repo)
