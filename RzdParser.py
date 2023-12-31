from RzdApiClient import *
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

    def handleOffers(self):
        
        try_number = 0
        last_error = None

        while try_number < self.RETRY_COUNT:
            try:
                try_number += 1

                response = self.rzd_client.getTrains(RzdCity.Moscow, RzdCity.Voronezh, "2023-12-29T00:00:00")

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

        for train in json_data['Trains']:

            train_number = train['TrainNumber']
            departure_datetime = time.strptime(train['DepartureDateTime'], '%Y-%m-%dT%H:%M:%S')
            arrival_datetime = time.strptime(train['ArrivalDateTime'], '%Y-%m-%dT%H:%M:%S')

            # datetime filter

            if (departure_datetime.tm_hour < 15 or (departure_datetime.tm_hour == 15 and departure_datetime.tm_min < 30)):
                continue

            if (arrival_datetime.tm_mday > 30):
                continue

            if (arrival_datetime.tm_mday == 30 and arrival_datetime.tm_hour > 12):
                continue

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

                # if you have 1 ticket and need to find 1 more on the same train

                if (train_number == '777А'):
                    temp_message = '*Билет на тот же поезд*\n' + message + str(group['MinPrice']) + '₽'
                    messages.append(temp_message)

                    continue

                tickets_count += group['TotalPlaceQuantity']

                if group['CarTypeName'] not in tickets_count_in_groups:
                    tickets_count_in_groups[group['CarTypeName']] = 0
                
                if group['CarTypeName'] not in tickets_costs_in_groups:
                    tickets_costs_in_groups[group['CarTypeName']] = []

                tickets_count_in_groups[group['CarTypeName']] += group['TotalPlaceQuantity']
                tickets_costs_in_groups[group['CarTypeName']].append(group['MinPrice'])

            # count and price filter

            if (tickets_count >= 3 and min(tickets_costs_in_groups[key]) < 3000):
                temp_message = '*Найдено три или более билетов на поезд*\n' + message + '\n'

                for key, value in tickets_count_in_groups.items():
                    temp_message += key + ': ' + str(value) + ' шт., от ' + str(min(tickets_costs_in_groups[key])) + '₽\n'

                messages.append(temp_message)

            for msg in messages:
                print(msg)

                self.tg_client.send_notification(msg)
            
