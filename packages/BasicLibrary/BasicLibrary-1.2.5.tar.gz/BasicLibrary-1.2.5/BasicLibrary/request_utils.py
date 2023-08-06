'''
Documentation：http的get、post请求封装
引用包名是：BasicLibrary   引用本python文件，请使用 from BasicLibrary.request_utils import *
'''

import requests
import json
from BasicLibrary.logger_utils import logger

def http_get(url, params=None, headers=None, timeout=None):
    '''
    http get请求
    【url】：请求url
    【headers】:请求头
    【params】:请求参数
    【timeout】:超时时间
    【return】:响应正文
    Examples:
        |     方法   | 参数   |   参数   |   参数   |    参数  |
        |  http_get  |  url  | headers |  params  | timeout |

    '''
    if url is None:
        logger.error('url参数是None!')
        raise AssertionError('url参数是None!')
    try:
        response = requests.get(url,headers=headers,params=params,timeout=timeout)
        Res = response.text
        try:
            resAndJosnDict = json.loads(Res)
        except json.decoder.JSONDecodeError as e:
            logger.info('响应不能转成json格式，原因%s'%e)
            resAndJosnDict = response
        return resAndJosnDict
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s'%e)
        raise AssertionError('发送请求失败，原因：%s'%e)

def http_post(url, params=None, headers=None, data=None,timeout=None):
    '''
        http post请求
        【url】：请求url
        【headers】:请求头
        【params】:请求参数
        【timeout】:超时时间
        【return】:响应正文
        Examples:
            |     方法    | 参数   |   参数   |   参数   |    参数  |
            |  http_post  |  url  | headers |  params  | timeout |

        '''
    if url is None:
        logger.error('url参数是None!')
        raise AssertionError('url参数是None!')
    try:
        if headers is None:
            headers = {}
        headers.update({'Content-Type': 'application/json;charset=UTF-8'})
        if isinstance(data,str):
            '''将data转换成json格式,dict类型'''
            data = json.loads(data)
        response = requests.post(url,headers=headers,params=params,json=data,timeout=timeout)
        Res = response.text
        try:
            resAndJosnDict = json.loads(Res)
        except json.decoder.JSONDecodeError as e:
            '''响应可能为空'''
            logger.info('响应不能转成json格式，原因%s'%e)
            resAndJosnDict = response
        return resAndJosnDict
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s'%e)


