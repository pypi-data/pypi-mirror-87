// ПРИМЕР ВЫВОДИТ МИЛЛИСЕКУНДЫ ПРОШЕДШИЕ ПОСЛЕ СТАРТА:

#include <sys/timeb.h>
// Подключаем библиотеку для работы с индикатором I2C-flash.
#include "../iarduino_I2C_4LED.h"

// Объявляем объект dispLED для работы с функциями и методами библиотеки iarduino_I2C_4LED, указывая адрес модуля на шине I2C.
// Если объявить объект без указания адреса (iarduino_I2C_4LED dispLED;), то адрес будет найден автоматически.
iarduino_I2C_4LED dispLED(0x09);

struct timeb start, end;

void loop(void);

int main()
{
	// Инициируем работу с индикатором.
	dispLED.begin();
	ftime(&start);
	for(;;)
		loop();
}

void loop()
{
	ftime(&end);
	int millis = (int)(1000.0 * (end.time - start.time) + (end.millitm - start.millitm));
	dispLED.print(millis);
	delay(1);
}
