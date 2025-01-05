import time
from Filters.Filters import TrainFilter


class DepartureTimeFilter(TrainFilter):
    """Время выезда"""

    def __init__(self, time_from: str, time_to: str = '23:59'):
        super().__init__()

        _time_from = time.strptime(time_from, '%H:%M')
        _time_to = time.strptime(time_to, '%H:%M')

        self.time_from = _time_from.tm_hour * 60 + _time_from.tm_min
        self.time_to = _time_to.tm_hour * 60 + _time_to.tm_min

    def apply(self, train):

        departure_time = train.departure_time.tm_hour * 60 + train.departure_time.tm_min

        return departure_time >= self.time_from and departure_time <= self.time_to


class TripDurationLowerThan(TrainFilter):
    """Время поездки"""

    def __init__(self, minutes: float):
        super().__init__()
        self.trip_duration = minutes

    def apply(self, train):
        return train.trip_duration < self.trip_duration


class TrainNumberEqual(TrainFilter):
    """Номер поезда равен"""

    def __init__(self, train_number: str):
        super().__init__()
        self.train_number = train_number

    def apply(self, train):
        return str.capitalize(train.display_number) == str.capitalize(self.train_number)


class TrainNumberNotEqual(TrainFilter):
    """Номер поезда не равен"""

    def __init__(self, train_number: str):
        super().__init__()
        self.train_number = train_number

    def apply(self, train):
        return str.capitalize(train.display_number) != str.capitalize(self.train_number)

