// ПРИМЕР ВЫВОДИТ ВРЕМЯ ПРОШЕДШЕЕ ПОСЛЕ СТАРТА:

#include <time.h>
#include "../iarduino_I2C_4LED.h"
iarduino_I2C_4LED dispLED(0x09);

struct tm *tm_struct;

int main()
{
	delay(500);
	//   Инициируем работу с индикатором.
	dispLED.begin();

	// Указываем двоеточию мигать (если оно выводится на индикатор).
	dispLED.blink(0, 1);

	for (;;) {
		time_t now = time(NULL);
		tm_struct = localtime(&now);
		int hour = tm_struct->tm_hour;
		int min = tm_struct->tm_min;
		dispLED.print(hour, min, TIME);
		delay(1000);
	}
}
