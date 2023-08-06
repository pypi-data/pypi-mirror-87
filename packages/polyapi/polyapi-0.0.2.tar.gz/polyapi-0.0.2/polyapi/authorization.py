# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль авторизации в Полиматике """
import requests
import logging
import time
import json
from typing import Tuple, Dict

from . import error_handler


class Authorization:
    def __init__(self, server_codes: Dict):
        """
        Инициализация класса Authorization
        :param server_codes: server_codes.json
        """
        self.server_codes = server_codes

    def login(self, user_name: str, url: str, password: str = None, language: str = None) -> Tuple:
        """
        Авторизация с паролем и без пароля
        :param user_name: имя пользователя
        :param password: пароль
        :param url: базовый URL стенда
        :param language: "en" / "ru" / "de" / "fr"
        :return: (Tuple) session_id, uuid/manager_id, func_timing
        """
        time1 = time.time()

        # для авторизации с паролем
        session = ""

        auth_command = self.server_codes.get("manager", {}).get("command", {}).get("authenticate", {}).get("id")
        auth_check = self.server_codes.get("manager", {}).get("command", {}).get("authenticate", {}).get("state", {}).\
            get("check")
        auth_login = self.server_codes.get("manager", {}).get("command", {}).get("authenticate", {}).get("state", {}).\
            get("login")
        language = self.server_codes.get("locale", {}).get(language)

        # для авторизации без пароля
        if password is None:
            # формирование id сессии
            url = url + "/login"
            payload = {"login": user_name}
            r = requests.get(url=url, params=payload)
            try:
                response = r.json()
            except json.decoder.JSONDecodeError:
                message = "Host {} not supporting non-password authorization. Please, specify the password!".format(
                    url
                )
                raise ValueError({'message': message})
            logging.info("Request: %s", payload)
            logging.info("Headers: %s", r.request.headers)
            logging.info("Response: %s", response)
            if len(r.history) > 0:
                for resp in r.history:
                    session = resp.cookies.get("session")
            else:
                session = response.get("session")

        # формирование params
        params = {
            "state": 0,
            "session": session,
            "queries": [
                # query1, query2, ..., queryN will be appended in this list
            ]
        }

        # формирование command
        command = {
            "plm_type_code": auth_command,
        }
        # для авторизации без пароля добавить в command состояние check
        if password is None:
            command.update({"state": auth_check})
        # для авторизации с паролем добавить в command состояние login и параметры:
        else:
            command.update({"state": auth_login})
            command.update({"login": user_name})
            command.update({"passwd": password})
            command.update({"locale": language})

        query1 = {
            "uuid": "00000000-00000000-00000000-00000000",
            "command": command
        }

        params["queries"].append(query1)

        r = requests.request(method="POST", url=url, json=params, timeout=60.0)

        logging.info("Request: %s", params)
        logging.info("Response: %s", r.json())

        # проверки
        session_id, uuid = error_handler.authorization_checks(params, r)

        time2 = time.time()
        func_timing = '{:s} func exec time: {:.2f} sec'.format("login", (time2 - time1))

        logging.info("login successful")
        return session_id, uuid, func_timing
