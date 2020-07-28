# response.css('div.each__news a::text').getall()

import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "dcnepal"
    start_urls = [
        'https://www.dcnepal.com/',
    ]

    def parse(self, response):
        urls = response.css('div.menu-menu-1-container ul#primary-menu li a::attr(href)').getall()
        for url in urls[2:]:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        url_list = response.css('div.each__news a::attr(href)').getall()
        main_news_url = response.css('div#main__news a::attr(href)').getall()
        url_list = url_list + main_news_url
        url_list = url_list[::2]

        for j in url_list:
            url = response.urljoin(j)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        next_page = response.css('div.uk-container a.next.page-numbers::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_list)

    def parse_detail(self, response):
        yield{
        'title':response.css('div.uk-container h1.entry-title.text__l::text').get(),
        'author':response.css('div.author__wrap.uk-flex.uk-flex-middle.uk-flex-wrap::text').get(),
        'published_date':response.css('div.post__time::text').get(),
        'contents':response.css('div.single__content p::text').getall(), 
        }