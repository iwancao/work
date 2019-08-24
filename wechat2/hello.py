import itchat
from itchat.content import TEXT, SHARING
import time
import sys
import urllib.request
from lxml import etree


class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w+", encoding= "utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def saveHTML(file, url):
    try:
        html = urllib.request.urlopen(url).read()
        file_name= file.replace('/', '_') + ".html"
        with open(file_name, "wb") as f:
            # 写文件用bytes而不是str，所以要转码
            f.write(html)
            print(file_name, " 成功保存到本地")
    except Exception as e:
        print("Error:" , e.args)
'''
## 消息类型

向注册方法传入的msg包含微信返回的字典的所有内容。

本api增加`Text`、`Type`（也就是参数）键值，方便操作。

itchat.content中包含所有的消息类型参数，内容如下表所示：

参数       |类型       |Text键值
:----------|:----------|:---------------
TEXT       |文本       |文本内容
MAP        |地图       |位置文本
CARD       |名片       |推荐人字典
NOTE       |通知       |通知文本
SHARING    |分享       |分享名称
PICTURE    |图片/表情  |下载方法
RECORDING  |语音       |下载方法
ATTACHMENT |附件       |下载方法
VIDEO      |小视频     |下载方法
FRIENDS    |好友邀请   |添加好友所需参数
SYSTEM     |系统消息   |更新内容的用户或群聊的UserName组成的列表
'''

@itchat.msg_register(TEXT)
def reply_msg(msg):
    print("收到一条信息：",msg['Content'])


@itchat.msg_register(SHARING, isMpChat=True)
def reply_msg(msg):
    #if msg['FromUserName']== '@cd44b079b0482331ad1bce2330d77658':
    print("公众号信息，来自发起者 ", msg['FromUserName'])
    parse(msg['Content'])

def login_after():
    mps = itchat.search_mps(name='云小石')
    if len(mps) > 0:
        print("找到公众号：", mps[0]['NickName'])

        for i in range(21):
            itchat.send_msg(str(i+1), toUserName=mps[0]['UserName'])
            print("Sending ", i+1, " to ", mps[0]['NickName'])
            time.sleep(5)

def parse(content):
    # 在这里做图文信息解析工作
    # 微信msg返回的是一个字典，其中最重要的部分是content， 里面的格式是XML
    # http://tool.oschina.net/codeformat/xml/ 试试这里格式化
    # content里面的核心内容在items里面，每个item有下面元素：
    # cover是封面图片链接
    # digest 是内容摘要，文字
    # title 是文章标题
    # url 网页链接

    parser = etree.XMLParser(strip_cdata=False) #这部很关键，CDATA内容不会被过滤
    root = etree.fromstring(content, parser)
    titles = root.xpath("//item/title")
    urls= root.xpath("//item/url")
    # 讲真，xpath太好用了，比beautifulSoup更加简洁

    count1= len(titles)
    count2= len(urls)
    if count1!= count2 or count1< 1:
        print("Cannt found enough items, Skip!")
        return

    for i in range(count1):
        # print("Title: ", titles[i].text, "\nLink: ", urls[i].text)
        saveHTML(titles[i].text, urls[i].text)


if __name__ == '__main__':
    sys.stdout = Logger()
    print("开始运行，查看log.txt文件")

    itchat.auto_login(hotReload=True, loginCallback=login_after)
    itchat.run()
