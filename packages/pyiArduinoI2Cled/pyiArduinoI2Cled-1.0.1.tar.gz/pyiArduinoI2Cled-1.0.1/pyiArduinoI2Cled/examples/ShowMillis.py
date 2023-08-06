#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ СЕКУНДЫ ПРОШЕДШИЕ ПОСЛЕ СТАРТА:

import time

# Подключаем библиотеку для работы с индикатором I2C-flash.
from pyiArduinoI2Cled import *

# Объявляем объект библиотеки pyiArduinoI2Cled, указывая адрес модуля на шине I2C.
disp = pyiArduinoI2Cled(0x09)

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#disp = pyiArduinoI2Cled()

start = time.time()

while True:

    now = time.time() - start
    # Выводим число с двумя знаками после запятой.
    disp.print(now , 2)
    time.sleep(.01)
