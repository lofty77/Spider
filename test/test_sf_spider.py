from nose.tools import assert_equal

import pytest
import sys
sys.path.append('../')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--headless')
    return chrome_options


def test_open_web(selenium, chrome_options):
    selenium.get('http://www.baidu.com')


if __name__ == '__main__':
    pass
