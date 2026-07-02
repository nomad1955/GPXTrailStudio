import xml.etree.ElementTree as ET

from gpx.model import (
    GPXDocument,
    Track,
    TrackSegment,
    TrackPoint,
)


class GPXLoader:
    """GPX 파일을 읽어 GPXDocument 객체를 생성"""

    def load(self, filename: str) -> GPXDocument:

        tree = ET.parse(filename)
        root = tree.getroot()

        # Namespace 처리
        namespace = {}
        prefix = ""

        if root.tag.startswith("{"):
            uri = root.tag.split("}")[0][1:]
            namespace["gpx"] = uri
            prefix = "gpx:"

        document = GPXDocument()
        document.creator = root.attrib.get("creator", "")
        document.version = root.attrib.get("version", "1.1")

        # Track
        for trk_node in root.findall(f"{prefix}trk", namespace):

            track = Track()

            name_node = trk_node.find(f"{prefix}name", namespace)
            if name_node is not None and name_node.text:
                track.name = name_node.text

            # Segment
            for seg_node in trk_node.findall(f"{prefix}trkseg", namespace):

                segment = TrackSegment()

                # TrackPoint
                for pt_node in seg_node.findall(f"{prefix}trkpt", namespace):

                    lat = float(pt_node.attrib["lat"])
                    lon = float(pt_node.attrib["lon"])

                    ele = None
                    ele_node = pt_node.find(f"{prefix}ele", namespace)
                    if ele_node is not None and ele_node.text:
                        try:
                            ele = float(ele_node.text)
                        except ValueError:
                            ele = None

                    time = None
                    time_node = pt_node.find(f"{prefix}time", namespace)
                    if time_node is not None:
                        time = time_node.text

                    point = TrackPoint(
                        lat=lat,
                        lon=lon,
                        ele_original=ele,
                        time=time,
                    )

                    segment.points.append(point)

                track.segments.append(segment)

            document.tracks.append(track)

        return document