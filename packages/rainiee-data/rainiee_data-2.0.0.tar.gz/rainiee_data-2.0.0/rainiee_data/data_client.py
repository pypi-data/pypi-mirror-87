import json
import rainiee_data.pro.data_pro as data_pro


class DataClient(object):

    def __init__(self, username, password):
        data_pro.init_token(username, password)

    def data_pro(self):
        return data_pro

    def get_token(self):
        return data_pro.get_token()

    @staticmethod
    def cn_stock_realtime(symbol):
        return data_pro.pro_bar(api_name='cn_stock_realtime', method_type='GET', req_param={'symbol': symbol})

    @staticmethod
    def cn_stock_eod(symbol, start_index, end_index, adj=None, frequency='d'):
        return data_pro.pro_bar(api_name='cn_stock_eod', method_type='GET',
                                req_param={'symbol': symbol, 'start_index': start_index, 'end_index': end_index,
                                           'adj': adj, 'frequency': frequency})

    @staticmethod
    def cn_index_eod(index_code, start_index, end_index):
        return data_pro.get_rainiee_client().cn_index_eod(method_type='GET', req_param={
            'index_code': index_code,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def cn_index_composition(index_code):
        return data_pro.get_rainiee_client().cn_index_composition(method_type='GET', req_param={
            'index_code': index_code
        })

    @staticmethod
    def cn_index_composition_weight(index_code):
        return data_pro.get_rainiee_client().cn_index_composition_weight(method_type='GET', req_param={
            'index_code': index_code
        })

    @staticmethod
    def cn_index_basic(market):
        return data_pro.get_rainiee_client().cn_index_basic(method_type='GET', req_param={
            'market': market
        })

    @staticmethod
    def cn_symbol_list(category):
        return data_pro.get_rainiee_client().cn_symbol_list(method_type='GET', req_param={
            'category': category
        })

    @staticmethod
    def na_etf_eod(symbol, start_date, end_date):
        return data_pro.get_rainiee_client().na_etf_eod(method_type='GET', req_param={
            'symbol': symbol,
            'start_date': start_date if isinstance(start_date, str) else start_date.strftime('%Y%m%d'),
            'end_date': end_date if isinstance(end_date, str) else end_date.strftime('%Y%m%d')
        })

    @staticmethod
    def na_etf_symbol(category):
        return data_pro.get_rainiee_client().na_etf_symbol(method_type='GET', req_param={
            'category': category
        })

    @staticmethod
    def cn_stockstats_latest_returns(symbol, gap=1):
        return data_pro.get_rainiee_client().cn_stockstats_latest_returns(method_type='GET', req_param={
            'symbol': symbol,
            'gap': gap
        })

    @staticmethod
    def cn_stockstats_returns(symbol, start_index, end_index):
        return data_pro.get_rainiee_client().cn_stockstats_returns(method_type='GET', req_param={
            'symbol': symbol,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def cn_stockstats_list(symbol, start_index, end_index):
        return data_pro.get_rainiee_client().cn_stockstats_list(method_type='GET', req_param={
            'symbol': symbol,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def cn_stockstats_sort(column, start_index, end_index):
        return data_pro.get_rainiee_client().cn_stockstats_sort(method_type='GET', req_param={
            'column': column,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def cn_stockstats_eod_portf_return(portf, hold_index):
        return data_pro.get_rainiee_client().cn_stockstats_eod_portf_return(method_type='POST', req_param={
            'portf': json.dumps(portf),
            'hold_index': hold_index
        })

    @staticmethod
    def cn_stockstats_is_enter_market(index, return_metric, calc_period):
        return data_pro.get_rainiee_client().cn_stockstats_is_enter_market(method_type='GET', req_param={
            'index': index,
            'return_metric': return_metric,
            'calc_period': calc_period
        })

    @staticmethod
    def cn_stockstats_top_turnover_rate(index, topk=100):
        return data_pro.get_rainiee_client().cn_stockstats_top_turnover_rate(method_type='GET', req_param={
            'index': index,
            'topk': topk
        })

    @staticmethod
    def na_etf_stockstats_list(symbol):
        return data_pro.get_rainiee_client().na_etf_stockstats_list(method_type='GET', req_param={
            'symbol': symbol
        })

    @staticmethod
    def na_etf_stockstats_sort(column, start_date, end_date):
        return data_pro.get_rainiee_client().na_etf_stockstats_sort(method_type='GET', req_param={
            'column': column,
            'start_date': start_date if isinstance(start_date, str) else start_date.strftime('%Y%m%d'),
            'end_date': end_date if isinstance(end_date, str) else end_date.strftime('%Y%m%d')
        })

    @staticmethod
    def get_trade_index(date):
        return data_pro.get_rainiee_client().trade_get_index(method_type='GET', req_param={
            'date': date if isinstance(date, str) else date.strftime('%Y%m%d')})

    @staticmethod
    def get_trade_date(index):
        return data_pro.get_rainiee_client().trade_get_date(method_type='GET', req_param={
            'index': index
        })
