import asyncio
from enum import StrEnum
from pprint import pprint
from typing import Any

from client_api.base import BaseGitApiClient
from settings import Settings
from utils.helpers import decode_base64_to_utf8


class MediaType(StrEnum):
    VND_GITHUB_JSON = "application/vnd.github+json"
    JSON = "application/json"


class GitHubAPIClient(BaseGitApiClient):
    def __init__(self, base_url="https://api.github.com", access_token: str = None, timeout: int = 120) -> None:
        super().__init__(base_url, access_token, timeout)

    async def get_projects(self, profile_name: str) -> dict[str, Any]:
        response = await self.client.get(f"/users/{profile_name}/repos")
        return response.json()


    async def get_emojis(self) -> dict[str, str]:
        return await self.client.get("/emojis").json()


    async def get_readme(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/readme",
            headers=self.__put_headers()
        )
        return response.json() if response.status_code == 200 else {}


    async def get_project_languages(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/languages",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_description(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"repos/{owner}/{repo}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_branches(self, owner: str, repo: str, pagination_size: int, page: int) -> list[dict[str, Any]]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/branches?per_page={pagination_size}&page={page}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_default_branch_info(self, owner: str, repo: str, default_branch: str = "main") -> dict[str, Any]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/branches/{default_branch}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_tree(self, owner: str, repo: str, sha: str, recursive: bool) -> dict[str, Any]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/git/trees/{sha}?recursive={int(recursive)}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_dependencies(self, owner: str, repo: str, base: str, head: str) -> dict[str, Any]:
        basehead = f"{base}...{head}"
        response = await self.client.get(
            url=f'/repos/{owner}/{repo}/dependency-graph/compare/{basehead}',
            headers=self.__put_headers(media_type=MediaType.VND_GITHUB_JSON)
        )
        return response.json()

    async def get_project_contributors(self, owner: str, repo: str) -> list[dict[str, Any]]:
        response = await self.client.get(
            url=f"/repos/{owner}/{repo}/contributors",
            headers=self.__put_headers(media_type=MediaType.VND_GITHUB_JSON)
        )
        return response.json()

    async def get_file_content(self, owner: str, repo: str, sha: str) -> dict[str, Any]:
        response = await self.client.get(f"/repos/{owner}/{repo}/git/blobs/{sha}", headers=self.__put_headers())
        return response.json()

    def __put_headers(self, media_type: MediaType = MediaType.JSON) -> dict[str, str]:
        return {
            "Accept": media_type.value,
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }


async def use_case():
    client = GitHubAPIClient(access_token=Settings().github_api.ACCESS_TOKEN)
    commit_info = await client.get_default_branch_info("evgesha1999123", "Soundpad-Android", "master")
    pprint(commit_info["commit"]["sha"])
    sha = commit_info["commit"]["sha"]
    project_tree_response = await client.get_project_tree("evgesha1999123", "Soundpad-Android", sha, True)
    pprint(project_tree_response)
    response = await client.get_file_content("evgesha1999123", "Soundpad-Android", "24cc076498883b0eb81054a033a224ea8a4f340e")
    pprint(decode_base64_to_utf8(response["content"]))

if __name__ == '__main__':
    # asyncio.run(watch_dependencies(GitHubAPIClient(access_token=Settings().github_api.ACCESS_TOKEN)))
    asyncio.run(use_case())