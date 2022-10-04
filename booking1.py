import os
import logging
import pandas as pd

import scrapy
from scrapy.crawler import CrawlerProcess


df = pd.read_csv("cities.csv")


list_urls = ["https://www.booking.com/searchresults.fr.html?ss=" +  city for city in df["City"]]

class BookingSpider(scrapy.Spider):
    # Name of your spider
    name = "booking"

    # Starting URL
    start_urls = list_urls
    
    
    
    def parse(self, response):

        split_url = response.url.split("ss=") 

        hotels = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div')


        for hotel in hotels:

            
            
            if  hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get() != None :

                if (hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[3]/text()').get() != None) :
                
                    yield {

                        "city" : split_url[-1], 
                    
                        "hotel_names" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                                                    
                        "scores" : hotel.xpath('div[1]/div[2]/div/div/div[2]/div[1]/a/span/div/div[1]/text()').get(),
                                        
                        "urls" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[2]/div[1]/a/@href').get().split("aid")[0],
                    
                        "text_description" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[3]/text()').get()
                                                
                                                                                                        
                    }

                else :

                    yield {

                        "city" : split_url[-1], 
                    
                        "hotel_names" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                                                    
                        "scores" : hotel.xpath('div[1]/div[2]/div/div/div[2]/div[1]/a/span/div/div[1]/text()').get(),
                                        
                        "urls" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[2]/div[1]/a/@href').get().split("aid")[0],
                    
                        "text_description" : hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[4]/text()').get()
                                                
                                                                                                        
                    }


        
# Name of the file where the results will be saved
filename = "booking.json"

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
process.crawl(BookingSpider)
process.start()