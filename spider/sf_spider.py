import json
import time
import datetime
import platform
import os.path as osp

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from data_management import DataManagement, Data


def log(page_id, item_id, status, start):
    end = datetime.datetime.now()
    print("page id: {0}, item id: {1}, status:{2}, duration:{3}".format(
        page_id, item_id, status, end - start))


class SfSpider:

    def __init__(self, debug, debug_pages, debug_items, head_less, url, file_name):

        self.debug = debug
        self.debug_pages = debug_pages
        self.debug_items = debug_items
        self.url = url
        self.refresh_count = 0

        self.data = DataManagement(file_name)

        executable = ''

        if platform.system() == 'Windows':
            print('Detected OS : Windows')
            executable = '../chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print('Detected OS : Linux')
            executable = '../chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('Detected OS : Mac')
            executable = '../chromedriver/chromedriver_mac'
        else:
            raise OSError('Unknown OS Type')

        if not osp.exists(executable):
            raise FileNotFoundError(
                'Chromedriver file should be placed at {}'.format(executable))

        if(head_less):
            # set headless
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(
                options=chrome_options, executable_path=executable)
        else:
            self.driver = webdriver.Chrome(executable_path=executable)

        # Setup wait for later
        self.wait = WebDriverWait(self.driver, 10)

    def __wait_until(self, mode, value):
        try:
            if(mode == "CLASS_NAME"):
                self.wait.until(EC.presence_of_element_located(
                    (By.CLASS_NAME, value)))
            elif(mode == "XPATH"):
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, value)))
            else:
                return False
        except TimeoutException:
            print("time out {0}".format(TimeoutException))
            return False

        else:
            return True

    def __wait_and_click(self, mode, value, sleep_time):
        #  Sometimes click fails unreasonably. So tries to click at all cost.
        try:
            if(mode == "LINK_TEXT"):
                elem = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, value)))
            elif(mode == "CSS_SELECTOR"):
                elem = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, value)))
            elif(mode == "XPATH"):
                elem = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, value)))
            else:
                print('wait_and_click() error...')

            elem.click()
            time.sleep(sleep_time)
        except Exception as e:
            print('Click time out - {}'.format(value))
            if(self.refresh_count < 1):
                self.refresh_count += 1
                print('Refreshing browser...')
                self.driver.refresh()
                time.sleep(2)
                return self.__wait_and_click(mode, value, sleep_time)
            else:
                print('more than MAX refresh count..')
                self.refresh_count = 0
                return False

        self.refresh_count = 0
        return True

    def do_crawling(self):

        self.driver.get(self.url)

        assert len(self.driver.window_handles) == 1

        self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "page-total")))

        if(self.debug):
            pages = self.debug_pages
        else:
            pages = int(self.driver.find_element_by_class_name(
                "page-total").text)

        for page in range(1, pages + 1):
            self.__do_page_crawling(page)

        self.driver.quit()
        self.data.close_file()

    def __do_page_crawling(self, page):
        if(page > 1):
            self.__wait_and_click("LINK_TEXT", str(page), 1)

        self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "sf-pai-item-list")))
        jsonData = json.loads(self.driver.find_element_by_id(
            "sf-item-list-data").get_attribute('innerHTML'))
        page_data = jsonData["data"]

        if(self.debug):
            items = self.debug_items
        else:
            items = len(page_data)

        for item in range(items):
            item_data = page_data[item]

            start = datetime.datetime.now()

            self.data.set_data(Data.id.name, item_data[Data.id.name])
            self.data.set_data(Data.status.name, item_data[Data.status.name])
            self.data.set_data(Data.start.name, item_data[Data.start.name])
            self.data.set_data(Data.end.name, item_data[Data.end.name])
            self.data.set_data(Data.title.name, item_data[Data.title.name])
            self.data.set_data(Data.consultPrice.name,
                               item_data[Data.consultPrice.name])
            self.data.set_data(Data.marketPrice.name,
                               item_data[Data.marketPrice.name])
            self.data.set_data(Data.currentPrice.name,
                               item_data[Data.currentPrice.name])
            self.data.set_data(Data.bidCount.name,
                               item_data[Data.bidCount.name])
            self.data.set_data(Data.delayCount.name,
                               item_data[Data.delayCount.name])
            self.data.set_data(Data.applyCount.name,
                               item_data[Data.applyCount.name])
            self.data.set_data(Data.itemUrl.name, item_data[Data.itemUrl.name])
            self.data.set_data(Data.supportLoans.name,
                               item_data[Data.supportLoans.name])
            self.data.set_data(Data.supportOrgLoan.name,
                               item_data[Data.supportOrgLoan.name])

            self.__do_item_crawling(page, item)

            log(page, item, item_data["status"], start)

    def __do_item_crawling(self, page_id, item_id):

        self.__wait_and_click("CSS_SELECTOR", "#pai-item-" +
                              str(self.data.get_data(Data.id.name)), 1)

        # Wait for the new window or tab
        self.wait.until(EC.number_of_windows_to_be(2))
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

       # bid times
        if self.__wait_until("XPATH", "/html[1]/body[1]/div[3]/div[4]/div[1]/div[1]/h1[1]"):
            textContent = self.driver.find_element_by_xpath(
                "/html[1]/body[1]/div[3]/div[4]/div[1]/div[1]/h1[1]").get_attribute('textContent')
        else:
            textContent = "error"

        self.data.set_data(Data.times.name, textContent)

        # TODO: degfine new field

       # 变卖公告，竞买公告
        self.__wait_and_click(
            "CSS_SELECTOR", "#J_DetailTabMenu > li.current.first > a", 0.5)

        self.data.set_data(Data.areaA.name, self.driver.find_element_by_id(
            "J_NoticeDetail").get_attribute('textContent'))

        self.__wait_and_click("LINK_TEXT", "标的物介绍", 0.5)

        self.data.set_data(Data.areaB.name, self.driver.find_element_by_id(
            "J_desc").get_attribute('textContent'))

        if(self.data.get_data(Data.status.name) == "done"):

            if self.data.get_data(Data.start.name) > 1486432800000:   # 2017-2-7
                if self.__wait_and_click("LINK_TEXT", "竞价成功确认书", 0.5):
                    if self.__wait_until("CLASS_NAME", "content-wrap"):
                        name = self.driver.find_element_by_class_name(
                            "c-content").text
                    else:
                        name = "用户姓名无名氏通过"
                else:
                    name = "用户姓名无名氏通过"
            else:
                name = "用户姓名无名氏通过"
        elif(self.data.get_data(Data.status.name) == "failure"):
            name = "用户姓名流拍通过"
        else:
            name = "用户姓名即将开始通过"
        self.data.set_data(Data.name.name, name)

        self.data.write_file()
        self.driver.close()
        self.driver.switch_to.window(handles[0])


if __name__ == '__main__':
    pass
