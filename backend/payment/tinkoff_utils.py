import logging

import requests
from hashlib import sha256

from core_base.logger import get_logger

logger = get_logger('pay_tink_utils_logs', level=logging.INFO)


def hash_to_sha256(text):
    return sha256(text.encode('utf-8')).hexdigest()


def generate_token(req_as_dict, password):
    """Генерировать токен для запроса"""

    req_as_list = []
    for key, val in (req_as_dict | {'Password': password}).items():
        req_as_list.append(
            {key: val}
        )
    req_as_list.sort(key=lambda x: list(x.keys())[0])
    values_concat = ''
    for item in req_as_list:
        values_concat += str(list(item.values())[0])
    hash_of_values_concat = hash_to_sha256(values_concat)
    # print('hash_of_values_concat: ', hash_of_values_concat)
    return hash_of_values_concat


def create_new_tinkoff_card_payment(terminal_key, password, amount, order_id, description, success_url=''):
    """
    Создать новый платеж

    :param terminal_key: Ключ терминала
    :param password: Пароль
    :param amount: Сумма в копейках
    :param order_id: Заказ ИД
    :param description: Описание заказа
    :param success_url: Страныца для перехода при платеже
    :return:
    """

    amount = amount * 100  # С копейкками
    req_as_dict = {
        'TerminalKey': terminal_key,
        'Amount': amount,
        'OrderId': order_id,
        'Description': description,
        'SuccessURL': success_url
    }
    print('req_as_dict', req_as_dict)
    logger.info(f'req_as_dict {req_as_dict}')
    token = generate_token(req_as_dict, password=password)
    res = requests.post(
        url='https://securepay.tinkoff.ru/v2/Init',
        json=req_as_dict | {'Token': token}
    )

    return res.json()


def get_tinkoff_card_payment(terminal_key, password, payment_id):
    req_as_dict = {
        'TerminalKey': terminal_key,
        'PaymentId': payment_id
    }
    token = generate_token(req_as_dict, password=password)

    res = requests.post(
        url='https://securepay.tinkoff.ru/v2/GetState',
        json=req_as_dict | {'Token': token}
    )

    return res.json()
