import json

import requests


class ApiException(Exception):
    pass


class ValException(ApiException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ApiResponse:
    """
     имя валюты, цену на которую надо узнать, -— base,
     имя валюты, цену в которой надо узнать, — quote,
     количество переводимой валюты — amount,
     возвращает нужную сумму в валюте.
    """
    @staticmethod
    def get_price(base, quote, amount):

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')
        d = json.loads(r.content)
        answer = float(d[quote])
        sum_to_telegram = ('{:.2f}'.format(amount * answer))
        return sum_to_telegram




