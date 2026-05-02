import pytest

from models.git.repo import NativeGitRepoSchema
from services.git_analyzer.git_analyzer import GitRepositoryAnalyzer, FilterMode
from tests.fixtures import git_client, user_profile


@pytest.fixture
def github_analyzer(git_client, user_profile):
    return GitRepositoryAnalyzer(
        git_client,
        user_profile,
    )


@pytest.mark.asyncio
async def test_github_client(github_analyzer):
    repos = await github_analyzer.get_user_repos()
    assert len(repos) == 14
    assert isinstance(repos[0], NativeGitRepoSchema)
    await github_analyzer.client.aclose()


@pytest.mark.asyncio
async def test_filter_repos(github_analyzer):
    github_analyzer.client.open()

    repos = await github_analyzer.get_user_repos()

    assert len(github_analyzer.repos) == 14
    assert github_analyzer.repos_cache == repos
    all_names = [repo.name for repo in repos]

    # test exclude filter
    filter_names = ["autopoweroff", "medical-parser", "Rainy", "test_orm"]
    github_analyzer.filter_repos(
        mode=FilterMode.EXCLUDE, filter_names=filter_names
    )
    assert len(github_analyzer.repos) == 10

    for repo in github_analyzer.repos:
        assert not name_exists(repo.name, filter_names)

    # test include filter
    github_analyzer.filter_repos(FilterMode.INCLUDE, filter_names)

    assert len(github_analyzer.repos) == 4

    for repo in github_analyzer.repos:
        assert name_exists(repo.name, all_names)

    #test exclude_all
    github_analyzer.filter_repos(FilterMode.EXCLUDE_ALL, filter_names)
    assert not github_analyzer.repos

    #test include_all
    github_analyzer.filter_repos(FilterMode.INCLUDE_ALL, filter_names)
    assert 14 == len(github_analyzer.repos) == len(github_analyzer.repos_cache)

    await github_analyzer.client.aclose()


def name_exists(name, filter_names):
    return name in filter_names