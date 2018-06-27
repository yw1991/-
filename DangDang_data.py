#encoding='utf-8'
import requests
from lxml import etree
import re
import time
import os
from multiprocessing import Pool
from config import *
from requests.exceptions import ConnectionError

#url= 'http://search.dangdang.com/?key=ai%D6%C7%C4%DC&category_path=01.00.00.00.00.00&page_index=1'
headers = {
'Cookie': '__permanent_id=20180529134606694275305799107137579; __visit_id=20180529134606717112102122970465069;'
          ' __out_refer=1527572767%7C!%7Cwww.baidu.com%7C!%7C; ddscreen=2;'
          ' NTKF_T2D_CLIENTID=guest146F8DE2-F34E-9D9F-0A1E-AA776D1E837D; '
          'nTalk_CACHE_DATA={uid:dd_1000_ISME9754_guest146F8DE2-F34E-9D,tid:1527573343518726}; producthistoryid=1251337959%2C1268362096;'
          ' MDD_sid=ba7541a352551c6738a52067de493384; MDD_permanent_id=20180529135806483252536170667952201;'
          ' MDD_province_id=-1; MDD_city_id=-1; MDD_area_id=-1; MDD_producthistoryids=1251337959; '
          '__rpm=s_112100.155956512835%2C155956512836..1527573172848%7Cs_112100.155956512835%2C155956512836..1527573783804; '
          '__trace_id=20180529140304556305343192963101795; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0',

'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'
}

def get_book_url(search,page):

    try:
            url = 'http://search.dangdang.com/?key={}&category_path=01.00.00.00.00.00&page_index={}'.format(search,
                                                                                                           1 * page+ 1)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                e1 = etree.HTML(response.text)
                href_lists = e1.xpath('//*[@id="component_0__0__6612"]/li/a/@href')
            else:
                return None
            print(href_lists)
            print(len(href_lists))

            return href_lists
    except ConnectionError:
        print("连接失败")
        return None


def get_book_data(url_lists,path):

        for href in url_lists:
            num = href.split("/", 3)[3].split(".", 2)[0]
            url_product = 'http://product.m.dangdang.com/{}.html'.format(num)
            url_detail = 'http://product.m.dangdang.com/detail{}-0-1.html?main_pid=&product_medium=0&category_id=7353&pod_pid=&category_path=01.54.12.00.00.00'.format(num)
            try:
                response1 = requests.get(url_product, headers=headers)
                if response1.status_code == 200:
                    e1 = etree.HTML(response1.text)
                else:
                    return None
                response2 = requests.get(url_detail, headers=headers)
                if response2.status_code == 200:
                    e2 = etree.HTML(response2.text)
                else:
                    return None
            except ConnectionError:
                print("连接失败")
                return None

            title = e1.xpath('/html/body/section[1]/article/text()')

            result1 = e2.xpath('/html/body/section[2]/p/text()')
            result2 = e2.xpath('/html/body/section[2]/text()')
            result3 = e2.xpath('/html/body/section[2]/div/text()')
            result4 = e2.xpath('/html/body/section[2]/div[2]/div[2]/text()')
            result5 = e2.xpath('/html/body/section[2]/div[5]/p/text()')
            result6 = e2.xpath('/html/body/section[2]/div[4]/div[2]/text()')
            result7 = e2.xpath('/html/body/section[2]/div[2]/p/text()')
            result8 = e2.xpath('/html/body/section[2]/div/p/text()')

            result = result1 + result2 + result3 + result4 + result5 + result6 + result7 + result8

            print(title)
            title_name = ''.join(title)
            titlename  = re.sub('[/,*]','',title_name)
#注意把'w'换成'a'
            name = '{}.txt'.format(titlename)
            filename = os.path.join(path,name)
            filename.replace('\\','/')
            print(filename)
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    for i in result:
                        i_result = ''.join(i)
                        # print(i_result)
                        f.write(i_result + '\n')
            except OSError:
                return  None


def main(page):
    print(page)
    title = KEYWORD
    path = 'C:/Users/Administrator/Desktop/{}'.format(title)
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    urls = get_book_url(title,page)
    get_book_data(urls,path)
    print("===============================结束========================================")


if __name__  == '__main__':

   pool = Pool()
   groups = ([x  for x in range(GROUP_START, GROUP_END+1)])
   print(groups)
   pool.map(main,groups)
   pool.close()
   pool.join()

