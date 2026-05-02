from pydantic import BaseModel, HttpUrl
from typing import Optional


class GitHubUser(BaseModel):
    login: str
    id: int
    avatar_url: HttpUrl
    url: HttpUrl
    html_url: HttpUrl
    repos_url: HttpUrl
    type: str
    user_view_type: Optional[str] = None
    public_repos: Optional[int] = None

    class Config:
        extra = "ignore"