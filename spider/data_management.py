import time
import csv
import re
from enum import Enum, unique
import pandas as pd


@unique
class Data(Enum):

    # release
    name = "中标人"
    year = "年份"
    month = "月份"
    start_time = "拍卖开始"
    end_time = "拍卖结束"
    times = "拍卖次数"
    title = "房屋地址"
    district = "区域"
    loadStatus = "贷款"
    originPrice = "市场评估价(万)"
    currentPrice = "当前价(万)"
    area = "建筑面积(平方米)"
    discount = "折扣(当前价/市场评估价)"
    unit = "单价(万)"
    bidCount = "举牌次数"
    delayCount = "举牌延迟次数"
    applyCount = "报名人数"
    unitName = "法院名字"
    itemUrl = "网页链接"

    # debug
    areaA = "候选面积1(平方米)"
    areaB = "后面面积2(平方米)"
    id = "拍品编号"
    status = "拍卖状态"
    consultPrice = "评估价(元)"
    marketPrice = "市场价(元)"
    supportLoans = "普通贷款"
    supportOrgLoan = "法服贷款"
    start = "拍卖开始时间戳"
    end = "拍卖结束时间戳"


class DataManagement:
    def __init__(self, file_name):
        self.data = {}

        self.file_name = file_name

        self.head = []
        for data in Data:
            self.head.append(data.value)

        self.__open_file()

    def __process_attri_name(self, attribute, data):
        index = data.find("通过")
        data = data[4:index]
        self.data[attribute] = data

        return data

    def __process_attri_area(self, attribute, data):
        left = data.find("建筑面积")
        if(left != -1):
            size = data[(left + 4): (left + 22)]
            areas = re.findall(r"\d+\.\d*", size)
            self.data[attribute] = areas[0] if areas else 0
        else:
            self.data[attribute] = 0

        return self.data[attribute]

    def __process_attri_times(self, attribute, data):
        keyword_postion = data.find("卖")
        if(keyword_postion != -1):
            data = data[1:keyword_postion + 1]
        else:
            data = "no content"

        self.data[attribute] = data

        return data

    def __process_attri_common(self, attribute, data):
        self.data[attribute] = data

    def __process_attri_url(self, attribute, data):
        url = "https:" + data
        self.data[attribute] = url

    def __clac_data(self):
        #
        if (int(self.data[Data.consultPrice.name]) > 0):
            originPrice = self.data[Data.consultPrice.name]
        else:
            originPrice = self.data[Data.marketPrice.name]
        #
        if (int(originPrice) == 0):
            self.data[Data.discount.name] = "error"
        else:
            self.data[Data.discount.name] = float("%.2f" % float(
                int(self.data[Data.currentPrice.name]) / originPrice))

       # change unit to from RMB yuan to  RMB Wan
        self.data[Data.originPrice.name] = float(
            "%.2f" % float(int(originPrice) / 10000))
        self.data[Data.currentPrice.name] = float(
            "%.2f" % float(int(self.data[Data.currentPrice.name]) / 10000))

      # set area
        if(float(self.data[Data.areaA.name]) > 0):
            self.data[Data.area.name] = self.data[Data.areaA.name]
            self.data[Data.unit.name] = float("%.2f" % float(
                int(self.data[Data.currentPrice.name]) / float(self.data[Data.area.name])))
        elif(float(self.data[Data.areaB.name]) > 0):
            self.data[Data.area.name] = self.data[Data.areaB.name]
            self.data[Data.unit.name] = float("%.2f" % float(
                int(self.data[Data.currentPrice.name]) / float(self.data[Data.area.name])))
        else:
            self.data[Data.area.name] = 0
            self.data[Data.unit.name] = 0

        ## start_time, end_time
        start = int(int(self.data[Data.start.name]) / 1000)
        self.data[Data.start_time.name] = str(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))

        end = int(int(self.data[Data.end.name]) / 1000)
        self.data[Data.end_time.name] = str(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)))

        # set year, month
        date_start = self.data[Data.start_time.name]
        data_split = date_start.split("-", 2)
        self.data[Data.year.name] = data_split[0]
        self.data[Data.month.name] = data_split[1]
        # set load
        if int(self.data[Data.supportLoans.name]) == 0 and int(self.data[Data.supportOrgLoan.name]) == 0:
            self.data[Data.loadStatus.name] = "不支持"
        elif int(self.data[Data.supportLoans.name]) == 1 and int(self.data[Data.supportOrgLoan.name]) == 1:
            self.data[Data.loadStatus.name] = "支持(法服&普通)"
        elif int(self.data[Data.supportOrgLoan.name]) == 1:
            self.data[Data.loadStatus.name] = "支持(法服)"
        else:
            self.data[Data.loadStatus.name] = "支持(普通)"

        # district
        address = self.data[Data.title.name]
        city_pos = address.find("市")
        district_pos = address.find("区")

        if city_pos > 0 and district_pos > 0:
            self.data[Data.district.name] = address[city_pos +
                                                    1:district_pos + 1]
        elif city_pos == -1 and district_pos > 0:
            city_pos = address.find("天津")
            if city_pos > -1:
                self.data[Data.district.name] = address[city_pos +
                                                        2:district_pos + 1]
            else:
                self.data[Data.district.name] = address[0:district_pos + 1]
        else:
            self.data[Data.district.name] = "未知区"
        ###

    def set_data(self, attribute, data):
        if(attribute == Data.name.name):
            self.__process_attri_name(attribute, data)
        elif(attribute == Data.areaA.name or attribute == Data.areaB.name):
            self.__process_attri_area(attribute, data)
        elif(attribute == Data.times.name):
            self.__process_attri_times(attribute, data)
        elif(attribute == Data.itemUrl.name):
            self.__process_attri_url(attribute, data)
        else:
            self.__process_attri_common(attribute, data)

    def get_data(self, attribute):
        return self.data[attribute]

    def __open_file(self):
        self.csv_file = open(self.file_name + ".csv", "w+")
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(self.head)

    def write_file(self):

        self.__clac_data()

        row = tuple(self.data[d.name] for d in Data)

        self.writer.writerow(row)

    def close_file(self):
        self.csv_file.close()
        csv = pd.read_csv(self.file_name + ".csv", encoding='utf-8')

        # debug excel
        csv.to_excel(self.file_name + "_debug.xlsx", sheet_name='data')

        # realse excel
        relase_column = list(self.head)
        relase_column.remove(Data.areaA.value)
        relase_column.remove(Data.areaB.value)
        relase_column.remove(Data.id.value)
        relase_column.remove(Data.status.value)
        relase_column.remove(Data.consultPrice.value)
        relase_column.remove(Data.marketPrice.value)
        relase_column.remove(Data.supportLoans.value)
        relase_column.remove(Data.supportOrgLoan.value)
        relase_column.remove(Data.start.value)
        relase_column.remove(Data.end.value)

        csv.to_excel(self.file_name + "_release.xlsx",
                     sheet_name='data', columns=relase_column)


if __name__ == '__main__':
    pass
