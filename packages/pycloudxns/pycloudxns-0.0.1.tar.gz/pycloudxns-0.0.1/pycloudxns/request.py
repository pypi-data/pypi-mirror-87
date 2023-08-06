# -*- coding: utf-8 -*-

from email.utils import formatdate
import calendar
import threading
import requests
import logging
import re
import base64
import time
import hashlib
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError

UUID_PATTERN = re.compile(r'[0-9a-zA-Z\-]{36}')

logger = logging.getLogger(__name__)

_STRPTIME_LOCK = threading.Lock()

_GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def content_md5(data):
    """计算data的MD5值，经过Base64编码并返回str类型。

    返回值可以直接作为HTTP Content-Type头部的值
    """
    if isinstance(data, str):
        data = hashlib.md5(data.encode('utf-8'))
    value = base64.b64encode(data.hexdigest().encode('utf-8'))
    return value.decode('utf-8')


def make_signature(access_key_secret, date=None):
    if isinstance(date, bytes):
        date = bytes.decode(date)
    if isinstance(date, int):
        date_gmt = http_date(date)
    elif date is None:
        date_gmt = http_date(int(time.time()))
    else:
        date_gmt = date

    data = str(access_key_secret) + "\n" + date_gmt
    return content_md5(data)


def to_unixtime(time_string, format_string):
    time_string = time_string.decode("ascii")
    with _STRPTIME_LOCK:
        return int(calendar.timegm(time.strptime(time_string, format_string)))


def http_date(timeval=None):
    """返回符合HTTP标准的GMT时间字符串，用strftime的格式表示就是"%a, %d %b %Y %H:%M:%S GMT"。
    但不能使用strftime，因为strftime的结果是和locale相关的。
    """
    return formatdate(timeval, usegmt=True)



class HTTP:
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'CloudXNS-Python/v3',
        'API-KEY': "",
        'API-REQUEST-DATE': "",
        'API-HMAC': "",
        'API-FORMAT': 'json',
    }
    API_URL = "https://www.cloudxns.net/api2/"

    def __init__(self, API_KEY, SECRET_KEY):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY

    def set_api_key(self, key):
        self.headers['API-KEY'] = key

    def set_date(self, date):
        self.headers['API-REQUEST-DATE'] = date

    def set_hmac(self, hmac):
        self.headers['API-HMAC'] = hmac

    def request(self, method, uri, **kwargs) -> dict:
        REQUEST_DATE = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime())
        sign_raw = (
            self.API_KEY,
            "%s%s" % (self.API_URL, "?%s" % str("&".join([f"{k}={v}" for k, v in kwargs['params'].items()])) if kwargs.get('params') else ""),
            REQUEST_DATE,
            self.SECRET_KEY
        )
        sign = "".join(sign_raw)
        API_HMAC = hashlib.md5(sign.encode()).hexdigest()
        self.set_api_key(self.API_KEY)
        self.set_hmac(API_HMAC)
        self.set_date(REQUEST_DATE)

        url = f"{self.API_URL}/{uri}"
        logging.debug(url)

        try:
            req = requests.api.request(method=method, url=url, timeout=600, headers=self.headers, **kwargs)

            if req.status_code != 200:
                return {'code': req.status_code, 'message': f'Response {req.status_code} {url}'}

            ret = req.json()

            if isinstance(ret, list):
                return {'code': 0, 'data': ret}

            # code = ret.get('code')
            # if not code == 0:
            #     logger.error(ret)
            # Bot.error(ret)
            return ret

        except JSONDecodeError:
            logger.error(f'獲取json出錯')
            return {'code': 1, 'message': f'獲取json出錯'}
        except ConnectionError:
            logger.error(f'連接超時 {url}')
            return {'code': 1, 'message': f'連接超時 {url}'}
        except Exception as e:
            logger.error(f'未知錯誤 {e} {type(e)}')
            return {'code': 1, 'message': f'未知錯誤 {e} {type(e)}'}


    def get(self, url, params=None, **kwargs) -> dict:
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('get', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> dict:
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> dict:
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('put', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('delete', url, **kwargs)
