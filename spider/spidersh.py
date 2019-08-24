from bs4 import BeautifulSoup
import requests
import xlrd, xlwt
from xlutils.copy import copy as xl_copy



URL= "http://www.hkritaikoohui.com/brand-list.html"

def go_through_page(url, sheet):
    wb_data = requests.get(URL)
    print(wb_data.status_code  , "  |  ", wb_data.encoding)

    page= BeautifulSoup(wb_data.content,'lxml')


    # print(page)
    count= 1
    for brand in page.find_all(name= 'h4', attrs={'class': 'heading-6 shop-name'}):
        title=brand.string
        print("品牌：", title)
        sheet.write(count,0, title)
        title=''
        count= count+1
    print("Total ", count, "brands found")

    count= 1
    for brand in page.find_all(name= 'p', attrs= {'class': 'shop-info'}):
        intro=brand.string
        print("介绍：", intro)
        sheet.write(count,1, intro)
        intro=''
        count= count+1

    print("Total ", count, "intro found")


rb = xlrd.open_workbook('太古里品牌入驻清单.xls', formatting_info=True)
wb= xl_copy(rb)
try:
    sheet = wb.add_sheet('上海太古汇')
except Exception:
    print("WARNING: Sheet[上海太古汇] 已经存在，覆盖其内容")
    sheet= wb.get_sheet('上海太古汇')

sheet.write(0,0, "品牌")
sheet.write(0,1, "介绍")
sheet.write(0,2, "联系方式")
go_through_page(URL, sheet)
wb.save('太古里品牌入驻清单.xls')