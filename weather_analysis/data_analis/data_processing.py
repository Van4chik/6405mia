import pandas as pd
import numpy as np
from .utils import cache_decorator

class WeatherDataProcessor:
    """
    Класс WeatherDataProcessor предназначен для обработки временных рядов погодных данных.

    Основные методы:
    - moving_average: Вычисление скользящего среднего для температур.
    - differential: Вычисление первой разности (дифференциала) значений температур.
    - autocorrelation: Вычисление автокорреляции температурного ряда.
    - find_extremes: Определение локальных максимумов и минимумов температур.
    - process_data: Интеграция всех метрик в один DataFrame.

Атрибуты:
        data (pd.DataFrame): Исходный DataFrame с погодными данными.

    Методы:
        process_data() -> pd.DataFrame:
            Обрабатывает данные и возвращает результат.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Инициализирует обработчик данных погоды.

        Параметры:
        - data (pd.DataFrame): Входные данные с индексом в виде дат и столбцом 'temperature'.
        """
        self.data = data

    @cache_decorator
    def moving_average(self, window: int) -> pd.Series:
        """
        Вычисляет скользящее среднее для столбца 'temperature'.

        Параметры:
        - window (int): Размер окна для скользящего среднего.

        Возвращает:
        - pd.Series: Скользящее среднее температур в заданном окне.
        """
        return self.data['temperature'].rolling(window=window).mean()

    @cache_decorator
    def differential(self) -> pd.Series:
        """
        Вычисляет первую разность температурного ряда (дифференциал).

        Возвращает:
        - pd.Series: Разности между последовательными температурами.
        """
        return self.data['temperature'].diff()

    @cache_decorator
    def autocorrelation(self, lag: int) -> float:
        """
        Вычисляет значение автокорреляции для заданного лага.

        Параметры:
        - lag (int): Задержка, для которой рассчитывается автокорреляция.

        Возвращает:
        - float: Значение автокорреляции.
        """
        return self.data['temperature'].autocorr(lag=lag)

    @cache_decorator
    def find_extremes(self) -> (pd.Series, pd.Series):
        """
        Находит локальные максимумы и минимумы в ряду температур.

        Возвращает:
        - tuple of pd.Series: (maxima, minima) где:
          - maxima: Серия с локальными максимумами температур.
          - minima: Серия с локальными минимумами температур.
        """
        maxima = self.data['temperature'][(self.data['temperature'].shift(1) < self.data['temperature']) & 
                                          (self.data['temperature'].shift(-1) < self.data['temperature'])]
        minima = self.data['temperature'][(self.data['temperature'].shift(1) > self.data['temperature']) & 
                                          (self.data['temperature'].shift(-1) > self.data['temperature'])]
        return maxima, minima

    def autocorrelation_generator(self):
        """
        Генератор, вычисляющий автокорреляцию для всех возможных лагов от 0 до длины ряда - 1.

        Генерирует:
        - float: значение автокорреляции поочерёдно для каждого лага.
        """
        n = len(self.data)
        for lag in range(n):
            yield self.autocorrelation(lag)

    @cache_decorator
    def process_data(self) -> pd.DataFrame:
        """
        Обрабатывает исходные погодные данные, интегрируя основные метрики в один DataFrame.

        В процессе обработки данные дополняются следующими столбцами:
        - 'moving_average': Скользящее среднее температур с окном в 7 дней.
        - 'differential': Первая разность (дифференциал) температур.
        - 'autocorrelation': Значения автокорреляции для всех лагов от 0 до длины ряда - 1.
        - 'maxima': Локальные максимумы температур.
        - 'minima': Локальные минимумы температур.

        Возвращает:
        - pd.DataFrame: DataFrame с исходными и вычисленными данными.
        """
        result = pd.DataFrame(index=self.data.index)
        result['temperature'] = self.data['temperature']
        result['moving_average'] = self.moving_average(window=7)
        result['differential'] = self.differential()
        result['autocorrelation'] = list(self.autocorrelation_generator())
        result['maxima'], result['minima'] = self.find_extremes()
        return result

def save_to_excel(df: pd.DataFrame, filename: str):
    """
    Сохраняет DataFrame в Excel файл.

    Параметры:
    - df (pd.DataFrame): DataFrame, который нужно сохранить.
    - filename (str): Путь и имя файла, в который будет сохранён DataFrame.
    """
    df.to_excel(filename)