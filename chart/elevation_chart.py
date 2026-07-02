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

            self.update()

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

        painter.setPen(QPen(QColor(220, 220, 220), 1))

        for i in range(6):
            y = margin + i * h / 5
            painter.drawLine(margin, y, margin + w, y)

        # ---------------- Profile ----------------

        polygon = QPolygonF()

        for point, dist in zip(self.points, self.distances):

            x = margin + (dist / total_distance) * w

            y = margin + (
                (max_ele - point.elevation)
                / (max_ele - min_ele)
            ) * h

            polygon.append(QPointF(x, y))

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(30, 80, 180), 2))
        painter.drawPolyline(polygon)

        # ---------------- Hover Cursor ----------------

        if self.hover_index >= 0:

            dist = self.distances[self.hover_index]

            x = margin + (dist / total_distance) * w

            painter.setPen(QPen(Qt.red, 1))

            painter.drawLine(
                int(x),
                margin,
                int(x),
                margin + h
            )

        # ---------------- Border ----------------

        painter.setPen(QPen(Qt.black, 1))
        painter.drawRect(margin, margin, w, h)