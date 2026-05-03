from pprint import pprint

from utils.dependence_parser.parsing_modules.languages.base import BaseFileTypeParser, FileType


class TomlDependenceParser(BaseFileTypeParser):
    def __init__(self, content: str) -> None:
        super().__init__(content)
        self.file_type = FileType.TOML

    def find_dependence_sections(self) -> dict[str, list[str]]:
        sections = {}

        lines = self.content.splitlines()
        current_section = ""

        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line
                sections[current_section] = []
            if current_section != "" and line != current_section:
                sections[current_section].append(line)

        pprint(sections)

        return sections

if __name__ == '__main__':
    parser = TomlDependenceParser(content='''[tool.poetry]
        name = "resume-ai-generator"
        version = "0.1.0"
        description = ""
        authors = ["evgesha1999 <evgesha.22013@gmail.com>"]
        readme = "README.md"
        
        [tool.poetry.dependencies]
        python = "^3.13"
        httpx = "^0.28.1"
        pydantic = "^2.13.3"
        pydantic-core = "^2.46.3"
        pydantic-settings = "^2.14.0"
        dishka = "^1.10.1"
        pytest = "^9.0.3"
        pytest-asyncio = "^1.3.0"
        
        
        [build-system]
        requires = ["poetry-core"]
        build-backend = "poetry.core.masonry.api"
        
        [dependency-groups]
        dev = [
            "pytest (>=9.0.3,<10.0.0)",
            "pytest-asyncio (>=1.3.0,<2.0.0)"
        ]
        ''')
    parser.find_dependence_sections()