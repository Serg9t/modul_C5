"""Файл содержит класс-обработчик ошибок и взаимодействие с API."""

import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать колличество {amount}!")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)
        new_price = resp[sym_key] * float(amount)
        return new_price
