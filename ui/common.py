#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from datetime import date

from PyQt4.QtCore import (Qt, QSize)
from PyQt4.QtGui import (QMainWindow, QLabel, QIcon, QLineEdit, QCommandLinkButton,
                         QPalette, QDateTimeEdit, QFont, QWidget, QTabBar,
                         QTextEdit, QColor, QIntValidator, QDoubleValidator)
from PyQt4.QtGui import QGridLayout, QGroupBox
from tools.periods import Period
from configuration import Config


class FMainWindow(QMainWindow):
    def __init__(self, parent=0, *args, **kwargs):
        QMainWindow.__init__(self)

        self.wc = 1100
        self.hc = 600
        self.resize(self.wc, self.hc)
        self.setWindowTitle(Config.NAME_ORGA)
        self.setWindowIcon(QIcon(Config.APP_LOGO))

    def change_context(self, context_widget, *args, **kwargs):

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.setWindowOpacity(0.90)
        d.exec_()


class F_Widget(QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QWidget.__init__(self, parent=parent, *args, **kwargs)
        self.pp = parent
        self.setMaximumWidth(self.pp.wc)

        css = """
            QWidget{
                border: 1px solid #dff;
                border-radius: 5px 5px 5px 5px;
                color: red;
                }
            """
        # self.setStyleSheet(css)

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.parentWidget().change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, modal=modal, *args, **kwargs)


class PyTextViewer(QTextEdit):

    # Initialise the instance.
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)

        self.setReadOnly(True)


class TabPane(QTabBar):

    def __init__(self, parent=None):
        super(TabPane, self).__init__(parent)

        css = """
        TabPane{
            border: 1px solid;
            border-radius: 20px 30px 2px;
        }
        Button_menu:hover{
            Background: #000;
            font-size:11px;
        }
        """
        # self.setStyleSheet(css)

    def addBox(self, box):
        self.setLayout(box)


class F_PageTitle(QLabel):

    def __init__(self, *args, **kwargs):
        super(F_PageTitle, self).__init__(*args, **kwargs)
        # self.setFont(QFont("Times New Roman", 50))
        css = """border-top-color: red; border:1px solid Gray;
                 font: 75 12pt 'URW Bookman L'; border-radius: 4px 14px 4px 4px;
                 gridline-color: rgb(255, 255, 255);"""
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(css)


class F_BoxTitle(QLabel):

    def __init__(self, *args, **kwargs):
        super(F_BoxTitle, self).__init__(*args, **kwargs)
        self.setFont(QFont("Times New Roman", 12, QFont.Bold, True))
        self.setAlignment(Qt.AlignLeft)


class Button(QCommandLinkButton):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setCursor(Qt.PointingHandCursor)
        # self.setCursor(Qt.ForbiddenCursor)
        # self.setFixedSize(100, 40)

        self.setFont(QFont("Comic Sans MS", 13, QFont.Bold, True))

        # self.setCheckable(True)


class Button_rond(Button):

    def __init__(self, *args, **kwargs):
        super(Button_rond, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img='save.png'))))
        css = """
                border-radius:9px;

                border:1px solid #4b8f29;

                color:#ffffff;
                font-family:arial;
                font-size:13px;
                font-weight:bold;
                padding:6px 12px;

        """
        self.setStyleSheet(css)


class Deleted_btt(Button):

    def __init__(self, *args, **kwargs):
        super(Deleted_btt, self).__init__(*args, **kwargs)
        # self.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      # img='save.png'))))
        css = """
                background-color:#fc8d83;
                border-radius:6px;
                border:1px solid #d83526;
                color:#ffffff;
                font-family:arial;
                font-size:15px;
                font-weight:bold;
                padding:6px 24px;
                text-decoration:none;
                """
        self.setStyleSheet(css)


class Warning_btt(Button):

    def __init__(self, *args, **kwargs):
        super(Warning_btt, self).__init__(*args, **kwargs)
        # self.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      # img='save.png'))))
        css = """
                    background-color:#ffec64;
                    border-radius:6px;
                    border:1px solid #ffaa22;
                    color:#333333;
                    font-family:arial;
                    font-size:15px;
                    font-weight:bold;
                    padding:6px 24px;

                """
        self.setStyleSheet(css)


