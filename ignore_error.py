from lxml import etree
from Crypto.Cipher import AES
from queue import Queue
from threading import Thread
import re, os, struct, requests


class DaiNeiVideoSpider:
    def __init__(self):
        self.url = 'http://tts.tmooc.cn/studentCenter/toMyttsPage'
        self.headers = {
            'Cookie': "ssss747859=1; ssss749546=0; ssss763527=0; isCenterCookie=no; cloudAuthorityCookie=0; tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; _qddaz=QD.996x4e.kolqbk.k6xr76vs; _qdda=3-1.1us199; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1584280122,1584798995,1584856545,1584860246; TMOOC-SESSION=e527d1039cb74f60bb54b9fcc8cec693; _qddab=3-pj1ohy.k82ovspt; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1584865080; sessionid=e527d1039cb74f60bb54b9fcc8cec693|E_bfuqhnh; versionListCookie=TSDTN201905; defaultVersionCookie=TSDTN201905; versionAndNamesListCookie=TSDTN201905N22N%25E8%25BD%25AF%25E4%25BB%25B6%25E6%25B5%258B%25E8%25AF%2595%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV05N22N749546; courseCookie=TESTING; stuClaIdCookie=749546; JSESSIONID=E3F91FE98C0DE9B7DC47A6648B480ACD; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1584856579,1584860263,1584864826,1584865136; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1584865136",
            'Referer': 'http://uc.tmooc.cn/userCenter/toUserCoursePage',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        # self.queue01=Queue()
        # self.queue_ts=Queue()

    def parse_one(self):
        video_list = []
        html = requests.get(url=self.url, headers=self.headers).content.decode('utf-8')
        parse_html = etree.HTML(html)
        # print(html)
        # ['http://tts.tmooc.cn/video/showVideo?menuId=678266&version=TSDTN201905',
        # 'http://tts.tmooc.cn/video/showVideo?menuId=678265&version=TSDTN201905',
        link_list = parse_html.xpath('//li[@class="sp"]/a/@href')
        # print(link_list)
        # print(len(link_list))
        for video in link_list:
            video_list.append(video)
            # print(video_list)
        self.parse_two(video_list)

    # http: // videotts.it211.com.cn / tsd19040430am / tsd19040430am.m3u8
    def parse_two(self, video_list):
        for url in video_list:
            # print(link_list)
            # print(len(link_list))
            html = requests.get(url=url, headers=self.headers).content.decode('utf-8')
            parse_html = etree.HTML(html)
            # active_WEB_WEB1805_N_NODE_DAY01_01.m3u8
            link_list01 = parse_html.xpath('//div[@class="video-list"]//p/@id')
            if len(link_list01) == 0:
                pass
            # print(link_list01)
            for item in link_list01:
                # print(item)
                a = item.split('_')
                if len(a) > 2:
                    last_url01 = a[1:]
                    last_url = '_'.join(last_url01)
                    middle_url = last_url.split('.')[0]
                    # print(middle_url)
                    m3u8_url = 'http://c.it211.com.cn/' + middle_url + '/' + last_url
                    # self.queue01.put(m3u8_url)
                    # 拿到半天的链接后直接进行.ts文件解析
                    self.parse_m3u8(m3u8_url)

                else:
                    last_url = item.split('_')[1]
                    middle_url = last_url.split('.')[0]
                    # print(middle_url)
                    m3u8_url = 'http://c.it211.com.cn/' + middle_url + '/' + last_url
                    # self.queue01.put(m3u8_url)
                    # 拿到半天的链接后直接进行.ts文件解析
                    self.parse_m3u8(m3u8_url)

    def parse_m3u8(self, m3u8_url):
        ts_list = []
        file = m3u8_url.split('/')[-1]
        dic_name = file.split('.')[0]
        html = requests.get(url=m3u8_url, headers=self.headers)
        # print(html)
        if html.status_code == 404:
            # print('url或视频出现错误,跳过')
            with open(r'G:\Programs\Codes\try\PythonProgram\TTSspider_old\error.txt', 'a') as f:
                f.write('{}文件写入错误，已跳过'.format(m3u8_url))
            pass
        else:
            html = requests.get(url=m3u8_url, headers=self.headers).text
            # print(html)
            parse_key = re.compile('URI="(.*?)"', re.S)
            key = parse_key.findall(html)[0]
            list01 = html.split('\n')
            for item in list01:
                if '.ts' in item:
                    # 拿到每半天所有ts链接
                    ts_list.append(item)
            self.write(key, dic_name, ts_list)

    def write(self, key, dic_name, ts_list):
        # 获得密匙
        keys = requests.get(url=key, headers=self.headers).content
        # 创建文件夹用来存放每半天的视频
        dir = r'J:\TSD\{}'.format(dic_name)
        # 如果文件夹不存在则创建文件夹并写入文件
        if not os.path.exists(dir):
            os.makedirs(dir)
            print('{}文件夹创建成功'.format(dic_name))

            # print(url)
            with open('{}/{}.mp4'.format(dir, dic_name), 'ab') as f:
                for url in ts_list:
                    res = requests.get(url=url, headers=self.headers).content
                    # dic=url.split('/')[-2]
                    file_name01 = url.split('-')[-1]
                    file_name02 = file_name01.split('.')[0]
                    cryptor = AES.new(keys, AES.MODE_CBC, keys)
                    f.write(cryptor.decrypt(res))

                    print('{}写入成功'.format(file_name02))
        else:
            pass

    def main(self):
        self.parse_one()


if __name__ == '__main__':
    spider = DaiNeiVideoSpider()
    spider.main()
