from PySide2 import QtCore, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *


def paintEvent(main_object, event):
    left_x = 12
    top_y = 276
    # 绘制准备工作，启用反锯齿
    painter = QPainter(main_object)
    painter.setRenderHints(QtGui.QPainter.Antialiasing)
    painter.setPen(QtCore.Qt.NoPen)
    # 先画圆角矩形背景
    background_rect_gradient = QConicalGradient(50, 50, 91)
    background_rect_gradient.setColorAt(0, QColor(255, 255, 255, 240))
    background_rect_gradient.setColorAt(1, QColor(255, 255, 255, 240))
    rectPath = QPainterPath()
    rectPath.addRoundedRect(QRectF(left_x, top_y, 181 + 24, 154), 10, 10)
    painter.setBrush(background_rect_gradient)
    painter.setPen(QPen(background_rect_gradient, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    painter.drawPath(rectPath)
    # 先画一个外圆
    background_arc_gradient = QConicalGradient(50, 50, 91)
    background_arc_gradient.setColorAt(0, QColor(main_object.line_color, main_object.line_color, main_object.line_color, 50))
    background_arc_gradient.setColorAt(1, QColor(main_object.line_color, main_object.line_color, main_object.line_color, 50))
    main_object.background_arc_pen = QPen()
    main_object.background_arc_pen.setBrush(background_arc_gradient)  # 设置画刷渐变效果
    main_object.background_arc_pen.setWidth(5)
    main_object.background_arc_pen.setCapStyle(Qt.RoundCap)
    painter.setPen(main_object.background_arc_pen)
    painter.drawArc(QtCore.QRectF(30 + left_x + 12, 17 + top_y, 120, 120), 0, 360*16)  # 画外圆
    # 再画一个内圆
    gradient = QConicalGradient(50, 50, 91)
    gradient.setColorAt(0, QColor(main_object.text_color))
    gradient.setColorAt(1, QColor(main_object.text_color))
    main_object.pen = QPen()
    main_object.pen.setBrush(gradient)  # 设置画刷渐变效果
    main_object.pen.setWidth(5)
    main_object.pen.setCapStyle(Qt.RoundCap)
    painter.setPen(main_object.pen)
    rotate_angle = 360 * main_object.schedule / main_object.drinking_count
    painter.drawArc(QtCore.QRectF(30 + left_x + 12, 17 + top_y, 120, 120), (90 - 0) * 16, int(-rotate_angle * 16))  # 画圆环
    # 提示文字
    font = QtGui.QFont()
    font.setFamily("思源黑体")
    font.setPointSize(11)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(QColor(main_object.text_color))
    if main_object.view_message == "positive":
        # 显示进度条当前进度(正着数)
        painter.drawText(QtCore.QRectF(left_x + 12, top_y, 181, 154),
                         Qt.AlignCenter, "今天第%d杯水" % main_object.schedule)
    else:
        if int(main_object.drinking_count - main_object.schedule) > 0:
            # 显示进度条当前进度(倒着数)
            painter.drawText(QtCore.QRectF(left_x + 12, top_y, 181, 154),
                             Qt.AlignCenter, "还有%d杯水" % int(main_object.drinking_count - main_object.schedule))
        elif int(main_object.drinking_count - main_object.schedule) == 0:
            # 显示进度条当前进度(倒着数)
            painter.drawText(QtCore.QRectF(left_x + 12, top_y, 181, 154),
                             Qt.AlignCenter, "%d杯水目标完成" % int(main_object.drinking_count))
        else:
            # 显示进度条当前进度(正着数)
            painter.drawText(QtCore.QRectF(left_x + 12, top_y, 181, 154),
                             Qt.AlignCenter, "今天第%d杯水" % main_object.schedule)
    # 画图完成，更新
    main_object.update()
