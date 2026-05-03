from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Vulnerability(BaseModel):
    severity: str
    advisory_ghsa_id: str
    advisory_summary: str
    advisory_url: HttpUrl

    class Config:
        extra = "ignore"


class DependencePackage(BaseModel):
    change_type: Optional[str] = Field(default=None, description="Тип изменения зависимости, например, 'added'")
    ecosystem: str = Field(..., description="Принадлежность пакета к экосистеме")
    license: Optional[str] = Field(default=None, description="Лицензия, если есть")
    manifest: str = Field(..., description="Файл манифеста, в котором объявлена эта зависимость")
    name: str = Field(..., description="Имя пакета")
    package_url: Optional[str] = Field(default=None, description="Url скачивания паккета")
    scope: Optional[str] = Field(default=None, description="Область видимости, в которой используется пакет")
    source_repository_url: Optional[HttpUrl] = Field(default=None, description="Url исходного репозитория пакета")
    version: str = Field(..., description="Версия пакета")
    vulnerabilities: Optional[list[Vulnerability]] = Field(default_factory=list, description="Сведения о уязвимостях, если есть")

    class Config:
        extra = "ignore"