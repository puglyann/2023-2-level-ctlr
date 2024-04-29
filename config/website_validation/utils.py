"""
Utils for websites validation.
"""
# pylint: disable=import-error
import dataclasses
import json
from dataclasses import dataclass
from typing import Optional, Union

import pandas as pd
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config.website_validation.constants import (CheckStatuses, CSV_REPORT_PATH, DIST_PATH,
                                                 JSON_BLACKLIST_PATH, JSON_REPORT_PATH,
                                                 JSON_WHITELIST_PATH)
from lab_5_scrapper.scrapper import Config


@dataclass
class SiteCheckStatus:
    """
    Result of website check whether it is dynamic or not.
    """
    result: CheckStatuses
    msg: Optional[str] = None


@dataclass
class SiteCheckResult:
    """
    Total summary of site analysis.
    """
    requests_headers: list[str]
    selenium_headers: list[str]
    status: SiteCheckStatus


def define_blacklist_and_whitelist(site_results: dict[str, SiteCheckResult]) -> tuple:
    """
    Collect data for blacklist and whitelist.

    Args:
        site_results (dict[str, SiteCheckResult]): Site results

    Returns:
        tuple: Data for blacklist and whitelist
    """
    whitelist = []
    blacklist = []
    count_dynamic = 0
    count_static = 0
    count_hybrid = 0
    for site_result in site_results:
        if site_results[site_result].status.result == CheckStatuses.ERROR or \
                site_results[site_result].requests_headers == ['ERROR'] or \
                site_results[site_result].selenium_headers == ['ERROR']:
            blacklist.append(site_result)
            continue
        if site_results[site_result].status.result == CheckStatuses.DYNAMIC:
            count_dynamic += 1
        elif site_results[site_result].status.result == CheckStatuses.STATIC:
            count_static += 1
        elif site_results[site_result].status.result == CheckStatuses.HYBRID:
            count_hybrid += 1
        whitelist.append(site_result)

    return whitelist, blacklist, count_dynamic, count_static, count_hybrid


def save_lists_to_json(full_report: tuple) -> None:
    """
    Save blacklist and whitelist to JSON format.

    Args:
        full_report (tuple): Sites report
    """
    whitelist_dict = {'count_dynamic': full_report[2],
                      'count_static': full_report[3],
                      'count_hybrid': full_report[4],
                      'whitelist': full_report[0]}
    blacklist_dict = {'blacklist': full_report[1]}
    with open(JSON_WHITELIST_PATH, 'w', encoding='utf-8') as file:
        json.dump(whitelist_dict, file, indent=4)

    with open(JSON_BLACKLIST_PATH, 'w', encoding='utf-8') as file:
        json.dump(blacklist_dict, file, indent=4)


def save_to_json(site_results: dict[str, SiteCheckResult]) -> None:
    """
    Save report to JSON format.

    Args:
        site_results (dict[str, SiteCheckResult]): Site results
    """
    raw_dict = {key: dataclasses.asdict(value) for key, value in site_results.items()}
    with open(JSON_REPORT_PATH, 'w', encoding='utf-8') as file:
        json.dump(raw_dict, file, indent=4)


def save_to_csv(site_results: dict[str, SiteCheckResult]) -> None:
    """
    Save report to csv format.

    Args:
        site_results (dict[str, SiteCheckResult]): Site results
    """
    values = []
    for url, status in site_results.items():
        value = [url, status.status.result, status.status.msg]

        if status.requests_headers:
            if 'ERROR' not in status.requests_headers:
                value.append('YES')
            else:
                value.append('ERROR')
        else:
            value.append('NO')

        if status.selenium_headers:
            if 'ERROR' not in status.requests_headers:
                value.append('YES')
            else:
                value.append('ERROR')
        else:
            value.append('NO')

        values.append(value)

    data_frame = pd.DataFrame(values, columns=['URL', 'Type', 'Notes',
                                               'Requests_headers', 'Selenium_headers'])

    DIST_PATH.mkdir(exist_ok=True)
    data_frame.to_csv(CSV_REPORT_PATH)


def create_driver(config: Config, headers: Union[list, tuple] = (),
                  is_headless: bool = True, timeout: int = 30) -> Chrome:
    """
    Create driver for Selenium-based checks.

    Args:
        config (Config): Config
        headers (Union[list, tuple]): Headers
        is_headless (bool): Headless or not
        timeout (int): Timeout

    Returns:
        Chrome: Driver for Selenium-based checks
    """
    options = Options()
    if is_headless:
        options.add_argument('--headless')

    # for slow computers put timout to 1 minute
    options.add_experimental_option('extensionLoadTimeout', 60000)

    for header in headers:
        options.add_argument(f"{header}={config.get_headers().get(header)}")

    driver = Chrome(options=options)
    driver.set_page_load_timeout(timeout)
    return driver


def get_amount_links_selenium(driver: Chrome) -> int:
    """
    Extract number of links on current page.

    Args:
        driver (Chrome): Driver

    Returns:
        int: Number of links on current page
    """
    try:
        return len(driver.find_elements(By.TAG_NAME, 'a'))
    except (TimeoutException, WebDriverException):
        return 0
