import datetime

from rules import Categories
from typing import Optional

class Driver:
    """
    Класс описывающий среднестатистического водителя
    """

    TWO_YEAR = 730           # два года в днях
    MAX_NOOB_SPEED = 70      # максимальная скорость для новичков
    MAX_MOVE_NOOB_TIME = 120 # максимальное время в пути для новичка 2 ч
    MAX_SPEED = 130          # максимальная скорость на территории РФ
    MAX_MOVE_TIME = 360      # максимальная время в пути для любого водителя без перерыва 4 ч

    def __init__(self, name, age: int, rules: Optional[Categories] = None,
                 experience: datetime = datetime.datetime.now()):

        self.name = name
        self.age = age
        self.rules = rules
        self.experience = experience

        self.max_speed = self.get_max_speed()
        self.max_move_time = self.get_max_time_in_move()
        self.max_distance = self.max_speed * (self.max_move_time * 60)

        self._max_country_speed = None

    @property
    def max_allowed_speed_in_counry(self):
        """
        возвращает максимально допустимую скорость в стране
        """
        return self._max_country_speed

    @max_allowed_speed_in_counry.setter
    def _max_allowed_speed_in_counry(self, new_value: int = 130):
        """
        устанавливает максимально допустимую скорость в стране
        :param new_value: новое значение максимальной скорости
        """
        if not isinstance(new_value, int):
            raise TypeError('Задайте скорость целочисленным значением')
        if new_value <= 0:
            raise ValueError('Задайте максимальную скорость положительным значением!')
        self._max_country_speed = new_value

    def get_max_speed(self):
        return self.MAX_NOOB_SPEED if self.experience.day < self.TWO_YEAR else self.MAX_SPEED

    def get_max_time_in_move(self):
        return self.MAX_MOVE_NOOB_TIME if self.experience.day < self.TWO_YEAR else self.MAX_MOVE_TIME

    @property
    def experience(self) -> datetime.timedelta:
        """
        возвращает стаж вождения как timedelta между текущей датой и датой выдачи ВУ
        """
        return (datetime.datetime.now() - self._experience)

    @experience.setter
    def experience(self, start_date: datetime):
        """
        установка даты начала отсчета стажа вождения
        :param start_date: дата выдачи ВУ
        """
        if not isinstance(start_date, datetime):
            TypeError('введите корректную дату')
        if abs(start_date - datetime.datetime.now()) > self.age:
            raise ValueError('Стаж больше возраста?')
        self._experience = start_date

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, age: int):
        """
        установка возраста водителя
        :param age: возраст
        """
        if not isinstance(age, int):
            raise TypeError('Задайте возраст целочисленным значением')
        if age < 0:
            raise ValueError("Возраст должен иметь положительное значение!")
        self._age = age

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, cat: str):
        """
        устаовка категории ВУ для водителя
        :param cat: желаемая категория
        """
        if not (cat is None):
            self._rules = Categories(self.age, cat)
        else:
            self._rules = None


    def __repr__(self):
        return f"{self.__class__.__name__}({self.name},{self.age},{self.rules})"

    def __str__(self):
        return f"Водитель {self.name}, возраст {self.age}, права {self.rules}"


if __name__ == '__main__':
    driver_vasya = Driver("Василий", 18, 'М')
    driver_ivan = Driver("Иван", 14)

    print(driver_vasya)
    print(driver_ivan)