class Button_save(Button):

    def __init__(self, *args, **kwargs):
        super(Button_save, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img='save.png'))))
        css = """
        background-color:#dbe6c4;
        border-radius:6px;
        border:1px solid #b2b8ad;
        color:#757d6f;
        font-family:arial;
        font-size:15px;
        font-weight:bold;
        padding:6px 24px;
        """
        self.setStyleSheet(css)
        self.setIconSize(QSize(20, 20))
        self.setFocusPolicy(Qt.TabFocus)
        font = QFont()
        font.setBold(True)


class Button_menu(Button):

    def __init__(self, *args, **kwargs):
        super(Button_menu, self).__init__(*args, **kwargs)

        # self.setFont(QFont("Times New Roman", 20))
        # self.setStyleSheet("width: 20px;")
        self.setIconSize(QSize(80, 80))
        self.setFocusPolicy(Qt.TabFocus)
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        # font.setWeight(40)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.setFont(font)


class Button_export(Button):

    def __init__(self, *args, **kwargs):
        super(Button_export, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('xls', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img='xls.png'))))


class ErrorLabel(QLabel):

    def __init__(self, text, parent=None):
        QLabel.__init__(self, text, parent)
        font = QFont()
        self.setFont(font)
        red = QColor(Qt.red)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, red)
        self.setPalette(palette)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FormatDate(QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super(FormatDate, self).__init__(*args, **kwargs)
        self.setDisplayFormat(u"dd/MM/yyyy")
        self.setCalendarPopup(True)


class FormLabel(QLabel):

    def __init__(self, text, parent=None):
        QLabel.__init__(self, text, parent)
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)


class LineEdit(QLineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        css = """
        LineEdit {
            border: 1px solid #dff;
            border-radius: 5px 5px 5px 5px;
        """
        # self.setStyleSheet(css)


class IntLineEdit(LineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        LineEdit.__init__(self, parent)
        self.setValidator(QIntValidator(0, 100000000, self))


class FloatLineEdit(LineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        LineEdit.__init__(self, parent)
        self.setValidator(QDoubleValidator(0.1, 0.1, 100, self))


class F_PeriodHolder(object):

    def __init__(self, main_date=date.today(), *args, **kwargs):
        self.duration = "week"
        self.main_date = Period(main_date.year, self.duration, main_date.isocalendar()[1])
        self.periods_bar = self.gen_bar_for(self.main_date)

    def gen_bar_for(self, main_date):
        return F_PeriodTabBar(parent=self, main_date=self.main_date)

    def change_period(self, main_date):
        self.main_date = main_date

    def getmain_date(self):
        return self._main_date

    def setmain_date(self, value):
        self._main_date = value

    main_date = property(getmain_date, setmain_date)


class F_PeriodTabBar(QTabBar):

    def __init__(self, parent, main_date, *args, **kwargs):

        super(F_PeriodTabBar, self).__init__(*args, **kwargs)

        for i in range(0, 3):
            self.addTab(u"{}".format(i))
        self.set_data_from(main_date)
        self.build_tab_list()

        self.currentChanged.connect(self.changed_period)

    def set_data_from(self, period):

        self.main_period = Period(period.year, period.duration, period.duration_number)
        self.periods = [self.main_period.previous, self.main_period.current, self.main_period.next]

    def build_tab_list(self):
        for index, period in enumerate(self.periods):
            self.setTabText(index, str(period.display_name()))
            self.setTabToolTip(index, unicode(period))
        self.setTabTextColor(1, QColor('SeaGreen'))
        self.setCurrentIndex(1)

    def changed_period(self, index):
        if index == -1 or index == 1:
            return False
        else:
            np = self.periods[index]
            self.set_data_from(np)
            self.build_tab_list()
            self.parentWidget().main_date = np
            self.parentWidget().change_period(np)


class EnterDoesTab(QWidget):

    def keyReleaseEvent(self, event):
        super(EnterDoesTab, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_Return:
            self.focusNextChild()


class EnterTabbedLineEdit(LineEdit, EnterDoesTab):
    pass
