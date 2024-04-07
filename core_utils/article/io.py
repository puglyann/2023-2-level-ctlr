"""
I/O operations for Article.
"""
import json
import pathlib
from pathlib import Path
from typing import Optional, Union

from core_utils.article.article import (Article, ArtifactType, date_from_meta,
                                        get_article_id_from_filepath)


def to_raw(article: Article) -> None:
    """
    Save raw text.

    Args:
        article (Article): Article instance
    """
    with open(article.get_raw_text_path(), 'w', encoding='utf-8') as file:
        file.write(article.text)


def from_raw(path: Union[pathlib.Path, str],
             article: Optional[Article] = None) -> Article:
    """
    Load raw text and create an Article with it.

    Args:
        path (Union[pathlib.Path, str]): Path to article raw text
        article (Optional[Article]): Article instance

    Returns:
        Article: Article instance
    """
    article_id = get_article_id_from_filepath(Path(path))

    with open(file=path,
              mode='r',
              encoding='utf-8') as article_file:
        text = article_file.read()

    article = article if article else Article(url=None,
                                              article_id=article_id)
    article.text = text
    return article


def to_cleaned(article: Article) -> None:
    """
    Save cleaned text.

    Args:
        article (Article): Article instance
    """
    with open(article.get_file_path(ArtifactType.CLEANED), 'w', encoding='utf-8') as file:
        file.write(article.get_cleaned_text())


def to_meta(article: Article) -> None:
    """
    Save metafile.

    Args:
        article (Article): Article instance
    """
    with open(article.get_meta_file_path(), 'w', encoding='utf-8') as meta_file:
        json.dump(article.get_meta(),
                  meta_file,
                  indent=4,
                  ensure_ascii=False,
                  separators=(',', ': '))


def from_meta(path: Union[pathlib.Path, str],
              article: Optional[Article] = None) -> Article:
    """
    Load meta.json file into the Article abstraction.

    Args:
        path (Union[pathlib.Path, str]): Path to meta info
        article (Optional[Article]): Article instance

    Returns:
        Article: Article instance
    """
    with open(path, encoding='utf-8') as meta_file:
        meta = json.load(meta_file)

    article = article if article else \
        Article(url=meta.get('url', None), article_id=meta.get('id', 0))

    article.article_id = meta.get('id', 0)
    article.url = meta.get('url', None)
    article.title = meta.get('title', '')
    article.date = date_from_meta(meta.get('date', None))
    article.author = meta.get('author', None)
    article.topics = meta.get('topics', None)
    article.pos_frequencies = meta.get('pos_frequencies', None)

    # intentionally leave it empty
    article.text = ''
    return article


def to_conllu(article: Article,
              include_morphological_tags: bool = False,
              include_pymorphy_tags: bool = False) -> None:
    """
    Save conllu information from the Article into the .conllu file.

    Args:
        article (Article): Article instance
        include_morphological_tags (bool): Flag to include morphological information
        include_pymorphy_tags (bool): Include pymorphy tags or not
    """
    article_type = ArtifactType.POS_CONLLU
    if include_morphological_tags:
        article_type = ArtifactType.MORPHOLOGICAL_CONLLU
    if include_pymorphy_tags:
        article_type = ArtifactType.FULL_CONLLU

    with open(file=article.get_file_path(article_type),
              mode='w',
              encoding='utf-8') as conllu_file:
        conllu_file.write(article.get_conllu_text(include_morphological_tags))


def to_json(article: Article,
            patterns_found: dict[str, list[tuple[list[str], str]]]) -> None:
    """
    Saves patterns as json.

    Args:
        article (Article): Article instance
        patterns_found (dict[str, list[tuple[list[str], str]]]): Found patterns
    """
    with open(article.get_pattern_path(), 'w', encoding='utf-8') as meta_file:
        json.dump(patterns_found,
                  meta_file,
                  indent=4,
                  ensure_ascii=False,
                  separators=(',', ': '))
