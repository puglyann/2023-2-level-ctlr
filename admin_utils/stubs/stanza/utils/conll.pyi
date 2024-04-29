from pathlib import Path
from typing import Protocol

class DocumentLike(Protocol):
    def __init__(self, sentences: list, text: str) -> None:
        """
        Initializes instance.
        """


class CoNLL:
    @staticmethod
    def conll2doc(input_file: Path) -> DocumentLike:
        """
        Load ConLLU file from disk.
        """
