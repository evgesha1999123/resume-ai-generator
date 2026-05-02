from abc import ABC, abstractmethod
from typing import Any

from httpx import AsyncClient


class BaseGitApiClient(ABC):
    def __init__(self, base_url: str, access_token: str, timeout: int) -> None:
        self.token = access_token
        self.base_url = base_url
        self.timeout = timeout
        self.client = AsyncClient(base_url=base_url, timeout=timeout)

    async def aclose(self) -> None:
        await self.client.aclose()

    def open(self) -> AsyncClient:
        self.client = AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self.client

    @abstractmethod
    async def get_projects(self, profile_name: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_readme(self, owner: str, repo: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_project_languages(self, owner: str, repo: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_project_description(self, owner: str, repo: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_project_branches(self, owner: str, repo: str, pagination_size: int, page: int) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_commit_sha(self, owner: str, repo: str, main_branch_name: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_project_tree(self, owner: str, repo: str, sha: str, recursive: bool) -> Any:
        raise NotImplementedError()