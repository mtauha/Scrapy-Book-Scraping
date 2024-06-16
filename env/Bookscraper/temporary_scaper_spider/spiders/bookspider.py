import scrapy
from Bookscraper.temporary_scaper_spider.items import BookItem 


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css('h3 a ::attr(href)').get()
            if book_url is not None:
                if 'catalogue' not in book_url:
                    next_url = str(self.start_urls[0]) + f'/catalogue/{book_url}'
                else:
                    next_url = str(self.start_urls[0]) + f'/{book_url}'
                yield response.follow(next_url, callback=self.parse_book_page)
            
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue' not in next_page:
                    next_url = str(self.start_urls[0]) + f'/catalogue/{next_page}'
            else:
                    next_url = str(self.start_urls[0]) + f'/{next_page}'
        yield response.follow(next_url, callback=self.parse)
    
    def parse_book_page(self, response):
        table = response.xpath('//table[@class="table table-striped"]')
        rows = table.xpath('//tr')
        bookitem = BookItem()

        bookitem["url"] = response.url
        bookitem["title"] = response.xpath('//div[@class="col-sm-6 product_main"]/h1[1]/text()').get()
        bookitem["genre"] = response.xpath('.//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get()
        bookitem["description"]= response.xpath('//article[@class="product_page"]/p/text()').get()
        bookitem["product_type"]= rows[1].xpath('.//td/text()').get()
        bookitem["price_excl_tax"]= rows[2].xpath('.//td/text()').get()
        bookitem["price_incl_tax"]= rows[3].xpath('.//td/text()').get()
        bookitem["tax"]= rows[4].xpath('.//td/text()').get()
        bookitem["availability"]= rows[5].xpath('.//td/text()').get()
        bookitem["num_reviews"]= rows[6].xpath('.//td/text()').get()
        bookitem["stars"]= response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[3]/@class').get()
        bookitem["category"] = response.xpath('.//*[@class="breadcrumb"]/li[3]/a/text()').get()

        yield bookitem