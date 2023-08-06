#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль с бизнес-сценариями """
import os
import re
import time
import ast
import datetime
import requests
import traceback
import pandas as pd
from itertools import count
from typing import List, Dict, Tuple, Any, Union

from . import error_handler
from . import executor
from . import manager_commands
from . import helper
from . import olap_commands
from . import authorization
from . import precondition


# -------------------------------------------------------------------------------
# logging
from autologging import traced, logged
import logging
from autologging import TRACE

today = lambda: datetime.datetime.now().strftime("%Y-%m-%d")  # ISO_8601: YYYY-MM-DD
LOGS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs/{}')
LOG_FILENAME = 'log-%s.log' % today()

logging.basicConfig(
    filename=LOGS_PATH.format(LOG_FILENAME),
    format='%(asctime)s  ::  %(levelname)s  ::  %(filename)s:%(lineno)d  ::  %(name)s.%(funcName)s  ::  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=TRACE)
logging.info(" ---------------------------------------------------------------------------------------------- ")
logging.info(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCRIPT STARTED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")

# -------------------------------------------------------------------------------


OPERANDS = ["=", "+", "-", "*", "/", "<", ">", "!=", "<=", ">="]
ALL_PERMISSIONS = 31
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декабрь"]
WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
PERIOD = {"Ежедневно": 1, "Еженедельно": 2, "Ежемесячно": 3}
WEEK = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3, "пятница": 4, "суббота": 5, "воскресенье": 6}
UPDATES = ["ручное", "по расписанию", "интервальное", "инкрементальное"]


def timing(f):
    """
    Profiling business logic funcs
    :param f: func to decorate
    :return:
    """

    def wrap(self, *args, **kwargs):
        self.func_name = f.__name__
        time1 = time.time()
        ret = f(self, *args, **kwargs)
        time2 = time.time()
        self.func_timing = '{:s} func exec time: {:.2f} sec'.format(f.__name__, (time2 - time1))
        return ret

    return wrap


@traced
@logged
class BusinessLogic:
    """
    Класс BusinessLogic.

    Используемые переменные класса:
    # язык интерфейса. Задается при авторизации. Возможно задать значения: "ru", "en", "de" или "fr"
    self.language = "ru"

    # базовый URL для работы
    self.url = url

    # словарь команд и состояний server-codes.json
    self.server_codes

    # id сессии
    self.session_id

    # uuid, который возвращается после авторизации
    self.authorization_uuid

    # список слоев сессии
    self.layers_list

    # id мультисферы
    self.cube_id

    # используемый id слоя
    self.active_layer_id

    # данные мультисферы в формате словаря {"dimensions": "", "facts": "", "data": ""}
    self.multisphere_data

    # для хранения названия мультисферы
    self.cube_name = ""

    # helper class
    self.h = helper.Helper(self)

    # общее количество строк текущей рабочей области
    self.total_row = 0

    # для измерения вреимени работы функций бизнес-логики
    self.func_timing = 0

    # записать имя функции для избежания конфликтов с декоратором
    self.func_name = ""

    :param login: логин пользователя Полиматика
    :param url: URL стенда Полиматика
    :param password: (необязательный) пароль пользователя Полиматика
    :param session_id: (необязательный) id сессии
    :param authorization_id: (необязательный) id авторизации
    """

    def __init__(self, login: str, url: str, password: str = None, session_id: str = None,
                 authorization_id: str = None, timeout: float = 60.0, jupiter: bool = False):
        logging.info("INIT CLASS BusinessLogic")

        """
        Инициализация класса BusinessLogic

        :param login: логин пользователя Полиматика
        :param url: URL стенда Полиматика
        :param password: (необязательный) пароль пользователя Полиматика
        :param session_id: (необязательный) id сессии
        :param authorization_id: (необязательный) id авторизации
        :param timeout: таймауты. по умолчанию = 60.0
        :param jupiter: (bool) запускается ли скрипт из Jupiter Notebook.
                По умолчанию jupiter = False (stderr stdout пишется в лог)
        """
        self.language = "ru"
        self.url = url
        self.server_codes = precondition.Preconditions(url).get_server_codes()

        # Флаг работы в Jupiter Notebook
        self.jupiter = jupiter
        # значение присвается в случае аварийного завершения работы
        # может быть удобно при работе в Jupiter Notebook
        self.current_exception = None

        self.login = login

        # для измерения вреимени работы функций бизнес-логики
        self.func_timing = 0

        if session_id is None:
            try:
                self.session_id, self.authorization_uuid, self.func_timing = authorization.Authorization(
                    self.server_codes
                ).login(
                    user_name=login,
                    password=password,
                    url=url,
                    language=self.language
                )
            except BaseException as e:
                logging.exception(e)
                logging.exception("APPLICATION STOPPED")
                self.current_exception = str(e)
                if self.jupiter:
                    print("EXCEPTION!!! %s" % e)
                    return
                raise
        else:
            self.session_id, self.authorization_uuid = session_id, authorization_id

        # инициализация модуля Manager
        self.manager_command = manager_commands.ManagerCommands(
            self.session_id, self.authorization_uuid, url, self.server_codes, self.jupiter)
        # класс выполняющий команды
        self.exec_request = executor.Executor(self.session_id, self.authorization_uuid, url, timeout)
        # id модуля мультисферы, значение присываивается после создания куба и получения данных о кубе
        self.multisphere_module_id = ""
        # инициализация модуля Olap. ВАЖНО! Перед использованием получить self.multisphere_module_id
        self.olap_command = olap_commands.OlapCommands(self.session_id, self.multisphere_module_id,
                                                       url, self.server_codes, self.jupiter)
        self.layers_list = []
        self.cube_id = ""
        self.active_layer_id = ""
        self.multisphere_data = {}
        # для хранения названия мультисферы
        self.cube_name = ""

        # helper class
        self.h = helper.Helper(self)

        # общее количество строк текущей рабочей области
        self.total_row = 0

        # записать имя функции для избежания конфликтов с декоратором
        self.func_name = ""

        # DataFrame content, DataFrame columns
        self.df, self.df_cols = "", ""

    def update_total_row(self):
        result = self.execute_olap_command(
            command_name="view",
            state="get_2",
            from_row=0,
            from_col=0,
            num_row=1,
            num_col=1
        )
        self.total_row = self.h.parse_result(result, "total_row")
        return self.total_row

    @timing
    def get_cube(self, cube_name: str, num_row: int = 100, num_col: int = 100) -> str:
        """
        Получить id куба по его имени и открыть мультисферу
        :param cube_name: (str) имя куба (мультисферы)
        :param num_row: (int) количество строк, которые будут выведены
        :param num_col: (int) количество колонок, которые будут выведены
        :return: id куба
        """
        self.cube_name = cube_name
        # получение списка описаний мультисфер
        result = self.execute_manager_command(command_name="user_cube", state="list_request")
        if self.jupiter:
            if "ERROR" in str(result):
                return result
        # try:
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if self.jupiter:
            if "ERROR" in str(cubes_list):
                return cubes_list

        # получить cube_id из списка мультисфер
        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError as e:
            logging.exception("EXCEPTION!!! %s", e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.multisphere_data = self.create_multisphere_module(num_row=num_row, num_col=num_col)
        self.update_total_row()

        return self.cube_id

    def get_multisphere_data(self, num_row: int = 100, num_col: int = 100) -> [Dict, str]:
        """
        Получить данные мультисферы
        :param self: экземпляр класса BusinessLogic
        :param num_row: количество отображаемых строк
        :param num_col: количество отображаемых столбцов
        :return: (Dict) multisphere data, format: {"dimensions": "", "facts": "", "data": ""}
        """
        # Получить список слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        # список слоев
        layers_list = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(layers_list):
                return layers_list
        try:
            # получить layer id
            self.layer_id = layers_list[0]["uuid"]
        except KeyError as e:
            logging.exception("EXCEPTION!!! %s\n%s", e, traceback.format_exc())
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise
        except IndexError as e:
            logging.exception("EXCEPTION!!! %s\n%s", e, traceback.format_exc())
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # инициализация модуля Olap
        self.olap_command = olap_commands.OlapCommands(self.session_id, self.multisphere_module_id, self.url,
                                                       self.server_codes, self.jupiter)

        # рабочая область прямоугольника
        view_params = {
            "from_row": 0,
            "from_col": 0,
            "num_row": num_row,
            "num_col": num_col
        }

        # получить список размерностей и фактов, а также текущее состояние таблицы со значениями
        # (рабочая область модуля мультисферы)
        query = self.olap_command.multisphere_data(self.multisphere_module_id, view_params)
        if self.jupiter:
            if "EXCEPTION" in str(query):
                return query
        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # multisphere data
        self.multisphere_data = {"dimensions": "", "facts": "", "data": ""}
        for item, index in [("dimensions", 0), ("facts", 1), ("data", 2)]:
            self.multisphere_data[item] = result["queries"][index]["command"][item]
        logging.info("Multisphere data successfully received: %s" % self.multisphere_data)
        return self.multisphere_data

    def get_cube_without_creating_module(self, cube_name: str) -> str:
        """
        Получить id куба по его имени, без создания модуля мультисферы
        :param cube_name: (str) имя куба (мультисферы)
        :return: id куба
        """
        self.cube_name = cube_name
        result = self.execute_manager_command(command_name="user_cube", state="list_request")

        # получение списка описаний мультисфер
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if self.jupiter:
            if "ERROR" in str(cubes_list):
                return cubes_list

        # получить cube_id из списка мультисфер
        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError:
            return "Cube '%s' not found" % cube_name
            # logging.exception("APPLICATION STOPPED")
            # self.current_exception = "Cube '%s' not found" % cube_name
            # if self.jupiter:
            #     return self.current_exception
            # raise
        return self.cube_id

    @timing
    def move_dimension(self, dim_name: str, position: str, level: int) -> [Dict, str]:
        """
        Вынести размерность
        :param dim_name: (str) Название размерности
        :param position: (str) "left" / "up" (выносит размерность влево, либо вверх)
        :param level: (int) 0, 1, 2, ... (считается слева-направо для левой позиции,
                      сверху - вниз для верхней размерности)
        :return: (Dict) результат команды Olap "dimension", состояние "move"
        """
        # проверки
        try:
            position = error_handler.checks(self, self.func_name, position)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получение id размерности
        self.multisphere_data = self.get_multisphere_data()
        dim_id = self.h.get_dim_id(self.multisphere_data, dim_name, self.cube_name)
        if self.jupiter:
            if "ERROR" in str(dim_id):
                return dim_id

        self.update_total_row()

        return self.execute_olap_command(command_name="dimension",
                                         state="move",
                                         position=position,
                                         id=dim_id,
                                         level=level)

    @timing
    def get_measure_id(self, measure_name: str) -> [str, bool]:
        """
        Получить id факта
        :param measure_name: (str) название факта
        :return: (str) id факта
        """
        # получить словарь с размаерностями, фактами и данными
        self.get_multisphere_data()

        # id факта
        m_id = self.h.get_measure_id(self.multisphere_data, measure_name, self.cube_name)
        if self.jupiter:
            if "ERROR" in str(m_id):
                return m_id
        return m_id

    @timing
    def get_dim_id(self, dim_name: str) -> [str, bool]:
        """
        Получить id размерности
        :param dim_name: (str) название размерности
        :return: (str) id факта
        """
        # получить словарь с размаерностями, фактами и данными
        self.get_multisphere_data()

        # id размерности
        dim_id = self.h.get_dim_id(self.multisphere_data, dim_name, self.cube_name)
        if self.jupiter:
            if "ERROR" in str(dim_id):
                return dim_id
        return dim_id

    @timing
    def get_measure_name(self, measure_id: str) -> str:
        """
        Получить название факта
        :param measure_id: (str) id факта
        :return: (str) название факта
        """
        # проверки
        try:
            error_handler.checks(self, func_name=self.func_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        measure_data = self.multisphere_data["facts"]
        logging.info("Full multisphere measure data: %s", measure_data)
        for i in measure_data:
            if i["id"] == measure_id:
                logging.info("Fact id: %s; its name: %s", measure_id, i["name"])
                return i["name"]
        logging.info("No measure %s in the multisphere!", measure_id)
        return "No measure id %s in the multisphere!" % measure_id

    @timing
    def get_dim_name(self, dim_id: str) -> str:
        """
        Получить ID размерности
        :param dim_id: (str) id размерности
        :return: (str) название размерности
        """
        # проверки
        try:
            error_handler.checks(self, func_name=self.func_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        dim_data = self.multisphere_data["dimensions"]
        logging.info("Full multisphere dimension data: %s ", dim_id)
        for i in dim_data:
            if i["id"] == dim_id:
                logging.info("Retrieved dimension id: %s; its name: %s", dim_id, i["name"])
                return i["name"]
        logging.info("No dimension id %s in the multisphere!", dim_id)
        return "No dimension id %s in the multisphere!" % dim_id

    @timing
    def delete_dim_filter(self, dim_name: str, filter_name: str, num_row: int = 100) -> [Dict, str]:
        """
        Убрать выбранный фильтр размерности
        :param dim_name: (str) Название размерности
        :param filter_name: (str) Название метки/фильтра
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере
        :return: (Dict) команда Olap "filter", state: "apply_data"
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # id размерности
        dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", dim_name)
        if self.jupiter:
            if "ERROR" in str(dim_id):
                return dim_id

        # Наложить фильтр на размерность (в неактивной области)
        # получение списка активных и неактивных фильтров
        result = self.execute_olap_command(command_name="filter",
                                           state="pattern_change",
                                           dimension=dim_id,
                                           pattern="",
                                           # кол-во значений отображается на экране, после скролла их становится больше:
                                           # num=30
                                           num=num_row)

        filters_list = self.h.parse_result(result=result, key="data")
        if self.jupiter:
            if "ERROR" in str(filters_list):
                return filters_list
        filters_values = self.h.parse_result(result=result, key="marks")
        if self.jupiter:
            if "ERROR" in str(filters_list):
                return filters_list

        # Снять метку по его интерфейсному названию
        for elem in filters_list:
            if elem == filter_name:
                ind = filters_list.index(filter_name)
                filters_values[ind] = 0
                break

        # 2. нажать применить
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def clear_all_dim_filters(self, dim_name: str, num_row: int = 100) -> [Dict, bool]:
        """
        Очистить все фильтры размерности
        :param dim_name: (str) Название размерности
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере
        :return: (Dict) команда Olap "filter", state: "apply_data"
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data(num_row=num_row)

        # получение id размерности
        dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", dim_name)
        if self.jupiter:
            if "ERROR" in str(dim_id):
                return dim_id

        # Наложить фильтр на размерность (в неактивной области)
        # получение списка активных и неактивных фильтров
        result = self.execute_olap_command(command_name="filter",
                                           state="pattern_change",
                                           dimension=dim_id,
                                           pattern="",
                                           # кол-во значений отображается на экране, после скролла их становится больше:
                                           # num=30
                                           num=num_row)

        filters_values = self.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        if self.jupiter:
            if "ERROR" in str(filters_values):
                return filters_values

        # подготовить список для снятия меток: [0,0,..,0]
        length = len(filters_values)
        for i in range(length):
            filters_values[i] = 0

        # 1. сначала снять все отметки
        self.execute_olap_command(command_name="filter", state="filter_all_flag", dimension=dim_id)

        # 2. нажать применить
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def put_dim_filter(self, dim_name: str, filter_name: Union[str, List] = None, start_date: Union[int, str] = None,
                       end_date: Union[int, str] = None) -> [Dict, str]:
        """
        Сделать выбранный фильтр активным

        Если в фильтрах используются месяцы, то использовать хначения (регистр важен!):
            ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
            "Ноябрь", "Декабрь"]

         Дни недели (регистр важен!): ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота",
            "Воскресенье"]
        :param dim_name: (str) Название размерности
        :param filter_name: (str) Название фильтра. None - если нужно указать интервал дат.
        :param start_date: (int, datetime.datetime) Начальная дата
        :param end_date: (int, datetime.datetime) Конечная дата
        :return: (Dict) команда Olap "filter", state: "apply_data"
        """
        # много проверок...
        # Заполнение списка dates_list в зависимости от содержания параметров filter_name, start_date, end_date
        try:
            dates_list = error_handler.checks(self,
                                              self.func_name,
                                              filter_name,
                                              start_date,
                                              end_date,
                                              MONTHS,
                                              WEEK_DAYS)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получение id размерности
        dim_id = self.get_dim_id(dim_name)

        # Наложить фильтр на размерность (в неактивной области)
        # получение списка активных и неактивных фильтров
        result = self.h.get_filter_rows(dim_id)

        filters_list = self.h.parse_result(result=result, key="data")  # получить названия фильтров
        if self.jupiter:
            if "ERROR" in str(filters_list):
                return filters_list
        filters_values = self.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        if self.jupiter:
            if "ERROR" in str(filters_values):
                return filters_values

        try:
            if (filter_name is not None) and (filter_name not in filters_list):
                if isinstance(filter_name, List):
                    for elem in filter_name:
                        if elem not in filters_list:
                            raise ValueError("No filter '%s' in dimension '%s'" % (elem, dim_name))
                else:
                    raise ValueError("No filter '%s' in dimension '%s'" % (filter_name, dim_name))
        except ValueError as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # подготовить список для снятия меток: [0,0,..,0]
        length = len(filters_values)
        for i in range(length):
            filters_values[i] = 0

        # сначала снять все отметки
        self.execute_olap_command(command_name="filter",
                                  state="filter_all_flag",
                                  dimension=dim_id)

        # ******************************************************************************************************

        # подготовить список фильтров с выбранными отмеченной меткой
        for idx, elem in enumerate(filters_list):
            if isinstance(filter_name, List):
                if elem in filter_name:
                    filters_values[idx] = 1
            # если фильтр по интервалу дат:
            elif filter_name is None:
                if elem in dates_list:
                    filters_values[idx] = 1
            # если фильтр выставлен по одному значению:
            elif elem == filter_name:
                ind = filters_list.index(filter_name)
                filters_values[ind] = 1
                break

        # 2. нажать применить
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def create_consistent_dim(self, formula: str, separator: str, dimension_list: List) -> [Dict, str]:
        """
        Создать составную размерность
        :param formula: (str) формат [Размерность1]*[Размерность2]
        :param separator: (str) "*" / "_" / "-", ","
        :param dimension_list: (List) ["Размерность1", "Размерность2"]
        :return: (Dict) команда модуля Olap "dimension", состояние: "create_union",
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # подготовка списка с id размерностей
        dim_ids = []
        for i in dimension_list:
            dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", i)
            if self.jupiter:
                if "ERROR" in str(dim_id):
                    return dim_id
            dim_ids.append(dim_id)

        # заполнение списка параметров единицами (1)
        visibillity_list = [1] * len(dim_ids)

        return self.execute_olap_command(command_name="dimension",
                                         state="create_union",
                                         name=formula,
                                         separator=separator,
                                         dim_ids=dim_ids,
                                         union_dims_visibility=visibillity_list)

    @timing
    def switch_unactive_dims_filter(self) -> [Dict, str]:
        """
        Переключить фильтр по неактивным размерностям
        :return: (Dict) команда модуля Olap "dimension", состояние "set_filter_mode"
        """
        result = self.execute_olap_command(command_name="dimension", state="set_filter_mode")
        self.update_total_row()
        return result

    @timing
    def copy_measure(self, measure_name: str) -> str:
        """
        Копировать факт
        :param measure_name: (str) имя факта
        :return: id копии факта
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # Получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter:
            if "ERROR" in str(measure_id):
                return measure_id

        result = self.execute_olap_command(command_name="fact", state="create_copy", fact=measure_id)

        new_measure_id = self.h.parse_result(result=result, key="create_id")

        return new_measure_id

    @timing
    def rename_measure(self, measure_name: str, new_measure_name: str) -> [Dict, str]:
        """
        Переименовать факт
        :param measure_name: (str) имя факта
        :param new_measure_name: (str) имя факта
        :return: (Dict) ответ после выполнения команды модуля Olap "fact", состояние: "rename"
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter:
            if "ERROR" in str(measure_id):
                return measure_id

        return self.execute_olap_command(command_name="fact", state="rename", fact=measure_id, name=new_measure_name)

    @timing
    def rename_dimension(self, dim_name: str, new_name: str) -> [Dict, str]:
        """
        Переименовать размерность
        :param dim_name: (str) наименование размерности
        :param new_name: (str) наименование копии размерности
        :return: (Dict) ответ после выполнения command_name="dimension", state="rename"
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, new_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить id размерности
        dim_id = self.get_dim_id(dim_name)

        # скопировать размерность
        result = self.execute_olap_command(command_name="dimension", state="create_copy", id=dim_id)
        copied_id = self.h.parse_result(result, "ndim_id")
        if self.jupiter:
            if "ERROR" in str(copied_id):
                return copied_id

        # переименовать скопированную размерность
        return self.execute_olap_command(command_name="dimension", state="rename", id=copied_id, name=new_name)

    @timing
    def change_measure_type(self, measure_id: str, type_name: str) -> [Dict, str]:
        """
        Поменять Вид факта
        :param measure_id: (str) id факта
        :param type_name: (str) название Вида факта (как в интерфейсе):
            "Значение"
            "Процент"
            "Ранг"
            "Количество уникальных"
            "Среднее"
            "Отклонение"
            "Минимум"
            "Максимум"
            "Изменение"
            "Изменение в %"
            "Нарастающее"
            "ABC"
            "Медиана"
            "Количество"
            "UNKNOWN"
        :return: (Dict) команда модуля Olap "fact", состояние: "set_type"
        """
        # Получить Вид факта (id)
        measure_type = self.h.get_measure_type(type_name)
        if self.jupiter:
            if "ERROR" in str(measure_type):
                return measure_type

        # выбрать Вид факта:
        return self.execute_olap_command(command_name="fact", state="set_type", fact=measure_id, type=measure_type)

    @timing
    def export(self, path: str, file_format: str) -> [Tuple, str]:
        """
        Экспортировать файл
        :param path: (str) путь, по которому файл будет сохранен
        :param file_format: (str) формат сохраненного файла: "csv", "xls", "json"
        :return (Tuple): file_name, path
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, file_format)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # Экспортировать полученный результат
        self.execute_olap_command(
            command_name="xls_export",
            state="start",
            export_format=file_format,
            export_destination_type="local"
        )

        logging.info("Waiting for file name...")
        time.sleep(10)
        result = self.execute_olap_command(command_name="xls_export", state="check")
        # progress doesn't work
        # progress = result["queries"][0]["command"]["progress"]
        # print("Progress: %s" % progress)

        file_name = self.h.parse_result(result=result, key="file_name")
        if self.jupiter:
            if "ERROR" in str(file_name):
                return file_name

        logging.info("File name: %s", file_name)

        # URL, по которому лежит файл экспортируемый файл: базовый URL/resources/файл
        file_url = self.url + "/" + "resources" + "/" + file_name

        # выполнить запрос
        try:
            r = self.exec_request.execute_request(params=file_url, method="GET")
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # сохранить файл по указанному пути
        file_name = file_name[:-8].replace(":", "_")
        filePath = path + "//" + file_name

        # запись файла в указанную директорию
        try:
            with open(filePath, 'wb') as f:
                f.write(r.content)
        except IOError as e:
            logging.exception("EXCEPTION!!! %s", e)
            logging.exception("Creating path recursively...")
            os.makedirs(path, exist_ok=True)
            with open(filePath, 'wb') as f:
                f.write(r.content)

        # проверка что файл скачался после экспорта
        filesList = os.listdir(path)
        assert file_name in filesList, "File %s not in path %s" % (file_name, path)
        return file_name, path

    @timing
    def create_calculated_measure(self, new_name: str, formula: str) -> [Dict, str]:
        """
        Создать вычислимый факт. Элементы формулы должный быть разделеный ПРОБЕЛОМ!
        Список используемых операндов: ["=", "+", "-", "*", "/", "<", ">", "!=", "<=", ">="]

        Примеры формул:
        top([Сумма долга];1000)
        100 + [Больницы] / [Количество вызовов врача] * 2 + corr([Количество вызовов врача];[Больницы])

        :param new_name: (str) Имя нового факта
        :param formula: (str) формула. Элементы формулы должный быть разделеный ПРОБЕЛОМ!
        :return: (Dict) команда модуля Olap "fact", состояние: "create_calc"
        """
        # получить данные мультисферы
        self.get_multisphere_data()

        # преобразовать строковую формулу в список
        formula_lst = formula.split()
        # количество фактов == кол-во итераций
        join_iterations = formula.count("[")
        # если в названии фактов есть пробелы, склеивает их обратно
        formula_lst = self.h.join_splited_measures(formula_lst, join_iterations)

        # параметра formula
        output = ""
        opening_brackets = 0
        closing_brackets = 0
        try:
            for i in formula_lst:
                if i == "(":
                    output += "("
                    opening_brackets += 1
                    continue
                elif i == ")":
                    output += ")"
                    closing_brackets += 1
                    continue
                elif i == "not":
                    output += "not"
                    continue
                elif i == "and":
                    output += "and"
                    continue
                elif i == "or":
                    output += "or"
                    continue
                elif "total(" in i:
                    m = re.search('\[(.*?)\]', i)
                    total_content = m.group(0)
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", total_content[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure_id:
                            return measure_id
                    output += "total(%s)" % measure_id
                    continue
                elif "top(" in i:
                    # top([из чего];сколько)
                    m = re.search('\[(.*?)\]', i)
                    measure_name = m.group(0)[1:-1]
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                    if self.jupiter:
                        if "ERROR" in measure_id:
                            return measure_id

                    m = re.search('\d+', i)
                    int_value = m.group(0)

                    output += "top( fact(%s) ;%s)" % (measure_id, int_value)
                    continue
                elif "if(" in i:
                    message = "if(;;) не реализовано!"
                    logging.warning(message)
                    logging.exception("APPLICATION STOPPED")
                    self.current_exception = message
                    if self.jupiter:
                        return self.current_exception
                    raise
                elif "corr(" in i:
                    m = re.search('\((.*?)\)', i)
                    measures = m.group(1).split(";")
                    measure1 = measures[0]
                    measure2 = measures[1]
                    measure1 = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure1[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure1:
                            return measure1
                    measure2 = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure2[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure2:
                            return measure2
                    output += "corr( fact(%s) ; fact(%s) )" % (measure1, measure2)
                    continue
                elif i[0] == "[":
                    # если пользователь ввел факт в формте [2019,Больница]
                    # где 2019 - элемент самой верхней размерности, Больница - название факта
                    if "," in i:
                        measure_content = i[1:-1].split(",")
                        elem = measure_content[0]
                        measure_name = measure_content[1]

                        # сформировать словарь {"элемент верхней размерности": индекс_элемнета}
                        result = self.execute_olap_command(command_name="view",
                                                           state="get_2",
                                                           from_row=0,
                                                           from_col=0,
                                                           num_row=1,
                                                           num_col=1)

                        top_dims = self.h.parse_result(result=result, key="top_dims")
                        if self.jupiter:
                            if "ERROR" in str(top_dims):
                                return top_dims
                        result = self.execute_olap_command(command_name="dim_element_list_data", state="pattern_change",
                                                           dimension=top_dims[0], pattern="", num=30)

                        top_dim_values = self.h.parse_result(result=result, key="data")
                        if self.jupiter:
                            if "ERROR" in str(top_dim_values):
                                return top_dim_values
                        top_dim_indexes = self.h.parse_result(result=result, key="indexes")
                        if self.jupiter:
                            if "ERROR" in str(top_dim_indexes):
                                return top_dim_indexes
                        top_dim_dict = dict(zip(top_dim_values, top_dim_indexes))

                        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                        if self.jupiter:
                            if "ERROR" in str(measure_id):
                                return measure_id

                        output += " fact(%s; %s) " % (measure_id, top_dim_dict[elem])
                        continue
                    measure_name = i[1:-1]
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                    if self.jupiter:
                        if "ERROR" in str(measure_id):
                            return measure_id
                    output += " fact(%s) " % measure_id
                    continue
                elif i in OPERANDS:
                    output += i
                    continue
                elif i.isnumeric():
                    output += i
                    continue
                else:
                    raise ValueError("Unknown element in formula: %s " % i)

            if opening_brackets != closing_brackets:
                raise ValueError("Неправильный баланс скобочек в формуле!\nОткрывающих скобочек: %s \n"
                                 "Закрывающих скобочек: %s" % (opening_brackets, closing_brackets))
        except BaseException as e:
            logging.exception("EXCEPTION!!! %s\n%s", e, traceback.format_exc())
            logging.exception("APPLICATION STOPPED!!!")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        result = self.execute_olap_command(command_name="fact",
                                           state="create_calc",
                                           name=new_name,
                                           formula=output,
                                           uformula=formula)

        return result

    @timing
    def run_scenario(self, scenario_id: Union[str, None] = None, scenario_name: Union[str, None] = None,
                     timeout: int = 60) -> [Dict, str, bool]:
        """
        Запустить сценарий и дождаться его загрузки. В параметрах нужно указать id сценария или имя сценария
        :param scenario_id: uuid сценария
        :param scenario_name: название сценария
        :param timeout: (int) таймаут
        :return: (Dict) результат выполнения команды модуля Manager: command_name="user_iface", state="save_settings",
                 module_id, settings
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, scenario_id, scenario_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # Получить список слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers = set()

        session_layers_lst = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers_lst):
                return session_layers_lst

        for i in session_layers_lst:
            layers.add(i["uuid"])

        # Получить данные по всем сценариям
        script_data = self.execute_manager_command(command_name="script", state="list")

        request_queries = script_data.get("queries")
        request_queries = next(iter(request_queries))
        script_desc = request_queries.get("command", {}).get("script_descs")

        if (scenario_name is not None) and (scenario_id is not None):
            script_id = self.h.get_scenario_data(script_data, scenario_name)
            if self.jupiter:
                if "ERROR" in script_id:
                    return script_id
            if script_id != scenario_id:
                # raise ValueError("ID или имя сценария некорректно!")
                message = "ERROR!!! ID или имя сценария некорректно!"
                logging.error(message)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise
            # Запустить сценарий
            self.execute_manager_command(command_name="script", state="run", script_id=scenario_id)

        # если пользователь ввел имя сценария:
        elif (scenario_name is not None) and (scenario_id is None):
            # Получить id сценария
            script_id = self.h.get_scenario_data(script_data, scenario_name)
            if self.jupiter:
                if "ERROR" in script_id:
                    return script_id

            # Запустить сценарий
            self.execute_manager_command(command_name="script", state="run", script_id=script_id)

        # если пользователь ввел ID сценария:
        elif (scenario_id is not None) and (scenario_name is None):
            # проверка корректности ID сценария
            uuids = []
            for script in script_desc:
                uuids.append(script["uuid"])
            if scenario_id not in uuids:
                # raise ValueError("No such scenario!")
                message = "ERROR!!! No such scenario!"
                logging.error(message)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise

            # Запустить сценарий
            self.execute_manager_command(command_name="script", state="run", script_id=scenario_id)

        # Сценарий должен создать новый слой и запуститься на нем
        # Получить список слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        # Получить новый список слоев сессии
        new_layers = set()

        session_layers_lst = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in session_layers_lst:
                return session_layers_lst

        for i in session_layers_lst:
            new_layers.add(i["uuid"])
        self.layers_list = list(new_layers)

        # получить id слоя, на котором запущен наш сценарий
        target_layer = new_layers - layers
        sc_layer = next(iter(target_layer))

        # ожидание загрузки сценария на слое
        output = self.h.wait_scenario_layer_loaded(sc_layer, timeout)
        if self.jupiter:
            if "EXCEPTION" in str(output):
                return output

        # параметр settings, для запроса, который делает слой активным
        settings = {"Profile": {
            "geometry": {"height": None, "width": 300, "x": 540.3125,
                         "y": "center", "z": 780}}, "cubes": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 813}}, "users": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 788}},
            "wm_layers2": {"lids": list(new_layers),
                           "active": sc_layer}}

        session_layers = self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layer_progress = self.h.parse_result(result=session_layers, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layer_progress):
                return user_layer_progress

        # проверка, что слой не в статусе Running
        # список module_descs должен заполнится, только если слой находится в статусе Stopped
        for _ in count(0):
            start = time.time()
            for i in user_layer_progress:
                if (i["uuid"] == sc_layer) and (i["script_run_status"]["message"] == "Running"):
                    session_layers = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
                    user_layer_progress = self.h.parse_result(result=session_layers, key="layers")
                    if self.jupiter:
                        if "ERROR" in str(user_layer_progress):
                            return user_layer_progress
                    time.sleep(5)
                end = time.time()
                exec_time = end - start
                if exec_time > 60.0:
                    logging.error("ERROR!!! Waiting script_run_status is too long! Layer info: %s", i)
                    logging.error("APPLICATION STOPPED!!!")
                    self.current_exception = "ERROR!!! Waiting script_run_status is too long! Layer info: %s" % i
                    if self.jupiter:
                        return self.current_exception
                    raise
            break

        # обновить get_session_layers
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layers = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layers):
                return user_layers

        for i in user_layers:
            if i["uuid"] == sc_layer:
                # для случаев, когда "module_descs" - пустой список (пустой сценарий) - вернуть False
                if not i["module_descs"]:
                    return False
                try:
                    self.multisphere_module_id = i["module_descs"][0]["uuid"]
                except IndexError:
                    logging.exception("No module_descs for layer id %s\nlayer data: %s", sc_layer, i)
                    logging.exception("APPLICATION STOPPED!!!")
                    self.current_exception = "No module_descs for layer id %s\nlayer data: %s" % (sc_layer, i)
                    if self.jupiter:
                        return self.current_exception
                    raise

                self.active_layer_id = i["uuid"]
                # инициализация модуля Olap (на случай, если нужно будет выполнять команды для работы с мультисферой)
                self.olap_command = olap_commands.OlapCommands(self.session_id, self.multisphere_module_id,
                                                               self.url, self.server_codes, self.jupiter)

                # Выбрать слой с запущенным скриптом
                self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=i["uuid"])

                self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=i["uuid"])

                result = self.execute_manager_command(command_name="user_iface", state="save_settings",
                                                      module_id=self.authorization_uuid, settings=settings)

                self.update_total_row()

                return result

    @timing
    def run_scenario_by_id(self, sc_id) -> Dict:
        """
        Запустить сценарий по id
        :param sc_id: id сценария
        :return: (Dict) command_name="script", state="run"
        """
        return self.execute_manager_command(command_name="script", state="run", script_id=sc_id)

    @timing
    def run_scenario_by_user(self, scenario_name: str, user_name: str, units: int = 500, timeout: int = 60) -> [Dict,
                                                                                                                str,
                                                                                                                bool]:
        """
        Запуск сценария от имени заданного пользователя.
        Внутри данного метода будет создана новая сессия (указанного пользователя). После выполнения сценария сессия будет убита.
        В параметрах нужно указать название сценария и имя используемого пользователя.
        :param scenario_name: название сценария
        :param user_name: имя пользователя, под которым запускается сценарий
        :param units: число строк мультисферы, из которых потом данные будут выгружены в данные мультисферы (df), данные о колонках (df_cols)
        :param timeout: (int) таймаут
        :return: (Tuple)  данные мультисферы df, данные о колонках мультсферы df_cols
        """
        sc = BusinessLogic(login=user_name, url=self.url)

        # Получить список слоев сессии
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers = set()

        session_layers_lst = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers_lst):
                return session_layers_lst

        for i in session_layers_lst:
            layers.add(i["uuid"])

        # Получить данные по всем сценариям
        script_data = sc.execute_manager_command(command_name="script", state="list")

        # Получить id сценария
        script_id = sc.h.get_scenario_data(script_data, scenario_name)
        if self.jupiter:
            if "ERROR" in script_id:
                return script_id

        # Запустить сценарий
        sc.execute_manager_command(command_name="script", state="run", script_id=script_id)

        # Сценарий должен создать новый слой и запуститься на нем
        # Получить список слоев сессии
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        # Получить новый список слоев сессии
        new_layers = set()

        session_layers_lst = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in session_layers_lst:
                return session_layers_lst

        for i in session_layers_lst:
            new_layers.add(i["uuid"])
        sc.layers_list = list(new_layers)

        # получить id слоя, на котором запущен наш сценарий
        target_layer = new_layers - layers
        sc_layer = next(iter(target_layer))

        # ожидание загрузки сценария на слое
        output = sc.h.wait_scenario_layer_loaded(sc_layer, timeout)
        if self.jupiter:
            if "EXCEPTION" in str(output):
                return output

        # параметр settings, для запроса, который делает слой активным
        settings = {"Profile": {
            "geometry": {"height": None, "width": 300, "x": 540.3125,
                         "y": "center", "z": 780}}, "cubes": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 813}}, "users": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 788}},
            "wm_layers2": {"lids": list(new_layers),
                           "active": sc_layer}}

        session_layers = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layer_progress = sc.h.parse_result(result=session_layers, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layer_progress):
                return user_layer_progress

        # проверка, что слой не в статусе Running
        # список module_descs должен заполнится, только если слой находится в статусе Stopped
        for _ in count(0):
            start = time.time()
            for i in user_layer_progress:
                if (i["uuid"] == sc_layer) and (i["script_run_status"]["message"] == "Running"):
                    session_layers = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
                    user_layer_progress = sc.h.parse_result(result=session_layers, key="layers")
                    if self.jupiter:
                        if "ERROR" in str(user_layer_progress):
                            return user_layer_progress
                    time.sleep(5)
                end = time.time()
                exec_time = end - start
                if exec_time > 60.0:
                    logging.error("ERROR!!! Waiting script_run_status is too long! Layer info: %s", i)
                    logging.error("APPLICATION STOPPED!!!")
                    self.current_exception = "ERROR!!! Waiting script_run_status is too long! Layer info: %s" % i
                    if self.jupiter:
                        return self.current_exception
                    raise
            break

        # обновить get_session_layers
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layers = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layers):
                return user_layers

        for i in user_layers:
            if i["uuid"] == sc_layer:
                # для случаев, когда "module_descs" - пустой список (пустой сценарий) - вернуть False
                if not i["module_descs"]:
                    return False
                try:
                    sc.multisphere_module_id = i["module_descs"][0]["uuid"]
                except IndexError:
                    logging.exception("No module_descs for layer id %s\nlayer data: %s", sc_layer, i)
                    logging.exception("APPLICATION STOPPED!!!")
                    self.current_exception = "No module_descs for layer id %s\nlayer data: %s" % (sc_layer, i)
                    if self.jupiter:
                        return self.current_exception
                    raise

                sc.active_layer_id = i["uuid"]
                # инициализация модуля Olap (на случай, если нужно будет выполнять команды для работы с мультисферой)
                sc.olap_command = olap_commands.OlapCommands(sc.session_id, sc.multisphere_module_id,
                                                             sc.url, sc.server_codes, sc.jupiter)

                # Выбрать слой с запущенным скриптом
                sc.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=i["uuid"])

                sc.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=i["uuid"])

                sc.execute_manager_command(command_name="user_iface", state="save_settings",
                                           module_id=self.authorization_uuid, settings=settings)

                sc.update_total_row()
                gen = sc.get_data_frame(units=units)
                self.df, self.df_cols = next(gen)
                sc.logout()

                return self.df, self.df_cols

    @timing
    def get_data_frame(self, units: int = 100):
        """
        Подгрузка мультисферы постранично, порциями строк.
        Приверы использования:
        I.
        gen = sc.get_data_frame()

        df, df_cols = next(gen)
        print(df)
        print(df_cols)

        II.
        gen = sc.get_data_frame()

        for i in gen:
            print("----")
            print(df)
            print(df_cols)

        :param units: количество подгружаемых строк, будет использоваться в num_row
        :return:
        """

        result = self.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                           num_row=1,
                                           num_col=1)
        total_cols = self.h.parse_result(result, "total_col")

        start = 0
        while self.total_row > 0:
            self.total_row = self.total_row - units
            result = self.execute_olap_command(
                command_name="view",
                state="get_2",
                from_row=start,
                from_col=0,
                num_row=units,
                num_col=total_cols
            )
            data = self.h.parse_result(result=result, key="data")
            df = pd.DataFrame(data[1:], columns=data[0])  # данные мультисферы
            df_cols = pd.DataFrame(data[0])  # названия колонок
            yield df, df_cols
            start += units
        return

    @timing
    def set_measure_level(self, measure_name: str, level: int) -> [Dict, str]:
        """
        Установить Уровень расчета факта
        :param measure_name: (str) имя факта
        :param level: (int) выставляет Уровень расчета
        :return: (Dict) результат выполнения команды: fact, state: set_level
        """
        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter:
            if "ERROR" in measure_id:
                return measure_id

        # выполнить команду: fact, state: set_level
        command1 = self.olap_command.collect_command(module="olap",
                                                     command_name="fact",
                                                     state="set_level",
                                                     fact=measure_id,
                                                     level=level)

        command2 = self.olap_command.collect_command("olap", "fact", "list_rq")
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        return result

    @timing
    def set_measure_precision(self, measure_names: List, precision: List) -> [Dict, str]:
        """
        Установить Уровень расчета факта
        :param measure_names: (List) список с именами фактов
        :param precision: (List) список с точностями фактов
                                (значения должны соответствовать значениям списка measure_names)
        :return: (Dict) результат выполнения команды: user_iface, state: save_settings
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, measure_names, precision)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить словать с размаерностями, фактами и данными
        self.get_multisphere_data()

        # получить id фактов
        measure_ids = []
        for measure_name in measure_names:
            measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
            if self.jupiter:
                if "ERROR" in measure_id:
                    return measure_id
            measure_ids.append(measure_id)

        # settings with precision for fact id
        settings = {"factsPrecision": {}}
        for idx, f_id in enumerate(measure_ids):
            settings["factsPrecision"].update({f_id: str(precision[idx])})

        # выполнить команду: user_iface, state: save_settings
        return self.execute_manager_command(command_name="user_iface",
                                            state="save_settings",
                                            module_id=self.multisphere_module_id,
                                            settings=settings)

    @timing
    def clone_current_olap_module(self) -> Dict:
        """
        Создать копию текущего OLAP-модуля
        :return: (Dict) ответ зпроса command:user_iface, state:clone_module
        """
        result = self.execute_manager_command(command_name="user_iface",
                                              state="clone_module",
                                              module_id=self.multisphere_module_id,
                                              layer_id=self.active_layer_id)

        # переключиться на module id созданной копии OLAP-модуля
        self.multisphere_module_id = self.h.parse_result(result=result, key="module_desc", nested_key="uuid")

        if self.jupiter:
            if "ERROR" in self.multisphere_module_id:
                return self.multisphere_module_id

        self.update_total_row()

        return result

    @timing
    def set_measure_visibility(self, measure_names: Union[str, List], is_visible: bool = False) -> [List, str]:
        """
        Изменение видимости факта (скрыть / показать факт).
        Можно изменять видимость одного факта или списка фактов.
        :param measure_names: (str, List) название факта/фактов
        :param is_visible: (bool) скрыть (False) / показать (True) факт. По умолчанию факт скрывается.
        :return: (List) список id фактов с изменной видимостью
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, is_visible)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # список фактов с измененной видимостью
        m_ids = []

        # если передан один факт (строка)
        if isinstance(measure_names, str):
            m_id = self.get_measure_id(measure_name=measure_names)

            self.execute_olap_command(command_name="fact", state="set_visible", fact=m_id, is_visible=is_visible)
            m_ids.append(m_id)
            return m_ids

        # если передан список фактов
        for measure in measure_names:
            m_id = self.get_measure_id(measure_name=measure)
            if not m_id:
                logging.error("No such measure name: %s", measure)
                continue
            self.execute_olap_command(command_name="fact", state="set_visible", fact=m_id, is_visible=is_visible)
            m_ids.append(m_id)
        return m_ids

    @timing
    def sort_measure(self, measure_name: str, sort_type: str) -> [Dict, str]:
        """
        Сортировать значения факта по возрастанию или по убыванию
        :param measure_name: (str) Имя факта
        :param sort_type: (int) "ascending"/"descending" (по возрастанию / по убыванию)
        :return: (Dict) command_name="view", state="set_sort"
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, sort_type)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        sort_values = {"ascending": 1, "descending": 2}
        sort_type = sort_values[sort_type]

        # получить данные нескрытых фактов (те, которые вынесены в колонки)
        result = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                           num_row=20, num_col=20)
        measures_data = self.h.parse_result(result=result, key="top")
        if self.jupiter:
            if "ERROR" in str(measures_data):
                return measures_data
        measures_list = []
        for i in measures_data:
            for elem in i:
                if "fact_id" in elem:
                    measure_id = elem["fact_id"].rstrip()
                    measures_list.append(self.get_measure_name(measure_id))

        # индекс нужного факта
        measure_index = measures_list.index(measure_name)

        return self.execute_olap_command(command_name="view", state="set_sort", line=measure_index, sort_type=sort_type)

    @timing
    def unfold_all_dims(self, position: str, level: int, num_row: int = 100, num_col: int = 100) -> [Dict, str]:
        """
        Развернуть все элементы размерности
        :param position: (str) "left" / "up"  (левые / верхние размерности )
        :param level: (int) 0, 1, 2, ... (считается слева-направо для левой позиции,
                            сверху - вниз для верхней размерности)
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере
        :param num_col: (int) Количество колонок, которые будут отображаться в мультисфере
        :return: (Dict) after request view get_hints
        """
        # проверки
        try:
            position = error_handler.checks(self, self.func_name, position)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # view   fold_all_at_level
        arraysDict = []
        for i in range(0, level + 1):
            arraysDict.append(self.olap_command.collect_command(module="olap", command_name="view",
                                                                state="fold_all_at_level", position=position, level=i))
        query = self.olap_command.collect_request(*arraysDict)
        try:
            self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # view  get
        self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                  num_row=num_row, num_col=num_col)

        # view  get_hints
        command1 = self.olap_command.collect_command(module="olap",
                                                     command_name="view",
                                                     state="get_hints",
                                                     position=1,
                                                     hints_num=100)
        command2 = self.olap_command.collect_command(module="olap",
                                                     command_name="view",
                                                     state="get_hints",
                                                     position=2,
                                                     hints_num=100)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)
        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def move_measures(self, new_order: List) -> [str, Any]:
        """
        Функция, упорядочивающая факты в заданной последовательности

        Пример: self.move_measures(new_order=["факт1", "факт2", "факт3", "факт4"])

        :param new_order: (List) список упорядоченных фактов
        :return: (str) сообщение об ошибке или об успехе
        """
        c = 0
        for idx, new_elem in enumerate(new_order):
            # get ordered measures list
            result = self.execute_olap_command(command_name="fact", state="list_rq")
            measures_data = self.h.parse_result(result=result, key="facts")
            if self.jupiter:
                if "ERROR" in str(measures_data):
                    return measures_data
            measures_list = [i["name"].rstrip() for i in measures_data]  # measures list in polymatica

            # check if measures are already ordered
            if (measures_list == new_order) and (c == 0):
                logging.warning("WARNING!!! Facts are already ordered!")
                return

            measure_index = measures_list.index(new_elem)
            # если индекс элемента совпал, то перейти к следующей итерации
            if measures_list.index(new_elem) == idx:
                continue

            # id факта
            measure_id = self.get_measure_id(new_elem)

            # offset
            measure_index -= c

            self.execute_olap_command(command_name="fact", state="move", fact=measure_id, offset=-measure_index)
            c += 1
        self.update_total_row()
        return "Fact successfully ordered!"

    @timing
    def set_width_columns(self, measures: List, left_dims: List, width: int = 890, height: int = 540) -> [Dict, str]:
        """
        Установить ширину колонок
        :param measures: [List] спиок с новыми значениями ширины фактов.
            ВАЖНО! Длина списка должна совпадать с количеством нескрытых фактов в мультисфере
            пример списка: [300, 300, 300, 233, 154]
        :param left_dims: [List] спиок с новыми значениями ширины рзамерностей, вынесенных в левую размерность.
        :param width: (int) ширина таблицы
        :param height: (int) высота таблицы
        :return: user_iface save_settings
        """
        # получить список нескрытых фактов
        result = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                           num_row=20, num_col=20)
        measures_data = self.h.parse_result(result=result, key="top")
        if self.jupiter:
            if "ERROR" in str(measures_data):
                return measures_data
        measures_list = []
        for i in measures_data:
            for elem in i:
                if "fact_id" in elem:
                    measure_id = elem["fact_id"].rstrip()
                    measures_list.append(self.get_measure_name(measure_id))

        # проверки
        try:
            error_handler.checks(self, self.func_name, measures, measures_list)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        settings = {"dimAndFactShow": True,
                    "itemWidth": measures,
                    "geometry": {"width": width, "height": height},
                    "workWidths": left_dims}

        return self.execute_manager_command(command_name="user_iface", state="save_settings",
                                            module_id=self.multisphere_module_id, settings=settings)

    @timing
    def load_profile(self, name: str) -> [Dict, str]:
        """
        Загрузить профиль по его названию
        :param name: (str) название нужного профиля
        :return: (Dict) user_iface, save_settings
        """
        # Получить множество слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers = set()

        session_layers = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers):
                return session_layers

        for i in session_layers:
            layers.add(i["uuid"])

        # Получить сохраненные профили
        result = self.execute_manager_command(command_name="user_layer", state="get_saved_layers")

        # Получить uuid профиля по его интерфейсному названию
        layers_descriptions = self.h.parse_result(result=result, key="layers_descriptions")
        if self.jupiter:
            if "ERROR" in str(layers_descriptions):
                return layers_descriptions

        self.active_layer_id = ""
        for i in layers_descriptions:
            if i["name"] == name:
                self.active_layer_id = i["uuid"]
        if self.active_layer_id == "":
            logging.error("No such profile: %s", name)
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "No such profile: %s" % name
            if self.jupiter:
                return self.current_exception
            raise

        # Загрузить сохраненный профиль
        self.execute_manager_command(command_name="user_layer", state="load_saved_layer", layer_id=self.active_layer_id)

        # Получить новое множество слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        new_layers = set()
        session_layers = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers):
                return session_layers
        for i in session_layers:
            new_layers.add(i["uuid"])

        # получить id слоя, на котором запущен загруженный сценарий
        target_layer = new_layers - layers
        sc_layer = next(iter(target_layer))

        # параметр settings, для запроса, который делает слой активным
        settings = {"Profile": {
            "geometry": {"height": None, "width": 300, "x": 540.3125,
                         "y": "center", "z": 780}}, "cubes": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 813}}, "users": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 788}},
            "wm_layers2": {"lids": list(new_layers),
                           "active": sc_layer}}
        for i in session_layers:
            if i["uuid"] == sc_layer:
                try:
                    self.multisphere_module_id = i["module_descs"][0]["uuid"]
                except IndexError:
                    logging.error("ERROR!!! No module_descs for layer id %s\nlayer data: %s", sc_layer, i)
                    logging.error("APPLICATION STOPPED!!!")
                    self.current_exception = "No module_descs for layer id %s\nlayer data: %s" % (sc_layer, i)
                    if self.jupiter:
                        return self.current_exception
                    raise

                self.active_layer_id = i["uuid"]
                # инициализация модуля Olap (на случай, если нужно будет выполнять команды для работы с мультисферой)
                self.olap_command = olap_commands.OlapCommands(self.session_id, self.multisphere_module_id,
                                                               self.url, self.server_codes, self.jupiter)

                # Выбрать слой с запущенным скриптом
                self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=i["uuid"])

                self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=i["uuid"])

                # ожидание загрузки слоя
                result = self.execute_manager_command(command_name="user_layer", state="get_load_progress",
                                                      layer_id=i["uuid"])
                progress = self.h.parse_result(result, "progress")
                while progress < 100:
                    time.sleep(0.5)
                    result = self.execute_manager_command(command_name="user_layer", state="get_load_progress",
                                                          layer_id=i["uuid"])
                    progress = self.h.parse_result(result, "progress")

                result = self.execute_manager_command(command_name="user_iface", state="save_settings",
                                                      module_id=self.authorization_uuid, settings=settings)
                self.update_total_row()

                return result

    @timing
    def create_sphere(self, cube_name: str, source_name: str, file_type: str, update_params: Dict,
                      sql_params: Dict = None, user_interval: str = "с текущего дня", filepath: str = "", separator="",
                      increment_dim=None, encoding: str = False, delayed: bool = False) -> [str, Dict]:
        """
        Создать мультисферу через импорт из источника
        :param cube_name: (str) название мультисферы, которую будем создавать
        :param filepath: (str) путь к файлу, либо (если файл лежит в той же директории) название файла.
            Не обязательно для бд
        :param separator: (str) разделитель для csv-источника. По умолчанию разделитель не выставлен
        :param increment_dim: (str) название размерности, необходимое для инкрементального обновления.
                            На уровне API параметр называется increment_field
        :param sql_params: (Dict) параметры для источника данных SQL.
            Параметры, которые нужно передать в словарь: server, login, passwd, sql_query
            Пример: {"server": "10.8.0.115",
                     "login": "your_user",
                     "passwd": "your_password",
                     "sql_query": "SELECT * FROM DIFF_data.dbo.TableForTest"}
        :param update_params: (Dict) параметры обновления мультисферы.
            Типы обновления:
              - "ручное"
              - "по расписанию"
              - "интервальное"
              - "инкрементальное" (доступно ТОЛЬКО для источника SQL!)
            Для всех типов обновления, кроме ручного, нужно обязательно добавить параметр schedule.
            Его значение - словарь.
               В параметре schedule параметр type:
               {"Ежедневно": 1,
                "Еженедельно": 2,
                "Ежемесячно": 3}
            В параметре schedule параметр time записывается в формате "18:30" (в запрос передается UNIX-time).
            В параметре schedule параметр time_zone записывается как в server-codes: "UTC+3:00"
            В параметре schedule параметр week_day записывается как в списке:
               - "понедельник"
               - "вторник"
               - "среда"
               - "четверг"
               - "пятница"
               - "суббота"
               - "воскресенье"
            Пример: {"type": "по расписанию",
                     "schedule": {"type": "Ежедневно", "time": "18:30", "time_zone": "UTC+3:00"}}
        :param user_interval: (str) интервал обновлений. Указать значение:
               {"с текущего дня": 0,
                "с предыдущего дня": 1,
                "с текущей недели": 2,
                "с предыдущей недели
                "с и по указанную дату": 11}": 3,
                "с текущего месяца": 4,
                "с предыдущего месяца": 5,
                "с текущего квартала": 6,
                "с предыдущего квартала": 7,
                "с текущего года": 8,
                "с предыдущего года": 9,
                "с указанной даты": 10,
                "с и по указанную дату": 11}
        :param source_name: (str) поле Имя источника. Не должно быть пробелов, и длина должна быть больше 5 символов!
        :param file_type: (str) формат файла. См. значения в server-codes.json
        :param encoding: (str) кодировка, например, UTF-8 (обязательно для csv!)
        :param delayed: (bool) отметить чекбокс "Создать мультисферу при первом обновлении."
        :return: (Dict) command_name="user_cube", state="save_ext_info_several_sources_request"
        """

        encoded_file_name = ""  # response.headers["File-Name"] will be stored here after PUT upload of csv/excel

        interval = {"с текущего дня": 0,
                    "с предыдущего дня": 1,
                    "с текущей недели": 2,
                    "с предыдущей недели": 3,
                    "с текущего месяца": 4,
                    "с предыдущего месяца": 5,
                    "с текущего квартала": 6,
                    "с предыдущего квартала": 7,
                    "с текущего года": 8,
                    "с предыдущего года": 9,
                    "с указанной даты": 10,
                    "с и по указанную дату": 11}

        # часовые зоны
        time_zones = self.server_codes["manager"]["timezone"]
        # проверки
        try:
            error_handler.checks(self, self.func_name, update_params, UPDATES, file_type, sql_params,
                                 user_interval, interval, PERIOD, WEEK, time_zones, source_name, cube_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        interval = interval[user_interval]

        if update_params["type"] != "ручное":
            # установить значение периода для запроса
            user_period = update_params["schedule"]["type"]
            update_params["schedule"]["type"] = PERIOD[user_period]

            # установить значение часовой зоны для запроса
            h_timezone = update_params["schedule"]["time_zone"]
            update_params["schedule"]["time_zone"] = time_zones[h_timezone]

            # преобразование времение в UNIX time
            user_time = update_params["schedule"]["time"]
            h_m = user_time.split(":")
            d = datetime.datetime(1970, 1, 1, int(h_m[0]) + 3, int(h_m[1]), 0)
            unixtime = time.mktime(d.timetuple())
            unixtime = int(unixtime)
            update_params["schedule"]["time"] = unixtime

        # пармаметр server_types для различных форматов данных
        server_types = self.server_codes["manager"]["data_source_type"]
        server_type = server_types[file_type]

        # создать мультисферу, получить id куба
        result = self.execute_manager_command(command_name="user_cube", state="create_cube_request",
                                              cube_name=cube_name)
        self.cube_id = self.h.parse_result(result=result, key="cube_id")
        if self.jupiter:
            if "ERROR" in self.cube_id:
                return self.cube_id

        # upload csv file
        if (file_type == "excel") or (file_type == "csv"):
            try:
                response = self.exec_request.execute_request(params=filepath, method="PUT")
            except BaseException as e:
                logging.exception(e)
                logging.exception("APPLICATION STOPPED")
                self.current_exception = str(e)
                if self.jupiter:
                    return self.current_exception
                raise

            encoded_file_name = response.headers["File-Name"]

        # data preview request, выставить кодировку UTF-8
        preview_data = {"name": source_name,
                        "server": "",
                        "server_type": server_type,
                        "login": "",
                        "passwd": "",
                        "database": "",
                        "sql_query": separator,
                        "skip": -1}
        # для бд выставить параметры server, login, passwd:
        if (file_type != "csv") and (file_type != "excel"):
            preview_data.update({"server": sql_params["server"]})
            preview_data.update({"login": sql_params["login"]})
            preview_data.update({"passwd": sql_params["passwd"]})
            preview_data.update({"sql_query": ""})
            # для бд psql прописать параметр database=postgres
            if file_type == "psql":
                preview_data.update({"database": "postgres"})
            # соединиться с бд
            result = self.execute_manager_command(command_name="user_cube",
                                                  state="test_source_connection_request",
                                                  datasource=preview_data)

        # для формата данных csv выставить кодировку
        if file_type == "csv":
            preview_data.update({"encoding": encoding})
        # для файлов заполнить параметр server:
        if (file_type == "csv") or (file_type == "excel"):
            preview_data.update({"server": encoded_file_name})

        # для бд заполнить параметр sql_query
        if (file_type != "csv") and (file_type != "excel"):
            preview_data.update({"sql_query": sql_params["sql_query"]})
        # для бд psql прописать параметр database=postgres
        if file_type == "psql":
            preview_data.update({"database": "postgres"})

        self.execute_manager_command(command_name="user_cube",
                                     state="data_preview_request",
                                     datasource=preview_data)

        # для формата данных csv сделать связь данных
        if file_type == "csv":
            self.execute_manager_command(command_name="user_cube",
                                         state="structure_preview_request",
                                         cube_id=self.cube_id,
                                         links=[])

        # добавить источник данных
        preview_data = [{"name": source_name,
                         "server": "",
                         "server_type": server_type,
                         "login": "",
                         "passwd": "",
                         "database": "",
                         "sql_query": separator,
                         "skip": -1}]
        # для формата данных csv выставить кодировку
        if file_type == "csv":
            preview_data[0].update({"encoding": encoding})
        # для файлов заполнить параметр server:
        if (file_type == "csv") or (file_type == "excel"):
            preview_data[0].update({"server": encoded_file_name})
        # для бд
        if (file_type != "csv") and (file_type != "excel"):
            preview_data[0].update({"server": sql_params["server"]})
            preview_data[0].update({"login": sql_params["login"]})
            preview_data[0].update({"passwd": sql_params["passwd"]})
            preview_data[0].update({"sql_query": sql_params["sql_query"]})
        # для бд psql прописать параметр database=postgres
        if file_type == "psql":
            preview_data[0].update({"database": "postgres"})
        self.execute_manager_command(command_name="user_cube",
                                     state="get_fields_request",
                                     cube_id=self.cube_id,
                                     datasources=preview_data)

        # структура данных
        result = self.execute_manager_command(command_name="user_cube", state="structure_preview_request",
                                              cube_id=self.cube_id, links=[])

        # словари с данными о размерностях
        dims = self.h.parse_result(result=result, key="dims")
        if self.jupiter:
            if "ERROR" in str(dims):
                return dims
        # словари с данными о фактах
        measures = self.h.parse_result(result=result, key="facts")
        if self.jupiter:
            if "ERROR" in str(measures):
                return measures

        try:
            # циклично добавить для каждой размерности {"field_type": "field"}
            for i in dims:
                i.update({"field_type": "field"})
                if file_type == "csv":
                    error_handler.checks(self, self.func_name, i)
            # циклично добавить для каждого факта {"field_type": "field"}
            for i in measures:
                i.update({"field_type": "field"})
                if file_type == "csv":
                    error_handler.checks(self, self.func_name, i)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # параметры для ручного обновления
        if update_params["type"] == "ручное":
            schedule = {"delayed": delayed, "items": []}
        elif update_params["type"] == "инкрементальное":
            # параметры для инкрементального обновления
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": "00000000"}
            # для сохранения id размерности инкремента
            increment_field = ""
            for dim in dims:
                if dim["name"] == increment_dim:
                    increment_field = dim["field_id"]
            if increment_dim is None:
                message = "Please fill in param increment_dim!"
                logging.error(message)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise
            if increment_field == "":
                logging.error("No such increment field in importing sphere: %s", increment_dim)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = "No such increment field in importing sphere: %s" % increment_dim
                if self.jupiter:
                    return self.current_exception
                raise
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval, increment_field=increment_field)
        elif update_params["type"] == "по расписанию":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
        elif update_params["type"] == "интервальное":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": None}
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval)
        else:
            logging.error("Unknown update type: %s", update_params["type"])
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "Unknown update type: %s" % update_params["type"]
            if self.jupiter:
                return self.current_exception
            raise
        interval = {"type": interval, "left_border": "", "right_border": "",
                    "dimension_id": "00000000"}
        # финальный запрос для создания мультисферы, обновление мультисферы
        return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                            cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                            schedule=schedule, interval=interval)

    @timing
    def update_cube(self, cube_name: str, update_params: Dict, user_interval: str = "с текущего дня",
                    delayed: bool = False, increment_dim=None) -> [Dict, str]:
        """
        Обновить существующий куб
        :param cube_name: (str) название мультисферы
        :param update_params: (Dict) параметры обновления мультисферы.
           Типы обновления:
              - "ручное"
              - "по расписанию"
              - "интервальное"
              - "инкрементальное" (доступно ТОЛЬКО для источника SQL!)
           Для всех типов обновления, кроме ручного, нужно обязательно добавить параметр schedule.
           Его значение - словарь.
               В параметре schedule параметр type:
               {"Ежедневно": 1,
                "Еженедельно": 2,
                "Ежемесячно": 3}
           В параметре schedule параметр time записывается в формате "18:30" (в запрос передается UNIX-time).
           В параметре schedule параметр time_zone записывается как в server-codes: "UTC+3:00"
           В параметре schedule параметр week_day записывается как в списке:
               - "понедельник"
               - "вторник"
               - "среда"
               - "четверг"
               - "пятница"
               - "суббота"
               - "воскресенье"
        :param user_interval: (str) интервал обновлений. Указать значение:
               {"с текущего дня": 0,
                "с предыдущего дня": 1,
                "с текущей недели": 2,
                "с предыдущей недели
                "с и по указанную дату": 11}": 3,
                "с текущего месяца": 4,
                "с предыдущего месяца": 5,
                "с текущего квартала": 6,
                "с предыдущего квартала": 7,
                "с текущего года": 8,
                "с предыдущего года": 9,
                "с указанной даты": 10,
                "с и по указанную дату": 11}
        :param increment_dim: (str) increment_dim_id, параметр необходимый для инкрементального обновления
        :param delayed: (bool) отметить чекбокс "Создать мультисферу при первом обновлении."
        :return: (Dict)user_cube save_ext_info_several_sources_request
        """
        interval = {"с текущего дня": 0,
                    "с предыдущего дня": 1,
                    "с текущей недели": 2,
                    "с предыдущей недели": 3,
                    "с текущего месяца": 4,
                    "с предыдущего месяца": 5,
                    "с текущего квартала": 6,
                    "с предыдущего квартала": 7,
                    "с текущего года": 8,
                    "с предыдущего года": 9,
                    "с указанной даты": 10,
                    "с и по указанную дату": 11}

        # часовые зоны
        time_zones = self.server_codes["manager"]["timezone"]

        # get cube id
        self.cube_name = cube_name
        result = self.execute_manager_command(command_name="user_cube", state="list_request")

        # получение списка описаний мультисфер
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if self.jupiter:
            if "ERROR" in str(cubes_list):
                return cubes_list

        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError as e:
            logging.exception("EXCEPTION!!! %s", e)
            logging.exception("APPLICATION STOPPED!!!")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить информацию о фактах и размерностях куба
        result = self.execute_manager_command(command_name="user_cube", state="ext_info_several_sources_request",
                                              cube_id=self.cube_id)

        # словари с данными о размерностях
        dims = self.h.parse_result(result=result, key="dims")
        if self.jupiter:
            if "ERROR" in str(dims):
                return dims
        # словари с данными о фактах
        measures = self.h.parse_result(result=result, key="facts")
        if self.jupiter:
            if "ERROR" in str(measures):
                return measures

        # циклично добавить для каждой размерности {"field_type": "field"}
        for i in dims:
            i.update({"field_type": "field"})
            # циклично добавить для каждого факта {"field_type": "field"}
        for i in measures:
            i.update({"field_type": "field"})

        if user_interval not in interval:
            logging.error("ERROR!!! No such interval: %s", user_interval)
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "ERROR!!! No such interval: %s" % user_interval
            if self.jupiter:
                return self.current_exception
            raise
        interval = interval[user_interval]

        if update_params["type"] != "ручное":
            # установить значение периода для запроса
            user_period = update_params["schedule"]["type"]
            update_params["schedule"]["type"] = PERIOD[user_period]

            # установить значение часовой зоны для запроса
            h_timezone = update_params["schedule"]["time_zone"]
            update_params["schedule"]["time_zone"] = time_zones[h_timezone]

            # преобразование времение в UNIX time
            user_time = update_params["schedule"]["time"]
            h_m = user_time.split(":")
            d = datetime.datetime(1970, 1, 1, int(h_m[0]) + 3, int(h_m[1]), 0)
            unixtime = time.mktime(d.timetuple())
            unixtime = int(unixtime)
            update_params["schedule"]["time"] = unixtime

        # параметры для ручного обновления
        if update_params["type"] == "ручное":
            schedule = {"delayed": delayed, "items": []}
        elif update_params["type"] == "инкрементальное":
            # параметры для инкрементального обновления
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": "00000000"}
            # для сохранения id размерности инкремента
            increment_field = ""
            for dim in dims:
                if dim["name"] == increment_dim:
                    increment_field = dim["field_id"]
            if increment_dim is None:
                message = "ERROR!!! Please fill in param increment_dim!"
                logging.error(message)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise
            if increment_field == "":
                logging.error("ERROR!!! No such increment field in importing sphere: %s", increment_dim)
                logging.error("APPLICATION STOPPED!!!")
                self.current_exception = "ERROR!!! No such increment field in importing sphere: %s" % increment_dim
                if self.jupiter:
                    return self.current_exception
                raise
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval, increment_field=increment_field)
        elif update_params["type"] == "по расписанию":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
        elif update_params["type"] == "интервальное":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": None}
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval)
        else:
            logging.error("ERROR!!! Unknown update type: %s", update_params["type"])
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "ERROR!!! Unknown update type: %s" % update_params["type"]
            if self.jupiter:
                return self.current_exception
            raise
        interval = {"type": interval, "left_border": "", "right_border": "",
                    "dimension_id": "00000000"}
        # финальный запрос для создания мультисферы, обновление мультисферы
        return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                            cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                            schedule=schedule, interval=interval)

    def wait_cube_loading(self, cube_name: str) -> str:
        """
        Ожидание загрузки мультисферы
        :param cube_name: (str) название мультисферы
        :return: информация из лога о создании мультисферы
        """
        # id куба
        self.cube_id = self.get_cube_without_creating_module(cube_name)

        # время старта загрузки мультисферы
        start = time.time()

        # Скачать лог мультисферы
        file_url = self.url + "/" + "resources/log?cube_id=" + self.cube_id
        # имя cookies: session (для скачивания файла)
        cookies = {'session': self.session_id}
        # выкачать файл GET-запросом
        r = requests.get(file_url, cookies=cookies)
        # override encoding by real educated guess as provided by chardet
        r.encoding = r.apparent_encoding
        # вывести лог мультисферы
        log_content = r.text

        logging.info("Содержание лога:\n")
        logging.info(log_content)
        logging.info("************************************************")
        while "Cube creation completed" not in log_content:
            logging.info("Cube '%s' is not created. Re-checking log file in 5 seconds...", cube_name)
            logging.info("Sphere loading time, sec: %s\n", int(time.time() - start))
            time.sleep(5)
            # выкачать файл GET-запросом
            r = requests.get(file_url, cookies=cookies)
            # override encoding by real educated guess as provided by chardet
            r.encoding = r.apparent_encoding
            # вывести лог мультисферы
            log_content = r.text
        # Сообщение об окончании загрузки файла
        output = log_content.split("\n")
        logging.info(output[-2])
        logging.info(output[-1])

        # Информация о времени создания сферы
        end = time.time()
        exec_time = end - start
        min = int(exec_time // 60)
        sec = int(exec_time % 60)
        logging.info("Время ожидания загрузки мультисферы: {} мин., {} сек".format(min, sec))

        return output

    @timing
    def group_dimensions(self, selected_dims: List) -> Dict:
        """
        Сгруппировать выбранные элементы самой левой размерности (работает, когда все размерности свернуты)
        :param selected_dims: (List) список выбранных значений
        :return: (Dict) view group
        """
        # подготовка данных
        result = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                           num_row=500, num_col=100)
        top_dims = self.h.parse_result(result, "top_dims")
        top_dims_qty = len(top_dims)
        result = self.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                           num_row=1000, num_col=100)
        data = self.h.parse_result(result, "data")

        data = data[1 + top_dims_qty:]  # исключает ячейки с названиями столбцов
        left_dim_values = [lst[0] for lst in data]  # получение самых левых размерностей элементов
        selected_indexes = set()
        for elem in left_dim_values:
            if elem in selected_dims:
                left_dim_values.index(elem)
                selected_indexes.add(left_dim_values.index(elem))  # только первые вхождения левых размерностей

        # отметить размерности из списка selected_dims
        sorted_indexes = sorted(selected_indexes)  # отстортировать первые вхождения левых размерностей
        for i in sorted_indexes:
            self.execute_olap_command(command_name="view", state="select", position=1, line=i, level=0)

        # сгруппировать выбранные размерности
        view_line = sorted_indexes[0]
        result = self.execute_olap_command(command_name="view", state="group", position=1, line=view_line, level=0)
        # обновить total_row
        self.update_total_row()
        return result

    @timing
    def group_measures(self, measures_list: List, group_name: str) -> Dict:
        """
        Группировка фактов в (левой) панели фактов
        :param measures_list: (List) список выбранных значений
        :param group_name: (str) новое название созданной группы
        :return: (Dict) command_name="fact", state="create_group", name=group_name
        """
        for measure in measures_list:
            # выделить факты
            measure_id = self.get_measure_id(measure)
            self.execute_olap_command(command_name="fact", state="set_selection", fact=measure_id, is_seleceted=True)

        # сгруппировать выбранные факты
        return self.execute_olap_command(command_name="fact", state="create_group", name=group_name)

    @timing
    def close_layer(self, layer_id: str) -> Dict:
        """
        Закрыть слой
        :param layer_id: ID активного слоя (self.active_layer_id)
        :return: (Dict) command="user_layer", state="close_layer
        """
        # cформировать список из всех неактивных слоев
        active_layer_set = set()
        active_layer_set.add(layer_id)
        unactive_layers_list = set(self.layers_list) - active_layer_set

        # если активный слой - единственный в списке слоев
        # создать и активировать новый слой
        if len(unactive_layers_list) == 0:
            result = self.execute_manager_command(command_name="user_layer", state="create_layer")
            other_layer = self.h.parse_result(result=result, key="layer", nested_key="uuid")
            if self.jupiter:
                if "ERROR" in str(other_layer):
                    return other_layer
            self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=other_layer)
            unactive_layers_list.add(other_layer)

        # активировать первый неактивный слой
        other_layer = next(iter(unactive_layers_list))
        self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=other_layer)

        # закрыть слой
        result = self.execute_manager_command(command_name="user_layer", state="close_layer", layer_id=layer_id)

        # удалить из переменных класса закрытый слой
        self.active_layer_id = ""
        self.layers_list.remove(layer_id)

        return result

    @timing
    def move_up_dims_to_left(self) -> [List, str]:
        """
        Переместить верхние размерности влево. После чего развернуть их
        :return: (List) преобразованный список id левых размерностей
        """
        self.get_multisphere_data()

        # выгрузить данные только из первой строчки мультисферы
        result = self.execute_olap_command(command_name="view",
                                           state="get",
                                           from_row=0,
                                           from_col=0,
                                           num_row=1,
                                           num_col=1)

        left_dims = self.h.parse_result(result=result, key="left_dims")
        if self.jupiter:
            if "ERROR" in str(left_dims):
                return left_dims
        top_dims = self.h.parse_result(result=result, key="top_dims")
        if self.jupiter:
            if "ERROR" in str(top_dims):
                return top_dims

        logging.info("left_dims:")
        logging.info(left_dims)
        logging.info("top_dims:")
        logging.info(top_dims)

        # если в мультисфере есть хотя бы одна верхняя размерность
        if len(top_dims) > 0:
            # вынести размерности влево, начиная с последней размерности списка
            for i in top_dims[::-1]:
                dim_name = self.get_dim_name(dim_id=i)
                self.move_dimension(dim_name=dim_name, position="left", level=0)

            commands = []
            for i in range(0, len(top_dims)):
                command = self.olap_command.collect_command(module="olap",
                                                            command_name="view",
                                                            state="fold_all_at_level",
                                                            level=i)
                if self.jupiter:
                    if "EXCEPTION" in str(command):
                        return command
                commands.append(command)
            # если в мультисфере нет ни одной левой размерности
            # удалить последнюю команду fold_all_at_level, т.к. ее нельзя развернуть
            if len(left_dims) == 0:
                del commands[-1]
            # если список команд fold_all_at_level не пуст
            # выполнить запрос command_name="view" state="fold_all_at_level",
            if len(commands) > 0:
                query = self.olap_command.collect_request(*commands)
                try:
                    self.exec_request.execute_request(query)
                except BaseException as e:
                    logging.exception(e)
                    logging.exception("APPLICATION STOPPED")
                    self.current_exception = str(e)
                    if self.jupiter:
                        return self.current_exception
                    raise
            output = top_dims[::-1] + left_dims
            self.update_total_row()
            return output
        return "No dimensions to move left"

    @timing
    def grant_permissions(self, user_name: str, clone_user: Union[str, bool] = False) -> [Dict, str]:
        """
        Предоставить пользователю Роли и Права доступа.
        Если не указывать параметр clone_user, то пользователю будут выставлены ВСЕ роли и права

        :param user_name: (str) имя пользователя
        :param clone_user: (str) имя пользователя, у которого будут скопированы Роли и Права доступа
        :return: (Dict) command_name="user", state="info" + command_name="user_cube", state="change_user_permissions"
        """
        # get user data
        result = self.execute_manager_command(command_name="user", state="list_request")

        users_data = self.h.parse_result(result=result, key="users")
        if self.jupiter:
            if "ERROR" in str(users_data):
                return users_data
        # user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == user_name}
        # склонировать права пользователя
        if clone_user:
            clone_user_permissions = {k: v for data in users_data for k, v in data.items() if
                                      data["login"] == clone_user}
            user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == user_name}
            requested_uuid = clone_user_permissions["uuid"]
            clone_user_permissions["login"], clone_user_permissions["uuid"] = user_permissions["login"], \
                                                                              user_permissions["uuid"]
            user_permissions = clone_user_permissions
        # или предоставить все права
        else:
            user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == user_name}
            user_permissions["roles"] = ALL_PERMISSIONS
            requested_uuid = user_permissions["uuid"]
        # cubes permissions for user
        result = self.execute_manager_command(command_name="user_cube", state="user_permissions_request",
                                              user_id=requested_uuid)

        cube_permissions = self.h.parse_result(result=result, key="permissions")
        if self.jupiter:
            if "ERROR" in str(cube_permissions):
                return cube_permissions

        # для всех кубов проставить "accessible": True (если проставляете все права),
        # 'dimensions_denied': [], 'facts_denied': []
        if clone_user:
            cube_permissions = [dict(item, **{'dimensions_denied': [], 'facts_denied': []}) for item
                                in cube_permissions]
        else:
            cube_permissions = [dict(item, **{'dimensions_denied': [], 'facts_denied': [], "accessible": True}) for item
                                in cube_permissions]
        # для всех кубов удалить cube_name
        for cube in cube_permissions:
            del cube["cube_name"]

        # предоставить пользователю Роли и Права доступа
        command1 = self.manager_command.collect_command("manager", command_name="user", state="info",
                                                        user=user_permissions)
        command2 = self.manager_command.collect_command("manager", command_name="user_cube",
                                                        state="change_user_permissions",
                                                        user_id=user_permissions["uuid"],
                                                        permissions_set=cube_permissions)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.manager_command.collect_request(command1, command2)
        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise
        return result

    @timing
    def select_all_dims(self) -> [Dict, str]:
        """
        Выделение всех элементов крайней левой размерности
        :return: (Dict) command_name="view", state="sel_all"
        """
        # получение спмска элементов левой размерности (чтобы проверить, что список не пуст)
        result = self.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0, num_row=1,
                                           num_col=1)
        left_dims = self.h.parse_result(result, "left_dims")
        if self.jupiter:
            if "ERROR" in str(left_dims):
                return left_dims

        # проверки
        try:
            error_handler.checks(self, self.func_name, left_dims)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # выделить все элементы левой размерности
        return self.execute_olap_command(command_name="view", state="sel_all", position=1, line=1, level=0)

    @timing
    def load_sphere_chunk(self, units: int = 100):
        """
        Подгрузка мультисферы постранично, порциями строк.
        :param units: количество подгружаемых строк, будет использоваться в num_row и num_col
        :return: (Dict) command_name="view", state="get_2"
        """
        start = 0
        while self.total_row > 0:
            self.total_row = self.total_row - units
            result = self.sc.execute_olap_command(
                command_name="view",
                state="get_2",
                from_row=start,
                from_col=0,
                num_row=units + 1,
                num_col=self.total_cols
            )
            rows_data = self.h.parse_result(result=result, key="data")

            # if self.measure_duplicated or self.dim_duplicated is True
            # add dim1 or fact1 to dim/fact name
            if self.measure_duplicated or self.dim_duplicated:
                rows_data[0] = self.columns

            for item in rows_data[1:]:
                yield dict(zip(rows_data[0], item))
            start += units
        return

    @timing
    def logout(self) -> Dict:
        """
        Выйти из системы
        :return: command_name="user", state="logout"
        """
        return self.execute_manager_command(command_name="user", state="logout")

    def execute_olap_command(self, command_name: str, state: str, **kwargs) -> [Dict, str]:
        """
        Выполнить любую команду модуля OLAP

        Пример: self.execute_olap_command(command_name="fact", state="list_rq")

        Руководство по API http://docs.polymatica.ru/pages/viewpage.action?pageId=411208003

        :param command_name: (str) название команды
        :param state: (str) название состояния
        :param kwargs: доп. параметры в формате param=value
        :return: (Dict) ответ выполненного запроса
        """
        try:
            # проверки
            error_handler.checks(self, self.execute_olap_command.__name__)

            logging.info("*" * 60)
            logging.info("STARTING OLAP COMMAND! command_name='%s' state='%s'", command_name, state)
            logging.info("*" * 60)

            command1 = self.olap_command.collect_command("olap", command_name, state, **kwargs)
            if self.jupiter:
                if "EXCEPTION" in str(command1):
                    return command1
            query = self.olap_command.collect_request(command1)

            # executing query and profiling
            start = time.time()

            result = self.exec_request.execute_request(query)

            end = time.time()
            func_time = end - start
            logging.info("RESPONSE TIME, sec: %s", round(func_time, 2))
            return result

        except BaseException as e:
            logging.exception("EXCEPTION!!! %s" % e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

    def execute_manager_command(self, command_name: str, state: str, **kwargs) -> [Dict, str]:
        """
        Выполнить любую команду модуля Manager.

        Пример: self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        Руководство по API http://docs.polymatica.ru/pages/viewpage.action?pageId=411208003

        :param command_name: (str) название команды
        :param state: (str) название состояния
        :param kwargs: доп. параметры в формате param=value
        :return: (Dict) ответ выполненного запроса
        """
        try:
            logging.info("*" * 60)
            if state == "logout":
                logging.info("LOGGING OUT...")
            logging.info("STARTING MANAGER COMMAND! command_name='%s' state='%s'", command_name, state)
            logging.info("*" * 60)
            command1 = self.manager_command.collect_command("manager", command_name, state, **kwargs)
            if self.jupiter:
                if "EXCEPTION" in str(command1):
                    return command1
            query = self.manager_command.collect_request(command1)

            # executing query and profiling
            start = time.time()

            result = self.exec_request.execute_request(query)

            end = time.time()
            func_time = end - start
            logging.info("RESPONSE TIME, sec: %s", round(func_time, 2))
            if state == "logout":
                logging.info(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")

            # fix issue with UnicodeEncodeError for admin get_user_list
            if command_name == "admin" and state == "get_user_list":
                return str(result).encode("utf-8")

            return result
        except BaseException as e:
            logging.exception("EXCEPTION!!! %s" % e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

    @timing
    def close_current_cube(self) -> Dict:
        """
        Закрыть текущую мультисферу
        :return: (Dict) command_name="user_iface", state="close_module"
        """
        current_module_id = self.multisphere_module_id
        self.multisphere_module_id = ""
        return self.execute_manager_command(command_name="user_iface", state="close_module",
                                            module_id=current_module_id)

    @timing
    def rename_group(self, group_name: str, new_name: str) -> [Dict, str]:
        """
        Переименовать группу пользователей
        :param group_name: (str) Название группы
        :param new_name: (str) Новое название группы
        :return: (Dict) command_name="group", state="edit_group"
        """
        # all groups data
        result = self.execute_manager_command(command_name="group",
                                              state="list_request")
        groups = self.h.parse_result(result, "groups")
        if self.jupiter:
            if "ERROR" in str(groups):
                return groups

        # empty group_data
        roles = ""
        group_uuid = ""
        group_members = ""
        description = ""

        # search for group_name
        for i in groups:
            # if group exists: saving group_data
            if i["name"] == group_name:
                roles = i["roles"]
                group_uuid = i["uuid"]
                group_members = i["members"]
                description = i["description"]
                break

        # check is group exist
        try:
            error_handler.checks(self, self.func_name, group_uuid, group_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # group_data for request
        group_data = {}
        group_data.update({"uuid": group_uuid})
        group_data.update({"name": new_name})
        group_data.update({"description": description})
        group_data.update({"members": group_members})
        group_data.update({"roles": roles})

        return self.execute_manager_command(command_name="group",
                                            state="edit_group",
                                            group=group_data)

    def create_multisphere_module(self, num_row: int = 10000, num_col: int = 100) -> [Dict, str]:
        """
        Создать модуль мультисферы
        :param self: экземпляр класса BusinessLogic
        :param num_row: количество отображаемых строк
        :param num_col: количество отображаемых колонок
        :return: self.multisphere_data
        """
        # Получить список слоев сессии
        logging.info("Getting layers list:")
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")

        # список слоев
        session_layers_lst = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers_lst):
                return session_layers_lst

        self.layers_list = []

        for i in session_layers_lst:
            self.layers_list.append(i["uuid"])

        try:
            # получить layer id
            self.active_layer_id = session_layers_lst[0]["uuid"]
        except KeyError as e:
            logging.exception("EXCEPTION!!! ERROR while parsing response: %s\n%s", e, traceback.format_exc())
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise
        except IndexError as e:
            logging.exception("EXCEPTION!!! ERROR while parsing response: %s\n%s", e, traceback.format_exc())
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        logging.info("layer_id: %s", self.active_layer_id)

        # Инициализировать слой
        logging.info("init layer %s...", self.active_layer_id)
        self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=self.active_layer_id)

        # Дождаться загрузки слоя
        result = self.execute_manager_command(command_name="user_layer", state="get_load_progress",
                                              layer_id=self.active_layer_id)

        progress = self.h.parse_result(result=result, key="progress")
        if self.jupiter:
            if "ERROR" in str(progress):
                return progress

        logging.info("Layer load progress...")
        logging.info("%s percent", progress)
        while progress < 100:
            result = self.execute_manager_command(command_name="user_layer", state="get_load_progress",
                                                  layer_id=self.active_layer_id)

            progress = self.h.parse_result(result=result, key="progress")
            if self.jupiter:
                if "ERROR" in str(progress):
                    return progress

            logging.info("%s percent", progress)

        # cоздать модуль мультисферы из <cube_id> на слое <layer_id>:
        result = self.execute_manager_command(command_name="user_cube",
                                              state="open_request",
                                              layer_id=self.active_layer_id,
                                              cube_id=self.cube_id,
                                              module_id="00000000-00000000-00000000-00000000")

        # получение id модуля мультисферы
        self.multisphere_module_id = self.h.parse_result(result=result, key="module_desc", nested_key="uuid")
        if self.jupiter:
            if "ERROR" in str(self.multisphere_module_id):
                return self.multisphere_module_id

        # инициализация модуля Olap
        self.olap_command = olap_commands.OlapCommands(self.session_id, self.multisphere_module_id,
                                                       self.url, self.server_codes)
        # рабочая область прямоугольника
        view_params = {
            "from_row": 0,
            "from_col": 0,
            "num_row": num_row,
            "num_col": num_col
        }
        # получить список размерностей и фактов, а также текущее состояние таблицы со значениями
        # (рабочая область модуля мультисферы)
        query = self.olap_command.multisphere_data(self.multisphere_module_id, view_params)
        if self.jupiter:
            if "EXCEPTION" in str(query):
                return query
        try:
            result = self.exec_request.execute_request(query)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # multisphere data
        self.multisphere_data = {"dimensions": "", "facts": "", "data": ""}
        for item, index in [("dimensions", 0), ("facts", 1), ("data", 2)]:
            self.multisphere_data[item] = result["queries"][index]["command"][item]
        logging.info("Multisphere data successfully received: %s", self.multisphere_data)

        return self.multisphere_data

    @timing
    def rename_grouped_elems(self, name: str, new_name: str) -> [Dict, str]:
        """
        Переименовать сгруппированные элементы левой размерности
        :param name: название группы элементов
        :param new_name: новое название группы элементов
        :return: (Dict) command_name="group", state="set_name"
        """
        group_id = ""

        res = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                        num_row=1000, num_col=1000)

        # взять id самой левой размерности
        left_dims = self.h.parse_result(res, "left_dims")
        if not len(left_dims):
            logging.error("No left dims!")
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "No left dims!"
            if self.jupiter:
                return self.current_exception
            raise
        left_dim_id = left_dims[0]

        # элементы левой размерности
        left_dim_elems = self.h.parse_result(res, "left")
        # вытащить group_id элемента размерности (если он есть у этого элемента)
        try:
            for elem in left_dim_elems:
                if "value" in elem[0]:
                    if elem[0]["value"] == name:
                        group_id = elem[0]["group_id"]
        except KeyError:
            logging.error("grouped elems has NO group_id: %s", name)
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "grouped elems has NO group_id: %s", name
            if self.jupiter:
                return self.current_exception
            raise

        if not group_id:
            logging.error("For the left dim: NO such elem: %s", name)
            logging.error("APPLICATION STOPPED!!!")
            self.current_exception = "For the left dim NO such elem: %s" % name
            if self.jupiter:
                return self.current_exception
            raise

        return self.execute_olap_command(command_name="group", state="set_name", dim_id=left_dim_id, group_id=group_id,
                                         name=new_name)

    @timing
    def get_cubes_for_scenarios_by_userid(self, user_name) -> List:
        """
        Для заданного пользователя получить список с данными о сценариях и используемых в этих сценариях мультисферах:

        [{"uuid": "b8ffd729",
          "name": "savinov_test",
          "description": "",
          "cube_ids": ["79ca1aa5", "9ce3ba59"],
          "cube_names": ["nvdia", "Роструд_БФТ_F_Measures_"]},
         ...
         ]
        :param user_name: имя пользователя, под которым запускается command_name="script", state="list_cubes_request"
        :return: (List) scripts_data
        """
        # авторизоваться поль пользователем user_name
        sc = BusinessLogic(login=user_name, url=self.url)

        scripts_data = []

        # script_descs
        script_lst = sc.execute_manager_command(command_name="script", state="list")
        script_descs = sc.h.parse_result(script_lst, "script_descs")

        # cubes data
        cubes = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_data = sc.h.parse_result(cubes, "cubes")

        for script in script_descs:
            # getting list of cube_ids for this scenario id
            res = sc.execute_manager_command(command_name="script", state="list_cubes_request",
                                             script_id=script["uuid"])
            cube_ids = sc.h.parse_result(res, "cube_ids")

            # saving cubes names in list
            cube_names = []
            for cube in cubes_data:
                for cube_id in cube_ids:
                    if cube_id == cube["uuid"]:
                        cube_name = cube["name"].rstrip()
                        cube_names.append(cube_name)

            # saving data for this scenario
            script_data = {
                "uuid": script["uuid"],
                "name": script["name"],
                "description": script["description"],
                "cube_ids": cube_ids,
                "cube_names": cube_names
            }
            scripts_data.append(script_data)

        # убить сессию пользователя user_name
        sc.logout()

        return scripts_data

    @timing
    def get_cubes_for_scenarios(self) -> List:
        """
        Получить список с данными о сценариях и используемых в этих сценариях мультисферах:

        [{"uuid": "b8ffd729",
          "name": "savinov_test",
          "description": "",
          "cube_ids": ["79ca1aa5", "9ce3ba59"],
          "cube_names": ["nvdia", "Роструд_БФТ_F_Measures_"]},
         ...
         ]
        :return: (List) scripts_data
        """
        scripts_data = []

        # script_descs
        script_lst = self.execute_manager_command(command_name="script", state="list")
        script_descs = self.h.parse_result(script_lst, "script_descs")

        # cubes data
        cubes = self.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_data = self.h.parse_result(cubes, "cubes")

        for script in script_descs:
            # getting list of cube_ids for this scenario id
            res = self.execute_manager_command(command_name="script", state="list_cubes_request",
                                               script_id=script["uuid"])
            cube_ids = self.h.parse_result(res, "cube_ids")

            # saving cubes names in list
            cube_names = []
            for cube in cubes_data:
                for cube_id in cube_ids:
                    if cube_id == cube["uuid"]:
                        cube_name = cube["name"].rstrip()
                        cube_names.append(cube_name)

            # saving data for this scenario
            script_data = {
                "uuid": script["uuid"],
                "name": script["name"],
                "description": script["description"],
                "cube_ids": cube_ids,
                "cube_names": cube_names
            }
            scripts_data.append(script_data)

        return scripts_data

    @timing
    def polymatica_health_check_user_sessions(self) -> int:
        """
        Подсчет активных пользовательских сессий [ID-3040]
        :return: (int) user_sessions
        """
        res = self.execute_manager_command(command_name="admin", state="get_user_list")

        # преобразовать полученную строку к utf-8
        res = res.decode("utf-8")

        # преобразовать строку к словарю
        res = ast.literal_eval(res)

        users_info = self.h.parse_result(res, "users")

        user_sessions = 0
        for user in users_info:
            if user["is_online"]:
                user_sessions += 1

        return user_sessions

    @timing
    def polymatica_health_check_all_multisphere_updates(self) -> Dict:
        """
        [ID-3010] Проверка ошибок обновления мультисфер (для целей мониторинга):
        0, если ошибок обновления данных указанной мультисферы не обнаружено
        1, если последнее обновление указанной мультисферы завершилось с ошибкой, но мультисфера доступна пользователям для работы
        2, если последнее обновление указанной мультисферы завершилось с ошибкой и она не доступна пользователям для работы
        OTHER - другие значения update_error и available
        :return: (Dict) multisphere_upds
        """

        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # словарь со статусами обновлений мультисфер
        multisphere_upds = {}

        for cube in cubes_list:
            if cube["update_error"] and not cube["available"]:
                multisphere_upds.update({cube["name"]: 2})
                continue
            elif cube["update_error"] and cube["available"]:
                multisphere_upds.update({cube["name"]: 1})
                continue
            elif not cube["update_error"] and cube["available"]:
                multisphere_upds.update({cube["name"]: 0})
                continue
            else:
                multisphere_upds.update({cube["name"]: "OTHER"})

        return multisphere_upds

    @timing
    def polymatica_health_check_multisphere_updates(self, ms_name: str) -> [int, str]:
        """
        [ID-3010] Проверка ошибок обновления мультисферы (для целей мониторинга):
        0, не обнаружено ошибок обновления данных указанной мультисферы и мультисфера доступна.
            (Проверка, что "update_error"=False и "available"=True)
        1, ошибок обновления данных указанной мультисферы
            (Проверка, что "update_error"=True или "available"=False)
        :param ms_name: (str) Название мультисферы
        :return: (int) 0 или 1
        """
        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # Проверка названия мультисферы
        try:
            error_handler.checks(self, self.func_name, cubes_list, ms_name)
        except BaseException as e:
            logging.exception(e)
            logging.exception("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        for cube in cubes_list:
            if cube["name"] == ms_name:
                if cube["update_error"] or not cube["available"]:
                    return 1
                break

        return 0

    @timing
    def polymatica_health_check_data_updates(self) -> [List, int]:
        """
        [ID-3010] Один из методов проверки обновления мультисфер (для целей мониторинга)
        :return: (int, List) 0, если ошибок обновления данных не обнаружено (последнее обновление для всех мультисфер выполнено успешно, без ошибок)
            Перечень мультисфер, последнее обновление которых завершилось с ошибкой
        """
        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # словарь со статусами обновлений мультисфер
        multisphere_upds = []

        for cube in cubes_list:
            if cube["update_error"]:
                multisphere_upds.append(cube["name"])

        if not multisphere_upds:
            return 0

        return multisphere_upds


class GetDataChunk:
    """ Класс для получения данных чанками """

    def __init__(self, sc: BusinessLogic):
        """
        Инициализация класса GetDataChunk
        :param sc: экземпляр класса BusinessLogic
        """
        logging.info("INIT CLASS GetDataChunk")
        self.jupiter = sc.jupiter

        # helper class
        self.h = helper.Helper(self)

        # экзмепляр класса BusinessLogic
        self.sc = sc
        # флаги наличия дубликатов размерностей и фактов
        self.measure_duplicated, self.dim_duplicated = False, False

        result = sc.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                         num_row=1, num_col=1)
        json_left_dims = self.h.parse_result(result, "left_dims")

        # количество левых размерностей
        self.dims_qty = len(json_left_dims)
        # список размерностей
        self.dim_lst = []
        # количество фактов в строке
        self.facts_qty = 0
        # getting multisphere total rows
        result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                              num_row=1, num_col=1)
        self.total_row = self.h.parse_result(result, "total_row")
        # словарь типов размерностей Полиматики
        self.olap_types = self.sc.server_codes["olap"]["olap_data_type"]
        # колонки в формате {"название размерности": str, "название факта": float}
        self.columns = self.get_col_types()

        # total number of cols
        # self.total_cols = len(self.columns)
        self.total_cols = self.dims_qty + self.facts_qty

    def get_col_types(self) -> Dict:
        """
        Получить колонки в формате {"название размерности": str, "название факта": float}
        :return: (dict) {"название размерности": str, "название факта": float}
        """

        # {"название размерности": str, "название факта": float}
        columns = {}

        # сохранить данные по всем колонкам
        columns_data = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                                    num_row=10, num_col=1000)

        # содержимое data (размерности, факты), первая строка с данными
        data = self.h.parse_result(columns_data, "data")
        data = data[1]

        # command="get" (necessary fields: left_dims, top)
        get_command = self.sc.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                                   num_row=10, num_col=1000)

        # ---------------------------------------- размерности ----------------------------------------
        # размерности вынесенные влево
        left_dims = self.h.parse_result(get_command, "left_dims")

        # данные о размерностях (чтобы извлечь названия размерностей)
        result = self.sc.execute_olap_command(command_name="dimension", state="list_rq")

        all_dims = self.h.parse_result(result, "dimensions")

        dims_dups = {}  # размерности-дубликаты
        # добавление размерностей в словарь колонок
        for my_dim in left_dims:
            for dim in all_dims:
                if my_dim == dim["id"]:
                    dim_olap_type = dim["olap_type"]
                    dim_olap_type = list(self.olap_types.keys())[
                        list(self.olap_types.values()).index(dim_olap_type)]
                    dim_name = dim["name"]
                    if dim_name in columns:
                        if dim_name not in dims_dups:
                            dims_dups.update({dim_name: 1})
                        else:
                            dims_dups[dim_name] += 1
                        dim_name = dim_name + " (dim%s)" % dims_dups[dim_name]
                        self.dim_duplicated = True
                    dim_type_data = {
                        "type": dim_olap_type,
                        "data_type": "dimension"
                    }
                    columns.update({dim_name: dim_type_data})
                    self.dim_lst.append(dim["name"])

        # ---------------------------------------- факты ----------------------------------------
        # extract facts from columns (only facts in columns! Some facts can be hidden)
        top = self.h.parse_result(get_command, "top")
        fact_data = ""
        for i in top:
            if "fact_id" in str(i):
                fact_data = i
                break

        col_fact = []

        # save values in col_fact
        for fact in fact_data:
            col_fact.append(fact["fact_id"])

        facts_dups = {}  # факты-дубликаты
        for fact in col_fact:
            fact_name = self.sc.get_measure_name(fact)
            if fact_name in columns:
                if fact_name not in facts_dups:
                    facts_dups.update({fact_name: 1})
                else:
                    facts_dups[fact_name] += 1
                fact_name = fact_name + " (fact%s)" % facts_dups[fact_name]
                self.measure_duplicated = True
            delta = len(columns) - self.dims_qty

            # gets actual measure fact from the first row:
            elem = data[self.dims_qty + delta]
            if isinstance(elem, float):
                fact_type_data = {
                    "type": "double",
                    "data_type": "fact"
                }
            else:
                fact_type_data = {
                    "type": "uint32",
                    "data_type": "fact"
                }

            columns.update({fact_name: fact_type_data})
            self.facts_qty += 1

        return columns

    def load_sphere_chunk(self, units: int = 100):
        """
        Подгрузка мультисферы постранично, порциями строк.
        :param units: количество подгружаемых строк, будет использоваться в num_row и num_col
        :return: (Dict) command_name="view", state="get_2"
        """
        start = 0
        while self.total_row > 0:
            self.total_row = self.total_row - units
            result = self.sc.execute_olap_command(
                command_name="view",
                state="get_2",
                from_row=start,
                from_col=0,
                num_row=units + 1,
                num_col=self.total_cols
            )
            rows_data = self.h.parse_result(result=result, key="data")

            # if self.measure_duplicated or self.dim_duplicated is True
            # add dim1 or fact1 to dim/fact name
            if self.measure_duplicated or self.dim_duplicated:
                rows_data[0] = self.columns

            for item in rows_data[1:]:
                yield dict(zip(rows_data[0], item))
            start += units
        return
