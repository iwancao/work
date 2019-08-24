from bs4 import BeautifulSoup
import requests
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

URL= "http://www.taikoolisanlitun.com/zh-CN/Shopping/ByFirstLetter"

from urllib.parse import urlencode

def get_brand(brand_value_key):
    url= 'http://www.taikoolisanlitun.com/files/taikooli/SLTAjax/BrandHandler.ashx?action=getBrand&letter=0&itemid='+ brand_value_key
    headers = {
        'Host': 'www.taikoolisanlitun.com',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://www.taikoolisanlitun.com/zh-CN/Shopping/ByFirstLetter',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    try:
        # print("URL:", url)
        # print("HEADERS: ", headers)
        response= requests.get(url, headers= headers)
        if response.status_code ==200:
            # print(response)
            return response.text
    except requests.ConnectionError as e:
        print("Error:" , e.args)


def go_through_page(url, sheet):
    wb_data = requests.get(URL)
    print(wb_data.status_code  , "  |  ", wb_data.encoding)

    page= BeautifulSoup(wb_data.content,'lxml')


    # print(page)
    count= 1
    for brand in page.find_all(name= 'div', attrs={'class': 's'}):
        try:
            brand_value_key= brand.attrs['data-value']
            print("Retrieving brand key value is ", brand_value_key, "...")
            content= get_brand(brand_value_key)
            brand_page= BeautifulSoup(content,'lxml')
            try:
                title=brand_page.find(name='h1').string
                intro= brand_page.find(name='p').string.strip('\n')
            except AttributeError:
                pass
            print("品牌：", title)
            print("介绍：", intro)

            contact=''
            for i, child in enumerate(brand_page.find(name='h3').children):
                try:
                    contact= contact+ child.string+ ' '
                except TypeError:
                    # DO nothing
                    pass
            print("电话：", contact )

            sheet.write(count,0, title)
            sheet.write(count,1, intro)
            sheet.write(count,2, contact)
            
            title=''
            intro=''
            contact=''
            
            count= count+1
        except KeyError:
            print("Ignore: ", brand)

    print("Total ", count, "brands found")

rb = xlrd.open_workbook('太古里品牌入驻清单.xls', formatting_info=True)
wb= xl_copy(rb)
try:
    sheet = wb.add_sheet('北京三里屯')
except Exception:
    print("WARNING: Sheet[北京三里屯] 已经存在，覆盖其内容")
    sheet= wb.get_sheet('北京三里屯')

sheet.write(0,0, "品牌")
sheet.write(0,1, "介绍")
sheet.write(0,2, "联系方式")
go_through_page(URL, sheet)
wb.save('太古里品牌入驻清单.xls')