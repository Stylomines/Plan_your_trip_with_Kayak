import os
import logging
import pandas as pd

import scrapy
from scrapy.crawler import CrawlerProcess


df = pd.read_csv("cities.csv")


list_urls = ["https://www.booking.com/searchresults.fr.html?ss=" +  city for city in df["City"]]

class BookingHotelSpider(scrapy.Spider):
    # Name of your spider
    name = "bookinghotel"

    # Starting URL
    start_urls = list_urls
      
    
    def parse(self, response):

        # selects the url of each hotel

        hotels = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div')

        for hotel in hotels:

            if hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get() != None :

                url_hotel=  hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[2]/div[1]/a/@href').get().split("aid")[0]
               
                yield response.follow(url_hotel, callback=self.hotel_booking)


    def hotel_booking(self, response):

        # It will get urls, name_hotels, scores, coordinates, text_description

        yield {

            'url' : response.url,

            'city' : response.xpath('//*[@id="ss"]/@value').get(),
                        
            'name_hotel' : response.xpath('//*[@id="hp_hotel_name"]/div/div/h2/text()').get(),

            'score' :  response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get(),     

            'coordinates': response.xpath('//*[@id="showMap2"]/span/@data-bbox').get(),

            "text_description" : response.xpath('//*[@id="property_description_content"]/p/text()').getall()
            
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