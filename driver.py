from rules import Categories

class Driver:
    def __init__(self, name: str, experience: int,  age: int, rules: Categories.category = None):
        self.name = name
        self.experience = experience
        self.age = age
        self.rules = rules

    def experience(self, experience: int):
        return self.experience

    def age(self, age: int):
        return self.age
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
        return f"{self.__class__.__name__}({self.name}, {self.experience}, {self.age}" \
               f"{self.rules.category}))"

    def __str__(self):
        return f"Водитель {self.name}, стаж вождения {self.experience} лет, возраст {self.age}," \
               f" права категории {self.rules.category}"




if __name__ == '__main__':


    driver_vasya = Driver("Василий", 20, 25, "B")
    driver_ivan = Driver("Иван", 25, 29, "B")


    print(driver_vasya)
    print(driver_ivan)