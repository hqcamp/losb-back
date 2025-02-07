from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework import serializers


def validate_location(location):
    """
    Validates the location field, which should be a JSON object with 'latitude' and 'longitude' keys.
    """
    expected_decimal_places = settings.COORD_DECIMAL_PLACES

    if not isinstance(location, dict):
        raise ValidationError("The 'location' field must be a JSON object.")

    required_keys = {"latitude", "longitude"}
    if set(location.keys()) != required_keys:
        raise ValidationError(f"The 'location' field must contain the keys: "
                              f"{required_keys}. Received: {location.keys()}")

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if not isinstance(latitude, float) or not isinstance(longitude, float):
        raise ValidationError("Both 'latitude' and 'longitude' must be floating-point numbers.")

    if not (-90 <= latitude <= 90):
        raise ValidationError("The 'latitude' value must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise ValidationError("The 'longitude' value must be between -180 and 180.")

    def check_decimal_places(value):
        str_value = str(value)
        integer_part, decimal_part = str_value.split('.')
        return len(decimal_part) <= expected_decimal_places

    if not check_decimal_places(latitude) or not check_decimal_places(longitude):
        raise ValidationError(f"Coordinates must have at most {expected_decimal_places} decimal places.")


def validate_file_size(file, max_size_mb=settings.MAX_FILE_SIZE_MB):
    """
    Validates that the uploaded file does not exceed the specified size limit.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValidationError(f"The file size must not exceed {max_size_mb} MB.")


def validate_location_field(value):
    if value is None:
        raise serializers.ValidationError("The 'location' field is required.")
    return value
