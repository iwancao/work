# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import urllib
import time, datetime
import json
import requests

import sys, os

import re
import youtube_dl
import pickle
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf-8'])

def esc(code=0):
    return f'\033[{code}m'

'''
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色

显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见

例子：
\033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
'''
def gen_playlist(root_dir, today, yesterday):
    dirs = os.listdir(root_dir)
    if not dirs:
        pint("No files found in "+ root_dir)
        return

    playlist= open(root_dir+ today+ "-news.dpl", "w+", encoding='utf8')
    playlist.write("DAUMPLAYLIST\n")
    id= 1

    dirs = sorted(dirs, key=lambda x: os.path.getctime(os.path.join(root_dir, x)), reverse=True) # 按照时间顺序排序

    for file in dirs:
        if (file.find(today) > -1 or file.find(yesterday) > -1) and file[-4:]=='.mp3':
            playlist.write("{}*file*{}\n{}*played*0\n".format(id, root_dir+file, id))
            id+= 1

    playlist.close()
    os.system("\"C:/iwan/Tools/PotPlayer 1.7.327/PotPlayerMini.exe\" {}{}-news.dpl".format(root_dir, today))

channels = {
    "洛杉矶华人资讯网How视频": 'UC-ayKOXvIcatt5VocwTrU9Q',
    #"SHA SA 萨莎 Саша": 'UC7Ky7FjJBI7ojx2Yqz2pkNQ',
    #"寒梅视角MEI HAN": 'UC-8fdTrDRgiJhSq3wRsaF-g',
    "局势君": 'UC4JKWRLYoyM3DCHuEh8IOfg',
    "中国人": 'UCMXOcEbl9nXgJRrQZBn6C0w',
    "Guan Video观视频工作室": 'UCYfJG6cGfW84FVLuy7semEg',
    "战忽局小助理": 'UCENGuKqPb7WojKuishb1OkQ',
    "無色覺醒": 'UCuCELS5-48uP1plTxlOJZQQ'
    }

class YBChannel:
    def __init__(self, channels, dump_path):
        self.channels= channels
        self.dump_path= dump_path
        self.app_key = 'AIzaSyAqvAyna-RGORV37qmiAkF7UTNXy9Lji5A' # Get from https://console.developers.google.com/apis/
        self.count = 0


    def search_channel(self, channel_id, t1, t2):
        first_url = 'https://www.googleapis.com/youtube/v3/search?' + 'key={}&channelId={}&part=snippet,id&publishedAfter={}&publishedBefore={}&order=date&maxResults=25'.format(self.app_key, channel_id, t1, t2)
        url = first_url

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        while True:
            print("[Main]", url)
            req = urllib.request.Request(url= url, headers= headers)
            page = urllib.request.urlopen(req).read()
            result = json.loads(page, encoding="utf-8")
            for i in result['items']:
                try:
                    self.get_videos_info(i['id']['videoId'])#获取作品ID
                except:
                    pass

            try:
                next_page_token = result['nextPageToken']#获取下一页作品
                url = first_url + '&pageToken={}'.format(next_page_token)
            except:
                print("---------------------------------------------------")
                break

    def get_videos_info(self, id):#获取作品信息
        url = 'https://www.googleapis.com/youtube/v3/videos'
        query = ''

        results = requests.get(url, params={'id': id, 'maxResults': 25, 'part': 'snippet,statistics',
                                               'key': self.app_key})
        page = results.content
        videos = json.loads(page, encoding="utf-8")['items']
        for video in videos:
            title= video['snippet']['title'][:30] #截断为30个字符
            when= video['snippet']['publishedAt'][:10] # + "-{:0>2d}".format(self.count+1)
            id= video['id']

            file_name= self.dump_path+ re.sub(r"[\%\!\.\/\\\:\*\?\"\<\>\|]", "_", '[{}]{}'.format(when, title))+ '.mp3'
            # 把所有奇怪的字符，% ! . / \ : * ? " < > | 都替换成 _
            print('Dumping '+ file_name)

            ydl_opts = {
                'format': 'bestaudio/best',
            	'outtmpl': file_name,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['https://www.youtube.com/watch?v={}'.format(id)])
                self.count+=1

    def update(self, t1, t2):
        ch_names= list(self.channels.keys())
        ch_ids= list(self.channels.values())

        for i in range(len(ch_names)):
            print("Starting searching channel :", ch_names[i])
            self.search_channel(ch_ids[i], t1, t2)

        return self.count

if __name__ == "__main__":
    if len(sys.argv)> 1:
        dump_path= sys.argv[1]
    else:
        dump_path= "C:/Download/News/"

    c = YBChannel(channels, dump_path)
    now= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    yesterday= (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d')+ now[10:]

    print("Starting update news for {} to {}...".format(now[:10], dump_path))

    count= c.update(yesterday, now)
    if count>0:
        print("Total [{}] news updated".format(count))
    else:
        print("No news updates for today")

    key= input("Press p to play the news, other key to quit... ")
    if key=='p' :
        gen_playlist(dump_path, now[:10], yesterday[:10])
