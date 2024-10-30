import pandas as pd
import numpy as np
import math
import os
from pathlib import Path

INDEX_OF_APPROVMENT = {
    '1': 0,
    '2': 0,
    '3': 0.58,
    '4': 0.9
}


class CR_MX:

    def __init__(self, names: list):
        """
        инициализация класса
        :param names: имена для столбцов и колонок (требуется убрать)
        """
        self.__rw_nm = names
        self.__cl_nm = names

    def get_rw_nm(self):
        return self.__rw_nm

    def get_cl_nm(self):
        return self.__cl_nm

    # Создание пустого представления данных в табличном виде
    def cr_pd_df(self) -> None:
        self._df = pd.DataFrame(data=None, columns=self.__cl_nm, index=self.__rw_nm)

    def view_df(self):
        return self._df


# Основной класс для работы с заполненными табличными данными
class FLL_MX(CR_MX):

    def __init__(self, names: list, data: list) -> None:
        super().__init__(names)
        self.__data = data
        self._names = names

    def cr_pd_df(self) -> None:
        self._df = pd.DataFrame(data=self.__data, columns=self.get_cl_nm(), index=self.get_rw_nm())

    # Забирает таблицы из excel в формате:
    """
                  комфорт  престижность  внешний вид  плавность
комфорт       1.000000             5     3.000000        0.5
престижность  0.200000             1     0.333333        0.2
внешний вид   0.333333             3     1.000000        0.2
плавность     2.000000             5     5.000000        1.0

    """

    def excl_pd_df(self, xlsx_name) -> None:
        self._df = None
        self._df = pd.read_excel(xlsx_name, index_col=0, header=0)

    # Среднее геометрическое по строкам
    def mid_str(self):
        np_data = self.view_df().to_numpy()
        len_str = len(np_data)

        # Возвращает произведение чисел каждой строки в степени 1/n
        return np.prod(np_data, axis=1) ** (1 / len_str)

    # Нахождение вектора собственных чисел
    def self_vector(self):
        # print('self vector')
        # print(f'{sum(self.mid_str())} aye')
        # Вызываем функцию среднего геометрического и делим на сумму всех средних геометрических
        return self.mid_str() / sum(self.mid_str())

    def self_max(self):
        # np_data = np.array(self.__data)
        np_data = self.view_df().to_numpy()

        # Находим максимальное собственное
        return sum(np.sum(np_data, axis=0) * self.self_vector())

    def index_of_approvment(self):
        # TODO ci по формуле (исправить момент с self.__data)
        ci = (self.self_max() - len(self.__data)) / (len(self.__data) - 1)
        # cci по формуле, шкала с первыми индексами задана в начале программы
        cci = ci / INDEX_OF_APPROVMENT[f'{len(self.__data)}']

        return cci

    # Представление через встроенные пакеты
    # Math part, regular functions
    def harmony(self):
        """
        рассчитываем собственные значения и критерий согласования
        :return:
        """
        values_ = self.view_df()[self._names].to_numpy()
        values_ = np.asmatrix(values_)
        n = len(values_)
        eigh = np.linalg.eigvals(values_)
        print(eigh)
        A = abs(eigh).max()
        c = (A - n) / (n - 1)

        return c

    def result(self):
        S = 0

        values_ = self.view_df()[self._names].to_numpy()
        values_ = np.asmatrix(values_)
        print(values_)
        n1 = len(values_)
        SE = np.zeros(n1)
        for n in range(n1):
            s = 0

            for k in range(n1):
                s = s + (values_[n, k])
            S = S + s
            SE[n] = s
            SE = SE / S
        return SE


if __name__ == '__main__':

    p = Path("SAATI")
    names = []
    for x in p.rglob("*"):
        # print(x)
        names.append(str(x))
    # print(names)
    onexone = FLL_MX(names=None, data=None)
    onexone.excl_pd_df(names[0])

    # рудимент
    objects = [0 for _ in range(len(names))]

    # Создаем пустой словарь, для создания пары ключ - значение. Ключ - признак/название файла, значение - объект класса
    # где объект класса - Pandas DataFrame (табличное представление)
    objects_d = {}

    # Создаем табличное представление из файлов excel
    for i in range(0, len(names)):
        objects_d[names[i]] = FLL_MX(names=None, data=None)
        objects_d[names[i]].excl_pd_df(names[i])

    # Веса у оценки характеристик
    self_vectors = objects_d[names[0]].self_vector()

    print('Матрица оцененая по шкале относительной важности (Оценка критериев):')
    print(objects_d[names[0]].view_df())
    print('Собственный вектор: ')
    print(objects_d[names[0]].self_vector())
    print(f'{'-' * 70}')
    print('Матрица оцененая по шкале относительной важности (Комфорт):')
    print(objects_d[names[1]].view_df())
    print('Собственный вектор: ')
    print(objects_d[names[1]].self_vector())
    print(f'{'-' * 70}')
    print('Матрица оцененая по шкале относительной важности (Престижность):')
    print(objects_d[names[2]].view_df())
    print('Собственный вектор: ')
    print(objects_d[names[2]].self_vector())
    print(f'{'-' * 70}')
    print('Матрица оцененая по шкале относительной важности (Внешний вид):')
    print(objects_d[names[3]].view_df())
    print('Собственный вектор: ')
    print(objects_d[names[3]].self_vector())
    print(f'{'-' * 70}')
    print('Матрица оцененая по шкале относительной важности (Плавность хода):')
    print(objects_d[names[4]].view_df())
    print('Собственный вектор: ')
    print(objects_d[names[4]].self_vector())
    print(f'{'-' * 70}')
    print('Обобщённая оценка вариантов относительно показателей')

    result = (self_vectors[0] * objects_d[names[1]].self_vector() + self_vectors[1] * objects_d[names[2]].self_vector()
              + self_vectors[2] * objects_d[names[3]].self_vector() + self_vectors[3] * objects_d[
                  names[4]].self_vector())
    print(result)

    result_arr = []
    # for name in names:




