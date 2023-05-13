# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from gcz_common.config import config
class GCZScrapyPipeline:
    def process_item(self, item, spider):
        spider.pipe.send(item)
        return item


#通过管道将数据写到csv中
class SaveCSVPipeline(object):
    file = None
    def open_spider(self, spider):
        if not os.path.exists(config.file.csvPath):
            os.mkdir(config.file.csvPath)
        if not os.path.exists(f'{config.file.csvPath}{config.file.phoneDataFileName}.csv'):
            self.file = open(f'{config.file.csvPath}{config.file.phoneDataFileName}.csv', 'w+', encoding='utf-8')
            column_name = 'title,price,business,evaluate,image_url,business_url,brond,goods_title,goods_id,goods_district,goods_weight,goods_cpu,play_memory,goods_color,goods_power,goods_memory,three_criterion,chromatic_system,screen_material,resolving_power,pixel,style\n'
            self.file.write(column_name)
        else:
            self.file = open(f'{config.file.csvPath}{config.file.phoneDataFileName}.csv', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        all_info = item['title']+','+item['price']+','+item['business']+','+item['evaluate']+','+item['image_url']+','+item['business_url']+','+item['brond']+','+item['goods_title']+','+item['goods_id']+','+item['goods_district']+','+item['goods_weight']+','+item['goods_cpu']+','+item['play_memory']+','+item['goods_color']+','+item['goods_power']+','+item['goods_memory']+','+item['three_criterion']+','+item['chromatic_system']+','+item['screen_material']+','+item['resolving_power']+','+item['pixel']+','+item['style']+'\n'
        self.file.write(all_info)
        return item
    def close_spider(self, spider):
        self.file.close()

import pymysql
class SaveMySQLPipeline(object):
    def open_spider(self, spider):

        #连接数据库
        try:
            self.db_conn = pymysql.connect(db=config.sql.database,
                                           host=config.sql.host,
                                           user=config.sql.user,
                                           password=config.sql.password,
                                           port=int(config.sql.port),
                                           charset=config.sql.charset)
            spider.mysqlConn = True
            self.db_cursor = self.db_conn.cursor()
            sql="""CREATE TABLE IF NOT EXISTS `goods`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `price` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `business` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `evaluate` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `image_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `business_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `brond` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;"""
            sql1 = """CREATE TABLE IF NOT EXISTS `goods_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_district` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_weight` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_cpu` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `play_memory` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_color` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_power` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `goods_memory` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `three_criterion` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `chromatic_system` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `screen_material` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `resolving_power` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `pixel` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `style` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;"""
            self.db_cursor.execute(sql)
            self.db_cursor.execute(sql1)
        except:
            print("数据库连接失败open_spider")
            spider.mysqlConn = False

    def process_item(self, item, spider):
        if not spider.mysqlConn:
            print("无数据库process_item")
            return item
        #goods表
        values = (item['title'],item['price'],item['business'],item['evaluate'],item['image_url'],item['business_url'],item['brond'])
        sql = 'insert into goods(title,price,business,evaluate,image_url,business_url,brond) values(%s,%s,%s,%s,%s,%s,%s)'
        #goods_info表
        values1 = (item['title'],item['goods_title'],item['goods_id'],item['goods_district'],item['goods_weight'],item['goods_cpu'],item['play_memory'],item['goods_color'],item['goods_power'],item['goods_memory'],item['three_criterion'],item['chromatic_system'],item['screen_material'],item['resolving_power'],item['pixel'],item['style'])
        sql1 = 'insert into goods_info(title,goods_title,goods_id,goods_district,goods_weight,goods_cpu,play_memory,goods_color,goods_power,goods_memory,three_criterion,chromatic_system,screen_material,resolving_power,pixel,style) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cursor.execute(sql,values)
        self.db_cursor.execute(sql1,values1)
        return item
    def close_spider(self,spider):
        if not spider.mysqlConn:
            print("无数据库close_spider")
            return
        self.db_conn.commit()
        self.db_cursor.close()
        self.db_conn.close()

def printLog(msg):
    if config.log.logShow: print(msg)
