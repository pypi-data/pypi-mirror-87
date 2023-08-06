// Данный пример меняет адрес модуля на указанный в argv[1].

#include <iostream>
#include "../iarduino_I2C_4LED.h"

iarduino_I2C_4LED module;

uint8_t newAddress = 9;

int main(int argc, char** argv){
        if (argc > 1) {

                newAddress = atoi(argv[1]);

        }

        if (module.begin()){

                std::cout << "На шине I2C найден модуль с адресом 0x";
                std::cout << std::hex << int(module.getAddress());
                std::cout << " который является четырёхразрядным индикатором\n";

                if (module.changeAddress(newAddress)){

                        std::cout << "Адрес модуля изменён на 0x";
                        std::cout << std::hex << int(module.getAddress()) << '\n';
                }
                else {

                        std::cout << "Адрес модуля изменить не удалось!" << '\n';

                }
        }
        else {

                std::cout << "Расширитель выводов не найден!" << '\n';

        }
}

//  ПРИМЕЧАНИЕ:
//  Данная программа демонстрирует не только возможность смены адреса
//  на указанный в переменной newAddress, но и обнаружение, и вывод
//  текущего адреса модуля на шине I2C.
