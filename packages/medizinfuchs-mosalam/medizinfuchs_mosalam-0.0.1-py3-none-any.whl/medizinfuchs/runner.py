import subprocess
from spider import Medizinfuchs

class MedizinfuchsScraper:
    product = None

    def __init__(self, product):
        self.product = product
        self.init_spider()

    def init_spider(self):
        LinkExtractorParamters = ["scrapy", "runspider", "spider.py",
                                  "-a", "product=" + self.product]
        RunnigProcess = subprocess.Popen(LinkExtractorParamters)
        RunnigProcess.wait()

    # def to_sqlite(self):
    #     Medizinfuchs().to_sqlite()


products = ['sildenafil', 'tadalafil', 'viagra', 'cialis', 'finasterid']

for product in products:

    scraper = MedizinfuchsScraper(product)
