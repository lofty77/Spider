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

from spider.sf_spider import SfSpider

#
# url = "https://www.baidu.com"

# @pytest.fixture
# def chrome_options(chrome_options):
#     chrome_options.add_argument('--headless')
#     return chrome_options


# def test_open_web(selenium, chrome_options):
#     selenium.get(link)


url = ("https://sf.taobao.com/item_list.htm?category=50025969&auction_source=0"
       "&province=%CC%EC%BD%F2&sorder=2&st_param=-1&"
       "auction_start_from=2019-07-21&auction_start_to=2019-10-21&spm=a213w.3064813.9001.2")

url_baidu = "https://www.baidu.com"


class TestSfSpider:

    def setup_class(self):

        self.item = {
            'id': 604063958339,
            'mnNotice': False,
            'credit': False,
            'itemUrl': '//sf-item.taobao.com/sf_item/604063958339.htm',
            'status': 'failure',
            'title': '天津滨海新区塘沽德景花园1-2-101房屋',
            'picUrl': '//img.alicdn.com/bao/uploaded/i2/TB1_GArgVY7gK0jSZKzqTWikpXa',
            'initialPrice': 1640000.0,
            'currentPrice': 1640000.0,
            'consultPrice': 2282000.0,
            'marketPrice': 0,
            'sellOff': True,
            'start': 1570759200000,
            'end': 1575943200000,
            'timeToStart': -5379580303,
            'timeToEnd': -195580303,
            'viewerCount': 7110,
            'bidCount': 0,
            'delayCount': 0,
            'applyCount': 0,
            'catNames': '',
            'collateralCatName': '',
            'xmppVersion': '1',
            'buyRestrictions': 0,
            'supportLoans': 0,
            'supportOrgLoan': 0
        }

    def teardown_class(self):
        pass

    def test_item_crawling(self):

        self.spider = SfSpider(
            debug=True, debug_pages=2, debug_items=2, head_less=True, url=url, file_name='demo')

        self.spider.executable = "/tmp/chromedriver/chromedriver"

        driver = self.spider._SfSpider__open_web()

        print("web title:" + driver.title)

        assert "拍卖" in driver.title

        status = self.spider._SfSpider__do_item_crawling(1, 0, self.item)

        assert status == True


if __name__ == '__main__':
    pytest.main(["-s", "test_sf_spider.py"])
