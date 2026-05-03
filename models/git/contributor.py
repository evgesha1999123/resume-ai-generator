from models.git.mixin.git_hub_user import GitHubUserMixin


class Contributor(GitHubUserMixin):
    contributions: int

    class Config:
        extra = "ignore"