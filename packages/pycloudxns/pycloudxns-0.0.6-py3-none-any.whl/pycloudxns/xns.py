from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import pickle
import os
import logging

logger = logging.getLogger(__name__)



class XNS:

    url = "https://www.cloudxns.net"
    filename = 'xns_cookie'

    def __init__(self,user,passwd):
        self.user = user
        self.passwd = passwd
        self.domainlist = {}



    @property
    def headers(self):
        return {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    def chk_login(self, cookie_jar):
        req = requests.get(f"{self.url}/Domain/index.html", headers=self.headers, cookies=cookie_jar)
        # print(req.text)
        if "账号登录" in req.text:
            logger.error('登入失敗')
            return self._cookie()
        else:
            logger.info('登入成功')
            return cookie_jar

    @property
    def cookie(self):
        logger.debug("get_cookie_jar")

        # xns_language = "zh-cn"
        if not os.path.exists(self.filename):
            return self._cookie()
        else:
            cookie_jar = pickle.load(open(self.filename, 'rb'))['cookie_jar']
            return self.chk_login(cookie_jar)

    @property
    def sid(self):
        url = f"{self.url}/Sign/signin.html"
        s1 = requests.get(
            url=url,
            headers=self.headers,
        )
        soup = BeautifulSoup(s1.text, 'lxml')
        sid = soup.select_one('input[name="sid"]').attrs.get('value')
        if sid:
            return sid
        else:
            raise Exception("沒有sid")

    def _cookie(self):
        url = f"{self.url}/Sign/login.html"
        req = requests.post(
            url=url,
            headers=self.headers,
            data={
                'current_url': '',
                'email': self.user,
                'password': self.passwd,
                'verify': '',
                'rememberme': 1,
                'sid': self.sid
            },
        )
        data = req.json()
        if data.get('status') == 1:
            logger.debug("登入成功")
            r = requests.get(url=data['data'], headers=self.headers, cookies=req.cookies)
            pickle.dump({'cookie_jar': r.cookies}, open(self.filename, 'wb'))
            return r.cookies
        else:
            logger.debug(req.json())
            raise Exception("無法登入")


    def get_domain_list(self):
        req = requests.get(f"{self.url}/Domain/index.html", headers=self.headers, cookies=self.cookie)
        soup = BeautifulSoup(req.text, 'lxml')


        for i in soup.select("#domainlist table td.name a"):
            self.domainlist[i.text] = {"name":i.text,"link":i.get('href')}

        while 1:
            next_page = [i.select_one('a').get('href') for i in soup.select(".pagination li") if '下一页' in i.text]
            if next_page:
                req = requests.get(f"{self.url}{next_page[0]}", headers=self.headers, cookies=self.cookie)
                soup = BeautifulSoup(req.text, 'lxml')
                for i in soup.select("#domainlist table td.name a"):
                    self.domainlist[i.text] = {"name":i.text,"link":i.get('href')}
            else:
                break

    def get_data(self, kwargs):
        url = kwargs.get('url')
        page = kwargs.get('page')
        name = kwargs.get('name')
        req = requests.get(
            url=url,
            headers=self.headers,
            cookies=self.cookie,
            params={"p": page}
        )

        soup = BeautifulSoup(req.text, 'lxml')

        for s in soup.select(".entry-header"):
            # if s.select_one(".entry-type.field").text == "A":
            #     continue
            data = {
                'name': s.select_one(".entry-name.field").text,
                'value': s.select_one(".entry-value.field span").text,
                'status': s.select_one(".entry-status p").text.strip(),
                'type': s.select_one(".entry-type.field span").text.strip(),
                'line': s.select_one(".entry-line.field span").text.strip(),
            }
            self.domainlist[name].update(data)

        # return ret

    def get_domain_datail(self, doamin):
        req = requests.get(
            url=doamin['link'],
            headers=self.headers,
            cookies=self.cookie
        )
        soup = BeautifulSoup(req.text, 'lxml')
        page = list(map(lambda x: int(x.get_text()) if x.get_text().isdigit() else None, soup.select(".pagination li")))
        if not page:
            maxpage = 1
        else:
            maxpage = max(filter(lambda x: x, page))

        url_list = ({'name':doamin['name'],'url': doamin['link'], 'page': page} for page in range(1, maxpage + 1))

        pool = ThreadPoolExecutor()
        pool.map(self.get_data, url_list)
        pool.shutdown()




if __name__ == '__main__':
    x = XNS(name='abc',url='https://www.cloudxns.net/Record/index/z_id/123456.html')
    # x.run()
    # x.export()
