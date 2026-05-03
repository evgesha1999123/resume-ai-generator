from abc import ABC, abstractmethod
from enum import StrEnum

from models.git.dependence_package import DependencePackage
from utils.dependence_parser.parsing_modules.filetypes.base import BaseFileTypeParser


class FileType(StrEnum):
    TXT = "txt"
    LOCK = "lock"
    JSON = "json"
    TOML = "toml"
    YAML = "yaml"
    XML = "xml"
    GRADLE = "gradle"
    KTS = "kts"
    MOD = "mod"
    SUM = "sum"
    GEMFILE = "Gemfile"
    CPROJ = "cproj"
    SWIFT = "swift"
    SBT = "sbt"
    EXS = "exs"
    CABAL = "cabal"


class BaseDependenceParser(ABC):
    def __init__(self, parsing_module: BaseFileTypeParser) -> None:
        self.parsing_module = parsing_module

    @abstractmethod
    def extract(self) -> list[DependencePackage]:
        raise NotImplementedError()