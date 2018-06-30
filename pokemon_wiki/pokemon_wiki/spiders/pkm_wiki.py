# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import pandas as pd


class PkmWikiSpider(scrapy.Spider):
    name = 'pkm_wiki'
    def start_requests(self):
        allowed_domains = ['wiki.52poke.com']

        start_urls = ['http://mpokemon.com/sm/cht/character.php']

        for x,y in enumerate(start_urls):
            url = y

            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.1},
                meta={'num': x}
                )

    def parse(self, response):

        # hp = response.xpath("//*[@class='bgl-HP']/text()").extract()[1]
        # atk = response.xpath("//*[@class='bgl-攻击']/text()").extract()[1]
        # defend = response.xpath("//*[@class='bgl-防御']/text()").extract()[1]
        # spAtk = response.xpath("//*[@class='bgl-特攻']/text()").extract()[1]
        # spDef = response.xpath("//*[@class='bgl-特防']/text()").extract()[1]
        # spd = response.xpath("//*[@class='bgl-速度']/text()").extract()[1]
        number = response.meta.get('num')

        output = response.body.decode('utf-8')
        with open('/Users/mac/Desktop/projects/pokemon/character-{}.html'.format(number), 'w') as f:
            f.write(output)



        # print(hp, atk, defend, spAtk, spDef, spd)
        return response
