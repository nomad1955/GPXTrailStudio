from dataclasses import dataclass

from core.geometry import Geometry


@dataclass
class StatisticsResult:
    point_count: int = 0

    distance: float = 0.0

    min_ele: float = 0.0
    max_ele: float = 0.0

    ascent: float = 0.0
    descent: float = 0.0


class GPXStatistics:

    @staticmethod
    def calculate(document):

        result = StatisticsResult()

        elevations = []

        previous_point = None
        previous_ele = None

        for track in document.tracks:

            for segment in track.segments:

                for point in segment.points:

                    result.point_count += 1

                    if point.elevation is not None:
                        elevations.append(point.elevation)

                    if previous_point is not None:

                        result.distance += Geometry.point_distance(
                            previous_point,
                            point,
                        )

                    if (
                        previous_ele is not None
                        and point.elevation is not None
                    ):

                        diff = point.elevation - previous_ele

                        # 비정상적인 변화는 무시 (임시)
                        if abs(diff) < 100:

                            if diff > 0:
                                result.ascent += diff
                            else:
                                result.descent += -diff

                    previous_point = point

                    if point.elevation is not None:
                        previous_ele = point.elevation

        if elevations:

            result.min_ele = min(elevations)
            result.max_ele = max(elevations)

        return result