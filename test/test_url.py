from nose.tools import assert_equal

import pytest
import sys
sys.path.append('../')

from spider import url


def test_get_chinese_city():

    city_chinese = url.get_chinese_city("tj")

    assert_equal(city_chinese, "天津")


def test_get_chinese_city_gbk():
    city_chinese_gbk = url.get_chinese_city_gbk("tj")

    assert_equal(city_chinese_gbk, "%CC%EC%BD%F2")


if __name__ == '__main__':
    pass
