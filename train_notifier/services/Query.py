from filters.Filters import BaseFilter
from services.ApiClients.RzdApiClient import RzdCity


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
