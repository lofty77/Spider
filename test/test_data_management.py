import pytest
from nose.tools import assert_equal
import sys

sys.path.append('../')

from spider.data_management import DataManagement

from spider.data_management import Data


class TestDataManagement:

  def setup_class(self):
    self.dm = DataManagement("demo_file")
    self.data = Data

  def teardown_class(self):
    pass

  def test_find_name(self):
    data = "用户姓名流拍通过"

    attribute = self.data.name.name

    assert_equal(
        "流拍", self.dm._DataManagement__process_attri_name(attribute, data))

  def test_find_area(self):
    data = "我的建筑面积是多少啊138.50平方好的"
    attribute = self.data.area.name

    assert_equal(
        "138.50", self.dm._DataManagement__process_attri_area(attribute, data))

  def test_find_times(self):
    data = "[第一次拍卖]"
    attribute = self.data.times.name

    assert_equal(
        "第一次拍卖", self.dm._DataManagement__process_attri_times(attribute, data))


if __name__ == '__main__':
  pytest.main(["-s", "test_data_management.py"])
