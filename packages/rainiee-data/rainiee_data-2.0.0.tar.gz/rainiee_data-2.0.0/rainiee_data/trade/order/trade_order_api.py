#!/usr/bin/python
# -*- coding: UTF-8 -*-
from rainiee_data.pro import data_pro


def trade_execute_order(symbol, index, order_type, price):
    return data_pro.get_rainiee_client().trade_execute_order(method_type='GET', req_param={
        'symbol': symbol,
        'index': index,
        'order_type': order_type,
        'price': price
    })
