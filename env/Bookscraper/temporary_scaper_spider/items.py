# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TemporaryScaperSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def serialize_price(value):
    return f'£ {str(value)}' 

class BookItem(scrapy.Item):
    url = scrapy.Field()
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
    category = scrapy.Field()
