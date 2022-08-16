# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    #Spoofing request headers
    def set_user_agent(self, request , spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[1]/text()").get(),
            'year': response.xpath("//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh'][1]/text()").get(),
            #some movies don't have a rating though :) so a little modification is required here to handle this 
            'duration': response.xpath("//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh'][1]/parent::li/parent::ul/li[3]/child::node()").getall(),
            'genre': response.xpath("//div[@data-testid='genres']/div[2]/a/span/text()").get(),
            'rating': response.xpath("//div[contains(@data-testid ,'hero-rating')][1]/a/div/div/div/div/span[1]/text()").get(),
            'movie_url': response.url
        }
