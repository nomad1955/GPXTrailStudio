from pathlib import Path
import json

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineSettings,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class DebugPage(QWebEnginePage):

    def javaScriptConsoleMessage(
        self,
        level,
        message,
        lineNumber,
        sourceID,
    ):
        print(f"[JS] {message}")


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()

        self.document = None
        self.points = []

        page = DebugPage(self)
        self.setPage(page)

        settings = self.settings()

        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled,
            True,
        )

        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            True,
        )

        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
            True,
        )

        self.loadFinished.connect(self.on_loaded)

        self.load_map()

    # ---------------------------------------------------------

    def load_map(self):

        project_root = Path(__file__).resolve().parent.parent

        html = project_root / "web" / "map.html"

        print("Loading :", html)
        print("Exists :", html.exists())

        self.load(QUrl.fromLocalFile(str(html)))

    # ---------------------------------------------------------

    def on_loaded(self, ok):

        print("Map Loaded :", ok)

    # ---------------------------------------------------------

    def run_js(self, script):

        self.page().runJavaScript(script)

    # ---------------------------------------------------------

    def set_document(self, document):

        self.document = document

        self.points = []

        coords = []

        for track in document.tracks:

            for segment in track.segments:

                for point in segment.points:

                    if point.elevation is None:
                        continue

                    self.points.append(point)

                    coords.append(
                        [point.lat, point.lon]
                    )

        if len(coords) < 2:
            return

        js = f"showTrack({json.dumps(coords)});"

        self.run_js(js)

        print("Track :", len(coords))

    # ---------------------------------------------------------

    def move_to_point(self, index):

        if index < 0:
            return

        if index >= len(self.points):
            return

        p = self.points[index]

        js = (
            f"moveMarker({p.lat}, {p.lon});"
        )

        self.run_js(js)