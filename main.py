import sys, getopt, time, math
import logging
from RzdProvider.RzdProvider import RzdProvider
from ApiClients.RzdApiClient import RzdCity
from Settings import Settings
from model.Notification import create_tables, create_notification, find_notification, Notification, notification_exists, update_notification, select_notifications_by_query_id
from Filters.Filters import BaseFilter, Filters
from Filters.OfferFilters import OnlyLowerPlacesFilter, PriceFilter, WithPetsFilter
from Filters.TrainFilters import TripDurationLowerThan
from ApiClients.TgClient import TgClient
from RzdProvider.TrainDTO import Train, Offer

class Query:
    query_id: int
    chat_id: str
    date: str
    origin: RzdCity
    dest: RzdCity
    filters: list[BaseFilter]

    def __init__(self, query_id: int, chat_id: str, date: str, origin: RzdCity, dest: RzdCity, filters: list[BaseFilter]):
        self.query_id = query_id
        self.chat_id = chat_id
        self.date = date
        self.origin = origin
        self.dest = dest
        self.filters = filters


rzd_provider = RzdProvider()
tg_client = TgClient()
logger = logging.getLogger()


def main(argv):
    logging.basicConfig(filename='bot.log', level=logging.INFO, format="%(asctime)s %(module)s %(levelname)s %(message)s")

    opts, _ = getopt.getopt(argv,":i")

    if ('-i', '') in opts:
        print('Creating tables..')
        create_tables()

    default_filters: list[BaseFilter] = [
        PriceFilter(4000),
        WithPetsFilter(),
        TripDurationLowerThan(14 * 60),
        OnlyLowerPlacesFilter()
    ]

    # just to not share chat_id in public repo
    chat_id = Settings().get('target_chat_id')

    queries = [
        Query(1, chat_id, "2025-01-07T00:00:00", RzdCity.Voronezh, RzdCity.Moscow, default_filters),
        Query(2, chat_id, "2025-01-08T00:00:00", RzdCity.Voronezh, RzdCity.Moscow, default_filters),
    ]

    for query in queries:
        try:
            handle_query(query)
        except ValueError as e:
            logger.error(e.args)
            tg_client.send_error_notification(e.args)
            
        time.sleep(1)

    
    
def handle_query(query: Query):
    trains = rzd_provider.get_trains(query.date, query.origin, query.dest)

    trains_filters = Filters(trains)

    for filter in query.filters:
        trains_filters.add(filter)

    filtered_trains = trains_filters.filter().aggregate()

    for train in filtered_trains:
        msg = format_train_for_tg(train)
        print(msg)

    remove_notifications_for_not_presented(filtered_trains, query)

    filtered_trains = remove_offers_that_not_changed(filtered_trains, query)

    create_or_update_notifications(filtered_trains, query)

    print('\n\nsending')

    for train in filtered_trains:
        msg = format_train_for_tg(train)
        tg_client.send_notification(query.chat_id, msg)
        print(msg)

    print('\nend.')


def remove_offers_that_not_changed(trains: list[Train], query: Query):
    result: list[Train] = []

    for train in trains:
        offers: list[Offer] = []

        for offer in train.offers:
            if not notification_exists(
                query.chat_id,
                query.query_id,
                train.display_number,
                format_time(train.departure_time),
                offer.car_type_name,
                offer.min_price,
                offer.place_quantity,
                offer.lower_place_quantity):
                offers.append(offer)

        if (len(offers) > 0):
            train_with_filtered_offers = Train().copy(train)
            train_with_filtered_offers.offers = offers

            result.append(train_with_filtered_offers)

    return result

def create_or_update_notifications(trains: list[Train], query: Query):
    for train in trains:
        for offer in train.offers:
            notification = find_notification(query.chat_id, query.query_id, train.display_number, format_time(train.departure_time), offer.car_type_name)

            if notification == None:
                create_notification(
                    query.chat_id,
                    query.query_id,
                    train.display_number,
                    format_time(train.departure_time),
                    offer.car_type_name,
                    offer.min_price,
                    offer.place_quantity,
                    offer.lower_place_quantity)
            else:
                update_notification(notification, offer.min_price, offer.place_quantity, offer.lower_place_quantity)

def remove_notifications_for_not_presented(trains: list[Train], query: Query):
    notifications = select_notifications_by_query_id(query.query_id)
    for notification in notifications:
        if not offer_for_notification_presented(trains, notification):
            print('deleting ', end='')
            print(notification)
            notification.delete_instance()

# TODO: may be bad performance, try to use map(diff of sets) instead of iterating
def offer_for_notification_presented(trains: list[Train], notification: Notification):
    for train in trains:
        if train.display_number != notification.train_number:
            continue

        for offer in train.offers:
            if offer.car_type_name == notification.car_type_name:
                return True

    return False

def format_train_for_tg(train: Train):
    msg = '*Поезд {}*🚆\n'.format(train.display_number.replace('*', r'\*'))
    msg += '{} - {}\n'.format(format_time(train.departure_time), format_time(train.arrival_time))
    msg += 'В пути: {}:{:02d}\n'.format(math.floor(train.trip_duration / 60.0), int(train.trip_duration) % 60)

    for offer in train.offers:
        msg += '{}: {}({}) шт., '.format(offer.car_type_name, offer.place_quantity, offer.lower_place_quantity)

        if (offer.min_price == offer.max_price):
            msg += '{:.2f}k\n'.format(offer.min_price / 1000)
        else:
            msg += '{:.2f}k - {:.2f}k\n'.format(offer.min_price / 1000, offer.max_price / 1000)

    return msg.replace('.', r'\.').replace('-', r'\-').replace('(', r'\(').replace(')', r'\)')

def format_time(datetime):
    return time.strftime('%d.%m %H:%M', datetime)


if __name__ == "__main__":
    main(sys.argv[1:])
