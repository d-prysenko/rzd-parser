from time import struct_time

class Offer:
    def __init__(self):
        self.service_class: str = ""
        self.place_quantity: int = 0
        self.lower_place_quantity: int = 0
        self.min_price: float = 0
        self.max_price: float = 0
        self.car_type_name: str = ""

    def copy(self, other_offer):
        self.service_class = other_offer.service_class
        self.place_quantity = other_offer.place_quantity
        self.lower_place_quantity = other_offer.lower_place_quantity
        self.min_price = other_offer.min_price
        self.max_price = other_offer.max_price
        self.car_type_name = other_offer.car_type_name

        return self

class Train:
    def __init__(self):
        self.number: str = ""
        self.display_number: str = ""
        
        self.departure_time: struct_time = struct_time([0,0,0,0,0,0,0,0,0])
        self.arrival_time: struct_time = struct_time([0,0,0,0,0,0,0,0,0])
        self.trip_duration: float = 0

        self.offers: list[Offer] = []

    def copy(self, other_train):
        self.number = other_train.number
        self.display_number = other_train.display_number
        self.departure_time = other_train.departure_time
        self.arrival_time = other_train.arrival_time
        self.trip_duration = other_train.trip_duration

        return self



        

