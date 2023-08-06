#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rainiee_data.pro import data_pro


def na_etf_stockstats_list(symbol):
    return data_pro.get_rainiee_client().na_etf_stockstats_list(method_type='GET', req_param={
        'symbol': symbol
    })


def na_etf_stockstats_sort(column, start_date, end_date):
    return data_pro.get_rainiee_client().na_etf_stockstats_sort(method_type='GET', req_param={
        'column': column,
        'start_date': start_date if isinstance(start_date, str) else start_date.strftime('%Y%m%d'),
        'end_date': end_date if isinstance(end_date, str) else end_date.strftime('%Y%m%d')
    })