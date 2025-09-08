from PySide2 import QtCore, QtGui, QtWidgets


class MyCalendar(QtWidgets.QCalendarWidget):

    focus_date_list = [
        '2023-02-10',
        '2023-02-11',
        '2023-02-12',
    ]

    def __init__(self, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if str(date.toString("yyyy-MM-dd")) in self.focus_date_list:
            painter.setPen(QtGui.QColor(255, 61, 64))
            painter.drawText(rect.center(), " *")
