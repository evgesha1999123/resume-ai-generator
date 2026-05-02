import pytest

from client_api.base import BaseGitApiClient
from core.di import container


@pytest.fixture
def user_profile():
    return "evgesha1999123"


@pytest.fixture
def git_client():
    return container.get(BaseGitApiClient)