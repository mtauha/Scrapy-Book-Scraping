# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class MYSQLPipeline:
    def __init__(self) -> None:
        load_dotenv('file.env')  # Ensure environment variables are loaded here
        
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('host'),
                user=os.getenv('user'),
                password=os.getenv('password'),
                database=os.getenv('database')
            )
            self.cursor = self.conn.cursor()
            print("Successfully connected to the database")
            
            # Create the books table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INT NOT NULL AUTO_INCREMENT,
                    url VARCHAR(255),
                    title TEXT,
                    product_type VARCHAR(255),
                    price_excl_tax DECIMAL(10, 2),
                    price_incl_tax DECIMAL(10, 2),
                    tax DECIMAL(10, 2),
                    availability INT,
                    num_reviews INT,
                    stars INT,
                    category VARCHAR(255),
                    description TEXT,
                    PRIMARY KEY (id)
                )
            """)
            self.conn.commit()
        
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def process_item(self, item, spider):
        if self.conn is not None:
            try:
                query = """
                INSERT INTO books (url, title, product_type, price_excl_tax, price_incl_tax, tax, availability, num_reviews, stars, category, description) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    item.get('url'),
                    item.get('title'),
                    item.get('product_type'),
                    item.get('price_excl_tax'),
                    item.get('price_incl_tax'),
                    item.get('tax'),
                    item.get('availability'),
                    item.get('num_reviews'),
                    item.get('stars'),
                    item.get('category'),
                    item.get('description')
                )
                self.cursor.execute(query, values)
                self.conn.commit()
            except Error as e:
                print(f"Error inserting item: {e}")
        return item

    def close_spider(self, spider):
        if self.conn is not None:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed")
 

class TemporaryScaperSpiderPipeline:
    def process_item(self, item, spider):
        pass
class BookScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        fields = adapter.field_names()

        for field in fields:
            if field != 'description':
                value = adapter.get(field)
                if value:  # Ensure value is not None
                    adapter[field] = value.strip()

        lower_case_keys = ["genre", "product_type"]
        for key in lower_case_keys:
            value = adapter.get(key)
            if value:  # Ensure value is not None
                adapter[key] = value.lower()

        price_keys = ["price_excl_tax", "price_incl_tax", "tax"]
        for key in price_keys:
            value = adapter.get(key)
            if value:  # Ensure value is not None
                value = value.replace('£', '').strip()
                adapter[key] = float(value)

        availability = adapter.get('availability')
        if availability:
            split = availability.split('(')
            if len(split) < 2:
                adapter['availability'] = 0
            else:
                availability = split[1].split(' ')
                adapter['availability'] = int(availability[0])

        stars = adapter.get('stars')
        if stars:
            stars = stars.replace("star-rating ", "").lower()
            star_mapping = {
                'one': 1,
                'two': 2,
                'three': 3,
                'four': 4,
                'five': 5
            }
            adapter['stars'] = star_mapping.get(stars, 0)  # Default to 0 if no match

        num_reviews = adapter.get('num_reviews')
        if num_reviews:
            adapter['num_reviews'] = int(num_reviews)

        return item