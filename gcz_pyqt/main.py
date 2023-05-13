import os
import sys
from views.UILauncherView import *

class main:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        ui = UILauncherView()
        ui.show()
        os._exit(app.exec_())