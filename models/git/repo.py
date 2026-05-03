from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from models.git.dependence_package import DependencePackage
from models.git.readme import GitHubApiReadme
from models.git.license import License
from models.git.user import GitHubUser


class GeneralGitRepoInfoSchema(BaseModel):
    readme: Optional[GitHubApiReadme] = Field(default=None, description="Readme проекта для общей информации")
    description: Optional[str] = Field(default="", description="Описание проекта")
    topics: list[str] = Field(..., description="Топики проекта")


class ProjectDependenciesSchema(BaseModel):
    # TODO: Структуру уточнить
    dependencies: list[DependencePackage] = Field(
        ..., description="Список зависимостей проекта для анализа используемого стека технологий"
    )


class ProjectStructureSchema(BaseModel):
    tree: list[str] = Field(..., description="Дерево проекта для базового анализа структуры")
    languages: list[str] = Field(..., description="Список используемых языков для анализа стека проекта")


class GitRepoDataSchema(BaseModel):
    general: GeneralGitRepoInfoSchema = Field(
        ..., description="Общая информация для получения базового представления о проекте"
    )
    dependencies: ProjectDependenciesSchema = Field(..., description="Зависимости проекта")
    structure: ProjectStructureSchema = Field(..., description="Сведения о структуре и архитектуре проекта")


class NativeGitRepoSchema(BaseModel):
    #TODO: Важно! Модель зависит от API GitHub, ее нужно сделать независимой от конкретного API.
    created_at: datetime = Field(..., description="Дата создания проекта")
    branches_url: HttpUrl = Field(..., description="Url всех веток проекта")
    clone_url: HttpUrl = Field(..., description="Url для клонирования проекта")
    comments_url: HttpUrl
    commits_url: HttpUrl
    description: Optional[str] = Field(default=None, description="Описание проекта")
    fork: bool
    forks: int
    forks_count: int
    full_name: str
    git_commits_url: HttpUrl
    git_refs_url: HttpUrl
    git_tags_url: HttpUrl

    has_discussions: bool
    has_downloads: bool
    has_issues: bool
    has_pages: bool
    has_projects: bool
    has_pull_requests: bool
    has_wiki: bool

    homepage: Optional[str] = Field(default=None)
    id: int = Field(..., description="ID репозитория")
    language: Optional[str] = Field(default="", description="Основной язык репозитория")
    languages_url: str = Field(..., description="Url для более подробной информации о языках репозитория")
    license: Optional[License] = Field(default=None, description="Лицензия проекта, если есть")
    name: str = Field(..., description="Короткое имя проекта")
    owner: GitHubUser = Field(..., description="Сводная информация о владельце репозитория")
    private: bool = Field(..., description="Флаг приватности репозитория")
    size: int = Field(..., description="Размер проекта")

    ssh_url: str
    svn_url: HttpUrl
    topics: Optional[list] = Field(default_factory=list, description="Топики проекта, если есть")
    tags_url: HttpUrl
    teams_url: HttpUrl
    trees_url: HttpUrl = Field(..., description="Url дерева проекта")
    url: HttpUrl = Field(..., description="Url репозитория проекта")

    visibility: str = Field(..., description="Тип видимости репозитория, напр. 'public'")

    default_branch: str = Field(..., description="Основная ветка проекта")

    class Config:
        extra = "ignore"