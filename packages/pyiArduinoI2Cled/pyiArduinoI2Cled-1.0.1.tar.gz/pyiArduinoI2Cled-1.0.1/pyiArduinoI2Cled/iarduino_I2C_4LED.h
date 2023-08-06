//	Библиотека для работы с 4-зазрядным LED индикатором, I2C-flash для Arduino: https://iarduino.ru/shop/Displei/chetyrehrazryadnyy-indikator-led-krasnyy-flash-i2c-trema-modul.html
//  Версия: 1.0.0
//  Последнюю версию библиотеки Вы можете скачать по ссылке: https://iarduino.ru/file/536.html
//  Подробное описание функций бибилиотеки доступно по ссылке: https://wiki.iarduino.ru/page/4-led-i2c/
//  Библиотека является собственностью интернет магазина iarduino.ru и может свободно использоваться и распространяться!
//  При публикации устройств или скетчей с использованием данной библиотеки, как целиком, так и её частей,
//  в том числе и в некоммерческих целях, просим Вас опубликовать ссылку: http://iarduino.ru
//  Автор библиотеки: Панькин Павел.
//  Если у Вас возникли технические вопросы, напишите нам: shop@iarduino.ru

#ifndef iarduino_I2C_4LED_h																						//
#define iarduino_I2C_4LED_h																						//
																												//
//#if defined(ARDUINO) && (ARDUINO >= 100)																		//
//#include		<Arduino.h>																						//
//#else																											//
//#include		<WProgram.h>																					//
//#endif																										//

#define DEC 10
#define HEX 16
#define OCT 8
#ifdef BIN
#undef BIN
#endif
#define BIN 2
																												//
#include		"iarduino_I2C_PI.h"																				//	Подключаем файл iarduino_I2C_I2C.h - для работы с шиной I2C		(используя функции структуры iI2C)
#include "WString.h"
																												//
#define			DEF_CHIP_ID_FLASH		0x3C																	//	ID линейки чипов - константа для всех чипов серии Flash (позволяет идентифицировать принадлежность чипа к серии).
#define			DEF_CHIP_ID_METRO		0xC3																	//	ID линейки чипов - константа для всех чипов серии Metro (позволяет идентифицировать принадлежность чипа к серии).
#define			DEF_MODEL_MOT			0x16																	//	Идентификатор модели - константа.
//				Адреса регистров модуля:																		//
#define			REG_FLAGS_0				0x00																	//	Адрес регистра флагов управления для чтения.
#define			REG_BITS_0				0x01																	//	Адрес регистра битов  управления для чтения и записи.
#define			REG_FLAGS_1				0x02																	//	Адрес регистра флагов управления для чтения.
#define			REG_BITS_1				0x03																	//	Адрес регистра битов  управления для чтения и записи.
#define			REG_MODEL				0x04																	//	Адрес регистра содержащего номер типа модуля.
#define			REG_VERSION				0x05																	//	Адрес регистра содержащего версию прошивки.
#define			REG_ADDRESS				0x06																	//	Адрес регистра содержащего текущий адрес модуля на шине I2C. Если адрес указан с флагом IF-PIN-ADDRES то адрес установится (и запишется в регистр) только при наличии 1 на входе PIN_ADDRES.
#define			REG_CHIP_ID				0x07																	//	Адрес регистра содержащего ID линейки чипов «Flash». По данному ID можно определить принадлежность чипа к линейки «Flash».
#define			REG_4LED_FREQUENCY		0x08																	//	Адрес регистра хранящего частоту обновления всех сегментов индикатора, значение от 1 до 255 Гц.
#define			REG_4LED_BRIGHTNESS		0x09																	//	Адрес регистра хранящего яркость индикатора, значение от 0 до 255 с шагом 8 (0-7 нет, 8-15 мин ... 247-255 макс).
#define			REG_4LED_FLG			0x10																	//	Адрес регистра хранящего флаги
#define			REG_4LED_BLINK			0x11																	//	Адрес регистра позволяющего мигать разрядами индикатора.
#define			REG_4LED_DEG			0x12																	//	Адрес регистра хранящего состояние светодиодов в 1 разряде индикатора. Далее следуют регистры 2, 3 и 4 разряда.
#define			REG_4LED_POINT			0x16																	//	Адрес регистра хранящего состояние светодиодов двоеточия.
//				Позиция битов и флагов:																			//
#define			LED_FLG_CA				0x80																	//	Флаг указывает   на то, что сегменты разрядов индикатора соединены по схеме с общим анодом.
#define			LED_BIT_SAVE_CA			0x40																	//	Бит  разрешает   изменение флага «FLG_OA».
#define			LED_BIT_TURN			0x01																	//	Бит  переворота  изображения индикатора.
#define			LED_BIT_FREQUENCY		0xC0																	//	Биты установки   частоты миганий разрядов индикатора.
#define			LED_BIT_DEG4			0x10																	//	Бит  указывающий мигать светодиодами двоеточия индикатора.
#define			LED_BIT_DEG3			0x08																	//	Бит  указывающий мигать светодиодами 4 разряда индикатора.
#define			LED_BIT_DEG2			0x04																	//	Бит  указывающий мигать светодиодами 3 разряда индикатора.
#define			LED_BIT_DEG1			0x02																	//	Бит  указывающий мигать светодиодами 2 разряда индикатора.
#define			LED_BIT_DEG0			0x01																	//	Бит  указывающий мигать светодиодами 1 разряда индикатора.

