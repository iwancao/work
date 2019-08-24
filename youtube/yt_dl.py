#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import youtube_dl
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'ascii'])


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
	'playliststart': 1,
	'playlistend': 10,
	'outtmpl': '%(release_date)s%(creator)s%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

# sys.setdefaultencoding('utf-8')

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/channel/UC-ayKOXvIcatt5VocwTrU9Q/'])