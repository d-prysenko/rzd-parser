import sys, getopt, time, math
from RzdProvider.RzdProvider import RzdProvider
from ApiClients.RzdApiClient import RzdCity
# from model.Train import create_tables
from Filters.Filters import BaseFilter, Filters
from Filters.OfferFilters import OnlyLowerPlacesFilter, PriceFilter, WithPetsFilter
from Filters.TrainFilters import TripDurationLowerThan
from ApiClients.TgClient import TgClient
from RzdProvider.TrainDTO import Train

class Query:
    date: str
    origin: RzdCity
    dest: RzdCity
    filters: list[BaseFilter]

    def __init__(self, date: str, origin: RzdCity, dest: RzdCity, filters: list[BaseFilter]):
        self.date = date
        self.origin = origin
        self.dest = dest
        self.filters = filters


rzd_provider = RzdProvider()
tg_client = TgClient()


def main(argv):

    # opts, _ = getopt.getopt(argv,":i")

    # if ('-i', '') in opts:
    #     print('Creating tables..')
    #     create_tables()

    default_filters: list[BaseFilter] = [
        PriceFilter(4000),
        WithPetsFilter(),
        TripDurationLowerThan(14 * 60),
        OnlyLowerPlacesFilter()
    ]

    queries = [
        Query("2025-01-07T00:00:00", RzdCity.Voronezh, RzdCity.Moscow, default_filters),
        Query("2025-01-08T00:00:00", RzdCity.Voronezh, RzdCity.Moscow, default_filters),
    ]

    for query in queries:
        try:
            handle_query(query.date, query.origin, query.dest, query.filters)
        except ValueError as e:
            tg_client.send_error_notification(e.args)
            
        time.sleep(1)


# def previous_same(train: Train):
#     prev = get_previous(train.number)

#     if prev == None:
#         return False
    
    
def handle_query(date: str, origin: RzdCity, dest: RzdCity, filters: list[BaseFilter]):
    trains = rzd_provider.get_trains(date, origin, dest)

    trains_filters = Filters(trains)

    for filter in filters:
        trains_filters.add(filter)

    filtered_trains = trains_filters.filter().aggregate()

    for train in filtered_trains:
        # if previous_same(train):
        #     continue

        msg = format_train_for_tg(train)
        tg_client.send_notification(msg)
        print(msg)


def format_train_for_tg(train: Train):
    msg = '*Поезд ' + train.number + '*\n' 
    msg += time.strftime('%d.%m %H:%M', train.departure_time) + ' - ' + time.strftime('%d.%m %H:%M', train.arrival_time) + '\n'
    msg += 'В пути: ' + str(math.floor(train.trip_duration / 60.0)) + ':' + "{:02d}".format(int(train.trip_duration) % 60) + '\n'

    for offer in train.offers:
        msg += offer.car_type_name + ': ' + str(offer.place_quantity) + '(' + str(offer.lower_place_quantity) + ') шт., '
        if (offer.min_price == offer.max_price):
            msg += "{:.2f}".format(offer.min_price / 1000) + 'k\n'
        else:
            msg += "{:.2f}".format(offer.min_price / 1000) + 'k - ' + "{:.2f}".format(offer.max_price / 1000) + 'k\n'

    return msg



if __name__ == "__main__":
    main(sys.argv[1:])


# offer( chat_id train_number min_price place_quantity lower_place_quantity )

# if (not in_db(chat_id, train_number) or
#     (offer=get_offer(chat_id, train_number)) and (min_price < offer.min_price or lower_places != 0 and offer.lower_places == 0))
#     send_notification()
#     update_offer(offer, min_price, lower_places)


# если не купил билет
#   присылать уведомление один раз
#   присылать уведомление если минимальная цена снизилась или появилось нижнее место
