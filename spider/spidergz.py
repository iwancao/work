from bs4 import BeautifulSoup
import requests
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

URL= "http://www.taikoohui.com/zh-CN/Shopping"
headers = {
    'Host': 'www.taikoohui.com',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type':	'application/json; charset=utf-8',
    'Referer': 'http://www.taikoohui.com/zh-CN/Shopping',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie':	'f5avrbbbbbbbbbbbbbbbb=DMJGPOACMJGEBPOMPBKIKHLBPODJBGPEIOMAJIFMEAEEEJHLBPKJEKHPLDPCDABDFAADOHHKOLJOJBIILALAPMOPGNNJGFFPLKFFCKBHKFLOOCLIILDNGKNBNMDAMFIJ; ASP.NET_SessionId=bhqy0xlg4lxru304boxxb2jh; sc_expview=0; tkh#lang=zh-CN; _ga=GA1.2.1733995353.1548948563; SC_ANALYTICS_GLOBAL_COOKIE=79250ef3ac02429eb8809cb393cee983|True; _gid=GA1.2.1386879653.1549117362; f5avrbbbbbbbbbbbbbbbb=BDLACEPDAJLODIBPDFIPKIAAOPBIHDBDGLGCCFCPKNKAJOBLAIKEMEENNALMMHKADFIDJBIJAJBCMDLOADPADOJBBNPBGGNKEDEGIGGCDACMOELNEDDAHHOFIKBEBLFN; Hm_lvt_6a4eb147fb4178d3487ad8d5aacb2e49=1548948562,1549117362,1549195626; Hm_lpvt_6a4eb147fb4178d3487ad8d5aacb2e49=1549203731',
    'Connection':	'keep-alive',
}

global count

from urllib.parse import urlencode

def get_string(node):
    text = ''
    for i, child in enumerate(node.descendants):
        try:
            text= text + child.string
        except Exception:
            pass
    return text

def analysis_brand(text, sheet):
    global count
    page= BeautifulSoup(text,'lxml')
    # print(page.dd.children)


    for brand in page.find_all(name= 'dd'):
        title=get_string(brand.contents[0])
        contact= get_string(brand.contents[3])
        intro= get_string(brand.contents[4])

        print("品牌：",title , "| 介绍 ：",intro , " | 联系：", contact )
        sheet.write(count,0, title)
        sheet.write(count,1, intro)
        sheet.write(count,2, contact)
        title=''
        intro= ''
        contact= ''
        count= count+1


def get_brands(page, sheet):
    url= 'http://www.taikoohui.com/files/taikoohui/ajax/AjaxShopping.ashx?method=getData&itemPath=%2Fsitecore%2Fcontent%2FHome%2FTaikooHui%2FShopping&pageIndex='+ str(page)+ '&firstQueryConditions=Brand&secondQueryConditions=All&isMobile=0'

    try:
        response= requests.get(url, headers= headers)
        stores= response.json().get('storeList')
        # print(url)
        # print(stores)
        if response.status_code ==200:
            analysis_brand(stores, sheet)
    except requests.ConnectionError as e:
        print("Error:" , e.args)



rb = xlrd.open_workbook('太古里品牌入驻清单.xls', formatting_info=True)
wb= xl_copy(rb)
try:
    sheet = wb.add_sheet('广州太古汇')
except Exception:
    print("WARNING: Sheet[广州太古汇] 已经存在，覆盖其内容")
    sheet= wb.get_sheet('广州太古汇')

sheet.write(0,0, "品牌")
sheet.write(0,1, "介绍")
sheet.write(0,2, "联系方式")

count= 1
for i in range(27):
    get_brands(i+1, sheet)
print("Total ", count, "brands found")
wb.save('太古里品牌入驻清单.xls')