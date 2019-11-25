
import datetime
import sys

from sf_spider import SfSpider
from url import generate_crawl_link
# if debug mode.  Debug = True. if Release mode, Debug = False.
G_Debug = True
G_Chrome_Hide = True

G_Debug_Pages = 2
G_Debug_Items = 2

G_File_Name = 'tianjin'


# will bid
# crawl_link = ("https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.60.53db26cdCGMLqt&category=50025969"
#                    "&auction_source=0&province=%CC%EC%BD%F2&sorder=1&st_param=-1&auction_start_seg=-1")
# #done bid
# crawl_link = ("https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.26.294826cdrtlKJJ&category=50025969&auction_source=0"
#              "&city=&province=%CC%EC%BD%F2&sorder=2&st_param=-1&auction_start_seg=-1")
#
# crawl_link = ("https://sf.taobao.com/item_list.htm?category=50025969&auction_source=0&province=%CC%EC%BD%F2&sorder=2"
#            "&st_param=-1&auction_start_seg=&auction_start_from=2017-02-01&auction_start_to=2017-02-20&&spm=a213w.3064813.9001.2")

# crawl_link = ("https://sf.taobao.com/item_list.htm?category=50025969&auction_source=0"
#              "&province=%CC%EC%BD%F2&sorder=2&st_param=-1&"
#              "auction_start_from=2019-07-21&auction_start_to=2019-10-21&spm=a213w.3064813.9001.2")


if __name__ == '__main__':

  print(sys.path)

  crawl_link = generate_crawl_link()

  start = datetime.datetime.now()
  print("start : {0}".format(start))

  sf = SfSpider(G_Debug, G_Debug_Pages, G_Debug_Items,
                G_Chrome_Hide, crawl_link, G_File_Name)

  sf.do_crawling()

  end = datetime.datetime.now()
  print("end : {0}".format(end))
  print("duration: {0}".format(end - start))
