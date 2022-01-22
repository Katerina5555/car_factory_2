import time
import uuid
from driver import Driver


class DriverTypeError(Exception):
    pass


class EngineIsNotRunning(Exception):
    pass


class DriverNotFoundError(Exception):
    pass


class Car:
    brand = None
    _max_speed = 180
    __created_car = 0

    def __init__(self, engine_type=None, body_type=None, gear_type=None,
                 drive_type=None, configuration=None, color=None):

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

    def start_engine(self):
        self.__status_engine = True

    def __is_ready_move(self):
        if not self.__status_engine:
            raise EngineIsNotRunning("двигатель не запущен")
        if self.__driver is None:
            raise DriverNotFoundError("водитель не найден")

        return True

    def move(self, distance=10):
        try:
            if self.__is_ready_move():
                for i in range(distance):
                    print(f'Машина проехала {i + 1} км.')
                    self.__mileage += 1
                    time.sleep(0.3)
            print('Машина проехала указанный путь')
        except (EngineIsNotRunning, DriverNotFoundError) as e:
            print(f"Машина не может поехать, т.к. {e}")

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


class Honda(Car):
    brand = "Honda"
    __created_car = 0

    def __init__(self):

        super().__init__()


if __name__ == '__main__':
    pass
    # car = Car('бензин', 'седан', 'автомат', 'полный', 'люкс', 'белый')
    # car_2 = Car('бензин', 'седан', 'автомат', 'полный', 'люкс', 'черный')
    #
    # honda1 = Honda('бензин', 'седан', 'автомат', 'полный', 'люкс', 'черный')
    # honda2 = Honda('бензин', 'седан', 'автомат', 'полный', 'люкс', 'черный')
    #
    # Car.change_brand("Kia")
    #
    # print(honda1.brand)

    # print(car.brand)
    # print(car_2.brand)
    # Car.change_brand("Nissan")
    # print(car.brand)
    # print(car_2.brand)

    # print(car._max_speed)
    # print(car_2._max_speed)
    # Car._set_max_speed(190)
    # print(car._max_speed)
    # print(car_2._max_speed)




    # Блок работы с защищёнными методами
    # car.start_engine()
    # car.driver = Driver('Иван')
    # car.driver = Driver('Иван')
    # # Блок работы с методами
    # car.move()
    # print(car.get_mileage())
    # car.move()
    # print(car.get_mileage())
    #
    # car._set_mileage(30)
    # print(car.get_mileage())
    # car.move()
    # print(car.get_mileage())
    # car._set_mileage(10)
    # print(car.get_mileage())

    # Блок сеттеров
    # car.driver = Driver('Иван')
    # print(car.driver)
    # car.set_driver(Driver('Иван'))
    # print(car.get_driver())
