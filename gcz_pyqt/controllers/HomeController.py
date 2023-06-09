import random
from multiprocessing import Pipe

import pandas

from gcz_common.config import config
from gcz_common.core.analyse import *
from gcz_common.utils.thread.ThreadUtil import ThreadUtil
from gcz_common.utils.process.ProcessUtil import ProcessUtil
from gcz_pyqt.views.UIHomeView import *
from gcz_scrapy.main import crawlerProcess


class HomeController:
    def __init__(self):
        self.ui = UIHomeView()
        self.ui.showMaximized()
        self.ui.scrapyPBClickCallback = self.scrapyPBClickCallback
        self.ui.clearTablePBClickCallback = self.clearTablePBClickCallback
        self.ui.loadLocalDataPBClickCallback = self.loadLocalDataPBClickCallback
        self.ui.createChartPBClickCallback = self.createChartPBClickCallback
        self.ui.chartParamsPBClickCallback = self.chartParamsPBClickCallback

        self.process = ProcessUtil(config.log.statementShow)
        self.thread = ThreadUtil(config.log.statementShow)

        (self.pipes, self.piper) = Pipe()

        self.thread.startThread(self.phoneDatasRecv)
        self.original = []
        self.chartsParams = {'pie': 1, 'bar': 1, 'line': 1}
        self.ui.setUI(self.chartsParams)
        self.priceCount = None

    # region 委托
    def phoneDatasRecv(self):
        while True:
            data = self.piper.recv()
            self.original.append(data)
            self.ui.setTableUI(data)

    def analysePhonePriceCount(self, data):
        count = {"lower": 0, "medium": 0, "higher": 0}
        for item in data:
            price = item['price']
            if price < 2000:
                count['lower'] += 1
            elif price < 4000:
                count['medium'] += 1
            else:
                count['biger'] += 1
        self.phonePriceCount = count

    def analysePhoneBrondCount(self, data):
        count = {}
        for item in data:
            price = item['price']
            if price < 2000:
                count['lower'] += 1
            elif price < 4000:
                count['medium'] += 1
            else:
                count['biger'] += 1
        self.phonePriceCount = count
    # endregion

    # region 按钮点击回调
    def scrapyPBClickCallback(self, statue):
        if statue: self.process.startProcess(crawlerProcess, args=(self.pipes,))
        else: self.process.stopProcess()

    def clearTablePBClickCallback(self):
        self.original = []

    def loadLocalDataPBClickCallback(self):
        if not os.path.exists(f'{config.file.csvPath}{config.file.phoneDataFileName}.csv'):
            self.ui.printLog(f"无本地数据，导入失败！")
            return
        data = pandas.read_csv(f'{config.file.csvPath}{config.file.phoneDataFileName}.csv')
        data = eval(data.to_json(orient="records", force_ascii=False))
        self.original = data
        def fun():
            for item in data:
                self.ui.setTableUI(item)
        self.thread.startThread(fun)
    def createChartPBClickCallback(self, type):
        types = ['pie', 'bar', 'line', "饼图", "柱状图", "折线图"]
        params = ["goods_memory", "play_memory"]
        params_pie = ['全部价位', '低端机', '中端机', '高端机']
        if self.original==None or len(self.original) == 0:
            self.ui.printLog(f"数据为空，无法生成{types[int(int(type)+2)]}！")
            return
        chart = types[type-1]
        if type == 1:
            PieCount = analysePhonePricePieCount(self.original)
            pie_set_colors(PieCount[params_pie[self.chartsParams[chart]-1]])
        else:
            priceCount, brondCount = analysePhonePriceCount(self.original, params[self.chartsParams[chart]%2-1])

            if type==2:
                bar_base_dict_config(brondCount)
            if type==3:
                scatter1(priceCount, self.chartsParams[chart])
        self.ui.setPyEchartUI([type])

    def chartParamsPBClickCallback(self, type, params):
        types = ['pie', 'bar', 'line', "饼图", "柱状图", "折线图"]

        self.chartsParams[types[type-1]] = params

        self.ui.setLightUI(type, self.chartsParams[types[type-1]])
    # endregion


