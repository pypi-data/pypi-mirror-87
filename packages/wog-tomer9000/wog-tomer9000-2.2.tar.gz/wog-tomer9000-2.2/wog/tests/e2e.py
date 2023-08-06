from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', action='store', help='Enter URL to test',
                    required=False, default='127.0.0.1:1000')
parser.add_argument('--driver', action='store', help='Enter selenium driver location',
                    required=False, default=r"C:\Users\tomer9000\chromedriver.exe")
arg = parser.parse_args()

def test_scores_service(app_url, driver_location):
    driver = webdriver.Chrome(fr"{driver_location}")
    try:
        driver.get(f"http://{app_url}/")
        q = driver.find_element_by_id("score")
        num_q = int(q.text)
        driver.close()
        print(num_q)
        return (num_q >= 1 or num_q <= 1000)
    except WebDriverException:
        driver.close()
        print(f"Website {app_url} isn't reachable")

def main_function(app_url, driver_location):
    if test_scores_service(app_url, driver_location):
        return 0
    return -1

print(main_function(arg.url, arg.driver))
