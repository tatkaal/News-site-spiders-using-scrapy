import re
from datetime import datetime
import scrapy
# from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider, Rule
# from news_crawler.items import KathmanduPostItem
from scrapy.linkextractors import LinkExtractor
def filter_keyword(keywords, contents):
    for string in contents:
        if any(ele in string.lower() for ele in keywords):
            return True
class IcrawlerSpider(CrawlSpider):
    name = 'post1'
    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        IcrawlerSpider.rules = [
           Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(IcrawlerSpider, self).__init__(*args, **kwargs)
    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        i = {}
        i['url'] = response.url
        return  i
class EkantipurSpider(scrapy.Spider):
    name = "ekantipur"
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get(url)
        self.domain = kwargs.get('domain')
        self.keyword = kwargs.get('keyword')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
    def parse(self, response):
        urls = response.css('ul li a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)
    def parse_list(self, response):
        urls = response.css('article.normal h2 a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
    def parse_detail(self, response):
        title = response.css('div.article-header h1::text').get()
        if title:
            item = {}
            item["title"] = title
            item["content"] = response.css('article.normal div.description p::text').getall()
            item["author"] = response.css('article.normal span.author a::text').get()
            item["article_published_date"] = response.css('article.normal time::text').get()
            item["article_updated_date"] = ''
            yield item
class KathmanduPostSpider(scrapy.Spider):
    name  = "kathmandupost"
    # def __init__(self, *args, **kwargs):
    #     self.url = kwargs.get('url')
    #     self.domain = kwargs.get('domain')
    #     self.keywords = kwargs.get('keywords')
    #     self.start_urls = [self.url]
    #     self.allowed_domains = [self.domain]
        # self.start_urls = ['https://kathmandupost.com/']
        # return scrapy.Request(url=self.start_urls, callback=self.parse)
    start_urls = [
        'https://kathmandupost.com',   
    ]
    def parse(self, response):
        urls = response.css('ul.list-unstyled li a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)
    # def load_more(self):
    def parse_list(self, response):
        urls = response.css('article.article-image a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
    def parse_detail(self, response):
        # keywords = ["migrant workers"]
        # found = False
        # 'content': response.css('section.story-section p::text').getall()
        title = response.css('div.col-sm-8 h1::text').get()
        content = response.css('section.story-section p::text').getall()
        if title:
            # if filter_keyword(self.keywords, content):
            item = {}
            item["title"] = response.css('div.col-sm-8 h1::text').get()
            item["content"] = response.css('section.story-section p::text').getall()
            item["author"] = response.css('h5.text-capitalize a::text').get()
            published_date = response.css('div.updated-time::text')[0].get()
            if published_date:
                try:
                    published_date = published_date.split(':')
                    item["article_published_date"] = str(datetime.strptime(published_date[1].strip(), "%b %d, %Y").date())
                except:
                    item["article_published_date"] = ''
            # item["article_published_date"] = response.css('div.updated-time::text')[0].get()
            item["article_updated_date"] = response.css('div.updated-time::text')[1].get()
            yield item
                # found = True
        # if found:
        #     # item = KathmanduPostItem()
        #     item = {}
        #     item["title"] = response.css('div.col-sm-8 h1::text').get()
        #     item["content"] = response.css('section.story-section p::text').getall()
        #     item["author"] = response.css('h5.text-capitalize a::text').get()
        #     item["article_published_date"] = response.css('div.updated-time::text')[0].get()
        #     yield item
            # yield {
            #     'title': response.css('div.col-sm-8 h1::text').get(),
            #     'published_date': response.css('div.updated-time::text')[0].get(),
            #     # 'updated_date': response.css('div.updated-time::text')[1].get(), 
            #     'author': response.css('h5.text-capitalize a::text').get(),
            #     'url': response.request.url,
            #     'content': response.css('section.story-section p::text').getall()
            # }
        # items = []
        # count = 0
        # for content in response.css('article.article-image'):
        #     title = content.css('a h3::text').get()
        #     # keyword = keyword_str()
        #     # keywords = ["nirmala pant case", "ifc", "government", "corrupt", "corruption"]
        #     contains = any(ele in title.lower() for ele in keywords) 
        #     if contains:
        #         yield {
        #             'title': content.css('a h3::text').get(),
        #             'content': content.css('p::text').get(), 
        #             'url': response.request.url
        #         }
            # title =  content.css('a h3::text').get()
            # content =  content.css('p::text').get()
            # items['title'] = title
            # items['content'] = content
            # yield 
            # count+=1
            # if count > 50:
            #     break
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
class HimalayanTimes(scrapy.Spider):
    name = "thehimalayantimes"
    start_urls = [
        'https://thehimalayantimes.com/',
    ]
    # def __init__(self, *args, **kwargs):
    #     self.url = kwargs.get(url)
    #     self.domain = kwargs.get('domain')
    #     self.keyword = kwargs.get('keyword')
    #     self.start_urls = [self.url]
    #     self.allowed_domains = [self.domain]
    def parse(self, response):
        urls = response.css('ul.nav li a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)
    def parse_list(self, response):
        urls = response.css('ul.mainNews li h4 a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
    def parse_detail(self, response):
        title = response.css('div.contentDetail h2 a::text').get()
        if title:
            item = {}
            item["title"] = title
            item["content"] = response.css('div.mainPost p::text').getall()
            # regex = re.compile(r'[\n\r\t]')
            # content = regex.sub("", content)
            # item["content"] = content
            item["author"] = response.css('div.contentDetail div.newsSource::text').get()
            item["article_published_date"] = response.css('div.contentDetail div.newsSource::text')[0].get()
            item["article_updated_date"] = ''
            yield item
class AnnapurnaPost(scrapy.Spider):
    name = "annapurna"
    start_urls = {
        'http://annapurnapost.com/',
    }
    def parse(self, response):
        urls  = response.css('ul.nav li a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)
    def parse_list(self, response):
        urls = response.css('h1 a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
    def parse_detail(self, response):
        yield {
            'title': response.css('div.detail-news h1::text').get(),
            'author': response.css('div.detail-news a span::text').get(),
            'published_date': response.css('div.detail-news p.detail-time i.fa::text').get(),
        }
class EkantipurSpider(scrapy.Spider):
    name = "text"
    start_urls = [
        'https://ekantipur.com/',
    ]
    def parse(self, response):
        urls = response.css('ul li a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_list)
    def parse_list(self, response):
        urls = response.css('article.normal h2 a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
    def parse_detail(self, response):
        title = response.css('div.article-header h1::text').get()
        if title:
            item = {}
            item["title"] = title
            item["content"] = response.css('article.normal div.description p::text').getall()
            item["author"] = response.css('article.normal span.author a::text').get()
            item["article_published_date"] = response.css('article.normal time::text').get()
            item["article_updated_date"] = ''
            yield item