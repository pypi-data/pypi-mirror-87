# -*- coding:utf-8 -*-
from rainiee_data.pro import client, login
from rainiee_data.utils import upass


def init_token(username=None, password=None):
    set_token(login.LoginApi(username, password).login())


def get_token():
    return upass.get_token()


def set_token(token):
    upass.set_token(token)


def get_rainiee_client():
    """
    get rainiee data client
    """
    return client.DataApi(upass.get_token())


def pro_bar(api_name=None, method_type='GET', req_param=None, api=None):
    api = api if api is not None else get_rainiee_client()
    return api.query(api_name, method_type, req_param)
