from dishka import Provider, Scope, provide

from client_api.base import BaseGitApiClient
from client_api.github import GitHubAPIClient
from settings import Settings


class AppProvider(Provider):
    scope = Scope.APP

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide(scope=scope)
    def get_github_api_client(self) -> BaseGitApiClient:
        return GitHubAPIClient(access_token=self.settings.github_api.ACCESS_TOKEN)