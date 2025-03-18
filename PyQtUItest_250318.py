from __future__ import annotations

import sys
from enum import IntEnum

from PySide6.QtCore import (Property, QEasingCurve, QObject, QPropertyAnimation,
                            QPointF, QRectF, Qt, QSize, QUrl)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import (QBrush, QColor, QIcon, QLinearGradient, QPainter,
                           QPainterPath, QPixmap)
from PySide6.QtWidgets import (QApplication, QGraphicsPixmapItem, QGraphicsItem,
                               QGraphicsScene, QListWidgetItem, QWidget, QGroupBox,
                               QVBoxLayout, QLabel, QFormLayout, QDoubleSpinBox, QSizePolicy)

sys.path.append("c:/Users/USER/OneDrive/문서/GitHub/opencv/resume/opencv")
from ui_form import Ui_Form


class PathType(IntEnum):
    LINEAR_PATH = 0
    CIRCLE_PATH = 1


class Animation(QPropertyAnimation):
    def __init__(self, target, prop):
        super().__init__(target, prop)
        self.set_path_type(PathType.LINEAR_PATH)

    def set_path_type(self, pathType):
        self._pathType = pathType
        self._path = QPainterPath()

    def updateCurrentTime(self, currentTime):
        if self._pathType == PathType.CIRCLE_PATH:
            if self._path.isEmpty():
                end = self.endValue()
                start = self.startValue()
                self._path.moveTo(start)
                self._path.addEllipse(QRectF(start, end))

            dura = self.duration()
            if dura == 0:
                progress = 1.0
            else:
                progress = (((currentTime - 1) % dura) + 1) / float(dura)

            eased_progress = self.easingCurve().valueForProgress(progress)
            if eased_progress > 1.0:
                eased_progress -= 1.0
            elif eased_progress < 0:
                eased_progress += 1.0

            pt = self._path.pointAtPercent(eased_progress)
            self.updateCurrentValue(pt)
            self.valueChanged.emit(pt)
        else:
            super(Animation, self).updateCurrentTime(currentTime)


