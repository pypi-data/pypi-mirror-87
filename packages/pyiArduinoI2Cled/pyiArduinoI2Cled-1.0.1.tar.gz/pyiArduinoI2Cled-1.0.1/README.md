[![](https://iarduino.ru/img/logo.svg)](https://iarduino.ru)[![](https://wiki.iarduino.ru/img/git-shop.svg?3)](https://iarduino.ru) [![](https://wiki.iarduino.ru/img/git-wiki.svg?2)](https://wiki.iarduino.ru) [![](https://wiki.iarduino.ru/img/git-lesson.svg?2)](https://lesson.iarduino.ru)[![](https://wiki.iarduino.ru/img/git-forum.svg?2)](http://forum.trema.ru)

# pyiArduinoI2Cled

**Данная библилотека (модуль для Python3) позволяет управлять электронными модулями (устройствами) [Четырёхразрядный индикатор LED]() от iArduino.ru по шине I2C на Raspberry Pi.**

Подробнее про модуль читайте в нашей [Wiki]()

## Установка ##

[Статья на сайте iarduino.ru](https://wiki.iarduino.ru/page/raspberry-python-modules/)

Установка из репозиториев PyPI в терминале Raspberry:

`sudo pip3 install pyiArduinoI2Cled`

Самостоятельная сборка из исходников:

`git clone https://github.com/tremaru/pyiArduinoI2Cled.git && cd pyiArduinoI2Cled/pyiArduinoI2Cled && python3 setup.py build_ext --inplace`

Примеры для Python находятся в папке `pyiArduinoI2Cled/examples`

Примеры для С++ находятся в папке `pyiArduinoI2Cled/cpp`. Так же в этой папке лежит *Makefile* для сборки
из исходников. Можно собрать сразу все примеры командой:
`make all` или `make`
Для сборки конкретного примера: `make "название примера"`
Например:
`make reset`
Для удаления собранных исполняемых файлов:
`make clean`

**This is a Python3 module for Raspberry Pi. It can work with []() by iarduino.ru**
