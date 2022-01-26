import datetime

from rules import Categories
from typing import Optional

class Driver:
    """
    Класс описывающий среднестатистического водителя
    """
    MAX_MOVE_NOOB_TIME = 120 # максимальное время в пути для новичка 2 ч

    MAX_MOVE_TIME = 360      # максимальная время в пути для любого водителя без перерыва 4 ч

    def __init__(self, name, age: int, rules: Optional[Categories] = None,
                 experience: datetime = datetime.datetime.now(), dist_limit: int = 20):
        """
        :param name: Имя водителя
        :param age: возраст (в годах)
        :param rules: наличие ВУ (объект класса Categories)
        :param experience: наличие стажа (дата выдачи ВУ)
        :param dist_limit: ограничение на максимальное расстояние без отдыха
        """

        self.name = name
        self.age = age
        self.rules = rules
        self.experience = experience
        self.dist_limit = dist_limit

        #  установка "начальных" значений

        self._set_max_allowed_speed_in_counry()  # установка в self._max_country_speed
                                                 # максимально допустимой скорости в стране
        self._set_max_noob_speed()               # установка в self._max_noob_country_speed
                                                 # ограничения максимальной скорости для неопытных водителей в стране
        self._set_test_roll_in_country()         # установка в self._test_roll
                                                 # величины "испытательного" срока для молодых водтителей
        self._set_max_time_behind_wheel()        # установка максимального времени за рулем для всех в
                                                 # _max_time_behind_wheel
        self._set_max_noob_time_behind_wheel()   # установка максимального времени за рулем для неопытных
                                                 # в _max_noob_time_behind_wheel

    def _set_max_time_behind_wheel(self, new_value: int = 360) -> None:
        """
        Установка максимальнгого времени за рулем для всех (без отдыха)
        :param new_value: новое значение в минутах (по умолчанию 360 мин)
        """
        self.__chek_time_of_wheel(new_value)
        self._max_time_behind_wheel = new_value

    def get_max_time_behind_wheel(self) -> int:
        """
        Получение максимальнгого времени за рулем для всех (без отдыха)
        :return: значение в минутах
        """
        return self._max_time_behind_wheel

    def _set_max_noob_time_behind_wheel(self, new_value = 120) -> None:
        """
        установка максимального времени без отдыха за рулем для новичков
        :param new_value: новое значение в минутах (по умолчанию - 120)
        """
        self.__chek_time_of_wheel(new_value)
        self._max_noob_time_behind_wheel = new_value

    def get_max_noob_time_behind_wheel(self) -> int:
        """
        Возвращает максимально допустимое время за рулем для новичка
        :return: максимальное время за рулем в минутах
        """
        return self._max_noob_time_behind_wheel

    @staticmethod
    def __chek_time_of_wheel(value) -> None:
        """
        проверка введенного времени на соответствие
        """
        if not isinstance(value, int):
            raise TypeError('Задайте время целочисленным значением (в минутах)')
        if (value <= 0) or (value >= 24 * 60):
            raise ValueError('Больше суток без перерыва никому ехать нельзя!')

    def _set_test_roll_in_country(self, new_value = 2) -> None:
        """
        установка нового значения "испытательного срока" для молодых водителей
        (по умолчанию - 2 года)
        :param new_value: новое значение в годах
        """
        if not isinstance(new_value, int):
            raise TypeError('Задайте испытательный срок целочисленным значением')
        if (new_value < 0) or (new_value >= 50):
            raise ValueError('Проверьте вводимые для испытательного срока значения!')
        self._test_roll = new_value

    def get_test_roll_in_country(self) -> int:
        """
        возвращает значение испытательного срока в стране
        """
        return self._test_roll

    def get_max_noob_speed(self) -> int:
        """
        возвращает максимально допустимую максимально допустимую скорость
        для неопытных водителей в стране
        """
        return self._max_noob_country_speed

    def _set_max_noob_speed(self, new_value: int = 70):
        """
        устанавливает значение максимальной скорости для неопытных водителей
        (по умолчанию - 70 км/ч)
        :param new_value: новое значение максимальной скорости (км/ч)
        """
        self.__chek_speed_value(new_value)
        self._max_noob_country_speed = new_value

    @staticmethod
    def __chek_speed_value(value) -> None:
        """проверка соответсвия значения скорости"""
        if not isinstance(value, int):
            raise TypeError('Задайте скорость целочисленным значением')
        if value <= 0:
            raise ValueError('Задайте максимальную скорость положительным значением!')

    def get_max_allowed_speed_in_counry(self):
        """
        возвращает максимально допустимую скорость в стране
        """
        return self._max_country_speed

    def _set_max_allowed_speed_in_counry(self, new_value: int = 130):
        """
        устанавливает максимально допустимую скорость в стране
        (по умолчанию = 130 км/ч)
        :param new_value: новое значение максимальной скорости
        """
        self.__chek_speed_value(new_value)
        self._max_country_speed = new_value

    def get_max_allowed_speed(self) -> int:
        """
        Возвращает максимально разрешенную скорость для водителя в зависимости от стажа
        и ограничений в стране
        :return: максимально разрешенная скорость в км/ч
        """
        return self.get_max_noob_speed() if self.experience.days < (self.get_test_roll_in_country() / 365) \
            else self.get_max_allowed_speed_in_counry()

    def get_max_time_in_move(self) -> int:
        """
        Возвращает максимальное время за рулем для водителя в зависимости от стажа установленных ограничений
        :return: время в минутах
        """
        return self.get_max_noob_time_behind_wheel() if self.experience.days < (self.get_test_roll_in_country() / 365) \
            else self.get_max_time_behind_wheel()

    @property
    def experience(self) -> datetime.timedelta:
        """
        возвращает стаж вождения как timedelta между текущей датой и датой выдачи ВУ
        """
        return datetime.datetime.now() - self._experience

    @experience.setter
    def experience(self, start_date: datetime):
        """
        установка даты начала отсчета стажа вождения
        :param start_date: дата выдачи ВУ ( в формате %d.%m.%Y)
        """
        if isinstance(start_date, str):
            start_date += ' 00:00'
            start_date = datetime.datetime.strptime(start_date, '%d.%m.%Y %H:%S')
        if not isinstance(start_date, datetime.date):
            TypeError('введите корректную дату')
        if abs((start_date - datetime.datetime.now()).days) > self.age * 365:
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
        return f"{self.__class__.__name__}({self.name},{self.age},{self.rules}, {self.experience})"

    def __str__(self):
        if self.experience.days // 365 > 0:
            return f"Водитель {self.name}, возраст {self.age}, права {self.rules}, " \
                   f"стаж {self.experience.days // 365} лет"
        elif self.experience.days // 30 > 0:
            return f"Водитель {self.name}, возраст {self.age}, права {self.rules}, " \
                   f"стаж {self.experience.days // 30} месяц(ев)"
        else:
            return f"Водитель {self.name}, возраст {self.age}, права {self.rules}, " \
                   f"стаж {self.experience.days} дней"


if __name__ == '__main__':
    driver_vasya = Driver("Василий", 56, 'М', "01.10.2000")
    driver_ivan = Driver("Иван", 14)

    print(driver_vasya)
    print(driver_vasya.get_max_time_in_move())
    print(driver_vasya.experience)
    print(driver_ivan)
