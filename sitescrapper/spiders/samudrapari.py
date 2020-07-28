import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "samudrapari"
    start_urls = [
        'http://samudrapari.com/',
    ]

    def parse(self, response):
        urls = response.css('#menu-main-navigation').getall()
    #     for url in urls[2:11]:
    #         url = response.urljoin(url)
    #         yield scrapy.Request(url=url, callback=self.parse_list)

    # def parse_list(self, response):
    #     url_list = response.css('div.media-body.p-mb-none-child.media-margin30 h3.title-semibold-dark.size-lg.mb-15 a::attr(href)').getall()

    #     for j in url_list:
    #         url = response.urljoin(j)
    #         yield scrapy.R
    # equest(url=url, callback=self.parse_detail)
        
    #     next_page = response.css('div.col-sm-6.col-12 ul.pagination li a::attr(href)')[-1].get()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse_list)

    # def parse_detail(self, response):
    #     yield{
    #     'title':response.css('div.single_view h1::text').get(),
    #     'author':response.css('div.dline_left span.writer::text').get(),
    #     'published_date':response.css('div.dline_left span.pubed::text').getall(),
    #     'contents':response.css('div.content-single p::text').getall(), 
    #     }