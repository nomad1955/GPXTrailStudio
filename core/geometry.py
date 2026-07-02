from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS = 6371000.0  # meters


class Geometry:
    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        """
        Haversine distance (meters)
        """

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return EARTH_RADIUS * c

    @staticmethod
    def point_distance(p1, p2):
        """
        두 TrackPoint 사이의 거리(m)
        """

        return Geometry.distance(
            p1.lat,
            p1.lon,
            p2.lat,
            p2.lon,
        )

    @staticmethod
    def cumulative_distance(points):
        """
        누적거리 계산

        반환값:
            [0.0, 12.3, 25.7, 40.8, ...]
        """

        if not points:
            return []

        distances = [0.0]
        total = 0.0

        for i in range(1, len(points)):
            total += Geometry.point_distance(points[i - 1], points[i])
            distances.append(total)

        return distances