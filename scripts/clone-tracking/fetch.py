"""Fetch download statistics for a GitHub repository and output to a directory."""

import os
import re
from datetime import datetime as dt
from datetime import timedelta
from time import sleep

import pandas as pd
from github import Github
from github.GithubException import GithubException
from requests.exceptions import ConnectionError, RequestException, Timeout


MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 5


def _is_transient_error(exc):
    if isinstance(exc, GithubException):
        status_code = getattr(exc, "status", None)
        return status_code is not None and status_code >= 500

    if isinstance(exc, RequestException):
        if isinstance(exc, (ConnectionError, Timeout)):
            return True

        response = getattr(exc, "response", None)
        if response is not None and response.status_code is not None:
            return response.status_code >= 500

        error_message = str(exc).lower()
        return (
            re.search(r"too many 5\d{2} error responses", error_message) is not None
            or "timed out" in error_message
        )

    return False


def _run_with_retries(func, repo):
    """Run a GitHub API request with retries on transient failures.

    Parameters
    ----------
    func : callable
        The callable to execute.
    repo : str
        Repository name in "owner/repo" format, used for logging.

    Returns
    -------
    object or None
        The callable output, or None if transient failures persist after retries.

    Raises
    ------
    GithubException or RequestException
        Raised immediately for non-transient errors.
    """
    total_attempts = MAX_RETRIES + 1
    for retry in range(total_attempts):
        attempt = retry + 1
        try:
            return func()
        except (GithubException, RequestException) as exc:
            if not _is_transient_error(exc):
                raise

            if retry == MAX_RETRIES:
                print(
                    f"Warning: Could not fetch clone statistics for {repo} after "
                    f"{total_attempts} attempts. Skipping this repository."
                )
                return None

            wait_seconds = RETRY_DELAY_SECONDS * (2**retry)
            print(
                f"Transient error while fetching clone statistics for {repo} "
                f"(attempt {attempt}/{total_attempts}): {exc}. "
                f"Retrying in {wait_seconds} seconds..."
            )
            sleep(wait_seconds)


def main(repo):
    """Fetch download statistics for a GitHub repository and output to a directory.

    Parameters
    ----------
    repo : str
        The name of the repository in the format "owner/repo".
    """
    print(f"Fetching clone statistics for {repo}...")
    token = os.environ.get("SECRET_TOKEN")
    g = Github(token)
    repoobj = _run_with_retries(lambda: g.get_repo(repo), repo)
    if repoobj is None:
        return

    # List clones for the repository
    clones = _run_with_retries(lambda: fetch_clones(repoobj), repo)
    if clones is None:
        return
    df_clones = clones_to_df(clones)
    owner_name, repo_name = repo.split("/")

    script_dir = os.path.dirname(__file__)
    stats_dir = os.path.abspath(os.path.join(script_dir, "../../_data/clone-tracking"))
    daily_dir = "daily"
    cum_dir = "cumulative"

    os.makedirs(os.path.join(stats_dir, daily_dir), exist_ok=True)
    os.makedirs(os.path.join(stats_dir, cum_dir), exist_ok=True)

    daily_clones_file = os.path.join(
        stats_dir,
        daily_dir,
        f"{owner_name}_{repo_name}_daily_clones.csv",
    )
    if os.path.isfile(daily_clones_file):
        df_clones_historical = pd.read_csv(daily_clones_file, index_col="date")
    else:
        df_clones_historical = pd.DataFrame(columns=["clone_count"])

    # Ensure that the index is a datetime object
    df_clones.index = pd.to_datetime(df_clones.index)
    df_clones_historical.index = pd.to_datetime(df_clones_historical.index)

    if len(df_clones):
        # Merge df_clones and df_clones_historical.
        df_clones = pd.concat([df_clones_historical, df_clones], axis=0)
        # Sort by clone count so the rows with the highest counts are first
        df_clones = df_clones.sort_values("clone_count", ascending=False)
        # Drop duplicate index rows, retaining the highest clone count,
        # which should be the most accurate
        df_clones = df_clones.loc[~df_clones.index.duplicated(keep="first")]
        # Sort by date
        df_clones = df_clones.sort_index()
    else:
        df_clones = df_clones_historical.copy()

    # Fill in missing dates with 0s
    df_clones = patch_df(df_clones)
    # Sort by date again (just to be safe)
    df_clones = df_clones.sort_index()

    df_clones.to_csv(daily_clones_file, index_label="date")

    # generate cumulative downloads for this repo + output to directory
    cumulative_clones_file = os.path.join(
        stats_dir,
        cum_dir,
        f"{owner_name}_{repo_name}_cum_clones.csv",
    )
    df_cum = df_clones.copy()
    df_cum["clone_count"] = df_cum["clone_count"].cumsum()
    df_cum.to_csv(cumulative_clones_file, index_label="date")


def patch_df(df):
    """Fill in dates where no clones were made with 0's.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing clone statistics.

    Returns
    -------
    pd.DataFrame
        The DataFrame with missing dates filled in.
    """
    cur_date = df.index[0].date()
    todays_date = dt.now().date()
    row = 0
    delta = timedelta(days=1)

    while cur_date <= todays_date:
        missing_clones = pd.DataFrame(
            {"clone_count": [0]}, index=pd.DatetimeIndex(data=[cur_date])
        )
        missing_clones.index.name = "date"

        if row >= len(df.index):
            df = pd.concat([df, missing_clones])
        elif df.index[row].date() != cur_date:
            df = pd.concat([df.iloc[:row], missing_clones, df.iloc[row:]])

        row += 1
        cur_date += delta
    return df


def clones_to_df(clones):
    """Convert clone statistics to a DataFrame.

    Parameters
    ----------
    clones : list of github.RepositoryClone
        The clone statistics.

    Returns
    -------
    pd.DataFrame
        The clone statistics as a DataFrame.
        The index is the date of the clone and the column is clone_count.
    """
    timestamps = []
    total_clone_counts = []

    for c in clones:
        timestamps.append(pd.to_datetime(c.timestamp).date())
        total_clone_counts.append(c.count)

    df = pd.DataFrame(
        data={"clone_count": total_clone_counts},
        index=pd.DatetimeIndex(data=timestamps),
    )
    df.index.name = "date"
    return df


def fetch_clones(repo):
    """Fetch clone statistics for a repository.

    Parameters
    ----------
    repo : github.Repository.Repository
        The repository object.

    Returns
    -------
    list of github.RepositoryClone
        The clone statistics.
    """
    clones = repo.get_clones_traffic()
    return clones["clones"]


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
