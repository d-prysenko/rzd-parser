from HttpClient import HttpClient
from enum import Enum

class RzdCity(Enum):
    Moscow = "2000000"
    Voronezh = "2014000"
    Spb = "2004000"

class RzdApiClient:
    http_client = HttpClient()

    def get_trains(self, origin, destination, date):
        payload = {
            'CarGrouping': "DontGroup",
            'CarIssuingType': "All",
            'DepartureDate': date,
            'Destination': destination.value,
            'GetByLocalTime': True,
            'Origin': origin.value,
            'SpecialPlacesDemand': "StandardPlacesAndForDisabledPersons",
            'TimeFrom': 0,
            'TimeTo': 24,
        }

        return self.http_client.post('https://ticket.rzd.ru/apib2b/p/Railway/V1/Search/TrainPricing?service_provider=B2B_RZD', payload)