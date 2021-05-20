from rest_framework import serializers
from .models import Movie, Genre, BelongsToCollection, ProductionCompany, ProductionCountry, SpokenLanguage

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('movies',)

class BelongsToCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BelongsToCollection
        exclude = ('movies',)

class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        exclude = ('movies',)

class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        exclude = ('movies',)

class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        exclude = ('movies',)


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    belongs_to_collection = BelongsToCollectionSerializer(read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    production_countries = ProductionCountrySerializer(many=True, read_only=True)
    spoken_languages = SpokenLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class TopRatedMovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    belongs_to_collection = BelongsToCollectionSerializer(read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    production_countries = ProductionCountrySerializer(many=True, read_only=True)
    spoken_languages = SpokenLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'