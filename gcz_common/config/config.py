# 全局配置文件
import os

import yaml

# region 配置

class file:
    echartPath=""
    csvPath=""
    pieFileName=""
    barFileName=""
    lineFileName=""
    phoneDataFileName=""

class scrapy:
  maxPageNum=""
  pageStep=""
  pageScroll=""
  timeInterval=""

class sql:
  host=""
  port="" 
  user="" 
  password="" 
  database="" 
  charset=""
  
class log:
  logShow=""
  logLevel=""
  statementShow=""
  logPassword=""

# endregion
class configEdit:
    def __init__(self):
        # 打开yaml文件
        configProdUrl = "./config.yaml"
        configLocalUrl = "resources/config/config.local.yaml"
        configUrl = "resources/config/config.yaml"
        if os.path.exists(configProdUrl):
            configUrl = configProdUrl
        elif os.path.exists(configLocalUrl):
            configUrl = configLocalUrl
        self.configUrl = configUrl
        self.read()
    def read(self):
        if not os.path.exists(self.configUrl):
            self.save()
        with open(self.configUrl, encoding="utf-8") as f:
            datas = yaml.load(f, Loader=yaml.FullLoader)
            self.parse(datas)
    
    def write(self, datas):
        if not os.path.exists(os.path.split(self.configUrl)[0]):
            os.makedirs(os.path.split(self.configUrl)[0])
        with open(self.configUrl, 'w+', encoding="utf-8") as f:
            yaml.dump(datas, f)
            self.parse(datas)
    
    def save(self):
        datas = self.toJson()
        if not os.path.exists(os.path.split(self.configUrl)[0]):
            os.makedirs(os.path.split(self.configUrl)[0])
        with open(self.configUrl, 'w+', encoding="utf-8") as f:
            yaml.dump(datas, f)

    def toJson(self):
        datas = {}
        fileConfig = {}
        fileConfig['echartPath'] = file.echartPath
        fileConfig['csvPath'] = file.csvPath
        fileConfig['pieFileName'] = file.pieFileName
        fileConfig['barFileName'] = file.barFileName
        fileConfig['lineFileName'] = file.lineFileName
        fileConfig['phoneDataFileName'] = file.phoneDataFileName
    
        scrapyConfig = {}
        scrapyConfig['maxPageNum'] = scrapy.maxPageNum
        scrapyConfig['pageStep'] = scrapy.pageStep
        scrapyConfig['pageScroll'] = scrapy.pageScroll
        scrapyConfig['timeInterval'] = scrapy.timeInterval
    
        sqlConfig = {}
        sqlConfig['host'] = sql.host
        sqlConfig['port'] = sql.port
        sqlConfig['user'] = sql.user
        sqlConfig['password'] = sql.password
        sqlConfig['database'] = sql.database
        sqlConfig['charset'] = sql.charset

        logConfig = {}
        logConfig['logShow'] = log.logShow
        logConfig['logLevel'] = log.logLevel
        logConfig['statementShow'] = log.statementShow
        logConfig['logPassword'] = log.logPassword
    
        datas['file'] = fileConfig
        datas['scrapy'] = scrapyConfig
        datas['sql'] = sqlConfig
        datas['log'] = logConfig
    
        return datas
    
    def parse(self, datas):
        fileConfig = datas['file']
        file.echartPath = fileConfig['echartPath']
        file.csvPath = fileConfig['csvPath']
        file.pieFileName = fileConfig['pieFileName']
        file.barFileName = fileConfig['barFileName']
        file.lineFileName = fileConfig['lineFileName']
        file.phoneDataFileName = fileConfig['phoneDataFileName']
    
        scrapyConfig = datas['scrapy']
        scrapy.maxPageNum = scrapyConfig['maxPageNum']
        scrapy.pageStep = scrapyConfig['pageStep']
        scrapy.pageScroll = scrapyConfig['pageScroll']
        scrapy.timeInterval = scrapyConfig['timeInterval']
    
        sqlConfig = datas['sql']
        sql.host = sqlConfig['host']
        sql.port = sqlConfig['port']
        sql.user = sqlConfig['user']
        sql.password = sqlConfig['password']
        sql.database = sqlConfig['database']
        sql.charset = sqlConfig['charset']

        logConfig = datas['log']
        if logConfig['logPassword'] != 'GCZ国粹章组':
            log.logShow = False
            log.logLevel = 'CRITICAL'
            log.statementShow = True
        else:
            log.logShow = logConfig['logShow']
            log.logLevel = logConfig['logLevel']
            log.statementShow = logConfig['statementShow']
        log.logPassword = logConfig['logPassword']

configEdit = configEdit()
