from ApiClients.RzdApiClient import RzdApiClient
import json
import requests
import time
from RzdProvider.TrainDTO import Train, Offer



class RzdProvider:
    rzd_client = RzdApiClient()

    RETRY_COUNT = 3
    
    """Need to prevent api errors/limits"""
    def _get_trains_from_api(self, origin, destination, datetime):
        try_number = 0
        last_error = None

        while try_number < self.RETRY_COUNT:
            try:
                try_number += 1

                response = self.rzd_client.get_trains(origin, destination, datetime)

                if (response.status_code != 200):
                    raise ValueError('status code is ' + str(response.status_code))

                break
            except requests.exceptions.RequestException as e:
                last_error = e.strerror
            except ValueError as e:
                last_error = e.args
            except:
                last_error = 'unknown error'
        
        if (try_number == self.RETRY_COUNT and last_error != None):
            raise ValueError(last_error)

        return response

    def get_trains(self, datetime, origin, destination):
        response = self._get_trains_from_api(origin, destination, datetime)

        json_data = json.loads(response.text)

        if ('errorInfo' in json_data):
            raise ValueError(json_data['errorInfo']['Message'])

        trains: list[Train] = []

        for json_train in json_data['Trains']:

            train = Train()
            train.number = json_train['TrainNumber']
            train.display_number = json_train['DisplayTrainNumber']
            train.departure_time = time.strptime(json_train['DepartureDateTime'], '%Y-%m-%dT%H:%M:%S')
            train.arrival_time = time.strptime(json_train['ArrivalDateTime'], '%Y-%m-%dT%H:%M:%S')
            train.trip_duration = json_train['TripDuration']

            for group in json_train['CarGroups']:
                if (group['HasPlacesForDisabledPersons']):
                    continue

                if (group['CarType'] == 'Baggage'):
                    continue

                if (group['MaxPrice'] <= 1):
                    continue

                offer = Offer()
                offer.min_price = group['MinPrice']
                offer.max_price = group['MaxPrice']
                offer.place_quantity = group['TotalPlaceQuantity']
                offer.lower_place_quantity = group['LowerPlaceQuantity']
                offer.service_class = group['ServiceClasses'][0] or ''
                offer.car_type_name = group['CarTypeName']

                train.offers.append(offer)
            
            if (len(train.offers) > 0):
                trains.append(train)
        
        return trains
