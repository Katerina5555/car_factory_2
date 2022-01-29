import hashlib
import random
import time
import uuid
from driver import Driver
import datetime

from typing import Union


class DriverTypeError(Exception):
    pass


class EngineIsNotRunning(Exception):
    pass


class DriverNotFoundError(Exception):
    pass


class DoTechnicalDiscussion(Exception):
    pass


class EngineIsRunning(Exception):
    pass


class DriverNoRules(Exception):
    pass


class Car:
    brand = None   #публичный
    _max_speed = 180    #защищенный
    __created_car = 0   #приватный

    def __init__(self, engine_type=None, body_type=None, gear_type=None, drive_type=None,
                 configuration=None, color=None, object_category=None):
        """создание атрибутов класса машина"""

        self.__body_type = body_type
        self._engine_type = engine_type
        self._gear_type = gear_type
        self._drive_type = drive_type
        self.configuration = configuration
        self.color = color

        self.__vin_number = uuid.uuid4()
        self.__created_time = time.time()
        self.__mileage = 0

        self.__status_engine = False
        self.__driver = None
        self.__last_to = 0  # пробег на котором было сделано последнее ТО
        self.__service_interval = 30  # необходимая частота ТО

        self.car_key = None  # ключ который хранится в машине, и сверяется с ключом водителя
        self.__keys_was_send = False  # переменная которая проверяет выдавались ли ключи
        self.__object_category = object_category

    def __new__(cls, *args, **kwargs):
        cls.__append_new_car_counter()
        print(f"Создано {cls.__created_car} класса {cls.__name__}")
        return super().__new__(cls)

    """создание методов класса"""

    @classmethod
    def change_brand(cls, new_brand):
        """Изменение наименования Брэнда"""
        cls.brand = new_brand

    @classmethod
    def set_max_speed(cls, max_speed) -> int:
        """Возможность изменения максимальной скорости"""
        if not isinstance(max_speed, (int, float)):
            raise TypeError(f'Ожидается тип {int} или {float}, получен {type(max_speed)}')
        cls._max_speed = max_speed

    @classmethod
    def __append_new_car_counter(cls):
        cls.__created_car += 1

    def __create_keys(self):
        h = hashlib.new('sha256')
        vin = str(self.__vin_number).encode('utf-8')
        h.update(vin)
        self.car_key = h.hexdigest()
        return self.car_key

    def get_keys(self):
        """Ключи выдаются только 1 раз"""
        if self.__keys_was_send:
            print('Ключи уже были выданы')
        else:
            self.__keys_was_send = True
            return self.__create_keys()

    def __check_keys(self, key):
        if self.car_key == key:
            return True
        else:
            print('Ключи не подходят')
            return False

    def start_engine(self, key):
        if self.__check_keys(key):
            self.__status_engine = True
            print('Машина завелась')
        else:
            print('Крутится стартер')

    def __is_ready_to_move(self):
        """Проверка готовности машины к движению - запущен ли двигатель"""

        if not self.__status_engine:
            raise EngineIsNotRunning("Двигатель не запущен")

        if self.__driver is None:
            raise DriverNotFoundError("Водитель не найден")
        return True

    def max_time_on_the_way(self) -> int:
        """Расчет максимального времени в пути:
        1) проверка типа стажа вождения
        2) проверка правильности заведенных данных по стажу вождения
        3) проверка соответствия стажа возрасту Водителя"""
        if not isinstance(self.driver.experience, int):
            raise TypeError('Задайте опыт целочисленным значением')
        elif int(self.driver.experience) < 0:
            raise ValueError("Cтаж может иметь только целочисленное значение")
        elif (self.driver.age - self.driver.experience) < 18:
            raise ValueError("Стаж не соответствует возрасту, права получены ранее 18 лет")
        elif self.driver.experience < 10:
            max_no_sleep = 5    # установлено 10 минут, чтобы долго не жждать результата
        else:
            max_no_sleep = 9

        return max_no_sleep

    def speed_limit(self) -> int:
        """
        Вспомогательный расчет максимальной скорости для водителя по стажу вождения
        """
        if self.driver.experience < 10:
            max_speed = 100
        else:
            max_speed = self._max_speed
        return max_speed

    def time_to_stop(self, start_mile):
        """
        Расчет максимального километража без отдыха для конкретного водителя
        """
        max_on_the_way = int(self.speed_limit()*(self.max_time_on_the_way() / 60))

        """
        Предупреждение о предстоящей остановке и инфо после
        """

        if (self.__mileage - start_mile) % max_on_the_way - (max_on_the_way // 4 * 3) == 0 and self.__mileage != 0:     #поставлено из длины пути. каждый километр повторять - отвлекает
                b = max_on_the_way - (self.__mileage -start_mile) % max_on_the_way
                print(f'Через {b} км машина вынужденно остановится. '
                f'Необходимо найти место для остановки')

        elif (self.__mileage - start_mile) % max_on_the_way == 0 and self.__mileage != start_mile:
                a = 2
                print(f'Вам необходимо отдохнуть. '
                    f'Вы можете продолжить движение через {a} минут(ы). '
                      f'Согласно регламента Вы можете двигаться без остановки {self.max_time_on_the_way()} минут, '
                      f'при текущей скорости ({self.speed_limit()} км/ч) - это {max_on_the_way} км.')
                time.sleep(a)

    def check_technical_discussion(self) -> bool:
        """Проверка необходимости прохождения ТОЖ
         1) если ТО сделано 40 и более к назад - машина не поедет без метода
         do_technical_discussion
         2) за 10 км - предупреждение о необходимости прохождения ТО
         3) через 30 - вопрос о том пройдено ТО или нет.
         при любом ответе, кроме Да - машина не продолжит движение"""
        if self.__mileage - self.__last_to >= 40:
            return False
        elif self.__mileage - self.__last_to == 20:
            print(f"Необходимо сделать ТО через 10 км")
        elif self.__mileage - self.__last_to == self.__service_interval:
            inspection_completed = input("Сейчас необходимо сделать ТО. ТО пройден?")
            if inspection_completed == "да":
                self.do_technical_discussion()
                print(f"ТО произведено")
            else:
                raise DoTechnicalDiscussion
        return True

    def do_technical_discussion(self):
        """Проходждение ТО"""
        self.__last_to = self.__mileage
        print("Очередное ТО пройден")

    def autostart_engine(self):
        """Проверка запущен ли двигатель
        Запуск двигателя при отрицательном ответе"""
        if not self.__status_engine:
            self.__status_engine = True
            return True
        else:
            EngineIsRunning("двигатель уже запущен")
            return False

    @staticmethod
    def move_direction(direction):
        direction_dict = {0: "прямо", 1: "налево", 2: "направо", 3: "разворот"}
        print(f"Автомобиль выполняет движение: {direction_dict.get(direction, 'прямо')}")

    def move(self, distance: Union[int, float]):
        """Движение:
        :param distance - дистанция планируемого движения
        1) текущий километраж назначается стартовым
        2) проверка готовности машины к движению
        2.1 проверка прохождения ТО
        2.2 направление движения
        2.3 проврека необходимости остановки
        2.4 подсчет пройденного пути
        3) при невозможности движения ошибки (отсутствие водителя,
        не запущен двигатель, не пройдено ТО)"""
        try:
            start_mile = self.get_mileage()
            if self.__is_ready_to_move():

                for i in range(distance):
                    if self.check_technical_discussion():
                        self.move_direction(random.randint(0, 10))
                        self.time_to_stop(start_mile)

                        print(f"Машина проехала {start_mile + i + 1} км")
                        self.__mileage += 1
                        time.sleep(0.3)

                    else:
                        raise DoTechnicalDiscussion("Срочно необходимо сделать ТО, "
                                                    "Автомобиль не может продолжить движение")

            print("Машина проехала указанный путь")
            print(f"Вы начали свой путь с пробегом {start_mile} км")
        except(EngineIsNotRunning, DriverNotFoundError) as e:
            print(f"Машина не может ехать, т.к. {e}")

    #  вывод и добалвение через геттер и сеттер
    # def set_driver(self, driver: Driver):
    #     if not isinstance(driver, Driver):
    #         raise DriverTypeError(f"Ожидается тип {Driver}, "
    #                               f"получен {type(driver)}")
    #     self.__driver = driver
    #
    # def get_driver(self):
    #     return self.__driver

    """получение и установка через свойства. вместо геттера и сеттера"""
    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver: Driver):

        if not isinstance(driver, Driver):
            raise DriverTypeError(f"Ожидается тип {Driver}, "
                              f"получен {type(driver)}")
        self.__driver = driver

    def get_mileage(self):
        """Возвращает значение пройденного пути"""
        return self.__mileage

    def _set_mileage(self, mileage: Union[int, float]):
        """установка пройденного километража и проверка на соответствие типа данных"""
        if not isinstance(mileage, (int, float)):
            raise TypeError(f"Ожидается тип данных {int} или {float}, получен {type(mileage)}")
        self.__mileage = mileage

    @staticmethod
    def miles_to_km(mile_count: Union[int, float]) -> Union[int, float]:
        """Перевод миль в километры"""
        return mile_count * 1.609


