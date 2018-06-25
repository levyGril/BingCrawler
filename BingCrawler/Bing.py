# Bing 壁纸爬虫
# 可以批量获取
# url:
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1529900281759&pid=hp&video=1
#
# method： get
# n 最大可以设置为8，最多可以获取八天的数据
import urllib
import urllib.request
import ssl
import time
import json
import os.path


class BingBgDownLoader(object):

    _bing_url = "https://cn.bing.com/"
    _bing_interface = _bing_url+"HPImageArchive.aspx?format=js&idx=0&n=%d&nc=%d&pid=hp&video=1"
    _img_filename = '[%s%s][%s].%s'

    # 构造函数,进行初始化
    def __init__(self):
        super(BingBgDownLoader, self).__init__()
        ssl._create_default_https_context = ssl._create_unverified_context


    # 下载壁纸图片
    def download(self, num=1, local_path='./'):
        if num < 1:
            num = 1
        url = self._bing_interface%(num, int(time.time()))
        print(url)
        img_infos = self._get_img_info(url)

        for info in img_infos:
            print(self._get_img_filename(info))
            print(self._get_img_url(info))
            self._down_img(self._get_img_url(info), local_path+self._get_img_filename(info))

    # 从接口获取图片资源信息
    def _get_img_info(self, url):
        request = urllib.request.urlopen(url).read()
        bgObjs = json.loads(bytes.decode(request))
        return bgObjs['images']

    # 从接口获取图片文件名
    def _get_img_filename(self, img_info):

        zh_name = '' # 中文名

        pos = img_info['copyright'].index('(')
        if pos< 0:
            zh_name = img_info['copyright']
        else:
            zh_name = img_info['copyright'][0:pos] # 使用字符串的切片
        entmp = img_info['url']
        en_name = entmp[entmp.rindex('/')+1 : entmp.rindex('_ZH')]  # rindex('/') 从后往前找，也就是最后一个／
        ex_name = entmp[entmp.rindex('.')+1: len(entmp)] # 获取后缀名
        pix = entmp[entmp.rindex('_')+1:entmp.rindex('.')] # 分辨率

        # img_name = zh_name+en_name+pix+ex_name
        img_name = self._img_filename%(zh_name, en_name, pix, ex_name)
        return img_name

    # 得到图片资源的URL
    def _get_img_url(self, img_info):
        return self._bing_url+img_info['url']

    # 下载图片 https://cn.bing.com/az/hprichbg/rb/MODIS_ZH-CN14242381223_1920x1080.jpg
    def _down_img(self, img_url, img_pathname):
        img_data = urllib.request.urlopen(img_url).read()
        f = open(img_pathname, 'wb')
        f.write(img_data)
        f.close()
        print('save successfully, image: ', img_url)


if __name__ == '__main__':
    dl = BingBgDownLoader();
    dl.download(2)