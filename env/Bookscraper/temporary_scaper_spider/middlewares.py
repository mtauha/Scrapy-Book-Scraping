# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import socket
from fake_headers import Headers
import struct
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TemporaryScaperSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TemporaryScaperSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


def fakeagents(results:int):
    ua = UserAgent() 

    user_agent = []
    for _ in range(results):
        user_agent.append(ua.random)

    return user_agent

class FakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    

    def __init__(self, settings) -> None:
        self.num_of_results = settings.get('NUM_OF_RESULTS')
        self.fake_user_agent_list = fakeagents(self.num_of_results)
    

    def _get_random_user_agent(self):
        random_index = random.randint(0, len(self.fake_user_agent_list) - 1)
        return self.fake_user_agent_list[random_index]
    
    def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent

        print("""******************** NEW HEADER ATTACHED ********************""")
        print(request.headers['User-Agent'])


def generate_random_ip():
    # Generate a random private IP address (IPv4) within the ranges defined for private networks
    networks = [
        (socket.inet_aton('192.0.0.0'), socket.inet_aton('223.255.255.0')),          
        (socket.inet_aton('128.0.0.0'), socket.inet_aton('191.255.0.0'))
    ]

    # Randomly select a private network range
    network_start, network_end = random.choice(networks)

    # Convert the IP address to an integer
    start_ip_int = struct.unpack('>I', network_start)[0]
    end_ip_int = struct.unpack('>I', network_end)[0]

    # Generate a random IP address within the selected network range
    random_ip_int = random.randint(start_ip_int, end_ip_int)

    # Convert the integer back to IP address format
    random_ip = socket.inet_ntoa(struct.pack('>I', random_ip_int))

    return random_ip

class FakeHTTPHeaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings:int) -> None:
        self.num_of_results = settings

    def _get_random_request_header(self):
        # Generate headers using the fake_headers module
        fake_headers = Headers(headers=True).generate()

        # Additional headers provided
        additional_headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
        }

        # Generate a random IP address and port
        host_ip = generate_random_ip()  # Generate random IP address
        port = random.randint(1024, 65535)  # Generate random port number
        host_header = f"{host_ip}:{port}"

        # Add Host header with the generated IP address and port
        additional_headers["Host"] = host_header

        # Merge both sets of headers
        random_header = {**fake_headers, **additional_headers}

        return random_header

    def process_request(self, request, spider):
        random_header = self._get_random_request_header()
        for header, value in random_header.items():
            request.headers[header] = value

        print("""******************** NEW HEADERS ATTACHED ********************""")
        print(request.headers)


class ProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.user = settings.get('PROXY_USER')