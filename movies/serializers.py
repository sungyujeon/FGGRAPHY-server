from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Movie, Genre, Genre_User, BelongsToCollection, ProductionCompany, ProductionCountry, SpokenLanguage, Review, Comment, Genre, Collection

User = get_user_model()

class UserSerailizaer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

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

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    belongs_to_collection = BelongsToCollectionSerializer(read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    production_countries = ProductionCountrySerializer(many=True, read_only=True)
    spoken_languages = SpokenLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)

class ReviewListSerializer(serializers.ModelSerializer):
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user', 'like_users', 'like_users_count')

class ReviewSerializer(serializers.ModelSerializer):
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user', 'like_users',)

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        exclude = ('movies',)

class GenreListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        exclude = ('movies',)

class GenreUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre_User
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ('user', 'movies', 'like_users',)

class CollectionListSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(many=True, read_only=True)
    class Meta:
        model = Collection
        fields = '__all__'