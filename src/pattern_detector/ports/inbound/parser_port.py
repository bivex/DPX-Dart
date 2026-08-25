from abc import ABC, abstractmethod
from typing import List
from ...domain.code_model import DartFile, CodeModel


class DartParserPort(ABC):
    @abstractmethod
    def parse_file(self, file_path: str, content: str) -> DartFile:
        pass

    @abstractmethod
    def parse_code_model(self, paths: List[str]) -> CodeModel:
        pass
