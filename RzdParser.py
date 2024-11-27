from RzdApiClient import *
from Train import *
from TgClient import TgClient
import urllib.parse
import json
import requests
import time
import datetime

class RzdParser:
    rzd_client = RzdApiClient()
    tg_client = TgClient()

    RETRY_COUNT = 3

    def handleOffers(self, datetime, origin, destination):

        try_number = 0
        last_error = None

        while try_number < self.RETRY_COUNT:
            try:
                try_number += 1

                response = self.rzd_client.getTrains(origin, destination, datetime)

                last_error = None

                if (response.status_code != 200):
                    raise ValueError('status code is ' + str(response.status_code))

                break
            except e:
                time.sleep(1)
                last_error = e
                print(e)

        if (last_error != None):
            self.tg_client.send_error_notification(last_error)

            return

        json_data = json.loads(response.text)

        all_trains = {}
        available_trains = {}

        for train in json_data['Trains']:

            train_number = train['TrainNumber']
            departure_datetime = time.strptime(train['DepartureDateTime'], '%Y-%m-%dT%H:%M:%S')
            arrival_datetime = time.strptime(train['ArrivalDateTime'], '%Y-%m-%dT%H:%M:%S')

            # datetime filter

            # if (departure_datetime.tm_hour < 15 or (departure_datetime.tm_hour == 15 and departure_datetime.tm_min < 30)):
            #     continue

            # if (departure_datetime.tm_hour < 8):
            #     continue

            # if (arrival_datetime.tm_mday > 30):
            #     continue

            # if (arrival_datetime.tm_mday == 30 and arrival_datetime.tm_hour > 12):
            #     continue

            # if (int(train['TripDuration']) / 60 > 19.5):
            #     continue

            # if (train_number != '035А' and train_number != '035A'):
            #     continue

            all_trains[train_number] = train['DepartureDateTime']

            if (self._is_in_db(train_number, train['DepartureDateTime'])):
                print(train_number + ' already sent')
                continue

            db_train = Train()
            db_train.train_number = train_number
            db_train.departure_datetime = train['DepartureDateTime']
            db_train.save()

            message = '*Поезд ' + train_number + '*\n' + time.strftime('%d.%m %H:%M', departure_datetime) + ' - ' + time.strftime('%d.%m %H:%M', arrival_datetime) + '\n'

            messages = []

            tickets_count = 0

            tickets_count_in_groups = {}
            tickets_costs_in_groups = {}

            for group in train['CarGroups']:
                if (group['HasPlacesForDisabledPersons']):
                    continue

                if (group['CarType'] == 'Baggage'):
                    continue

                if (group['MaxPrice'] <= 1):
                    continue

                is_pet_class_found = False
                for service_class in group['ServiceClasses']:
                    print('Поезд' + train_number + ' ' + service_class)
                    if service_class == '3Б' or service_class == '3Д' or service_class == '3У':
                        is_pet_class_found = True
                
                if (not is_pet_class_found):
                    continue

                # if you have 1 ticket and need to find 1 more on the same train

                # if (train_number == '146Э' and group['MinPrice'] < 2700):
                #     temp_message = '*Билет на тот же поезд*\n' + message + str(group['MinPrice']) + '₽'
                #     messages.append(temp_message)

                #     continue

                tickets_count += group['TotalPlaceQuantity']

                if group['CarTypeName'] not in tickets_count_in_groups:
                    tickets_count_in_groups[group['CarTypeName']] = 0
                
                if group['CarTypeName'] not in tickets_costs_in_groups:
                    tickets_costs_in_groups[group['CarTypeName']] = []

                tickets_count_in_groups[group['CarTypeName']] += group['TotalPlaceQuantity']
                tickets_costs_in_groups[group['CarTypeName']].append(group['MinPrice'])

            # count and price filter

            # if (tickets_count >= 3 and min(tickets_costs_in_groups[key]) < 3000):
            #     temp_message = '*Найдено три или более билетов на поезд*\n' + message + '\n'

            #     for key, value in tickets_count_in_groups.items():
            #         temp_message += key + ': ' + str(value) + ' шт., от ' + str(min(tickets_costs_in_groups[key])) + '₽\n'

            #     messages.append(temp_message)
            
            available_price_group = {}

            for key, value in tickets_count_in_groups.items():
                min_group_cost = min(tickets_costs_in_groups[key])
                
                if (min_group_cost < 4500):
                    available_price_group[key] = min_group_cost

            if (len(available_price_group) > 0):
                train_info_header = message
                groups_info = ''
                
                for key, value in available_price_group.items():
                    groups_info += key + ': ' + str(tickets_count_in_groups[key]) + ' шт., от ' + str(available_price_group[key]) + '₽\n'

                message_to_user = train_info_header + groups_info

                available_trains[train_number] = train['DepartureDateTime']

                print(message_to_user)

                self.tg_client.send_notification(message_to_user)

        non_available_trains = all_trains.keys() - available_trains.keys()

        for key in non_available_trains:
            if (self._is_in_db(key, all_trains[key])):
                self._delete_unavailable(key, all_trains[key])

    def _is_in_db(self, number, departure_datetime):
        return Train.select().where(Train.train_number == number and Train.departure_datetime == departure_datetime).count() > 0  

    def _delete_unavailable(self, number, departure_datetime):
        return Train.get(Train.train_number == number and Train.departure_datetime == departure_datetime).delete_instance()
