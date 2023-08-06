# distutils: language = c++
# cython: language_level = 3

from iarduino_I2C_4LED cimport iarduino_I2C_4LED
import ctypes
#import numpy as np
#from time import sleep

DEF_CHIP_ID_FLASH =  0x3C
DEF_CHIP_ID_METRO =  0xC3

# Адреса регистров модуля:
REG_FLAGS_0          =  0x00
REG_BITS_0           =  0x01
REG_FLAGS_1          =  0x02
REG_BITS_1           =  0x03
REG_MODEL            =  0x04
REG_VERSION          =  0x05
REG_ADDRESS          =  0x06
REG_CHIP_ID          =  0x07
REG_SHT_PERIOD       =  0x08
REG_SHT_FLG          =  0x10
REG_SHT_TEM_L        =  0x11
REG_SHT_HUM_L        =  0x13
REG_SHT_TEM_CHANGE   =  0x15
REG_SHT_HUM_CHANGE   =  0x16

#
DEC                  =  10
LEN1                 =  11
LEN2                 =  12
LEN3                 =  13
LEN4                 =  14
HEX                  =  16
TIME                 =  17
TEMP                 =  18
LEFT                 =  19
RIGHT                =  20
POS1                 =  21
POS2                 =  22
POS3                 =  23
POS4                 =  24
LED_CA               =  0xC0
LED_CC               =  0x40




NO_BEGIN = 1

cdef class pyiArduinoI2Cled:
    cdef iarduino_I2C_4LED c_module

    def __cinit__(self, address=None, auto=None):

        if address is not None:

            self.c_module = iarduino_I2C_4LED(address)

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля,"
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

        else:

            self.c_module = iarduino_I2C_4LED()

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля, "
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

    def begin(self):
        return self.c_module.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_module.changeAddress(newAddr)

    def reset(self):
        return self.c_module.reset()

    def getAddress(self):
        return self.c_module.getAddress()

    def getVersion(self):
        return self.c_module.getVersion()

    def getPullI2C(self):
        return self.c_module.getPullI2C()

    def setPullI2C(self, flag = True):
        if flag is not True:
                return self.c_module.setPullI2C(flag)
        else:
                return self.c_module.setPullI2C(True)

    def scheme(self, var):
        self.c_module.scheme(var)

    def fps(self, freq):
        self.c_module.fps(freq)

    def light(self, level):
        self.c_module.light(level)

    def turn(self, flg):
        self.c_module.turn(flg)

    def clear(self):
        self.c_module.clear()

    def point(self, pos, flg):
        self.c_module.point(pos, flg)

    def blink(self, pos, flg):
        self.c_module.blink(pos, flg)

    def frequ(self, f):
        self.c_module.frequ(f)

    def setLED(self, a=0, b=0, c=0, d=0, e=False):
        self.c_module.setLED(a, b, c, d, e)

    def print(self, a=255, b=255, c=255, d=255, e=255, f=255, g=255):

        char_index = None
        args = [a, b, c, d, e, f, g]

        for i in args:
            if isinstance(i, str):
                char_index = args.index(i)

        cdef int ca[4]

        if isinstance(a, str):

            bt = bytearray(a, "utf-8")
            self.c_module.printStr(bt)

        elif isinstance(a, list):

            for i in xrange(len(ca)):
                ca[i] = a[i]

            self.c_module.printArr(ca)

        elif char_index is not None:

            bt = bytearray(args[char_index], "utf-8")
            del args[char_index]

            if isinstance(a, int):

                self.c_module.print(a, int(bt[0]), int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))

            if isinstance(a, float):

                self.c_module.printFloatChar(a, int(bt[0]), int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))

        elif isinstance(a, float):

            self.c_module.printFloatNoChar(a, b, c, d, e, f)

        elif isinstance(a, int):

            self.c_module.printIntNoChar(a, b, c, d, e, f)

        else:

            return
