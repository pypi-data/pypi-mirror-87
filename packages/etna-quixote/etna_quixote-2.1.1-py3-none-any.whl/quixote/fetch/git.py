from datetime import datetime
import git
from quixote import get_context


def clone(url: str, target_path: str = None, maximum_date: datetime = None):
    """
    Fetch the delivery from a Git repository

    :param url:                 the URL to clone from
    :param target_path:         the path to which the repository should be cloned to
    :param maximum_date:        the maximum date to consider for commits
    """
    target_path = target_path or get_context()["delivery_path"]
    repo = git.Repo.clone_from(url, target_path)
    if maximum_date is not None and repo.active_branch.is_valid():
        end_timestamp = int(maximum_date.timestamp())
        accepted_commits = repo.iter_commits(until=end_timestamp)
        commit = next(accepted_commits, None)
        if commit is None:
            raise ValueError(f"unable to checkout with maximum date {maximum_date}: no commits found")
        repo.git.checkout(commit)
