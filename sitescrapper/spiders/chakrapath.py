import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "chakrapath"
    start_urls = [
        'http://www.chakrapath.com/',
    ]

    def parse(self, response):
        urls = response.css('div.collapse navbar-collapse navbar-ex1-collapse ul li a::attr(href)').getall()
