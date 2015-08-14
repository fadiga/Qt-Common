###############################
#                             #
#  Coded By: Ibrihima Fadiga  #
#  Original: 10/08/15         #
#  File: style CSS PyQt       #
###############################

from models import SettingsAdmin


class CSS(object):

    """docstring for CSS"""

    # def __init__(self, arg):
    #     super(CSS, self).__init__()
    #     self.arg = arg

    qtabbar = """
            /*QTabWidget::tab-bar {
                alignment: center;
            }*/
            QTabBar::tab {
               background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 2px solid #C4C4C3;
                border-bottom-color: #C2C7CB;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }
            QTabBar::tab:selected {
                border-color: #9B9B9B;
                border-bottom-color: #C2C7CB;
            }
        """
    _cstyle = """{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #AB6D40, stop: 1 #000);
                  color: #EBEBEB;}
    """
    appStyle_fat = ("""QMainWindow{background-color: #E5E5E5;}
                    QToolBar {background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E5E5E5, stop: 1 #7A7A7A); color: #fff;}
                    QMenuBar """ + _cstyle + """
                    QMenuBar::item """ + _cstyle + """
                    QMenuBar::item::selected """ + _cstyle + """
                    QMenu {background-color: #7A7A7A;color: rgb(255,255,255);}
                    QMenu::item::selected """ + _cstyle + """
                    QLineEdit {background-color: #DADADA;}
                    QTableView {selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 #AB6D40, stop: 1 #000);background-color: #CACACA;}
                    QDialog  """ + _cstyle
                    )
    _cstyle = """{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #B6B6B6, stop: 1 #2A211C);
                  color: rgb(255,255,255);}"""
    appStyle_kadi = ("""
        QMainWindow{background-color: #E5E5E5;}
        QToolBar """ + _cstyle + """
        QMainWindow  """ + _cstyle + """
        QMenuBar """ + _cstyle + """
        QMenuBar::item """ + _cstyle + """
        QMenuBar::item::selected {background-color: rgb(30,30,30);}
        QMenu {background-color: #7A7A7A;color: rgb(255,255,255);}
        QMenu::item::selected {background-color: rgb(30,30,30);}
        QLineEdit {background-color: #DADADA;}
        QLabel {color: #f4f4f4; font-weight: bold;}
        QTableView {
            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                        stop: 0 #B6B6B6, stop: 1 #B6B6B6);
            background-color: #7A7A7A;
        }
        QDialog  """ + _cstyle + qtabbar
                     )

    appStyle = ""

    dict_style = {1: appStyle, 2: appStyle_fat, 3: appStyle_kadi}
    # list_style = [(i) for i in dict_style.keys()]
    appStyle = dict_style.get(SettingsAdmin.get(id=1).style_number)
