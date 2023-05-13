import os
import time

from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from config import config
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QUrl

from views.home import *

class UIHomeView(QWidget, Ui_Form):
    def __init__(self):
        super(UIHomeView, self).__init__()
        self.setupUi(self)
        self.initParams()
        self.initUI()
        self.initSlot()
        self.initMethod()
        self.initAction()

    def initParams(self):
        self.message = QtWidgets.QMessageBox  # 初始化消息弹框，information消息，critical失败

        self.logCount = 1
        self.lastLog = None
        self.image = None
        self.count = 0
        self.lastTime = time.time()
        self.videoWriter = None

    def btnClick(self, status, title, content):
        if status == self.tmsg.code.info:
            self.message.information(self, title, content)
        elif status == self.tmsg.code.error:
            self.message.critical(self, title, content)
        elif status == self.tmsg.code.warning:
            self.message.warning(self, title, content)

    def initAction(self):
        self.scrapyPBClickCallback = None
        self.clearTablePBClickCallback = None
        self.loadLocalDataPBClickCallback = None

        self.createChartPBClickCallback = None
        self.chartParamsPBClickCallback = None

    def initUI(self):
        # file = QtCore.QFile(':qss/qss/main.qss')
        # file.open(QtCore.QFile.ReadOnly)
        # styleSheet = file.readAll()
        # styleSheet = str(styleSheet)[1:]
        # self.setStyleSheet(styleSheet)

        self.view = QWebEngineView(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.gridLayout_3.addWidget(self.view, 0, 0, 1, 1)
        self.label.close()

        self.view_2 = QWebEngineView(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.view_2.sizePolicy().hasHeightForWidth())
        self.view_2.setSizePolicy(sizePolicy)
        self.gridLayout_7.addWidget(self.view_2, 0, 0, 1, 1)
        self.label_3.close()

        self.view_3 = QWebEngineView(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.view_3.sizePolicy().hasHeightForWidth())
        self.view_3.setSizePolicy(sizePolicy)
        self.gridLayout_4.addWidget(self.view_3, 0, 0, 1, 1)
        self.label_4.close()

        self.tableWidget.horizontalHeader().setStyleSheet( "QHeaderView::section{background-color:rgb(155, 194, 230);font:11pt '宋体';color: black;};")
        self.tableWidget.verticalHeader().setStyleSheet( "QHeaderView::section{background-color:rgb(155, 194, 230);font:11pt '宋体';color: black;};")

    def initSlot(self):
        self.pushButton_2.clicked.connect(lambda: self.scrapyPBClick(self.pushButton_2.text()))
        self.pushButton_6.clicked.connect(lambda: self.clearTablePBClickPBClick(self.pushButton_6.text()))
        self.pushButton_3.clicked.connect(lambda: self.loadLocalDataPBClick(self.pushButton_3.text()))
        self.pushButton.clicked.connect(lambda: self.openCsvPath(self.pushButton.text()))
        self.initLightSlot([1, 2, 3])

    def initLightSlot(self, lis):
        def initLightSlot(index):
            eval(f'self.light{index}_swich_PB').clicked.connect(lambda: self.createChartPBClick(index, eval(f'self.light{index}_swich_PB').text()))
            eval(f'self.light{index}_1_PB').clicked.connect(lambda: self.chartParamsPBClick(index, 1, f"{eval(f'self.light{index}_swich_PB').text()}_{eval(f'self.light{index}_1_PB').text()}"))
            eval(f'self.light{index}_2_PB').clicked.connect(lambda: self.chartParamsPBClick(index, 2, f"{eval(f'self.light{index}_swich_PB').text()}_{eval(f'self.light{index}_1_PB').text()}"))
            eval(f'self.light{index}_3_PB').clicked.connect(lambda: self.chartParamsPBClick(index, 3, f"{eval(f'self.light{index}_swich_PB').text()}_{eval(f'self.light{index}_1_PB').text()}"))
            eval(f'self.light{index}_4_PB').clicked.connect(lambda: self.chartParamsPBClick(index, 4, f"{eval(f'self.light{index}_swich_PB').text()}_{eval(f'self.light{index}_1_PB').text()}"))
        for index in lis:
            initLightSlot(index)

    def initMethod(self):
        pass

    # region setUI
    def setUI(self, data):
        charts = {'pie': 1, 'bar': 2, 'line': 3}
        for key in data:
            value = data[key]
            self.setLightUI(charts[key], value)

        self.setPyEchartUI()

    def setPyEchartUI(self, data=[1, 2, 3]):
        # 加载 html 文件并在 pyqt 窗口中显示
        fileUrl = config.file
        if 1 in data:
            pieurl = QUrl(f"file:///{fileUrl.echartPath}{fileUrl.pieFileName}.html")
            self.view.load(pieurl)
            self.view.setZoomFactor(0.5)
        if 2 in data:
            barurl = QUrl(f"file:///{fileUrl.echartPath}{fileUrl.barFileName}.html")
            self.view_2.load(barurl)
            self.view_2.setZoomFactor(0.5)
        if 3 in data:
            lineurl = QUrl(f"file:///{fileUrl.echartPath}{fileUrl.lineFileName}.html")
            self.view_3.load(lineurl)
            self.view_3.setZoomFactor(0.5)

    def setTableUI(self, data):
        currentRowCount = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(currentRowCount+1)
        titleList = list(
            'title,price,business,evaluate,image_url,business_url,brond,goods_title,goods_id,goods_district,goods_weight,goods_cpu,play_memory,goods_color,goods_power,goods_memory,three_criterion,chromatic_system,screen_material,resolving_power,pixel,style'.split(
                ','))
        for i in range(0, len(data)):
            self.tableWidget.setItem(currentRowCount, i, QTableWidgetItem(str(data[titleList[i]])))

    def setLightUI(self, chart, params):
        index = 0
        for i in range(1, 5):
            if chart != 1:
                statue = i in params[0:2]
                if i == params[0]:
                    index = 0
                else:
                    index = 1
            else:
                index = 0
                statue = i == params
            if statue:
                if index:
                    exec(f'self.light{chart}_{i}_PB.setStyleSheet("background-color: rgb(255,204,0);color: rgb(255, 255, 255);")')
                else:
                    exec(
                        f'self.light{chart}_{i}_PB.setStyleSheet("background-color: rgb(153,204,0);color: rgb(255, 255, 255);")')
            else:
                exec(f'self.light{chart}_{i}_PB.setStyleSheet("background-color: rgb(153,153,153);color: rgb(255, 255, 255);")')
    # endregion

    # region Slot
    def openCsvPath(self, btnName):
        self.printLog(f"点击了{btnName}按钮")
        dirs = config.file.csvPath
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        os.startfile(dirs)

    def scrapyPBClick(self, btnName):
        self.printLog(f"点击了{btnName}按钮")
        if (btnName == "开始爬取"):
            titleList = (
                'title,price,business,evaluate,image_url,business_url,brond,goods_title,goods_id,goods_district,goods_weight,goods_cpu,play_memory,goods_color,goods_power,goods_memory,three_criterion,chromatic_system,screen_material,resolving_power,pixel,style'.split(
                    ','))
            self.tableWidget.setColumnCount(len(titleList))
            self.tableWidget.setHorizontalHeaderLabels(titleList)
            self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "border: 0px;")
            self.pushButton_2.setText("终止爬取")
            statue = True
        else:
            self.pushButton_2.setText("开始爬取")
            statue = False
        # self.message.information(self, "消息提示", f"点击了{btnName}按钮")
        if self.scrapyPBClickCallback:
            self.scrapyPBClickCallback(statue)

    def clearTablePBClickPBClick(self, btnName):
        self.printLog(f"点击了{btnName}按钮")
        # self.message.information(self, "消息提示", f"点击了{btnName}按钮")
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border: 0px;\n"
                                       "border-image: url(:/img/img/jpg/bg.jpg);")
        if self.clearTablePBClickCallback:
            self.clearTablePBClickCallback()

    def loadLocalDataPBClick(self, btnName):
        self.printLog(f"点击了{btnName}按钮")
        # self.message.information(self, "消息提示", f"点击了{btnName}按钮")
        titleList = (
            'title,price,business,evaluate,image_url,business_url,brond,goods_title,goods_id,goods_district,goods_weight,goods_cpu,play_memory,goods_color,goods_power,goods_memory,three_criterion,chromatic_system,screen_material,resolving_power,pixel,style'.split(
                ','))
        self.tableWidget.setColumnCount(len(titleList))
        self.tableWidget.setHorizontalHeaderLabels(titleList)
        self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border: 0px;")
        if self.loadLocalDataPBClickCallback:
            self.loadLocalDataPBClickCallback()

    def createChartPBClick(self, index, btnName):
        self.printLog(f"点击了{btnName}按钮")
        # self.message.information(self, "消息提示", f"点击了{btnName}按钮")
        if self.createChartPBClickCallback:
            self.createChartPBClickCallback(index)

    def chartParamsPBClick(self, index, value, btnName):
        self.printLog(f"点击了{btnName}按钮")
        # self.message.information(self, "消息提示", f"点击了btnName按钮")
        if self.chartParamsPBClickCallback:
            self.chartParamsPBClickCallback(index, value)

    # endregion

    def printLog(self, msg):
        if self.lastLog == msg:
            self.logCount = self.logCount + 1
            msg += f' * {self.logCount}'
        else:
            self.logCount = 1
            self.lastLog = msg
        self.label_2.setText(msg)
        if config.log.logShow: print(msg)
