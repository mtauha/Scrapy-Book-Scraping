# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

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