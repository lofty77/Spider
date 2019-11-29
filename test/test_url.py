from nose.tools import assert_equal

import pytest

import sys

sys.path.append('../')

from spider import url


def test_get_chinese_city():

    city_chinese = url.get_chinese_city("tj")

    assert_equal(city_chinese, "天津")


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--headless')
    return chrome_options


def test_open_web(selenium, chrome_options):
    selenium.get('http://www.baidu.com')


if __name__ == '__main__':
    print(sys.path)
