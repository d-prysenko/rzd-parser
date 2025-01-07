from services.RzdProvider.OfferDTO import Offer
from time import struct_time

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



        

