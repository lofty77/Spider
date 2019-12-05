from nose.tools import assert_equal

import pytest
import sys
sys.path.append('../')

from spider import url


@pytest.fixture(scope="function")
def do_input():

    def _do_input(data):
        return data
    yield _do_input

    url.input = input


def test_get_city(do_input):
    url.input = lambda x: do_input("tj")
    output = url.get_city()
    assert_equal(output, "tj")


def test_get_chinese_city():

    city_chinese = url.get_chinese_city("tj")

    assert_equal(city_chinese, "天津")


def test_get_chinese_city_gbk():
    city_chinese_gbk = url.get_chinese_city_gbk("tj")

    assert_equal(city_chinese_gbk, "%CC%EC%BD%F2")


def test_get_date(do_input):
    # Override the Python built-in input method
    url.input = lambda x: do_input("2019-01-01")
    output = url.get_date("start")
    assert_equal(output, "2019-01-01")


if __name__ == '__main__':
    pytest.main(["-s", "test_url.py"])
