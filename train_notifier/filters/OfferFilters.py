from filters.Filters import OfferFilter


class PriceFilter(OfferFilter):
    """Цена"""

    def __init__(self, price: float):
        super().__init__()
        self.price = price

    def apply(self, offer):
        return offer.min_price < self.price
    

class WithPetsFilter(OfferFilter):
    """Проезд с животными"""

    def __init__(self):
        super().__init__()

    def apply(self, offer):
        return offer.service_class in [
            '3Б', '3Д', '3У',
            '2К', '2У', '2Л', '2Н', '2Д', '2Э', '2Ф', '2Б',
            '2А',
            '2В', '2Ж', '3Ж', '1В',
            '3О', '3Р',
            '1Э', '1Ф', '1У', '1Л', '1Е', '1Б',
            '1А', '1И', '1М'
        ]


class OnlyLowerPlacesFilter(OfferFilter):
    """Только нижние места"""

    def __init__(self):
        super().__init__()

    def apply(self, offer):
        return offer.lower_place_quantity > 0
