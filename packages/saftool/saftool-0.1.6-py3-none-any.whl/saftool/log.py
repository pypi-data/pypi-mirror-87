# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log
   Description :
   Author :        艾登科技 Asdil
   date：          2020/10/9
-------------------------------------------------
   Change Activity:
                   2020/10/9:
-------------------------------------------------
"""
__author__ = 'Asdil'
import logging


def simple_init(level='INFO', log_path=None):
    """add方法用于新建一个log

    Parameters
    ----------
    level: str
        日志级别
    log_path: str
        保存路径
    Returns
    ----------
    """
    logger = logging.getLogger()
    level_dict = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
    logger.setLevel(level_dict[level])

    if log_path is not None:
        # create a file handler
        handler = logging.FileHandler(log_path)
        handler.setLevel(level)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:%(lineno)s - %(message)s')
        handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    return logger