class Pixmap(QObject):
    def __init__(self, pix):
        super().__init__()
        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    def get_pos(self):
        return self.pixmap_item.pos()

    pos = Property(QPointF, get_pos, set_pos)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ui = Ui_Form()
        self._ui.setupUi(self)

        # QGraphicsScene 생성
        self._scene = QGraphicsScene()
        self._ui.graphicsView.setScene(self._scene)

        # 아이콘 크기 설정
        self._iconSize = self._ui.easingCurvePicker.iconSize()
        if (not self._iconSize.isValid() or 
            self._iconSize.width() < 64 or 
            self._iconSize.height() == 0):
            self._iconSize = QSize(64, 64)

        # EasingCurvePicker 설정 및 기본값 세팅
        self._ui.easingCurvePicker.setIconSize(self._iconSize)
        dummy = QEasingCurve()
        self._ui.periodSpinBox.setValue(dummy.period())
        self._ui.amplitudeSpinBox.setValue(dummy.amplitude())
        self._ui.overshootSpinBox.setValue(dummy.overshoot())

        # 시그널 연결
        self._ui.easingCurvePicker.currentRowChanged.connect(self.curve_changed)
        self._ui.buttonGroup.idClicked.connect(self.path_changed)
        self._ui.periodSpinBox.valueChanged.connect(self.period_changed)
        self._ui.amplitudeSpinBox.valueChanged.connect(self.amplitude_changed)
        self._ui.overshootSpinBox.valueChanged.connect(self.overshoot_changed)

        # -------------------------------
        # (1) "Video" 그룹박스를 만들고, QWebEngineView를 추가
        # -------------------------------
        self.imageGroupBox = QGroupBox("Video", self)
        self.imageLayout = QVBoxLayout(self.imageGroupBox)

        # QWebEngineView 생성 후, 원하는 URL (유튜브) 로드
        self.videoView = QWebEngineView()
        self.videoView.load(QUrl("https://www.youtube.com/watch?v=4mLCCC1cbqM"))
        self.imageLayout.addWidget(self.videoView)
        self.videoView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoView.setMinimumSize(800, 450)

        self.imageGroupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 레이아웃에 "Video" 그룹박스 배치
        self._ui.gridLayout.addWidget(self.imageGroupBox, 2, 0, 1, 2)

        # -------------------------------
        # (2) Speed라는 새 속성
        # -------------------------------
        self.speedLabel = QLabel("Speed", self._ui.groupBox)
        self.speedSpinBox = QDoubleSpinBox(self._ui.groupBox)
        self.speedSpinBox.setRange(0.1, 10.0)
        self.speedSpinBox.setSingleStep(0.1)
        self.speedSpinBox.setValue(1.0)
        self.speedSpinBox.valueChanged.connect(self.speed_changed)
        self._ui.formLayout.addRow(self.speedLabel, self.speedSpinBox)

        # gridLayout의 특정 행(2번 행)에 Stretch 부여
        self._ui.gridLayout.setRowStretch(2, 1)
        # 필요하면 위쪽 행은 stretch 0
        self._ui.gridLayout.setRowStretch(0, 0)
        self._ui.gridLayout.setRowStretch(1, 0)

        # -------------------------------
        # Pixmap 아이템 생성 및 애니메이션
        # -------------------------------
        pixmap = QPixmap(r"C:\hachuping250318.png")
        self._item = Pixmap(pixmap)
        self._scene.addItem(self._item.pixmap_item)

        self._anim = Animation(self._item, b'pos')
        self._anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        self.create_curve_icons()
        self._ui.easingCurvePicker.setCurrentRow(0)
        self.start_animation()

    def create_curve_icons(self):
        pix = QPixmap(self._iconSize)
        gradient = QLinearGradient(0, 0, 0, self._iconSize.height())
        gradient.setColorAt(0.0, QColor(240, 240, 240))
        gradient.setColorAt(1.0, QColor(224, 224, 224))
        brush = QBrush(gradient)
        curve_types = [(f"QEasingCurve.{e.name}", e) for e in QEasingCurve.Type if e.value <= 40]
        painter = QPainter()
        for curve_name, curve_type in curve_types:
            pix.fill(Qt.GlobalColor.transparent)
            painter.begin(pix)
            painter.fillRect(pix.rect(), brush)
            curve = QEasingCurve(curve_type)
            painter.setPen(QColor(0, 0, 255, 64))
            x_axis = self._iconSize.height() / 1.5
            y_axis = self._iconSize.width() / 3.0
            painter.drawLine(0, x_axis, self._iconSize.width(), x_axis)
            painter.drawLine(y_axis, 0, y_axis, self._iconSize.height())
            curve_scale = self._iconSize.height() / 2.0
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(Qt.GlobalColor.red)
            start = QPointF(y_axis, x_axis - curve_scale * curve.valueForProgress(0))
            painter.drawRect(start.x() - 1, start.y() - 1, 3, 3)
            painter.setBrush(Qt.GlobalColor.blue)
            end = QPointF(y_axis + curve_scale, x_axis - curve_scale * curve.valueForProgress(1))
            painter.drawRect(end.x() - 1, end.y() - 1, 3, 3)
            curve_path = QPainterPath()
            curve_path.moveTo(start)
            t = 0.0
            while t <= 1.0:
                to = QPointF(y_axis + curve_scale * t, x_axis - curve_scale * curve.valueForProgress(t))
                curve_path.lineTo(to)
                t += 1.0 / curve_scale
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.strokePath(curve_path, QColor(32, 32, 32))
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            painter.end()
            item = QListWidgetItem()
            item.setIcon(QIcon(pix))
            item.setText(curve_name)
            self._ui.easingCurvePicker.addItem(item)

    def start_animation(self):
        self._anim.setStartValue(QPointF(0, 0))
        self._anim.setEndValue(QPointF(100, 100))
        self._anim.setDuration(2000)
        self._anim.setLoopCount(-1)
        self._anim.start()

    def curve_changed(self, row):
        curve_type = QEasingCurve.Type(row)
        self._anim.setEasingCurve(curve_type)
        self._anim.setCurrentTime(0)
        is_elastic = (curve_type.value >= QEasingCurve.Type.InElastic.value and curve_type.value <= QEasingCurve.Type.OutInElastic.value)
        is_bounce = (curve_type.value >= QEasingCurve.Type.InBounce.value and curve_type.value <= QEasingCurve.Type.OutInBounce.value)
        overshoot = (curve_type.value >= QEasingCurve.Type.InBack.value and curve_type.value <= QEasingCurve.Type.OutInBack.value)
        self._ui.periodSpinBox.setEnabled(is_elastic)
        self._ui.amplitudeSpinBox.setEnabled(is_elastic or is_bounce)
        self._ui.overshootSpinBox.setEnabled(overshoot)

    def path_changed(self, index):
        self._anim.set_path_type(index)

    def period_changed(self, value):
        curve = self._anim.easingCurve()
        curve.setPeriod(value)
        self._anim.setEasingCurve(curve)

    def amplitude_changed(self, value):
        curve = self._anim.easingCurve()
        curve.setAmplitude(value)
        self._anim.setEasingCurve(curve)

    def overshoot_changed(self, value):
        curve = self._anim.easingCurve()
        curve.setOvershoot(value)
        self._anim.setEasingCurve(curve)

    def speed_changed(self, value):
        base_duration = 2000
        new_duration = int(base_duration / value)
        self._anim.setDuration(new_duration)
        self._anim.setCurrentTime(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())