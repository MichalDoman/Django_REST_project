from rest_framework import serializers

from movielist.models import Movie
from .models import Cinema, Screening


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        view_name="movie",
        lookup_field="pk",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cinema
        fields = ['id', 'name', 'city', 'movies']


class ScreeningSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="title", queryset=Movie.objects.all())
    cinema = serializers.SlugRelatedField(slug_field="name", queryset=Cinema.objects.all())

    class Meta:
        model = Screening
        fields = ['movie', 'cinema', 'date']
