# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Часто используемые служебные функции """
from typing import List, Dict, Tuple
from itertools import count
import traceback
import logging
import time


class Helper:
    def __init__(self, sc):
        """
        Инициализация класса GetDataChunk
        :param sc: экземпляр класса BusinessLogic
        """
        # экзмепляр класса BusinessLogic
        self.sc = sc
        self.jupiter = sc.jupiter

    def get_cube_id(self, cubes_list: List, cube_name: str) -> [str, bool]:
        """
        Получить id мультисферы
        :param cubes_list: список мультисфер
        :param cube_name: название мультисферы
        :return: id мультисферы
        """
        for cube in cubes_list:
            if cube["name"] == cube_name:
                return cube["uuid"]
        raise ValueError("No such cube in cubes list: %s\n%s" % (cube_name, traceback.format_exc()))

    def get_measure_or_dim_id(self, multisphere_data: Dict, measure_dim: str, name) -> [str, bool]:
        """
        Получить id факта или размерности
        :param multisphere_data: рабочая область мультисферы
        :param measure_dim: "facts" / "dimensions"
        :param name: название размерности / факта
        :return: id размерности / факта
        """
        for item in multisphere_data[measure_dim]:
            if item["name"].rstrip() == name.rstrip():
                return item["id"]
        logging.error("No such %s: %s\n%s", measure_dim[:-1], name, traceback.format_exc())
        logging.error("APPLICATION STOPPED!!!")
        if self.jupiter:
            return "ERROR!!! No such %s: %s\n%s" % (measure_dim[:-1], name, traceback.format_exc())
        raise

    def get_dim_id(self, multisphere_data: Dict, name: str, cube_name: str) -> [str, bool]:
        """
        Получить id размерности
        :param multisphere_data: рабочая область мультисферы
        :param name: название размерности
        :param cube_name: название текущей мультисферы
        :return: id размерности
        """
        for item in multisphere_data["dimensions"]:
            if item["name"].rstrip() == name.rstrip():
                return item["id"]
        logging.error("Dimension name [%s] is not valid for Multisphere [%s]", name, cube_name)
        logging.error("APPLICATION STOPPED!!!")
        if self.jupiter:
            return "ERROR!!! Dimension name [%s] is not valid for Multisphere [%s]" % (name, cube_name)
        raise

    def get_measure_id(self, multisphere_data: Dict, name: str, cube_name: str) -> [str, bool]:
        """
        Получить id факта
        :param multisphere_data: рабочая область мультисферы
        :param name: имя факта
        :param cube_name: название текущей мультисферы
        :return: id факта
        """
        for item in multisphere_data["facts"]:
            if item["name"].rstrip() == name.rstrip():
                return item["id"]
        logging.error("Measure name [%s] is not valid for Multisphere [%s]", name, cube_name)
        logging.error("APPLICATION STOPPED!!!")
        if self.jupiter:
            return "ERROR!!! Measure name [%s] is not valid for Multisphere [%s]" % (name, cube_name)
        raise

    def get_measure_type(self, name: str) -> [bool, int]:
        """
        return Вид факта (value)
        :param name: Вид факта
        :return: Вид факта (id)
        """
        measure_types = {"Значение": 0,
                         "Процент": 1,
                         "Ранг": 2,
                         "Количество уникальных": 3,
                         "Среднее": 4,
                         "Отклонение": 5,
                         "Минимум": 6,
                         "Максимум": 7,
                         "Изменение": 8,
                         "Изменение в %": 9,
                         "Нарастающее": 10,
                         "ABC": 11,
                         "Медиана": 12,
                         "Количество": 13,
                         "UNKNOWN": 14
                         }
        if name not in measure_types:
            logging.error("ERROR!!! No such measure type: %s\n", name, traceback.format_exc())
            logging.error("APPLICATION STOPPED!!!")
            if self.jupiter:
                return "ERROR!!! No such measure type: %s\n" % name
            raise
        return measure_types[name]

    def join_splited_measures(self, formula_lst: List, join_iterations: int):
        """
        если в фактах есть пробелы, склеивает их обратно
        :param formula_lst: (List) формула, разбитая на список (разделитель - пробел)
        :param join_iterations: (int) количество итераций == количеству "[" в формуле
        :return: (List) formula_lst со склееными фактами
        """
        # если кол-во итераций закончилось (факты закончились) - выйти из функции
        if join_iterations == 0:
            return formula_lst
        # кол-во "[" и "]"
        openning_sqr_braket = 0
        closing_sqr_braket = 0

        # если все [факты с пробелами] и так склеены - вернуть formula_lst
        for idx, elem in enumerate(formula_lst):
            openning_sqr_braket += elem.count("[")
            closing_sqr_braket += elem.count("]")
            if openning_sqr_braket != closing_sqr_braket:
                break
            if (openning_sqr_braket == closing_sqr_braket) and (idx == len(formula_lst) - 1):
                return formula_lst

        # здесь будет сохранен [Факт, соединенный обратно по пробелу]
        joined_measure = ""
        # кол-во "[" и "]"
        openning_sqr_braket = 0
        closing_sqr_braket = 0
        # индексы, которые занимает рассплитенный факт в списке:
        measure_indexes = []

        for idx, elem in enumerate(formula_lst):
            # если факт и так не разделен по пробелу
            # и если в формуле есть функции corr, top, total, if - переход к след. итерации
            if ("[" in elem and "]" in elem) and ("corr(" not in joined_measure) and ("top(" not in joined_measure) and \
                    ("total(" not in joined_measure) and ("if(" not in joined_measure):
                continue
            openning_sqr_braket += elem.count("[")
            closing_sqr_braket += elem.count("]")
            # если в рассплитенном списке есть [Факт
            # конкатенировать его с joined_measure
            if openning_sqr_braket > 0:
                joined_measure += elem
                joined_measure += " "
            # если факт в виде [Факт
            # добавить индекс к списку measure_indexes
            if (openning_sqr_braket != 0) and (closing_sqr_braket == 0):
                measure_indexes.append(idx)
            # если элемент == факт, и этот факт в виде [Факт]
            # добавить индекс к списку measure_indexes и выйти из цикла
            if (openning_sqr_braket != 0) and (closing_sqr_braket != 0):
                if openning_sqr_braket == closing_sqr_braket:
                    measure_indexes.append(idx)
                    break

        # удалить рассплитенный факт из formula_lst
        for _ in measure_indexes:
            formula_lst.pop(measure_indexes[0])
        joined_measure = joined_measure.rstrip()

        # добавить в formula_lst [Факт, соединенный обратно по пробелу]
        formula_lst.insert(measure_indexes[0], joined_measure)

        # уменьшить кол-во итераций (кол-во фактов) на 1
        join_iterations -= 1

        # рекурсивно вызвать join_splited_measures()
        return self.join_splited_measures(formula_lst, join_iterations)

    def get_scenario_data(self, scenario_data: Dict, scenario_name: str) -> [str, bool]:
        """
        Получение id сценария по имени сценария
        :param scenario_data: (Dict) данные по всем сценариям, можно получить в модуле Manager, command: "script",
                            state: "list"
        :param scenario_name: (str) название сценария
        :return: id сценария
        """
        script_descs = self.parse_result(result=scenario_data, key="script_descs")

        for i in script_descs:
            if i["name"] == scenario_name:
                return i["uuid"]
        logging.error("ERROR!!! No such scenario name: %s", scenario_name)
        logging.error("APPLICATION STOPPED!!!")
        if self.jupiter:
            return "ERROR!!! No such scenario name: %s" % scenario_name
        raise

    def wait_scenario_layer_loaded(self, sc_layer: str, timeout: int) -> [Tuple, str]:
        """
        Функция ожидает, когда слой с запущенным сценарием загрузится
        :param self: экземпляр класса BusinessLogic
        :param sc_layer: (str) id слоя со сценарием
        :param timeout: (int) таймаут
        :return: (tuple) общее число шагов сценария, число законченных шагов
        """
        start = time.time()
        finished_steps, total_steps = 0, 1
        while finished_steps < total_steps:
            time.sleep(0.5)

            # check for timeout
            end = time.time()
            if (end - start) > timeout:
                try:
                    raise TimeoutError("Timeout while waiting loading scenario layer!")
                except Exception as e:
                    logging.exception("EXCEPTION!!! %s", e)
                    logging.exception("APPLICATION STOPPED")
                    self.sc.current_exception = "EXCEPTION!!! %s" % e
                    if self.jupiter:
                        return self.sc.current_exception
                    raise

            progress = self.sc.execute_manager_command(command_name="script", state="run_progress", layer_id=sc_layer)
            logging.info(progress)

            total_steps = self.parse_result(result=progress, key="total_steps_count")
            finished_steps = self.parse_result(result=progress, key="finished_steps_count")

        return total_steps, finished_steps

    def parse_result(self, result: Dict, key: str, nested_key: str = None):
        """
        Парсит и проверяет на ошибки ответ в виде ['queries'][0]['command']['значение']['['необязательное значение']
        :param result: (Dict) нераспарсенный ответ от API
        :param key: (str) ключ, значение которого нужно распарсить
        :param nested_key: (str) вложенный ключ, значение которого нужно распарсить
        :return: итоговое значение
        """
        request_queries = result.get("queries")
        request_queries = next(iter(request_queries))
        request_command = request_queries.get("command")
        value = request_command.get(key)
        if value is None:
            logging.error("ERROR while parsing response: ['queries'][0]['command']['%s']", key)
            logging.error("APPLICATION STOPPED")
            if self.jupiter:
                return "ERROR while parsing response: ['queries'][0]['command']['%s']" % key
            raise
        if nested_key is not None:
            nested_value = value.get(nested_key)
            if nested_value is None:
                logging.error("ERROR while parsing response: ['queries'][0]['command']['%s']['%s']", key, nested_key)
                logging.error("APPLICATION STOPPED")
                if self.jupiter:
                    return "ERROR while parsing response: ['queries'][0]['command']['%s']['%s']" % (key, nested_key)
                raise
            return nested_value
        return value

    def get_rows_cols(self, num_row: int = None, num_col: int = None) -> Dict:
        """
        Загрузить строки и колонки мультисферы
        :param self: экземпляр класса BusinessLogic
        :param num_row: (int) количество строк мультисферы
        :param num_col: (int) количество колонок мультисферы
        :return: (Dict) command_name="view", state="get_2"
        """

        if (num_row is not None) and (num_col is not None):
            return self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                                num_row=num_row,
                                                num_col=num_col)

        # 1000, 2000, 3000, ...
        gen = count(1000, 1000)

        prev_data = []

        result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                              num_row=next(gen),
                                              num_col=next(gen))
        data = self.parse_result(result=result, key="data")

        while len(prev_data) < len(data):
            prev_data = data
            result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                                  num_row=next(gen), num_col=next(gen))
            data = self.parse_result(result=result, key="data")
        return result

    def get_filter_rows(self, dim_id: str) -> Dict:
        """
        Загрузить строки и колонки мультисферы
        :param self: экземпляр класса BusinessLogic
        :param dim_id: (str) id размерности
        :return: (Dict) command_name="view", state="get_2"
        """

        # 1000, 2000, 3000, ...
        gen = count(1000, 1000)

        prev_data = []

        result = self.sc.execute_olap_command(command_name="filter",
                                              state="pattern_change",
                                              dimension=dim_id,
                                              pattern="",
                                              # кол-во значений отображается на экране, после скролла их становится больше:
                                              # num=30
                                              num=next(gen))

        data = self.parse_result(result=result, key="data")

        while len(prev_data) < len(data):
            prev_data = data
            result = self.sc.execute_olap_command(command_name="filter",
                                                  state="pattern_change",
                                                  dimension=dim_id,
                                                  pattern="",
                                                  # кол-во значений отображается на экране, после скролла их становится больше:
                                                  # num=30
                                                  num=next(gen))
            data = self.parse_result(result=result, key="data")
        return result

    # def get_default_args(func) -> Dict:
    #     """
    #     Получение дефолтных параметров функции
    #     :param func: название функции
    #     :return: (Dict) словарь параметров функции
    #     """
    #     signature = inspect.signature(func)
    #     return {
    #         k: v.default
    #         for k, v in signature.parameters.items()
    #         if v.default is not inspect.Parameter.empty
    #     }