#define			LED_SEG_A				0x80																	//	Бит  определяет состояние сегмента A.                  A                           A
#define			LED_SEG_B				0x40																	//	Бит  определяет состояние сегмента B.                ┌─┴─┐                       ┌─┴─┐
#define			LED_SEG_C				0x20																	//	Бит  определяет состояние сегмента C.             ┌─┐└───┘┌─┐       P-UP      ┌─┐└───┘┌─┐
#define			LED_SEG_D				0x10																	//	Бит  определяет состояние сегмента D.          F ─┤ │  G  │ ├─ B    ┌┴┐    F ─┤ │  G  │ ├─ B
#define			LED_SEG_E				0x08																	//	Бит  определяет состояние сегмента E.             └─┘┌─┴─┐└─┘       └─┘       └─┘┌─┴─┐└─┘
#define			LED_SEG_F				0x04																	//	Бит  определяет состояние сегмента F.             ┌─┐└───┘┌─┐       ┌─┐       ┌─┐└───┘┌─┐
#define			LED_SEG_G				0x02																	//	Бит  определяет состояние сегмента G.          E ─┤ │     │ ├─ C    └┬┘    E ─┤ │     │ ├─ C
#define			LED_SEG_H				0x01																	//	Бит  определяет состояние сегмента H.             └─┘┌───┐└─┘┌─┐    P-DN      └─┘┌───┐└─┘┌─┐
#define			LED_SEG_P_UP			0x02																	//	Бит  определяет состояние сегмента P-UP.             └─┬─┘   └┬┘                 └─┬─┘   └┬┘
#define			LED_SEG_P_DN			0x01																	//	Бит  определяет состояние сегмента P-DN.               D      H                    D      H
																												//
