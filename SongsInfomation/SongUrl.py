# coding: UTF-8
"""获取歌曲直链"""
from MusicAPI.QQMusic import QQMusicAPI as qq
from RequestsHelper import RequestsHelper as reqhelper
from SongsInfomation.KeyInfo import KeyInfo
from requests.exceptions import HTTPError


class SongUrl:
    domain = qq.domain
    quality = qq.quality
    reverse_quality = {"m4a": 'C400', "mp3": 'M500'}
    download_format_url = qq.download_format_url


    @classmethod
    def get_url_by_mid(cls, song_mid, quality=None):
        vkey = KeyInfo.get_vkey()
        if quality is not None:
            song_url = cls.download_format_url.format(cls.domain[0], cls.reverse_quality[quality], song_mid, quality, vkey)
            try:
                reqhelper.url_is_error(song_url)
            except HTTPError:
                return None
            else:
                return song_url
        else:

            for k, v in cls.quality.items():
                if k == 'M800':
                    song_url = cls.download_format_url.format(cls.domain[1], k, song_mid, v, vkey)
                else:
                    song_url = cls.download_format_url.format(cls.domain[0], k, song_mid, v, vkey)
                try:
                    reqhelper.url_is_error(song_url)
                except HTTPError:
                    continue
                else:
                    return song_url
        return None


if __name__ == '__main__':
    print(SongUrl.get_url_by_mid('000sU9jC3bN2dY', 'mp3'))
    print(SongUrl.get_url_by_mid('000sU9jC3bN2dY', 'm4a'))

