import pytest
from selenium import webdriver
import platform
import os

if not os.environ["CHROMEDRIVER_PATH"]:
    CHROMEDRIVER_PATH="../../chromedriver"

if platform.system() == "Darwin":
    CHROME_PATH="../../Google\ Chrome.app"

CHROMEDRIVER_PATH_ABS=os.path.abspath(CHROMEDRIVER_PATH)

@pytest.fixture(scope="module")
def chrome_driver(request):
    chromedriver_path = '/path/to/chromedriver'
    chrome_path = '/path/to/chrome'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    chrome_options.add_argument("--headless")
    def teardown():
        driver.quit()

    request.addfinalizer(teardown)
    return driver