//				DEC     				10																		//	print( 0xFFF , DEC          ); вывод числа в 10-тичной системе					= 4095
#define			LEN1					11																		//	print( 1234  , LEN1         ); вывод числа в 1 разряде							= •••4
#define			LEN2					12																		//	print( 123   , LEN2         ); вывод числа в 2 разрядах							= ••23
#define			LEN3					13																		//	print( 12    , LEN3         ); вывод числа в 3 разрядах							= •012
#define			LEN4					14																		//	print( 1     , LEN4         ); вывод числа в 4 разрядах							= 0001
//				HEX     				16																		//	print( 4095  , HEX          ); вывод числа в 16-ричной системе					= •FFF
#define			TIME					17																		//	print( 1 , 2 , TIME         ); вывод времени									= 01:02
#define			TEMP					18																		//	print( 12    , TEMP         ); вывод температуры								= •12°
#define			LEFT					19																		//	print( 12    ,[POS4], LEFT  ); вывод числа со сдвигом от влево  от 4 позиции	= ••12
#define			RIGHT					20																		//	print( 12    ,[POS1], RIGHT ); вывод числа со сдвигом от вправо от 1 позиции	= 12••
#define			POS1					21																		//	print( 12    , POS1 ,[LEFT] ); вывод числа со сдвигом от влево  от 1 позиции	= 2•••
#define			POS2					22																		//	print( 12    , POS2 ,[LEFT] ); вывод числа со сдвигом от влево  от 2 позиции	= 12••
#define			POS3					23																		//	print( 12    , POS3 ,[LEFT] ); вывод числа со сдвигом от влево  от 3 позиции	= •12•
#define			POS4					24																		//	print( 12    , POS4 ,[LEFT] ); вывод числа со сдвигом от влево  от 4 позиции	= ••12
#define			LED_CA					0xC0																	//	scheme( LED_CA );              светодиоды индикатора включены по схеме с общим анодом.
#define			LED_CC					0x40																	//	scheme( LED_CC );              светодиоды индикатора включены по схеме с общим катодом.
																												//
