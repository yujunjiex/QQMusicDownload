# coding: UTF-8
"""QQ音乐api"""


class QQMusicAPI:
    search_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    single_song_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg' \
                      '?data={{"comm":{{"ct":24,"cv":0}},"songinfo":{{"method":"get_song_detail_yqq",' \
                      '"param":{{"song_type":0,"song_mid":\"{}\","song_id":0}},' \
                      '"module":"music.pf_song_detail_svr"}}}}'

    album_pic_url = 'http://imgcache.qq.com/music/photo/album_300/{}/300_albumpic_{}_0.jpg'  # 两个参数为albumid%100, albumid

    fcg_url = 'http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg?json=3&guid=5150825362&format=json'
    download_format_url = "{}/{}{}.{}?vkey={}&guid=5150825362&fromtag=1"

    smart_box_url = 'https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg?key={}'  # 搜索关键字联想

    # 音乐品质
    domain = ['http://dl.stream.qqmusic.qq.com/', 'http://streamoc.music.tc.qq.com/']
    quality = {'M800': 'mp3', 'M500': 'mp3', 'C400': 'm4a'}

    def __init__(self):
        if self.__class__ == QQMusicAPI:
            raise NotImplementedError("Cannot create object of class QQMusicAPI")

