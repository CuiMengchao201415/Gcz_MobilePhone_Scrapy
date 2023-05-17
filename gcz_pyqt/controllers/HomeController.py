import random
from multiprocessing import Pipe

import pandas
from pyecharts.charts import Line, Bar, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

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
        self.chartsParams = {'pie': 1, 'bar': [1, 2, 0], 'line': [1, 2, 0]}
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
        for item in data:
            self.ui.setTableUI(item)

    def createChartPBClickCallback(self, type):
        types = ['pie', 'bar', 'line', "饼图", "柱状图", "折线图"]
        params = ["price", "brond", "goods_memory", "play_memory"]
        if self.original==None or len(self.original) == 0:
            self.ui.printLog(f"数据为空，无法生成{types[int(int(type)+2)]}！")
            return
        chart = types[type-1]
        if type == 1:
            if self.chartsParams[chart] == 1:
                if self.priceCount and random.randint(0, 1):
                    PieCount = self.priceCount
                else:
                    PieCount = analysePhonePricePieCount(self.original)
                pie_set_colors(PieCount)
            else:
                PieCount = analysePhonePieCount(self.original, params[self.chartsParams[chart]-1])
                pie_set_colors(PieCount)

        else:
            if 1 in self.chartsParams[chart][0:2]:
                param = 2
                for i in self.chartsParams[chart][0:2]:
                    if i != 1: param = i
                priceCount, brondCount = analysePhonePriceCount(self.original, params[param-1])
                self.priceCount = priceCount
                if type == 2:
                    bar_base_dict_config(brondCount)
                else:
                    line_base(brondCount)
            else:
                count = analysePhoneCount(self.original, [params[self.chartsParams[chart][0:2][0]-1], params[self.chartsParams[chart][0:2][1]-1]])
                if type == 2:
                    bar_base_dict_config(count)
                else:
                    line_base(count)
        self.ui.setPyEchartUI([type])

    def chartParamsPBClickCallback(self, type, params):
        types = ['pie', 'bar', 'line', "饼图", "柱状图", "折线图"]
        if type==1:
            self.chartsParams[types[type-1]] = params
        else:
            temp = self.chartsParams[types[type-1]][2]
            if params == self.chartsParams[types[type-1]][0] or params == self.chartsParams[types[type-1]][1]:
                return
            self.chartsParams[types[type-1]][temp % 2] = params
            self.chartsParams[types[type-1]][2] += 1

        self.ui.setLightUI(type, self.chartsParams[types[type-1]])
    # endregion


def analysePhonePricePieCount(data):
    """
    根据手机价格统计手机数量
    :param data:
    :return:
    """
    count = {"低端机": 0, "中端机": 0, "高端机": 0}
    for item in data:
        try:
            price = float(item['price'])
        except Exception as e:
            continue
        if price < 2000:
            count['低端机'] += 1
        elif price < 5000:
            count['中端机'] += 1
        else:
            count['高端机'] += 1
    return count

def analysePhonePieCount(data, param):
    """
    根据商品某一属性统计商品数量
    :param data:
    :param param:
    :return:
    """
    count = {}
    for item in data:
        try:
            temp = item[param]
        except Exception as e:
            continue
        if temp in count:
            count[temp] += 1
        else:
            count[temp] = 1
    return count


def dictCountAdd1(data, key1, key2, value1):
    if key1 not in data.keys():
        data[key1] = value1.copy()
    if key2 in data[key1]:
        data[key1][key2] += 1
    else:
        data[key1][key2] = 1


