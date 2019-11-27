from nose.tools import assert_equal

from Spider.spider import url


def test_get_chinese_city():

    city_chinese = url.get_chinese_city("tj")

    assert_equal(city_chinese, "天津")
