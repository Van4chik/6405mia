from setuptools import setup, find_packages
"""
Этот модуль содержит настройки для установки пакета weather_analysis.

Пакет weather_analysis предназначен для анализа данных о погоде. Он включает в себя инструменты для загрузки,
обработки и анализа метеорологических данных с использованием библиотек pandas, numpy и meteostat.

Функции:
    setup() - функция настройки setuptools, которая определяет параметры установки пакета.

Аргументы функции setup:
    name (str): Название пакета.
    version (str): Версия пакета.
    packages (list): Список пакетов, включенных в установку.
    install_requires (list): Список зависимостей, необходимых для работы пакета.
    entry_points (dict): Определение точек входа для консольных скриптов.
"""
setup(
    name='weather_analysis',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'meteostat',
        'openpyxl'
    ],
    entry_points={
        'console_scripts': [
            'weather_analysis=weather_analysis.cli:main',
        ],
    },
)