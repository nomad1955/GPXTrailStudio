from dataclasses import dataclass

from core.geometry import Geometry


@dataclass
class ProfilePoint:
    """
    고도표에 사용할 점
    """
    distance: float      # 누적거리(m)
    elevation: float     # 고도(m)


class ProfileBuilder:

    @staticmethod
    def build(document):
        """
        GPXDocument → ProfilePoint 리스트
        """

        profile = []

        total_distance = 0.0

        for track in document.tracks:

            for segment in track.segments:

                previous = None

                for point in segment.points:

                    if point.elevation is None:
                        continue

                    if previous is not None:
                        total_distance += Geometry.point_distance(
                            previous,
                            point,
                        )

                    profile.append(
                        ProfilePoint(
                            distance=total_distance,
                            elevation=point.elevation,
                        )
                    )

                    previous = point

        return profile

    @staticmethod
    def downsample(profile, max_points):
        """
        화면 폭에 맞게 Profile을 축소한다.

        profile : ProfilePoint 리스트
        max_points : 화면에 그릴 최대 점수
        """

        if len(profile) <= max_points:
            return profile

        step = len(profile) / max_points

        result = []

        index = 0.0

        while int(index) < len(profile):

            result.append(profile[int(index)])

            index += step

        return result