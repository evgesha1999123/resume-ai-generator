from pydantic import HttpUrl
from typing import Optional

from models.git.mixin.git_hub_user import GitHubUserMixin


class GitHubUser(GitHubUserMixin):
    repos_url: HttpUrl
    public_repos: Optional[int] = None

    class Config:
        extra = "ignore"