# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GCZScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field() #标题
    price = scrapy.Field() #价格
    business = scrapy.Field() #商家
    evaluate = scrapy.Field() #评论人数
    image_url = scrapy.Field() #照片链接
    business_url = scrapy.Field() #商家链家

    brond = scrapy.Field() #品牌
    goods_title = scrapy.Field() #商品类型
    goods_id = scrapy.Field()  #商品编号
    goods_district = scrapy.Field() #商品产地
    goods_weight = scrapy.Field() #商品毛重
    goods_cpu = scrapy.Field() #商品CPU
    play_memory = scrapy.Field() #运行内存
    goods_color = scrapy.Field() #机身颜色
    goods_power = scrapy.Field() #充电功率
    goods_memory = scrapy.Field() #机身内存
    three_criterion = scrapy.Field() #三防准则
    chromatic_system = scrapy.Field() #机身色系
    screen_material = scrapy.Field() #屏幕材料
    resolving_power = scrapy.Field() #分辨率
    pixel = scrapy.Field() #后摄主像素
    style = scrapy.Field() #风格

