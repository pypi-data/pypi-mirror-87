from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import sys
import argparse

# adding optional args, url of wog's score and driver of selenium-chrome
parser = argparse.ArgumentParser()
parser.add_argument('--url', action='store', help='Enter URL to test',
                    required=False, default='127.0.0.1:8777')
parser.add_argument('--driver', action='store', help='Enter selenium driver location',
                    required=False, default=r"C:\Users\tomer9000\chromedriver.exe")
arg = parser.parse_args()

def test_scores_service(app_url, driver_location):
    '''
    Test wog web service.
    :param app_url: URL where the wog web service runs.
    :param driver_location: selenium chromedriver location.
    :return: True if the score is between 1 to 1,000, else False
    '''
    if os.name == 'nt':
        # if os that runs e2e is Windows.
        driver = webdriver.Chrome(fr"{driver_location}")
        return _query_url(driver, app_url)
    elif os.name == 'posix':
        # If os that runs e2e is Unix-based.
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(fr"{driver_location}", chrome_options=chrome_options)
        return _query_url(driver, app_url)

def _query_url(driver_to_query, app_url):
    """
    Internal usage in order not to run it twice
    :param driver_to_query: chromedriver already loaded with the necessary parameters.
    :param app_url: URL where the wog web service runs.
    :return: True if the score is between 1 to 1,000, else False
    """
    try:
        driver_to_query.get(f"http://{app_url}/")
        q = driver_to_query.find_element_by_id("score")
        num_q = int(q.text)
        driver_to_query.close()
        return (num_q >= 1 and num_q <= 1000)
    except WebDriverException:
        driver_to_query.close()
        print(f"Website {app_url} isn't reachable")

def main_function(app_url, driver_location):
    """
    call our tests function.
    :param app_url: URL where the wog web service runs.
    :param driver_location: selenium chromedriver location.
    :return: -1 as an OS exit code if the tests failed and 0 if they passed.
    """
    if test_scores_service(app_url, driver_location):
        return sys.exit(0)
    return sys.exit(-1)

print(main_function(arg.url, arg.driver))
