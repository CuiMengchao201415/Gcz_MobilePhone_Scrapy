import os

import pymysql
from PyQt5.QtWidgets import QWidget
from gcz_common.config import config
from gcz_pyqt.views.setting import *


class UISettingView(QWidget, Ui_Form):
    def __init__(self):
        super(UISettingView, self).__init__()
        self.setupUi(self)
        self.initParams()
        self.initSlot()
        self.initUi()

    def initParams(self):
        self.message = QtWidgets.QMessageBox  # 初始化消息弹框，information消息，critical失败

    def initUi(self):
        self.lineEdit.setText(str(config.file.echartPath))
        self.lineEdit_2.setText(str(config.file.csvPath))
        self.lineEdit_3.setText(str(config.file.pieFileName))
        self.lineEdit_18.setText(str(config.file.barFileName))
        self.lineEdit_19.setText(str(config.file.lineFileName))
        self.lineEdit_20.setText(str(config.file.phoneDataFileName))

        self.lineEdit_5.setText(str(config.scrapy.maxPageNum))
        self.lineEdit_13.setText(str(config.scrapy.pageStep))
        self.lineEdit_4.setText(str(config.scrapy.pageScroll))
        self.lineEdit_6.setText(str(config.scrapy.timeInterval))

        self.lineEdit_7.setText(str(config.sql.host))
        self.lineEdit_8.setText(str(config.sql.port))
        self.lineEdit_9.setText(str(config.sql.user))
        self.lineEdit_10.setText(str(config.sql.password))
        self.lineEdit_12.setText(str(config.sql.database))
        self.lineEdit_11.setText(str(config.sql.charset))

        self.lineEdit_14.setText(str(config.log.logShow))
        self.lineEdit_15.setText(str(config.log.logLevel))
        self.lineEdit_16.setText(str(config.log.statementShow))
        self.lineEdit_17.setText(str(config.log.logPassword))

    def initSlot(self):
        self.pushButton.clicked.connect(lambda: self.selectPath('echart'))
        self.pushButton_5.clicked.connect(lambda: self.selectPath('csv'))
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton_4.clicked.connect(self.check)
        self.pushButton_3.clicked.connect(self.save)

    def selectPath(self, name):
        """
        选择文件保存路径
        :return:
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选择文件夹", "/")
        if not directory: return
        if (name == 'echart'):
            self.lineEdit.setText(directory+'/')
        else:
            self.lineEdit_2.setText(directory + '/')

    def reset(self):
        res = self.message.question(self, "询问", "是否重置当前配置", self.message.Yes | self.message.No)
        if (res == self.message.No):
            return

        self.initParams()
        self.initUi()
        self.message.information(self, "提示", "重置当前配置成功", self.message.Ok)

    def check(self):
        res = self.message.question(self, "询问", "是否检查当前配置可用性", self.message.Yes | self.message.No)
        if (res == self.message.No):
            return

        host = self.lineEdit_7.text()
        port = self.lineEdit_8.text()
        user = self.lineEdit_9.text()
        password = self.lineEdit_10.text()
        database = self.lineEdit_12.text()
        charset = self.lineEdit_11.text()
        try:
            conn = pymysql.connect(db=database,
                                           host=host,
                                           user=user,
                                           password=password,
                                           port=int(port),
                                           charset=charset)
            conn.close()
            self.message.information(self, "提示", "数据库可用", self.message.Ok)
        except:
            self.message.critical(self, "提示", "数据库不可用", self.message.Ok)

        exit_code = os.system('ping www.baidu.com')
        if not exit_code:
            self.message.information(self, "提示", "网络通信可用", self.message.Ok)
        else:
            self.message.critical(self, "提示", "网络通信不可用", self.message.Ok)


    def save(self):
        res = self.message.question(self, "询问", "是否保存当前配置", self.message.Yes | self.message.No)
        if (res == self.message.No):
            return

        datas = {}
        fileConfig = {}
        fileConfig['echartPath'] = self.lineEdit.text()
        fileConfig['csvPath'] = self.lineEdit_2.text()
        fileConfig['pieFileName'] = self.lineEdit_3.text()
        fileConfig['barFileName'] = self.lineEdit_18.text()
        fileConfig['lineFileName'] = self.lineEdit_19.text()
        fileConfig['phoneDataFileName'] = self.lineEdit_20.text()

        scrapyConfig = {}
        scrapyConfig['maxPageNum'] = int(self.lineEdit_5.text())
        scrapyConfig['pageStep'] = int(self.lineEdit_13.text())
        scrapyConfig['pageScroll'] = int(self.lineEdit_4.text())
        scrapyConfig['timeInterval'] = int(self.lineEdit_6.text())

        sqlConfig = {}
        sqlConfig['host'] = self.lineEdit_7.text()
        sqlConfig['port'] = int(self.lineEdit_8.text())
        sqlConfig['user'] = self.lineEdit_9.text()
        sqlConfig['password'] = self.lineEdit_10.text()
        sqlConfig['database'] = self.lineEdit_12.text()
        sqlConfig['charset'] = self.lineEdit_11.text()

        logConfig = {}
        logConfig['logShow'] = self.lineEdit_14.text() == "True"
        logConfig['logLevel'] = self.lineEdit_15.text()
        logConfig['statementShow'] = self.lineEdit_16.text() == "True"
        logConfig['logPassword'] = self.lineEdit_17.text()

        datas['file'] = fileConfig
        datas['scrapy'] = scrapyConfig
        datas['sql'] = sqlConfig
        datas['log'] = logConfig

        config.configEdit.write(datas)

        self.message.information(self, "提示", "保存当前配置成功，部分配置重启应用后生效", self.message.Ok)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UISettingView()
    ui.show()
    sys.exit(app.exec_())