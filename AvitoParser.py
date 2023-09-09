from enum import Enum
from pyquery import PyQuery
from Product import Product
from HttpClient import HttpClient
from TgClient import TgClient
import urllib.parse


class Sort(Enum):
    date = 104


class AvitoParser:
    base_url = 'https://www.avito.ru/voronezh?f=ASgCAgECAUXGmgwVeyJmcm9tIjoxMjAwMCwidG8iOjB9&q='
    # baseUrl = 'http:// 0.0.0.0:8080'
    http_client = HttpClient()
    tg_client = TgClient()

    item_path = '[data-marker="catalog-serp"] > div'
    title_path = '[data-marker="item-title"]'
    params_path = '[data-marker="item-specific-params"]'

    def handleAds(self, search_str, sort=Sort.date):
        query_url = self.base_url + search_str + '&s=' + str(sort.value)

        response = self.http_client.get(query_url)

        print(response.status_code)

        if (response.status_code != 200):
            self.tg_client.send_notification('Код ответа: ' + str(response.status_code))

        # with open('resp.html', 'w') as fresp:
        #     fresp.write(response.text)

        pq = PyQuery(response.text)

        for item in pq.items(self.item_path):

            params = self._get_params(item)
            ram = self._get_ram(params)

            if ram != 0 and ram <= 64:
                continue

            id = self._get_id(item)

            if (self._is_in_db(id)):
                continue

            title = self._get_title(item)
            url = 'https://www.avito.ru' + item.find(self.title_path).attr['href']

            product = Product()
            product.product_id = id
            product.title = title
            product.params = params
            product.ram = ram
            product.url = url
            product.save()

            msg = title + ' ' + params + ' ' + url

            self.tg_client.send_notification(msg)

            print(id + ' ' + title + ' ' + str(ram))


    def _get_params(self, item):
        return item.find(self.params_path).text()
    
    def _get_ram(self, params):
        try:
            return int(params.split(',')[1].strip().split()[0])
        except:
            return 0

    def _get_id(self, item):
        return item.attr['id']

    def _get_title(self, item):
        return item.find(self.title_path).text()

    def _is_in_db(self, id):
        return Product.select().where(Product.product_id == id).count() > 0
