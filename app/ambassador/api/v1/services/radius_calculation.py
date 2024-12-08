from geopy.distance import distance as geopy_distance


class CoordinatesService:
    @staticmethod
    def calculate_radius(queryset, latitude: float, longitude: float, radius: float):
        filtered_videos = (
            video.id for video in queryset
            if geopy_distance(
                (video.location['latitude'], video.location['longitude']),
                (latitude, longitude)
            ).km <= radius
        )

        return queryset.filter(id__in=filtered_videos)
