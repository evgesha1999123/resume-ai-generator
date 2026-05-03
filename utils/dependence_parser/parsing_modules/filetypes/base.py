from abc import ABC, abstractmethod


class BaseFileTypeParser(ABC):
    def __init__(self, content: str) -> None:
        self.content: str = content

    @abstractmethod
    def find_dependence_sections(self) -> list[str] | dict[str, list[str]]:
        raise NotImplementedError()