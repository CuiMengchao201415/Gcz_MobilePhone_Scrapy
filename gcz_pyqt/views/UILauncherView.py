import os
from PyQt5.QtWidgets import QWidget
from views.launcher import *
from controllers.HomeController import HomeController
from views.UISettingView import UISettingView

class UILauncherView(QWidget, Ui_Form):
    def __init__(self):
        super(UILauncherView, self).__init__()
        self.setupUi(self)
        self.uiSettingView = UISettingView()
        self.initSlot()

    def initSlot(self):
        self.pushButton_2.clicked.connect(self.toSetting)
        self.pushButton.clicked.connect(self.toHome)

    def toSetting(self):
        self.uiSettingView.show()

    def toHome(self):
        HomeController()
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UILauncherView()
    ui.show()
    os._exit(app.exec_())