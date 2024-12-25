import sys, getopt, time
from RzdParser import RzdParser
from RzdApiClient import RzdCity
# from model.Train import create_tables
from Filters import DepartureTimeFilter, Filters, OnlyLowerPlacesFilter, PriceFilter, WithPetsFilter
from TgClient import TgClient


queries = [
    {"chat_id", "2025-01-17T00:00:00", RzdCity.Moscow, RzdCity.Spb, "filters"},
    {"chat_id", "2025-01-06T00:00:00", RzdCity.Moscow, RzdCity.Voronezh, "filters"},
    {"chat_id", "2025-01-16T00:00:00", RzdCity.Moscow, RzdCity.Spb, "filters"},
]


def main(argv):

    # opts, _ = getopt.getopt(argv,":i")

    # if ('-i', '') in opts:
    #     print('Creating tables..')
    #     create_tables()

    parser = RzdParser()
    tg_client = TgClient()
    
    # parser.handleOffers("2024-09-01T00:00:00", RzdCity.Voronezh, RzdCity.Moscow)
    # time.sleep(1)
    # parser.getTrains("2024-12-29T00:00:00", RzdCity.Moscow, RzdCity.Voronezh)
    trains = parser.get_trains("2025-01-16T00:00:00", RzdCity.Moscow, RzdCity.Spb)
    # trains = parser.get_trains("2024-12-29T00:00:00", RzdCity.Moscow, RzdCity.Voronezh)

    filtered_trains = Filters(trains) \
        .add(PriceFilter(5000)) \
        .add(WithPetsFilter()) \
        .filter() \
        .aggregate()



    print(filtered_trains)

    for train in filtered_trains:
        msg = '*Поезд ' + train.display_number + '*\n' + time.strftime('%d.%m %H:%M', train.departure_time) + ' - ' + time.strftime('%d.%m %H:%M', train.arrival_time) + '\n'
        for offer in train.offers:
            msg += offer.car_type_name + ': ' + str(offer.place_quantity) + '(' + str(offer.lower_place_quantity) + ') шт., ' + str(offer.min_price) + '₽ - ' + str(offer.max_price) + '₽\n'
        tg_client.send_notification(msg)

    # time.sleep(1)
    # parser.handleOffers("2024-07-09T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-10T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-11T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-12T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-13T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-14T00:00:00")


if __name__ == "__main__":
    main(sys.argv[1:])


# offer( chat_id train_number min_price lower_places )

# if (not in_db(chat_id, train_number) or
#     (offer=get_offer(chat_id, train_number)) and (min_price < offer.min_price or lower_places != 0 and offer.lower_places == 0))
#     send_notification()
#     update_offer(offer, min_price, lower_places)


# если не купил билет
#   присылать уведомление один раз
#   присылать уведомление если минимальная цена снизилась или появилось нижнее место
