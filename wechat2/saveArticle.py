import os
import time
import datetime
from urllib.request import Request, urlopen
from urllib import request
import re
class DownWx():
    def __init__(self):  # 构造函数
        super().__init__()
    # 保存图片
    def put_file_img(self,dir,image_url):
        #判断图片的保存类型 截取后4位地址 jpeg =png =jpg =gif
        exts = image_url[-4:]
        file_leixing = "." + exts.replace("=","")
        filename = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", image_url)#提取中文和数字
        try:
            print("[IMG]", image_url, filename +file_leixing)
            request.urlretrieve(image_url, filename +file_leixing)
        except:
            print(image_url,"下载失败")
        return "img/" + filename +file_leixing
    #开始下载文章
    def get_file_article(self,url,qcode=False):
        req = Request(url)
        response = urlopen(req)
        htmls = response.read().decode('utf-8', 'ignore')

        isExists = os.path.exists("/img")
        if not isExists:
            print('目录不存在')
            os.makedirs("/img")
        else:
            print('img 目录存在')
        #内容主体
        res = re.findall('<div class="rich_media_content " id="js_content">[\s\S]*?</div>', htmls)
        content = res[0] #内容主体
        # 所有图片
        res = re.findall('<img.*?data-src=[\'|\"](.*?(?:[\.?]))[\'|\"].*?[\/]?>',content)
        # <img.*?data-src=[\'|\"](.*?(?:[\.gif|\.jpg|\.png|\.jpeg|\.?]))[\'|\"].*?[\/]?>
        #  去除重复图片地址
        res = set(res)
        # 储存原地址和下载后地址
        old = []
        new = []
        for i in res:
            # 图片保存成功 替换地址
            print("[ORG]",i)
            old.append(i)
            new.append(self.put_file_img("/img",i))
        old.append('data-src')
        new.append('src')
        for i in range(len(old)):
            htmls = htmls.replace(old[i], new[i])  # 全部
            content = content.replace(old[i], new[i])  #只有主体的部分
        fp = open("test"+".html",'w',encoding='utf-8')  # 打开一个文本文件
        fp.write(htmls)  # 写入数据全部
        #fp.write(content)  # 写入数据 只有主体的部分
        fp.close()  # 关闭文件
if __name__ == '__main__':
    w = DownWx()
    url = 'http://mp.weixin.qq.com/s?__biz=MzI2MjE5Nzc3OQ==&mid=504084244&idx=8&sn=68261486b81cd63311797adc57062553&chksm=71b1d06846c6597ea48b83467c49e3bb1950c9f8fa46dce0dd74fd6445e7605f88822c003c2a&scene=20&xtrack=1#rd'
    w.get_file_article(url, True)
