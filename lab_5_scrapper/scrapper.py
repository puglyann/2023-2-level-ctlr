"""
Crawler implementation.
"""
# pylint: disable=too-many-arguments, too-many-instance-attributes, unused-import, undefined-variable
import datetime
import json
import pathlib
import shutil
import re
from random import randrange
from time import sleep
from typing import Pattern, Union

import requests

from bs4 import BeautifulSoup
from core_utils.article.article import Article
from core_utils.article.io import to_raw, to_meta
from core_utils.config_dto import ConfigDTO
from core_utils.constants import ASSETS_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH


class IncorrectVerifyError(Exception):
    pass


class IncorrectSeedURLError(Exception):
    pass


class IncorrectNumberOfArticlesError(Exception):
    pass


class IncorrectHeadersError(Exception):
    pass


class IncorrectEncodingError(Exception):
    pass


class IncorrectTimeoutError(Exception):
    pass


class NumberOfArticlesOutOfRangeError(Exception):
    pass


class Config:
    """
    Class for unpacking and validating configurations.
    """

    def __init__(self, path_to_config: pathlib.Path) -> None:
        """
        Initialize an instance of the Config class.

        Args:
            path_to_config (pathlib.Path): Path to configuration.
        """
        self.path_to_config = path_to_config
        self._validate_config_content()
        self.config = self._extract_config_content()

        self._encoding = self.config.encoding
        self._headers = self.config.headers
        self._headless_mode = self.config.headless_mode
        self._num_articles = self.config.total_articles
        self._seed_urls = self.config.seed_urls
        self._should_verify_certificate = self.config.should_verify_certificate
        self._timeout = self.config.timeout

    def _extract_config_content(self) -> ConfigDTO:
        """
        Get config values.

        Returns:
            ConfigDTO: Config values
        """
        with open(self.path_to_config, 'r') as f:
            conf = json.load(f)

        return ConfigDTO(
            seed_urls=conf['seed_urls'],
            total_articles_to_find_and_parse=conf['total_articles_to_find_and_parse'],
            headers=conf['headers'],
            encoding=conf['encoding'],
            timeout=conf['timeout'],
            should_verify_certificate=conf['should_verify_certificate'],
            headless_mode=conf['headless_mode']
        )

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt.
        """
        with open(self.path_to_config, 'r', encoding='utf-8') as file:
            conf = json.load(file)

        if not (isinstance(conf['seed_urls'], list)
                and all(re.match(r"https?://(www.)?", seed_url) for seed_url in conf['seed_urls'])):
            raise IncorrectSeedURLError

        num_of_a = conf['total_articles_to_find_and_parse']
        if (not isinstance(num_of_a, int) or num_of_a < 0 or isinstance(num_of_a, bool)) \
                or (isinstance(num_of_a, int) and not (1 <= num_of_a <= 150)):
            raise IncorrectNumberOfArticlesError

        if not isinstance(conf['headers'], dict):
            raise IncorrectHeadersError

        if not isinstance(conf['encoding'], str):
            raise IncorrectEncodingError

        if not (isinstance(conf['timeout'], int) and (0 < conf['timeout'] < 60)
        ):
            raise IncorrectTimeoutError

        if (not isinstance(conf['should_verify_certificate'], bool)) \
                or (not isinstance(conf['headless_mode'], bool)):
            raise IncorrectVerifyError

        if num_of_a not in range(1, 151):
            raise NumberOfArticlesOutOfRangeError

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls.

        Returns:
            list[str]: Seed urls
        """
        return self._seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape.

        Returns:
            int: Total number of articles to scrape
        """
        return self._num_articles

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting.

        Returns:
            dict[str, str]: Headers
        """
        return self._headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing.

        Returns:
            str: Encoding
        """
        return self._encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response.

        Returns:
            int: Number of seconds to wait for response
        """
        return self._timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate.

        Returns:
            bool: Whether to verify certificate or not
        """
        return self._should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode.

        Returns:
            bool: Whether to use headless mode or not
        """
        return self._headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Deliver a response from a request with given configuration.

    Args:
        url (str): Site url
        config (Config): Configuration

    Returns:
        requests.models.Response: A response from a request
    """
    sleep(randrange(3))
    return requests.get(url=url,
                        headers=config.get_headers(),
                        timeout=config.get_timeout(),
                        verify=config.get_verify_certificate())


class Crawler:
    """
    Crawler implementation.
    """

    url_pattern: Union[Pattern, str]

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the Crawler class.

        Args:
            config (Config): Configuration
        """
        self.config = config
        self.urls = []
        self.url_pattern = 'https://new-science.ru'

    def _extract_url(self, article_bs: BeautifulSoup) -> str:
        """
        Find and retrieve url from HTML.

        Args:
            article_bs (bs4.BeautifulSoup): BeautifulSoup instance

        Returns:
            str: Url from HTML
        """
        url = ''
        for div in article_bs.find_all('div', {'class': 'post-details'}):
            for urls in div.select('a'):
                url = urls['href']
        return self.url_pattern + url

    def find_articles(self) -> None:
        """
        Find articles.
        """
        urls = []

        for url in self.get_search_urls():
            response = make_request(url, self.config)

            if not response.ok:
                continue

            src = response.text
            soup = BeautifulSoup(src, 'lxml')
            urls.append(self._extract_url(soup))

        self.urls.extend(urls)

    def get_search_urls(self) -> list:
        """
        Get seed_urls param.

        Returns:
            list: seed_urls param
        """
        return self.config.get_seed_urls()


# 10
# 4, 6, 8, 10


class HTMLParser:
    """
    HTMLParser implementation.
    """

    def __init__(self, full_url: str, article_id: int, config: Config) -> None:
        """
        Initialize an instance of the HTMLParser class.

        Args:
            full_url (str): Site url
            article_id (int): Article id
            config (Config): Configuration
        """
        self.full_url = full_url
        self.article_id = article_id
        self.config = config
        self.article = Article(full_url, article_id)

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Find text of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        all_body = article_soup.find_all('div')

        texts = []
        if all_body:
            all_divs = all_body[0].find_all('div', class_='entry-content entry clearfix')
            texts = []
            for div_bs in all_divs:
                texts.append(div_bs.text)

        self.article.text = ''.join(texts)

    def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> Article:
        """
        Find meta information of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        response = make_request(self.full_url, self.config)
        if response.ok:
            article_bs = BeautifulSoup(response.text, 'lxml')
            self._fill_article_with_text(article_bs)
            self._fill_article_with_meta_information(article_bs)

        return self.article

    def unify_date_format(self, date_str: str) -> datetime.datetime:
        """
        Unify date format.

        Args:
            date_str (str): Date in text format

        Returns:
            datetime.datetime: Datetime object
        """

    def parse(self) -> Union[Article, bool, list]:
        """
        Parse each article.

        Returns:
            Union[Article, bool, list]: Article instance
        """


def prepare_environment(base_path: Union[pathlib.Path, str]) -> None:
    """
    Create ASSETS_PATH folder if no created and remove existing folder.

    Args:
        base_path (Union[pathlib.Path, str]): Path where articles stores
    """
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir(parents=True)


def main() -> None:
    """
    Entrypoint for scrapper module.
    """
    conf = Config(CRAWLER_CONFIG_PATH)
    crawler = Crawler(conf)
    crawler.find_articles()
    prepare_environment(ASSETS_PATH)

    for id_num, url in enumerate(crawler.urls, 1):
        parser = HTMLParser(url, id_num, conf)
        article = parser.parse()
        if isinstance(article, Article):
            to_raw(article)
            to_meta(article)


if __name__ == "__main__":
    main()
