# coding=utf-8
import sys

cities = {
    'bj': '北京',
    'sh': '上海',
    'tj': '天津',
    'wh': '武汉',
}


def create_prompt_city_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    city_info = list()
    count = 0
    for en_name, ch_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if count % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city do you want to crawl?\n' + ''.join(city_info) + '\n' + 'input : '


def create_prompt_date_text(dateType):

    if dateType == "start":
        prompt = '\n' + 'which date do you want to start (e.g.: 2019-01-01) ?\n' + \
            '\n' + 'input start day: '
    else:
        prompt = '\n' + 'which date do you want to end (e.g.: 2019-01-01) ?\n' + \
            '\n' + 'input end day: '
    return prompt


def get_chinese_city(en):
    """
    拼音拼音名转中文城市名
    :param en: 拼音
    :return: 中文
    """
    return cities.get(en, None)


def get_chinese_city_gbk(en):

    city = get_chinese_city(en)

    city_gbk = repr(city.encode('gbk')).replace("\\x", "%")[2:-1].upper()

    return city_gbk


def get_city():
    city = None
    # 允许用户通过命令直接指定
    if len(sys.argv) < 2:
        print("Wait for your choice.")
        # 让用户选择爬取哪个城市的二手房小区价格数据
        prompt = create_prompt_city_text()

        city = input(prompt)

    elif len(sys.argv) == 2:
        city = str(sys.argv[1])
        print("City is: {0}".format(city))
    else:
        print("At most accept one parameter.")
        exit(1)

    chinese_city = get_chinese_city(city)
    if chinese_city is not None:
        message = 'OK, start to crawl ' + get_chinese_city(city)
        print(message)
    else:
        print("No such city, please check your input.")
        exit(1)
    return city


def get_date(dateType):

    prompt = create_prompt_date_text(dateType)

    date = input(prompt)

    return date


def generate_crawl_link():

    city_en = get_city()

    city_chinese_gbk = get_chinese_city_gbk(city_en)

    date_start = get_date("start")

    date_end = get_date("end")

    link1 = "https://sf.taobao.com/item_list.htm?category=50025969&auction_source=0&province="
    link2 = "&sorder=2&st_param=-1&auction_start_from="
    link3 = "&auction_start_to="
    link4 = "&spm=a213w.3064813.9001.2"

    link = link1 + city_chinese_gbk + link2 + date_start + link3 + date_end + link4

    return link


if __name__ == '__main__':

    print(generate_crawl_link())
