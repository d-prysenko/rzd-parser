from model.Notification import Notification


class NotificationRepository:
    def create(
            self,
            chat_id: str,
            query_id: int,
            train_number: str,
            departure_datetime: str,
            car_type_name: str,
            min_price: float,
            place_quantity: int,
            lower_place_quantity: int
            ):
        return Notification.create(
            chat_id=chat_id,
            query_id=query_id,
            train_number=train_number,
            departure_datetime=departure_datetime,
            car_type_name=car_type_name,
            min_price=min_price,
            place_quantity=place_quantity,
            lower_place_quantity=lower_place_quantity
        )

    def get_or_none(
            self,
            chat_id: str,
            query_id: int,
            train_number: str,
            departure_datetime: str,
            car_type_name: str
            ):
        return Notification.get_or_none(
            (Notification.chat_id == chat_id) &
            (Notification.query_id == query_id) &
            (Notification.train_number == train_number) &
            (Notification.departure_datetime == departure_datetime) &
            (Notification.car_type_name == car_type_name))

    def select_all_by_query_id(self, query_id: int):
        return Notification.select().where(Notification.query_id == query_id)

    def exists(
            self,
            chat_id: str,
            query_id: int,
            train_number: str,
            departure_datetime: str,
            car_type_name: str,
            min_price: float,
            place_quantity: int,
            lower_place_quantity: int
            ):
        return Notification.get_or_none(
            (Notification.chat_id == chat_id) &
            (Notification.query_id == query_id) &
            (Notification.train_number == train_number) &
            (Notification.departure_datetime == departure_datetime) &
            (Notification.car_type_name == car_type_name)& 
            (Notification.min_price == min_price) &
            (Notification.place_quantity == place_quantity) &
            (Notification.lower_place_quantity == lower_place_quantity)) != None

    def update(
            self,
            notification: Notification,
            min_price: float,
            place_quantity: int,
            lower_place_quantity: int
            ):
        notification.min_price = min_price
        notification.place_quantity = place_quantity
        notification.lower_place_quantity = lower_place_quantity
        notification.save()