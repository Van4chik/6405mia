import unittest
import pandas as pd
from data_analysis.weather_analysis.data_analis.data_processing import WeatherDataProcessor

class TestWeatherDataProcessor(unittest.TestCase):
    """
    Класс TestWeatherDataProcessor содержит тесты для проверки функционала класса WeatherDataProcessor.

    Методы класса:
    - setUp: подготавливает данные для тестирования.
    - test_moving_average: тестирует вычисление скользящего среднего.
    - test_differential: тестирует вычисление дифференциала температуры.
    - test_autocorrelation: тестирует вычисление автокорреляции.
    - test_find_extremes: тестирует поиск экстремумов в данных.
    - test_process_data: тестирует полную обработку данных.
    """    
    def setUp(self):
        """
        Подготавливает тестовые данные перед каждым тестом.

        Создает DataFrame с двумя колонками:
        - 'date': даты с 2023-01-01 по 2023-01-10.
        - 'temperature': значения температуры от 0 до 7 с некоторыми повторениями.
        
        Устанавливает 'date' в качестве индекса DataFrame и создает экземпляр WeatherDataProcessor.
        """
        data = {
            'date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
            'temperature': [0, 1, 2, 1, 3, 4, 2, 5, 6, 7]
        }
        self.df = pd.DataFrame(data).set_index('date')
        self.processor = WeatherDataProcessor(self.df)

    def test_moving_average(self):
        """
        Тестирует метод moving_average класса WeatherDataProcessor.

        Проверяет:
        - Длину результата (должна быть на 2 меньше исходной из-за окна в 3 элемента).
        - Значение первого вычисленного скользящего среднего.
        """
        ma = self.processor.moving_average(3)
        self.assertEqual(len(ma.dropna()), 8)
        self.assertAlmostEqual(ma.dropna().iloc[0], 1.0)

    def test_differential(self):
        """
        Тестирует метод differential класса WeatherDataProcessor.

        Проверяет:
        - Длину результата (должна быть на 1 меньше исходной, так как это первая разность).
        - Значение первой разности.
        """
        diff = self.processor.differential()
        self.assertEqual(len(diff.dropna()), 9)
        self.assertEqual(diff.iloc[1], 1)

    def test_autocorrelation(self):
        """
        Тестирует метод autocorrelation класса WeatherDataProcessor.

        Проверяет:
        - Тип возвращаемого значения (должен быть float).
        """
        ac = self.processor.autocorrelation(1)
        self.assertIsInstance(ac, float)

    def test_find_extremes(self):
        """
        Тестирует метод find_extremes класса WeatherDataProcessor.

        Проверяет:
        - Количество найденных максимумов и минимумов.
        - Значения первого найденного максимума и минимума.
        """
        maxima, minima = self.processor.find_extremes()
        self.assertEqual(len(maxima), 2)
        self.assertEqual(len(minima), 2)
        self.assertAlmostEqual(maxima.iloc[0], 2)
        self.assertAlmostEqual(minima.iloc[0], 1)

    def test_process_data(self):
        """
        Тестирует метод process_data класса WeatherDataProcessor.

        Проверяет:
        - Наличие ожидаемых колонок в результате.
        - Соответствие длины колонки 'autocorrelation' длине исходного DataFrame.
        """
        processed_data = self.processor.process_data()
        self.assertIn('moving_average', processed_data.columns)
        self.assertIn('differential', processed_data.columns)
        self.assertIn('autocorrelation', processed_data.columns)
        self.assertIn('maxima', processed_data.columns)
        self.assertIn('minima', processed_data.columns)
        self.assertEqual(len(processed_data['autocorrelation']), len(self.df))

if __name__ == '__main__':
    unittest.main()