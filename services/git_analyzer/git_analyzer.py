import asyncio
from enum import Enum
from typing import Literal

from client_api.base import BaseGitApiClient
from core.di import container
from models.git.contributor import Contributor
from models.git.dependence_package import DependencePackage
from models.git.readme import GitHubApiReadme
from models.git.repo import NativeGitRepoSchema, GeneralGitRepoInfoSchema, ProjectDependenciesSchema
from utils.dependence_parser import DependenceParser


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
        self.dependence_parser = DependenceParser()


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
        general_git_repo_info_schemas: list[GeneralGitRepoInfoSchema] = []
        for repo in self.repos:
            readme_response: dict = await self.client.get_readme(owner=repo.owner.login, repo=repo.name)
            general_git_repo_info_schemas.append(
                GeneralGitRepoInfoSchema(
                    readme=GitHubApiReadme(**readme_response) if readme_response else None,
                    description=repo.description,
                    topics=repo.topics)
            )
        return general_git_repo_info_schemas


    async def get_all_projects_dependencies(self) -> list[list[DependencePackage]]:
        return [await self.get_project_dependencies(repo) for repo in self.repos]


    async def get_project_dependencies(self, repo: NativeGitRepoSchema) -> list[DependencePackage]:
        contributors = await self._get_serialized_contributors(repo)
        if self._is_single_contributor(contributors):
            return await self._find_dependencies_for_one_contrib(contributors[0], repo)
        else:
            return await self.dependence_parser.parse_dependencies(repo)


    async def _get_serialized_contributors(self, repo: NativeGitRepoSchema) -> list[Contributor]:
        response_contrib = await self.client.get_project_contributors(owner=repo.owner.login, repo=repo.name)
        return [Contributor(**contributor) for contributor in response_contrib]


    async def _find_dependencies_for_one_contrib(
            self,
            contributor: Contributor,
            repo: NativeGitRepoSchema
    ) -> list[DependencePackage]:

        commits = contributor.contributions
        response_dependencies = await self.client.get_dependencies(
            owner=repo.owner.login, repo=repo.name, base="HEAD", head=f"HEAD~{commits - 1}"
        )
        return [DependencePackage(**package) for package in response_dependencies]


    @staticmethod
    def _is_single_contributor(contributors: list[Contributor]) -> bool:
        return len(contributors) == 1


async def use_case():
    from pprint import pprint
    analyzer = GitRepositoryAnalyzer(git_client=container.get(BaseGitApiClient), user_profile_name="evgesha1999123")
    await analyzer.get_user_repos()
    print(len(analyzer.filter_repos(FilterMode.EXCLUDE, ["autopoweroff", "medical-parser", "Rainy", "test_orm"])))
    pprint(await analyzer.get_general_repo_infos())


if __name__ == '__main__':
    asyncio.run(use_case())