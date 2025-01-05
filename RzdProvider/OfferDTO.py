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
