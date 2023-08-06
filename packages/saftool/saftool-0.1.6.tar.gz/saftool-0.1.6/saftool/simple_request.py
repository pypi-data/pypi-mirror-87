# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     simple_request
   Description :
   Author :        艾登科技 Asdil
   date：          2020/10/29
-------------------------------------------------
   Change Activity:
                   2020/10/29:
-------------------------------------------------
"""
__author__ = 'Asdil'
import json
import requests


def post(url, data, header=None):
    """post方法用于发送post
    Parameters
    ----------
    url : str
        url地址
    data : dict
        post body数据
    header : dict
        post header 数据
    Returns
    ----------
    """
    header = header if header else {'Content-Type': 'application/x-www-form-urlencoded'}
    ret = requests.post(url=url,
                        data=json.dumps(data),
                        headers=header)
    ret = ret.json()
    return ret
