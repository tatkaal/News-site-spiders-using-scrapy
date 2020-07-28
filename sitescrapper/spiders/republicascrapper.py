import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "myRepublica"
    start_urls = [
        'https://myrepublica.nagariknetwork.com/',
    ]

    def parse(self, response):
        urls = response.css('div#navbar ul.navbar-nav li a::attr(href)').getall()
        for url in urls[1:]:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        url_list = response.css('div.categories-list-info div.main-heading a::attr(href)').getall()
        new_list = url_list[::2]
        for j in new_list:
            url = response.urljoin(j)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        next_page = response.css('ul.pagination li a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_list)

    def parse_detail(self, response):
        yield{
        'title':response.css('div.main-heading h2::text').get(),
        'author':response.css('div.main-heading div.headline-time a::text')[0].get(),
        'published_date':response.css('div.main-heading div.headline-time p::text').get(),
        }