from rest_framework import serializers


class ReleaseYearValidator:
    '''Валидатор для года выпуска'''

    def __init__(self, min_year=1900, max_year=9999):
        self.min_year = min_year
        self.max_year = max_year

    def __call__(self, value):
        if not (self.min_year <= value <= self.max_year):
            raise serializers.ValidationError(
                f"Release year must be between {self.min_year} and {self.max_year}."
            )


class TrackNumberValidator:
    '''Валидатор для номера трека'''

    def __call__(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Track number must be a positive integer."
            )
