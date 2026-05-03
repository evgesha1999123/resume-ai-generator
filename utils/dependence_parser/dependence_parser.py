import asyncio

from client_api.base import BaseGitApiClient
from models.git.dependence_package import DependencePackage
from models.git.repo import NativeGitRepoSchema
from pprint import pprint


class DependenceParser:
    DEPENDENCY_FILES = {
        "python": [
            "requirements.txt",
            "pyproject.toml",
            "Pipfile",
            "setup.py",
            "setup.cfg",
            "poetry.lock",
        ],
        "javascript": [
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ],
        "typescript": [
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ],
        "java": [
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
        ],
        "kotlin": [
            "build.gradle.kts",
            "build.gradle",
            "settings.gradle.kts",
            "settings.gradle",
            "libs.versions.toml",
        ],
        "go": [
            "go.mod",
            "go.sum",
        ],
        "ruby": [
            "Gemfile",
            "Gemfile.lock",
        ],
        "php": [
            "composer.json",
            "composer.lock",
        ],
        "csharp": [
            ".csproj",
            ".sln",
            "packages.config",
        ],
        "rust": [
            "Cargo.toml",
            "Cargo.lock",
        ],
        "swift": [
            "Package.swift",
            "Package.resolved",
        ],
        "dart": [
            "pubspec.yaml",
            "pubspec.lock",
        ],
        "scala": [
            "build.sbt",
        ],
        "elixir": [
            "mix.exs",
            "mix.lock",
        ],
        "haskell": [
            "package.yaml",
            ".cabal",
            "stack.yaml",
        ],
    }

    def __init__(self, git_client: BaseGitApiClient) -> None:
        self.client = git_client

    async def parse_dependencies(self, schema: NativeGitRepoSchema) -> None:
        sha = await self.client.get_default_branch_info(
            owner=schema.owner.name, repo=schema.name, default_branch=schema.default_branch
        )
        tree_response = await self.client.get_project_tree(
            owner=schema.owner.login, repo=schema.name, sha=sha, recursive=True
        )
        pprint(tree_response)

# if __name__ == '__main__':
#     asyncio.run()