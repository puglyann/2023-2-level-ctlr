"""
Interface definitions for text processing pipelines.
"""
# pylint: disable=too-few-public-methods, unused-argument
from dataclasses import dataclass
from typing import Protocol

from core_utils.article.article import Article


class PipelineProtocol(Protocol):
    """
    Interface definition for pipeline.
    """

    def run(self) -> None:
        """
        Key API method.
        """


class HasConLLUStr(Protocol):
    """
    Utility subclass to mimic UDPipe result.
    """
    conll_str: str


class UDPipeResultProtocol(Protocol):
    """
    Utility class to mimic UDPipe result.
    """
    _: HasConLLUStr


class StanzaDocument(Protocol):
    """
    Utility class to mimic Stanza Document.
    """


class CoNLLUDocument(Protocol):
    """
    Utility class to mimic UDPipe Doc.
    """


class AbstractCoNLLUAnalyzer(Protocol):
    """
    Mock definition of library-specific entity.
    """

    def process(self, docs: list[StanzaDocument]) -> list[StanzaDocument]:
        """
        Process given document.

        Args:
            docs (list[StanzaDocument]): Collection of original Documents.

        Returns:
            list[StanzaDocument]: Collection of resulting documents.
        """

    def __call__(self, text: str) -> UDPipeResultProtocol:
        """
        Run analyzer as a function.

        Args:
            text (str): Raw document content.

        Returns:
            UDPipeResultProtocol: Output document.
        """


class LibraryWrapper(Protocol):
    """
    Interface definition for text analyzers.
    """
    _analyzer: AbstractCoNLLUAnalyzer

    def _bootstrap(self) -> AbstractCoNLLUAnalyzer:
        """
        Bootstrap analyzer with required models and settings.

        Returns:
            AbstractCoNLLUAnalyzer: Instance of analyzer.
        """

    def analyze(self, texts: list[str]) -> list[StanzaDocument | str]:
        """
        Analyze given texts.

        Args:
            texts (list[str]): Texts to analyze.

        Returns:
            list[StanzaDocument | str]: Collection of processed documents.
        """

    def to_conllu(self, article: Article) -> None:
        """
        Write ConLLU content to a file.

        Args:
            article (Article): Article to save
        """

    def from_conllu(self, article: Article) -> CoNLLUDocument:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            CoNLLUDocument: Document ready for parsing
        """
        print(f'from_conllu should be implemented for {self.__class__.__name__}!')
        raise NotImplementedError


@dataclass
class TreeNode:
    """
    Interface definition for node in the graph.
    """
    upos: str
    text: str
    children: list['TreeNode']
