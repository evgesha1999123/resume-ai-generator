import asyncio
from enum import Enum
from typing import Literal

from client_api.base import BaseGitApiClient
from core.di import container
from models.git.repo import GitRepoDataSchema, NativeGitRepoSchema, GeneralGitRepoInfoSchema


class FilterMode(Enum):
    EXCLUDE = 0
    INCLUDE = 1
    INCLUDE_ALL = 2
    EXCLUDE_ALL = 3

    @classmethod
    def selective(cls) -> list[Literal]:
        return [cls.INCLUDE, cls.EXCLUDE]

    @classmethod
    def all(cls) -> list[Literal]:
        return [cls.EXCLUDE_ALL, cls.INCLUDE_ALL]


class GitRepositoryAnalyzer:
    """
    Класс, выполняющий работу по парсингу гит - репозиториев.
    Нужен, чтобы получить pydantic-модель с информационными схемами.
    """
    def __init__(
            self,
            git_client: BaseGitApiClient,
            user_profile_name: str
    ) -> None:
        self.client = git_client
        self.user_profile_name = user_profile_name
        self.repos_cache: list[NativeGitRepoSchema] = []
        self.repos: list[NativeGitRepoSchema] = []

    async def get_user_repos(self) -> list[NativeGitRepoSchema]:
        repos = await self.client.get_projects(self.user_profile_name)
        self.repos = [NativeGitRepoSchema(**repo) for repo in repos]
        self.repos_cache = self.repos
        return self.repos

    def filter_repos(self, mode: FilterMode, filter_names: list[str]) -> list[NativeGitRepoSchema]:
        if mode in FilterMode.selective():
            self._filter_selective(mode, filter_names)
        else:
            self._filter_all(mode)

        return self.repos

    def _filter_selective(self, mode: FilterMode, filter_names: list[str]) -> None:
        self.repos = list(
            filter(
                lambda repo:
                    repo.name in filter_names if mode == FilterMode.INCLUDE else repo.name not in filter_names,
                    self.repos_cache,
            )
        )

    def _filter_all(self, mode: FilterMode) -> None:
        if mode == FilterMode.EXCLUDE_ALL:
            self.repos = []
        else:
            self.repos = self.repos_cache

    async def get_general_repo_infos(self) -> list[GeneralGitRepoInfoSchema]:
        pass

    async def get_get_repo_infos(self) -> list[GitRepoDataSchema]:
        pass

async def use_case():
    analyzer = GitRepositoryAnalyzer(git_client=container.get(BaseGitApiClient), user_profile_name="evgesha1999123")
    await analyzer.get_user_repos()
    print(len(analyzer.filter_repos(FilterMode.EXCLUDE, ["autopoweroff", "medical-parser", "Rainy", "test_orm"])))


if __name__ == '__main__':
    asyncio.run(use_case())