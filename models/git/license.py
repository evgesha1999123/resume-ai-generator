from typing import Optional

from pydantic import BaseModel, HttpUrl


class License(BaseModel):
    key: Optional[str]
    name: Optional[str]
    spdx_id: Optional[str]
    url: Optional[HttpUrl]
    node_id: Optional[str]