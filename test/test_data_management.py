import pytest
from nose.tools import assert_equal

import sys
sys.path.append('../')

from spider.data_management import DataManagement


class TestDataManagement:

  def setup_class(self):
    self.dm = DataManagement("demo_file")

  def teardown_class(self):
    pass

  def test_find_name(self):
    data = "用户姓名流拍通过"

    attribute = "none"

    assert_equal("流拍",self.dm._DataManagement__process_attri_name(attribute, data))


if __name__ == '__main__':
  pytest.main(["-s", "test_data_management.py"])
