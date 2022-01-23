from rules import Categories
from typing import Optional


class Driver:
    def __init__(self, name, age: int, rules: Optional[Categories] = None):
        self.name = name
        self.age = age
        self.rules = rules

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age: int):
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
        if not (cat is None):
            self._rules = Categories(self.age, cat)
        else:
            self._rules = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name},{self.age},{self.rules})"

    def __str__(self):
        return f"Водитель {self.name}, возраст {self.age}, права {self.rules}"


if __name__ == '__main__':
    driver_vasya = Driver("Василий", 18)
    driver_ivan = Driver("Иван", 14)

    print(driver_vasya)
    print(driver_ivan)


