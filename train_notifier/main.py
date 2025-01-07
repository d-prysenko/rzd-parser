import sys, getopt, time
import logging
from services.RzdProvider.RzdProvider import RzdProvider
from services.RzdProvider.TrainDTO import Train, Offer
from services.Settings import Settings
from services.NotificationManager import NotificationManager
from model.Notification import create_tables, Notification
from filters.Filters import BaseFilter, Filters
from filters.OfferFilters import OnlyLowerPlacesFilter, PriceFilter, WithPetsFilter
from filters.TrainFilters import TripDurationLowerThan
from services.ApiClients.RzdApiClient import RzdCity
from services.ApiClients.TgClient import TgClient
from services.Query import Query


rzd_provider = RzdProvider()
tg_client = TgClient()
logger = logging.getLogger()
notification_manager = NotificationManager()


def main(argv):
    logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format="%(asctime)s %(module)s %(levelname)s %(message)s")

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
        Query(1, chat_id, "2025-01-06T00:00:00", RzdCity.Voronezh, RzdCity.Moscow, default_filters),
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
        print_train(train)

    filtered_trains = notification_manager.prepare_trains_for_notifications(filtered_trains, query)

    print('\n\nsending')

    for train in filtered_trains:
        msg = notification_manager.format_train_for_tg(train)
        tg_client.send_notification(query.chat_id, msg)
        print(msg)

    print('\nend.')

def print_train(train: Train):
    print(f"Поезд {train.display_number}")
    print(time.strftime('%d.%m %H:%M', train.departure_time) + " - " + time.strftime('%d.%m %H:%M', train.arrival_time))

    for offer in train.offers:
        print(f"{offer.car_type_name}: {offer.place_quantity}({offer.lower_place_quantity})")

    print()

if __name__ == "__main__":
    main(sys.argv[1:])