def analysePhonePriceCount(data, param="brond"):
    """
    根据商品价格和商标统计数量
    :param data:
    :param param:
    :return:
    """
    priceCount = {'0-999': 0, '1000-1999': 0, '2000-2999': 0, '3000-4999': 0, '5000-9999': 0, '1万+': 0}
    defaultPriceCount = {'0-999': 0, '1000-1999': 0, '2000-2999': 0, '3000-4999': 0, '5000-9999': 0, '1万+': 0}
    brondCount = {}

    for item in data:
        try:
            price = float(item['price'])
            brond = item[param]
            if param == 'brond':
                if brond not in ["Apple", "华为（HUAWEI）", "小米（MI）", "荣耀（HONOR）", "vivo", "OPPO"]:
                    brond = "杂牌"
        except Exception as e:
            continue

        if price < 1000:
            key = '0-999'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        elif price < 2000:
            key = '1000-1999'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        elif price < 3000:
            key = '2000-2999'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        elif price < 5000:
            key = '3000-4999'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        elif price < 10000:
            key = '5000-9999'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
        else:
            key = '1万+'
            priceCount[key] += 1
            dictCountAdd1(brondCount, brond, key, defaultPriceCount)
    return priceCount, brondCount

def analysePhoneCount(data, params=['brond', 'play_memory']):
    """
    根据商品任意两个属性统计商品数量
    :param data:
    :param params:
    :return:
    """
    count = {}
    defaultCount = {}
    if params[0] == 'brond': defaultCount = {'Apple': 0, '华为（HUAWEI）': 0, '小米（MI）': 0, '荣耀（HONOR）': 0, 'vivo': 0, 'OPPO': 0, '杂牌': 0}
    if params[0] == 'play_memory': defaultCount = {'未公布': 0, '4GB及以下': 0, '6GB': 0, '8GB': 0, '12GB': 0, '16GB': 0, '无': 0,
                                             'OPPO': 0, '杂牌': 0}
    if params[0] == 'goods_memory': defaultCount = {'64GB及以下': 0, '128GB': 0, '256GB': 0, '512GB': 0, '1TB': 0, '无': 0,
                                             'OPPO': 0, '杂牌': 0}
    for item in data:
        try:
            param1 = item[params[0]]
            param2 = item[params[1]]
            if params[0] == 'brond':
                if param1 not in ["Apple", "华为（HUAWEI）", "小米（MI）", "荣耀（HONOR）", "vivo", "OPPO"]:
                    param1 = "杂牌"
            if params[1] == 'brond':
                if param2 not in ["Apple", "华为（HUAWEI）", "小米（MI）", "荣耀（HONOR）", "vivo", "OPPO"]:
                    param2 = "杂牌"
        except Exception as e:
            continue

        if param2 not in count:
            count[param2] = defaultCount.copy()
        if param1 in count[param2]:
            count[param2][param1] += 1
        else:
            count[param2][param1] = 1

    return count

def pie_set_colors(data):
    """
    生成饼状图
    :param data:
    :return:
    """
    if type(data) == dict:
        data = [list(z) for z in zip(data.keys(), data.values())]
    pie = (
        Pie()
        .add("", data)
        # .set_colors(["blue", "green", "yellow", "red", "pink","orange"])
        # .set_colors(["blue", "green", "yellow"])
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图"))
    )
    pie.render(config.file.echartPath+config.file.pieFileName+".html")

def bar_base_dict_config(data):
    """
    生成柱状图
    :param data:
    :return:
    """
    if type(data) == dict:
        xaxis = list(data[list(data.keys())[0]].keys())
        yaxis = []
        for key in data.keys():
            yaxis.append({"key": key, "values": list(data[key].values())})
    else:
        xaxis = data['xaxis']
        yaxis = data['yaxis']
    bar = Bar({"theme": ThemeType.MACARONS})
    bar.add_xaxis(xaxis)
    for item in yaxis:
        bar.add_yaxis(item["key"], item["values"])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱状图"))
    bar.render(config.file.echartPath+config.file.barFileName+".html")

def line_base(data):
    """
    生成折线图
    :param data:
    :return:
    """
    if type(data) == dict:
        xaxis = list(data[list(data.keys())[0]].keys())
        yaxis = []
        for key in data.keys():
            yaxis.append({"key": key, "values": list(data[key].values())})
    else:
        xaxis = data['xaxis']
        yaxis = data['yaxis']

    line = Line()
    line.add_xaxis(xaxis)
    for item in yaxis:
        line.add_yaxis(item["key"], item["values"])
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图"))

    line.render(config.file.echartPath+config.file.lineFileName+".html")


