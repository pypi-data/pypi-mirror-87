#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ ТЕКУЩЕЕ СИСТЕМНОЕ ВРЕМЯ

from datetime import datetime
from time import sleep

# Подключаем библиотеку для работы с индикатором I2C-flash.
from pyiArduinoI2Cled import *

# Объявляем объект библиотеки pyiArduinoI2Cled, указывая адрес модуля на шине I2C.
disp = pyiArduinoI2Cled(0x09)

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#disp = pyiArduinoI2Cled()

# Указываем двоеточию мигать (если оно выводится на индикатор).
disp.blink(0, True)

try:

    while True:

        hour = datetime.now().hour
        minute = datetime.now().minute

        # Выводим значения i и j как время (через двоеточие).
        disp.print(hour, minute, TIME)

except:

    # Очищаем дисплей если сценарий был прерван из-за исключения
    disp.clear()
