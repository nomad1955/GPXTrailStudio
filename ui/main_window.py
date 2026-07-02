from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QSplitter,
)

from gpx.loader import GPXLoader
from core.statistics import GPXStatistics

from ui.info_panel import InfoPanel
from ui.map_widget import MapWidget
from chart.elevation_chart import ElevationChart


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.document = None

        self.setWindowTitle("GPX Trail Studio V0.4.2")
        self.resize(1500, 900)

        self.create_menu()
        self.create_ui()

        self.statusBar().showMessage("Ready")

    # ---------------------------------------------------------
    # Menu
    # ---------------------------------------------------------

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = QAction("Open GPX...", self)
        open_action.triggered.connect(self.open_gpx)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        menu.addMenu("View")
        menu.addMenu("Tools")
        menu.addMenu("Help")

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_ui(self):

        self.info_panel = InfoPanel()

        self.map_widget = MapWidget()

        self.chart = ElevationChart()

        # ★ 고도표 → 지도 연동
        self.chart.pointHovered.connect(
            self.map_widget.move_to_point
        )

        right_splitter = QSplitter(Qt.Vertical)

        right_splitter.addWidget(self.map_widget)
        right_splitter.addWidget(self.chart)

        right_splitter.setStretchFactor(0, 3)
        right_splitter.setStretchFactor(1, 2)

        main_splitter = QSplitter(Qt.Horizontal)

        main_splitter.addWidget(self.info_panel)
        main_splitter.addWidget(right_splitter)

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)

        self.setCentralWidget(main_splitter)

    # ---------------------------------------------------------
    # Open GPX
    # ---------------------------------------------------------

    def open_gpx(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open GPX",
            "",
            "GPX Files (*.gpx)"
        )

        if not filename:
            return

        loader = GPXLoader()

        try:
            self.document = loader.load(filename)

        except Exception as e:
            self.statusBar().showMessage(str(e))
            return

        stats = GPXStatistics.calculate(self.document)

        track_count = len(self.document.tracks)

        segment_count = sum(
            len(track.segments)
            for track in self.document.tracks
        )

        # 정보 패널
        self.info_panel.update_information(
            filename,
            track_count,
            segment_count,
            stats,
        )

        # 지도
        self.map_widget.set_document(self.document)

        # 고도표
        self.chart.set_document(self.document)

        self.statusBar().showMessage(
            f"Tracks : {track_count}   "
            f"Segments : {segment_count}   "
            f"Points : {stats.point_count}"
        )