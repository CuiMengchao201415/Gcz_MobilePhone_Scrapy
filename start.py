import sys
import os
sys.path.append(os.path.dirname(__file__)+"/gcz_pyqt")
sys.path.append(os.path.dirname(__file__)+"/gcz_common")
sys.path.append(os.path.dirname(__file__)+"/resources")
sys.path.append(os.path.dirname(__file__)+"/gcz_scrapy")


if __name__ == '__main__':
    from gcz_pyqt.main import main
    main()


