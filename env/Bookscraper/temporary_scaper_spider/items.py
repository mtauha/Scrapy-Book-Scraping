# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_price(value):
    return f'£ {str(value)}' 

class BookItem:
    title = scrapy.Field()
    genre = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()     # scrapy.Field(serializer=serialize_price)
    price_incl_tax = scrapy.Field()     # scrapy.Field(serializer=serialize_price) 
    tax =  scrapy.Field()               # scrapy.Field(serializer=serialize_price) 
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    description = scrapy.Field()
