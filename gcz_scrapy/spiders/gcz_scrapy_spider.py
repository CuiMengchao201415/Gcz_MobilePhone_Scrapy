from scrapy import Request
from scrapy import Spider
from selenium import webdriver

from config import config
from gcz_scrapy.items import GCZScrapyItem
import re
import time
class GCZScrapySpider(Spider):
    name = 'gcz_scrapy'

    def __init__(self, pipe):
        self.pipe = pipe
        self.driver = webdriver.Chrome()

        self.start_urls = []
        i = 1
        while i <= config.scrapy.maxPageNum:
            url = f'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&pvid=8858151673f941e9b1a4d2c7214b2b52&page={i}'
            self.start_urls.append(url)
            i += config.scrapy.pageStep



    def parse(self, response):
        # self.printLog(response.url)
        item = GCZScrapyItem()
        list_selector = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        # self.printLog(list_selector)
        for one_selector in list_selector:
            # try:
            image_url = one_selector.xpath('div/div[1]/a/img/@gcz_pyqt').extract()
            if image_url == []:
                image_url = '无图片链接'
            else:
                image_url = response.urljoin(image_url[0])
            self.printLog('图片链接：',image_url)

            price = one_selector.xpath('div/div[3]/strong/i/text()').extract()
            if price == []:
                price = '无'
            else:
                price = price[0]
            self.printLog('价格：',price)

            detail_url = one_selector.xpath('div/div[4]/a/@href').extract()
            if detail_url == []:
                detail_url = '无'
            else:
                detail_url = response.urljoin(detail_url[0])
            self.printLog('详情页链接：',detail_url)

            evaluate = one_selector.xpath('div/div[5]/strong/a/text()').extract()
            if evaluate == []:
                evaluate = '无'
            else:
                evaluate = evaluate[0]
            self.printLog('评价：',evaluate)

            business = one_selector.xpath('div/div[7]/span/a/text()').extract()
            if business == []:
                business = '无'
            else:
                business = business[0]
            self.printLog('商家：',business)

            business_url = one_selector.xpath('div/div[7]/span/a/@href').extract()
            if business_url == []:
                business_url = '无商家链接'
            else:
                business_url =response.urljoin(business_url[0])
            self.printLog('商家链接：',business_url, '\n')


            item['image_url'] = image_url
            item['price'] = price
            item['evaluate'] = evaluate
            item['business'] = business
            item['business_url'] = business_url

            #跳转到详情页
            yield Request(detail_url,
                          meta={
                              'item':item #定义一个key为item,然后将解析后的item值放置在这
                          },callback=self.detailinfo_parse)
            # except:
            #     pass
    def detailinfo_parse(self,response):
        time.sleep(config.scrapy.timeInterval)
        item = response.meta['item']
        title = response.xpath('//div[@class="itemInfo-wrap"]/div[@class="sku-name"]/text()').extract()
        if title == []:
            title = '无'
        elif len(title) == 1:
            title = title[0].replace('\n','').strip()
        else:
            try:
                title = title[1].replace('\n','').strip()
            except:
                pass
        self.printLog('标题:',title)
        brond = response.xpath('//ul[@class="p-parameter-list"]/li/@title').extract()
        if brond == []:
            brond = '杂牌'
        else:
            brond = brond[0]

        self.printLog('品牌:',brond)
        # 商品名称
        goods_title = re.findall('<li title=".*?">商品名称：(.*?)</li>',response.text)
        if goods_title == []:
            goods_title = '无'
        else:
            goods_title = goods_title[0]
        self.printLog('商品名称:',goods_title)
        #商品编号
        goods_id = re.findall('<li title=".*?">商品编号：(.*?)</li>', response.text)
        if goods_id == []:
            goods_id = '无'
        else:
            goods_id = goods_id[0]
        self.printLog('商品编号:',goods_id)
        #商品地区
        goods_district = re.findall('<li title=".*?">商品产地：(.*?)</li>', response.text)
        if goods_district == []:
            goods_district = '无'
        else:
            goods_district = goods_district[0]
        self.printLog('商品产地:',goods_district)
        #商品毛重
        goods_weight = re.findall('<li title=".*?">商品毛重：(.*?)</li>', response.text)
        if goods_weight == []:
            goods_weight = '无'
        else:
            goods_weight = goods_weight[0]
        self.printLog('商品毛重:',goods_weight)
        #CPU型号
        goods_cpu = re.findall('<li title=".*?">CPU型号：(.*?)</li>', response.text)
        if goods_cpu == []:
            goods_cpu = '无'
        else:
            goods_cpu = goods_cpu[0]
        self.printLog('CPU型号:',goods_cpu)
        #运行内存
        play_memory = re.findall('<li title=".*?">运行内存：(.*?)</li>', response.text)
        if play_memory == []:
            play_memory = '无'
        else:
            play_memory = play_memory[0]
        self.printLog('运行内存:',play_memory)
        #机身颜色
        goods_color = re.findall('<li title=".*?">机身颜色：(.*?)</li>', response.text)
        if goods_color == []:
            goods_color = '无'
        else:
            goods_color = goods_color[0]
        self.printLog('机身颜色:',goods_color)
        #充电功率
        goods_power = re.findall('<li title=".*?">充电功率：(.*?)</li>', response.text)
        if goods_power == []:
            goods_power = '无'
        else:
            goods_power = goods_power[0]
        self.printLog('充电功率:',goods_power)
        #机身内存
        goods_memory = re.findall('<li title=".*?">机身内存：(.*?)</li>', response.text)
        if goods_memory == []:
            goods_memory = '无'
        else:
            goods_memory = goods_memory[0]
        self.printLog('机身内存:',goods_memory)
        #三防标准
        three_criterion = re.findall('<li title=".*?">三防标准：(.*?)</li>', response.text)
        if three_criterion == []:
            three_criterion = '无'
        else:
            three_criterion = three_criterion[0]
        self.printLog('三防标准',three_criterion)
        #机身色系
        chromatic_system = re.findall('<li title=".*?">机身色系：(.*?)</li>', response.text)
        if chromatic_system == []:
            chromatic_system = '无'
        else:
            chromatic_system = chromatic_system[0]
        self.printLog('机身色系:',chromatic_system)
        #屏幕材料
        screen_material = re.findall('<li title=".*?">机身色系：(.*?)</li>',response.text)
        if screen_material == []:
            screen_material = '无'
        else:
            screen_material = screen_material[0]
        self.printLog('屏幕材质:',screen_material)
        #屏幕分辨率
        resolving_power = re.findall('<li title=".*?">屏幕材质：(.*?)</li>', response.text)
        if resolving_power == []:
            resolving_power = '无'
        else:
            resolving_power = resolving_power[0]
        self.printLog('屏幕分辨率:',resolving_power)
        #后摄主像素
        pixel = re.findall('<li title=".*?">后摄主像素：(.*?)</li>', response.text)
        if pixel == []:
            pixel = '无'
        else:
            pixel = pixel[0]
        self.printLog('后摄主像素',pixel)
        #风格
        style = re.findall('<li title=".*?">风格：(.*?)</li>', response.text)
        if style == []:
            style = '无'
        else:
            style = style[0]
        self.printLog('风格:',style,'\n')

        item['title'] = title
        item['brond'] = brond
        item['goods_title'] = goods_title
        item['goods_id'] = goods_id
        item['goods_district'] = goods_district
        item['goods_weight'] = goods_weight
        item['goods_cpu'] = goods_cpu
        item['play_memory'] = play_memory
        item['goods_color'] = goods_color
        item['goods_power'] = goods_power
        item['goods_memory'] = goods_memory
        item['three_criterion'] = three_criterion
        item['chromatic_system'] = chromatic_system
        item['screen_material'] = screen_material
        item['resolving_power'] = resolving_power
        item['pixel'] = pixel
        item['style'] = style

        yield item
        
    def printLog(self, msg, *args):
        if(config.log.logShow): print(msg, *args)


