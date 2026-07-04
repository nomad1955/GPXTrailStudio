from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QWidget

from core.geometry import Geometry


class ElevationChart(QWidget):

    # 현재 마우스가 가리키는 Point 번호
    pointHovered = Signal(int)

    def __init__(self):
        super().__init__()

        self.points = []
        self.distances = []

        self.hover_index = -1
        self.zoom_start = -1
        self.zoom_end = -1
        self.zoom_mode = False

        self.setMinimumHeight(300)
        self.setMouseTracking(True)

    # ---------------------------------------------------------

    def set_document(self, document):

        self.points = []
        self.distances = []
        self.hover_index = -1

        if document is None:
            self.update()
            return

        total_distance = 0.0

        for track in document.tracks:
            for segment in track.segments:

                prev = None

                for point in segment.points:

                    if point.elevation is None:
                        continue

                    self.points.append(point)

                    if prev is None:
                        self.distances.append(total_distance)
                    else:
                        total_distance += Geometry.point_distance(prev, point)
                        self.distances.append(total_distance)

                    prev = point

        print("Points :", len(self.points))
        print("Distances :", len(self.distances))

        if self.distances:
            print("Total Distance :", self.distances[-1])

        self.update()

    # ---------------------------------------------------------

    def mouseMoveEvent(self, event):

        if len(self.points) < 2:
            return

        margin = 40
        width = self.width() - margin * 2

        x = event.position().x()

        if x < margin:
            index = 0

        elif x > margin + width:
            index = len(self.points) - 1

        else:

            ratio = (x - margin) / width

            index = int(ratio * (len(self.points) - 1))

        if index != self.hover_index:

            self.hover_index = index

            self.pointHovered.emit(index)

            if self.zoom_mode:
                self.zoom_end = index

            self.update()

    # ---------------------------------------------------------

    def mousePressEvent(self, event):

        if len(self.points) < 2:
            return

        margin = 40
        w = self.width() - margin * 2

        x = event.position().x()

        ratio = (x - margin) / w
        ratio = max(0.0, min(1.0, ratio))

        index = int(ratio * (len(self.points) - 1))

        self.zoom_start = index
        self.zoom_end = index
        self.zoom_mode = True

    # ---------------------------------------------------------

    def mouseReleaseEvent(self, event):

        self.zoom_mode = False

    # ---------------------------------------------------------

    def leaveEvent(self, event):

        self.hover_index = -1
        self.update()

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

        if len(self.points) < 2:
            return

        margin = 40

        w = self.width() - margin * 2
        h = self.height() - margin * 2

        elevations = [p.elevation for p in self.points]

        min_ele = min(elevations)
        max_ele = max(elevations)

        if max_ele <= min_ele:
            max_ele = min_ele + 1

        total_distance = self.distances[-1]

        if total_distance <= 0:
            return

        # ---------------- Grid ----------------

        painter.setRenderHint(QPainter.Antialiasing)

        # 배경
        painter.fillRect(
            margin,
            margin,
            w,
            h,
            QColor(248, 248, 248)
        )

        # 가로 Grid
        painter.setPen(QPen(QColor(225, 225, 225), 1))

        # ---------------- Grid ----------------

        painter.setPen(QPen(QColor(220,220,220),1))

        for i in range(6):

            y = margin + i*h/5

            painter.drawLine(
                margin,
                y,
                margin+w,
                y
            )

        # ---------------- Profile ----------------

        profile = QPolygonF()

        for point, dist in zip(self.points, self.distances):

            x = margin + (dist / total_distance) * w

            y = margin + (
                (max_ele - point.elevation)
                / (max_ele - min_ele)
            ) * h

            profile.append(QPointF(x, y))

        # Area Fill
        fill = QPolygonF(profile)
        fill.append(QPointF(margin + w, margin + h))
        fill.append(QPointF(margin, margin + h))

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(120, 180, 255, 110))
        painter.drawPolygon(fill)

        painter.setPen(
            QPen(
                QColor(20,70,170),
                2.5,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin
            )
        )
        painter.setBrush(Qt.NoBrush)
        painter.drawPolyline(profile)

        # ---------------- Hover Cursor ----------------

        if self.hover_index >= 0:

            point = self.points[self.hover_index]
            dist = self.distances[self.hover_index]

            x = margin + (dist / total_distance) * w

            y = margin + (
                (max_ele - point.elevation)
                / (max_ele - min_ele)
            ) * h

            painter.setPen(QPen(Qt.red, 1))
            painter.drawLine(int(x), margin, int(x), margin + h)

            painter.setBrush(Qt.red)
            painter.drawEllipse(QPointF(x, y), 4, 4)

            painter.setPen(Qt.black)

            text = f"{dist/1000:.2f} km\n{point.elevation:.0f} m"

            painter.drawText(
                int(x + 8),
                int(y - 8),
                text
            )
        painter.setBrush(Qt.NoBrush)

        # ---------------- Border ----------------

        # ---------------- X Axis ----------------

        import math

        max_km = total_distance / 1000.0

        if max_km <= 5:
            tick_step = 0.5
        elif max_km <= 15:
            tick_step = 1
        elif max_km <= 40:
            tick_step = 2
        elif max_km <= 80:
            tick_step = 5
        elif max_km <= 150:
            tick_step = 10
        else:
            tick_step = 20

        max_km = total_distance / 1000.0

        tick = 0.0

        painter.setPen(QPen(Qt.black, 1))

        while tick <= max_km + 0.001:

            x = margin + (tick / max_km) * w

            painter.drawLine(
                int(x),
                margin + h,
                int(x),
                margin + h + 5
            )

            label = f"{tick:g}"

            painter.drawText(
                int(x - 10),
                margin + h + 20,
                label
            )

            tick += tick_step

        painter.drawText(
            margin + w - 18,
            margin + h + 38,
            "km"
        )
        
        # ---------------- Y Axis ----------------

        import math

        step = math.ceil((max_ele - min_ele) / 5 / 100) * 100

        top = math.ceil(max_ele / step) * step
        bottom = math.floor(min_ele / step) * step

        count = int((top - bottom) / step)

        for i in range(count + 1):

            ele = top - i * step

            y = margin + (top - ele) / (top - bottom) * h

            painter.drawLine(
                margin - 5,
                int(y),
                margin,
                int(y)
            )

            painter.drawText(
                5,
                int(y + 5),
                f"{int(ele)}"
            )

        painter.drawText(5, 20, "m")

        painter.drawRect(margin, margin, w, h)