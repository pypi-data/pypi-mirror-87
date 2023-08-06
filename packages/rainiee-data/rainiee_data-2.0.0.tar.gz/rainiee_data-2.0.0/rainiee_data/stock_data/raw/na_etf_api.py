#!/usr/bin/python
# -*- coding: UTF-8 -*-
from rainiee_data.pro import data_pro


def na_etf_eod(symbol, start_date, end_date):
    return data_pro.get_rainiee_client().na_etf_eod(method_type='GET', req_param={
        'symbol': symbol,
        'start_date': start_date if isinstance(start_date, str) else start_date.strftime('%Y%m%d'),
        'end_date': end_date if isinstance(end_date, str) else end_date.strftime('%Y%m%d')
    })


def na_etf_symbol(category):
    return data_pro.get_rainiee_client().na_etf_symbol(method_type='GET', req_param={
        'category': category
    })
