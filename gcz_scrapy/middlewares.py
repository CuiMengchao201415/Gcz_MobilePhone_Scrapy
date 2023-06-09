# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from gcz_common.config import config


class GCZScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # gcz_scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time

class GCZScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # gcz_scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        if spider.name == 'gcz_scrapy':
            spider.driver.get(request.url)  # 获取请求网页
            try:
                # wait = WebDriverWait(spider.driver,20)
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME,'gl-warp clearfix')))
                spider.driver.execute_script(f'window.scrollTo(0,document.body.scrollHeight/{config.scrapy.pageScroll})')  # 将页面滑动到页面的一半
                for i in range(config.scrapy.pageScroll):  # 滚动3次
                    time.sleep(config.scrapy.timeInterval)
                    spider.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                origin_code = spider.driver.page_source  # 获得到加载完成的页面代码
                # 将源代码构成一个Request对象，并返回
                res = HtmlResponse(url=request.url, encoding='utf-8',
                                   body=origin_code,
                                   request=request)
                return res
            except TimeoutException:  # 超时
                pass
            except NoSuchElementException:  # 异常
                pass
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #设置基数
import random #随机选择
from fake_useragent import UserAgent
class GczUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random