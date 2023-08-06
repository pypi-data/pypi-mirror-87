#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

from rainiee_data.pro import data_pro


def cn_stockstats_latest_returns(symbol, gap=1):
    return data_pro.get_rainiee_client().cn_stockstats_latest_returns(method_type='GET', req_param={
        'symbol': symbol,
        'gap': gap
    })


def cn_stockstats_returns(symbol, start_index, end_index):
    return data_pro.get_rainiee_client().cn_stockstats_returns(method_type='GET', req_param={
        'symbol': symbol,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_stockstats_returns_matrix(symbol_list, start_index, end_index):
    return data_pro.get_rainiee_client().cn_stockstats_returns_matrix(method_type='POST', req_param={
        'symbol_list': symbol_list,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_stockstats_list(symbol, start_index, end_index):
    return data_pro.get_rainiee_client().cn_stockstats_list(method_type='GET', req_param={
        'symbol': symbol,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_stockstats_sort(column, start_index, end_index):
    return data_pro.get_rainiee_client().cn_stockstats_sort(method_type='GET', req_param={
        'column': column,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_stockstats_eod_portf_return(portf, hold_index):
    return data_pro.get_rainiee_client().cn_stockstats_eod_portf_return(method_type='POST', req_param={
        'portf': json.dumps(portf),
        'hold_index': hold_index
    })


def cn_stockstats_is_enter_market(index, return_metric, calc_period):
    return data_pro.get_rainiee_client().cn_stockstats_is_enter_market(method_type='GET', req_param={
        'index': index,
        'return_metric': return_metric,
        'calc_period': calc_period
    })


def cn_stockstats_top_turnover_rate(index, topk=100):
    return data_pro.get_rainiee_client().cn_stockstats_top_turnover_rate(method_type='GET', req_param={
        'index': index,
        'topk': topk
    })
