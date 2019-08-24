from bs4 import BeautifulSoup
import requests
import xlrd, xlwt
from xlutils.copy import copy as xl_copy



URL= "http://www.soltklcd.com/zh-CN/Shopping"

def go_through_page(url, sheet):
    wb_data = requests.get(URL)
    print(wb_data.status_code  , "  |  ", wb_data.encoding)

    page= BeautifulSoup(wb_data.content,'lxml')

    data= page.find(name= 'ul', attrs={'id': 'logolistdata'})

    count= 1
    for i, brand in enumerate(data.children):
        title=brand.contents[3].string
        contact= brand.contents[5].string
        intro= brand.contents[7].string

        print("品牌：",title , "| 介绍 ：",intro , " | 联系：", contact )
        sheet.write(count,0, title)
        sheet.write(count,1, intro)
        sheet.write(count,2, contact)
        title=''
        intro= ''
        contact= ''
        count= count+1

    print("Total ", count, "brands found")

rb = xlrd.open_workbook('太古里品牌入驻清单.xls', formatting_info=True)
wb= xl_copy(rb)
try:
    sheet = wb.add_sheet('成都远洋太古里')
except Exception:
    print("WARNING: Sheet[成都远洋太古里] 已经存在，覆盖其内容")
    sheet= wb.get_sheet('成都远洋太古里')
sheet.write(0,0, "品牌")
sheet.write(0,1, "介绍")
sheet.write(0,2, "联系方式")
go_through_page(URL, sheet)
wb.save('太古里品牌入驻清单.xls')