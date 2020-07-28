import scrapy

class RepublicaSpider(scrapy.Spider):
    name = "imagekhabar"
    start_urls = [
        'https://imagekhabar.com/',
    ]

    def parse(self, response):
        urls = response.css('div.ne-main-menu nav#dropdown ul li a::attr(href)').getall()
        for url in urls[2:11]:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        url_list = response.css('div.media-body.p-mb-none-child.media-margin30 h3.title-semibold-dark.size-lg.mb-15 a::attr(href)').getall()

        for j in url_list:
            url = response.urljoin(j)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        next_page = response.css('div.col-sm-6.col-12 ul.pagination li a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_list)

    def parse_detail(self, response):
        yield{
        'title':response.css('div.position-relative.mb-30 h1.title-semibold-dark.size-c30::text').get(),
        'author':response.css('div.news-details-layout1 p strong::text').get(),
        'published_date':response.css('div.position-relative.mb-30 ul.post-info-dark.mb-30 li::text')[2].getall(),
        'contents':response.css('div.news-details-layout1 p::text').getall(), 
        }