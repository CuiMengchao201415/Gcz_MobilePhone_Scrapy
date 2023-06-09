# CrawlerProcess
from multiprocessing import Process

import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

from gcz_scrapy.spiders.gcz_scrapy_spider import GCZScrapySpider

def crawlerProcess(pipe):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(GCZScrapySpider, pipe=pipe)
    process.start()

def crawlerRunner():
    runner = CrawlerRunner()

    d = runner.crawl(GCZScrapySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished

