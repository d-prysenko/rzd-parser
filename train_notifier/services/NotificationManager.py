import math
import time
from model.Notification import Notification
from model.NotificationRepository import NotificationRepository
from services.Query import Query
from services.RzdProvider.OfferDTO import Offer
from services.RzdProvider.TrainDTO import Train


class NotificationManager:
    def __init__(self):
        self.notification_rep = NotificationRepository()

    def prepare_trains_for_notifications(self, trains: list[Train], query: Query) -> list[Train]:
        self._remove_notifications_for_non_presented_offers(trains, query)

        filtered_trains = self._remove_non_changed_offers(trains, query)

        self._create_or_update_notifications(filtered_trains, query)

        return filtered_trains
    
    def format_train_for_tg(self, train: Train):
        msg = '*Поезд {}*🚆\n'.format(train.display_number.replace('*', r'\*'))
        msg += '{} - {}\n'.format(self._format_time(train.departure_time), self._format_time(train.arrival_time))
        msg += 'В пути: {}:{:02d}\n'.format(math.floor(train.trip_duration / 60.0), int(train.trip_duration) % 60)

        for offer in train.offers:
            msg += '{}: {}({}) шт., '.format(offer.car_type_name, offer.place_quantity, offer.lower_place_quantity)

            if (offer.min_price == offer.max_price):
                msg += '{:.2f}k\n'.format(offer.min_price / 1000)
            else:
                msg += '{:.2f}k - {:.2f}k\n'.format(offer.min_price / 1000, offer.max_price / 1000)

        return msg.replace('.', r'\.').replace('-', r'\-').replace('(', r'\(').replace(')', r'\)')
    

    def _remove_notifications_for_non_presented_offers(self, trains: list[Train], query: Query):
        notifications = self.notification_rep.select_all_by_query_id(query.query_id)
        for notification in notifications:
            if not self._offer_for_notification_presented(trains, notification):
                print('deleting ', end='')
                print(notification)
                notification.delete_instance()

    # TODO: may be bad performance, try to use map(diff of sets) instead of iterating
    def _offer_for_notification_presented(self, trains: list[Train], notification: Notification):
        for train in trains:
            if train.display_number != notification.train_number:
                continue

            for offer in train.offers:
                if offer.car_type_name == notification.car_type_name:
                    return True

        return False
    
    def _remove_non_changed_offers(self, trains: list[Train], query: Query):
        result: list[Train] = []

        for train in trains:
            offers: list[Offer] = []

            for offer in train.offers:
                if not self.notification_rep.exists(
                    query.chat_id,
                    query.query_id,
                    train.display_number,
                    self._format_time(train.departure_time),
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

    def _create_or_update_notifications(self, trains: list[Train], query: Query):
        for train in trains:
            for offer in train.offers:
                notification = self.notification_rep.get_or_none(query.chat_id, query.query_id, train.display_number, self._format_time(train.departure_time), offer.car_type_name)

                if notification == None:
                    self.notification_rep.create(
                        query.chat_id,
                        query.query_id,
                        train.display_number,
                        self._format_time(train.departure_time),
                        offer.car_type_name,
                        offer.min_price,
                        offer.place_quantity,
                        offer.lower_place_quantity)
                else:
                    self.notification_rep.update(notification, offer.min_price, offer.place_quantity, offer.lower_place_quantity)

    def _format_time(self, datetime):
        return time.strftime('%d.%m %H:%M', datetime)