# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import urllib
import time, datetime
import json
import requests

import sys, os
import delegator # 子进程库

import re
import youtube_dl
import pickle
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf-8'])

from eliot import start_action, to_file

import colorama
'''
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL

'''
def color(s, color):
	return color+ s + colorama.Style.RESET_ALL

def gen_playlist(root_dir, today, yesterday):
    dirs = os.listdir(root_dir)
    if not dirs:
        print("No files found in "+ root_dir)
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
    # os.system("\"C:/iwan/Tools/PotPlayer 1.7.327/PotPlayerMini.exe\" {}{}-news.dpl".format(root_dir, today))
    delegator.run("\"C:/iwan/Tools/PotPlayer 1.7.327/PotPlayerMini.exe\" {}{}-news.dpl".format(root_dir, today), block= False) # 没有阻塞，直接退出

channels = {
    "洛杉矶华人资讯网How视频": 'UC-ayKOXvIcatt5VocwTrU9Q',
    #"SHA SA 萨莎 Саша": 'UC7Ky7FjJBI7ojx2Yqz2pkNQ',
    #"寒梅视角MEI HAN": 'UC-8fdTrDRgiJhSq3wRsaF-g',
    "局势君": 'UC4JKWRLYoyM3DCHuEh8IOfg',
    "中国人": 'UCMXOcEbl9nXgJRrQZBn6C0w',
    "Guan Video观视频工作室": 'UCYfJG6cGfW84FVLuy7semEg',
    "战忽局小助理": 'UCENGuKqPb7WojKuishb1OkQ',
	"洞察天下": 'UCMrOWtXrYPXtpTv9TQW8CiQ',
	"HKEECCO": 'UC3QkmBofoooHkJzWkyEHbyA',
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
            # print("[Main]", url)
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

        results = requests.get(url, params={'id': id, 'maxResults': 25, 'part': 'snippet,statistics',
                                               'key': self.app_key})
        page = results.content
        videos = json.loads(page, encoding="utf-8")['items']
        for video in videos:
            title= video['snippet']['title'][:30] #截断为30个字符
            when= video['snippet']['publishedAt'][:10] # + "-{:0>2d}".format(self.count+1)
            id= video['id']
            link= "https://www.youtube.com/watch?v={}".format(id)

            file_name= self.dump_path+ re.sub(r"[\%\!\.\/\\\:\*\?\"\<\>\|]", "_", '[{}]{}'.format(when, title))+ '.mp3'
            # 把所有奇怪的字符，% ! . / \ : * ? " < > | 都替换成 _
            print('Dumping '+ colorama.Fore.GREEN+ colorama.Style.BRIGHT+ file_name + colorama.Style.RESET_ALL)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'ignore-errors': True,
            	'outtmpl': file_name,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }


            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                with start_action(action_type="下载视频", url=link):
                	ydl.download([link])
            self.count+=1

    def update(self, t1, t2):
        ch_names= list(self.channels.keys())
        ch_ids= list(self.channels.values())

        for i in range(len(ch_names)):
            print("Starting searching channel :", colorama.Fore.YELLOW+ colorama.Style.BRIGHT+ ch_names[i]+ colorama.Style.RESET_ALL)
            self.search_channel(ch_ids[i], t1, t2)

        return self.count

if __name__ == "__main__":
    colorama.init()
    to_file(open("ybnews.log", "w"))

    if len(sys.argv)> 1:
        dump_path= sys.argv[1]
        if dump_path[-1]!= '/':
            dump_path+= '/'
        if os.path.exists(dump_path)== False:
            print("The {} does not exists, will create...".format(dump_path))
            os.makedirs(dump_path)
    else:
        dump_path= "C:/Download/News/"

    c = YBChannel(channels, dump_path)
    now= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    yesterday= (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d')+ now[10:]

    print("Starting update news for {} {} to {}{}...".format(colorama.Fore.RED+ colorama.Style.BRIGHT, now[:10], dump_path, colorama.Style.RESET_ALL))

    count= c.update(yesterday, now)
    if count>0:
        print("Total [{}] news updated".format(count))
    else:
        print("No news updates for today")

    key= input("Press p to play the news, other key to quit... ")
    if key=='p' :
        gen_playlist(dump_path, now[:10], yesterday[:10])
