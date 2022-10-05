import os
import logging
import pandas as pd

import scrapy
from scrapy.crawler import CrawlerProcess


df = pd.read_json("src/booking.json", encoding='utf-8')


list_urls = [url for url in df["urls"]]

class BookingHotelSpider(scrapy.Spider):
    # Name of your spider
    name = "bookingHotel"

    # Starting URL
    start_urls = list_urls[0:2]
    
    
    
    def parse(self, response):

        return {

            'name_hotels' : response.xpath('//*[@id="hp_hotel_name"]/div/div/h2/text()').get(),

            'scores' :  response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get(),     

            'coordinates': response.xpath('//*[@id="showMap2"]/span/@data-bbox').get(),

            "text_description2" : response.xpath('//*[@id="property_description_content"]/p/text()').getall()

        }

        
# Name of the file where the results will be saved
filename = "booking_hotel.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingHotelSpider)
process.start()