class iarduino_I2C_4LED{																						//
	public:																										//
	/**	Конструктор класса **/																					//
		iarduino_I2C_4LED							(uint8_t address=0){										//	Конструктор класса													(Параметр: адрес модуля на шине I2C, если не указан (=0), то адрес будет определён).
													if(address>0x7F){ address>>=1; }							//	Корректируем адрес, если он указан с учётом бита RW.
							valAddrTemp			=	address;													//	Сохраняем переданный адрес модуля.
							objI2C				=	new iarduino_I2C;											//	Переопределяем указатель objI2C на объект производного класса iarduino_I2C.
		}																										//
	/**	Пользовательские функции **/																			//
		bool				begin					(void				);										//	Объявляем  функцию инициализации модуля								(Параметр:  отсутствует).
		bool				reset					(void				);										//	Объявляем  функцию перезагрузки модуля								(Параметр:  отсутствует).
		bool				changeAddress			(uint8_t			);										//	Объявляем  функцию смены адреса модуля на шине I2C					(Параметр:  новый адрес модуля).
		uint8_t				getAddress				(void				){ return valAddr;	}					//	Определяем функцию возвращающую текущий адрес модуля на шине I2C	(Параметр:  отсутствует).
		uint8_t				getVersion				(void				){ return valVers;	}					//	Определяем функцию возвращающую текущую версию прошивки модуля		(Параметр:  отсутствует).
		bool				getPullI2C				(void				);										//	Объявляем  функцию возвращающую флаг наличия подтяжки шины I2C		(Параметр:  отсутствует).
		bool				setPullI2C				(bool=true			);										//	Объявляем  функцию установки    подтяжки шины I2C					(Параметр:  флаг подтяжки).
		void				scheme					(uint8_t			);										//	Объявляем  функцию установки    схемы включения светодиодов			(Параметр:  частота в Гц от 1 до 255).
		void				fps						(uint8_t			);										//	Объявляем  функцию установки    частоты обновления данных			(Параметр:  частота в Гц от 1 до 255).
		void				light					(uint8_t			);										//	Объявляем  функцию установки    яркости индикатора				 	(Параметр:  яркость от 0 до 7).
		void				turn					(bool				);										//	Объявляем  функцию разворота    изображения на индикаторе		 	(Параметр:  флаг разворота).
		void				clear					(void				){ _printNumS(""); }					//	Определяем функцию очистки всех разрядов индикатора					(Параметр:  отсутствует).
		void				point					(uint8_t=255,bool=0	);										//	Объявляем  функцию установки    точек								(Параметры: ПОЗИЦИЯ от 1 до 4 или 0 для двоеточия, СОСТОЯНИЕ 0/1).
		void				blink					(uint8_t=255,bool=0	);										//	Объявляем  функцию установки    миганий разрядов					(Параметры: ПОЗИЦИЯ от 1 до 4 или 0 для двоеточия, СОСТОЯНИЕ 0/1).
		void				frequ					(uint8_t			);										//	Объявляем  функцию установки    частоты мигания разрядов			(Параметр:	ЧАСТОТА от 1 до 4 Гц).
		void				setLED					(uint8_t=0, uint8_t=0, uint8_t=0, uint8_t=0, bool=0);		//	Объявляем  функцию установки    светодиодов по битам				(Параметры: БАЙТ старшего разряда, БАЙТ, БАЙТ, БАЙТ младшего разряда, ФЛАГ двоеточия).
		void				print					(    int16_t i,          int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle('0',j1,j2,j3,j4,j5); if(valType==TIME){_printNumT(i,j1);}else{_printNumI(i);}}
		void				print					(    int16_t i, char j0, int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(    int16_t i,          int j1    , char j0, int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(    int16_t i,          int j1    ,          int j2    , char j0, int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(    int16_t i,          int j1    ,          int j2    ,          int j3    , char j0, int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(    int16_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    , char j0, int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(    int16_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    ,          int j5,    char j0){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(i);}
		void				print					(   uint16_t i,          int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle('0',j1,j2,j3,j4,j5); if(valType==TIME){_printNumT(int16_t(i),j1);}else{_printNumI(int16_t(i));}}
		void				print					(   uint16_t i, char j0, int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint16_t i,          int j1    , char j0, int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint16_t i,          int j1    ,          int j2    , char j0, int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint16_t i,          int j1    ,          int j2    ,          int j3    , char j0, int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint16_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    , char j0, int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint16_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    ,          int j5,    char j0){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle('0',j1,j2,j3,j4,j5); if(valType==TIME){_printNumT(int16_t(i),j1);}else{_printNumI(int16_t(i));}}
		void				print					(    int32_t i, char j0, int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1    , char j0, int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1    ,          int j2    , char j0, int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1    ,          int j2    ,          int j3    , char j0, int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    , char j0, int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(    int32_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    ,          int j5,    char j0){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle('0',j1,j2,j3,j4,j5); if(valType==TIME){_printNumT(int16_t(i),j1);}else{_printNumI(int16_t(i));}}
		void				print					(   uint32_t i, char j0, int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1    , char j0, int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1    ,          int j2    , char j0, int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1    ,          int j2    ,          int j3    , char j0, int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    , char j0, int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(   uint32_t i,          int j1    ,          int j2    ,          int j3    ,          int j4    ,          int j5,    char j0){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumI(int16_t(i));}
		void				print					(     double i,          int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle('0',j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i, char j0, int j1=255,          int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i,          int j1    , char j0, int j2=255,          int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i,          int j1    ,          int j2    , char j0, int j3=255,          int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i,          int j1    ,          int j2    ,          int j3    , char j0, int j4=255,          int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i,          int j1    ,          int j2    ,          int j3    ,          int j4    , char j0, int j5=255        ){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(     double i,          int j1    ,          int j2    ,          int j3    ,          int j4    ,          int j5,    char j0){_sortStyle( j0,j1,j2,j3,j4,j5); _printNumF(i);}
		void				print					(      char *i		){_sortStyle(' ',255,255,255,255,255);                                                                                                       _printNumS(i);}
		void				print					(const char *i		){_sortStyle(' ',255,255,255,255,255); char j[10]; j[9]=0; for(size_t k=0; k<9; k++){j[k]=i[k]; if(i[k]==0){k=10;}}                         _printNumS(j);}
		void				print					(     String i		){_sortStyle(' ',255,255,255,255,255); char j[10]; j[9]=0; for(size_t k=0; k<9; k++){j[k]=i[k]; if(i[k]==0){k=10;}}                         _printNumS(j);}
		void				print					(      int i[]		){_sortStyle(' ',255,255,255,255,255);                                                                                                       _printNumA(i);}
	private:																									//
	/**	Внутренние переменные **/																				//
		uint8_t				valAddrTemp			=	0;															//	Определяем переменную для хранения адреса модуля на шине I2C который был указан, но не был проверен.
		uint8_t				valAddr				=	0;															//	Определяем переменную для хранения адреса модуля на шине I2C.
		uint8_t				valVers				=	0;															//	Определяем переменную для хранения версии прошивки модуля.
		uint8_t				data[5];																			//	Объявляем  массив     для хранения получаемых/передаваемых данных.
		uint8_t				dataTemp[5]			=	{0,0,0,0,0};												//	Объявляем  массив     для хранения уже записанных данных в индикатор.
		uint8_t				varLen;																				//	0,1,2,3,4,255         длинна (количество рязрядов) выводимого числа, 255-по размеру числа.
		char				symZero;																			//	' '                   символ заменяющий знаки 0 перед числом (если «varLen» больше разрядности числа).
		uint8_t				valPos;																				//	POS1 - POS4           позиция (номер разряда) выводимого числа.
		uint8_t				valDir;																				//	LEFT / RIGHT          направление сдвига от указанной позиции.
		uint8_t				valType;																			//	DEC/HEX/TIME/TEMP     тип выводимого числа.
		uint8_t				valPart;																			//	0,1,2,3,4,255         количество знаков после запятой, 255-не указано.
		char				arrString[11];																		//	"X.X.:X.X."           строка символов для вывода на экран.
		iarduino_I2C_BASE*	objI2C;																				//	Объявляем  указатель  на  объект полиморфного класса iarduino_I2C_BASE, но в конструкторе данного класса этому указателю будет присвоена ссылка на производный класс iarduino_I2C.
	/**	Внутренние функции **/																					//
		void				_writeData				(uint8_t, uint8_t								);			//	Объявляем  функцию вывода одного разряда							(Параметры: байт, позиция).
		void				_writeData				(void											);			//	Объявляем  функцию вывода строки «arrString» на весь индикатор.		(Параметр:  отсутствует).
		uint8_t				_codeSymbol				(char											);			//	Объявляем  функцию закодировать символ для его вывода				(Параметр:  символ).
		void				_printNumI				(int16_t										);			//	Объявляем  функцию вывод целого числа.
		void				_printNumF				(double											);			//	Объявляем  функцию вывод числа с плавающей точкой.
		void				_printNumS				(const char*									);			//	Объявляем  функцию вывод строки.
		void				_printNumA				(int i[]										);			//	Объявляем  функцию вывод массива.
		void				_printNumT				(uint8_t, uint8_t								);			//	Объявляем  функцию вывод времени.
		void				_sortStyle				(char,uint8_t,uint8_t,uint8_t,uint8_t,uint8_t	);			//	Объявляем  функцию сортировка параметров вывода.
		void				_strInsert				(char*, char, int, int							);			//	Объявляем  функцию вставить в строку char* символ char, int раз, начиная с int позиции.
		void				_strDelete				(char*, int, int								);			//	Объявляем  функцию удалить из строки char* int символов, начиная с int позиции.
		bool				_readBytes				(uint8_t, uint8_t								);			//	Объявляем  функцию чтения данных в  массив  data					(Параметры: номер первого регистра, количество байт).
		bool				_writeBytes				(uint8_t, uint8_t, uint8_t=0					);			//	Объявляем  функцию записи данных из массива data					(Параметры: номер первого регистра, количество байт, номер первого элемента массива data).
};																												//
																												//
#endif																											//
