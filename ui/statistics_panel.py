from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QGroupBox,
    QVBoxLayout
)


class StatisticsPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.distance = QLabel("-")
        self.uphill = QLabel("-")
        self.downhill = QLabel("-")
        self.max_ele = QLabel("-")
        self.min_ele = QLabel("-")
        self.track_count = QLabel("-")
        self.point_count = QLabel("-")

        form = QFormLayout()
        form.addRow("거리", self.distance)
        form.addRow("상승고도", self.uphill)
        form.addRow("하강고도", self.downhill)
        form.addRow("최고고도", self.max_ele)
        form.addRow("최저고도", self.min_ele)
        form.addRow("Track 수", self.track_count)
        form.addRow("Point 수", self.point_count)

        group = QGroupBox("GPX 정보")
        group.setLayout(form)

        layout = QVBoxLayout()
        layout.addWidget(group)
        layout.addStretch()

        self.setLayout(layout)

    def clear(self):

        self.distance.setText("-")
        self.uphill.setText("-")
        self.downhill.setText("-")
        self.max_ele.setText("-")
        self.min_ele.setText("-")
        self.track_count.setText("-")
        self.point_count.setText("-")

    def set_statistics(
        self,
        distance,
        uphill,
        downhill,
        max_ele,
        min_ele,
        track_count,
        point_count
    ):

        self.distance.setText(f"{distance:.2f} km")
        self.uphill.setText(f"{uphill:.0f} m")
        self.downhill.setText(f"{downhill:.0f} m")
        self.max_ele.setText(f"{max_ele:.0f} m")
        self.min_ele.setText(f"{min_ele:.0f} m")
        self.track_count.setText(str(track_count))
        self.point_count.setText(f"{point_count:,}")