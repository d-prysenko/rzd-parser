import abc
from enum import Enum
from services.RzdProvider.TrainDTO import Train, Offer

class FilterType(Enum):
    Train = 1
    Offer = 2

class BaseFilter(abc.ABC):
    @abc.abstractmethod
    def get_type(self) -> FilterType:
        """Filter type"""

    @abc.abstractmethod
    def apply(self, entity) -> bool:
        """Apply filter"""

class TrainFilter(BaseFilter):
    """Base Abstract Train Filter"""

    def get_type(self):
        return FilterType.Train

    @abc.abstractmethod
    def apply(self, train: Train) -> bool:
        """Apply filter"""

class OfferFilter(BaseFilter):
    """Base Abstract Offer Filter"""

    def get_type(self):
        return FilterType.Offer

    @abc.abstractmethod
    def apply(self, offer: Offer) -> bool:
        """Apply filter"""


class Filters:
    offer_filters: list[OfferFilter] = []
    train_filters: list[TrainFilter] = []

    def __init__(self, trains: list[Train]):
        self.trains = trains

    def add(self, filter: BaseFilter):

        if (filter.get_type() == FilterType.Offer):
            self.add_offer_filter(filter)
        elif (filter.get_type() == FilterType.Train):
            self.add_train_filter(filter)

        return self
    
    def add_offer_filter(self, filter):
        self.offer_filters.append(filter)

    def add_train_filter(self, filter):
        self.train_filters.append(filter)

    def filter(self):
        result: list[Train] = []

        for train in self.trains:

            train_filter_passed = self._filter_apply(train, self.train_filters)

            if (not train_filter_passed):
                continue

            filtered_offers = []

            for offer in train.offers:

                offer_filter_passed = self._filter_apply(offer, self.offer_filters)
                
                if (not offer_filter_passed):
                    continue

                filtered_offers.append(offer)
            
            if (len(filtered_offers) > 0):
                train_with_filtered_offers = Train().copy(train)
                train_with_filtered_offers.offers = filtered_offers

                result.append(train_with_filtered_offers)

        self.trains = result

        return self

    def _filter_apply(self, entity, filters: list[BaseFilter]):
        filter_passed = True

        for filter in filters:
            if (not filter.apply(entity)):
                filter_passed = False
                break

        return filter_passed
        
    
    def aggregate(self):
        result: list[Train] = []

        for train in self.trains:
            offers_map: dict[str, Offer] = {}

            for offer in train.offers:

                type_id = offer.car_type_name

                if (offer.lower_place_quantity > 0):
                    type_id += '_lower'

                if (type_id in offers_map.keys()):
                    offers_map[type_id].lower_place_quantity += offer.lower_place_quantity
                    offers_map[type_id].place_quantity += offer.place_quantity
                    offers_map[type_id].min_price = min(offers_map[type_id].min_price, offer.min_price)
                    offers_map[type_id].max_price = max(offers_map[type_id].max_price, offer.max_price)
                else:
                    offers_map[type_id] = Offer().copy(offer)
                    
            aggregated_train = Train().copy(train)

            for offer in offers_map.values():            
                aggregated_train.offers.append(offer)

            result.append(aggregated_train)

        self.trains = result

        return result








