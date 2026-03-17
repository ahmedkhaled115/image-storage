import scrapy
import re 
import pandas as pd

class InfoSpider(scrapy.Spider):
    name = "info"
    allowed_domains = ["www.gravityperformance.co.uk"]
    custom_settings = {
        'FEEDS': {
            'gravityperformance2.csv': {
                'format': 'csv',
                'encoding': 'utf-8-sig',
            },
            # 'concurrency': 10
        }
    }
    
    def start_requests(self):
        with open('urls.txt', 'r') as f:
            urls = f.read().splitlines()
        df = pd.read_csv("gravityperformance2.csv")
        links = df['url'].to_list()
        for url in urls:
            if url in links:
                continue
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # breakpoint()
        title = response.xpath('//h1//text()').get()
        category = ''.join(response.xpath('//nav[@class="woocommerce-breadcrumb"]/a/text()').getall()[1:2]).strip()
        tags = ', '.join(response.xpath('//nav[@class="woocommerce-breadcrumb"]/a/text()').getall()[1:])
        price = response.xpath('//meta[@property="product:price:amount"]/@content').get()
        description = ''.join(response.xpath('//meta[@property="og:description"]/@content').getall()).strip()
        # get image using regex from "ImageObject","url":"https://www.gravityperformance.co.uk/wp-content/uploads/2022/02/ZZ03626-04.jpg","height":"1600","width":"1600"}
        images = ', '.join(re.findall(r'"ImageObject","url":"(.*?)",', response.text))

        yield{
            'title': title,
            'category': category,
            'price': price,
            'description': description,
            'images': images,
            'url': response.url
        }
