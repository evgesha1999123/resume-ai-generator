from typing import Optional

from pydantic import BaseModel, HttpUrl


class GitHubUserMixin(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    url: HttpUrl
    html_url: HttpUrl
    type: str
    user_view_type: Optional[str] = None