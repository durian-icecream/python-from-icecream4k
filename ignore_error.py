import struct

import requests
from lxml import etree
from Crypto.Cipher import AES
from queue import Queue
import re
import os
from threading import Thread

class DaiNeiVideoSpider:
    def __init__(self):
        self.url='http://tts.tmooc.cn/studentCenter/toMyttsPage'
        self.headers = {
            'Cookie': 'ssss763527=0; cloudAuthorityCookie=0; tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; _qddaz=QD.rwf95u.l864tk.ka0g2ska; versionListCookie=WEBTN201805; defaultVersionCookie=WEBTN201805; versionAndNamesListCookie=WEBTN201805N22NWeb%25E5%2589%258D%25E7%25AB%25AF%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV05N22N763527; courseCookie=WEB; stuClaIdCookie=763527; isCenterCookie=yes; _qddab=3-wi4elm.kam6bsxw; TMOOC-SESSION=a6fccd7bd39948a58b11c0fd8d2f6235; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1590110207,1590127365,1590370039,1590391993; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1590393196; sessionid=a6fccd7bd39948a58b11c0fd8d2f6235|E_bfur9u0; JSESSIONID=E5D0EA0BEB8CB92C3B3B8537FF343EAA; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1590127413,1590370062,1590391990,1590397487; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1590397487',
            'Referer': 'http://uc.tmooc.cn/userCenter/toUserCoursePage',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        # self.queue01=Queue()
        # self.queue_ts=Queue()
    #解析一级页面获取所有假链接
    def parse_one(self):
        video_list=[]
        html = requests.get(url=self.url, headers=self.headers).content.decode('utf-8')
        parse_html = etree.HTML(html)
        # print(html)
        # 所有课程链接  76天课程链接
        #
        # ['http://tts.tmooc.cn/video/showVideo?menuId=678266&version=TSDTN201905',
         # 'http://tts.tmooc.cn/video/showVideo?menuId=678265&version=TSDTN201905',
        link_list = parse_html.xpath('//li[@class="sp"]/a/@href')
        # print(link_list)
        # print(len(link_list))
        for video in link_list[:]:
            video_list.append(video)
            # print(video_list)

        self.parse_two(video_list)


    # http: // videotts.it211.com.cn / tsd19040430am / tsd19040430am.m3u8
    # 解析二级界面从二级界面中找出m3u8链接
    def parse_two(self,video_list):
        for url in video_list:
            # print(link_list)
            # print(len(link_list))
            html=requests.get(url=url,headers=self.headers).content.decode('utf-8')
            parse_html = etree.HTML(html)
            # 每天上午  下午链接
            # active_WEB_WEB1805_N_NODE_DAY01_01.m3u8
            link_list01 = parse_html.xpath('//div[@class="video-list"]//p/@id')
            if len(link_list01)==0:
                pass
            # print(link_list01)
            for item in link_list01:
                # print(item)
                a=item.split('_')
                if len(a)>2:
                    last_url01 = a[1:]
                    last_url='_'.join(last_url01)
                    middle_url = last_url.split('.')[0]
                    # print(middle_url)
                    m3u8_url = 'http://c.it211.com.cn/' + middle_url + '/' + last_url
                    # self.queue01.put(m3u8_url)

                    # 拿到半天的链接后直接进行.ts文件解析
                    self.parse_m3u8(m3u8_url)

                else:
                    last_url=item.split('_')[1]
                    middle_url=last_url.split('.')[0]
                    # print(middle_url)
                    m3u8_url='http://c.it211.com.cn/'+middle_url+'/'+last_url
                    # self.queue01.put(m3u8_url)

                    #拿到半天的链接后直接进行.ts文件解析
                    self.parse_m3u8(m3u8_url)
    #
    #
    #
    def parse_m3u8(self,m3u8_url):
        ts_list=[]
        file=m3u8_url.split('/')[-1]
        dic_name=file.split('.')[0]
        html=requests.get(url=m3u8_url,headers=self.headers)
        # print(html)
        if html.status_code==404:
            # print('url或视频出现错误,跳过')
            with open('/Users/hanlong/Desktop/web视频/error.txt','a') as f:
                f.write('{}文件写入错误，已跳过'.format(m3u8_url))
            pass

        # print(html)
        else:
            html = requests.get(url=m3u8_url, headers=self.headers).text
            # print(html)
            parse_key = re.compile('URI="(.*?)"', re.S)
            key = parse_key.findall(html)[0]
            list01 = html.split('\n')
            for item in list01:
                if '.ts' in item:
                    #拿到每半天所有ts链接
                    ts_list.append(item)


            self.write(key,dic_name,ts_list)
    #
    def write(self,key,dic_name,ts_list):
        # pass

        # 获得密匙
        keys = requests.get(url=key, headers=self.headers).content
        # 创建文件夹用来存放每半天的视频
        dir = '/Users/hanlong/Desktop/web视频/{}'.format(dic_name)
        #如果文件夹不存在则创建文件夹并写入文件
        if not os.path.exists(dir):
            os.makedirs(dir)
            print('{}文件夹创建成功'.format(dic_name))

       # print(url)
            with open('{}/{}.mp4'.format(dir, dic_name), 'ab') as f:
                for url in ts_list:
                    res=requests.get(url=url,headers=self.headers).content
                    # dic=url.split('/')[-2]
                    file_name01=url.split('-')[-1]
                    file_name02=file_name01.split('.')[0]
                    cryptor = AES.new(keys, AES.MODE_CBC, keys)
                    f.write(cryptor.decrypt(res))

                    print('{}写入成功'.format(file_name02))
        else:
            pass
                    #
                    # if len(file_name02)==1:
                    #     file_name='00{}'.format(file_name02)
                    # elif len(file_name02)==2:
                    #     file_name = '0{}'.format(file_name02)
                    # else:
                    #     file_name=file_name02






    def main(self):
        self.parse_one()

if __name__=='__main__':
    spider=DaiNeiVideoSpider()
    spider.main()