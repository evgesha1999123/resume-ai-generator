import asyncio
from typing import Optional, Any
from settings import Settings
from pprint import pprint

from httpx import AsyncClient, Response


class GitAPIClient:
    def __init__(self, access_token: Optional[str] = None, base_url="https://api.github.com") -> None:
        self.token = access_token
        self.base_url = base_url
        self.client = AsyncClient(base_url=base_url, timeout=120)


    async def get_emojis(self):
        return await self.client.get(f"{self.base_url}/emojis")


    async def get_readme(self, owner: str, repo: str) -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/readme",
            headers=self.__put_headers()
        )


    async def get_project_languages(self, owner: str, repo: str) -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/languages",
            headers=self.__put_headers()
        )


    async def get_project_description(self, owner: str, repo: str) -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}",
            headers=self.__put_headers()
        )


    async def get_project_branches(self, owner: str, repo: str, pagination_size: int, page: int) -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/branches?per_page={pagination_size}&page={page}",
            headers=self.__put_headers()
        )


    async def get_commit_sha(self, owner: str, repo: str, main_branch_name: str = "main") -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/branches/{main_branch_name}",
            headers=self.__put_headers()
        )


    async def get_project_tree(self, owner: str, repo: str, sha: str, recursive: bool) -> Response:
        return await self.client.get(
            url=f"{self.base_url}/repos/{owner}/{repo}/git/trees/{sha}?recursive={str(int(recursive))}",
            headers=self.__put_headers()
        )


    def __put_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github-commitcomment.raw+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }


async def use_case():
    client = GitAPIClient(access_token=Settings().github_api.ACCESS_TOKEN)
    # response = await client.get_readme(owner="evgesha1999123", repo="resume-ai-generator")
    for it in range(11):
        branches_response = await client.get_project_branches("flutter", "engine", pagination_size=100, page=it)
        response_json = branches_response.json()
        find_master_branch(response_json)
    # response = await client.get_project_tree(owner="flutter", repo="engine", sha="70671823931a630cd40c4db50db67a9d7e1367cf", recursive=True)
    # print(response.text)
    # print(response.status_code)
    # pprint(response.json())

def find_master_branch(response_json: list[dict[str, Any]]):
    for branch in response_json:
        branch_name = branch["name"]
        if branch_name in ["master", "main"]:
            print(branch["name"])
            return
    print("NOT FOUND!")


if __name__ == '__main__':
    asyncio.run(use_case())