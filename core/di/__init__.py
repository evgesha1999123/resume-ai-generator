from dishka import make_container

from core.di.app_provider import AppProvider
from settings import settings

providers = [AppProvider(settings=settings)]

container = make_container(*providers)