import requests
from config import keys


class ConvertException(BaseException):
    pass


class CryptoConversion:
    @staticmethod
    def convert(quote: str, base: str, amount: str, ):
        try:
            keys_ticker_base = keys[base]
        except KeyError:
            raise ConvertException(f'валюты {base} нет в нашем боте\n'
                                   'Для того чтобы посмотреть список доступных валют для перевода '
                                   'введите команду /values')
        try:
            keys_ticker_quote = keys[quote]
        except KeyError:
            raise ConvertException(f'валюты {quote} нет в нашем боте\n'
                                   'Для того чтобы посмотреть список доступных валют для перевода '
                                   'введите команду /values')
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym="
                         f"{keys_ticker_quote}&tsyms={keys_ticker_base}").json()
        t = r[keys[base].upper()] * int(amount)
        return t
