#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rainiee_data.pro import data_pro


def cn_stock_eod(symbol, start_index, end_index):
    return data_pro.get_rainiee_client().cn_stock_eod(method_type='GET', req_param={
        'symbol': symbol,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_stock_realtime(symbol):
    return data_pro.get_rainiee_client().cn_stock_realtime(method_type='GET', req_param={
        'symbol': symbol
    })
