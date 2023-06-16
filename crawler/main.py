import scrapy
import psycopg2
import json


class SRealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    url_base = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1' \
               '&page=1&per_page=500'

    def __init__(self, *args, **kwargs):
        super(SRealitySpider, self).__init__(*args, **kwargs)
        self.conn = psycopg2.connect(
            host='postgres',
            port='5432',
            dbname='default_db',
            user='default',
            password='secret123'
        )

    def start_requests(self):
        # Make a request to Seznam's API :)
        # Simpler than parsing a page that is dynamically loaded. This is the recommended
        # approach according to scrapy docs.
        yield scrapy.Request(url=self.url_base, callback=self.parse_flats)

    def parse_flats(self, response: scrapy.http.response.Response):
        data = json.loads(response.text)

        # List of all flats (we directly ask for 500 of them)
        estates = data['_embedded']['estates']

        with self.conn.cursor() as cursor:
            # Clear table
            # (in case the database was already filled by previous `docker compose up` call)
            cursor.execute("TRUNCATE TABLE flats_sell")

            for estate in estates:
                name = estate['name']
                locality = estate['locality']
                price_tag = f"{estate['price']} CZK" if estate['price'] > 1 else "consult price with EA"
                title = f"{name} @ {locality}, {price_tag}"

                image_url = estate['_links']['image_middle2'][0]['href']

                insert_query = "INSERT INTO flats_sell (title, image_url) VALUES (%s, %s)"
                cursor.execute(insert_query, (title, image_url))
        self.conn.commit()

    def closed(self, reason):
        self.conn.close()
