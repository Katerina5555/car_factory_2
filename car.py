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
    brand = None
    _max_speed = 180
    __created_car = 0

    def __init__(self, engine_type=None, body_type=None, gear_type=None,
                 drive_type=None, configuration=None, color=None, object_category=None):

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
        print(f"Создано {cls.__created_car} машина класса {cls.__name__}")
        return super().__new__(cls)

    @classmethod
    def change_brand(cls, new_brand):
        cls.brand = new_brand

    @classmethod
    def _set_max_speed(cls, max_speed):
        if not isinstance(max_speed, (int, float)):
            raise TypeError(
                f'Ожидается тип {int} или {float}, получен {type(max_speed)}')
        cls._max_speed = max_speed

    @classmethod
    def __append_new_car_counter(cls):
        cls.__created_car += 1

    def start_engine(self, key):
        if self.__check_keys(key):
            self.__status_engine = True
            print('Машина завелась')
        else:
            print('Крутится стартер')

    def __is_ready_move(self):
        if not self.__status_engine:
            raise EngineIsNotRunning("двигатель не запущен")
        if self.__driver is None:
            raise DriverNotFoundError("водитель не найден")

        return True

    # def __is_ready_move(self):
    #     if not self.__status_engine:
    #         raise EngineIsNotRunning("двигатель не запущен")
    #     if self.__driver is None:
    #         raise DriverNotFoundError("водитель не найден")
    #     if self.driver.rules is None:
    #         raise DriverNoRules("без прав нельзя!")
    #     if self.__object_category != self.driver.rules:
    #         raise DriverNoRules("права водителя не подходят для этого ТС!")

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

    def move(self, distance=10):
        try:
            if self.__is_ready_move():
                for i in range(distance):
                    if self.check_technical_discussion():
                        self.move_direction(random.randint(0, 10))
                        print(f'Машина проехала {i + 1} км.')
                        self.__mileage += 1
                        time.sleep(0.1)

                        if self.__mileage % 20 == 0:
                            a = 3
                            print(f'Вам необходимо отдохнуть. Вы можете продолжить движение через {a} минут(ы)')
                            time.sleep(a)

                    else:
                         raise DoTechnicalDiscussion("Срочно необходимо сделать ТО")
            print('Машина проехала указанный путь')
        except (EngineIsNotRunning, DriverNotFoundError) as e:
            print(f"Машина не может поехать, т.к. {e}")


    @staticmethod
    def move_direction(direction):
        direction_dict = {0: "прямо", 1: "налево", 2: "направо", 3: "разворот"}
        print(f"Автомобиль выполняет движение: {direction_dict.get(direction, 'прямо')}")

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver: Driver):
        if not isinstance(driver, Driver):
            raise DriverTypeError(
                f"Ожидается тип {Driver}, получен {type(driver)}")
        self.__driver = driver

    def get_mileage(self):
        return self.__mileage

    def _set_mileage(self, mileage):
        if not isinstance(mileage, (int, float)):
            raise TypeError(
                f'Ожидается тип {int} или {float}, получен {type(mileage)}')
        self.__mileage = mileage

    def check_technical_discussion(self) -> bool:
        if self.__mileage - self.__last_to == 40:
            return False
        elif self.__mileage - self.__last_to == 20:
            print(f"Необходимо сделать ТО через 10 км")
        elif self.__mileage - self.__last_to == self.__service_interval:
            print(f"Сейчас необходимо сделать ТО")
        return True

    def do_technical_discussion(self):
        self.__last_to = self.__mileage
        print("Очередное ТО пройден")

    def autostart_engine(self):
        if not self.__status_engine:
            self.__status_engine = True
            return True
        else:
            EngineIsRunning("двигатель уже запущен")
            return False


class Honda(Car):
    brand = "Honda"
    __created_car = 0

    def __init__(self):

        super().__init__()


if __name__ == '__main__':
    # pass
    car = Car('бензин', 'седан', 'автомат', 'полный', 'люкс', 'белый')
    # driver_key = car.get_keys()
    # car.start_engine(driver_key)

    start_time = datetime.time(15, 47, 0, 0)
    while True:
        a = datetime.datetime.now().time()
        print(a)
        print(start_time)
        if a > start_time:
            print(car.autostart_engine())
            break
