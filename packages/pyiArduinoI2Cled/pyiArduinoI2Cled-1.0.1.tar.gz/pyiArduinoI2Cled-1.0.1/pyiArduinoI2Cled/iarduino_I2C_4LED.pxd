cdef extern from "iarduino_I2C_4LED.cpp":
    pass

cdef extern from "itoa.cpp":
    pass

cdef extern from "dtostrf.cpp":
    pass

cdef extern from "WString.cpp":
    pass


cdef extern from "iarduino_I2C_4LED.h":
    cdef cppclass iarduino_I2C_4LED:
        iarduino_I2C_4LED() except +
        iarduino_I2C_4LED(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
        bint getPullI2C()
        bint setPullI2C(bint)
        void scheme(unsigned char)
        void fps(unsigned char)
        void light(unsigned char)
        void turn(bint)
        void clear()
        void point(unsigned char, bint)
        void blink(unsigned char, bint)
        void frequ(unsigned char);
        void setLED(unsigned char, unsigned char, unsigned char, unsigned char, bint);
#       void print(short, int, int, int, int, int)
#       void print(short, char, int, int, int, int, int)
#       void print(short, int, char, int, int, int, int)
#       void print(short, int, int, char, int, int, int)
#       void print(short, int, int, int, char, int, int)
#       void print(short, int, int, int, int, char, int)
#       void print(short, int, int, int, int, int, char)
#       void print(unsigned short, int, int, int, int, int)
#       void print(unsigned short, char, int, int, int, int, int)
#       void print(unsigned short, int, char, int, int, int, int)
#       void print(unsigned short, int, int, char, int, int, int)
#       void print(unsigned short, int, int, int, char, int, int)
#       void print(unsigned short, int, int, int, int, char, int)
#       void print(unsigned short, int, int, int, int, int, char)
        void printIntNoChar "print"(int, int, int, int, int, int)
#       void print(int, char, int, int, int, int, int)
#       void print(int, int, char, int, int, int, int)
#       void print(int, int, int, char, int, int, int)
#       void print(int, int, int, int, char, int, int)
#       void print(int, int, int, int, int, char, int)
#       void print(int, int, int, int, int,          int, char)
#       void print(unsigned int, int, int, int, int, int)
#       void print(unsigned int, char, int, int, int, int, int)
#       void print(unsigned int, int, char, int, int, int, int)
#       void print(unsigned int, int, int, char, int, int, int)
#       void print(unsigned int, int, int, int, char, int, int)
#       void print(unsigned int, int, int, int, int, char, int)
#       void print(unsigned int, int, int, int, int, int, char)
        void printFloatNoChar "print"(double, int, int, int, int, int)
        void printFloatChar "print"(double, char, int, int, int, int, int)
#       void print(double, int, char, int, int, int, int)
#       void print(double, int, int, char, int, int, int)
#       void print(double, int, int, int, char, int, int)
#       void print(double, int, int, int, int, char, int)
#       void print(double, int, int, int, int, int, char)
        void print(int, char, int, int, int, int, int)
        void printStr "print"(char*)
        void printArr "print"(int*)
