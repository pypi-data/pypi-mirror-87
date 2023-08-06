#!/usr/bin/python
# -*- coding: UTF-8 -*-
from rainiee_data.pro import data_pro


def cn_index_eod(index_code, start_index, end_index):
    return data_pro.get_rainiee_client().cn_index_eod(method_type='GET', req_param={
        'index_code': index_code,
        'start_index': start_index,
        'end_index': end_index
    })


def cn_index_composition(index_code):
    return data_pro.get_rainiee_client().cn_index_composition(method_type='GET', req_param={
        'index_code': index_code
    })


def cn_index_composition_weight(index_code):
    return data_pro.get_rainiee_client().cn_index_composition_weight(method_type='GET', req_param={
        'index_code': index_code
    })


def cn_index_basic(market):
    return data_pro.get_rainiee_client().cn_index_basic(method_type='GET', req_param={
        'market': market
    })


def cn_symbol_list(category):
    return data_pro.get_rainiee_client().cn_symbol_list(method_type='GET', req_param={
        'category': category
    })
