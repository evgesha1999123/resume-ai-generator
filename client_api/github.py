from typing import Any

from client_api.base import BaseGitApiClient
from settings import Settings


class GitHubAPIClient(BaseGitApiClient):
    def __init__(self, base_url="https://api.github.com", access_token: str = None, timeout: int = 120) -> None:
        super().__init__(base_url, access_token, timeout)

    async def get_projects(self, profile_name: str) -> dict[str, Any]:
        response = await self.client.get(f"{self.base_url}/users/{profile_name}/repos")
        return response.json()

    async def get_emojis(self) -> dict[str, str]:
        return await self.client.get(f"{self.base_url}/emojis").json()


    async def get_readme(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/readme",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_languages(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/languages",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_description(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_branches(self, owner: str, repo: str, pagination_size: int, page: int) -> list[dict[str, Any]]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/branches?per_page={pagination_size}&page={page}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_commit_sha(self, owner: str, repo: str, main_branch_name: str = "main") -> dict[str, Any]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/branches/{main_branch_name}",
            headers=self.__put_headers()
        )
        return response.json()


    async def get_project_tree(self, owner: str, repo: str, sha: str, recursive: bool) -> dict[str, Any]:
        response = await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/git/trees/{sha}?recursive={int(recursive)}",
            headers=self.__put_headers()
        )
        return response.json()


    def __put_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github-commitcomment.raw+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }


async def use_case():
    client = GitHubAPIClient(access_token=Settings().github_api.ACCESS_TOKEN)
    default_branch_sha = await get_default_branch_sha(client)

    project_tree_response = await client.get_project_tree("flutter", "engine", default_branch_sha, True)
    with open("tree.json", mode="w+", encoding="utf-8") as f:
        f.write(str(project_tree_response))

def find_default_branch_sha(response_json: list[dict[str, Any]]) -> str | None:
    for branch in response_json:
        branch_name = branch["name"]
        if branch_name in ["master", "main"]:
            return branch["commit"]["sha"]
    print("not found, wait")
    return None

async def get_default_branch_sha(client: GitHubAPIClient) -> str:
    default_branch_sha = None
    current_page = 1
    while not default_branch_sha:
        branches_response = await client.get_project_branches(
            owner="flutter",
            repo="engine",
            pagination_size=100,
            page=current_page
        )
        response_json = branches_response
        default_branch_sha = find_default_branch_sha(response_json)
        current_page += 1
    return default_branch_sha