"""
Validate websites parameters.
"""
# pylint: disable=import-error,assignment-from-no-return
import json
import re
import time
from copy import deepcopy

import bs4 as bs
import requests
from selenium.common.exceptions import (ElementClickInterceptedException, NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from config.website_validation.constants import (BUTTONS_PATH, CheckStatuses, CONFIG_PATH,
                                                 DIST_PATH, HEADERS_ATTEMPTS)
from config.website_validation.utils import (create_driver, define_blacklist_and_whitelist,
                                             get_amount_links_selenium, save_lists_to_json,
                                             save_to_csv, save_to_json, SiteCheckResult,
                                             SiteCheckStatus)
from lab_5_scrapper.scrapper import Config, make_request


def get_requests_required_headers(url: str, config: Config) -> list:
    """
    Check if headers or cookies are needed.

    Args:
        url (str): Site url
        config (Config): Config

    Returns:
        list: A list of headers
    """
    for headers_attempt in HEADERS_ATTEMPTS:
        try:
            tmp_config: Config = deepcopy(config)
            # pylint: disable=protected-access
            tmp_config._headers = {key: value for key, value in
                                   config._headers.items() if key in headers_attempt}
            response = make_request(url, tmp_config)
            if response.status_code == 200:
                return headers_attempt
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass

    return ['ERROR']


def is_site_dynamic(url: str, config: Config, headless: bool = True) -> SiteCheckStatus:
    """
    Check dynamic site or not.

    Check if dynamic by more links loading in
    when scrolling and new page loading when clicking 'show more'.

    Args:
        url (str): Site url
        config (Config): Config
        headless (bool): Headless or not

    Returns:
        SiteCheckStatus: Site status
    """
    print('\tdynamic checks')

    DIST_PATH.mkdir(exist_ok=True)

    # Check 1: if no links in HTML we get with standard GET -> dynamic
    try:
        response = make_request(url, config)

        print(f'\t\tplain GET: {response.status_code}')

        soup = bs.BeautifulSoup(response.text, 'html.parser')

        if not soup.find_all('a'):
            return SiteCheckStatus(CheckStatuses.DYNAMIC, 'empty HTML using requests')
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        pass

    # Check 2: if number of links after scrolling is bigger than before -> dynamic
    headers = ['user-agent', 'accept', 'accept-encoding', 'accept-language', 'cookie']
    driver = create_driver(config, headers=headers, is_headless=headless, timeout=30)

    try:
        driver.get(url)
        print('\t\topened Chrome')
    except (TimeoutException, WebDriverException):
        return SiteCheckStatus(CheckStatuses.ERROR, 'unable to load the page')

    time.sleep(5)  # Wait for page to fully load. Otherwise, it scrolls before page fully loads

    driver.implicitly_wait(5)
    print('\t\tafter sleeps')

    links_before_count = get_amount_links_selenium(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        WebDriverWait(driver, 6).until(
            lambda browser: get_amount_links_selenium(driver) > links_before_count + 3)
    except (TimeoutException, WebDriverException):
        pass

    driver.implicitly_wait(5)
    print('\t\tready for links check')

    links_after_count = get_amount_links_selenium(driver)
    if links_after_count > links_before_count + 3:
        if driver.current_url != url:
            return SiteCheckStatus(CheckStatuses.HYBRID)
        return SiteCheckStatus(CheckStatuses.DYNAMIC, 'scrollable')
    return is_dynamic_with_buttons(url, driver)


def is_dynamic_with_buttons(url: str, driver: WebDriver) -> SiteCheckStatus:
    """
    Check if new page is loading when clicking 'show more'.

    Args:
        url (str): Site url
        driver (WebDriver): Driver

    Returns:
        SiteCheckStatus: Site status
    """
    with open(BUTTONS_PATH, encoding='utf-8') as file:
        links_texts = [x.strip() for x in file.readlines()]

    show_more_links = get_links_with_one_of_names(driver, links_texts)
    print(f'\t\tnumber of show more links: {len(show_more_links)}')
    if not show_more_links:
        return SiteCheckStatus(CheckStatuses.STATIC)

    links_before = get_amount_links_selenium(driver)

    for link in show_more_links:
        try:
            driver.execute_script("arguments[0].click();", link)
            print('\t\tclicked show more')
            time.sleep(2)
        except (ElementClickInterceptedException, WebDriverException):
            pass

        if get_amount_links_selenium(driver) > links_before:
            if driver.current_url == url:
                return SiteCheckStatus(CheckStatuses.DYNAMIC, 'clickable')
            return SiteCheckStatus(CheckStatuses.HYBRID)

    return SiteCheckStatus(CheckStatuses.STATIC)


def get_selenium_required_headers(url: str, config: Config, page_load_timeout: int = 60) -> list:
    """
    Check if headers are needed.

    Args:
        url (str): Site url
        config (Config): Config
        page_load_timeout (int): Page load timeout

    Returns:
        list: List of required headers
    """
    for headers_attempt in HEADERS_ATTEMPTS:
        driver = create_driver(config, headers=headers_attempt,
                               is_headless=True, timeout=page_load_timeout)
        try:
            driver.get(url)
            return headers_attempt
        except (TimeoutException, WebDriverException):
            pass

    return ['ERROR']


def get_links_with_one_of_names(driver: WebDriver, names: list) -> list[WebElement]:
    """
    Return the first element with one of the names.

    Args:
        driver (WebDriver): Driver
        names (list): Names

    Returns:
        list[WebElement]: The first element with one of the names
    """
    def validate_element(element: WebElement, search_name: str) -> bool:
        if search_name.lower().strip() not in element.text.lower() \
                or element.location['y'] < 20 or \
                len(re.sub(r"[\s\n\t\"\'.…]", "", element.text)) > len(search_name) * 1.5:
            return False

        return True

    result_elements = []

    all_possible_names = []
    for name in names:
        for name_variant in [name.lower(), name.upper(), name.capitalize()]:
            all_possible_names.append(f"{name_variant}")

    for name in all_possible_names:
        try:
            driver.implicitly_wait(0.1)
            for element in [*driver.find_elements(By.XPATH, f"//button[contains(.,'{name}')]"),
                            *driver.find_elements(By.XPATH, f"//a[contains(.,'{name}')]")]:
                if validate_element(element, name):
                    result_elements.append(element)
                    print(f"\t\t\tadded button {name} with text {element.text[:100]}...")
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

    # Check divs last
    for name in all_possible_names:
        try:
            driver.implicitly_wait(0.1)
            for element in [*driver.find_elements(By.XPATH, f"//div[contains(.,'{name}')]")]:
                if validate_element(element, name):
                    result_elements.append(element)
                    print(f"\t\t\tadded button {name} with text {element.text}")
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

    return result_elements


def validate_websites(urls: list, config: Config) -> None:
    """
    Save a dictionary with whether the url can be accessed.

    Args:
        urls (list): List of site urls
        config (Config): Config
    """
    responses = {}

    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        json_data = json.load(config_file)
        blacklist = json_data.get('blacklist', [])

    for url in urls:
        if url in blacklist:
            continue

        print(f'Validating {url}...')

        dynamic_check_result: SiteCheckStatus = is_site_dynamic(url, config)
        print(f'\tsite check: {dynamic_check_result.result}')
        if dynamic_check_result.msg:
            print(f'\tsite check msg: {dynamic_check_result.msg}')

        selenium_headers = []
        if dynamic_check_result.result == CheckStatuses.DYNAMIC:
            selenium_headers = get_selenium_required_headers(url, config)
            print(f'\tnumber of selenium headers: {len(selenium_headers)}')

        requests_headers = []
        if dynamic_check_result.result != CheckStatuses.ERROR:
            requests_headers = get_requests_required_headers(url, config)
        print(f'\tnumber of requests headers: {len(requests_headers)}')

        responses[url] = SiteCheckResult(
            requests_headers,
            selenium_headers,
            status=dynamic_check_result
        )

        save_to_csv(responses)
        save_to_json(responses)
        save_lists_to_json(define_blacklist_and_whitelist(responses))


def main() -> None:
    """
    Entrypoint for sites validation.
    """
    config = Config(CONFIG_PATH)
    config_urls = config.get_seed_urls()

    validate_websites(config_urls, config)


if __name__ == "__main__":
    main()
