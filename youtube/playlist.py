# -*- coding: UTF-8 -*-
import sys, os
import time, datetime

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

if __name__ == "__main__":
    now= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')[:10]
    yesterday= (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d')
    gen_playlist("C:/Download/News/", now, yesterday)
