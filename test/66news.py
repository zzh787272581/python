import requests
import time
from bs4 import BeautifulSoup
import os


class MeiTu():
    def __init__(self):
        self.host = 'http://www.66news.org/'
        self.dir = "D:\mzitu\m66news"
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self, url):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        if html is None:
            return False
        all_a = BeautifulSoup(html.text, 'lxml').find_all('div', class_='c cl')
        for a in all_a:
            a_obj = a.find('a')
            title = a_obj['title']
            print(u'开始保存：', title)  ##加点提示不然太枯燥了
            path = str(title).replace("?", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(path)  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            page_url = a_obj['href']
            self.img(path, page_url)  ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！

    # def html(self, path, href):  ##这个函数是处理套图地址获得图片的页面地址
    #     html = self.request(href)
    #     if html is None:
    #         return False
    #     self.headers['referer'] = href
    #     max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
    #     for page in range(1, int(max_span) + 1):
    #         page_url = href + '/' + str(page)
    #         self.img(path, page_url)  ##调用img函数

    def img(self, path, page_url):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        if img_html is None:
            return False
        img_list = BeautifulSoup(img_html.text, 'lxml').find_all('ignore_js_op')
        for img in img_list:
            img_url = self.host + img.find('img')['zoomfile']
            self.save(path, img_url)

    def save(self, path, img_url):  ##这个函数保存图片
        name = img_url[-9:-4]
        if os.path.isfile(self.dir + '/' + path + '/' + name + '.jpg'):
            print(u'文件已经存在', name + '.jpg')
            return True
        img = self.request(img_url)
        if img is None:
            return False
        f = open(self.dir + '/' + path + '/' + name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
        print(u'文件已经保存成功', self.dir + '/' + path + '/' + name + '.jpg')

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.dir, path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(self.dir, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url):  ##这个函数获取网页的response 然后返回
        try:
            r = requests.get(url, headers=self.headers, timeout=3)
            return r
        except (requests.ConnectionError, IndexError, UnicodeEncodeError, TimeoutError, requests.ReadTimeout) as e:
            print(e.args)
            return None
        except requests.HTTPError as f:
            print('The server couldn\'t fulfill the request.')
            return None


start = time.time()
meitu = MeiTu()  ##实例化
meitu.all_url('http://www.66news.org/forum-48-1.html')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
print(u'执行时间:', time.time() - start)
