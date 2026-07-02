from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QVBoxLayout,
)

from core.statistics import StatisticsResult


class InfoPanel(QGroupBox):
    """
    GPX 정보 표시 패널
    """

    def __init__(self):
        super().__init__("GPX Information")

        layout = QVBoxLayout()

        self.lbl_file = QLabel("File :")
        self.lbl_tracks = QLabel("Tracks :")
        self.lbl_segments = QLabel("Segments :")
        self.lbl_points = QLabel("Track Points :")
        self.lbl_distance = QLabel("Distance :")
        self.lbl_min = QLabel("Min Elevation :")
        self.lbl_max = QLabel("Max Elevation :")
        self.lbl_up = QLabel("Total Ascent :")
        self.lbl_down = QLabel("Total Descent :")

        layout.addWidget(self.lbl_file)
        layout.addWidget(self.lbl_tracks)
        layout.addWidget(self.lbl_segments)
        layout.addWidget(self.lbl_points)
        layout.addSpacing(10)

        layout.addWidget(self.lbl_distance)
        layout.addWidget(self.lbl_min)
        layout.addWidget(self.lbl_max)
        layout.addWidget(self.lbl_up)
        layout.addWidget(self.lbl_down)

        layout.addStretch()

        self.setLayout(layout)

    def clear(self):

        self.lbl_file.setText("File :")
        self.lbl_tracks.setText("Tracks :")
        self.lbl_segments.setText("Segments :")
        self.lbl_points.setText("Track Points :")
        self.lbl_distance.setText("Distance :")
        self.lbl_min.setText("Min Elevation :")
        self.lbl_max.setText("Max Elevation :")
        self.lbl_up.setText("Total Ascent :")
        self.lbl_down.setText("Total Descent :")

    def update_information(
        self,
        filename: str,
        track_count: int,
        segment_count: int,
        stats: StatisticsResult,
    ):

        self.lbl_file.setText(f"File : {filename}")
        self.lbl_tracks.setText(f"Tracks : {track_count}")
        self.lbl_segments.setText(f"Segments : {segment_count}")
        self.lbl_points.setText(f"Track Points : {stats.point_count}")

        self.lbl_distance.setText(
            f"Distance : {stats.distance / 1000:.2f} km"
        )

        self.lbl_min.setText(
            f"Min Elevation : {stats.min_ele:.1f} m"
        )

        self.lbl_max.setText(
            f"Max Elevation : {stats.max_ele:.1f} m"
        )

        self.lbl_up.setText(
            f"Total Ascent : {stats.ascent:.1f} m"
        )

        self.lbl_down.setText(
            f"Total Descent : {stats.descent:.1f} m"
        )