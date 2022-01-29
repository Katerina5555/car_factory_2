
class Categories:
    __CAT = {'A': 18,    # Мотоциклы
             "A1": 16,   # Легкие мотоциклы
             "B": 18,    # Легковые автомобили, небольшие грузовики(до 3, 5 тонн)
             "BE": 18,   # Легковые автомобили с прицепом
             "В1": 18,   # Трициклы
             "C": 18,    # Грузовые автомобили(от  3, 5 тонн)
             "CE": 21,   # Грузовые автомобили с прицепом
             'С1': 18,   # Средние грузовики(от 3, 5  до 7, 5 тонн)
             'С1E': 18,  # Средние грузовики с прицепом
             'D': 21,    # Автобусы
             "DE": 21,   # Aвтобусы с    прицепом
             "D1": 21,   # Небольшие автобусы
             "D1E": 21,  # Небольшие автобусы с прицепом
             "М": 16,    # Мопеды
             "Tm": 21,   # Трамваи
             "Tb": 21    # Троллейбусы
             }

    def __init__(self, age_: int, cat_: str):

        self.age = age_
        self.category = cat_

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age_: int):
        if not isinstance(age_, int):
            raise TypeError('Задайте возраст целочисленным значением')

        if age_ < 0:
            raise ValueError("Возраст должен иметь положительное значение!")

        self._age = age_

    @property
    def category(self):
        return self._cat

    @category.setter
    def category(self, cat_: str):
        """
        Установка категории в зависимости от возраста водителя
        :param cat_: желаемая категория
        :param age: возраст водителя
        """
        if not isinstance(cat_, str):
            raise TypeError('Категория задается строковым значением')

        if not (cat_ in self.__CAT):
            raise ValueError('Нет такой категории!')

        if self.age < self.__CAT[cat_]:
            raise ValueError('Ваш водитель еще молод! Пусть немного постареет!')

        self._cat = cat_

    def __repr__(self):
        return f'{self.__class__.__name__}({self.age},{self.category})'

    def __str__(self):
        return f'Возраст - {self.age}, категория {self.category}'


class Rules:

    def __init__(self, category: str):

        self.category = Categories(self.driver.age, category)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.driver},{self.category})'

    def __str__(self):
        return f'Водитель {self.driver.name}, возраст - {self.driver.age}, категория {self.category}'