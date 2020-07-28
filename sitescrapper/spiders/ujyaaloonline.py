import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "ujaaloonline"
    start_urls = [
        'https://ujyaaloonline.com/',
    ]

    def parse(self, response):
        urls = response.css('div.menu-wrap mean-menu ul li a::attr(href)').getall()
    #     for url in urls[0:10]:
    #         url = response.urljoin(url)
    #         yield scrapy.Request(url=url, callback=self.parse_list)

    # def parse_list(self, response):
    #     url_list = response.css('div.business a::attr(href)').getall()

    #     for j in url_list:
    #         url = response.urljoin(j)
    #         yield scrapy.Request(url=url, callback=self.parse_detail)
        
    #     next_page = response.css('div.pagination ul.pagination li a::attr(href)')[-1].get()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse_list)

    # def parse_detail(self, response):
    #     yield{
    #     'title':response.css('div.blog-details padding-25 bg-white bd-grey mb-10 h1::text').get(),
    #     'author':response.css('div.newstext p strong::text').get(),
    #     'published_date':response.css('div.post-meta ul li::text').getall()[3],
    #     'contents':response.css('div.newstext p::text').getall(), 
    #     }