class Honda(Car):
    brand = "Honda"
    __created_car = 0

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    # print(Car().miles_to_km(40))
    #
    #
    car = Car("бензин", "седан", "автомат", "полный", "люкс", "белый")
    # car_2 = Car("бензин", "седан", "автомат", "полный", "люкс", "черный")
    # honda = Honda("бензин", "седан", "автомат", "полный", "люкс", "белый")
    # honda_2 = Honda("бензин", "седан", "автомат", "полный", "люкс", "черный")


    # print(car.brand)
    # print(car_2.brand)
    # Car.change_brand("Mitsubishi")
    # print(car.brand)
    # print(car_2.brand)
    #
    # print(car._max_speed)
    # print(car_2._max_speed)
    # Car.set_max_speed(200)
    # print(car._max_speed)
    # print(car_2._max_speed)
    #
    #блок работы с защищенными методами
    driver_key = car.get_keys()
    # car.do_technical_discussion()
    car.start_engine(driver_key)
    car.driver = Driver("Иван", 25, 45, "B")
    print(car.driver)

    # блок методов экземпляра

    car._set_mileage(20)
    car.move(45)
    print(car.get_mileage())
    # car.move()
    # print(car)
    # print(car.get_mileage())

    # car._set_mileage(30)
    # print(car.get_mileage())
    # car.move()
    # print(car.get_mileage())
    # car._set_mileage(10)

    #блок сеттеров
    # для чистого геттера и сеттера
    # car.set_driver(Driver("Иван"))
    # print(car.get_driver())





