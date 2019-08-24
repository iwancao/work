from bs4 import BeautifulSoup
import requests
import time

from urllib.parse import urlencode


def get_girl(id):
    URL= "http://www.mm523.com/meitu/"
    headers = {
        'Host':	'www.mm523.com',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': '__51cke__=; Hm_lvt_fa76e2afb22fc92b15cc4e74eaa2a264=1550320231; nxzphecookieclassrecord=%2C10%2C15%2C9%2C; __tins__19810179=%7B%22sid%22%3A%201550320230176%2C%20%22vd%22%3A%2033%2C%20%22expires%22%3A%201550323049990%7D; __51laig__=33; Hm_lpvt_fa76e2afb22fc92b15cc4e74eaa2a264=1550321250',
        'Connection': 'keep-alive=false',
    }

    url= URL+str(id)+'/'

    print("Trying ...", url)

    count= 0
    try:
        response= requests.get(url, headers= headers)
        # print(response)
        if response.status_code ==200:
            # print("Found girl page at ", url)
            page= BeautifulSoup(response.content,'lxml')
            girl= page.find(name= 'h1')
            # print(girl)
            if girl== None:
                print("哎呀，没有标题")
                title= 'No Name'
                return
            title= girl.text
            print('找到女孩...', title)
            picbox= page.find(name='div',  attrs={'class': 'picsbox picsboxcenter'})
            if picbox== None:
                print("哎呀，没有照片")
                return
            for i, child in enumerate(picbox.descendants):
                if child.name == 'img':
                    file= child.attrs['lazysrc']
                    file_name= 'c:\\temp\\meitu\\'+ title+ '-'+ str(count+1)+ '.png'
                    print("正在抓取文件... ", file_name)
                    pic = requests.get(file)
                    with open(file_name, 'wb') as file:
                        file.write(pic.content)
                    count= count+1

        response.close()
    except requests.ConnectionError as e:
        print("Error:" , e.args)

    time.sleep(1)
    return count

count= 0
for i in range(9999):
    count= count+ get_girl(10000+i)
print("总共下载 ", count, "张图片")
