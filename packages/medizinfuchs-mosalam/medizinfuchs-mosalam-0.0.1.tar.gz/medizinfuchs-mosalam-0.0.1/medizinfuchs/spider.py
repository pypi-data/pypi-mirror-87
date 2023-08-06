import sqlite3
import json
import re
import subprocess
import scrapy
import pandas as pd


class Medizinfuchs(scrapy.Spider):
    name = 'medizinfuchs_spider'
    allowed_domains = ['medizinfuchs.de']
    start_urls = ["https://www.medizinfuchs.de/"]
    items = {"position": [],
             "manufacturer": [],
             "name": [],
             "product_id": [],
             "low_price": [],
             "number_of_pills": [],
             "dosage": []
             }
    product_list = None

    def __init__(self, *args, **kwargs):
        super(Medizinfuchs, self).__init__(*args, **kwargs)
        self.product = kwargs.get('product')
        self.start_urls[0] = self.start_urls[0] + f"{self.product}.html"
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("products.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        print("################inside create table###########################")
        self.curr.execute("""create table IF NOT EXISTS products_tb(
            position int,
            name text,
            manufacturer text,
            product_id text,
            low_price real,
            number_of_pills text,
            dosage text,
            timestamp DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
        ) """)
        self.conn.commit()

    def parse(self, response):
        """Pasre method works as a call back method for the crawler, it process all the collected data

        Yields:
            Dictionary: dictionary that holds all the collected data to be passed to pandas
        """
        # ((\d+(mg|MG))|(\d+ (mg|MG)))
        dosage_pattern = re.compile(r"[0-9]+mg")
        number_of_pills_pattern = re.compile(r"(\d+-st)|(\dx\d+-st)")
        json_data = response.xpath(
            '//script[@type="application/ld+json"]/text()').get()
        data = json.loads(json_data)
        products = data.get('itemListElement')
        number_of_pills = response.css(".package::text").getall()

        for product in products:
            self.items['position'].extend([product.get('position', 0)])
            self.items['manufacturer'].extend([product.get('manufacturer')])
            self.items['name'].extend([product.get('name')])
            dosage_return = re.findall(
                dosage_pattern, product.get('name').lower().replace(' ', ''))
            if len(dosage_return) == 0:
                dosage_return = ['NA']
            self.items['dosage'].extend(dosage_return)
            self.items['product_id'].extend([product.get('productID')])
            self.items['low_price'].extend(
                [product.get('offers').get('lowPrice')])

        self.items['number_of_pills'].extend(
            [i.split(' ')[0] for i in number_of_pills])

        self.to_pandas()

        yield self.items

        for next_page in response.css('nav.Pagination a::attr(href)').getall():
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

    def to_pandas(self):
        product_list = pd.DataFrame(self.items)
        self.to_sqlite(product_list)
        return product_list

    def to_sqlite(self, df):
        df.to_sql('products_tb', self.conn, if_exists='append', index=False)
