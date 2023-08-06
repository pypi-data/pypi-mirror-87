#!/usr/bin/python
# -*- coding: UTF-8 -*-
from rainiee_data.pro import data_pro


def trade_get_index(date):
    return data_pro.get_rainiee_client().trade_get_index(method_type='GET', req_param={'date': date if isinstance(date, str) else date.strftime('%Y%m%d')})


def trade_get_date(index):
    return data_pro.get_rainiee_client().trade_get_date(method_type='GET', req_param={
        'index': index
    })
