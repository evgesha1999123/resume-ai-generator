from pydantic import BaseModel, Field, HttpUrl


class GitHubApiReadme(BaseModel):
    name: str
    path: str
    sha: str
    size: int
    url: HttpUrl = Field(..., description="Url GitHub")
    download_url: HttpUrl = Field(..., description="Url для скачивания содержимого")
    type: str = Field(..., description="Тип 'file', и др.")
    content: str = Field(..., description="Закодированное (в base64 по умолчанию) содержимое файла")
    encoding: str = Field(..., description="Кодировка содержимого файла")

    class Config:
        extra = "ignore"